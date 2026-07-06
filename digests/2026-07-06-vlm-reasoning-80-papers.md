---
period: "deep-dive"
range: "CVPR 2026 · VLM × 推理/RL 全部 80 篇"
generated: "2026-07-06"
method: "8 路并行检索分析（WebSearch，abstract 级），每篇提取问题/方法/结果/出身/口味评分"
---

# CVPR 2026 · VLM × 推理/RL — 80 篇逐篇详析

> **口径**：信息来自 WebSearch 检索到的 abstract/项目页摘要（原文 PDF 被本环境网络策略屏蔽）。
> 每篇标注"置信"：`abstract级` = 有摘要级信息；`仅标题` = 检索不到、仅凭标题推断（全部如实标注，未编造）。
> "贴合度"按用户口味打分：工程化 / training-free / 小而美加分；纯 benchmark、重资源减分；VLA/驾驶/导航固定 ≤2。
> 统计：80 篇中 abstract级 ~70 篇，仅标题 ~10 篇；VLA/导航/驾驶类 10 篇（已按用户要求降权）。

## 🏆 贴合度 Top 榜（5/5，共 7 篇）

| 论文 | 一句话 | 关键数字 |
|---|---|---|
| **Thinking Diffusion** | training-free 修复 dMLLM"先答后想"：PSP 延迟出答案 + VRG 放大视觉信号 | +7.5% 且快 3 倍 |
| **DeepScan** | training-free 三阶段视觉证据扫描，即插即用任意 LVLM | Qwen2.5-VL-7B 在 V* 达 90.6% |
| **Why RL > SFT?** | RL 泛化优势 = 隐式难度过滤；提出 DC-SFT 用难度筛选替代 RL | DC-SFT 反超 RL 且更省 |
| **Deeper Thought, Weaker Aim** | 诊断"想得越深看得越偏"= attention dispersion，training-free 重加权修复 | 数字待核 |
| **VideoThinker (Beyond Perceptual Shortcuts)** | 因果去偏 RL：1% 数据、无 SFT，3B 超 7B | MVBench +2.1 超 Video-UTR-7B |
| **See It, Say It, Sorted** | training-free 迭代框架：每步推理都要视觉证据背书 | 数字待核 |
| **GAR（声源定位）** | training-free"生成-自检-修正"meta-reasoning 闭环 | competitive，开源 |

## 💎 高分梯队（4/5，摘选）

| 论文 | 亮点 | 出身 |
|---|---|---|
| **TTRV** | 测试时 RL、零标注：频率+熵做奖励 | 16 数据集平均 +24.6%/+10.0%，8B 超 GPT-4o 2.3% |
| **ANTS** | test-time OOD 检测，CVPR **Oral** | FPR95 -3.1% |
| **GASP (Beyond 3D VQAs)** | 几何先验注入，不用 3D VQA 数据 | VSI-Bench +29.0% |
| **POINTS-Long** | 双模式视觉 token：1/40 token 保 97.7%+ 精度 | 上交+腾讯 WeChat AI |
| **PDCR** | 发现"视觉步骤被文本步骤统计淹没"，分簇归一化 reward | KAIST+UIUC+MSRA |
| **ReasonX** | MLLM-as-judge 相对比较当 GRPO reward，免标注 | Imperial+Adobe；WHDR -9~25% |
| **Keep it SymPL** | 把 allocentric 空间问题"翻译"成模型会做的符号布局，免训练 | 待核 |
| **Learning to Focus (USTC)** | 用"信息差"逼模型真用裁剪区域，免轨迹监督 | USTC |
| **CodeDance** | 代码即工具：自由编排可执行视觉推理，有涌现组合 | 待核 |
| **ORCA** | DocVQA 多 agent：分解-路由-辩论-校验，开源 | 待核 |
| **Saliency-R1** | saliency 对齐当 reward："对齐注意而非只对齐答案" | 疑似 CUHK |
| **dMLLM-TTS** | 统一模型自己当自己的 verifier 做 TTS | 南大+上海AI Lab等 |
| **Think-as-You-See** | 流式视频 CoT：TTFT 10.6s→≈0 | 待核 |
| **EgoMind** | geometry-free 空间推理：仅 5K SFT + 20K RL | 北航 |
| **REALM** | 2D MLLM 零 3D 训练迁移到 3DGS 分割编辑 | 待核 |
| **Pixels Don't Lie** | bootstrap 人工反馈做推理监督：小模型胜 30x baseline (96.2%) | 待核 |
| **Think Visually, Reason Textually** | ARC-AGI 模态分工：视觉管抽象、语言管执行 | 待核 |
| **ASO** | 发现 VLM 安全的"风格不一致"盲点 | 待核 |
| **Seeing Clearly** | 免微调补丁修复罕见物体 blindness | 待核 |

## 📡 我从 80 篇里读出的 5 个信号

1. **"推理伤感知"已成独立证据链**：Deeper Thought Weaker Aim（注意力发散）、AV-Reasoner（OOD 上推理无增益的负结果）、NoRD（驾驶去 CoT 反而省 3 倍 token）、Thinking Diffusion（dMLLM 先答后想）——**四篇互不相识的工作从不同角度证明"无脑加 CoT 有代价"**。修这个 trade-off 的窗口正开着。
2. **training-free 阵营战斗力惊人**：7 篇 5/5 里 6 篇不训练或几乎不训练；DeepScan（90.6% V*）证明测试时管线能逼平 RL 训练路线。**"先试 training-free，再考虑 RL"应成为默认工作流**。
3. **RL 的红利在转向"数据与奖励设计"**：Why RL>SFT（难度过滤）、HoneyBee（配方科学）、VideoThinker（1% 数据）、PDCR（分簇归一化）、VOLD（cold-start 对齐前提）——**堆算力的时代在退，理解"为什么 work"的时代在来**。
4. **MLLM-as-judge 正在变成通用零件**：ReasonX（低层视觉 reward）、Pixels Don't Lie（推理监督放大器）、dMLLM-TTS（自我 verifier）——拿现成 MLLM 当裁判/验证器，是低成本高杠杆的复用范式。
5. **空间推理量大但方法密度低**：15+ 篇空间/3D 里大半是 benchmark 或数据注入；真正省事的是 SymPL（问题重构）、GASP（先验注入免 VQA 数据）这类"换表示"的思路。

## 🎯 建议深读顺序（结合可复现性）
1. **TTRV**（零标注测试时 RL，数字最猛）
2. **Why RL > SFT?**（结论若稳，直接改变后训练实践）
3. **DeepScan / Thinking Diffusion**（training-free 代表，即插即用）
4. **PDCR**（reward 设计，MSRA 背书，开源）

---

# 逐篇详析（80 篇，按标题字母序分 8 组）


## 第 1 组

### A Causal Marriage between VLM and IRM from Understanding to Reasoning
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_A_Causal_Marriage_between_VLM_and_IRM_from_Understanding_to_CVPR_2026_paper.pdf
- 问题: VLM 在多模态 OOD（分布外）场景下的理解与推理泛化不足。
- 方法: 将 VLM 与 Invariant Risk Minimization (IRM) 以因果框架结合，提供理论框架并验证（搜索摘要仅给到此粒度）。
- 结果: 声称在多模态 OOD understanding 与 reasoning 任务上有"substantial improvements"，具体数字未检索到。
- 出身: Peng Cheng Laboratory + HKUST (Guangzhou)（一作 Ziliang Chen）
- 贴合度: 3/5 — 因果+不变性是有理论味的"小而美"方向，但偏理论、无法确认工程可用性与训练开销。
- 判断: VLM×IRM 的组合少见、有理论深度，但摘要信息太少，实际增益规模存疑。
- 置信: abstract级（部分，细节缺失）

### ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models
- 链接: https://arxiv.org/abs/2601.11404
- 问题: VLA 模型用语言/视觉 CoT 做中间推理，信息间接、难以传递精确动作所需的细粒度信号。
- 方法: 提出 Action Chain-of-Thought——推理直接在动作空间进行：Explicit Action Reasoner (EAR) 生成粗参考轨迹作为显式动作推理步，Implicit Action Reasoner (IAR) 从多模态内部表征提取隐式动作先验，共同条件化 action head。
- 结果: LIBERO 98.5%、LIBERO-Plus 84.1%、VLABench 47.4%。
- 出身: AgibotTech（智元机器人，GitHub 官方仓库所属）
- 贴合度: 2/5 — 用户暂不关注VLA。
- 判断: "在动作空间里思考"的范式转换想法干净，LIBERO 接近饱和但 LIBERO-Plus/VLABench 数字有说服力；仅对关注机器人方向者有价值。
- 置信: abstract级

### ANTS: Adaptive Negative Textual Space Shaping for OOD Detection via Test-Time MLLM Understanding and Reasoning
- 链接: https://arxiv.org/abs/2509.03951
- 问题: 现有基于负文本空间的 OOD 检测缺乏对 OOD 图像的真正理解，且缺少与 ID 标签语义相近的负标签，near-OOD 表现受限。
- 方法: 测试时缓存疑似 OOD 的历史图像，让 MLLM 描述它们生成表达性负句子（far-OOD）；对 near-OOD 则缓存视觉相近的 ID 类子集、用 MLLM 推理生成针对性的相似负标签；再用 adaptive weighted score 统一两种设定。
- 结果: ImageNet benchmark 上 FPR95 降低 3.1%；CVPR 2026 Oral。
- 出身: 未核实（GitHub: ZhuWenjie98）
- 贴合度: 4/5 — 纯 test-time、无需训练，思路轻巧可落地；扣一分因依赖 MLLM 在线推理的额外开销。
- 判断: 训练-free 的 OOD 检测里少见地同时照顾 near/far 两种设定，Oral 背书；亮点明确。
- 置信: abstract级

### AV-Reasoner: Improving and Benchmarking Clue-Grounded Audio-Visual Counting for MLLMs
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Lu_AV-Reasoner_Improving_and_Benchmarking_Clue-Grounded_Audio-Visual_Counting_for_MLLMs_CVPR_2026_paper.pdf
- 问题: MLLM 的音视频计数能力弱且缺乏"有依据（clue-grounded）"的评测。
- 方法: 提出 CG-AV-Counting benchmark（497 个长视频、1,027 个多模态问题、5,845 条人工标注 clue，支持黑盒/白盒评测）；并用 GRPO + curriculum learning 训练 AV-Reasoner 模型，从相关任务泛化计数能力。
- 结果: 多个 benchmark 达 SOTA；但作者自己发现 out-of-domain 场景下语言空间推理不带来增益。
- 出身: 未核实（作者 Lidong Lu, Guo Chen, Zhiqi Li, Yicheng Liu, Tong Lu，机构搜索结果未明示）
- 贴合度: 3/5 — benchmark+RL 训练偏重资源；加分项是诚实汇报"reasoning 在 OOD 上无增益"这一负结果。
- 判断: 负结果（语言推理不泛化）比 SOTA 数字更有信息量，值得引用。
- 置信: abstract级

### AXG-Reasoner: Error Detection and Explanation in Long Task Videos with Vision-Language Models
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Lee_AXG-Reasoner_Error_Detection_and_Explanation_in_Long_Task_Videos_with_CVPR_2026_paper.pdf
- 问题: 长程序性任务视频中的操作错误检测与解释（仅标题推断）。
- 方法: 未检索到方法细节；作者此前工作是基于 Generalized Task Graph 的程序性视频错误识别（ICCV 2025），本篇可能是其 VLM 化延续（推测，未核实）。
- 结果: 未检索到。
- 出身: Northeastern University（Shih-Po Lee, Ehsan Elhamifar）
- 贴合度: 3/5 — 长视频错误检测+可解释是实用方向，但方法与开销均未知，无法确认工程友好度。
- 判断: 该组在程序性视频错误检测上有连续积累（CVPR'24→ICCV'25→本篇），方向可信，细节待读原文。
- 置信: 仅标题（机构/作者已核实）

