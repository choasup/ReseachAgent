---
title: "Harness Engineering for Self-Improvement"
authors: "Lilian Weng"
venue: "Lil'Log 博客（2026-07-04，31 分钟长文）"
published: "2026-07"
archived: "2026-07-21"
arxiv: ""
code: "https://lilianweng.github.io/posts/2026-07-04-harness/"
topics: ["Agent/harness", "自我改进/RSI", "工作流合成"]
tags: ["harness", "RSI", "self-improvement", "survey", "context-engineering", "evolutionary-search"]
rating: "⭐⭐⭐⭐⭐"
---

# Harness Engineering for Self-Improvement（Lilian Weng 综述）

> ✅ 本篇为**全文一手精读**（GitHub Pages raw 通道抓取完整 HTML，非摘要级）。

## TL;DR
1. 论点：**harness（模型外围的编排系统）与裸模型智能同等重要**，是递归自我改进（RSI）
   的近期现实路径——RSI 不会从"模型改自己权重"开始，会从"模型改自己的 harness"开始。
2. 给出优化对象的演进谱系：**prompt → 结构化上下文 → workflow → harness 代码 → 优化器代码**，
   并系统梳理每级的代表工作（ACE/MCE/Meta-Harness、ADAS/AFlow、STOP/Self-Harness/AHE、
   AlphaEvolve/DGM、SIA）。
3. 七大未决挑战：弱评估器、记忆生命周期、负结果偏差、多样性坍缩、reward hacking、
   长期健康度、人类角色上移。

## 三个 Harness 设计模式
1. **Workflow 自动化**：目标导向的 plan→execute→observe→improve 循环，agent 分析自己的轨迹迭代。
2. **文件系统当持久记忆**：长程任务的状态/日志/产物放文件不塞上下文；读写文件是模型的
   预训练基本功，harness 借文件系统"免费"继承模型能力增长。
3. **子代理与后台任务**：并行假设搜索、隔离子任务；关键设计是**并行显式化、可查**（落文件
   而非藏在临时对话里，中断可恢复）。
- 案例：coding agent 的工具面已跨产品收敛（文件/shell/git/MCP/子代理/定时任务）。
- 关键预测：harness 改进最终会被内化进模型（如 prompt 工程的先例），但**与外部世界的接口层永存**。

## 优化谱系（核心贡献）
- **上下文工程**：ACE（playbook 化：Generator/Reflector/Curator，条目化防 context collapse）
  → MCE（双层：机制 vs 内容分离，skill 演化 + 上下文优化，2601.21557）
  → Meta-Harness（"优化 harness 的 harness"，输出 Pareto 前沿候选，2603.28052）。
- **Workflow 设计**：手工（AI Scientist@Nature 2026、ScientistOne 的 Chain-of-Evidence、
  Autodata 的 challenger/solver/verifier）→ 搜索（ADAS meta-agent 编程、AFlow MCTS）。
- **自改进 harness**：
  - STOP（2023 奠基：改进"改进器"；**警示：弱模型递归会退化**——递归结构不够，底座智能是前提）；
  - **Lin et al. 2026 关键解耦**：harness-updating（写 harness 的能力）从 Qwen3.5-9B 到
    Opus 4.6 **几乎持平**；harness-benefit（用好 harness 的能力）**非单调，中档模型受益最大**；
  - Self-Harness（weakness mining → 有界提案 → held-in/held-out 双重回归验证，2606.09498）；
  - **AHE**（可观测性三支柱：组件/经验/决策全部文件化，每次编辑=可证伪的预测；**权限外置**
    （runs/验证器/模型配置只读）防 reward hacking；TerminalBench-2 上超过 OpenCode/Terminus-2/
    Codex 等人工 harness，冻结后迁移 SWE-bench 不掉——**证明学到的是工程经验不是过拟合**，2604.25850）。
- **进化搜索**：Promptbreeder/GEPA → AlphaEvolve（EVOLVE-BLOCK 标记 + meta-prompt 共进化）
  → ShinkaEvolve（采样效率三件套）→ **DGM**（agent 改自己的 harness 仓库，SWE-bench 20%→50%）。
  适用边界：评估快且客观的域好使；评估慢/模糊的域挣扎。
- **与权重联合优化**：SIA（她明确点出实验混淆，"方向有趣、证据临时"）、Continual Harness。

## 七大挑战（她的清单）
弱评估器（research taste 无 verifier）/ 记忆生命周期（她预测**上下文工程终将内化为智能本身**）/
负结果偏差（文献只发成功，模型不会放弃假设；harness 应让失败易于保存）/ 多样性坍缩 /
reward hacking（评估器与权限必须在演化环外）/ 长期健康度（RLVR 抓不到可维护性/迁移成本）/
人类上移而非移除。

## 我的评价
- **价值**：这是 harness 这个新兴领域的第一篇系统综述，参考文献表就是完整 reading list；
  "优化对象谱系"一图值千金；她对弱证据工作（SIA）的点名批评展示了综述的判断力。
- **与本库的强共振**：AFlow/ADAS 正是我们上周聊的工作流合成线（耦合搜索那篇的上游）；
  AHE 的"证据驱动编辑"与 VisCritic/巡检 v1 的差分思想同源；"负结果保存"正是本库
  "不臆造、如实标注"约定的理论依据；文中三大设计模式（文件持久记忆/子代理/后台任务）
  恰好就是本知识库会话的工作方式。
- **可跟进**：Appendix 的基准清单（PaperBench/RE-Bench/MLE-bench/KernelBench 等）可直接
  用于评估自动研究 agent；AHE（2604.25850）与 Self-Harness（2606.09498）值得深读。

## 关联
- 本库：topics/agents.md（工作流合成线）、VisCritic 笔记（过程奖励）、
  digests/2026-07-06-mllm-benchmark-guide.md（评测三层塔 vs 她的"弱评估器"挑战）。
- 关键引文：ACE (ICLR'26)、MCE (2601.21557)、Meta-Harness (2603.28052)、AHE (2604.25850)、
  Self-Harness (2606.09498)、DGM (2505.22954)、AlphaEvolve (2506.13131)、AI Scientist (Nature 651)。
