# 开源 VLM 摸底评测终版报告：9 模型 × 10 数据集

> 统一 harness（VLMEvalKit + vLLM serve）横评 9 个开源 VLM：9 个公共基准 + 1 个自建
> 巡检基准（真实门店监控）。硬件 AMD MI308X（ROCm 6.3）。评测日期 2026-07-07 ~ 07-09。
> 巡检基准详细报告见 `INSPECTION_REPORT.md`。

## 0. 执行摘要

**总排行（10 项均分）**：

| # | 模型 | 总均分 | 公共9项 | 巡检 | 备注 |
|---|---|---|---|---|---|
| 1 | **Qwen3-VL-8B-Instruct** | **78.9** | **81.0** | 60.2 | 全能冠军：文档/OCR/幻觉/计数四项第一 |
| 2 | GLM-4.1V-9B-Thinking | 75.4 | 77.7 | 54.6 | 综合推理三项第一（MMMU/MMStar/RWQA）；图表是致命短板 |
| 3 | Ovis2-8B | 74.9 | 77.6 | 50.7 | OCR/文档强；巡检垫底 |
| 4 | Qwen2.5-VL-7B | 74.7 | 77.0 | 54.0 | 图表第一（85.8）；被 Qwen3 代际全面超越 |
| 5 | InternVL3-8B | 72.6 | 73.9 | **60.8** | 公共中游，**巡检第一**——两榜错位最典型 |
| 6 | Molmo-7B-D | 70.9 | 72.5 | 56.6 | POPE 第一；推理/OCR 弱 |
| 7 | Pixtral-12B | 66.2 | 67.4 | 55.5 | 参数最大但整体三线 |
| 8 | LLaVA-OneVision-7B | 63.6 | 65.0 | 51.0 | 2024 老架构掉队（OCR 53.5） |
| 9 | Idefics3-8B | 58.9 | 59.6 | 52.2 | 全面垫底（ChartQA 41.5） |

**三个核心发现**：
1. **代际红利真实存在**：Qwen2.5-VL→Qwen3-VL 同门升级 +4.2 总均分（MMMU +14、幻觉 +4、巡检 +6）。
2. **公共榜与巡检榜严重错位**：巡检榜 InternVL3(60.8) ≈ Qwen3-VL(60.2) 断层领先，而公共榜
   第 2-4 名（GLM/Ovis2/Qwen2.5）巡检全部 ≤55、Ovis2 垫底——**公共基准分数无法预测
   真实业务场景表现**，这正是自建 benchmark 的价值证明。
3. **巡检全员不及格**：9 模型巡检 50.7~60.8（随机=50），系统性漏报（答 yes 率 9-22% vs
   真实 48%）。zero-shot VLM 做巡检不可用；与 MME-RealWorld（监控域无一过 60%）、
   FoodMonitor（最佳 0.36）等学术结论互证。

## 1. 分基准完整矩阵（0-100，加粗=该行最高）

| 基准 | GLM-4.1V | Idefics3 | InternVL3 | LLaVA-OV | Ovis2 | Pixtral | Qwen2.5-VL | **Qwen3-VL** | Molmo |
|---|---|---|---|---|---|---|---|---|---|
| MMMU | **68.1** | 40.3 | 57.1 | 47.0 | 52.9 | 47.3 | 51.9 | 66.1 | 47.7 |
| MMStar | **72.9** | 55.2 | 64.8 | 57.1 | 65.3 | 52.2 | 62.7 | 71.5 | 56.3 |
| RealWorldQA | **72.4** | 60.9 | 62.8 | 63.5 | 70.7 | 61.8 | 67.5 | 70.7 | 70.7 |
| DocVQA | 91.8 | 79.2 | 90.0 | 82.2 | 93.4 | 84.8 | 94.7 | **95.7** | 91.5 |
| ChartQA | 57.4 | 41.5 | 82.3 | 74.4 | 83.1 | 70.4 | **85.8** | 83.2 | 83.8 |
| OCRBench | 86.2 | 50.8 | 82.4 | 53.5 | 89.3 | 68.4 | 88.7 | **89.9** | 66.1 |
| POPE | 87.0 | 85.4 | 88.9 | 85.2 | 88.8 | 81.5 | 86.6 | 87.6 | **89.0** |
| HallusionBench | 73.3 | 58.6 | 63.0 | 54.3 | 66.5 | 63.8 | 69.6 | **73.8** | 62.4 |
| CountBenchQA | **90.1** | 64.9 | 73.5 | 67.6 | 88.5 | 76.6 | 85.8 | **90.1** | 85.4 |
| **Inspection(巡检)** | 54.6 | 52.2 | **60.8** | 51.0 | 50.7 | 55.5 | 54.0 | 60.2 | 56.6 |

