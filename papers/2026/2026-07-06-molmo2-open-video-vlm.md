---
title: "Molmo2: Open Weights and Data for Vision-Language Models with Video Understanding and Grounding"
authors: "Christopher Clark et al."
venue: "arXiv 2601.10611"
published: "2026-01"
archived: "2026-07-06"
arxiv: "https://arxiv.org/abs/2601.10611"
code: "https://allenai.org/molmo"
topics: ["VLM / 多模态大模型", "视频理解", "开源模型"]
tags: ["open-weights", "open-data", "video-grounding", "pointing", "video-understanding", "dataset"]
rating: "⭐⭐⭐⭐⭐"
---

# Molmo2: Open Weights and Data for VLMs with Video Understanding and Grounding

> ⚠️ **来源说明**：arXiv/AI2 官网/tech report PDF 均被本环境网络策略屏蔽，未读原文正文。
> 以下基于 abstract + AI2 官方博客的搜索摘要 + 多个报道源（SiliconANGLE 等）交叉印证；
> 具体数字标注了出处，架构细节以原文为准。

## TL;DR
1. AI2（Allen Institute for AI）的全开放（权重+数据+配方）VLM 系列第二代，把 Molmo 的
   "pointing 接地"能力从单图扩展到**多图与视频**：视频问答、视频指点（video pointing）、目标跟踪。
2. 核心贡献是 **9 个全新开放数据集**（7 视频 + 2 多图，共 900 万+ 多模态样本），
   全部**不依赖闭源 VLM** 采集——延续"不蒸馏闭源模型"的路线。
3. 8B 模型在开放权重+数据类中最强，**视频接地上甚至超过 Gemini 3 Pro**
   （video pointing F1 38.4 vs 20.0；video tracking J&F 56.2 vs 41.1）。

## 背景与问题
- 最强多模态模型仍是闭源的；开源模型普遍靠蒸馏闭源 VLM 的合成数据"曲线救国"，
  社区缺乏"从零构建高性能 VLM"的基础知识（一代 Molmo 提出的问题，本作延续）。
- 视频理解+接地（grounding/pointing/tracking）上，开放模型与闭源差距尤其大。

## 核心方法
**数据（主要贡献）**：9 个新数据集，均由人工采集/标注，不用闭源 VLM：
- 高细节**视频 caption** 预训练集（Molmo2-Cap）：人工口述旁白转写 + Molmo 帧级细节增强，
  平均每段视频 900+ 词（远超常规视频 caption 数据）。
- 自由形式**视频 QA** 微调集；复杂 query 的**目标跟踪**集；创新的**视频 pointing** 集；2 个多图数据集。

**架构**（标准 MLLM 管线）：冻结的 **SigLIP 2 ViT** 编码图像/帧（固定或 tiled 分辨率）
→ 特征池化 + connector 投影成 token → 喂给预训练 LLM（Qwen3 或 OLMo3）。

**训练配方**：
- 三阶段：① 图像 caption + 图像 pointing 预训练 → ② 图/视频/多图混合 SFT → ③ 短程长上下文训练。
- **Message-tree 编码**：一段视频常有多条标注（caption、QA、pointing……）。传统做法每条标注
  重复编码一次视频；message-tree 把视觉输入作为第一条消息、每条标注作为一个分支，线性化成
  单序列 + 自定义注意力掩码防止分支互看。平均每例 4 条标注，SFT 时一个 16,348 token 序列能
  packing 进 3.8 个样本，**训练效率 15×**。
- **视觉 token 双向注意力**：打破 LLM 的因果掩码限制，让视觉 token 互相可见，改善帧间信息整合。
- **Token 加权策略**：微调时按任务加权 token 损失，平衡多样任务的学习。

**模型家族**：Molmo2 8B / 4B（基座 Qwen 3）+ Molmo2-O 7B（基座 AI2 自家 OLMo3，全栈开放）。
另：CVPR 2026 poster 收录。

