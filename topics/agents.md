---
topic: "LLM / 多模态 Agent"
slug: "agents"
keywords: [LLM agent, multimodal agent, GUI agent, computer use, tool use, multi-agent, planning, agentic]
created: "2026-07-08"
last_tracked: "2026-09-09"
---

# 主题追踪：LLM / 多模态 Agent

## 这个方向在关注什么
GUI/computer-use agent 是当前最活跃的落地方向：怎么给 agent 造可验证的训练环境、
怎么设计过程奖励（process reward）、怎么从失败经验自我进化。CVPR 2026 数据显示
Agent 类论文占比 1.0%→2.8%（30→112 篇），正处早期放量段。

## 里程碑 / 必读论文
- [ ] SenseSearch（CVPR'26，RL 教 VLM 调用搜索/裁剪工具）— 见 topics/vlm.md 80 篇详析
- [ ] Ego2Web（CVPR'26，第一人称视频→web 任务基准）
- [ ] MolmoPoint-GUI + GUISyn（GUI grounding 基建）— 见 Molmo 系列分析

## 追踪记录

### 2026-09-09 · RSIH / RSI-Harness：harness 演化集群里少见的**能直接跑的开源实现**（代码库一手精读）
> 触发：用户给了 CosmosMind AI Lab 的三个源（论文 metarsi-v1.pdf / GitHub RSI-Harness / HF）。
> **论文 PDF 与 HF 两个域被本环境 egress proxy 拦截，未读到；论文标题公网零命中。** 以下只出自公开代码库。

