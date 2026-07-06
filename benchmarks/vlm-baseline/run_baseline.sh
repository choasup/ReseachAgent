#!/usr/bin/env bash
# VLM 摸底：3 模型 × 9 基准（VLMEvalKit）
# 用法：在 VLMEvalKit 仓库根目录执行本脚本；断点续跑安全（--reuse）。
set -uo pipefail

BENCHMARKS="MMMU_DEV_VAL MMStar RealWorldQA DocVQA_VAL ChartQA_TEST OCRBench POPE HallusionBench CountBenchQA"
MODELS=("Qwen3-VL-8B-Instruct" "GLM4_1VThinking-9b" "molmo-7B-D-0924")

# 判分：无 OPENAI_API_KEY 时退回纯规则匹配（两边一致即公平）
JUDGE_ARGS=""
if [ -z "${OPENAI_API_KEY:-}" ]; then
  echo "[warn] OPENAI_API_KEY 未设置，MCQ 抽取退回 exact_matching"
  JUDGE_ARGS="--judge exact_matching"
fi

for MODEL in "${MODELS[@]}"; do
  echo "============================================================"
  echo ">>> $MODEL"
  echo "============================================================"
  # Molmo 需要 transformers==4.50.3；若与主环境冲突，用 conda env 隔离：
  #   conda activate vlmeval-molmo （里面 pip install transformers==4.50.3）
  python run.py --data $BENCHMARKS --model "$MODEL" --verbose --reuse $JUDGE_ARGS \
    2>&1 | tee "run_${MODEL//\//_}.log"
  echo "<<< $MODEL done (log: run_${MODEL//\//_}.log)"
done

echo "全部完成。汇总： python merge_results.py outputs/"
