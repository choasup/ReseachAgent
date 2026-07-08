---
topic: "LLM / 多模态 Agent"
slug: "agents"
keywords: [LLM agent, multimodal agent, GUI agent, computer use, tool use, multi-agent, planning, agentic]
created: "2026-07-08"
last_tracked: "2026-07-08"
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
- GUI agent 的竞争焦点正从"模型"转向"**环境与奖励**"：可验证环境（OpenComputer）、
  过程奖励（VisCritic）、失败经验利用（UI-Voyager）——和 LLM RL 的演化路径一致。
- **VisCritic 最贴用户口味**（奖励设计的小而美），R-WoM 连接 RAG 主线，优先深读候选。
- 工业界开始拿真实生产环境训 agent（AliyunConsoleAgent），信号：赛道进入实用期。