## 主要结果
| 任务 | Molmo2 | 对比 | 出处 |
|---|---|---|---|
| Video pointing (F1) | **38.4** | Gemini 3 Pro 20.0 | abstract/AI2 博客 |
| Video tracking (J&F) | **56.2** | Gemini 3 Pro 41.1 | abstract/AI2 博客 |
| Video counting (acc) | **35.5** | Qwen3-VL 29.6 | abstract |
| 短视频/计数/caption | 开放权重+数据类中最佳 | 长视频"competitive" | abstract |

## 与 Qwen3-VL 的头对头（来自论文/AI2 博客口径）
- **人评 win rate**：Molmo2-8B vs Qwen3-VL-8B = **53%**；4B vs 4B = **51%**（整体打平略胜）。
- **视频理解 7 基准平均**（NextQA/PerceptionTest/MVBench/Video-MME 等）：Molmo2-8B 开放权重最佳。
- **分项互有胜负**：开放式视频 QA Molmo2 胜；**captioning 输给 Qwen3-VL 和 GLM-4.1V**。
- **接地是代差**：video counting 35.5 vs 29.6；video pointing/tracking Qwen3-VL 基本无对位能力。
- 推理吞吐/延迟的直接对比未见公开数字（性能侧只有训练效率 message-tree 15× 可引）。

### 速度相关硬参数（已核实 + 推算）
- 视觉编码器：**SigLIP 2 So400m/14 384px**（~400M 参数，冻结）；connector 用多头注意力池化，
  **图像 2×2、视频帧 3×3 池化**。
- 推算 token 预算：384px/14 ≈ 27×27=729 patch → 视频 **~81 token/帧**（÷9）、图像 ~182 token/crop（÷4）。
  每帧成本低且固定；对比 Qwen3-VL 原生动态分辨率（token 随输入分辨率浮动、可调 max_pixels）。
- 部署：**vLLM 自 v0.15.0 官方支持 Molmo2**；社区有 NVFP4 量化版（需定制 vLLM build）。
  Qwen 生态成熟度仍明显占优（各框架 day-0、量化格式全）。
- 同规模（4B/8B）下 decode 速度由 LLM 主导，两家应相近；差异主要在 **prefill 的视觉 token 数**。

## 局限与存疑
- 长视频只是"competitive"而非领先——长时序仍是短板（原文如何分析未读到）。
- 视频接地的惊艳数字集中在 pointing/tracking 这类**该系列自己定义并深耕的任务**上，
  基准选择对其有利；通用视频 QA 上与顶级闭源的差距需看原文完整表格。
- 与 Qwen3-VL 的对比口径（模型规模、评测设置）待核。

## 我的评价
- **亮点**：当前"真开源"（权重+数据+配方全开放）路线的标杆工作。最有价值的不是模型本身，
  而是**"不蒸馏闭源模型也能做出 SOTA 级 VLM"的完整配方**——数据怎么采、三阶段怎么训、
  packing/注意力怎么改，全部可复现。pointing/tracking 作为"可验证的接地"接口，对 agent、
  机器人、视频编辑等下游都是实用能力。
- **对你的价值**：①开源基座选型——做视频接地相关应用，Molmo2 8B 是目前开放类最强候选；
  ②9 个数据集本身是稀缺资产（尤其 video pointing/tracking 标注）；③"人工口述 caption"
  的数据采集方法论值得借鉴。
- **值得深读**：是。优先看：双向视觉注意力 + token 加权的消融、长视频短板的分析、
  数据集的规模/质量细节。

## 关联（系列脉络）
- **一代**：Molmo and PixMo (arXiv 2409.17146, 2024-09) — 单图时代的开放 VLM 标杆，
  见 [笔记](2026-07-06-molmo-pixmo.md)。
- **后续**：MolmoPoint (arXiv 2603.28069) — 用 grounding tokens 改进 VLM pointing（系列衍生，未深读）。
- 对比阅读：Qwen3-VL（开放权重但数据不开放）、本库 CVPR 2026 VLM×推理清单中的
  video grounding 工作（SARL-STG、TempR1）。

**Sources**: [arXiv abs](https://arxiv.org/abs/2601.10611) · [AI2 博客](https://allenai.org/blog/molmo2) · [SiliconANGLE 报道](https://siliconangle.com/2025/12/16/allen-institute-ai-introduces-molmo-2-bringing-open-video-understanding-ai-systems/)
