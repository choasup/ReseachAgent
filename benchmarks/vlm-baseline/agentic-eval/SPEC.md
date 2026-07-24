# Agentic 视觉评测系统 · 第一切片设计

日期:2026-07-24 · 状态:设计已批准,待转实现计划

## 1. 背景与研究动机

现有三榜(通用 / 巡检 / 细粒度)全部是**无工具、单次前向**口径。本项目最硬的发现是:
细粒度小目标感知是系统性短板,而 ZwZ 证明「训练时把 zoom 内化为原语」能补上这个短板。

由此引出本系统要回答的研究问题:**「推理时外挂工具」能否达到甚至超过「训练时内化」?**
三方对照 —— 无工具基线 vs 推理时工具增强 vs ZwZ(训练内化)。

完整系统是多个独立子系统(视觉工具层 / 代码沙箱 / Agent 编排 / 评测协议+判分 / 模型接入)。
本 spec 只覆盖**第一切片:代码沙箱 × K3 对标集**,验证核心链路后再长出其余子系统。

## 2. 第一切片范围

- **工具**:代码执行沙箱(Python)。视觉工具(zoom/crop)属后续切片。
- **数据**:K3 对标集 —— MathVision / CharXiv_reasoning_val / MMMU_Pro(已在 LMUData)。
- **目标**:复现 K3 表 "w/ python" 口径,产出每题「无工具 vs 有沙箱」对比。
- **模型**:先 Qwen3.6-35B-A3B + Qwen3-VL-235B 两个,管线通过后再铺开到全 11 模型。
- **实现路线**:方案 A —— code-block 框架 + Docker 沙箱(非原生 function-calling,
  任何 instruction 模型都能跑,保横向对照)。

## 3. 威胁模型(决定隔离级别)

研究评测环境,沙箱执行的是「我们自己评测的模型生成的代码」,**不是防御恶意攻击者**。
故隔离级别务实:容器 + 无网 + 超时 + 资源限 + 图像只读挂载即可,不需要 gVisor/VM 级隔离。

## 4. 与现有系统的关系 —— 独立轻量评测器

**不塞进 VLMEvalKit**(其判分链路已被本轮四个 bug 证明脆弱且难改,且不原生支持 agentic 多轮)。
新评测器复用现有资产:vLLM serve 端点、数据 TSV、LLM-judge。Agent loop 与沙箱是独立新模块,
边界清晰、可单测、不污染跑出所有历史结果的老管线。

## 5. 组件(各自单一职责)

| 模块 | 职责 | 依赖 |
|---|---|---|
| `agent_loop.py` | 编排:发题→收输出→解析代码块→调沙箱→回灌→多轮→收敛最终答案 | parser, sandbox, vLLM 端点 |
| `sandbox.py` | Docker 执行器:起容器、注入代码、收 stdout/生成图、超时/资源限、销毁 | Docker |
| `codeblock_parser.py` | 从模型输出抽 ```python 块 + 抽最终答案,容错不规范输出 | 无 |
| `runner.py` | 遍历数据集、并发、结果入库(复用现有 judge 判分) | agent_loop, judge |

## 6. 数据流(单题)

题干+图 → 模型(system prompt 教工具用法)→ 输出含 ```python``` 块 → parser 抽代码
→ sandbox 执行(图像 :ro 挂载)→ stdout/生成图回灌为下一轮输入 → 循环
→ 模型给 `Final Answer:` 或触顶 → LLM-judge 判分 + 存工具调用轨迹。

## 7. Docker 沙箱规格

- 基础镜像:python + PIL / numpy / opencv / matplotlib。
- 每次执行:`--network none`、超时 30s、内存 2G、图像 `:ro` 挂载、无持久化。
- 多轮上限 5 轮;单题代码总执行预算 90s。
- 触顶未收敛 → 记为「未完成」(而非崩溃),计入超时率。

## 8. 判分与口径

- 第一切片**沿用 Qwen3-VL-8B-Instruct 当 judge**(与历史三榜同口径,可比)。
  agentic 最终答案多为代码算出的结构化值,judge 压力比长推理小。judge 升级另做独立实验。
- 每题产出两列:**无工具基线 vs 有沙箱**,增量即工具增益。
- 与 K3 数字对比时声明:协议非精确复刻(K3 "w/ python" 协议未公开),
  仅在「有无工具」趋势上可比,不做绝对值对齐。

## 9. 实现约束

- **GPU 轮换**:Qwen3.6 与 235B 均需 4 卡 TP,服务器仅 HIP 4-7 空闲,**不能同时 serve**,
  须轮换(serve A → 跑完 → rm → serve B)。沿用现有 rotate 编排模式。
- Qwen3.6 serve 走 ROCm 7.0 镜像 `vllm/vllm-openai-rocm:latest`(已验证兼容 6.3 宿主 + MI308X);
  235B 走旧 `rocm/vllm:latest`。两者镜像不同,轮换脚本需分别处理。

## 10. 第一切片验收标准

在 MathVision / CharXiv / MMMU_Pro 上,对 Qwen3.6 + 235B 各跑通,产出「无工具 vs 有沙箱」
对比表,且沙箱执行成功率、平均轮数、超时率有日志可查。

## 11. 后续切片(不在本 spec)

视觉工具层(zoom/crop)、扩到全部 11 模型、agentic 判分轨迹质量分析、judge 升级实验。