- **RSIH（[CosmosMind-ai/RSI-Harness](https://github.com/CosmosMind-ai/RSI-Harness)）** —— 把 harness 配置做成
  一等公民产物 **Genome**：12 个字段所有权互斥的组件（instructions/tools/skills/commands/model/runtime/
  policies/integrations/appearance/settings/keybindings/resources）打成一个自包含目录，可版本化、可 diff、
  发给别人就能跑。建在 Pi coding agent 上，**不 fork core**；配置是 patch 语义（缺省即继承默认）。
  · 其中 `harness-rsi`（命令 `gee`）是**"造 Genome 的 Genome"**：读 RSIH/Pi/Claude Code 的真实 session 历史，
  先聚合（工具直方图、高频命令、反复出现的纠正）再选择性读原文，判定哪条该变 skill / tool / MCP / memory，
  **讲完整方案等用户确认后才落盘**。`src/` 里没有一行为它特设的代码——自指性是它的主要论据。
  · **落在 Weng 谱系的"优化 harness 代码"一级，但去掉自动搜索、换成人确认**——可看作 Meta-Harness(2603.28052)
  的低风险工程版。
  · ⚠️ **仓库自述"不包含 benchmark、数据生成、训练或评测实现"** → 没有 accept gate、没有 held-out 曲线，
  按 STOP / AHE / Self-Harness 的教训，"改进"目前无法证伪。同 org 另两个 repo（SWE-Prometheus 22 题、
  SWE-PolyVision 48 题）只放公开题面，验证补丁与结果全部不公开 → 若论文主实验建在其上，外部无法核分。
  · [笔记](../papers/2026/2026-09-09-rsih-genome-harness.md)
- **顺带捞到的邻近工作（未读，待验证）**：[HarnessBank 2607.13683](https://arxiv.org/abs/2607.13683)
  （semantic gene-bank search + gated verification for agent-harness self-evolution）——"基因库 + 门控验证"
  与 Genome 的隐喻高度撞车，但**它有 verification gate 而 RSIH 没有**，是最直接的对照组，优先深读。
  [Meta^n 2608.24735](https://arxiv.org/abs/2608.24735)（元操作固定、只递归扩张输入）同样待验。

### 2026-08-12 · ⭐ Harness 演化已成独立子赛道（WebSearch，abstract 级未深读）
> 触发：7-21 归档 Lilian Weng《Harness Engineering》后首次回扫。结论：这不再是"一篇综述 + 几个案例"，
> 而是**半年内至少 9 篇、8 月单周 2 篇**的成型集群，且已有配套开源实现。

**8 月新论文（本轮最值得跟的两篇）**
- **EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents**（2026-08-05）
  — 把 harness 状态抽象成统一的 **BPE workspace**（Belief 环境信念 / Progress 任务进度 / Experience 经验复用），
  用"监督 harness 微调 + cost-aware GRPO"把**何时读写外部状态**训成策略。
  ·（把 harness 从"人写的代码"变成"可训练的协调层"，是 Weng 谱系里"优化 harness 代码"的 RL 化身）
  · [arXiv 2608.05446](https://arxiv.org/abs/2608.05446)
- **EvolveNet: Collaborative Harness Evolution for Agent Self-Improvement**（2026-08-05，HKBU + USTC + HKUST）
  — 指出现有 harness 演化都假设"所有执行经验能汇到单个优化器"，现实里经验是**分散且不能汇集**的；
  于是做**联邦式演化**：共享 harness 广播到各数据本地客户端，各自在本地负载上演化出 specialist program，
  **只聚合程序改动、不聚合原始负载**，多路搜索并行、串行深度下降。5 个场景验证（text-to-SQL / 数据科学编码 / 竞赛编程 / SWE / agentic workflow）。
  ·（**最贴口味**：小而美的机制改动 + 直击工业落地的数据隔离痛点 + 出身好）
  · [arXiv 2608.04968](https://arxiv.org/abs/2608.04968)

**同一集群的前序工作（补齐谱系，此前库里只有 Weng 综述 + Self-Harness）**
- **Self-Harness: Harnesses That Improve Themselves** · [arXiv 2606.09498](https://arxiv.org/abs/2606.09498)（已在 watch）
- **HarnessX: A Composable, Adaptive, and Evolvable Agent Harness Foundry** · [arXiv 2606.14249](https://arxiv.org/abs/2606.14249)
- **DemoEvolve: Overcoming Sparse Feedback in Agentic Harness Evolution with Demonstrations** — 用示范解 harness 演化的稀疏反馈 · [arXiv 2605.24539](https://arxiv.org/abs/2605.24539)
- **EvoTrainer: Co-Evolving LLM Policies and Training Harnesses** — 策略与训练 harness 共同演化 · [arXiv 2606.03108](https://arxiv.org/abs/2606.03108)
- **From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws** — 从失败轨迹定位并修复 harness 缺陷 · [arXiv 2606.06324](https://arxiv.org/abs/2606.06324)
- **Code as Agent Harness** · [arXiv 2605.18747](https://arxiv.org/abs/2605.18747)
- **GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents** · [arXiv 2605.29668](https://arxiv.org/abs/2605.29668)
- **Adaptive Auto-Harness: Sustained Self-Improvement on Open-Ended Task Streams** · [arXiv 2606.01770](https://arxiv.org/abs/2606.01770)
  · ⚠️**待核**：我们 7-21 的 Weng 笔记里记的 AHE 是 arXiv 2604.25850，与此 ID 不同；是同名不同篇、还是笔记 ID 有误，需读原文确认。

**配套开源实现（git）**
- [iLearn-Lab/EvoHarness](https://github.com/iLearn-Lab/EvoHarness) — terminal-native agent 基础设施：tools / commands / skills / agents / plugins / MCP / memory / approvals + **controlled self-evolution**。
  ·（形态几乎就是"可自我演化版 Claude Code"，值得对着我们自己的 CLAUDE.md 工作流读）· ⚠️ star 数未核实（api.github.com 本环境 403）
- [A-EVO-Lab/a-evolve](https://github.com/A-EVO-Lab/a-evolve/tree/release/harness-evolution) — `release/harness-evolution` 分支，harness 演化实现

### 2026-07-08 · GUI / computer-use agent 近期新论文（WebSearch，abstract 级未深读）
- **VisCritic: Visual State Comparison as Process Reward for GUI Agents** — 用"动作前后视觉状态对比"当过程奖励训 GUI agent，奖励设计思路干净 · [arXiv 2606.24525](https://arxiv.org/abs/2606.24525) · ⭐口味高配
- **OpenComputer: Verifiable Software Worlds for Computer-Use Agents** — 给 CUA 造可验证的软件环境（训练+评测基建） · [arXiv 2605.19769](https://arxiv.org/abs/2605.19769)
- **R-WoM: Retrieval-augmented World Model for Computer-use Agents** — 检索增强的世界模型预测 GUI 状态转移，RAG×agent 交叉 · [arXiv 2510.11892](https://arxiv.org/abs/2510.11892)
- **UI-Voyager: Self-Evolving GUI Agent Learning via Failed Experience** — 从失败轨迹自我进化 · [arXiv 2603.24533](https://arxiv.org/abs/2603.24533)
- **Skill-Guided Continuation Distillation for GUI Agents** — 技能引导的续写蒸馏 · [arXiv 2606.18890](https://arxiv.org/abs/2606.18890)
- **ToolCUA** — GUI 操作与工具调用的最优路径编排 · [arXiv 2605.12481](https://arxiv.org/abs/2605.12481)
- **AliyunConsoleAgent** — 真实云控制台环境里蒸馏+RL 训 web agent（工业界实战） · [arXiv 2606.09447](https://arxiv.org/abs/2606.09447)
- **Hallucination Cascade** — 分析多 agent 系统中幻觉的级联传播（可靠性视角） · [arXiv 2606.07937](https://arxiv.org/abs/2606.07937)

## 当前判断
- **（2026-08-12 更新）harness 演化是本主题当前增速最快的支线**。半年成型，8 月单周 2 篇，
  且分化出两条互补路线：**EvoHarness-RL = 把 harness 使用训成策略（纵向做深）**，
  **EvolveNet = 让多方各自演化再合并（横向做广）**。前者对应 Weng 谱系的"优化 harness 代码"，
  后者提前解决了她文中没展开的**经验孤岛/数据不出域**问题——这恰好是企业落地的真门槛。
- GUI agent 的竞争焦点正从"模型"转向"**环境与奖励**"：可验证环境（OpenComputer）、
  过程奖励（VisCritic）、失败经验利用（UI-Voyager）——和 LLM RL 的演化路径一致。
- **VisCritic 最贴用户口味**（奖励设计的小而美），R-WoM 连接 RAG 主线，优先深读候选。
- 工业界开始拿真实生产环境训 agent（AliyunConsoleAgent），信号：赛道进入实用期。
