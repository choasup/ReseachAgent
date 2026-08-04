#!/usr/bin/env python3
"""Seedance B-roll 生成脚本（在你本地/GPU 机器上跑，key 走环境变量不进代码）。

用法：
  export ARK_API_KEY=你的key
  export SEEDANCE_MODEL=doubao-seedance-2-0   # ← 以火山方舟控制台的实际模型ID为准
  pip install requests
  python generate_broll.py            # 生成全部 3 个镜头
  python generate_broll.py opening    # 只生成指定镜头

产物落在 ./out/*.mp4，检查满意后：
  git add out && git commit -m "broll clips" && git push
然后回 Claude 会话说一声，由云端把镜头剪进样片。

范围纪律：只做 1 个片头 + 2 个转场。生成镜头不承载信息，只做氛围——信息由原文图和信息卡承载。
"""
import os, sys, time, json, base64, pathlib
import requests

API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"
KEY = os.environ.get("ARK_API_KEY") or sys.exit("请先 export ARK_API_KEY=...")
MODEL = os.environ.get("SEEDANCE_MODEL") or sys.exit(
    "请先 export SEEDANCE_MODEL=<控制台里的模型ID>（如 doubao-seedance-2-0-xxx）")
HERE = pathlib.Path(__file__).parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
ASSETS = HERE.parent / "assets"

# ---- 镜头清单（刻意只有 3 个）----
SHOTS = {
    "opening": dict(
        ref=ASSETS / "card-hook.png",   # 风格参考：钩子卡（深色科技风锚定）
        dur=10,
        prompt=(
            "深色科技空间，中央一个发光的神经网络核心，周围的工具图标（终端、文件、齿轮）"
            "被光线逐一接入核心，接入时核心亮度提升，镜头缓慢推进，深蓝黑色调，电影感体积光，"
            "无文字，无人物，节奏沉稳"
        )),
    "transition-evolution": dict(       # 用于 05:00 谱系段 → 案例段之间
        ref=ASSETS / "asset2-ladder.png",
        dur=8,
        prompt=(
            "抽象的发光台阶在黑暗中自下而上逐级点亮，颜色从绿到蓝到紫到橙到红，"
            "镜头随最高一级的红光缓慢上升并轻微震动，极简风格，无文字"
        )),
    "transition-coldwater": dict(       # 用于 10:00 冷水段开场
        ref=ASSETS / "card-coldwater.png",
        dur=6,
        prompt=(
            "深色画面，三滴水珠依次落入平静的黑色水面，激起蓝红色冷光涟漪，"
            "慢镜头，极简，无文字，安静克制"
        )),
}

def b64(p):
    return "data:image/png;base64," + base64.b64encode(open(p, "rb").read()).decode()

def submit(name, shot):
    content = [
        {"type": "text",
         "text": f"{shot['prompt']} --resolution 1080p --duration {shot['dur']} --watermark false"},
    ]
    if shot["ref"].exists():
        content.append({"type": "image_url", "image_url": {"url": b64(shot["ref"])},
                        "role": "reference_image"})
    r = requests.post(API, headers={"Authorization": f"Bearer {KEY}",
                                    "Content-Type": "application/json"},
                      json={"model": MODEL, "content": content}, timeout=60)
    r.raise_for_status()
    tid = r.json()["id"]
    print(f"[{name}] 任务提交: {tid}")
    return tid

def poll(name, tid):
    while True:
        r = requests.get(f"{API}/{tid}", headers={"Authorization": f"Bearer {KEY}"}, timeout=60)
        r.raise_for_status()
        d = r.json()
        st = d.get("status")
        if st == "succeeded":
            url = d["content"]["video_url"]
            data = requests.get(url, timeout=300).content
            out = OUT / f"{name}.mp4"
            out.write_bytes(data)
            print(f"[{name}] ✅ {out} ({len(data)//1024} KB)")
            return
        if st in ("failed", "cancelled"):
            print(f"[{name}] ❌ {st}: {json.dumps(d)[:300]}"); return
        print(f"[{name}] {st} ...")
        time.sleep(10)

if __name__ == "__main__":
    targets = sys.argv[1:] or list(SHOTS)
    for name in targets:
        poll(name, submit(name, SHOTS[name]))
    print("done. 检查 out/ 后 git add/commit/push，然后回会话喊云端剪辑。")