### Adversarial Style Optimization: Enhancing VLM Jailbreaks by GRPO-based Stylistic Triggers Optimization
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Luo_Adversarial_Style_Optimization_Enhancing_VLM_Jailbreaks_by_GRPO-based_Stylistic_Triggers_CVPR_2026_paper.pdf
- 问题: 发现 MLLM 存在"Stylistic Inconsistency"——理解能力对视觉风格鲁棒，但安全防御可被特定风格触发绕过。
- 方法: ASO 是即插即用增强模块：微调一个图像编辑模型，把优化后的风格修改叠加到已有对抗图像上；用 GRPO agent + Structurally-Tiered 策略优化风格修改。
- 结果: 未检索到具体数字（摘要仅定性描述"放大已有视觉 jailbreak"）。
- 出身: 未核实（一作 Luo）
- 贴合度: 4/5 — plug-and-play、可叠加已有攻击，方法轻巧且揭示了一个有意思的安全盲点；扣一分因需微调图像编辑模型。
- 判断: "风格一致性 vs 安全一致性"的观察是亮点，安全研究角度新颖；缺量化结果是短板。
- 置信: abstract级（缺数字）

### AwareVLN: Reasoning with Self-awareness for Vision-Language Navigation
- 链接: https://arxiv.org/abs/2605.22816
- 问题: VLN 方法缺乏对"agent-指令-场景"关系的显式可解释理解。
- 方法: 端到端自感知推理机制；单个 VLM 联合预测 mode token（[REASON] vs [ACT]）与文本——在子任务边界等关键节点触发稀疏推理（总结场景/进度/下一步），ACT 模式将移动命令解析为低级原语。
- 结果: 未检索到具体数字。
- 出身: 未核实（一作 Guo）
- 贴合度: 2/5 — 用户暂不关注VLA（导航类）。
- 判断: [REASON]/[ACT] 双模式、按需稀疏推理的设计优雅，但属导航范畴。
- 置信: abstract级（缺数字）

### BOP-ASK: Object-Interaction Reasoning for Vision-Language Models
- 链接: https://arxiv.org/abs/2511.16857
- 问题: 现有空间推理 benchmark 只测高层关系（left of/behind），忽略精确 3D 定位、物理兼容性、affordance、多步空间规划等细粒度理解。
- 方法: 基于 BOP 数据集的 6D 物体位姿构建大规模数据集：约 150k 图像、33M+ QA 对，涵盖物体关系/操作 affordance/运动可行性/场景级推理；另发布 OOD 测试集 BOP-ASK-lab。
- 结果: 评测了闭源与开源 VLM（具体分数未检索到）。
- 出身: NVIDIA（+ NYU；作者含 Stan Birchfield, Jonathan Tremblay 等）
- 贴合度: 3/5 — 数据集/benchmark 类偏重资源，但从 6D 位姿自动派生细粒度标注的 pipeline 有工程巧思。
- 判断: 用 BOP 位姿反推 affordance/抓取/路径的思路是亮点，填补细粒度物体交互评测空白；本身是数据集贡献而非方法。
- 置信: abstract级（缺模型分数）

### Beyond 3D VQAs: Injecting 3D Spatial Priors into Vision-Language Models for Enhanced Geometric Reasoning
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Yeh_Beyond_3D_VQAs_Injecting_3D_Spatial_Priors_into_Vision-Language_Models_CVPR_2026_paper.pdf
- 问题: VLM 3D 空间推理弱；靠 3D-VQA 微调易过拟合数据集偏差，接专用 3D 编码器又笨重不灵活。
- 方法: 提出 GASP (Geometric-Aware Spatial Priors)，把几何先验直接注入 LLM 的 transformer 层，主张空间理解应源于学习基础几何先验而非高层 VQA 监督。
- 结果: 内部对应匹配准确率从 <5% 提升到 peak layer >70%、时序鲁棒 >85%；下游 All-Angles Bench +18.2%、VSI-Bench +29.0%，且不使用任何 3D VQA 数据训练。
- 出身: 未核实（作者含 Chun-Hsiao Yeh, Yi Ma, Shengyi Qian 等）
- 贴合度: 4/5 — "不用 3D VQA 数据"就大幅提升、还给出内部机制（对应匹配率）证据，小而扎实；扣一分因需改动 transformer 层。
- 判断: 亮点是把"内部对应匹配率"作为可解释探针并展示因果式提升，数字漂亮（VSI-Bench +29%）；很实。
- 置信: abstract级

### Beyond Perceptual Shortcuts: Causal-Inspired Debiasing Optimization for Generalizable Video Reasoning in Lightweight MLLMs
- 链接: https://arxiv.org/abs/2605.01324
- 问题: RL 微调让轻量 MLLM 学到数据偏差诱导的"感知捷径"而非真正推理，泛化差。
- 方法: 提出 VideoThinker 因果框架，两阶段——先经 Bias Aware Training 造一个"bias model"，再用 Causal Debiasing Policy Optimization (CDPO) 把模型推离有偏逻辑。
- 结果: VideoThinker-R1 仅用 1% RL 训练数据、无 SFT，即超 VideoRFT-3B 平均 +3.2%；并超更大的 Video-UTR-7B（MVBench +2.1%、TempCompass +3.8%）。开源。
- 出身: Sun Yat-sen University（中山大学）
- 贴合度: 5/5 — 轻量模型 + 仅 1% 数据 + 无 SFT 就超更大模型，数据高效、工程友好、开源，典型"小而美"。
- 判断: 数据效率是最大亮点（1% 数据 + 无 SFT 超 7B），CDPO 的因果去偏思路清晰；很贴合关注低成本训练的需求。
- 置信: abstract级

## 第 2 组

### Breaking the Regional Perception Bottleneck of Multimodal Large Language Models via External Reasoning Framework
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_Breaking_the_Regional_Perception_Bottleneck_of_Multimodal_Large_Language_Models_CVPR_2026_paper.pdf
- 问题: MLLM 对图像局部区域（regional）的细粒度感知能力不足，成为瓶颈。（仅标题推断）
- 方法: 提出 External Reasoning Framework，通过外部推理流程绕开 MLLM 内部的区域感知限制。（仅标题推断，搜索结果仅确认标题、作者与页码，未见方法细节）
- 结果: 未检索到
- 出身: 作者为 Jinrong Zhang、Zhaoyang Xu、Xusheng He、Xinrui Li、Na Zheng、Jianlong Wu（CVPR 2026, pp. 33531-33541）；机构未核实
- 贴合度: 3/5 — "external" 框架有 training-free / 工程化的可能性加分，但方法细节未检索到，无法确认
- 判断: 两次搜索均未抓到 abstract，只能确认这是 CVPR 2026 正式收录论文；需读原文才能评价
- 置信: 仅标题

### CodeDance: A Dynamic Tool-integrated MLLM for Executable Visual Reasoning
- 链接: https://arxiv.org/abs/2512.17312
- 问题: 固定 schema 的工具调用限制了 MLLM 的视觉推理灵活性，需要更通用的可执行推理机制。
- 方法: 以可执行代码作为通用 solver：模型自行定义、组合、执行代码来编排多工具、计算中间结果、渲染可视化产物（框/线/图表）实现透明可自检的推理；用 RL 训练，训练中涌现新工具调用、未见过的组合与跨任务迁移。
- 结果: 在 visual search、math、chart QA 等 benchmark 上一致超过 schema-driven 和 text-only baseline，并超过 GPT-4o 等闭源模型和更大的开源模型（未见具体数字）。
- 出身: 未核实（作者 Qi Song、Honglin Li、Yingchen Yu 等；有开源 repo CodeDance-VL/CodeDance）
- 贴合度: 4/5 — code-as-tool 的可执行视觉推理方向工程价值高、有开源代码；但需 RL 训练，非 training-free
- 判断: 亮点是从固定 schema 工具调用升级到自由代码编排且有涌现组合能力；"超过 GPT-4o"需看具体任务口径
- 置信: abstract级

### Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning
- 链接: https://arxiv.org/abs/2512.24426
- 问题: 驾驶 VLA 模型缺乏在执行前审视并修正自身规划动作的能力。
- 方法: CF-VLA 先生成分时间段的 meta-actions 概括驾驶意图，再基于 meta-actions 和视觉上下文做 counterfactual reasoning，模拟潜在后果、识别不安全行为并输出修正后的 meta-actions 指导轨迹生成；具备自适应思考（仅在困难场景启用反事实推理）。
- 结果: 大规模驾驶数据集上轨迹精度提升最高 17.6%，安全指标提升 20.5%。
- 出身: 未核实（作者 Zhenghao Peng、Wenhao Ding 等 14 人）
- 贴合度: 2/5 — 用户暂不关注VLA；adaptive reasoning 的按需思考机制本身有借鉴价值
- 判断: 反事实自省 + 按需推理是驾驶 VLA 里较优雅的安全机制，但领域不在用户关注范围
- 置信: abstract级

### Decouple to Generalize: Context-First Self-Evolving Learning for Data-Scarce Vision-Language Reasoning
- 链接: https://arxiv.org/abs/2512.06835
- 问题: VLM 的 RL 训练依赖大量高质量多模态数据，在化学、地球科学、多模态数学等数据稀缺的专业领域难以开展。
- 方法: DoGe 双解耦框架：把自演化认知过程解耦为"learning-application"循环，设计可学习的 Thinker + 冻结的 Solver 两个组件，先从问题 context 学习而非直接解题；建立在 multimodal GRPO 之上。
- 结果: 未检索到（具体数字搜索摘要未给出）
- 出身: 未核实
- 贴合度: 3/5 — 面向 data-scarce 场景的自演化方案有实用价值，冻结 Solver 的设计较轻量；但仍是 RL 训练路线且效果数字未见
- 判断: "context-first"解耦是针对合成数据方法忽视问题情境的合理切入，泛化性主张需看实验
- 置信: abstract级

### DeepScan: A Training-Free Framework for Visually Grounded Reasoning in Large Vision-Language Models
- 链接: https://arxiv.org/abs/2603.03857
- 问题: 现有 grounded reasoning 方法追求一次性定位完整证据，在干扰性上下文中鲁棒性差。
- 方法: 三阶段 training-free 流程：Hierarchical Scanning 自底向上做局部线索探索与多尺度证据提取；Refocusing 由 LVLM 与视觉专家协同优化证据视图；Evidence-Enhanced Reasoning 通过 hybrid evidence memory 聚合多粒度视图。
- 结果: 搭配 Qwen2.5-VL-7B 在 V* 上达 90.6% 总体准确率；即插即用，可在测试时接入不同 LVLM backbone。
- 出身: 未核实（作者 Yangfu Li、Hongjian Zhan 等；代码开源 github.com/YChenL/DeepScan）
- 贴合度: 5/5 — training-free、即插即用、7B 小模型出强结果且开源，完全命中用户偏好
- 判断: 亮点是无需 RL 训练即在 V* 逼近/超过训练类方法；代价可能是多阶段推理的 test-time 开销（搜索结果未提延迟）
- 置信: abstract级

