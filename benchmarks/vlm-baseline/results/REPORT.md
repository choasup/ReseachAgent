# VLM 摸底评测报告：Qwen3-VL-8B vs GLM-4.1V-9B vs Molmo-7B-D

> 目的：在自建 benchmark 之前，用统一 harness（VLMEvalKit）把三家开源 8–9B VLM 在 9 个公共
> 基准上的差距摸清楚，确定自建题该往哪些维度出。
> 评测日期：2026-07-07/08 · 硬件：AMD MI308X（ROCm 6.3）· Harness：open-compass/VLMEvalKit@main

## 0. 执行摘要（TL;DR）

- **综合最强：Qwen3-VL-8B**（9 基准均分 **81.0**），文档/图表/OCR 全面领先；
  **GLM-4.1V-9B**（均分 **77.7**）综合推理类微弱占优；**Molmo-7B-D**（均分 **72.5**）除幻觉(POPE)外整体靠后。
- **差距最大的三个维度（＝自建 benchmark 的出题重点）**：
  **图表理解 ChartQA**（GLM 57.4 vs Qwen/Molmo ~83，差 26 分）、
  **OCR**（Molmo 66.1 vs Qwen 89.9，差 24 分）、
  **综合学科推理 MMMU**（Molmo 47.7 vs GLM 68.1，差 20 分）。
- **⚠️ 方法学关键点**：README 指定的 `--judge exact_matching` 纯规则判分**对"先推导后给答案"的
  冗长输出系统性漏判**，会把 Qwen/GLM 的真实能力严重低估（Qwen MMMU 被压到 21%，实为 66%）。
  本报告主表采用**本机 LLM-judge 重新抽取答案**的修正值（方法与验证见 §2），并保留原始 exact 值对照。

---

## 1. 实验设置

| 项 | 配置 |
|---|---|
| 模型 | `Qwen3-VL-8B-Instruct`、`GLM4_1VThinking-9b`(=THUDM/GLM-4.1V-9B-Thinking)、`molmo-7B-D-0924` |
| 基准（9） | MMMU_DEV_VAL, MMStar, RealWorldQA, DocVQA_VAL, ChartQA_TEST, OCRBench, POPE, HallusionBench, CountBenchQA |
| 推理后端 | Qwen/GLM 用 **vLLM serve**（OpenAI 兼容，16 并发 batch）；Molmo 用 transformers（remote code） |
| 判分 | VQA/OCR/计数/Y-N 走各自规则；MCQ 与 Y-N 的答案抽取用 **本机 vLLM 当 LLM-judge**（见 §2） |
| 硬件 | AMD MI308X（gfx942, 192GB/卡），ROCm 6.3 + torch 2.8 |

**ROCm 适配（3 处坑，全部固化在 `patch_vlmevalkit.py`）**：① Qwen3-VL/GLM 视觉塔 SDPA 在 gfx942 上
**静默算错**（把图看成彩色竖条，不报错），强制 `attn_implementation="eager"` + SDPA 限 math 后端；
② 视觉塔 patch-embed 的 `Conv3d`、GLM downsample 的 `Conv2d`（kernel==stride）触发 MIOpen 段错误，
替换为等价 matmul（CPU 数值对齐验证）；③ `get_gpu_memory()` 只认 nvidia-smi，改用 `torch.cuda.mem_get_info`。
三模型均通过真图 sanity check（描述+计数正确）后才放行全量评测。

---

## 2. 评分方法学：为什么必须用 LLM-judge（关键）

VLMEvalKit 在无 `OPENAI_API_KEY` 时退回 `exact_matching` 纯规则抽答案。实测发现它**对冗长输出系统性漏判**：
模型把答案写在长篇推导的结尾（如 `**Answer: D. $77,490**`、`the answer is \(B\)`、`correct choice is B`），
正则抓不到就判 0。这对 **Qwen（Instruct，爱展开）伤害最大，对 Molmo（输出极简）几乎无影响**——
即 exact_matching 不仅低估，还**对不同模型不公平**。

**修法**：用本机空闲的 Qwen vLLM 容器当 LLM-judge（VLMEvalKit 官方 `LOCAL_LLM` 机制），对 5 个
抽取敏感基准（MMMU/MMStar/RealWorldQA/POPE/HallusionBench）× 3 模型统一重评。VQA/OCR/计数走 ANLS/
精确匹配/数字比对，不受影响、不动。

### exact_matching → LLM-judge 修正对照

