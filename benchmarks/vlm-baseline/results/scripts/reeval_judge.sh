#!/usr/bin/env bash
# 抽取敏感基准（MCQ + Y/N）用本机 vLLM 当 LLM judge 重评，修 exact_matching 对冗长输出的漏判。
# 幂等：已有 *_gpt-4o-mini*result* 的基准跳过。用法: reeval_judge.sh <模型输出目录名...>
set -uo pipefail
BASE=/home/tione/notebook/research/choasliu
W=$BASE/013_mllm/benchmarks/vlm-baseline/VLMEvalKit
source $BASE/miniforge3/etc/profile.d/conda.sh
conda activate vlmeval
export HF_HOME=$BASE/hf_home LMUData=$BASE/LMUData HF_HUB_OFFLINE=1
export OPENAI_API_KEY=dummy OPENAI_API_BASE=http://127.0.0.1:18001/v1/chat/completions LOCAL_LLM=Qwen3-VL-8B-Instruct
unset https_proxy http_proxy
cd $W
BENCHES="${BENCHES:-MMMU_DEV_VAL MMStar RealWorldQA POPE HallusionBench}"
mkdir -p $W/outputs/_exact_backup
for MODEL in "$@"; do
  for B in $BENCHES; do
    # 找含该基准预测的原始目录
    xlsx=$(ls outputs/$MODEL/T*/${MODEL}_${B}.xlsx 2>/dev/null | head -1)
    [ -z "$xlsx" ] && { echo "SKIP $MODEL/$B (无预测)"; continue; }
    # 已有 judge 结果则跳过
    if ls outputs/$MODEL/T*/${MODEL}_${B}_gpt-4o-mini*result*.xlsx >/dev/null 2>&1; then
      echo "SKIP $MODEL/$B (已judge)"; continue
    fi
    D=$(dirname "$xlsx")
    for m in "${D}/${MODEL}_${B}_acc.csv" "${D}/${MODEL}_${B}_score.csv" "${D}/${MODEL}_${B}_score.json"; do
      [ -f "$m" ] && cp "$m" "$W/outputs/_exact_backup/$(basename ${m%.*})_EXACT.${m##*.}" && rm -f "$m"
    done
    echo "[$(date '+%T')] REEVAL $MODEL/$B"
    timeout 1800 python run.py --data $B --model "$MODEL" --mode eval --judge gpt-4o-mini --api-nproc 16 --reuse >/dev/null 2>&1 \
      && echo "  OK $MODEL/$B" || echo "  FAIL_REEVAL $MODEL/$B"
  done
done
echo REEVAL_JUDGE_DONE
