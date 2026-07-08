# 001_VLM_benchmark —— VLM 摸底评测 + 交互 demo

三家开源 VLM（Qwen3-VL-8B / GLM-4.1V-9B / Molmo-7B-D）在 9 个公共基准上的摸底评测，
以及一个可拖图对比三模型的网页 demo。运行在本机 AMD MI308X（ROCm 6.3）。

## 目录

```
001_VLM_benchmark/
├── VLMEvalKit/              # 打过 ROCm 补丁的评测框架（见 patch_vlmevalkit.py）
│   └── outputs/             # 各模型各基准的预测与判分结果
├── demo_server.py           # 交互 demo（网页 UI，路径自适应，可整目录搬迁）
├── demo_history.jsonl       # demo 测试记录（持久化）
├── examples.json            # demo 示例用例（从各基准抽样）
├── patch_vlmevalkit.py      # ROCm 补丁（eager attn / Conv->matmul / LLM-judge 注册等）
├── merge_results.py         # 汇总 summary.csv（judge 修正口径）
├── sample_cases.py          # 抽正确/错误样例
├── reeval_judge.sh          # 抽取敏感基准用本机 vLLM 当 judge 重评
├── make_examples.py         # 生成 demo 示例用例
└── run_*.sh / *.log         # 各阶段运行脚本与日志
```

共享资源（不在本目录，绝对路径引用）：
- conda: `~/research/choasliu/miniforge3`，env `vlmeval`(transformers 4.57) / `vlmeval-molmo`(4.50.3)
- 权重: `~/research/choasliu/hf_home`；基准数据: `~/research/choasliu/LMUData`

## 结果

均分 Qwen 81.0 > GLM 77.7 > Molmo 72.5。完整报告见仓库 choasup/ReseachAgent
分支 claude/modest-allen-0mwbds 的 `benchmarks/vlm-baseline/results/REPORT.md`。

**关键**：README 指定的 `exact_matching` 判分对冗长输出系统性漏判（Qwen MMMU 21%→66%），
主表用本机 vLLM 当 LLM-judge 重抽答案修正，验证：翻负=0、Molmo 零变化。

## 交互 demo

```bash
# 服务器上（若未运行）：
cd ~/research/choasliu/Project/001_VLM_benchmark
conda activate vlmeval-molmo   # 或直接用该 env 的 python
HIP_VISIBLE_DEVICES=2 nohup python demo_server.py > demo.log 2>&1 &
# 本机开隧道后浏览器访问 http://localhost:7860
ssh -N -L 7860:localhost:7860 -p <端口> root@<服务器>
```

依赖：Qwen/GLM 的 vLLM serve 容器（`qweneval` 18001 / `glmeval` 18002）+ Molmo（transformers，
demo 进程内加载，占 1 张卡）。demo 功能：拖图 + 提问 → 三模型并行作答；示例用例一键载入；
测试记录持久化到 demo_history.jsonl。

## 复现评测
`bash reeval_judge.sh <model>` 重评；`python merge_results.py VLMEvalKit/outputs` 汇总。
ROCm 适配全在 `patch_vlmevalkit.py`（幂等，clone 新 VLMEvalKit 后跑一次即可）。
