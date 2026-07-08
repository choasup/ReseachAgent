#!/usr/bin/env python3
"""VLM 三模型对比 demo（在 vlmeval-molmo env 跑）。
- Molmo: 本机 transformers 加载一次（含 rocm_fix 补丁）
- Qwen/GLM: 代理本机 vLLM serve(18001/18002) 的 OpenAI 端点
网页 UI：拖图 + 问题 -> 三模型并行推理 -> 并排显示。
端口 7860，用 ssh -L 转发到本地浏览器访问。
"""
import os, sys, io, json, base64, tempfile, time, threading, urllib.request, traceback
from concurrent.futures import ThreadPoolExecutor
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from PIL import Image

BASE = "/home/tione/notebook/research/choasliu"          # 共享资源根（conda/hf_home/LMUData）
PROJ = os.path.dirname(os.path.abspath(__file__))        # 项目根（随本文件位置走，搬迁无需改）
HIST_PATH = os.path.join(PROJ, "demo_history.jsonl")
EX_PATH = os.path.join(PROJ, "examples.json")
HIST_LOCK = threading.Lock()
sys.path.insert(0, os.path.join(PROJ, "VLMEvalKit"))
os.environ.setdefault("HF_HOME", f"{BASE}/hf_home")
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HIP_VISIBLE_DEVICES", "2")   # 物理 Dev1（空闲）

QWEN_API = "http://127.0.0.1:18001/v1/chat/completions"
GLM_API = "http://127.0.0.1:18002/v1/chat/completions"

print("[demo] loading Molmo (transformers, ~1min) ...", flush=True)
from vlmeval.config import supported_VLM
MOLMO = supported_VLM["molmo-7B-D-0924"]()
print("[demo] Molmo ready.", flush=True)


