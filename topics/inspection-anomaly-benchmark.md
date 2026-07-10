---
topic: "巡检/异常检测的 VLM Benchmark"
slug: "inspection-anomaly-benchmark"
keywords: ["industrial anomaly detection benchmark", "MLLM anomaly detection", "surveillance video anomaly", "compliance analysis benchmark", "inspection VLM"]
created: "2026-07-09"
last_tracked: "2026-07-09"
---

# 主题追踪：巡检/异常检测的 VLM Benchmark

## 这个方向在关注什么
用 VLM/MLLM 做"发现异常/违规"类任务的评测：工业质检缺陷、监控视频异常、
门店/厨房合规巡检。与我们自建的 Inspection benchmark（餐饮门店单帧巡检，
benchmarks/vlm-baseline）直接相关——学术界结论与我们一致：**现有 MLLM 在
无提示异常发现上远未达到可用水平**。

## 里程碑 / 必读论文
- [ ] **MMAD**（ICLR 2025）— 工业 IAD 的 MLLM benchmark 事实标准
- [ ] **FoodMonitor**（2026-05）— 商用厨房监控合规，与我们业务场景几乎对口
- [ ] **ZwZ / Zoom-Bench**（ICML 2026）— 巡检漏报问题的解法蓝本（重点追踪）
- [ ] **MME-RealWorld**（ICLR 2025）— 高分辨率真实场景（含监控域）标杆（重点追踪）
- [ ] **RealWorldQA**（xAI）— 已在我们评测矩阵，持续对比（重点追踪）

## 追踪记录