### Deeper Thought, Weaker Aim: Understanding and Mitigating Perceptual Impairment during Reasoning in Multimodal Large Language Models
- 链接: https://arxiv.org/abs/2603.14184
- 问题: MLLM 在长推理模式下出现感知受损：多步推理时视觉注意力发散、漂离问题相关区域，"想得越深看得越偏"。
- 方法: 定位根因为 attention dispersion；提出 training-free 的 Visual Region-Guided Attention (VRGA)，按 entropy-focus 准则选出视觉头并重加权其注意力，引导模型在推理中聚焦问题相关区域。
- 结果: 在 visual grounding 与推理准确率上有提升（具体数字未检索到）。
- 出身: 未核实（作者 Ruiying Peng、Xueyu Wu、Lu Hou 等）
- 贴合度: 5/5 — 诊断+机制分析+training-free 注意力干预，小而美，典型的可直接落地的推理期修补
- 判断: 亮点是把"推理伤害感知"归因到可操作的注意力头层面；局限是 attention 重加权类方法对模型/任务的普适性常需逐个验证
- 置信: abstract级

### EE-RL: Vision Language Guided Reinforcement Learning with Explorer and Expert model for End-to-End Autonomous Driving
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Li_EE-RL_Vision_Language_Guided_Reinforcement_Learning_with_Explorer_and_Expert_CVPR_2026_paper.pdf
- 问题: 端到端自动驾驶在稀疏关键场景下策略学习困难。
- 方法: RL-based Explorer + LoRA 微调的 VLM Expert 组合，双 replay buffer；设计 StateHash 度量图像与车辆状态相似度以跳过不必要的 VLM 推理、提升单位时间专家经验产量；统一支持 SAC/TD3/DDPG 三种 off-policy backbone。
- 结果: 未检索到具体数字（搜索摘要仅描述框架，代码开源 github.com/CAVTestLab/EE-RL）
- 出身: 未核实（作者 Xiaolong Li、Lan Yang 等；CVPR 2026, pp. 32082-32092）
- 贴合度: 2/5 — 驾驶类固定≤2，用户暂不关注VLA/驾驶；StateHash 缓存 VLM 推理的工程技巧本身可借鉴
- 判断: StateHash 去重跳过 VLM 推理是实用的降本设计，但整体属驾驶 RL 管线，不在用户关注面
- 置信: abstract级

### EMO-R3: Reflective Reinforcement Learning for Emotional Reasoning in Multimodal Large Language Models
- 链接: https://arxiv.org/abs/2602.23802
- 问题: MLLM 难以捕捉人类情绪的复杂性与主观性；SFT 泛化差、可解释性弱，GRPO 类 RL 又不契合情绪认知的内在特性。
- 方法: 两个组件：Structured Emotional Thinking 引导模型按步骤、按可解释格式做情绪推理；Reflective Emotional Reward 让模型复评自身推理，含视觉-文本一致性与情绪推理有效性两类奖励。
- 结果: 未检索到（搜索摘要未给具体数字）
- 出身: 未核实（作者 Yiyang Fang 等 8 人）
- 贴合度: 2/5 — 情绪推理是垂直小领域，RL 训练路线且无突出工程/通用价值信号；reflective reward 设计中规中矩
- 判断: 把反思机制做进 reward 是合理尝试，但情绪任务的"主观性"恰恰让 reward 可靠性存疑
- 置信: abstract级

### EgoMind: Activating Spatial Cognition through Linguistic Reasoning in MLLMs
- 链接: https://arxiv.org/abs/2604.03318
- 问题: 现有空间推理方法依赖 3D 先验或几何监督、数据准备成本高，纯 2D 方法又难以处理跨帧空间关系。
- 方法: geometry-free 的 CoT 框架：Role-Play Caption 跨帧联合构建连贯的语言化 scene graph，Progressive Spatial Analysis 逐步推理到任务问题；仅用 5K 自动生成的 SFT 样本 + 20K RL 样本。
- 结果: 在 VSI-Bench、SPAR-Bench、SITE-Bench、SPBench 上取得有竞争力的结果（具体数字未检索到）。
- 出身: Beihang University（北航，作者 Zhenghao Chen、Huiqun Wang、Di Huang）
- 贴合度: 4/5 — 免 3D 监督、数据量小（5K SFT + 20K RL），"小而美"路线加分；仍需训练故不满分
- 判断: 亮点是证明纯语言化空间推理可替代昂贵的几何监督；"competitive"措辞暗示未必全面 SOTA
- 置信: abstract级

### EgoProx: Evaluating MLLMs on Egocentric 3D Proximity Reasoning Across a Cognitive Hierarchy
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Li_EgoProx_Evaluating_MLLMs_on_Egocentric_3D_Proximity_Reasoning_Across_a_CVPR_2026_paper.pdf
- 问题: MLLM 能否从第一人称视角对身体与周围物体的 3D 邻近关系做具身推理（3D 感知-动作耦合）尚不清楚。
- 方法: 首个 egocentric 3D proximity reasoning benchmark，按认知层级分四维：Intention、Exploration、Exploitation、Chain of Actions；用近似变换与相对空间关系表示 proximity，agent-based 数据引擎规模化生成一致的 QA 对。
- 结果: 主流 MLLM 含有一定空间知识，但仍难以在空间推理 VQA 中有效利用（具体数字未检索到）。
- 出身: 未核实
- 贴合度: 2/5 — 纯 benchmark 论文减分，且偏具身/egocentric 场景；认知层级的任务分解设计尚有参考价值
- 判断: 结论（模型"有知识但用不出来"）与本 chunk 多篇诊断类工作互相印证，但作为评测集对用户直接价值有限
- 置信: abstract级

## 第 3 组

### Eliciting Complex Spatial Reasoning in MLLMs through Wide-Baseline Matching
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Zhong_Eliciting_Complex_Spatial_Reasoning_in_MLLMs_through_Wide-Baseline_Matching_CVPR_2026_paper.pdf
- 问题: （仅标题推断）通过 wide-baseline 图像匹配任务激发 MLLM 的复杂空间推理能力
- 方法: 未检索到（仅标题推断：可能以宽基线视角对应/匹配作为训练或提示信号）
- 结果: 未检索到
- 出身: 未核实
- 贴合度: 3/5 — 匹配驱动空间推理的思路可能小而美，但两次检索均未命中，无法确认是否 training-free 或重训练
- 判断: 两次搜索均未检索到该论文的任何摘要信息，暂无法评估
- 置信: 仅标题

### Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning
- 链接: https://arxiv.org/abs/2601.09708
- 问题: VLA 中显式 CoT 推理链过长导致推理延迟高
- 方法: 用 latent CoT 做可言语化（verbalizable）的隐式规划，从教师模型蒸馏，并用 preference-guided 目标对齐操作轨迹，迁移语言与视觉规划能力
- 结果: 相比现有方法推理延迟最高降低 89.3%
- 出身: NVIDIA Research Taiwan（搜索结果含 research.nvidia.com 页面）
- 贴合度: 2/5 — 用户暂不关注VLA；latent CoT 蒸馏思路本身对效率工程有借鉴价值
- 判断: 亮点是把"推理提速"落到 VLA 场景且保留可解释性（latent 可 verbalize），但领域不在用户关注面上
- 置信: abstract级

### From Indoor to Open World: Revealing the Spatial Reasoning Gap in MLLMs
- 链接: https://arxiv.org/abs/2512.19683
- 问题: 现有空间推理 benchmark 局限于室内或过于简化，无法诊断 MLLM 在开放世界的空间智能
- 方法: 用同步 stereo 相机 + LiDAR + IMU/GPS 的行人视角视频构建大规模户外 benchmark，自动生成从定性关系到定量度量/运动学的分层空间问题
- 结果: 室内 benchmark 上的性能增益在开放世界设置中消失；模型严重依赖语言先验而非视觉 grounding
- 出身: 未核实
- 贴合度: 2/5 — 纯 benchmark 且传感器采集重资源；"室内增益户外失效"的结论有参考价值但无方法产出
- 判断: 结论（linguistic prior 依赖）对评估空间推理方法有警示意义，但属于诊断型工作
- 置信: abstract级

### From Intuition to Investigation: A Tool-Augmented Reasoning MLLM Framework for Generalizable Face Anti-Spoofing
- 链接: https://arxiv.org/abs/2603.01038
- 问题: MLLM 式 FAS 只生成粗粒度语义描述（如 mask 轮廓），难感知细粒度视觉痕迹，跨域泛化受限
- 方法: TAR-FAS 框架，将 FAS 重构为 Chain-of-Thought with Visual Tools (CoT-VT)：先直觉观察、再自适应调用外部视觉工具做细粒度取证；配套工具增强标注 pipeline 与 ToolFAS-16K 多轮工具调用轨迹数据集
- 结果: 在 one-to-eleven 跨域协议下达 SOTA（未检索到具体数字）
- 出身: 未核实
- 贴合度: 3/5 — agentic tool-use 思路工程化、数据集小（16K）加分；但 FAS 垂直领域较窄
- 判断: 亮点是把 agent 式工具调用引入取证型视觉任务，范式可迁移到其他细粒度检测
- 置信: abstract级

### G$^2$VLM: Geometry Grounded Vision Language Model with Unified 3D Reconstruction and Spatial Reasoning
- 链接: https://arxiv.org/abs/2511.21688
- 问题: 3D 重建与空间理解在 VLM 中割裂，空间推理缺乏几何 grounding
- 方法: Mixture-of-Transformer-Experts 架构：几何感知 expert（视觉几何学习）+ 语义感知 expert（多模态理解），经共享 self-attention 交互；原生用学到的 3D 几何特征直接预测 3D 属性并支持 in-context/交错推理
- 结果: 未检索到具体数字；已开源（GitHub InternRobotics/G2VLM，含 2B-MoT 权重）
- 出身: InternRobotics（上海AI实验室系，Jiangmiao Pang 等；GitHub org 明确）
- 贴合度: 3/5 — 统一模型需重训练减分；2B 规模不大且代码权重全开源加分
- 判断: 亮点是重建与推理真正共享几何特征而非外挂 depth；预印本较早（2025-11），CVPR 版可能有更新
- 置信: abstract级

### Generate, Analyze, and Refine: Training-Free Sound Source Localization via MLLM Meta-Reasoning
- 链接: https://arxiv.org/abs/2604.06824
- 问题: 对比学习式声源定位缺乏显式推理与验证，复杂声学场景下失效
- 方法: Training-free 的 GAR 三段 pipeline：Generation 产生初始 bbox 与音频分类；Analysis 用 open-set role tagging + anchor voting 量化 Audio-Visual Consistency；Refinement 用自适应 gating 避免不必要修正
- 结果: 单源/多源 benchmark 上取得有竞争力的性能（未检索到具体数字）；代码开源（GAR-SSL）
- 出身: Kyung Hee University（Subin Park, Jung Uk Kim）
- 贴合度: 5/5 — training-free、纯 prompt/pipeline 工程、小而美、开源，正中偏好
- 判断: 亮点是"生成-自检-修正"的 meta-reasoning 闭环无需任何训练；局限是仅"competitive"而非明确超越训练式方法
- 置信: abstract级

