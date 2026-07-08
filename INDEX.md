# 知识库索引 INDEX

> 本文件是整个知识库的总目录，**每次新增/修改论文解读后同步更新**。
> 按主题分组；每行格式：`论文标题 · 一句话结论 · [笔记](路径) · tags`。

_最后更新：2026-07-08_

## 统计
- 已归档论文：4
- 追踪主题：2（vlm + agents）

## 按主题

### Agent / 过程奖励
- **VisCritic** (投稿 ECCV'26) · 动作前后截图差分当步级奖励：Siamese ViT + 零人工标注 + 推理期即插即用 · [笔记](papers/2026/2026-07-08-viscritic-visual-process-reward.md) · `GUI-agent` `process-reward` `plug-and-play`

### 开源 VLM / 视频理解
- **Molmo2** (AI2) · 全开放（权重+数据+配方）视频 VLM：9 个新数据集不蒸馏闭源模型，8B 在 video pointing/tracking 上超 Gemini 3 Pro (F1 38.4 vs 20.0) · [笔记](papers/2026/2026-07-06-molmo2-open-video-vlm.md) · `open-weights` `video-grounding` `pointing` `dataset`
- **Molmo and PixMo** (AI2, CVPR 2025) · 系列一代：口述式高质量 caption + 2D pointing，证明不蒸馏闭源也能 SOTA · [笔记](papers/2026/2026-07-06-molmo-pixmo.md) · `open-weights` `pointing` `dataset`

### 工业异常检测 / 多模态 VLM
- **ADSeeker** (CVPR 2026) · 用图文知识库 SEEK-M&V + Q2K RAG 把领域知识注入 VLM 做零样本异常检测与推理，发布最大规模 IAD 数据集 MulA(26类/72缺陷型) · [笔记](papers/2026/2026-06-30-adseeker-knowledge-grounded-ad.md) · `industrial-anomaly-detection` `VLM` `RAG` `zero-shot` `dataset`

## 按时间线
<!-- 最近归档的在最上面 -->
- 2026-07-08 · **VisCritic** — 视觉状态对比做 GUI agent 过程奖励 · [笔记](papers/2026/2026-07-08-viscritic-visual-process-reward.md)
- 2026-07-06 · **Molmo2** — AI2 全开放视频 VLM（pointing/tracking 超 Gemini 3 Pro） · [笔记](papers/2026/2026-07-06-molmo2-open-video-vlm.md)
- 2026-07-06 · **Molmo and PixMo** — 系列一代，开放 VLM 方法论奠基 · [笔记](papers/2026/2026-07-06-molmo-pixmo.md)
- 2026-06-30 · **ADSeeker** — 知识注入的工业异常检测与推理框架 · [笔记](papers/2026/2026-06-30-adseeker-knowledge-grounded-ad.md)
