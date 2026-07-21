---
topic: "VLM / 多模态大模型"
slug: "vlm"
keywords: [vision-language model, multimodal LLM, VLM efficiency, visual reasoning, VLM RAG, training-free]
created: "2026-07-06"
last_tracked: "2026-07-20"
---

# 主题追踪：VLM / 多模态大模型

## 这个方向在关注什么
VLM/MLLM 正在成为视觉研究的"底座"。CVPR 2026 全量分析显示其占比 6.9%→10.0%，
且与推理/RL（80 篇共现）、效率（35）、医学（35）深度耦合。当前最热的交叉是
**VLM × 推理/RL**（全场增速第一的方向，1.8%→8.7%）。

## 追踪记录

### 2026-07-20 · 两周增量（WebSearch，abstract 级未深读）
> watch 检查：ZwZ 后续暂无新节点；开源模型无新版本发布。以下按 watch 方法线归位。

**⭐ 命中 watch 方法线**
- **Attend to Evidence** — 证据锚定的空间注意力监督做 multimodal RLVR ·（**推理伤感知修复线** + Saliency-R1 同思路：对齐注意而非只对齐答案）· [arXiv 2605.30912](https://arxiv.org/pdf/2605.30912)
- **Attend, Transform, or Silence** — 算子级视觉跳过（逐 operator 决定视觉 token 是否参与计算）做高效 MLLM 推理 ·（效率线，小而美）· [arXiv 2606.31903](https://arxiv.org/pdf/2606.31903)
- **ToolGate** — 工具增强 VLM agent 的 token 高效"调用前门控" ·（agent×效率交叉，路由思想的微缩版）· [arXiv 2606.03054](https://arxiv.org/pdf/2606.03054)

**潜视觉推理线（Monet 后续演化）**
- **DeepLatent** — 并行潜视觉推理做 "think with images" · [arXiv 2606.00562](https://arxiv.org/pdf/2606.00562)
- **Chain-of-Visual-Thought (CoVT)** — 连续视觉 token 做思考链 · [arXiv 2511.19418](https://arxiv.org/pdf/2511.19418)

**自进化 / 验证线**
- **RISE** — 自进化 VLM 的"可靠改进"（防自进化退化）· [arXiv 2605.20914](https://arxiv.org/pdf/2605.20914)
- **Reflect to Inform** — 信息增益驱动的验证提升多模态推理 · [arXiv 2603.26348](https://arxiv.org/pdf/2603.26348)

**其它**
- **ConFoThinking** — 聚焦注意力驱动的 VQA 思考 · [arXiv 2603.00165](https://arxiv.org/pdf/2603.00165)
- **Visual-OPSD**（西交）— 跨模态 on-policy 自蒸馏做统一多模态推理 · 题名可搜（链接待核）


### 2026-07-08 · 近期新论文（WebSearch，abstract 级未深读）
- **One Token per Multimodal Evidence** — 每条多模态证据压成 1 个 latent memory token，资源受限 QA 的极致压缩 · [arXiv 2606.10572](https://arxiv.org/abs/2606.10572) · ⭐小而美
- **RedVTP** — training-free 加速扩散 VLM：masked token 引导视觉 token 剪枝（接库里 Thinking Diffusion / dMLLM-TTS 的 dMLLM 线） · [arXiv 2511.12428](https://arxiv.org/abs/2511.12428)
- **From Similarity to Structure** — training-free 上下文压缩，混合图先验（LLM 侧但方法可借鉴） · [arXiv 2604.23277](https://arxiv.org/abs/2604.23277)
- 关联：agent 侧同期发现见 topics/agents.md（VisCritic / R-WoM 等 8 篇）

**第二轮补扫（同日，换角度：世界模型/长视频/统一模型/小模型）**
- **HPP: Hierarchical Programmatic Probing for Long Video Understanding** — 解耦感知与推理的程序化探测做长视频理解 · [arXiv 2606.21734](https://arxiv.org/abs/2606.21734) · ⭐疑似 training-free pipeline，贴口味
- **World2VLM** — 把世界模型的"想象"蒸馏进 VLM 做动态空间推理，世界模型×VLM 交叉 · [arXiv 2604.26934](https://arxiv.org/abs/2604.26934) · ⭐方向新颖
- **CLGRPO** — 小 VLM 的推理能力增强（RL） · [arXiv 2506.18048](https://arxiv.org/abs/2506.18048) · ⭐小模型贴口味
- **A Stitch in Time Saves Nine** — 用小 VLM 精准引导大 VLM 加速 · [arXiv 2412.03324](https://arxiv.org/abs/2412.03324) · 小而美加速（2024-12，补录）
- **Self-Evolving Spatial Reasoning via Geometric Logic Consistency** — 几何逻辑一致性做自监督空间推理进化 · [arXiv 2605.18162](https://arxiv.org/abs/2605.18162)
- **PnP-U3D** — plug-and-play 3D 框架桥接自回归与扩散的统一理解生成 · [arXiv 2602.03533](https://arxiv.org/abs/2602.03533)
- **SpaceEra++** — 视频 3D 空间推理全栈系统（数据/模型/训练/推理） · [arXiv 2607.01784](https://arxiv.org/abs/2607.01784) · 7月刚挂出
- **Lance** — 多任务协同的统一多模态建模 · [arXiv 2605.18678](https://arxiv.org/abs/2605.18678)
- **UNIVID** — 统一视频审核 VLM（内容安全垂直） · [arXiv 2606.05748](https://arxiv.org/abs/2606.05748)
- **Do VLMs Have a Moral Backbone?** — VLM 道德判断脆弱性分析（诊断型） · [arXiv 2601.17082](https://arxiv.org/abs/2601.17082)

### 2026-07-06 · CVPR 2026 全量：VLM × 推理/RL 交叉（80 篇完整清单）

> 来源：52CV 接收清单标题级筛选（同时命中 VLM 桶与推理/RL 桶），链接为 arXiv 或 CVF 原文。
> 按子方向分组；组内按标题字母序。趋势总览见 `digests/2026-07-06-cvpr2026-trend-analysis.md`。

#### ⚡ 训练-free / 测试时（最贴口味） · 7 篇
- [ANTS: Adaptive Negative Textual Space Shaping for OOD Detection via Test-Time MLLM Understanding and Reasoning](https://arxiv.org/abs/2509.03951)
- [DeepScan: A Training-Free Framework for Visually Grounded Reasoning in Large Vision-Language Models](https://arxiv.org/abs/2603.03857)
- [Generate, Analyze, and Refine: Training-Free Sound Source Localization via MLLM Meta-Reasoning](https://arxiv.org/abs/2604.06824)
- [See It, Say It, Sorted: An Iterative Training-Free Framework for Visually-Grounded Multimodal Reasoning in LVLMs](https://arxiv.org/abs/2602.21497)
- [Seeing Clearly, Reasoning Confidently: Plug-and-Play Remedies for Vision Language Model Blindness](https://arxiv.org/abs/2602.19615)
- [TTRV: Test-Time Reinforcement Learning for Vision Language Models](https://arxiv.org/abs/2510.06783)
- [dMLLM-TTS: Self-Verified and Efficient Test-Time Scaling for Diffusion Multi-Modal Large Language Models](https://arxiv.org/abs/2512.19433)

#### 🤖 Agentic / 工具调用 · 7 篇
- [CodeDance: A Dynamic Tool-integrated MLLM for Executable Visual Reasoning](https://arxiv.org/abs/2512.17312)
- [IBISAgent: Reinforcing Pixel-Level Visual Reasoning in MLLMs for Universal Biomedical Object Referring and Segmentation](https://arxiv.org/abs/2601.03054)
- [Learning to Focus and Precise Cropping:A Reinforcement Learning Framework with Information Gaps and Grounding Loss for MLLMs](https://arxiv.org/abs/2603.27494)
- [MindPower: Enabling Theory-of-Mind Reasoning in VLM-based Embodied Agents](https://arxiv.org/abs/2511.23055)
- [ORCA: Orchestrated Reasoning with Collaborative Agents for Document Visual Question Answering](https://arxiv.org/abs/2603.02438)
- [REALM: An MLLM-Agent Framework for Open World 3D Reasoning Segmentation and Editing on Gaussian Splatting](https://arxiv.org/abs/2510.16410)
- [SenseSearch: Empowering Vision-Language Models with High-Resolution Agentic Search-Reasoning via Reinforcement Learning](https://openaccess.thecvf.com/content/CVPR2026/papers/Chng_SenseSearch_Empowering_Vision-Language_Models_with_High-Resolution_Agentic_Search-Reasoning_via_Reinforcement_CVPR_2026_paper.pdf)

#### 🔬 RL 方法学 / 机理分析 · 15 篇
- [Adversarial Style Optimization: Enhancing VLM Jailbreaks by GRPO-based Stylistic Triggers Optimization](https://openaccess.thecvf.com/content/CVPR2026/papers/Luo_Adversarial_Style_Optimization_Enhancing_VLM_Jailbreaks_by_GRPO-based_Stylistic_Triggers_CVPR_2026_paper.pdf)
- [EMO-R3: Reflective Reinforcement Learning for Emotional Reasoning in Multimodal Large Language Models](https://arxiv.org/abs/2602.23802)
- [HoneyBee: Data Recipes for Vision-Language Reasoners](https://arxiv.org/abs/2510.12225)
- [Incentivizing Versatile Video Reasoning in MLLMs via Data-Efficient Reinforcement Learning](https://openaccess.thecvf.com/content/CVPR2026/papers/Wang_Incentivizing_Versatile_Video_Reasoning_in_MLLMs_via_Data-Efficient_Reinforcement_Learning_CVPR_2026_paper.pdf)
- [MoE-GRPO: Optimizing Mixture-of-Experts via Reinforcement Learning in Vision-Language Models](https://arxiv.org/abs/2603.24984)
- [PDCR: Perception-Decomposed Confidence Reward for Vision-Language Reasoning](https://arxiv.org/abs/2605.13467)
- [PROMPTMINER: Black-Box Prompt Stealing against Text-to-Image Generative Models via Reinforcement Learning and VLM-Guided Optimization](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_PROMPTMINER_Black-Box_Prompt_Stealing_against_Text-to-Image_Generative_Models_via_Reinforcement_CVPR_2026_paper.pdf)
- [SARL-STG: A Spatially Aware Reinforcement Learning Framework for Refining MLLMs in Spatio-Temporal Video Grounding](https://openaccess.thecvf.com/content/CVPR2026/papers/Gao_SARL-STG_A_Spatially_Aware_Reinforcement_Learning_Framework_for_Refining_MLLMs_CVPR_2026_paper.pdf)
- [Saliency-R1: Enforcing Interpretable and Faithful Vision-language Reasoning via Saliency-map Alignment Reward](https://arxiv.org/abs/2604.04500)
- [TableMix: Enhancing Multimodal Table Reasoning in MLLMs from a Data-Centric Perspective](https://openaccess.thecvf.com/content/CVPR2026/papers/Liu_TableMix_Enhancing_Multimodal_Table_Reasoning_in_MLLMs_from_a_Data-Centric_CVPR_2026_paper.pdf)
- [TempR1: Improving Temporal Understanding of MLLMs via Temporal-Aware Multi-Task Reinforcement Learning](https://arxiv.org/abs/2512.03963)
- [Towards Reasoning-Preserving Unlearning in Multimodal Large Language Models](https://arxiv.org/abs/2512.17911)
- [VOLD: Reasoning Transfer from LLMs to Vision-Language Models via On-Policy Distillation](https://arxiv.org/abs/2510.23497)
- [Vision-Language Attribute Disentanglement and Reinforcement for Lifelong Person Re-Identification](https://arxiv.org/abs/2603.19678)
- [Why Does RL Generalize Better Than SFT? A Data-Centric Perspective on VLM Post-Training](https://arxiv.org/abs/2602.10815)

#### 📐 空间 / 3D / 4D 推理 · 15 篇
- [Beyond 3D VQAs: Injecting 3D Spatial Priors into Vision-Language Models for Enhanced Geometric Reasoning](https://openaccess.thecvf.com/content/CVPR2026/papers/Yeh_Beyond_3D_VQAs_Injecting_3D_Spatial_Priors_into_Vision-Language_Models_CVPR_2026_paper.pdf)
- [EgoMind: Activating Spatial Cognition through Linguistic Reasoning in MLLMs](https://arxiv.org/abs/2604.03318)
- [EgoProx: Evaluating MLLMs on Egocentric 3D Proximity Reasoning Across a Cognitive Hierarchy](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_EgoProx_Evaluating_MLLMs_on_Egocentric_3D_Proximity_Reasoning_Across_a_CVPR_2026_paper.pdf)
- [Eliciting Complex Spatial Reasoning in MLLMs through Wide-Baseline Matching](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhong_Eliciting_Complex_Spatial_Reasoning_in_MLLMs_through_Wide-Baseline_Matching_CVPR_2026_paper.pdf)
- [From Indoor to Open World: Revealing the Spatial Reasoning Gap in MLLMs](https://arxiv.org/abs/2512.19683)
- [G$^2$VLM: Geometry Grounded Vision Language Model with Unified 3D Reconstruction and Spatial Reasoning](https://arxiv.org/abs/2511.21688)
- [HandVQA: Diagnosing and Improving Fine-Grained Spatial Reasoning about Hands in Vision-Language Models](https://arxiv.org/abs/2603.26362)
- [Keep it SymPL: Symbolic Projective Layout for Allocentric Spatial Reasoning in Vision-Language Models](https://arxiv.org/abs/2602.19117)
- [Learning to Reason in 4D: Dynamic Spatial Understanding for Vision Language Models](https://arxiv.org/abs/2512.20557)
- [R4: Retrieval-Augmented Reasoning for Vision-Language Models in 4D Spatio-Temporal Space](https://arxiv.org/abs/2512.15940)
- [S$^2$-MLLM: Boosting Spatial Reasoning Capability of MLLMs for 3D Visual Grounding with Structural Guidance](https://arxiv.org/abs/2512.01223)
- [SpaceMind: Camera-Guided Modality Fusion for Spatial Reasoning in Vision-Language Models](https://arxiv.org/abs/2511.23075)
- [SpatiaLQA: A Benchmark for Evaluating Spatial Logical Reasoning in Vision-Language Models](https://arxiv.org/abs/2602.20901)
- [SpatialStack: Layered Geometry-Language Fusion for 3D VLM Spatial Reasoning](https://arxiv.org/abs/2603.27437)
- [Thinking in Dynamics: How Multimodal Large Language Models Perceive, Track, and Reason Dynamics in Physical 4D World](https://arxiv.org/abs/2603.12746)

#### 🎬 视频 / 时序推理 · 5 篇
- [AXG-Reasoner: Error Detection and Explanation in Long Task Videos with Vision-Language Models](https://openaccess.thecvf.com/content/CVPR2026/papers/Lee_AXG-Reasoner_Error_Detection_and_Explanation_in_Long_Task_Videos_with_CVPR_2026_paper.pdf)
- [Beyond Perceptual Shortcuts: Causal-Inspired Debiasing Optimization for Generalizable Video Reasoning in Lightweight MLLMs](https://arxiv.org/abs/2605.01324)
- [ID-Crafter: VLM-Grounded Online RL for Compositional Multi-Subject Video Generation](https://arxiv.org/abs/2511.00511)
- [Recurrent Reasoning with Vision-Language Models for Estimating Long-Horizon Embodied Task Progress](https://arxiv.org/abs/2603.17312)
- [Think-as-You-See: Streaming Chain-of-Thought Reasoning for Large Vision-Language Models](https://arxiv.org/abs/2603.02872)

#### 📊 基准 / 评测 · 3 篇
- [AV-Reasoner: Improving and Benchmarking Clue-Grounded Audio-Visual Counting for MLLMs](https://openaccess.thecvf.com/content/CVPR2026/papers/Lu_AV-Reasoner_Improving_and_Benchmarking_Clue-Grounded_Audio-Visual_Counting_for_MLLMs_CVPR_2026_paper.pdf)
- [QUANTIPHY: A Quantitative Benchmark Evaluating Physical Reasoning Abilities of Vision-Language Models](https://arxiv.org/abs/2512.19526)
- [Think 360deg: Beyond Depth: Evaluating the Width-centric Reasoning Capability of MLLMs](https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_Think_360deg_Beyond_Depth_Evaluating_the_Width-centric_Reasoning_Capability_of_CVPR_2026_paper.pdf)

#### 🧩 其它（感知-推理协同 / 幻觉 / 领域应用） · 18 篇
- [A Causal Marriage between VLM and IRM from Understanding to Reasoning](https://openaccess.thecvf.com/content/CVPR2026/papers/Chen_A_Causal_Marriage_between_VLM_and_IRM_from_Understanding_to_CVPR_2026_paper.pdf)
- [BOP-ASK: Object-Interaction Reasoning for Vision-Language Models](https://arxiv.org/abs/2511.16857)
- [Breaking the Regional Perception Bottleneck of Multimodal Large Language Models via External Reasoning Framework](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_Breaking_the_Regional_Perception_Bottleneck_of_Multimodal_Large_Language_Models_CVPR_2026_paper.pdf)
- [Decouple to Generalize: Context-First Self-Evolving Learning for Data-Scarce Vision-Language Reasoning](https://arxiv.org/abs/2512.06835)
- [Deeper Thought, Weaker Aim: Understanding and Mitigating Perceptual Impairment during Reasoning in Multimodal Large Language Models](https://arxiv.org/abs/2603.14184)
- [From Intuition to Investigation: A Tool-Augmented Reasoning MLLM Framework for Generalizable Face Anti-Spoofing](https://arxiv.org/abs/2603.01038)
- [Grounded Chain-of-Thought for Multimodal Large Language Models](https://arxiv.org/abs/2503.12799)
- [Harnessing Chain-of-Thought Reasoning in Multimodal Large Language Models for Face Anti-Spoofing](https://arxiv.org/abs/2506.01783)
- [POINTS-Long: Adaptive Dual-Mode Visual Reasoning in MLLMs](https://arxiv.org/abs/2604.11627)
- [PixDLM: A Dual-Path Multimodal Language Model for UAV Reasoning Segmentation](https://arxiv.org/abs/2604.15670)
- [Pixels Don't Lie (But Your Detector Might): Bootstrapping MLLM-as-a-Judge for Trustworthy Deepfake Detection and Reasoning Supervision](https://openaccess.thecvf.com/content/CVPR2026/papers/Kuckreja_Pixels_Dont_Lie_But_Your_Detector_Might_Bootstrapping_MLLM-as-a-Judge_for_CVPR_2026_paper.pdf)
- [Prototypical Action Reasoning Facilitated by Vision-Language Alignment for Egocentric Action Anticipation](https://openaccess.thecvf.com/content/CVPR2026/papers/Shao_Prototypical_Action_Reasoning_Facilitated_by_Vision-Language_Alignment_for_Egocentric_Action_CVPR_2026_paper.pdf)
- [ReAG: Reasoning-Augmented Generation for Knowledge-based Visual Question Answering](https://arxiv.org/abs/2511.22715)
- [ReasonX: MLLM-Guided Intrinsic Image Decomposition](https://arxiv.org/abs/2512.04222)
- [See Further, Think Deeper: Advancing VLM's Reasoning Ability with Low-level Visual Cues and Reflection](https://openaccess.thecvf.com/content/CVPR2026/papers/Wu_See_Further_Think_Deeper_Advancing_VLMs_Reasoning_Ability_with_Low-level_CVPR_2026_paper.pdf)
- [StaR-KVQA: Structured Reasoning Traces for Implicit-Knowledge Visual Question Answering](https://arxiv.org/abs/2510.06638)
- [Think Visually, Reason Textually: Vision-Language Synergy in Abstract Reasoning](https://openaccess.thecvf.com/content/CVPR2026/papers/Zhang_Think_Visually_Reason_Textually_Vision-Language_Synergy_in_Abstract_Reasoning_CVPR_2026_paper.pdf)
- [Thinking Diffusion: Penalize and Guide Visual-Grounded Reasoning in Diffusion Multimodal Language Models](https://arxiv.org/abs/2604.05497)

#### 🚗 VLA / 驾驶 / 导航（暂不关注，仅存档） · 10 篇
- [ACoT-VLA: Action Chain-of-Thought for Vision-Language-Action Models](https://arxiv.org/abs/2601.11404)
- [AwareVLN: Reasoning with Self-awareness for Vision-Language Navigation](https://arxiv.org/abs/2605.22816)
- [Counterfactual VLA: Self-Reflective Vision-Language-Action Model with Adaptive Reasoning](https://arxiv.org/abs/2512.24426)
- [EE-RL: Vision Language Guided Reinforcement Learning with Explorer and Expert model for End-to-End Autonomous Driving](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_EE-RL_Vision_Language_Guided_Reinforcement_Learning_with_Explorer_and_Expert_CVPR_2026_paper.pdf)
- [Fast-ThinkAct: Efficient Vision-Language-Action Reasoning via Verbalizable Latent Planning](https://arxiv.org/abs/2601.09708)
- [HybridDriveVLA: Vision-Language-Action Model with Visual CoT reasoning and ToT Evaluation for Autonomous Driving](https://openaccess.thecvf.com/content/CVPR2026/papers/Bassole_HybridDriveVLA_Vision-Language-Action_Model_with_Visual_CoT_reasoning_and_ToT_Evaluation_CVPR_2026_paper.pdf)
- [NoRD: A Data-Efficient Vision-Language-Action Model that Drives without Reasoning](https://arxiv.org/abs/2602.21172)
- [Progress-Think: Semantic Progress Reasoning for Vision-Language Navigation](https://arxiv.org/abs/2511.17097)
- [TRM-VLA: Temporal-Aware Chain-of-Thought Reasoning and Memorization for Vision-Language-Action Models](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_TRM-VLA_Temporal-Aware_Chain-of-Thought_Reasoning_and_Memorization_for_Vision-Language-Action_Models_CVPR_2026_paper.pdf)
- [Towards Open Environments and Instructions: General Vision-Language Navigation via Fast-Slow Interactive Reasoning](https://arxiv.org/abs/2601.09111)

## 当前判断
- **test-time RL / training-free 推理增强**是最值得盯的小而美赛道（TTRV、DeepScan、
  Seeing Clearly 等 7 篇），改动小、无需训练数据，工程价值直接。
- **"推理伤感知"现象**被多篇独立指出（Deeper Thought Weaker Aim；More Thought Less
  Accuracy?）——说明简单堆 CoT 有代价，修复这个 trade-off 的工作会是下一波。
- **机理分析**开始出现（Why Does RL Generalize Better Than SFT?），方向从"刷点"转向"搞懂"。
- 空间/3D 推理量大（15 篇）但偏 benchmark 和数据注入，方法创新密度一般。