### Grounded Chain-of-Thought for Multimodal Large Language Models
- 链接: https://arxiv.org/abs/2503.12799
- 问题: MLLM 视觉幻觉严重，答案缺乏可验证的视觉空间依据
- 方法: 提出 Grounded CoT (GCoT) 学习任务：模型逐步识别并 ground 相关视觉线索（输出坐标）作为答案依据；构建 MM-GCoT 数据集（5,033 图、24,022 条 GCoT 样本）与答案准确率/grounding 准确率/一致性三维评测体系
- 结果: 未检索到具体数字
- 出身: 未核实（作者 Qiong Wu、Rongrong Ji 等，搜索结果未明示机构）
- 贴合度: 3/5 — 数据集小（24K）、思路直击幻觉可验证性加分；需微调、偏 benchmark 建设减分
- 判断: "答案-grounding 一致性"这一评测维度比数据集本身更有复用价值
- 置信: abstract级

### HandVQA: Diagnosing and Improving Fine-Grained Spatial Reasoning about Hands in Vision-Language Models
- 链接: https://arxiv.org/abs/2603.26362
- 问题: VLM 在通用 benchmark 近人类水平，但对手部这类高自由度关节结构的细粒度空间推理系统性失败
- 方法: 基于 FreiHAND/InterHand2.6M/FPHA 三个 3D 手部数据集自动构建 160 万+受控多选题（关节角度、距离、相对位置），诊断出手指幻觉、几何误读等模式，并用 3D-grounded 数据训练改进
- 结果: 学到的 3D 空间知识零样本迁移：手势识别 +10.33%、hand-object interaction +2.63%
- 出身: 未核实
- 贴合度: 3/5 — 从既有 3D 数据集程序化造题的 pipeline 成本低、可复制加分；本质仍是 benchmark+微调路线
- 判断: 亮点是诊断到改进的完整闭环且有零样本迁移证据；1.6M 题量对训练资源有一定要求
- 置信: abstract级

### Harnessing Chain-of-Thought Reasoning in Multimodal Large Language Models for Face Anti-Spoofing
- 链接: https://arxiv.org/abs/2506.01783
- 问题: FAS 依赖单一视觉模态做二分类，跨设备/环境/攻击类型泛化差且不可解释
- 方法: 提出 FaceCoT——首个面向 FAS 的大规模 VQA/CoT 数据集，含 108 万训练样本（源自 CelebA-Spoof 与 WFAS），覆盖 2D 打印、屏幕重放、3D 面具等 14 类攻击，用视觉-语言协同推理做检测
- 结果: 搜索摘要称显著提升鲁棒性与可解释性；未检索到具体数字
- 出身: 未核实（作者 Honglu Zhang、Zhaofeng He 等）
- 贴合度: 2/5 — 以百万级数据集构建为主体，重资源、偏 benchmark；与同 chunk 的 TAR-FAS 相比工程巧思较少
- 判断: 价值主要在数据资产（首个 FAS CoT-VQA 数据集）；方法层面是标准 MLLM 微调路线
- 置信: abstract级

### HoneyBee: Data Recipes for Vision-Language Reasoners
- 链接: https://arxiv.org/abs/2510.12225
- 问题: 高性能视觉-语言推理训练数据该怎么配比/构建，其原理缺乏系统研究
- 方法: 受控实验系统研究数据配方：context（图-题对）来源策略、定向干预（image caption 辅助信号、混入 text-only 推理数据）、以及图像/问题/CoT 三维度扩量；产出 HoneyBee 数据集（350K 图-题对、2.5M CoT 样本）
- 结果: 3B 模型在 MathVerse 上超 SOTA 7.8%、超 base 模型 24.8%；caption 辅助与 text-only 推理混入均带来显著增益
- 出身: Meta FAIR + UCLA（Hritik Bansal 等）
- 贴合度: 3/5 — 数据配方结论（caption 信号、text-only 混入、扩量规律）可直接指导实践加分；2.5M CoT 的复现成本高减分
- 判断: 亮点是少见的受控数据消融科学，结论比数据集本身更值得记；3B 小模型打 SOTA 有说服力
- 置信: abstract级

## 第 4 组

### HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.pdf
- 问题: 自动驾驶 VLA 的动作选择缺乏前瞻推理与审慎评估。
- 方法: 混合式 VLA：Visual CoT (V-CoT) 做视觉前瞻（visual anticipation），Tree-of-Thought Evaluation (ToT-E) 对候选动作做审慎评估后再选择。
- 结果: 未检索到（搜索结果只给出 CVPR 2026 收录页码 32421-32430，无量化指标）。
- 出身: 未核实（作者 Bassole, Kim, Jung, Sung 等，机构未在搜索结果中提及）。
- 贴合度: 2/5 — 用户暂不关注 VLA；驾驶类固定≤2。
- 判断: V-CoT + ToT 组合思路常见，且 ToT 推理开销大，工程落地存疑；细节太少难以判断增量。
- 置信: abstract级（信息很薄，仅一句方法描述）

### IBISAgent: Reinforcing Pixel-Level Visual Reasoning in MLLMs for Universal Biomedical Object Referring and Segmentation
- 链接: https://arxiv.org/abs/2601.03054
- 问题: 现有 MLLM 分割方案靠隐式 seg token + 同时微调像素 decoder，易灾难性遗忘，且单趟推理无法迭代修正 mask。
- 方法: 把分割重构成多步 MDP：MLLM 生成交错的推理 + 文本 click 动作、调用分割工具（SAM2）产 mask，不改架构；两阶段训练 + 细粒度 reward 激励持续自我改进。基座 Qwen2.5-VL-7B。
- 结果: 未检索到具体数字（仅"高质量 mask、无需架构修改"的定性描述）。
- 出身: 未核实（作者 Yankai Jiang 等，搜索结果只列人名未列机构；GitHub: Yankai96/IBISAgent）。
- 贴合度: 3/5 — 不改架构、复用 SAM2 的 agentic 设计工程味足（加分），但需两阶段 RL 训练且限生物医学域（减分）。
- 判断: 亮点是"click 动作 + 工具调用"替代 seg token，避免动 decoder；可迁移到通用 referring segmentation，值得关注开源实现。
- 置信: abstract级

### ID-Crafter: VLM-Grounded Online RL for Compositional Multi-Subject Video Generation
- 链接: https://arxiv.org/abs/2511.00511
- 问题: 多主体视频生成中各主体身份信息互相冲突，identity 保持与交互语义双双退化。
- 方法: 三件套：层级 identity-preserving attention（intra-subject / inter-subject / cross-modal 逐级聚合）；预训练 VLM 做细粒度语义引导捕捉主体间关系；再加 online RL 阶段针对关键概念精修。
- 结果: 声称在多主体视频生成 benchmark 上达新 SOTA（identity 保持、时序一致性、整体质量），未检索到具体数字。
- 出身: Xiamen University、East China Normal University、Peking University、CUHK（搜索结果明确提到）。
- 贴合度: 2/5 — 视频生成 + online RL 属重资源训练路线，attention 层级设计偏堆叠，非用户偏好的小而美。
- 判断: VLM 当 reward/grounding 源做视频生成 RL 是当前热门配方，工程复现成本高；亮点在把 identity 冲突拆成三个聚合层级。
- 置信: abstract级

### Incentivizing Versatile Video Reasoning in MLLMs via Data-Efficient Reinforcement Learning
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_Incentivizing_Versatile_Video_Reasoning_in_MLLMs_via_Data-Efficient_Reinforcement_Learning_CVPR_2026_paper.pdf
- 问题: 用少量数据通过 RL 激发 MLLM 的多任务（versatile）视频推理能力（仅标题推断）。
- 方法: 数据高效 RL；supplemental 片段仅提到"multi-task cold start 对最新 Qwen3-VL-8B 带来一致增益"，具体机制未检索到。
- 结果: 未检索到。
- 出身: 未核实。
- 贴合度: 3/5 — data-efficient RL 方向贴合（加分），但两次搜索几乎没挖到实质内容，无法确认含金量。
- 判断: 局限：公开信息极少（无 arXiv 页可见），只能等读原文；"多任务 cold start"这一点与 VideoRFT 一脉相承。
- 置信: 仅标题（附一句 supplemental 片段）

### Keep it SymPL: Symbolic Projective Layout for Allocentric Spatial Reasoning in Vision-Language Models
- 链接: https://arxiv.org/abs/2602.19117
- 问题: VLM 擅长 egocentric 空间推理，但换到 allocentric（以物体为中心）视角时性能大幅退化。
- 方法: SymPL 把 allocentric 问题重构成 VLM 天然擅长的符号布局形式：从图像+问题估计 3D 信息 → 正交投影 → 物体抽象为最小符号 → 空间划分为两色区域 → 查询转成位置估计任务。
- 结果: allocentric 与 egocentric 任务均"substantially improves"，且在视觉错觉与多视角场景下更鲁棒；未检索到具体数字。
- 出身: 未核实。
- 贴合度: 4/5 — 推理时重构、无需训练的 pipeline，小而美、机制可解释（加分）；依赖 3D 估计模块的级联误差是隐患。
- 判断: 亮点：不训模型而是把问题"翻译"成模型会做的形式，属典型 training-free 巧思，值得 /paper 深读。
- 置信: abstract级

### Learning to Focus and Precise Cropping: A Reinforcement Learning Framework with Information Gaps and Grounding Loss for MLLMs
- 链接: https://arxiv.org/abs/2603.27494
- 问题: MLLM 用裁剪工具看细节时过度依赖全局输入、不真正利用裁剪区域内的信息。
- 方法: 两阶段 RL、无需轨迹监督：阶段一"Information Gap"——降低全局图粒度，逼模型靠裁剪区域的信息增益答题；阶段二用少量 bbox 标注加 grounding loss 提升裁剪精度。
- 结果: 声称在高分辨率 VQA benchmark 上达 SOTA；未检索到具体数字。
- 出身: University of Science and Technology of China（USTC）等。
- 贴合度: 4/5 — 无轨迹监督 + 少量标注的 data-efficient 设计，"信息差逼迫聚焦"机制简洁，工程化强（加分）。
- 判断: 亮点：用输入退化制造 information gap 来塑造 reward，比堆裁剪轨迹数据优雅；对"看小字/高分屏截图"类应用直接有用。
- 置信: abstract级

### Learning to Reason in 4D: Dynamic Spatial Understanding for Vision Language Models
- 链接: https://arxiv.org/abs/2512.20557
- 问题: VLM 在动态空间推理（DSR）上很弱——难以推理 3D 几何与物体关系随时间的演化。
- 方法: DSR Suite 三件套：自动 pipeline 从野生视频抽取相机位姿/点云/mask/朝向/3D 轨迹生成 MCQ 数据（DSR-Train）+ benchmark + 轻量 Geometry Selection Module (GSM)，把预训练 4D 重建先验按问题语义压缩成少量 geometry token 注入 VLM。
- 结果: 集成到 Qwen2.5-VL-7B 后动态空间推理能力显著提升，且通用视频理解 benchmark 精度不掉；未检索到具体数字。
- 出身: The University of Hong Kong + ARC Lab, Tencent PCG。
- 贴合度: 3/5 — 轻量模块加分，但 dataset+benchmark+model 全家桶偏重、偏 benchmark 驱动。
- 判断: 亮点是 GSM 轻量注入 4D 先验而非全量重训；但数据管线依赖多个 4D 重建模型，复现资源不低。
- 置信: abstract级

