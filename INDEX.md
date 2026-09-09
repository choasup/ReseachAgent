# 知识库索引 INDEX

> 本文件是整个知识库的总目录，**每次新增/修改论文解读后同步更新**。
> 按主题分组；每行格式：`论文标题 · 一句话结论 · [笔记](路径) · tags`。

_最后更新：2026-09-09_

## 统计
- 已归档论文：9
- 追踪主题：2（vlm + agents）

## 按主题

### Agent / Harness / 自我改进
- **RSIH / RSI-Harness** (CosmosMind AI Lab, 2026-09) · 把 harness 配置做成可版本化/可分享的 **Genome**（12 组件 + patch 语义），`harness-rsi` 是"造 Genome 的 Genome"——**⚠️ 论文 PDF 与 HF 被网络策略拦截未读到，仓库自述无 benchmark/评测，"改进"尚不可证伪** · [笔记](papers/2026/2026-09-09-rsih-genome-harness.md) · `harness` `RSI` `genome` `论文未读`
- **Harness Engineering for Self-Improvement** (Lilian Weng, Lil'Log 2026-07) · harness 是 RSI 的近期路径：优化谱系 prompt→上下文→workflow→harness代码→优化器代码，全文精读 · [笔记](papers/2026/2026-07-21-lilian-weng-harness-engineering.md) · `harness` `RSI` `survey`

### Agent / 过程奖励
- **VisCritic** (投稿 ECCV'26) · 动作前后截图差分当步级奖励：Siamese ViT + 零人工标注 + 推理期即插即用 · [笔记](papers/2026/2026-07-08-viscritic-visual-process-reward.md) · `GUI-agent` `process-reward` `plug-and-play`

### VLM 前沿方法
- **ZwZ / Zooming without Zooming** (ICML 2026, SJTU+蚂蚁) · 把 zoom 变训练原语：微裁剪出题蒸回全图 + DAPO，74K 数据单次前向拿细粒度感知（ZoomBench +20、比工具法快10×）——我们实测巡检召回翻倍 · [笔记](papers/2026/2026-07-10-zwz-region-to-image-distillation.md) · `fine-grained` `distillation` `RL` `zoom`
- **HPP** · 长视频理解改写成"LLM 写代码逐步探查视频"，感知与推理解耦，LongVideoBench 等大幅提升 · [笔记](papers/2026/2026-07-08-hpp-programmatic-video-probing.md) · `long-video` `training-free` `code-as-tool`
- **World2VLM** · 世界模型合成未来视角当训练监督，把"想象力"蒸馏进 VLM——推理期零额外开销反超 test-time 方法 · [笔记](papers/2026/2026-07-08-world2vlm-imagination-distillation.md) · `world-model` `distillation` `spatial`

### 开源 VLM / 视频理解
- **Molmo2** (AI2) · 全开放（权重+数据+配方）视频 VLM：9 个新数据集不蒸馏闭源模型，8B 在 video pointing/tracking 上超 Gemini 3 Pro (F1 38.4 vs 20.0) · [笔记](papers/2026/2026-07-06-molmo2-open-video-vlm.md) · `open-weights` `video-grounding` `pointing` `dataset`
- **Molmo and PixMo** (AI2, CVPR 2025) · 系列一代：口述式高质量 caption + 2D pointing，证明不蒸馏闭源也能 SOTA · [笔记](papers/2026/2026-07-06-molmo-pixmo.md) · `open-weights` `pointing` `dataset`

### 工业异常检测 / 多模态 VLM
- **ADSeeker** (CVPR 2026) · 用图文知识库 SEEK-M&V + Q2K RAG 把领域知识注入 VLM 做零样本异常检测与推理，发布最大规模 IAD 数据集 MulA(26类/72缺陷型) · [笔记](papers/2026/2026-06-30-adseeker-knowledge-grounded-ad.md) · `industrial-anomaly-detection` `VLM` `RAG` `zero-shot` `dataset`

## 按时间线
<!-- 最近归档的在最上面 -->
- 2026-09-09 · **RSIH / RSI-Harness**（CosmosMind）— Genome 化的可分享 harness；论文未读到，仅代码库精读 · [笔记](papers/2026/2026-09-09-rsih-genome-harness.md)
- 2026-07-21 · **Harness Engineering**（Lilian Weng）— harness 综述，全文精读 · [笔记](papers/2026/2026-07-21-lilian-weng-harness-engineering.md)
- 2026-07-08 · **HPP** — 程序化探查解耦长视频感知与推理 · [笔记](papers/2026/2026-07-08-hpp-programmatic-video-probing.md)
- 2026-07-08 · **World2VLM** — 世界模型想象力蒸馏进 VLM · [笔记](papers/2026/2026-07-08-world2vlm-imagination-distillation.md)
- 2026-07-08 · **VisCritic** — 视觉状态对比做 GUI agent 过程奖励 · [笔记](papers/2026/2026-07-08-viscritic-visual-process-reward.md)
- 2026-07-06 · **Molmo2** — AI2 全开放视频 VLM（pointing/tracking 超 Gemini 3 Pro） · [笔记](papers/2026/2026-07-06-molmo2-open-video-vlm.md)
- 2026-07-06 · **Molmo and PixMo** — 系列一代，开放 VLM 方法论奠基 · [笔记](papers/2026/2026-07-06-molmo-pixmo.md)
- 2026-06-30 · **ADSeeker** — 知识注入的工业异常检测与推理框架 · [笔记](papers/2026/2026-06-30-adseeker-knowledge-grounded-ad.md)
