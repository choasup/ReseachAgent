---
title: "MetaRSI / RSI²: A Meta-Recursive Self-Improving System for Recursive Self-Improving Systems Themselves"
authors: "CosmosMind AI Lab（作者名单未读到）"
venue: "自托管 PDF（www.cosmosmind.ai），无 arXiv 记录、无第三方索引"
published: "未知（GitHub 仓库 2026-09-08 更新）"
archived: "2026-09-09"
arxiv: ""
code: "https://github.com/CosmosMind-ai/RSI-Harness"
topics: ["Agent/harness", "自我改进/RSI"]
tags: ["harness", "RSI", "genome", "pi-coding-agent", "config-as-artifact", "论文未读", "证据不全"]
rating: "暂不评分（论文正文未读到）"
---

# MetaRSI / RSI²（论文未读）+ RSI-Harness / RSIH（代码库全文精读）

## ⚠️ 归档状态：三源可达性

| 来源 | 状态 | 我做了什么 |
|---|---|---|
| GitHub `CosmosMind-ai/RSI-Harness` | ✅ 可达 | **一手全文读取** README + `docs/README.md` + `docs/genome/harness-rsi.md`（raw.githubusercontent 通道） |
| 论文 `www.cosmosmind.ai/research/metarsi-v1.pdf` | ❌ 不可达 | WebFetch 与 curl 均被本环境 egress proxy 拦截（`CONNECT tunnel failed, 403`）；`cosmosmind.ai` 与 `www.` 两个 host 都被拦 |
| HuggingFace `CosmosMind/RSI-Harness` | ❌ 不可达 | `huggingface.co` 整域被 egress proxy 拦截 |

**另：论文标题在公网检索不到任何痕迹。** 精确串检索 `"A Meta-Recursive Self-Improving System for
Recursive Self-Improving Systems"`、`"MetaRSI"`、`"CosmosMind" AI Lab` 全部零命中（返回的都是
Meta^n 2608.24735、Gödel Agent、RSI 维基等邻近工作）。不可达 ≠ 不存在——被拦是**我这边的网络策略**，
不是对方的问题；但"没有 arXiv、没有第三方索引、GitHub 上零处提及论文"这三条是可确证的事实。

**因此：本笔记不含任何论文的方法/实验/数字。** 下面所有内容出自公开代码库正文，逐条可追。

## TL;DR（仅覆盖已核实部分）
1. RSIH 把 **agent 的 harness 配置本身做成一等公民产物**：一个叫 **Genome** 的自包含目录
   （system prompt、工具、skills、MCP、运行时策略、主题、键位……12 个组件），可版本化、可 diff、
   可直接发给别人跑。构建在 Pi coding agent 之上，**不 fork core**，只用其公开配置面。
2. 其中一个 Genome 叫 **`harness-rsi`（命令 `gee`）——它的产物是别的 Genome**：读你在
   RSIH / Pi / Claude Code 里的真实 session 历史，聚合出工具直方图、高频命令、反复出现的纠正，
   判定哪条该变 skill、哪条该变 tool、哪条该进 memory，**讲完整方案等你确认后才落盘**。
3. 作者自己给 RSI 的定义是收窄的：*"不是模型改自己的权重，而是改**自己的 harness**，
   且用的就是你手写 harness 时会用的那套手段"*（README「Self-referential」节）。

## 核心设计（出处：README + docs/genome/harness-rsi.md）

- **两条不变量，各由一个测试守住**（README「Why this design」）：
  1. 不带 `--genome` 时 `rsih` 行为与 `pi` 完全一致，只是配置目录变成 `~/.rsih`；
  2. Pi 能配的，Genome 都能配——`test/pi-surface.test.ts` 从 Pi 的 `.d.ts` 抽出每个 settings key
     和 keybinding id，**漏路由一个就红**，Pi 升级加开关时测试先告诉你。
- **配置是 patch 不是 replacement**：字段缺省=继承 Pi 默认，`null`=显式重置，只有出现的值才覆盖
  （对象递归 merge、数组整体替换）。→ *"改一个字段不需要重写整个 harness"*。
- **12 组件字段所有权互斥**：越界写入在加载期即失败（`tools` 组件想设 `system_prompt` → 直接报错）。
- **自指性是关键论据**：`src/` 里**没有一行**为 `harness-rsi` 特设的代码——它的宪章在 `instructions`
  组件、方法论在文件型 skill、三个交互工具在自带 extension，全部是任意 Genome 都有的手段
  （docs/genome/harness-rsi.md「为什么它能只是一个 Genome」）。
- **一条设计原则**：*"除了 agent 自己确实拿不到的东西，什么都不写成代码"*——extension 里只有 3 个工具，
  因为只有 3 件事 agent 做不到（session 目录名是编码路径、库太大必须有界读、多选/提问页需要键盘焦点）。
  **extension 里没有任何模型调用。**