### MindPower: Enabling Theory-of-Mind Reasoning in VLM-based Embodied Agents
- 链接: https://arxiv.org/abs/2511.23055
- 问题: VLM 具身 agent 缺乏 Theory-of-Mind 决策；现有 ToM benchmark 只测人类心理状态、忽略机器人自身视角，导致决策与动作不连贯。
- 方法: Robot-Centric 框架：Perception → Belief/Desire/Intention（Mental Reasoning）→ Decision → Action 三级六层；提出 Mind-Reward 优化目标，约束 ToM 推理与行为一致；配 False-Belief Correction 与 Implicit Goal Inference 两个评测任务。
- 结果: 决策上超 GPT-4o 12.77%，动作生成超 12.49%。
- 出身: 未核实（项目页 zhangdaxia22.github.io）。
- 贴合度: 2/5 — 具身 agent 决策-动作类，按 VLA/导航口径固定≤2，用户暂不关注 VLA。
- 判断: "机器人自身视角的 ToM"切入点新，但比较基线是 GPT-4o 提示式方案，说服力有限。
- 置信: abstract级

### MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models
- 链接: https://arxiv.org/abs/2603.24984
- 问题: MoE VLM 的确定性 top-K 路由会错过更优专家组合并导致专家过拟合。
- 方法: 把专家选择形式化为序列决策问题，用 GRPO 优化路由策略，让模型通过探索 + reward 反馈学自适应 expert routing。
- 结果: 未检索到具体数字（CVPR 2026 收录，pages 14957-14967）。
- 出身: Korea University + KAIST（一作 Dohwan Ko）。
- 贴合度: 3/5 — "用 GRPO 训路由而非权重"角度干净、问题定义小而美（加分），但需要 MoE VLM 全量 RL 训练、资源门槛高（减分）。
- 判断: 亮点：把 RL 后训练的作用点从生成内容移到架构内部路由，思路可复用到 LLM MoE；效果量级未知。
- 置信: abstract级

### NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning
- 链接: https://arxiv.org/abs/2602.21172
- 问题: 驾驶 VLA 依赖海量数据 + 昂贵的密集 reasoning 标注，训练/推理都贵。
- 方法: NoRD（No Reasoning for Driving）：基于 Qwen2.5-VL-3B-Instruct 直接预测 action token、不产推理轨迹；针对小规模无推理数据上标准 GRPO 因 difficulty bias 失效的问题，改用 Dr. GRPO。
- 结果: 在 Waymo 与 NAVSIM 上以不到 60% 的微调数据、零 reasoning 标注达到与现有 VLA 相当的性能，token 数减少 3 倍。
- 出身: Applied Intuition（research blog + 开源仓库 Applied-Intuition-Open-Source/nord）。
- 贴合度: 2/5 — 驾驶 VLA 固定≤2，用户暂不关注 VLA；不过其"去 reasoning + Dr. GRPO 修 difficulty bias"的反思本身有借鉴价值。
- 判断: 亮点：工业界的"反 CoT"实证——推理轨迹对驾驶动作预测可能是昂贵的冗余，这一结论对其他 VLA 域也有警示意义。
- 置信: abstract级

## 第 5 组

### ORCA: Orchestrated Reasoning with Collaborative Agents for Document Visual Question Answering
- 链接: https://arxiv.org/abs/2603.02438
- 问题: DocVQA 中单一模型对多模态文档组件（文本/表格/图形）理解不细、推理不可控。
- 方法: 多智能体框架：reasoning agent 先把 query 分解为逻辑步骤，routing 机制从 "agent dock" 激活各模态专用 agent；加 debate + thesis-antithesis 仲裁和 sanity checker 保证一致性。
- 结果: 在 3 个 benchmark 上显著超 SOTA（搜索摘要未给具体数字）；代码开源（github.com/AymenLass/ORCA）。
- 出身: 未核实（作者 Aymen Lassoued, Mohamed Ali Souibgui, Yousri Kessentini）。
- 贴合度: 4/5 — 编排式 agent 系统偏工程化、可复用，debate/仲裁机制是现成 MLLM 之上的 orchestration（近 training-free）；扣分点是 pipeline 较重、无具体数字可核。
- 判断: 亮点是把"分解-路由-辩论-校验"做成完整可开源的 DocVQA agent 范式；局限是多 agent 推理成本和延迟未知。
- 置信: abstract级

### PDCR: Perception-Decomposed Confidence Reward for Vision-Language Reasoning
- 链接: https://arxiv.org/abs/2605.13467
- 问题: RL 训练 VLM 推理时，全局 reward 归一化把稀疏的视觉感知步骤信号淹没在大量文本推理步骤里（mixture-induced signal degradation）。
- 方法: 无监督技能分解：用模型内部的 Visual Dependence Score 量化每步的视觉依赖，聚类分离 perception/reasoning 步骤，再在各技能簇内部归一化 confidence gain 计算分解式 advantage。
- 结果: 未检索到具体数字；代码开源（github.com/hee-suk-yoon/PDCR）。
- 出身: KAIST、UIUC、Microsoft Research Asia。
- 贴合度: 4/5 — 小而美的 reward 设计洞察（分簇归一化），无需额外标注，可直接嫁接到现有 RLVR 流程；扣分是仍属 RL 训练方法、需算力。
- 判断: 亮点是指出并量化了"视觉步骤被文本步骤统计淹没"这一具体病灶，思路可迁移到其他混合技能 RL 场景。
- 置信: abstract级

### POINTS-Long: Adaptive Dual-Mode Visual Reasoning in MLLMs
- 链接: https://arxiv.org/abs/2604.11627
- 问题: MLLM 处理长视觉输入时视觉 token 开销大，精度与效率难以按需权衡。
- 方法: 原生双模式 MLLM（focus / standby），仿人眼动态缩放视觉 token；配可动态拆卸的 KV-cache 设计，原生支持流式视觉理解和超长视觉记忆。
- 结果: 细粒度任务 focus 模式保持最优；长视觉理解 standby 模式仅用 1/40–1/10 视觉 token 保留 97.7–99.7% 原精度。
- 出身: 上海交通大学 + 腾讯 WeChat AI。
- 贴合度: 4/5 — 效率工程导向强（token 压缩 + KV-cache 可拆卸），数字扎实，工业团队出品可落地；扣分是需原生训练双模式，非即插即用。
- 判断: 亮点是把"精度-效率"做成推理期可切换的旋钮而非两个模型；40 倍 token 压缩下精度几乎无损的数字很亮眼。
- 置信: abstract级

### PROMPTMINER: Black-Box Prompt Stealing against Text-to-Image Generative Models via Reinforcement Learning and VLM-Guided Optimization
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Li_PROMPTMINER_Black-Box_Prompt_Stealing_against_Text-to-Image_Generative_Models_via_Reinforcement_CVPR_2026_paper.pdf
- 问题: 从生成图像黑盒逆向出高价值 T2I prompt——现有方法要么需白盒梯度、要么依赖大规模标注数据。
- 方法: 将 prompt stealing 建模为 MDP，在冻结 captioner 之上用 RL 训练轻量 adapter，potential-based reward shaping 提供稠密引导，再加 fuzz testing 式优化阶段挖掘有效 modifier。
- 结果: 在 3 个数据集、4 个 T2I 模型上图像相似度与文本对齐均达 SOTA；可泛化到未知目标模型的 in-the-wild 图像，对常见后处理防御鲁棒。具体数字未检索到。
- 出身: 未核实。
- 贴合度: 3/5 — 冻结 captioner + 小 adapter 的轻量工程路线加分，攻击框架完整；但属安全攻击细分方向，与用户主线（推理/效率）距离较远。
- 判断: 亮点是把 fuzz testing 引入 prompt 逆向这一跨界组合；局限是价值偏红队/IP 保护场景。
- 置信: abstract级

### PixDLM: A Dual-Path Multimodal Language Model for UAV Reasoning Segmentation
- 链接: https://arxiv.org/abs/2604.15670
- 问题: UAV 遥感影像的 reasoning segmentation：斜视角、超高分辨率、极端尺度变化、小目标使现有 MLLM 分割方法失效。
- 方法: 定义 Spatial/Attribute/Scene 三维语义推理任务，构建 DRSeg benchmark（1 万张高分辨率航拍图 + CoT QA 标注）；模型用 Dual-Path encoder（解耦语义推理与像素感知）+ 层次化 decoder。
- 结果: CVPR 2026 Highlight；具体指标数字未检索到；数据/模型/代码开源。
- 出身: 厦门大学（MAC 组）。
- 贴合度: 2/5 — 数据集 + 领域专用模型的重资源路线，UAV 遥感垂直领域与用户方向重叠小；Highlight 和全开源是加分项但不改变领域错位。
- 判断: 亮点是双路解耦设计和高质量 CoT 标注 benchmark；对不做遥感的用户主要是方法论参考。
- 置信: abstract级

### Pixels Don't Lie (But Your Detector Might): Bootstrapping MLLM-as-a-Judge for Trustworthy Deepfake Detection and Reasoning Supervision
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Kuckreja_Pixels_Dont_Lie_But_Your_Detector_Might_Bootstrapping_MLLM-as-a-Judge_for_CVPR_2026_paper.pdf
- 问题: deepfake 检测模型给出的自然语言解释常常没有视觉证据支撑，可靠性存疑。
- 方法: DeepfakeJudge 框架：OOD benchmark（含最新生成/编辑伪造）+ 人工视觉推理标注子集 + 一组无需 ground-truth rationale 的评估模型；Judge 通过 bootstrapped generator-evaluator 过程把少量人工反馈放大为结构化推理监督，支持 pointwise/pairwise 评估。
- 结果: meta-evaluation 上 reasoning-bootstrapped 模型准确率 96.2%，胜过大 30 倍的 baseline；judge 与人工评分高相关、pairwise 一致率 98.9%；用户研究 70% 偏好其生成的 reasoning。数据/模型/代码全开源。
- 出身: 未核实（GitHub: KjAeRsTuIsK/DeepfakeJudge）。
- 贴合度: 4/5 — 小模型打赢 30x 大模型的"小而美"典型，bootstrap 人工反馈的监督放大思路可迁移到任何 MLLM-as-a-judge 场景；扣分是 deepfake 垂直领域。
- 判断: 亮点是"评推理质量不需要 ground-truth rationale"这一 judge 设计，比结果本身更有通用价值。
- 置信: abstract级

### Progress-Think: Semantic Progress Reasoning for Vision-Language Navigation
- 链接: https://arxiv.org/abs/2511.17097
- 问题: VLN 长程任务中 agent 不清楚自己在多步指令中"走到了哪一步"，现有方法只预测数值进度或直接出动作。
- 方法: 语义进度推理：从视觉观测预测"指令风格"的进度描述。三阶段：Self-Aligned Progress Pretraining（视觉历史与指令前缀的可微对齐自举推理模块）、Progress-Guided Policy Pretraining（进度状态注入导航上下文）、后续微调。
- 结果: R2R-CE、RxR-CE 上导航性能、时序一致性、可解释性均有提升；具体数字未检索到。
- 出身: 未核实（Shao Wang 等 12 位作者）。
- 贴合度: 2/5 — 用户暂不关注VLA/导航类，固定≤2；语义进度对齐的想法本身不错。
- 判断: "monotonic co-progression"（观测与指令单调共进）是个干净的归纳偏置，但应用域不在用户关注范围。
- 置信: abstract级

