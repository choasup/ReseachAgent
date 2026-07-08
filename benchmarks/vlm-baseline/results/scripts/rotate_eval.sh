#!/usr/bin/env bash
# 轮换评测新增开源模型：每个模型 vllm serve（端口 18011, HIP1 卡 0.30 显存）
# -> 等就绪 -> apple sanity -> 10 数据集（judge=本机 18001 Qwen）-> 关容器。
# 幂等：已有全部 10 项指标文件的模型跳过。
set -uo pipefail
BASE=/home/tione/notebook/research/choasliu
T=$BASE/Project/001_VLM_benchmark
HUB=$BASE/hf_home/hub
source $BASE/miniforge3/etc/profile.d/conda.sh
conda activate vlmeval
export HF_HOME=$BASE/hf_home LMUData=$BASE/LMUData HF_HUB_OFFLINE=1
export OPENAI_API_KEY=dummy OPENAI_API_BASE=http://127.0.0.1:18001/v1/chat/completions LOCAL_LLM=Qwen3-VL-8B-Instruct
unset https_proxy http_proxy
cd $T/VLMEvalKit
B="MMMU_DEV_VAL MMStar RealWorldQA DocVQA_VAL ChartQA_TEST OCRBench POPE HallusionBench CountBenchQA Inspection"

# 注册名|served名|HF目录名
MODELS="
InternVL3-8B-vllm|InternVL3-8B|models--OpenGVLab--InternVL3-8B
Qwen2.5-VL-7B-vllm|Qwen2.5-VL-7B-Instruct|models--Qwen--Qwen2.5-VL-7B-Instruct
MiniCPM-V-2.6-vllm|MiniCPM-V-2_6|models--openbmb--MiniCPM-V-2_6
Ovis2-8B-vllm|Ovis2-8B|models--AIDC-AI--Ovis2-8B
LLaVA-OneVision-7B-vllm|llava-onevision-qwen2-7b-ov-hf|models--llava-hf--llava-onevision-qwen2-7b-ov-hf
Phi-3.5-Vision-vllm|Phi-3.5-vision-instruct|models--microsoft--Phi-3.5-vision-instruct
Idefics3-8B-vllm|Idefics3-8B-Llama3|models--HuggingFaceM4--Idefics3-8B-Llama3
DeepSeek-VL2-small-vllm|deepseek-vl2-small|models--deepseek-ai--deepseek-vl2-small
Pixtral-12B-vllm|Pixtral-12B-2409|models--mistralai--Pixtral-12B-2409
"

log(){ echo "[$(date '+%F %T')] $*"; }

serve_and_eval(){
  local reg=$1 served=$2 hfdir=$3
  local snap=$(ls -d $HUB/$hfdir/snapshots/*/ 2>/dev/null | head -1)
  [ -z "$snap" ] && { log "SKIP $reg (权重未下载)"; return; }
  # 幂等：10 项指标齐了就跳过
  local done_n=$(ls outputs/$reg/T*/${reg}_*_acc.csv outputs/$reg/T*/${reg}_*_score.csv outputs/$reg/T*/${reg}_*_score.json 2>/dev/null | wc -l)
  [ "$done_n" -ge 10 ] && { log "SKIP $reg (已完成 $done_n 项)"; return; }
  log "SERVE $reg <- $snap"
  docker rm -f rotate_eval >/dev/null 2>&1
  docker run -d --name rotate_eval --network host --device /dev/kfd --device /dev/dri --shm-size 16g \
    -e HIP_VISIBLE_DEVICES=1 -v /home/tione/notebook:/notebook rocm/vllm:latest \
    vllm serve "${snap/\/home\/tione\/notebook/\/notebook}" \
    --served-model-name "$served" --port 18011 --gpu-memory-utilization 0.30 \
    --max-num-seqs 16 --trust-remote-code >/dev/null
  # 等就绪（最多 15 分钟）
  local up=0
  for i in $(seq 1 90); do
    curl -s --max-time 4 http://127.0.0.1:18011/v1/models 2>/dev/null | grep -q "$served" && { up=1; break; }
    docker ps --format '{{.Names}}' | grep -q rotate_eval || break
    sleep 10
  done
  if [ $up -ne 1 ]; then
    log "SERVE_FAIL $reg"; docker logs rotate_eval 2>&1 | tail -8; docker rm -f rotate_eval >/dev/null 2>&1
    echo "$reg" >> $T/rotate_failed.txt; return
  fi
  # sanity: apple 描述
  local ans=$(python - "$served" << "PYEOF"
import sys, json, base64, urllib.request
served = sys.argv[1]
b64 = base64.b64encode(open("assets/apple.jpg", "rb").read()).decode()
body = {"model": served, "max_tokens": 64, "messages": [{"role": "user", "content": [
    {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
    {"type": "text", "text": "Describe this image in one short sentence."}]}]}
req = urllib.request.Request("http://127.0.0.1:18011/v1/chat/completions",
                             data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
try:
    d = json.load(urllib.request.urlopen(req, timeout=120))
    print((d["choices"][0]["message"].get("content") or d["choices"][0]["message"].get("reasoning_content") or "")[:100].replace("\n", " "))
except Exception as e:
    print("SANITY_ERR", type(e).__name__, str(e)[:80])
PYEOF
)
  log "SANITY $reg: $ans"
  case "$ans" in SANITY_ERR*) log "SANITY_FAIL $reg"; docker rm -f rotate_eval >/dev/null 2>&1; echo "$reg" >> $T/rotate_failed.txt; return;; esac
  echo "$ans" | grep -qiE "apple|fruit|red" || log "WARN $reg sanity 未提到苹果，请复核"
  # 评测（judge 直连本机 18001）
  log "EVAL $reg 开始 10 数据集"
  timeout 28800 python run.py --data $B --model "$reg" --verbose --reuse --judge gpt-4o-mini --api-nproc 16 \
    > $T/rotate_${reg}.log 2>&1
  log "EVAL $reg 结束 (指标数: $(ls outputs/$reg/T*/${reg}_* 2>/dev/null | grep -cE '_acc.csv|_score.csv|_score.json'))"
  docker rm -f rotate_eval >/dev/null 2>&1
}

echo "$MODELS" | while IFS="|" read -r reg served hfdir; do
  [ -z "$reg" ] && continue
  serve_and_eval "$reg" "$served" "$hfdir"
done
log ROTATE_ALL_DONE
