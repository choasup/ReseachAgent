---
title: "Molmo and PixMo: Open Weights and Open Data for State-of-the-Art Vision-Language Models"
authors: "Matt Deitke, Christopher Clark et al. (AI2)"
venue: "arXiv 2409.17146 (CVPR 2025)"
published: "2024-09"
archived: "2026-07-06"
arxiv: "https://arxiv.org/abs/2409.17146"
code: "https://github.com/allenai/molmo"
topics: ["VLM / 多模态大模型", "开源模型"]
tags: ["open-weights", "open-data", "pointing", "dataset", "image-captioning"]
rating: "⭐⭐⭐⭐⭐"
---

# Molmo and PixMo: Open Weights and Open Data for SOTA VLMs

> 来源：abstract + AI2 博客 + 多个技术解读（opencv.org / analyticsvidhya / interconnects.ai 等）
> 交叉印证；原文 PDF 被本环境屏蔽，个别训练细节以原文为准。

## TL;DR
1. AI2 的全开放 VLM 一代：证明**不用任何闭源 VLM 的数据**（不蒸馏）也能做到 SOTA 级 VLM。
2. 核心是 **PixMo 数据集**（7 个子集，3 人工 + 4 合成）：口述式高细节 caption、
   人工 QA、以及**230 万条 2D pointing 标注**——"指得出"能力的起点。
3. **Molmo-72B 学术基准 11 项平均 81.2**，超 Gemini 1.5 Pro / Claude 3.5 Sonnet，
   人类偏好 Elo 仅次于 GPT-4o。

## PixMo：7 个子数据集
**人工采集（核心）**：
- **PixMo-Cap**：712k 图像、130 万条转写 caption。标注员**对着图像口述 60–90 秒**再转写，
  平均每图 200+ 词——"口述比打字更长更细"的方法论起点。
- **PixMo-AskModelAnything**：73k 图像、162k 人工 QA（标注员与纯文本 LLM 交互编辑答案）。
- **PixMo-Points**：**230 万条 pointing 标注**——点出物体位置，支撑计数与"指着回答"。

**合成（只用纯文本 LLM，不用 VLM，守住"不蒸馏"底线）**：PixMo-CapQA、PixMo-Docs、
PixMo-Clocks 等（用 LLM+代码生成图表/文档/时钟图像与 QA）。

## 架构（四组件，标准但有巧思）
1. **预处理器**：图像 → 多尺度、多裁剪（multi-crop）；**overlapping crops** 保证边缘 patch
   也带上下文（如商标文字不会被切断在裁剪边界）。
2. **ViT 编码器**：OpenAI CLIP ViT-L/14 336px（SigLIP / MetaCLIP 也可，结果相近）。
3. **Connector**：MLP 投影到 LLM 维度 + 池化减少视觉 token 数。
4. **解码器 LLM**：四档——OLMoE-1B-7B（全开放 MoE）、OLMo-7B（全开放）、
   Qwen2-7B、Qwen2-72B（性能最强）。

## 训练
两阶段：① PixMo-Cap 上做 caption 生成预训练（ViT 与 LLM 联合更新）→ ② 全部 PixMo 混合 SFT。
无 RLHF（依据摘要级信息；细节待核原文）。

## 结果
| 模型 | 11 基准平均 | 备注 |
|---|---|---|
| MolmoE-1B | 68.6 | 最高效 |
| Molmo-7B-O (OLMo) | 74.6 | 全开放栈 |
| Molmo-7B-D (Qwen2) | 77.3 | |
| **Molmo-72B** | **81.2** | 超 Gemini 1.5 Pro/Flash、Claude 3.5 Sonnet；人类偏好第 2（仅次 GPT-4o） |

## 数据与评测的可查资源
- **训练集可逐条翻看**：HF collection [allenai/pixmo](https://huggingface.co/collections/allenai/pixmo)，
  含 [pixmo-cap](https://huggingface.co/datasets/allenai/pixmo-cap)、
  [pixmo-points](https://huggingface.co/datasets/allenai/pixmo-points)（字段：image URL + points(x,y 像素) + label）、
  [pixmo-ask-model-anything]、[pixmo-cap-qa](https://huggingface.co/datasets/allenai/pixmo-cap-qa)、
  [pixmo-docs](https://huggingface.co/datasets/allenai/pixmo-docs)、
  [pixmo-point-explanations](https://huggingface.co/datasets/allenai/pixmo-point-explanations) 等；
  图像以 URL 存储需自行下载；许可 ODC-BY-1.0。
  pointing 评测集：[pixmo-points-eval](https://huggingface.co/datasets/allenai/pixmo-points-eval)。
- **测试集 = 11 个学术基准**（论文汇报口径）：AI2D(test)、ChartQA(test)、VQA v2(test)、
  DocVQA(test)、InfographicVQA(test)、TextVQA(val)、RealWorldQA、MMMU(val)、
  MathVista(testmini)、CountBenchQA、Flickr Count；另加大规模人类偏好 Elo 评测。
  论文自注：同一基准因评测细节不同可差 ~10 个点，对比时优先引用原作者数字。

## 训练样本真实格式（源自官方代码 allenai/molmo, olmo/data/data_formatter.py）
- **问题端**：从 ~50 个模板随机抽，如 `Point to the {label} in the image.` / `Show me where the {label} are` /
  `Locate every {label}.`；并配有 "No pointing" 反向模板教模型按需关闭指点。
- **回答端**（坐标归一化到 0–100，保留 1 位小数，按 x 排序）：
  - 单点：`<point x="63.5" y="44.2" alt="{label}">{label}</point>`
  - 多点：`<points x1="24.1" y1="30.2" x2="63.5" y2="44.2" alt="...">...</points>`
  - 计数（pointing 版 CoT）：`Counting the <points ...> shows a total of N.` —— 先指后数
  - 无目标：`There are none.`
- 训练时留出 pointing 评测集（hold_out_pointing_eval，即 HF 上的 pixmo-points-eval）。

## 我的评价
- **亮点**：一篇论文同时立起三根柱子——数据方法论（口述采集）、差异化能力（pointing）、
  开放原则（不蒸馏+全公开）。72B 打平/超过闭源旗舰给了"人工数据路线"最强背书。
- **局限**：pointing 靠文本输出坐标（低效，后被 MolmoPoint 用 grounding tokens 重做）；
  多裁剪+池化的分辨率处理在超高分图上仍是妥协；评测集中在单图。
- **地位**：系列奠基之作，也是社区"从零训 VLM"的标准参考。

## 关联
- **二代**：[Molmo2 笔记](2026-07-06-molmo2-open-video-vlm.md)（扩展到视频）。
- **架构衍生**：MolmoPoint（arXiv 2603.28069，grounding tokens 替代坐标文本）。
- 系列分析：[digests/2026-07-06-molmo-series-analysis.md](../../digests/2026-07-06-molmo-series-analysis.md)

**Sources**: [arXiv](https://arxiv.org/abs/2409.17146) · [AI2 博客](https://allenai.org/blog/molmo) · [GitHub](https://github.com/allenai/molmo) · [HF Molmo-72B](https://huggingface.co/allenai/Molmo-72B-0924) · [interconnects 解读](https://www.interconnects.ai/p/molmo-and-llama-3-vision)
