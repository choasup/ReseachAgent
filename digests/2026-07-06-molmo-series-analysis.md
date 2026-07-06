---
period: "series-analysis"
range: "Molmo 系列（AI2）：2024-09 ~ 2026-05，5 篇"
generated: "2026-07-06"
---

# Molmo 系列纵向分析（AI2 全开放多模态路线）

> 来源：abstract + AI2 官方博客搜索摘要交叉印证（原文 PDF 被本环境屏蔽）。
> 单篇笔记见 papers/2026/（Molmo、Molmo2 已归档）。

## 系列全景

```
感知线（VLM）                                机器人线（ARM/VLA）
─────────────────────────────              ─────────────────────────
Molmo & PixMo (2024-09)                     MolmoAct 7B (2025-08)
  单图 VLM + 2D pointing                       "3D 空间里思考"的动作推理模型
  arXiv 2409.17146, CVPR 2025                  12K robot episodes, 成功率 72.1%
        │                                            │
        ▼                                            ▼
Molmo2 (2026-01)                            MolmoAct2 (2026-05)
  视频理解 + video pointing/tracking            真机部署：快 37x，双臂操作数据集
  9 个新数据集, 8B/4B(Qwen3) + O-7B(Olmo)      Think 变体：自适应深度推理
  接地任务超 Gemini 3 Pro                       arXiv 2605.02881
        │
        ▼
MolmoPoint (2026-03)
  pointing 的架构革命：grounding tokens
  8K 样本 = +20 F1；含 GUI 专用模型
  arXiv 2603.28069
```
另有变体：Molmo2-ER（具身推理特化，+300 万样本）、MolmoE（一代 MoE 版）。

## 三条不变的主线（系列哲学）

1. **全开放，不蒸馏闭源**：权重+数据+训练配方全放出，所有数据不经过闭源 VLM——
   这是和 Qwen-VL（只开权重）、LLaVA 系（依赖 GPT-4V 合成数据）的本质区别。
   系列存在的意义 = 给社区"从零造 VLM"的完整知识。
2. **Pointing 作为核心接口**：从一代 2D pointing → 二代视频 pointing/tracking →
   MolmoPoint 把它做成专用架构。"指出来"比"说出来"可验证、可交互，
   天然是 agent/机器人/GUI 的动作接口——这是该系列最独特的战略赌注。
3. **数据方法论 > 模型架构**：口述式 caption（打字→口述，长度和细节倍增）、
   人工标注 pointing、不用合成蒸馏。每一代的主要贡献都是"怎么采到好数据"。

## 技术演进的三级跳

| 阶段 | 解决什么 | 关键招 |
|---|---|---|
| Molmo/PixMo | 开源 VLM 靠蒸馏闭源的困局 | PixMo 人工数据 + 口述采集 |
| Molmo2 | 接地能力扩到时序（视频） | 9 数据集 + 双向视觉注意力 + token 加权 |
| MolmoPoint | 坐标文本输出的低效（难学的坐标系 + 高 token 数） | **grounding tokens**：`<PATCH>→<SUBPATCH>→<LOCATION>` 粗到细直接选视觉 token |

MolmoPoint 是系列里最"小而美"的一步：把 pointing 从"生成坐标字符串"改成
"注意力选 token"，**8,192 个训练样本就比 baseline 高约 20 F1**，预训练收敛更快——
典型的"改表示而非堆数据"。

## 对你口味的价值点（按优先级）

1. **MolmoPoint-GUI-8B + GUISyn 数据集**（36K 高分屏截图、200 万+标注点）——
   这直接是 **GUI agent 的 grounding 基建**，与你的 agent 主线强相关，现成可用。
2. **Molmo2 的数据配方**：口述式视频 caption（平均 900+ 词/段）、message-tree 编码、
   packing 技巧——做多模态后训练的可复制方法论。
3. **grounding tokens 的思想**：输出空间从文本坐标改成视觉 token 选择，
   这个"换表示"思路可迁移到任何需要空间输出的 VLM 任务。
4. MolmoAct 线（VLA）按你偏好降权，但注意：它证明 pointing 接口能一路通到机器人控制，
   若日后关注具身可回头看。

## 批评与存疑

- **评测选择性**：pointing/tracking 是 AI2 自己定义并深耕的任务，
  "超 Gemini 3 Pro"的惊艳数字集中于此；通用视频 QA 上与顶级闭源差距仍在（长视频仅 competitive）。
- **规模上限**：系列主力停在 7B/8B（一代有 72B），"全开放"路线在算力上限上的竞争力待观察。
- **人工数据的扩展性**：口述采集质量高但贵，能否跟上数据需求的增长是长期问题。
- 各代具体消融（双向注意力、token 加权的真实贡献）**原文未读到**，待核。

## 一句话总结

> Molmo 系列是"**开放 + 可验证接地**"路线的最完整实践：用人工数据方法论替代闭源蒸馏，
> 用 pointing 把 VLM 的输出从"话"变成"可执行的动作接口"，并沿着
> 图像→视频→GUI→机器人一路把这个接口铺下去。**看懂 Molmo 系列 ≈ 看懂开放多模态的一条完整技术路线。**

## 链接
- Molmo/PixMo: https://arxiv.org/abs/2409.17146 · [笔记](../papers/2026/2026-07-06-molmo-pixmo.md)
- Molmo2: https://arxiv.org/abs/2601.10611 · [笔记](../papers/2026/2026-07-06-molmo2-open-video-vlm.md)
- MolmoPoint: https://arxiv.org/abs/2603.28069 · [AI2 博客](https://allenai.org/blog/molmopoint)
- MolmoAct2: https://arxiv.org/abs/2605.02881 · [GitHub](https://github.com/allenai/molmoact2)
- 系列主页: https://allenai.org/molmo
