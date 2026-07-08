---
title: "VisCritic: Visual State Comparison as Process Reward for GUI Agents"
authors: "待核（arXiv 2606.24525）"
venue: "arXiv 2606.24525（投稿 ECCV 2026）"
published: "2026-06"
archived: "2026-07-08"
arxiv: "https://arxiv.org/abs/2606.24525"
code: ""
topics: ["LLM / 多模态 Agent", "GUI agent", "过程奖励"]
tags: ["GUI-agent", "process-reward", "plug-and-play", "inference-time", "weak-supervision"]
rating: "⭐⭐⭐⭐"
---

# VisCritic: Visual State Comparison as Process Reward for GUI Agents

> ⚠️ 来源：abstract 级（WebSearch；arXiv 原文被本环境屏蔽）。具体数字未检索到，待读原文。

## TL;DR
1. GUI agent 长程任务容易走偏，缺**步级校验**：每一步动作到底成没成功，没人告诉它。
2. VisCritic 的解法：**直接对比动作前后的两张截图**（视觉特征空间），
   用 Siamese ViT 抽"变化感知"表征 + Action-Aware Critic Head 联合判断
   动作成功与否 / 任务进度 / 错误类型。
3. **即插即用的推理期模块**：不训 agent 本体；critic 的训练数据从已有轨迹弱监督自动构造，
   **零额外人工标注**。在 5 个基准上对多种 GUI agent 普遍有提升（具体数字待核）。

## 背景与问题
- GUI agent 靠 outcome reward（任务最终成败）训练/运行，长程任务中间步骤出错无法及时发现，
  错误累积直至失败；步级 process reward 又通常需要昂贵的人工步级标注。

## 核心方法
- **信号来源**：不问模型"你觉得这步对吗"（易幻觉），而是看**世界的变化**——
  pre-action / post-action 截图对比。点了按钮页面没变 = 动作失败，这是客观证据。
- **架构**：Siamese vision transformer 双塔抽两张截图的 change-aware 表征；
  Action-Aware Critic Head 以动作为条件，联合输出：动作是否成功、任务进度、错误类型。
- **数据**：从现有 agent 轨迹弱监督构造 critic 训练样本（无新人工标注）。
- **用法**：推理期挂在任意 GUI agent 旁边做步级验证/诊断（plug-and-play）。

## 主要结果
- 5 个基准、多种 GUI agent 上普遍提升 + 提供可视化诊断线索（具体数字未检索到，待原文）。

## 局限与存疑
- 提升幅度未知（abstract 未给数字）；critic 自身的误判率、对"页面变化但语义失败"
  （如弹了个错误对话框）的判别能力待核。
- 弱监督标签质量依赖既有轨迹的多样性。

## 我的评价
- **亮点**：把"步级奖励"从主观判断改成**客观的世界状态差分**——思想干净；
  零人工标注 + 推理期即插即用，完全命中"小而美+工程化"。
- **与用户业务的直接关联**：巡检 benchmark（Inspection v0）发现通用 VLM 系统性漏报，
  而 VisCritic 的"对比出变化"正是同一思想的另一面——**"正常参照 vs 当前画面"的
  对比协议可以直接借用其 Siamese 差分架构**。做 Inspection v1 时值得参考。
- 值得深读：是（重点看 5 基准数字、错误类型分类的粒度、critic 误判分析）。

## 关联（同赛道竞品，2026 上半年扎堆）
- GUI-Shepherd（2509.23738）：长序列 GUI 任务的过程奖励与验证
- StainFlow（2606.07027）：实体染色追踪 + 证据链接做过程奖励
- Adaptive Milestone Reward（2602.11524）：自适应里程碑奖励
- Video-Based Reward Modeling for CUA（2603.10178）：视频奖励建模
- 本库关联：topics/agents.md 追踪记录；巡检 benchmark 见 benchmarks/vlm-baseline/results/INSPECTION_REPORT.md
