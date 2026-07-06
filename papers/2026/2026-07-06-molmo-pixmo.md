---
title: "Molmo and PixMo: Open Weights and Open Data for State-of-the-Art Vision-Language Models"
authors: "Matt Deitke, Christopher Clark et al. (AI2)"
venue: "arXiv 2409.17146 (CVPR 2025)"
published: "2024-09"
archived: "2026-07-06"
arxiv: "https://arxiv.org/abs/2409.17146"
code: "https://allenai.org/molmo"
topics: ["VLM / 多模态大模型", "开源模型"]
tags: ["open-weights", "open-data", "pointing", "dataset", "image-captioning"]
rating: "⭐⭐⭐⭐"
---

# Molmo and PixMo: Open Weights and Open Data for SOTA VLMs

> ⚠️ **来源说明**：基于 abstract + 公开摘要收录（Molmo2 系列的前作背景），未读原文正文。
> 作为系列脉络的第一篇，笔记从简；需要时可再深读补全。

## TL;DR
1. AI2 的全开放 VLM 一代：针对"开源 VLM 靠蒸馏闭源模型的合成数据"这一行业通病，
   证明**不用任何外部 VLM 的数据也能做到 SOTA**。
2. 核心是 **PixMo 数据集**：人工**口述**采集的高细节图像 caption（预训练）+ 自由 QA（微调）
   + 创新的 **2D pointing 数据集**（可验证接地的起点）。
3. Molmo-72B 在基准评测中拿到最高分，人类偏好评测第二，超过多数闭源与开源模型。

## 方法要点
- **口述式 caption 采集**：让标注员对着图像口头描述再转写——比打字获得远更长、
  更细的描述，是该系列数据方法论的起点。
- **2D pointing**：训练模型"用坐标指出答案在哪"，让回答可验证、可交互——
  这一能力在 Molmo2 中被扩展到视频（video pointing/tracking）。

## 我的评价
- 系列的**方法论奠基之作**：确立"人工高质量数据 + 全开放 + 不蒸馏闭源"三原则，
  以及 pointing 这一差异化能力。评价 Molmo2 的增量时以此为基线。

## 关联
- **二代**：[Molmo2 笔记](2026-07-06-molmo2-open-video-vlm.md)（视频理解+接地，本系列主笔记）。
- PixMo 数据集是社区复现"从零训 VLM"的常用资产。

**Sources**: [arXiv abs](https://arxiv.org/abs/2409.17146) · [HuggingFace paper page](https://huggingface.co/papers/2409.17146)