### Prototypical Action Reasoning Facilitated by Vision-Language Alignment for Egocentric Action Anticipation
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Shao_Prototypical_Action_Reasoning_Facilitated_by_Vision-Language_Alignment_for_Egocentric_Action_CVPR_2026_paper.pdf
- 问题: 第一人称视频的动作预判（egocentric action anticipation）（仅标题推断）。
- 方法: 未检索到；仅标题推断：以动作原型（prototype）为中介、借视觉-语言对齐做动作推理。
- 结果: 未检索到（两次搜索均未命中该论文）。
- 出身: 未核实。
- 贴合度: 2/5 — 仅标题可判：egocentric 动作预判属视频理解垂直方向，与用户主线重叠低；原型+对齐听起来是常规组合。
- 判断: 信息不足，无法评估贡献大小；如需可后续用 /paper 直读原文。
- 置信: 仅标题

### QUANTIPHY: A Quantitative Benchmark Evaluating Physical Reasoning Abilities of Vision-Language Models
- 链接: https://arxiv.org/abs/2512.19526
- 问题: 现有物理推理评测都是定性 VQA，无法衡量 VLM 能否从视频定量推断运动学量。
- 方法: 首个定量物理推理 benchmark：3.3K+ 视频-文本实例带数值 ground truth，给定一个物理属性作先验，评估对物体尺寸、速度、加速度的数值估计；统一 prompt 与打分标准。
- 结果: 当前 VLM"说得头头是道但算不对"——定性理解与定量推理之间存在显著 gap（具体分数未检索到）。
- 出身: Stanford（Li Fei-Fei、Ehsan Adeli 等）。
- 贴合度: 2/5 — 纯 benchmark 减分，无方法贡献；"定量而非 VQA"的评测角度和数值 ground truth 设计是其中亮点。
- 判断: 作为诊断工具有价值（暴露 VLM 数值物理推理短板），但对用户可直接借鉴的东西少。
- 置信: abstract级

### R4: Retrieval-Augmented Reasoning for Vision-Language Models in 4D Spatio-Temporal Space
- 链接: https://arxiv.org/abs/2512.15940
- 问题: VLM 缺乏持久、结构化的时空记忆，无法回溯过去事件或跨时间整合观测。
- 方法: Training-free 框架：持续构建 4D 知识库——把物体级语义描述锚定到度量空间和时间轴，形成可跨 agent 共享的持久世界模型；推理时把自然语言 query 分解为语义/空间/时间三种 key 检索相关观测，注入 VLM 推理。
- 结果: 未检索到具体数字。
- 出身: Karlsruhe Institute of Technology、Porsche AG、University of Michigan、Voxel51。
- 贴合度: 3/5 — training-free + 检索增强是明确加分项，思路是"给 VLM 外挂结构化 4D RAG"；扣分是 Porsche 背景暗示偏自动驾驶/具身场景，且无量化结果可核。
- 判断: 亮点是把 RAG 的 key 空间从纯语义扩展到"语义+度量空间+时间"三元检索；实际检索精度和延迟是待验证的关键。
- 置信: abstract级

## 第 6 组

### REALM: An MLLM-Agent Framework for Open World 3D Reasoning Segmentation and Editing on Gaussian Splatting
- 链接: https://arxiv.org/abs/2510.16410
- 问题: 现有 3D 分割方法难以理解含糊的推理式指令，而擅长推理的 2D VLM 又缺乏 3D 空间理解。
- 方法: 直接在 3D Gaussian Splatting 上做 MLLM-agent 式推理分割，无需 3D 专门 post-training；提出 Global-to-Local Spatial Grounding (GLSpaG) 策略应对视角选择敏感问题，逐视角推理（LMSeg）后层级聚合成 3D mask，并支持删除/替换/风格迁移等 3D 编辑。
- 结果: 未检索到（搜索摘要未给出具体数字）。
- 出身: 未核实（GitHub 见 ChangyueShi/REALM-Code）。
- 贴合度: 4/5 — 无需 3D 后训练的 agent 化方案，工程化、训练-free 倾向加分；但 3DGS pipeline 组件较多、依赖多视角渲染推理，运行开销存疑。
- 判断: 亮点是把 2D MLLM 推理能力"零 3D 训练"迁移到 3DGS 分割+编辑，GLSpaG 解决视角敏感是关键工程贡献。
- 置信: abstract级

### ReAG: Reasoning-Augmented Generation for Knowledge-based Visual Question Answering
- 链接: https://arxiv.org/abs/2511.22715
- 问题: 知识型 VQA 中现有 retrieval-augmented 方法检索精度低、passage 噪声大、推理能力有限。
- 方法: Reasoning-Augmented multimodal RAG：粗粒度+细粒度检索结合一个 critic model 过滤无关 passage；多阶段训练——SFT 冷启动 + RL 强化对检索内容的推理。
- 结果: 未检索到。
- 出身: 未核实。
- 贴合度: 3/5 — 多模态 RAG + critic 过滤思路对做知识增强系统有工程参考价值，但依赖多阶段 RL 训练，非训练-free，且属较拥挤的赛道。
- 判断: critic 过滤 + RL 推理的组合合理，但缺数字支撑，与近期一批 multimodal RAG 工作差异化待验证。
- 置信: abstract级

### ReasonX: MLLM-Guided Intrinsic Image Decomposition
- 链接: https://arxiv.org/abs/2512.04222
- 问题: 基于合成配对数据训练的 intrinsic decomposition（albedo/depth/normal/光照）模型在真实野外图像上泛化差。
- 方法: 把 MLLM 当作感知裁判（perceptual judge）给出相对内在属性比较，将这些比较作为 GRPO reward，在无标注真实图像上微调分解模型。
- 结果: IIW albedo 上 WHDR 降低 9–25%，ETH3D 深度精度最高提升 46%。
- 出身: Imperial College London + Adobe Research（作者 Alara Dirik 等）。
- 贴合度: 4/5 — "MLLM-as-judge → GRPO reward → 无标注自监督"是可复用的小而美范式，工程化程度高；应用领域（intrinsic decomposition）偏低层视觉略窄。
- 判断: 亮点是用相对比较而非绝对标注绕开真实数据缺标签问题，把 RLHF 式思路引入低层视觉，范式可迁移性强。
- 置信: abstract级

### Recurrent Reasoning with Vision-Language Models for Estimating Long-Horizon Embodied Task Progress
- 链接: https://arxiv.org/abs/2603.17312
- 问题: 具身 agent 长时程任务的进度估计：现有 VLM 方法只用视频理解不用复杂推理，且长视频轨迹处理算力上不可行。
- 方法: R²VLM——recurrent reasoning 框架，迭代处理局部视频片段，用一条不断演化的 Chain of Thought 维护全局上下文，CoT 显式记录任务分解、关键步骤及完成状态。
- 结果: 未检索到。
- 出身: 未核实（作者 Yuelin Zhang、Sijie Cheng 等）。
- 贴合度: 2/5 — 具身/机器人任务进度估计属 VLA 相关方向，用户暂不关注 VLA；recurrent CoT 处理长视频的思路本身有借鉴价值。
- 判断: "演化 CoT 作为循环状态"是流式长视频推理的干净设计，但应用场景锁定具身任务。
- 置信: abstract级

### S$^2$-MLLM: Boosting Spatial Reasoning Capability of MLLMs for 3D Visual Grounding with Structural Guidance
- 链接: https://arxiv.org/abs/2512.01223
- 问题: MLLM 做 3D Visual Grounding 时空间推理弱，且依赖低效的点云重建。
- 方法: 用 feed-forward 3D 重建的结构感知做空间引导（训练时注入 3D 结构理解，推理时隐式空间推理、免点云重建）；structure-enhanced 模块含 intra-view/inter-view attention 与多级位置编码。
- 结果: 未检索到具体数字。
- 出身: Shanghai Jiao Tong University + Nanyang Technological University。
- 贴合度: 3/5 — "训练时蒸结构、推理时免重建"是务实的效率设计加分；但需专门训练。
- 判断: 亮点在推理侧甩掉点云重建的效率收益；缺数字，提升幅度未知。
- 置信: abstract级

### SARL-STG: A Spatially Aware Reinforcement Learning Framework for Refining MLLMs in Spatio-Temporal Video Grounding
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Gao_SARL-STG_A_Spatially_Aware_Reinforcement_Learning_Framework_for_Refining_MLLMs_CVPR_2026_paper.pdf
- 问题: 用 RL 精调 MLLM 以提升 spatio-temporal video grounding（视频中时空同时定位目标）能力。
- 方法: 空间感知的 RL 框架；搜索结果提及借助 open-vocabulary detector、定制 query 与辅助模块适配 MLLM（细节有限，两次搜索仅命中 supplemental PDF）。
- 结果: 未检索到。
- 出身: 未核实（一作 Gao）。
- 贴合度: 2/5 — RL 精调 + 检测器 + 辅助模块，重训练重组件，工程简洁性差；STVG 赛道也偏 benchmark 驱动。
- 判断: 信息太少难下结论；从可见描述看是 RL-for-grounding 的常规组合拳，无明显小而美信号。
- 置信: abstract级（信息不完整，接近仅标题）

### Saliency-R1: Enforcing Interpretable and Faithful Vision-language Reasoning via Saliency-map Alignment Reward
- 链接: https://arxiv.org/abs/2604.04500
- 问题: VLM 推理偏重文本线索、忽视视觉证据，产生无依据/编造的回答，可信度存疑。
- 方法: 提出零额外计算开销的 saliency map 技术，追踪视觉信息在推理链中的流动；以 saliency map 与人工标注 bounding box 的重叠度作为 reward，用 GRPO 对齐"模型关注区域"与"关键区域"。
- 结果: 提升推理 faithfulness、可解释性与任务性能（未见具体数字）；已放出训练数据与 Saliency-R1-3B/7B 模型。
- 出身: 未核实（作者 Shizhan Gong、Qi Dou 等，疑似 CUHK 系但摘要未明示）。
- 贴合度: 4/5 — saliency 免额外开销 + 3B/7B 小模型 + 开源全套，小而美、工程化加分；依赖人工 bbox 标注做 reward 略扣分。
- 判断: 把可解释性工具直接变成 RL reward 是巧思，"对齐注意而非只对齐答案"值得关注。
- 置信: abstract级

### See Further, Think Deeper: Advancing VLM's Reasoning Ability with Low-level Visual Cues and Reflection
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_See_Further_Think_Deeper_Advancing_VLMs_Reasoning_Ability_with_Low-level_CVPR_2026_paper.pdf
- 问题: VLM 推理时忽视细粒度低层视觉特征，且缺乏视觉层面的自我反思。
- 方法: ForeSight——统一的多模态交错（interleaved）推理框架：一组低层视觉工具把细粒度视觉信息注入推理链（See Further），mask-based 视觉反馈机制让模型动态复查并更新答案（Think Deeper）。
- 结果: ForeSight-7B 显著超越同规模模型，部分指标超过 SOTA 闭源模型（未见具体数字）。
- 出身: Baidu Inc. + Zhejiang University + Harbin Institute of Technology。
- 贴合度: 3/5 — 7B 规模 + 视觉工具化的交错推理有工程参考价值；但需训练整套框架，"超闭源 SOTA"的口径待验证。
- 判断: 低层视觉工具 + mask 反馈的组合是当前 "think with images" 热潮的典型样本，亮点在把反思落到视觉证据上而非纯文本。
- 置信: abstract级