| 基准 | Qwen exact→judge | GLM exact→judge | Molmo exact→judge |
|---|---|---|---|
| MMMU_DEV_VAL | **21.0 → 66.1** (+45) | 44.1 → 68.1 (+24) | 47.0 → 47.7 (+0.7) |
| MMStar | 56.7 → 71.5 (+15) | 57.7 → 72.9 (+15) | 56.3 → 56.3 (0) |
| RealWorldQA | 70.5 → 70.7 (+0.3) | 67.7 → 72.4 (+4.7) | 70.7 → 70.7 (0) |
| HallusionBench | **54.5 → 73.8** (+19) | 71.5 → 73.3 (+1.8) | 62.4 → 62.4 (0) |
| POPE | 87.6 → 87.6 (0) | 87.0 → 87.0 (0) | 89.0 → 89.0 (0) |

**修正值可信的三条证据**：
1. **翻负 = 0**：judge 从未把 exact 判对的样本改判错——只做单向补救，绝无瞎给分。
2. **Molmo 零变化**：输出简洁的 Molmo 修正幅度 ≈0（MMMU 47→47.7），证明 judge 不会系统性抬分，
   只精准补救被冗长输出埋没的正确答案。
3. **抽样人工核对**：翻正样本结尾均确有正确答案（如 GT=D、结尾 `Correct Answer: D. $0`），
   是正则漏抓而非模型答对——判分修正方向正确。

> 结论：主表用 judge 修正值做跨模型比较是**更公平、更接近真实能力**的口径。原始 exact 值见
> `results/summary_exact_matching.csv` 存档。

---

## 3. 量化结果（judge 修正，0–100）

| 维度 | 基准 | **Qwen3-VL-8B** | **GLM-4.1V-9B** | **Molmo-7B-D** | 最强 |
|---|---|:--:|:--:|:--:|:--:|
| 综合推理 | MMMU_DEV_VAL | 66.1 | **68.1** | 47.7 | GLM |
| 综合推理 | MMStar | 71.5 | **72.9** | 56.3 | GLM |
| 真实场景 | RealWorldQA | 70.7 | **72.4** | 70.7 | GLM |
| 文档 | DocVQA_VAL | **95.7** | 91.8 | 91.5 | Qwen |
| 图表 | ChartQA_TEST | 83.2 | 57.4 | **83.8** | Molmo≈Qwen |
| OCR | OCRBench | **89.9** | 86.2 | 66.1 | Qwen |
| 幻觉 | POPE | 87.6 | 87.0 | **89.0** | Molmo |
| 幻觉 | HallusionBench | **73.8** | 73.3 | 62.4 | Qwen |
| 计数 | CountBenchQA | **90.1** | **90.1** | 85.4 | Qwen=GLM |
| **均分** | | **81.0** | 77.7 | 72.5 | **Qwen** |

**按维度差距（＝各模型能力分水岭）**：
- **图表 ChartQA**：Qwen 83.2 / Molmo 83.8 领先，**GLM 仅 57.4**——GLM 读柱状图/折线图数值明显吃力（差 26 分，全表最大）。
- **OCR**：Qwen 89.9 / GLM 86.2 强，**Molmo 仅 66.1**——Molmo 密集文字识别弱（差 24 分）。
- **综合学科推理 MMMU/MMStar**：GLM≈Qwen（66–73），**Molmo 落后 15–20 分**——Molmo 不擅长需要学科知识的多步推理。
- **文档 DocVQA**：三家都强（91–96），Qwen 微弱领先，差异化价值低。
- **幻觉 POPE**：三家都 87–89 逼近饱和；**HallusionBench 更能区分**（Qwen/GLM ~73 vs Molmo 62）。
- **计数 CountBenchQA**：三家都强（85–90），且 **Molmo 反而最低**——见 §5 讨论。

---

## 4. 定性分析（含真实采样，正确 / 错误各一）

> 采样自各模型逐题判分结果，`pred` 为模型原始输出（截断）。完整样例见 `results/samples.json`。

### 4.1 Qwen3-VL-8B —— 文档/OCR/图表全能，弱在综合推理与幻觉抵抗
- **强项 OCR（对）**：Q "what is written" · GT `CENTRE` · pred `centre` ✅（大小写/规范化后命中）
- **强项 DocVQA（对）**：Q "How many energetic brands has ITC created" · GT `50` · pred `over 50` ✅
- **典型错误 计数（差 1）**：Q "How many golfers" · GT `9` · pred `8` ❌——密集小目标漏数 1 个。
- **典型错误 OCR（形近误认）**：Q "what is written" · GT `Crisp` · pred `c-7` ❌——艺术字/手写体崩坏。
- **行为特征**：Instruct 模型爱长篇推导（HallusionBench 有回答以 "Based on a visual comparison…" 开头
  而非直接 yes/no），正是 §2 里被 exact_matching 漏判的根源。