def resize_data_uri(b64_or_uri, box=1280):
    raw = b64_or_uri.split(",", 1)[1] if b64_or_uri.startswith("data:") else b64_or_uri
    im = Image.open(io.BytesIO(base64.b64decode(raw))).convert("RGB")
    im.thumbnail((box, box))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    return im, "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def call_openai(api, model, data_uri, prompt, temp, max_tokens=512, extra=None):
    body = {"model": model, "max_tokens": max_tokens, "temperature": temp,
            "messages": [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": data_uri}},
                {"type": "text", "text": prompt}]}]}
    if extra:
        body.update(extra)
    req = urllib.request.Request(api, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    msg = d["choices"][0]["message"]
    out = (msg.get("content") or "").strip()
    rc = (msg.get("reasoning_content") or "").strip()
    return out, rc


def run_qwen(uri, prompt):
    try:
        out, _ = call_openai(QWEN_API, "Qwen3-VL-8B-Instruct", uri, prompt, 0.7,
                             extra={"top_p": 0.8})
        return {"answer": out, "think": ""}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def run_glm(uri, prompt):
    try:
        out, rc = call_openai(GLM_API, "GLM-4.1V-9B-Thinking", uri, prompt, 0.8, 1024,
                              extra={"top_p": 0.6})
        import re
        out = re.sub(r"</?answer>|<\|begin_of_box\|>|<\|end_of_box\|>", "", out).strip()
        return {"answer": out, "think": rc}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def run_molmo(img, prompt):
    try:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            img.save(f, "JPEG"); path = f.name
        ans = MOLMO.generate([path, prompt])
        os.unlink(path)
        return {"answer": str(ans).strip(), "think": ""}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


POOL = ThreadPoolExecutor(max_workers=3)


def thumb_uri(img, box=220):
    im = img.copy(); im.thumbnail((box, box))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=70)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def save_history(rec):
    try:
        with HIST_LOCK, open(HIST_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    except Exception:
        traceback.print_exc()


def load_history(limit=200):
    if not os.path.exists(HIST_PATH):
        return []
    with HIST_LOCK, open(HIST_PATH, encoding="utf-8") as f:
        lines = f.readlines()
    out = []
    for ln in lines[-limit:]:
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    out.reverse()   # 最新在前
    return out


def infer(image_uri, prompt):
    img, uri = resize_data_uri(image_uri)
    futs = {"qwen": POOL.submit(run_qwen, uri, prompt),
            "glm": POOL.submit(run_glm, uri, prompt),
            "molmo": POOL.submit(run_molmo, img, prompt)}
    res = {k: v.result() for k, v in futs.items()}
    rec = {"id": int(time.time() * 1000), "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
           "prompt": prompt, "thumb": thumb_uri(img), **res}
    save_history(rec)
    return {"result": res, "record": rec}


HTML = """<!doctype html><html lang=zh><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1"><title>VLM 三模型对比 demo</title>
<style>
:root{--bg:#0f1217;--card:#171b22;--ink:#e7eaef;--mut:#9aa3b0;--faint:#69727f;--line:#242a33;
--qwen:#17a897;--glm:#6f7ce8;--molmo:#dd6f6f;--mono:ui-monospace,Menlo,monospace;
--sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
@media(prefers-color-scheme:light){:root{--bg:#f5f6f8;--card:#fff;--ink:#14181f;--mut:#586070;
--faint:#8a929e;--line:#e4e7ec;--qwen:#0e9c8c;--glm:#5866d6;--molmo:#cc5a3c}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.5}
.wrap{max-width:1080px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:21px;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--mut);font-size:13px;margin:0 0 22px}
.panel{display:grid;grid-template-columns:300px 1fr;gap:18px;align-items:start}
@media(max-width:720px){.panel{grid-template-columns:1fr}}
#drop{border:1.5px dashed var(--line);border-radius:14px;background:var(--card);min-height:200px;
display:flex;align-items:center;justify-content:center;text-align:center;cursor:pointer;overflow:hidden;position:relative}
#drop.hi{border-color:var(--qwen)}#drop img{max-width:100%;max-height:340px;display:block}
#drop .ph{color:var(--faint);font-size:13px;padding:24px}
.controls{display:flex;flex-direction:column;gap:10px}
textarea{width:100%;background:var(--card);color:var(--ink);border:1px solid var(--line);border-radius:10px;
padding:11px 12px;font-family:var(--sans);font-size:14px;resize:vertical;min-height:80px}
.presets{display:flex;flex-wrap:wrap;gap:6px}
.presets button{background:transparent;border:1px solid var(--line);color:var(--mut);border-radius:20px;
padding:4px 11px;font-size:11.5px;cursor:pointer;font-family:var(--mono)}
.presets button:hover{border-color:var(--qwen);color:var(--ink)}
#run{background:var(--qwen);color:#fff;border:0;border-radius:10px;padding:12px;font-size:14px;font-weight:600;
cursor:pointer}#run:disabled{opacity:.5;cursor:default}
.results{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:22px}
@media(max-width:720px){.results{grid-template-columns:1fr}}
.rc{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 15px;border-top:3px solid var(--c)}
.rc h3{margin:0 0 3px;font-size:14px;display:flex;align-items:center;gap:7px}
.rc .dot{width:9px;height:9px;border-radius:50%;background:var(--c)}
.rc .t{font-family:var(--mono);font-size:10.5px;color:var(--faint);margin-bottom:9px}
.rc .ans{font-size:13.5px;white-space:pre-wrap;word-break:break-word;min-height:20px}
.rc .think{margin-top:10px;font-size:11.5px;color:var(--mut);border-top:1px dashed var(--line);padding-top:8px;
white-space:pre-wrap;max-height:160px;overflow:auto}
.rc .think summary{cursor:pointer;color:var(--faint);font-family:var(--mono);font-size:10.5px}
.rc.err .ans{color:#e8794f}
.spin{display:inline-block;width:13px;height:13px;border:2px solid var(--line);border-top-color:var(--c);
border-radius:50%;animation:s .7s linear infinite;vertical-align:-2px}
@keyframes s{to{transform:rotate(360deg)}}
#exwrap{margin-bottom:16px}
.exlabel{font-family:var(--mono);font-size:11px;color:var(--faint);margin-bottom:8px;letter-spacing:.04em}
#examples{display:flex;gap:10px;overflow-x:auto;padding-bottom:4px}
.excard{flex:none;width:96px;cursor:pointer;border:1px solid var(--line);border-radius:10px;overflow:hidden;
background:var(--card);transition:border-color .15s}
.excard:hover{border-color:var(--qwen)}
.excard img{width:96px;height:70px;object-fit:cover;display:block;background:var(--bg)}
.excard .exb{font-family:var(--mono);font-size:9.5px;color:var(--mut);padding:4px 6px;text-align:center;
white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.histhead{display:flex;align-items:baseline;gap:12px;margin:34px 0 14px;padding-bottom:8px;border-bottom:1px solid var(--line)}
.histhead h2{font-size:15px;margin:0;font-family:var(--mono)}
.histhead #hcount{color:var(--faint);font-weight:400}
.histnote{font-size:11.5px;color:var(--faint);margin-left:auto;font-family:var(--mono)}
.hempty{color:var(--faint);font-size:13px;padding:24px 0;text-align:center}
.hcard{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:13px 15px;margin-bottom:12px}
.hhead{display:flex;gap:12px;align-items:center;margin-bottom:10px}
.hhead img{width:56px;height:56px;object-fit:cover;border-radius:8px;flex:none;background:var(--bg)}
.hmeta{min-width:0}.hq{font-size:13.5px;font-weight:600;word-break:break-word}
.hts{font-family:var(--mono);font-size:10.5px;color:var(--faint);margin-top:2px}
.hbody{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
@media(max-width:720px){.hbody{grid-template-columns:1fr}}
.hcol{border-left:2px solid var(--c);padding-left:9px}
.hm{font-family:var(--mono);font-size:11px;color:var(--mut);display:flex;align-items:center;gap:6px;margin-bottom:3px}
.hm .dot{width:7px;height:7px;border-radius:50%;background:var(--c)}
.hans{font-size:12.5px;white-space:pre-wrap;word-break:break-word}
.herr{color:#e8794f}
</style></head><body><div class=wrap>
<h1>VLM 三模型对比 demo</h1>
<p class=sub>拖入 / 点击上传一张图 → 输入问题 → Qwen3-VL-8B · GLM-4.1V-9B · Molmo-7B-D 并行作答。judge 修正口径同评测；模型在 AMD MI308X 本地推理。</p>
<div id=exwrap><div class=exlabel>示例用例（点一下载入图 + 问题，来自各基准）</div>
  <div id=examples></div></div>
<div class=panel>
  <div id=drop><div class=ph>拖图到这里<br>或点击选择<br><span style="font-size:11px">JPG / PNG</span></div>
    <input id=file type=file accept=image/* hidden></div>
  <div class=controls>
    <textarea id=q placeholder="问关于这张图的问题，例如：图里有几个人？他们在做什么？">这张图里有什么？请简要描述。</textarea>
    <div class=presets>
      <button data-q="这张图里有什么？请简要描述。">描述</button>
      <button data-q="图中一共有几个主要物体？只回答数字。">计数</button>
      <button data-q="图片里写了什么文字？原样输出。">OCR</button>
      <button data-q="根据图表，最大的值是多少？">读图表</button>
      <button data-q="这张图有什么不寻常或不合理的地方吗？">找异常</button>
    </div>
    <button id=run>运行三模型</button>
  </div>
</div>
<div class=results>
  <div class=rc id=r_qwen style="--c:var(--qwen)"><h3><span class=dot></span>Qwen3-VL-8B</h3><div class=t>Instruct · vLLM</div><div class=ans>—</div></div>
  <div class=rc id=r_glm style="--c:var(--glm)"><h3><span class=dot></span>GLM-4.1V-9B</h3><div class=t>Thinking · vLLM</div><div class=ans>—</div></div>
  <div class=rc id=r_molmo style="--c:var(--molmo)"><h3><span class=dot></span>Molmo-7B-D</h3><div class=t>transformers</div><div class=ans>—</div></div>
</div>
<div class=histhead><h2>测试记录 <span id=hcount>0</span></h2><span class=histnote>存于服务器，刷新/换设备都在</span></div>
<div id=history></div>
</div>
<script>
let IMG=null;const drop=document.getElementById('drop'),file=document.getElementById('file');
function show(uri){IMG=uri;drop.innerHTML='<img src="'+uri+'">'}
drop.onclick=()=>file.click();
file.onchange=e=>{const f=e.target.files[0];if(!f)return;const r=new FileReader();r.onload=()=>show(r.result);r.readAsDataURL(f)};
['dragover','dragenter'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('hi')}));
['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('hi')}));
drop.addEventListener('drop',e=>{const f=e.dataTransfer.files[0];if(!f)return;const r=new FileReader();r.onload=()=>show(r.result);r.readAsDataURL(f)});
document.querySelectorAll('.presets button').forEach(b=>b.onclick=()=>document.getElementById('q').value=b.dataset.q);
const run=document.getElementById('run');
run.onclick=async()=>{
  if(!IMG){alert('先上传一张图');return}
  const prompt=document.getElementById('q').value.trim()||'描述这张图。';
  run.disabled=true;run.textContent='推理中…';
  for(const m of ['qwen','glm','molmo']){const c=document.getElementById('r_'+m);
    c.classList.remove('err');c.querySelector('.ans').innerHTML='<span class=spin></span>';
    const old=c.querySelector('.think');if(old)old.remove();}
  try{
    const res=await fetch('/infer',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({image:IMG,prompt})});
    const d=await res.json();const rr=d.result||{};
    for(const m of ['qwen','glm','molmo']){const c=document.getElementById('r_'+m),r=rr[m]||{};
      if(r.error){c.classList.add('err');c.querySelector('.ans').textContent='⚠ '+r.error}
      else{c.querySelector('.ans').textContent=r.answer||'(空)';
        if(r.think){const el=document.createElement('details');el.className='think';
          el.innerHTML='<summary>思维链</summary>'+esc(r.think);c.appendChild(el)}}}
    if(d.record)prependHistory(d.record);
  }catch(e){alert('请求失败: '+e)}
  run.disabled=false;run.textContent='运行三模型';
};
function esc(s){return String(s).replace(/[&<>"]/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[ch]))}
const MODS=[['qwen','Qwen','var(--qwen)'],['glm','GLM','var(--glm)'],['molmo','Molmo','var(--molmo)']];
function histCard(r){
  const el=document.createElement('div');el.className='hcard';
  const cols=MODS.map(([k,nm,c])=>{const v=r[k]||{};
    const body=v.error?('<span class=herr>⚠ '+esc(v.error)+'</span>'):esc(v.answer||'(空)');
    return '<div class=hcol style="--c:'+c+'"><div class=hm><span class=dot></span>'+nm+'</div><div class=hans>'+body+'</div></div>';}).join('');
  el.innerHTML='<div class=hhead><img src="'+r.thumb+'"><div class=hmeta><div class=hq>'+esc(r.prompt)+'</div><div class=hts>'+esc(r.ts)+'</div></div></div><div class=hbody>'+cols+'</div>';
  return el;
}
function prependHistory(r){const h=document.getElementById('history');
  document.getElementById('hempty')?.remove();h.insertBefore(histCard(r),h.firstChild);
  document.getElementById('hcount').textContent=h.querySelectorAll('.hcard').length;}
async function loadExamples(){try{const d=await(await fetch('/examples')).json();
  const box=document.getElementById('examples');if(!d.length){document.getElementById('exwrap').style.display='none';return}
  d.forEach(ex=>{const c=document.createElement('div');c.className='excard';c.title=ex.prompt;
    c.innerHTML='<img src="'+ex.img+'"><div class=exb>'+esc(ex.bench)+'</div>';
    c.onclick=()=>{show(ex.img);document.getElementById('q').value=ex.prompt;
      document.getElementById('drop').scrollIntoView({block:'center'})};
    box.appendChild(c)});}catch(e){}}
loadExamples();
async function loadHistory(){try{const d=await(await fetch('/history')).json();
  const h=document.getElementById('history');h.innerHTML='';
  if(!d.length){h.innerHTML='<div id=hempty class=hempty>还没有测试记录。上传一张图跑一次就会记在这里。</div>';}
  else d.forEach(r=>h.appendChild(histCard(r)));
  document.getElementById('hcount').textContent=d.length;}catch(e){}}
loadHistory();
</script></body></html>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body, ctype="application/json"):
        b = body if isinstance(body, bytes) else body.encode()
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            self._send(200, HTML, "text/html; charset=utf-8")
        elif self.path == "/history":
            self._send(200, json.dumps(load_history(), ensure_ascii=False))
        elif self.path == "/examples":
            try:
                with open(EX_PATH, encoding="utf-8") as f:
                    self._send(200, f.read())
            except Exception:
                self._send(200, "[]")
        else:
            self._send(404, b"nf")

    def do_POST(self):
        if self.path != "/infer":
            self._send(404, b"nf"); return
        try:
            n = int(self.headers.get("Content-Length", 0))
            req = json.loads(self.rfile.read(n))
            out = infer(req["image"], req.get("prompt", "描述这张图。"))
            self._send(200, json.dumps(out, ensure_ascii=False))
        except Exception as e:
            traceback.print_exc()
            self._send(500, json.dumps({"error": str(e)}))


if __name__ == "__main__":
    port = int(os.environ.get("DEMO_PORT", "7860"))
    print(f"[demo] serving on 0.0.0.0:{port}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), H).serve_forever()