### 有出处的工程实测数字（作者在文档里给的，非我复现）
| 项 | 数字 | 出处 |
|---|---|---|
| `resources.isolate` 前/后 | 用户 `~/.agents/skills` 下 **58 个 skill 全进 prompt，36 KB** → 隔离后剩 1 个，**7 KB** | harness-rsi.md「为什么要 isolate」 |
| session 扫描性能 | Pi 152 个 19ms / Claude 53 个 7ms / 三源共 **357 个 38ms** | 同上「session 的来源」 |
| Claude 记录里"用户真说的话"判据 | `promptSource === "typed"`；退化规则与其**逐条一致（69 typed / 24 包装标签）** | 同上 |
| 未接 Codex 的原因 | `~/.codex/sessions` **1341 文件 / 2.9 GB**，单文件最大 298 MB，首条真实用户消息偏移中位 **49 KB**，36% 超 64 KB 读窗 | 同上 |

## 局限与存疑（我的判断）

1. **标题的"递归"和代码里的"递归"不是一回事。** 公开代码里的元层级只有**一层**：
   `harness-rsi` 是"造 Genome 的 Genome"。README 没有任何"Genome 改进 `harness-rsi` 自己、
   再用改进后的它造下一代"的闭环描述。论文标题里的 *meta-recursive / RSI for RSI systems themselves*
   这层，**在公开材料里我找不到对应实现**。
2. **它目前不是闭环 RSI，是"人确认的一次性 harness 生成"。** 流程第 6 步写死：*"用户没答之前不写任何文件"*，
   `AskUserQuestion` 是硬门。这是好工程（防漂移），但意味着没有自动化的 improve→evaluate→accept 循环。
3. **最要命的一条：没有评测。** README 与 `docs/README.md` 都白纸黑字写着
   *"仓库不包含 benchmark、数据生成、训练或评测实现"*。而 harness 自改进这条线的教训恰恰是
   **递归结构不够**——STOP 证明弱模型递归会退化，AHE / Self-Harness 都配 held-in/held-out 双重回归验证
   才敢说"接受这次更新"（见 [Weng 综述笔记](2026-07-21-lilian-weng-harness-engineering.md)）。
   **一个自称 RSI 的系统若不给 accept gate 和 held-out 曲线，"改进"这个词就是空的。** 论文若有实验，
   全部证据在那份我读不到的 PDF 里。
4. **同组织另两个仓库暗示了实验是怎么做的，也暗示了复现难度。** `CosmosMind-ai` 下另有
   `SWE-Prometheus`（22 题）与 `SWE-PolyVision`（48 题），二者都只放**公开题面**，
   明确排除"验证补丁、分数、结果、traces、reference answers"。若论文主实验建在这两个上，
   **外部第三方无法独立复现或核分**。
5. 仓库很新（org 三个仓库均显示 2026-09-08 更新，star 数为个位数），公网无任何第三方讨论。

## 我的评价

- **值得看的地方（与论文声称无关，纯工程）**：把 harness 配置做成**可 diff、可继承、可发给人**的 artifact，
  以及"12 组件字段所有权互斥 + patch 语义 + 用 Pi 的 `.d.ts` 反向守全覆盖"这套约束设计，是本库
  harness 线里少见的**把工程契约写死**的做法。`gee` 的"证据先聚合、原文选择性读、场景当尺子筛证据、
  证据与意图打架时把两种读法一起交给用户"——这套 session forensics 方法论本身就可以直接借鉴到本知识库。
- **对我们的价值**：这是 [2026-08-12 追踪](../../topics/agents.md) 那个 harness 演化集群里
  **少数能直接跑的开源实现**（对照：EvoHarness-RL 训练化 / EvolveNet 联邦化都还只是论文）。
  按 Weng 的优化谱系，它落在 **"优化 harness 代码"** 这一级，但**去掉了自动搜索**，换成人确认——
  可以理解为 Meta-Harness（2603.28052）的"低风险工程版"。
- **是否值得深读/复现**：代码值得读（尤其 `harness-rsi` 的 skill 正文）；**论文在拿到 PDF 前不做任何评价**。
  按本库口味（工程化、小而美、可复现）：机制部分对味，**但"出身"与"可验证性"两项目前都不满足**。

## 关联
- [Harness Engineering for Self-Improvement（Lilian Weng）](2026-07-21-lilian-weng-harness-engineering.md) — 谱系与七大挑战，本篇的判断框架
- [topics/agents.md](../../topics/agents.md) — harness 演化集群追踪（EvoHarness-RL / EvolveNet / Self-Harness / AHE）
- 邻近工作（检索所得，未读）：[Meta^n 2608.24735](https://arxiv.org/abs/2608.24735)（元操作固定、递归扩张输入）、
  [HarnessBank 2607.13683](https://arxiv.org/abs/2607.13683)（harness 基因库 + 门控验证 —— 与 Genome 的"可分享基因"隐喻高度撞车，值得对比）
- **待补（拿到 PDF 后）**：论文的 method / 实验设置 / RSI² 的第二层元究竟指什么 / accept gate 与 held-out 曲线 / HF 上放的是什么产物

## 复现路径（给未来的自己）
```bash
git clone https://github.com/CosmosMind-ai/RSI-Harness.git && cd RSI-Harness
./install.sh          # 需要 Node 22.19+
rsih :paperlab        # 示例 Genome：论文实验 harness
gee                   # == rsih :harness-rsi，交互式造 Genome
```