### 4.2 GLM-4.1V-9B —— 综合推理最强，图表读数是短板
- **强项 MMMU（对）**：会计题 "solve for per unit overhead" · GT `B` · pred 展开加权平均法推导后给出 B ✅
- **强项 DocVQA（对）**：Q "how many children unsatisfactory" · GT `seven/7` · pred `7` ✅
- **典型错误 ChartQA（读数错）**：Q "value of the lowest bar" · GT `23` · pred 逐项列举后仍报错值 ❌——柱高→数值映射不准。
- **典型错误 OCR（形近）**：GT `zula` · pred `7ula` ❌（z→7）。
- **行为特征**：thinking 模型，答案前有长推理链（reasoning parser 剥离），措辞如 `the answer is \(B\)`
  非标准，exact_matching 同样漏判（MMMU 44%→68%）。

### 4.3 Molmo-7B-D —— 幻觉抵抗好（POPE 最高），综合推理/OCR 明显弱
- **强项 POPE/计数（对）**：Q "How many headsets" · GT `10` · pred `10` ✅；HallusionBench 简洁答 `yes/no` 抽取无歧义。
- **典型错误 计数（大偏差）**：Q "How many arrows" · GT `8` · pred `12` ❌——复杂场景计数偏差比 Qwen/GLM 大。
- **典型错误 OCR**：GT `ALLEN` · pred `alert` ❌；MMMU 学科题 GT `B` · pred `A` ❌（知识+多步推理吃力）。
- **行为特征**：输出**极简**（单词/单字母），故 exact_matching 与 judge 结果几乎一致——这也解释了它
  在需要长推理的 MMMU/MMStar 上分数低：不是被判分坑，是真的不展开推理。

---

## 5. 对自建 benchmark 的启示

1. **出题重点＝差距最大的维度**（模型间最可区分）：
   **① 图表数值读取（ChartQA 类）** —— GLM 的明确短板，Qwen/Molmo 强，区分度 26 分；
   **② 密集/艺术字 OCR** —— Molmo 短板，区分度 24 分；
   **③ 需学科知识的多步视觉推理（MMMU 类）** —— Molmo 短板，区分度 20 分。
   这三类做进自建题最能拉开梯度、暴露能力边界。
2. **计数需重新设计**：README 预期"Molmo 计数占优"（pointing 训练红利）**未被复现**——CountBenchQA 走
   纯文本答案，Molmo 反而最低(85.4)。说明**Molmo 的 pointing/接地优势不体现在文本计数 Q&A 上**，
   印证 README"已知空白"：pointing 对比需要**坐标/框选协议**，不是文本问答能测的——这正是自建题的空间。
3. **区分度低、可少出的维度**：DocVQA、POPE 三家都接近饱和（>87），做基线校准可以，但不适合作为主打差异维度。
4. **幻觉用 HallusionBench 而非 POPE**：POPE 已饱和；HallusionBench 更能区分（Molmo 明显弱）。

---

## 6. 复现与文件清单

- 全流程脚本与 ROCm 补丁：服务器 `013_mllm/benchmarks/vlm-baseline/`（`patch_vlmevalkit.py`,
  `run_*.sh`, `reeval_judge.sh`, `merge_results.py`, `sample_cases.py`）。
- 本目录文件：
  - `summary.csv` —— 主表（judge 修正，0–100）
  - `summary_exact_matching.csv` —— 原始 exact_matching 值（存档对照）
  - `samples.json` —— 各模型各基准正确/错误采样（每类 3 条，含问题/GT/模型输出）
  - `logs/run_*.log` —— 三模型推理日志
- 读数原则：① 只比这次统一跑出的数字，**不与各家论文自报数字混比**；② 差 <2 分视为噪声；
  ③ 主表为 judge 修正口径，跨模型公平。

## 7. 已知局限
- LLM-judge 用的是本机 Qwen3-VL-8B（非 GPT-4 级），抽取答案是简单任务、已验证翻负=0，但极端边界可能有个别误判。
- Molmo 的 pointing/接地能力本套基准**测不到**（VLMEvalKit 无 pixmo-points-eval），需自建坐标协议评测。
- 未评 thinking/non-thinking 对照、未评视频与多图接地——留待自建 benchmark 阶段。