### 2026-07-09（设立三个重点追踪对象，补充动态）
- **ZwZ / Zoom-Bench 详情**（上海交大 + 蚂蚁，ICML 2026）— Region-to-Image 蒸馏：
  把"agentic zooming"从推理时工具内化为训练原语（单次前向），RL(DAPO) + 仅 74K
  合成数据；**基座正是 Qwen3-VL-4B/8B、Qwen2.5-VL-7B**（我们矩阵同款），开源模型
  细粒度感知 SOTA · [arXiv 2602.11858](https://arxiv.org/abs/2602.11858) ·
  [code](https://github.com/inclusionAI/Zooming-without-Zooming) · **已 /paper**（papers/2026/2026-07-10-zwz-region-to-image-distillation.md）
  ⭐⭐ 我们巡检"漏报"的直接解法蓝本：ZwZ-8B 可作巡检微调起点或直接拿来测。
- **MME-RealWorld 生态**：有 **Lite 版**（每任务 50 样本，VLMEvalKit / lmms-eval
  原生支持——可低成本加入我们矩阵）与 **CN 中文版**（5,917 中文场景 QA，更贴
  我们业务）；同系 Video-MME（CVPR 2025）·
  [HF Lite](https://huggingface.co/datasets/yifanzhang114/MME-RealWorld-Lite) ·
  [GitHub](https://github.com/MME-Benchmarks/MME-RealWorld)
- **RealWorldQA 动态**：榜单当前由 Qwen3.6 Plus 领先（0.854）；数据集 CC BY-ND ·
  [HF](https://huggingface.co/datasets/xai-org/RealworldQA) ·
  [解读](https://huggingface.co/blog/KennyUTC/realworldqa)

### 2026-07-09（首次梳理，按与我们场景的相关度排序）
- **FoodMonitor: Benchmarking MLLMs for Explainable Compliance Analysis** —
  商用厨房监控合规分析：477 段 60s 视频、3,307 条违规标注、8 类 27 项检查项、
  人员级+环境级双通道、要求时空定位；评 11 个 MLLM（含 Qwen3-VL、GLM-4.6V、
  Gemini-3、Doubao-Seed-2.0），**最佳综合分仅 0.360**，空间定位是主要瓶颈 ·
  [arXiv 2605.24503](https://arxiv.org/html/2605.24503) · 未 /paper
  ⭐ 与我们的 Inspection v0 最对口（他们视频+定位，我们单帧+判断），结论互证。
- **MMAD: A Comprehensive Benchmark for MLLMs in Industrial Anomaly Detection**
  （ICLR 2025）— 39,672 题 / 8,366 张工业图，7 个子任务（异常判别/定位/描述等），
  底料含 MVTec-AD/VisA；GPT-4o 平均 74.9%，"远未达工业要求" ·
  [arXiv 2410.09453](https://arxiv.org/abs/2410.09453) ·
  [code](https://github.com/jam-cc/MMAD) · 未 /paper
- **SurveillanceVQA-589K** — 589K QA 的监控视频理解 benchmark（含异常理解），
  规模最大 · [arXiv 2505.12589](https://arxiv.org/pdf/2505.12589) · 未 /paper
- **Benchmarking Compact VLMs for Clip-Level Surveillance Anomaly Detection**
  （2025-11）— 小型 VLM 做 CCTV 片段级异常检测的统一评测协议 ·
  [MDPI](https://www.mdpi.com/2313-433X/11/11/400) · 未 /paper
- **The Evolution of Video Anomaly Detection: DNN→MLLM（综述）** —
  视频异常检测到 MLLM 时代的统一框架综述 ·
  [arXiv 2507.21649](https://arxiv.org/pdf/2507.21649) · 未 /paper
- 传统底料（非 QA 型）：**MVTec-AD**（5,354 图/15 类工业品缺陷）、
  **VisA**（10,821 图/12 类）像素级 AD；**UCF-Crime / XD-Violence** 监控视频异常；
  PPE/hygiene 目标检测数据集（31k 图，YOLO 系）；planogram compliance（货架陈列 CV）。
  方法线：WinCLIP、AnomalyGPT（AAAI'24）、FADE 等 zero-shot AD。

### 2026-07-09（补充：真实图像理解场景线）
- **MME-RealWorld**（ICLR 2025）— 最大人工标注高分辨率真实场景 benchmark：
  13,366 张图（均 2000×1500）、29,429 QA、43 子任务、5 域，**内含"视频监控
  (Monitoring)"子域**；28 个 SOTA MLLM（GPT-4o/Gemini/Claude）**无一达 60%** ·
  [arXiv 2408.13257](https://arxiv.org/abs/2408.13257) ·
  [code](https://github.com/MME-Benchmarks/MME-RealWorld) · 未 /paper
  ⭐ 与我们巡检最直接的公共对标（监控域+高分辨率+人都觉得难）。
- **V\*Bench / SEAL**（CVPR 2024）— 高清拥挤场景找小物体（191 图，均 2246×1582）；
  提出 LLM 引导的视觉搜索机制（先搜索定位再回答）·
  [arXiv 2312.14135](https://arxiv.org/abs/2312.14135) · 未 /paper
  ⭐ "先找后判"机制可作巡检 v1 的方法对照组。
- **Zoom-Bench**（2026）— 845 题，专测"决定性视觉证据极小、被全局上下文淹没"
  的细粒度感知——正是我们垃圾桶/客区漏报的学术形态 ·
  [via VisualNeedle 引用](https://arxiv.org/pdf/2605.26380) · 未 /paper
- **VisualNeedle**（2026-05）— 信息密集场景的主动视觉搜索 benchmark ·
  [arXiv 2605.26380](https://arxiv.org/pdf/2605.26380) · 未 /paper
- **HRScene** — 25 个真实数据集统一的高分辨率理解评测（1K~35K 分辨率），
  VLM 均分仅 49.7% · [arXiv 2504.18406](https://arxiv.org/html/2504.18406) · 未 /paper
- **HR-Bench**（4K/8K）— 超高分辨率单实例/跨实例细粒度感知；
  **CVSearch**（2026-05）认知视觉搜索 · [arXiv 2605.23655](https://arxiv.org/pdf/2605.23655)
- 相关经典：RealWorldQA（已在我们矩阵）、MMVP（CLIP-blind 细粒度视觉缺陷）、BLINK（低层感知）。

## 当前判断
- **空位明确**：工业质检（MMAD，近拍单物体）和视频监控（FoodMonitor/SurveillanceVQA，
  时序+定位）两头都有了，但"**远距监控单帧、多目标、开放场景的巡检判断**"
  （即我们 Inspection v0 的形态）没有公开学术 benchmark——我们的数据（26k 张
  已标注门店巡检图）在这个空位上有真实价值。
- 学界结论一致：SOTA MLLM（含闭源）在此类任务上 0.36~0.75，均未达业务可用；
  空间定位与细粒度异常发现是共同瓶颈——与我们测得的"系统性漏报"互证。
- 值得深读：MMAD（题型设计/判分协议可借鉴出题）、FoodMonitor（规则驱动+
  双通道标注结构可借鉴 v1 升级）。
- **真实图像理解线的定位**：我们巡检测出的"系统性漏报"，在学术上对应
  "高分辨率小目标细粒度感知/视觉搜索"缺陷（MME-RealWorld 监控域无一过 60%、
  HRScene 均分 49.7%、V*/Zoom-Bench 专攻此点）——证据链完整。两个可执行动作：
  ① 把 MME-RealWorld(-Lite) 加进评测矩阵做公共对照（VLMEvalKit 原生支持）；
  ② 巡检 v1 增加 V*/SEAL 式"先搜索后回答"方法对照组，验证 zoom-in 能挽回多少召回。
