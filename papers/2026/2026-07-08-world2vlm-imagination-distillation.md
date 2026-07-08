---
title: "World2VLM: Distilling World Model Imagination into VLMs for Dynamic Spatial Reasoning"
authors: "待核（arXiv 2604.26934）"
venue: "arXiv 2604.26934"
published: "2026-04"
archived: "2026-07-08"
arxiv: "https://arxiv.org/abs/2604.26934"
code: "论文称已开源代码与数据集（链接待核）"
topics: ["VLM / 多模态大模型", "世界模型", "空间推理"]
tags: ["world-model", "distillation", "spatial-reasoning", "data-synthesis", "post-training"]
rating: "⭐⭐⭐⭐"
---

# World2VLM: Distilling World Model Imagination into VLMs

> ⚠️ 来源：abstract 级（WebSearch；arXiv 原文被本环境屏蔽）。具体数字未检索到。

## TL;DR
1. VLM 静态理解强，但**动态空间推理**（想象自己移动后场景怎么变）很弱——缺"想象力"。
2. World2VLM：**训练时**用视图一致的生成式世界模型合成"未来视角"，构造双向监督
   （正向：动作→结果；逆向：结果→动作），两阶段 post-training 蒸馏进 VLM。
3. 关键卖点：**把世界模型的开销留在训练期**——推理时就是普通 VLM，
   却在 SAT-Real/SAT-Synthesized/VSI-Bench/MindCube 上超过"推理期挂世界模型"的方法。

## 核心方法
```
初始观测 + 参数化相机轨迹
  → 视图一致世界模型合成几何对齐的未来帧
  → 自动生成双向 QA 监督（forward: 这样动会看到什么 / inverse: 看到这些说明怎么动了）
  → 紧凑数据集上两阶段 post-training
```
- 数据是**程序化合成**的（世界模型当"标注员"），无需人工空间标注。
- 与 test-time 世界模型方法（如 Thinking with Imagination, 2606.06476）形成路线对照：
  **训练期蒸馏 vs 推理期想象**——本文证明前者更省且更强（据 abstract）。

## 我的评价
- **亮点**：架构上一分钱不加（推理就是原 VLM），把贵的东西（世界模型生成）全部
  摊销到训练数据构造里——**"用生成模型造监督"** 与 PixMo"用人工造监督"、
  ReasonX"用 MLLM-judge 造监督"同属一个大范式：监督信号工程。
- **存疑**：世界模型合成质量的上限就是学生的上限（幻觉传染风险）；"compact dataset"
  多大、两阶段配方细节、对非自我中心运动的泛化，均待读原文。
- **对你的价值**：动态空间推理是具身/视频的基础能力；这条"训练期蒸馏"路线比
  推理期挂重模型的方案工程上友好得多。

## 关联
- 对照路线：Thinking with Imagination（2606.06476，推理期世界模拟器做 agentic 空间推理）。
- 本库关联：VOLD（LLM→VLM 推理蒸馏，同为"迁移能力"）、DSR Suite（4D 先验注入）、
  Self-Evolving Spatial Reasoning（2605.18162，几何一致性自监督）。
- 大图景：世界模型占比翻倍（CVPR 2026 趋势分析 0.45%→0.89%），此文是"世界模型当工具用"
  而非"造世界模型"的代表。
