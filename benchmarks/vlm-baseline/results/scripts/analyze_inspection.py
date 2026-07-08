#!/usr/bin/env python3
"""巡检结果诊断：分场景 acc、yes率、误判方向。用法: analyze_inspection.py <outputs>"""
import pandas as pd, glob, sys, os

O = sys.argv[1]
MODELS = ["Qwen3-VL-8B-Instruct-vllm", "GLM4_1VThinking-9b-vllm", "molmo-7B-D-0924"]

for M in MODELS:
    fs = sorted(glob.glob(f"{O}/{M}/T*/{M}_Inspection_auxmatch.xlsx"))
    if not fs:
        print(f"{M}: 无 auxmatch"); continue
    df = pd.read_excel(fs[-1])
    acc = (df["score"] == 1).mean() * 100 if "score" in df else float("nan")
    yes_rate = (df["extracted"].astype(str).str.lower() == "yes").mean() * 100
    unk = (df["extracted"].astype(str) == "Unknown").mean() * 100
    print(f"\n===== {M.split('-vllm')[0][:20]} | overall {acc:.1f} | 答yes率 {yes_rate:.0f}% | Unknown {unk:.0f}% =====")
    g = df.groupby("category").apply(
        lambda x: pd.Series({
            "acc": (x["score"] == 1).mean() * 100,
            "yes召回": (x[x["answer"] == "Yes"]["score"] == 1).mean() * 100,
            "no特异": (x[x["answer"] == "No"]["score"] == 1).mean() * 100,
        }), include_groups=False).round(0)
    print(g.to_string())
# 抽 2 条 Qwen 错例
fs = sorted(glob.glob(f"{O}/{MODELS[0]}/T*/{MODELS[0]}_Inspection_auxmatch.xlsx"))
df = pd.read_excel(fs[-1])
w = df[df["score"] != 1].head(3)
print("\n===== Qwen 错例抽样 =====")
for _, r in w.iterrows():
    print(f"[{r['category']}/{r.get('subcat','')}] GT={r['answer']} 提取={r['extracted']}")
    print("  pred:", str(r["prediction"])[:150].replace("\n", " "))