### See It, Say It, Sorted: An Iterative Training-Free Framework for Visually-Grounded Multimodal Reasoning in LVLMs
- 链接: https://arxiv.org/abs/2602.21497
- 问题: LVLM 长 CoT 中的视觉幻觉传播——某一步与视觉证据不符后，后续步骤会连锁导向错误答案。
- 方法: 训练-free、即插即用的迭代框架：测试时用视觉证据逐步监督推理，构建文本化 visual-evidence pool 引导生成；证据不足时由 visual decider 模块根据当前推理上下文从图像动态抽取补充证据。
- 结果: 未检索到具体数字；代码已开源。
- 出身: 未核实（一作 Yongchang Zhang）。
- 贴合度: 5/5 — 训练-free + plug-and-play + 绕开 RL 训练 + 开源，完全命中用户偏好；主要成本在推理时迭代。
- 判断: 亮点是把"每一步 token 都要有视觉证据背书"做成纯测试时机制；局限是迭代式 decoding 的延迟开销未知。
- 置信: abstract级

### Seeing Clearly, Reasoning Confidently: Plug-and-Play Remedies for Vision Language Model Blindness
- 链接: https://arxiv.org/abs/2602.19615
- 问题: VLM 对预训练数据中稀缺的罕见物体（rare objects）做以物体为中心的推理时表现差（"blindness"）。
- 方法: 免 VLM 微调的即插即用模块：借助视觉基础模型先验与同义词增强文本描述学习罕见物体的多模态 class embedding，再用轻量 attention 增强模块精炼视觉 token 并丰富文本 prompt。
- 结果: 未检索到具体数字（摘要称"substantially improves"）。
- 出身: 未核实（作者 Xin Hu、Haomiao Ni、Jihun Hamm、Zhengming Ding 等）。
- 贴合度: 4/5 — plug-and-play、免主模型微调、模块轻量，工程化加分；仍需训练 class embedding 与增强模块，且针对"罕见物体"场景略窄。
- 判断: 定位精准的小补丁式工作：不动 VLM 本体、只在输入两侧（视觉 token + prompt）做增强，落地成本低。
- 置信: abstract级

## 第 7 组

### SenseSearch: Empowering Vision-Language Models with High-Resolution Agentic Search-Reasoning via Reinforcement Learning
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Chng_SenseSearch_Empowering_Vision-Language_Models_with_High-Resolution_Agentic_Search-Reasoning_via_Reinforcement_CVPR_2026_paper.pdf
- 问题: VLM 在高分辨率图像上做知识密集型问答时缺乏主动检索与细粒度感知能力。
- 方法: 用 RL 训练模型在 multi-turn reasoning 中自适应调用 image search、text search 和 image crop 三种工具；同系工作 SenseNova-MARS 提出 BN-GSPO（Batch-Normalized Group Sequence Policy Optimization）稳定训练。
- 结果: 在 <7B 开源 agentic 模型中 SOTA，平均超 MMSearch-R1 4.94 分、超 GPT-4o-mini 11.78 分，与 Gemini-2.5-Flash / GPT-4o 持平。
- 出身: 未核实（关联工作 SenseNova-MARS 命名暗示 SenseTime，仅推断）
- 贴合度: 3/5 — 7B 小模型 + 工具调用的 agentic 路线有工程参考价值，但 RL 训练管线偏重资源。
- 判断: 亮点是小模型靠工具增强打平闭源大模型；局限是依赖外部搜索服务，落地场景受限。
- 置信: abstract级

### SpaceMind: Camera-Guided Modality Fusion for Spatial Reasoning in Vision-Language Models
- 链接: https://arxiv.org/abs/2511.23075
- 问题: VLM 在纯 RGB 输入下的 3D 空间推理（距离估计、尺寸比较、跨视角一致性）能力弱。
- 方法: 双编码器架构（VGGT 做空间理解 + InternViT 做 2D 视觉），核心是把 camera representation 当作主动引导模态而非被动元数据，在 LLM 前加轻量 Camera-Guided Modality Fusion 模块替代浅层融合。
- 结果: 在 VSI-Bench、SQA3D、SPBench 上 SOTA，VSI-Bench 和 SPBench 上大幅超过开源与闭源系统（具体数字未检索到）。
- 出身: 未核实（GitHub 账号 RealMikeDuke）
- 贴合度: 3/5 — 轻量融合模块、推理期无需 3D 传感器是加分项，但仍需完整训练管线。
- 判断: 亮点是"相机表征作为引导模态"的想法干净且推理时零额外传感器；与 VGGT 的耦合可能限制泛化。
- 置信: abstract级

### SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models
- 链接: https://arxiv.org/abs/2602.20901
- 问题: 缺少评测"空间关系 + 多步任务逻辑依赖"组合能力的基准。
- 方法: 构建 9,605 个 QA 对，来自 241 个真实室内场景；对 41 个主流 VLM 做系统评测。
- 结果: 最先进模型在空间逻辑推理上依然表现不佳（具体分数未检索到）。
- 出身: 未核实（一作 Yuechen Xie）
- 贴合度: 2/5 — 纯 benchmark，无方法贡献，对工程实践的直接价值有限。
- 判断: 规模和模型覆盖面（41 个 VLM）扎实，但"VLM 空间推理差"已是共识，增量结论有限。
- 置信: abstract级

### SpatialStack: Layered Geometry-Language Fusion for 3D VLM Spatial Reasoning
- 链接: https://arxiv.org/abs/2603.27437
- 问题: 现有做法把多视角几何 transformer 接入 VLM 时只融合深层特征，丢弃层次化几何信号，成为空间理解瓶颈。
- 方法: 分层融合框架，将 geometry encoder 的多层级特征与 language backbone 逐层堆叠对齐，兼顾局部几何精度与全局语义。
- 结果: VLM-SpatialStack 在多个 3D spatial reasoning benchmark 上 SOTA；具体数字未检索到。
- 出身: 未核实
- 贴合度: 3/5 — 通用融合框架可迁移性好，但属于"多加一层融合"式改进，训练成本不低。
- 判断: 动机（深层 vs 多层融合）清晰，与 SpaceMind 同赛道，值得横向对比二者的融合位置选择。
- 置信: abstract级

### StaR-KVQA: Structured Reasoning Traces for Implicit-Knowledge Visual Question Answering
- 链接: https://arxiv.org/abs/2510.06638
- 问题: 无外部检索、仅靠 MLLM 内部知识的 KVQA（IK-KVQA）中，推理过程隐式、解释弱、SFT 后泛化脆弱。
- 方法: 引入双路结构化推理轨迹——文本+视觉上的 symbolic relation paths 加 path-grounded 自然语言解释，作为比 answer-only 监督更强的归纳偏置。
- 结果: 未检索到具体数字。
- 出身: 未核实
- 贴合度: 3/5 — 无需外部检索是加分项，结构化轨迹监督思路小而美，但需构造轨迹数据再微调。
- 判断: 亮点是把 self-taught reasoning（StaR 范式）搬到 KVQA 并强调符号路径可解释性；效果量级未知需读原文。
- 置信: abstract级

### TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf
- 问题: VLA 模型缺乏时序感知的推理与记忆能力（仅标题推断）。
- 方法: 时序感知 CoT 推理 + 记忆机制用于 VLA（仅标题推断，摘要未检索到）。
- 结果: 未检索到。
- 出身: 未核实（作者 Xiang Li、Ya-Li Li、Yuan Wang、Shengjin Wang）
- 贴合度: 2/5 — 用户暂不关注VLA。
- 判断: 两次搜索仅获得 CVPR 2026 收录信息（pp. 10943-10953），无摘要级内容，无法评估实质贡献。
- 置信: 仅标题

### TTRV: Test-Time Reinforcement Learning for Vision Language Models
- 链接: https://arxiv.org/abs/2510.06783
- 问题: VLM 部署后无法在无标注数据的情况下适配测试分布。
- 方法: 首个 VLM 测试时 RL 框架：基于 GRPO，对每个测试样本多次推理，用输出频率构造奖励，同时以输出经验分布的低熵作为额外奖励控制多样性，全程无需标注。
- 结果: 物体识别最高提升 52.4%、VQA 最高 29.8%；16 个数据集上平均提升 24.6% / 10.0%；InternVL 8B 加 TTRV 后在 8 个识别 benchmark 上平均超 GPT-4o 2.3%。
- 出身: 未核实（作者含 Singh、Marjit、Kuehne、Feris、Glass、Mirza 等）
- 贴合度: 4/5 — 无标注、无需训练数据、即插即用于现成模型，非常工程化；扣分点是每样本多次推理带来推理时开销。
- 判断: 亮点是把 TTRL 思路干净地迁移到视觉域且数字亮眼；需警惕频率奖励在分布外样本上的自我强化偏差。
- 置信: abstract级

### TableMix: Enhancing Multimodal Table Reasoning in MLLMs from a Data-Centric Perspective
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Liu_TableMix_Enhancing_Multimodal_Table_Reasoning_in_MLLMs_from_a_Data-Centric_CVPR_2026_paper.pdf
- 问题: MLLM 的表格图像推理能力不足，从数据侧（配比/混合/合成）入手改进（仅标题推断）。
- 方法: 未检索到（推测为数据混合或数据构造策略，仅标题推断）。
- 结果: 未检索到。
- 出身: 未核实
- 贴合度: 3/5 — data-centric 路线通常不改架构、可复用性强（仅标题推断），但无摘要信息，暂给中评。
- 判断: 两次搜索均未命中该论文，可能未挂 arXiv，需读 CVPR 原文确认。
- 置信: 仅标题

### TempR1: Improving Temporal Understanding of MLLMs via Temporal-Aware Multi-Task Reinforcement Learning
- 链接: https://arxiv.org/abs/2512.03963
- 问题: MLLM 对长视频的时序理解（时序定位、动作检测、时敏问答）能力弱。
- 方法: 基于 GRPO 的多任务 RL：构建覆盖 TG、DTG、TAL、VHD、GVQA 五类任务、60K+ 样本的语料；按预测区间与 GT 实例的三种对应类型设计定制化 localization reward。
- 结果: 多个 benchmark 上 SOTA（具体分数未检索到）。
- 出身: 未核实
- 贴合度: 3/5 — 奖励设计有可借鉴的工程细节，但多任务 RL + 60K 语料属于重训练路线。
- 判断: 亮点是按区间对应关系分类设计奖励，比通用 IoU 奖励更细；属于 R1 风格视频时序方向的扎实增量工作。
- 置信: abstract级

### Think 360deg: Beyond Depth: Evaluating the Width-centric Reasoning Capability of MLLMs
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_Think_360deg_Beyond_Depth_Evaluating_the_Width-centric_Reasoning_Capability_of_CVPR_2026_paper.pdf
- 问题: 现有评测只关注长链条的"推理深度"，缺少对"推理宽度"（并行搜索、多约束剪枝、试错回溯）的评估。
- 方法: 构建 Think360° 多模态 benchmark：1200+ 案例，考察 trial-and-error、branch-and-bound、divide-and-conquer、hypothesize-and-test 等宽度型认知技能；评测 12 个模型系列、30+ MLLM。
- 结果: 当前模型在常规 VQA 上强，但难以把深度链式思考与宽度探索式搜索结合完成 insight-based reasoning（具体分数未检索到）。
- 出身: 未核实
- 贴合度: 2/5 — 纯 benchmark 无方法贡献；但"宽度 vs 深度"的评测视角对理解 test-time scaling 的短板有概念价值。
- 判断: 亮点是提出正交于 depth 的评测维度，问题定义新颖；1200 案例规模偏小，结论稳健性存疑。
- 置信: abstract级

## 第 8 组