## 2. 方法学（口径与公平性）

- **推理**：8 个模型走 vLLM serve（OpenAI 兼容 API，16 并发；采样参数用各模型自带
  generation_config，公平且零维护）；Molmo 走 transformers（含 ROCm 补丁）。
- **判分**：VQA/OCR/计数走规则；MCQ/Y-N 的答案抽取统一用**本机 LLM-judge**
  （`exact_matching` 对冗长输出系统性漏判：Qwen3 MMMU 21%→66%——详见首版报告章节，
  修正可信性验证：翻负=0、简洁模型零变化）。
- **ROCm 适配**：eager attention（gfx942 SDPA 视觉塔静默算错）、Conv2d/3d(kernel==stride)
  →matmul（MIOpen 段错误）、get_gpu_memory 补丁。全部固化在 `scripts/patch_vlmevalkit.py`。
- **巡检基准**：339 题 Y/N、7 场景、红圈标注 inpaint 防作弊，详见 `INSPECTION_REPORT.md`。

### 未纳入模型及原因
| 模型 | 原因 |
|---|---|
| Phi-3.5-Vision | vLLM API 兼容失败：sanity 通过但基准请求全部超时（"Failed to obtain answer via API"） |
| DeepSeek-VL2-small | vLLM-ROCm 镜像 EngineCore 启动失败（含 `--hf-overrides` 架构指定后仍崩） |
| MiniCPM-V-2.6 | HF gated 仓库，无访问授权 |
| Llama-3.2-11B-Vision | HF gated 仓库，无访问授权 |

## 3. 各模型一句话画像

- **Qwen3-VL-8B**：买它。四项第一，无明显短板；巡检也在第一梯队。
- **GLM-4.1V-9B**：推理型选手（thinking 模型），MMMU/MMStar 最强；**读图表数值弱得反常**
  （57.4，比第一低 28 分），做 BI/图表场景避开。
- **Ovis2-8B**：OCR/文档专精（89.3/93.4）；但真实监控场景理解全场最差（巡检 50.7≈随机）。
- **Qwen2.5-VL-7B**：图表最强；其余全面被 Qwen3 超越——无理由继续选它。
- **InternVL3-8B**：公共平庸、**巡检最强**——训练分布可能更贴近真实监控/工业图像；
  做真实场景应用值得优先试。
- **Molmo-7B-D**：幻觉抵抗与 pointing 特色（输出坐标）；学科推理/OCR 明显弱。
- **Pixtral-12B / LLaVA-OV-7B / Idefics3-8B**：整体三线，无单项冠军，不推荐。

## 4. 对自建 benchmark 与业务的结论

1. **出题重点**（区分度最大）：图表数值读取（分差 44）、OCR（分差 39）、学科多步推理
   （分差 28）、巡检类真实场景（两榜错位的核心证据源）。
2. **巡检业务选型**：InternVL3-8B 与 Qwen3-VL-8B 起点最高，但 60 分意味着都必须
   微调/提示工程后才可用；建议下一步做"正常参照描述"提示对照实验 + V*/SEAL 式
   两段法（先定位后判断）验证，然后走少样本微调。
3. **学术定位**：远距监控单帧多目标巡检判断在学术界是空白（MMAD 工业近拍、
   FoodMonitor 视频时序），26k 已标注巡检图有发表/开源价值。

## 5. 文件清单

- `summary.csv` — 终版 9×10 矩阵 · `summary_exact_matching.csv` — 首版 exact 口径存档
- `INSPECTION_REPORT.md` / `inspection_report.html` — 巡检专项报告（含用例与错例图）
- `samples.json` — 首版三模型正确/错误采样 · `logs/` — 全部推理日志（gz）
- `scripts/` — 全流程可复现脚本（构建/补丁/注册/轮换评测/判分修正/汇总/采样/demo）
- 服务器工作区：`~/research/choasliu/Project/001_VLM_benchmark/`（含 VLMEvalKit outputs、
  demo 服务、Inspection.tsv）
