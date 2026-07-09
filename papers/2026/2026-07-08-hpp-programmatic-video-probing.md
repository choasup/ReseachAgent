---
title: "HPP: Hierarchical Programmatic Probing for Long Video Understanding by Decoupling Perception and Reasoning"
authors: "Awais Rauf, Ahmed Hasssan, Greg Slabaugh（疑似 QMUL Slabaugh 组，待核）"
venue: "arXiv 2606.21734"
published: "2026-06"
archived: "2026-07-08"
arxiv: "https://arxiv.org/abs/2606.21734"
code: "https://awaisrauf.com/hpp（项目页，本环境无法访问）"
topics: ["VLM / 多模态大模型", "长视频理解", "Agent/工具"]
tags: ["long-video", "training-free", "code-as-tool", "perception-reasoning-decoupling", "agentic"]
rating: "⭐⭐⭐⭐"
---

# HPP: Hierarchical Programmatic Probing for Long Video Understanding

> ⚠️ 来源：abstract 级（WebSearch；arXiv 原文被本环境屏蔽）。具体数字未检索到。

## TL;DR
1. 长视频理解的病根：VLM 把几千帧压成视觉 token，**感知和多步推理挤在同一次前向里**——
   LLM 的潜表征根本装不下"发现并执行多步策略"。
2. HPP 的解法：**把长视频理解改写成"写代码逐步探查视频"**——会写代码的 LLM 在交互式
   编码环境里规划多步策略，按需调用 VLM 对局部片段做感知（感知与推理彻底解耦）。
3. 三个组件：信息密度感知的层次化切分、late-interaction 语义检索、粗到细时序定位的
   结构化探查函数。LongVideoBench 平均 66.4、MLVU 71.8，EgoSchema 等上"匹敌或超过大一个数量级的模型"。

## 核心方法（管线）
```
长视频 → 信息密度感知的层次切分（树状索引）
问题 → LLM 写代码：检索相关段（late-interaction）→ 调 VLM 看局部 →
        根据返回结果决定下一步探查（粗→细迭代）→ 汇总作答
```
- 本质是 **CodeDance 思想（code-as-tool）在长视频上的实例化**：让代码承担"策略执行"，
  VLM 只干它擅长的"局部看图"。
- 无需训练新模型（组合现成 LLM+VLM），属 agentic pipeline 路线。

## 我的评价
- **亮点**：问题诊断精准（"一次前向装不下多步策略"），解法把每个组件放回其舒适区；
  与库里 Deeper Thought Weaker Aim（推理伤感知）互为印证——解耦是共同答案。
- **效率结论（重要）**：与标准帧采样比 token 用量——短视频略亏（探查开销），
  视频越长任务越难反转越狠，**最长最难任务上省至 16× token**；且计算随问题难度自适应
  （简单问题少迭代、时序复杂问题多探查）。
- **核心假设被验证**："把高阶时序推理外化为自适应的代码驱动探查，胜过在单次前向里
  扩大感知规模"——不 scale VLM 也能强。
- **存疑**：绝对延迟（多轮 LLM 调用的墙钟时间）未见报告；对编码能力强的 LLM 依赖重；
  70.4/69.3 两个数字与 VideoMME/EgoSchema 的对应关系未能核实。
- **对你的价值**：长视频/监控场景（如巡检的视频版）可以直接借这套"先索引再按需细看"的架构，
  避免整段视频塞 token。

## 关联
- 同期同思想扎堆（"解耦感知与推理"正在成为长视频共识）：MemDreamer（2606.07512，
  层次图记忆+agentic 检索）、VideoARM（2512.12360）、Decoupling Perception from Reasoning
  for Hallucination-Resistant Video Understanding（2511.18463）。
- 本库关联：CodeDance（code-as-tool）、DeepScan（分层扫描证据）、POINTS-Long（双模式效率）。