### Think Visually, Reason Textually: Vision-Language Synergy in Abstract Reasoning
- 链接: https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_Think_Visually_Reason_Textually_Vision-Language_Synergy_in_Abstract_Reasoning_CVPR_2026_paper.pdf （arXiv: https://arxiv.org/abs/2511.15703）
- 问题: 前沿模型（GPT-5、Grok 4）仍无法从少量样例中归纳结构化变换规则（ARC-AGI 抽象推理），现有方法把它当纯文本任务，忽略人类依赖的视觉抽象。
- 方法: 两个协同策略：Vision-Language Synergy Reasoning (VLSR) 将 ARC-AGI 分解为模态对齐的子任务（视觉管全局模式抽象与验证，语言管细节推理）；Modality-Switch Self-Correction (MSSC) 用视觉做自我纠错。
- 结果: 未检索到具体数字（摘要仅给出方法框架与假设）。
- 出身: 未核实（一作 Beichen Zhang 等 7 人）。
- 贴合度: 4/5 — 提示/流程层面的模态分工策略，无需训练、可直接套用到现有前沿模型，小而美；扣一分在于面向 ARC 这种偏学术的 benchmark。
- 判断: "视觉负责抽象、语言负责执行"的分工假设有洞察力，且 MSSC 的跨模态自纠错思路可迁移到其他 VLM 任务；但缺具体数字，实际提升幅度待读原文确认。
- 置信: abstract级

### Think-as-You-See: Streaming Chain-of-Thought Reasoning for Large Vision-Language Models
- 链接: https://arxiv.org/abs/2603.02872
- 问题: 现有视频推理假设"看完全片再推理"的 batch 模式，与真实视频流的逐帧到达不符，导致高延迟和时间漂移。
- 方法: TaYS 统一框架实现边看边推理：时间对齐的 reasoning units、streaming attention mask 强制时间因果、解耦的位置编码解决跨模态索引冲突、并行 dual KV-cache 把视觉编码与文本推理解耦，实现帧摄入与 token 解码并发。
- 结果: 在 VideoEspresso 上基于 Qwen2.5-VL：推理准确率 +2.9%，TTFT 从 10.6s 降到接近零，推理事件偏差降低 55%。
- 出身: 未核实。
- 贴合度: 4/5 — 系统工程味很足（KV-cache 设计、注意力掩码、并行推理），TTFT 近零的收益对实时应用直接可用；需要 stream-constrained 训练，不是纯 training-free，略扣分。
- 判断: 亮点是把 streaming LLM 的系统技巧完整移植到视频 CoT，延迟收益数量级明显；准确率提升本身较小（2.9%），价值主要在工程侧。
- 置信: abstract级

### Thinking Diffusion: Penalize and Guide Visual-Grounded Reasoning in Diffusion Multimodal Language Models
- 链接: https://arxiv.org/abs/2604.05497
- 问题: 扩散多模态 LLM（dMLLM）在很早的 timestep 就生成最终答案 token（先答后想），且早期步骤几乎不依赖视觉输入，导致推理质量差。
- 方法: 两个 training-free 机制：Position & Step Penalty (PSP) 在早期 timestep 惩罚靠后位置的 token，延迟过早出答案、强制渐进式推理；Visual Reasoning Guidance (VRG) 借鉴 classifier-free guidance 放大视觉 grounding 信号。
- 结果: training-free，准确率最高 +7.5%，且比用 4 倍扩散步数的模型推理快 3 倍以上。
- 出身: Hanyang University（Keuntae Kim, Mingyu Kang, Yong Suk Choi）。
- 贴合度: 5/5 — 完全 training-free、推理时即插即用、还顺带提速 3 倍，典型的"小而美"；对 dMLLM 行为诊断（早期答案坍缩）本身也有认知价值。
- 判断: "dMLLM 先出答案再补推理"的观察是个漂亮的失败模式诊断，两个修复机制都轻量；局限是仅适用于扩散架构 MLLM，生态还小。
- 置信: abstract级

### Thinking in Dynamics: How Multimodal Large Language Models Perceive, Track, and Reason Dynamics in Physical 4D World
- 链接: https://arxiv.org/abs/2603.12746
- 问题: 检验当前 MLLM 能否感知、跟踪并推理动态演化场景中的时空动力学。
- 方法: 构建大规模 benchmark Dyn-Bench：来自真实+合成视频数据集，含 1k 视频、7k VQA 对、3k 动态物体 grounding 对。
- 结果: 关键发现：现有模型无法同时在时空推理和动态理解两方面保持强性能。代码在 GitHub（Dynamics-X/Thinking-in-Dynamics）。
- 出身: 未核实（一作 Yuzhi Huang）。
- 贴合度: 2/5 — 纯 benchmark 论文，无新方法；对做 4D/物理理解方向的人有参考价值，但对工程落地贡献有限。
- 判断: "时空推理与动态感知不可兼得"是有信息量的负结果，但 benchmark 型工作生命周期短、易被下一代模型刷掉。
- 置信: abstract级

### Towards Open Environments and Instructions: General Vision-Language Navigation via Fast-Slow Interactive Reasoning
- 链接: https://arxiv.org/abs/2601.09111
- 问题: 面向 General Scene Adaptation VLN（GSA-VLN）任务，在多样环境和不一致指令下学习泛化的导航能力。
- 方法: Slow4Fast 交互框架：fast reasoning 由策略网络实时输出动作并存储记忆；slow reasoning 处理记忆、提炼泛化经验并反哺强化策略网络。
- 结果: 在 GSA-R2R 数据集上"展示了优越性"，未检索到具体数字。
- 出身: Tianjin University、Hefei University of Technology（Yang Li, Aming Wu, Zihao Zhang, Yahong Han）。
- 贴合度: 2/5 — 导航类，用户暂不关注VLA；fast-slow 双系统设计本身在具身方向已较常见。
- 判断: 记忆驱动的 slow 回路反哺 fast 策略的闭环有一定新意，但属 VLN 赛道内的增量工作。
- 置信: abstract级

### Towards Reasoning-Preserving Unlearning in Multimodal Large Language Models
- 链接: https://arxiv.org/abs/2512.17911
- 问题: 对推理型 MLLM 做 unlearning 时，即使最终答案被遗忘，中间 CoT 步骤仍会泄露敏感信息；而干预过猛又会损伤通用推理能力。
- 方法: 提出首个 RMLLM unlearning 基准 RMLLMU-Bench（新增推理泄露/推理保持指标）；并提出 R-MUSE——training-free 的推理时干预框架，通过 subspace guidance 与自适应 steering 操纵内部表征，同时遗忘答案与推理轨迹并保留通用推理。
- 结果: 系统评测显示现有 unlearning 方法要么推理过程泄露严重、要么推理能力大幅退化；R-MUSE 具体数字未检索到。
- 出身: 未核实。
- 贴合度: 3/5 — R-MUSE 是 training-free 的表征 steering，工程上轻量加分；但 unlearning 属合规/安全细分赛道，且一半篇幅是 benchmark。
- 判断: "CoT 泄露被遗忘内容"是个此前被忽视的真实漏洞，问题定义比方法更有价值。
- 置信: abstract级

### VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation
- 链接: https://arxiv.org/abs/2510.23497
- 问题: 高质量图文推理数据稀缺，而纯文本推理数据丰富——如何把文本 LLM 的推理能力迁移给 VLM。
- 方法: VOLD 将 GRPO 强化学习与 on-policy distillation 结合，让学生 VLM 的推理轨迹受文本 teacher 引导；关键发现是必须先做 cold-start 对齐，否则师生分布差异过大时 on-policy 蒸馏无法提供有效指导。
- 结果: 在 MMMU-Pro、MathVision、MathVista、LogicVista 上显著超过 baseline 并超过 SOTA（具体数字未检索到）。
- 出身: 未核实（作者 Walid Bousselham, Hilde Kuehne, Cordelia Schmid——Schmid/Kuehne 组）。
- 贴合度: 3/5 — "文本推理数据白嫖给 VLM"的思路实用，cold-start 对齐的教训对做后训练的人有直接参考价值；但 GRPO+蒸馏训练管线资源不轻。
- 判断: 亮点是明确指出 on-policy 蒸馏的分布对齐前提条件，这是可复用的方法论；作者阵容也提示工作质量较可靠。
- 置信: abstract级

### Vision-Language Attribute Disentanglement and Reinforcement for Lifelong Person Re-Identification
- 链接: https://arxiv.org/abs/2603.19678
- 问题: 终身行人重识别（LReID）中，现有 VLM 方法只做全局学习，未利用细粒度属性知识，限制了新知识获取与抗遗忘能力。
- 方法: VLADR：Multi-grain Text Attribute Disentanglement 挖掘图像的全局与局部文本属性；Interdomain Cross-modal Attribute Reinforcement 通过跨模态属性对齐引导视觉属性抽取，并用跨域属性对齐实现细粒度知识迁移。
- 结果: 抗遗忘指标超 SOTA 1.9%–2.2%，泛化指标超 2.1%–2.5%。
- 出身: 未核实（GitHub 仓库为 zhoujiahuan1991/CVPR2026-VLADR）。
- 贴合度: 2/5 — 行人 ReID 垂直赛道的 benchmark 刷分型工作，提升幅度约 2 个点，对用户方向参考价值有限。
- 判断: "共享人体属性作为跨域锚点"的思路合理，但属细分任务内的常规增量。
- 置信: abstract级

### Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training
- 链接: https://arxiv.org/abs/2602.10815
- 问题: 解释为什么 RL 后训练的 VLM 在 OOD 上一致优于 SFT。
- 方法: 数据视角的归因：RL 的泛化优势来自一种隐式数据过滤机制——天然偏向中等难度样本；并发现在难样本上训练会显著损害 OOD 性能。据此提出 Difficulty-Curated SFT (DC-SFT)：按样本难度显式过滤训练集的简单方法。
- 结果: DC-SFT 不仅大幅超过标准 SFT 的 OOD 泛化，还反超 RL 训练，同时更稳定、计算更省（具体数字未检索到）。
- 出身: 未核实。
- 贴合度: 5/5 — 把"RL vs SFT"这个热门争论还原为数据难度筛选问题，结论可直接落地（一个过滤步骤替代昂贵的 RL 管线），典型的小而美+省资源。
- 判断: 如果"难度过滤后的 SFT 能打平 RL"的结论稳健，对后训练实践是高性价比信号；风险在于结论可能依赖特定难度度量与任务分布，需读原文验证。
- 置信: abstract级

### dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models
- 链接: https://arxiv.org/abs/2512.19433
- 问题: 对统一图像生成+理解的扩散多模态 LLM（dMLLM）做 test-time scaling 时，传统在"轨迹探索 × 迭代精化"两个维度上线性搜索的成本高达 O(NT)，且依赖外部 verifier 做 best-of-N。
- 方法: 双轴 scaling 框架（trajectory exploration scaling 提升假设多样性 + iterative refinement scaling 稳定生成），并引入自验证机制：利用模型自身的图像理解能力内部评估生成结果，去掉外部 verifier。
- 结果: 加 TTS 后生成图像质量与 prompt 对齐度更高；具体数字未检索到。代码基于 Lumina-DiMOO。
- 出身: Nanjing University、Shanghai Innovation Institute、Shanghai AI Lab、Shanghai Jiao Tong University、Peking University、NUS。
- 贴合度: 4/5 — 推理时方法、无需训练、用模型自身理解能力做 verifier 省掉外部模型，工程实用；扣分在于 TTS 本身仍是花算力换质量的路线。
- 判断: "统一模型自己当自己的 verifier"是 dMLLM 架构红利的聪明利用，闭环设计优雅；效果目前只有定性描述，量化收益待确认。
- 置信: abstract级
