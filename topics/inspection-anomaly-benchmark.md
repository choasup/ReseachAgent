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

## 追踪记录

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

## 当前判断
- **空位明确**：工业质检（MMAD，近拍单物体）和视频监控（FoodMonitor/SurveillanceVQA，
  时序+定位）两头都有了，但"**远距监控单帧、多目标、开放场景的巡检判断**"
  （即我们 Inspection v0 的形态）没有公开学术 benchmark——我们的数据（26k 张
  已标注门店巡检图）在这个空位上有真实价值。
- 学界结论一致：SOTA MLLM（含闭源）在此类任务上 0.36~0.75，均未达业务可用；
  空间定位与细粒度异常发现是共同瓶颈——与我们测得的"系统性漏报"互证。
- 值得深读：MMAD（题型设计/判分协议可借鉴出题）、FoodMonitor（规则驱动+
  双通道标注结构可借鉴 v1 升级）。
