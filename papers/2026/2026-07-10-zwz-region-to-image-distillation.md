---
title: "Zooming without Zooming: Region-to-Image Distillation for Fine-Grained Multimodal Perception"
authors: "Lai Wei et al.（上海交大 + 蚂蚁 inclusionAI）"
venue: "ICML 2026（arXiv）"
published: "2026-02"
archived: "2026-07-10"
arxiv: "https://arxiv.org/abs/2602.11858"
code: "https://github.com/inclusionAI/Zooming-without-Zooming"
topics: ["vlm", "inspection-anomaly-benchmark"]
tags: ["fine-grained-perception", "distillation", "RL", "DAPO", "benchmark", "zoom"]
rating: "⭐⭐⭐⭐⭐"
---

# Zooming without Zooming: Region-to-Image Distillation for Fine-Grained Multimodal Perception

## TL;DR
> MLLM 看不清大图里的小目标，现有解法是推理时反复裁剪放大（agentic zooming），又慢又长。
> 本文把 zoom 变成**训练时原语**：教师模型在微小裁剪（<10% 面积）上出题，把区域级监督
> "蒸馏"回全图（框注/空间提示 + DAPO RL），仅 74K 合成数据就让 Qwen 系基座在单次前向内
> 获得细粒度感知——ZoomBench +15~20 分、比工具调用方法**快约 10 倍**且更准，通用能力零损失。

## 背景与问题
- MLLM 细粒度感知弱：图像 token 化时小目标信息被稀释；决定性证据小且被全局上下文淹没。
- 现有 agentic zooming（DeepEyes/Mini-o3/Thyme 等）推理时迭代裁剪-再看，延迟高、轨迹长、
  易受工具误差累积影响。
- 缺一个专测"证据极小"的 benchmark 来量化这个能力（→ ZoomBench）。

## 核心方法（R2I：Region-to-Image Distillation）
- **一句话**：区域上生成的"看得清"监督，搬回全图上训练"不放大也看得清"。
- 流程：
  1. 检测器出候选框，取面积 <10%（τ=0.1）的微小区域；
  2. 教师模型在 micro-crop 上生成感知类 QA，多数投票保共识、抑幻觉；
  3. 关键难点：区域内清晰的问题放回全图会歧义 → **框叠加到原图 + 提示词加空间约束**，
     构成增强三元组 (I′, Q′, A)；
  4. 难度过滤（小模型能答对的丢弃）→ 74K 合成数据（对比 Oasis 500K / DeepEyes 47K）；
  5. **DAPO** RL 训练，最大化任务奖励 r(Â, A)。
- 与已有方法区别：不是教模型"何时调用 zoom 工具"，而是把 zoom 后才能获得的监督信号
  内化进权重——推理时单次前向。

## ZoomBench（845 题 VQA）
- 6 维度：微粒度计数 / OCR / 颜色属性 / 结构属性 / 材料属性 / 物体识别。
- **Dual-view 协议**：同一题分别用全图（Global）与对应 micro-crop（Regional）作答，
  差值 = **zooming gap**（如 Qwen3-VL-8B：Regional 63.08% → Global 37.87%，gap 25.21%）。
- 构建：教师在裁剪上出题 → 映射回全图 → 人工校验有效性/难度/正确性。

## 主要结果
| 指标 / 任务 | ZwZ | baseline | 备注 |
|---|---|---|---|
| ZoomBench (Global) | ZwZ-8B **58.11** | Qwen3-VL-8B 37.87 | +20.2（§4/表1） |
| ZoomBench (4B/7B) | 55.74 / 55.62 | 40.24 / 42.49 | 各 +15.5 / +13.1 |
| 跨基准平均（表2） | ZwZ-8B **68.12** | GLM-4.5V 65.04 / Qwen3-VL-235B 67.55 | 8B 超 235B |
| vs agentic（表4，4 基准均分） | ZwZ-8B **81.9**（单次前向） | DeepEyesV2 74.6 / Mini-o3 76.1（迭代工具） | 且 ~10× 快（图5） |
| zooming gap | 15.26%（最小） | 基座 25.21% | gap 显著收窄 |

## 局限与存疑
- 论文自认（§6.4）：空间推理与多物体感知覆盖不足（未在 TreeBench 等评测）；可通过
  合成空间/搜索类工具数据扩展。
- 依赖高分辨率编码（明确"不下采样"）；数据管线质量受教师模型与检测器上限约束。
- 我的质疑：合成 QA 偏"属性感知"类，任务分布窄——**已被我们实测印证**：在我们的
  巡检 benchmark 上，ZwZ 清洁类（小目标脏污）大涨、人物合规类反而回落（见下）。

## 我的评价
- **亮点**：干净的小改动大收益——74K 数据、RL 训练、零推理开销；dual-view 的
  zooming gap 是个可复用的诊断指标；出身好（SJTU+蚂蚁，ICML'26）。符合"小而美+工程化"口味。
- **对我们的价值（已实测验证，2026-07-10，本库 benchmarks/vlm-baseline）**：
  ZwZ-8B 在我们 339 题巡检集上总分 60.5 ≈ 基座 60.2，但**异常召回 32%→62% 翻倍**
  （答 yes 率 22%→51%，≈真实 48%），F1 ~0.44→0.60；MME-RealWorld-Lite 监控域感知
  36.1→46.4；公共 9 基准零损失。分场景：制作区清洁 82（全场最高）、客区 +16；
  人员/物料类回落——**R2I 配方对"小目标脏污发现"直接有效，人物合规需另配数据**。
- **值得复现**：是。落地路径 = 复刻 R2I 管线（我们有 26k 已标注巡检图，异常框可从
  红圈标注反推），把"巡检异常裁剪"当 micro-crop 源，DAPO 蒸回全图。

## 关联
- 相关：[[2026-07-06-molmo2-open-video-vlm]]（pointing 路线）；V*/SEAL（推理时 zoom 的代表，
  arXiv 2312.14135）；topics/inspection-anomaly-benchmark.md（巡检 benchmark 版图）。
- 后续追踪：ZwZ 的空间推理扩展版；R2I 用于业务数据的复刻实验（我们的下一步）。
