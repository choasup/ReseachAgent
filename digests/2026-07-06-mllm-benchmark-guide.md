---
period: "methodology"
range: "多模态模型评测现状 + 自建 benchmark 方案（Qwen/Molmo/GLM 对比）"
generated: "2026-07-06"
---

# 多模态模型怎么测 & 自建 Benchmark 指南

## 业界评测地图
评测 = 基准 × 出题形式 × 判分 × 运行工具。

| 能力 | 常用基准 |
|---|---|
| 综合学科/推理 | MMMU/MMMU-Pro、MMStar、MM-Vet、MMBench |
| OCR/文档/图表 | DocVQA、ChartQA、OCRBench、InfographicVQA、TextVQA |
| 数学视觉 | MathVista、MathVision |
| 幻觉 | POPE、HallusionBench |
| 接地/指点 | RefCOCO(框)、pixmo-points-eval(点)、ScreenSpot(GUI) |
| 计数 | CountBenchQA、PixMo-Count |
| 视频 | Video-MME、MVBench、NextQA、PerceptionTest、LongVideoBench |
| 人评 | 视觉 Arena/Elo |

- 出题形式：MCQ（最稳）/ 短答案（需抽取规则）/ 开放生成（LLM-as-judge）。
- 判分可靠性：规则可验证 > 选项匹配 > LLM judge > 人评。
- **运行工具：VLMEvalKit（open-compass）**，220+ 模型/80+ 基准，已支持
  Qwen2/3-VL、Molmo 系列、GLM-4V；备选 lmms-eval。不要自写 runner
  （评测细节可造成 ~10 分差异，Molmo 论文明示）。

## 自建 benchmark 七步
0. **差异化定位**：通用基准已饱和；机会在"没人测好的能力"。推荐定位：
   可验证细粒度视觉任务（定位/计数/OCR小字/幻觉抵抗/格式遵循/业务域），
   正打 Qwen(通用强)/Molmo(接地强)/GLM(caption强) 的分歧点。
1. 能力矩阵：5-6 维 × 80-150 题/维（总 500-800，保显著性）。
2. **数据必须新**（自拍/业务图/2026 后网图），老图必污染——这是自建的最大价值。
3. MCQ 为主（选项位置随机化）+ 点选/计数（规则可验证）。
4. 锁箱：JSONL + split 写死 + sha256（见 templates/dataset-format.md）。
5. 运行协议：全模型走同一 harness、temperature=0、同 prompt、每题 3 次取多数；
   **绝不引用各家自报数字**。
6. 判分：能规则就规则；judge 模型固定+prompt 公开，抽样人工核一致率。
7. 报告：分维度分数 + bootstrap 置信区间 + 失败 case 图集（定性比分数更有传播力）。

## 防坑
- 污染（老图）/ 口径（必须同 harness）/ 主场偏差（点选题偏 Molmo，报告里明说）
- 每维 <50 题的差距是噪声 / API 版 vs 开源版行为不同要注明

## 关联
- Molmo 三层塔评测方法论：digests/2026-07-06-molmo-series-analysis.md
- 数据保存格式：templates/dataset-format.md
- Qwen vs Molmo 头对头现状：papers/2026/2026-07-06-molmo2-open-video-vlm.md
