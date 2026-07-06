# VLM 摸底评测包（Qwen3-VL vs Molmo vs GLM）

> 目的：在自建 benchmark 之前，用统一 harness（VLMEvalKit）把三家模型在公共基准上的
> 差距摸清楚，确定自建题该往哪些维度出。
> 所有模型名/基准名已对照 VLMEvalKit 源码核实（2026-07-06, open-compass/VLMEvalKit@main）。

## 硬件要求
- 8B/9B 模型：1×80G（A100/H100）或 2×48G；bf16。
- 每个"模型×9基准"约 2–6 小时（取决于卡和基准大小）。

## 环境安装
```bash
conda create -n vlmeval python=3.10 -y && conda activate vlmeval
git clone https://github.com/open-compass/VLMEvalKit && cd VLMEvalKit
pip install -e .
# 注意：Molmo 系列要求 transformers==4.50.3（或 4.46.1/4.51/4.53）
# Qwen3-VL / GLM-4.1V 要求较新 transformers —— 版本冲突时为 Molmo 单开一个 env
```

## 模型（VLMEvalKit 注册名，已核实）
| 家族 | 注册名 | 说明 |
|---|---|---|
| Qwen | `Qwen3-VL-8B-Instruct` | 也可加 `Qwen3-VL-8B-Thinking` 对照 |
| Molmo | `molmo-7B-D-0924` | ⚠️ Molmo2 暂未进 VLMEvalKit（截至核实日），一代 7B-D 先顶上；
|  |  | 跑前用 `python -c "from vlmeval.config import supported_VLM; print([k for k in supported_VLM if 'olmo' in k.lower()])"` 再查一次 |
| GLM | `GLM4_1VThinking-9b` | = THUDM/GLM-4.1V-9B-Thinking；老基线可加 `glm-4v-9b` |

## 基准（9 个，名字已核实）
| 维度 | 基准名 | 判分 |
|---|---|---|
| 综合推理 | `MMMU_DEV_VAL`、`MMStar` | MCQ |
| 真实场景 | `RealWorldQA` | MCQ |
| 文档/图表 | `DocVQA_VAL`、`ChartQA_TEST` | 短答案精确匹配 |
| OCR | `OCRBench` | 规则 |
| 幻觉 | `POPE`、`HallusionBench` | Yes/No |
| 计数 | `CountBenchQA` | 规则 |

MCQ 答案抽取失败时 VLMEvalKit 会调用 judge LLM：设 `OPENAI_API_KEY`，
或加 `--judge exact_matching` 纯规则（更严格但两边一致，公平）。

## 跑
```bash
bash run_baseline.sh            # 全矩阵：3 模型 × 9 基准
# 或单跑：
python run.py --data MMMU_DEV_VAL POPE --model Qwen3-VL-8B-Instruct --verbose --reuse
```
`--reuse` 断点续跑；结果落在 `outputs/<model>/`（每基准一个 csv/xlsx + 汇总 acc）。

## 汇总
```bash
python merge_results.py outputs/   # 生成 summary.csv：行=基准，列=模型
```

## 读数原则（防坑）
1. 只比这次统一跑出的数字，**不与各家论文自报数字混比**（口径差可达 ~10 分）。
2. 每维度差距 < 2 分视为噪声（这些基准单集 ~500-2000 题）。
3. 预期图景（供校验，来自本知识库调研）：Qwen3-VL 综合/文档占优；
   Molmo 计数占优（pointing 训练红利）；GLM caption/描述类占优。
   若结果与预期大幅相反，先查环境（transformers 版本/prompt 模板）再下结论。
4. 差距最大的 2-3 个维度 = 自建 benchmark 的出题重点（转 digests/2026-07-06-mllm-benchmark-guide.md 第二步）。

## 已知空白（这套摸不到的）
- **pointing/接地对比**：pixmo-points-eval 不在 VLMEvalKit；且 Qwen/GLM 无原生点输出，
  需要设计"框选/坐标文本"的公平协议——放到自建 benchmark 阶段做。
- Molmo2 / 视频基准：等 VLMEvalKit 支持或走 vLLM 自定义 runner。
