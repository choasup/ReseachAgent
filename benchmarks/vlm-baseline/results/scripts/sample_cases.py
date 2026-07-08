#!/usr/bin/env python3
"""从各模型各基准逐题结果里抽正确/错误样例（供报告定性分析）。
不同基准逐题正确性来源不同：
  MCQ(MMMU/MMStar/RealWorldQA)      : *_gpt-4o-mini*result*.xlsx 的 hit
  Y/N(POPE/HallusionBench)          : *_auxmatch.xlsx 的 score
  VQA(DocVQA/ChartQA)               : *_results.xlsx 的 eval_score(>=0.5 视为对)
  OCRBench                          : 原始 xlsx，规范化后 gt 命中 pred
  CountBenchQA                      : 原始 xlsx，抽数字比对
输出 JSON。用法: python sample_cases.py <outputs> [每类条数] > samples.json
"""
import pandas as pd, glob, os, sys, json, re, ast

O = sys.argv[1]
N = int(sys.argv[2]) if len(sys.argv) > 2 else 3
MODELS = ["Qwen3-VL-8B-Instruct-vllm", "GLM4_1VThinking-9b-vllm", "molmo-7B-D-0924"]
MCQ = ["MMMU_DEV_VAL", "MMStar", "RealWorldQA"]
YN = ["POPE", "HallusionBench"]
VQA = ["DocVQA_VAL", "ChartQA_TEST"]
ALL = MCQ + VQA + ["OCRBench"] + YN + ["CountBenchQA"]


def latest(*pats):
    fs = []
    for p in pats:
        fs += glob.glob(p)
    return sorted(fs)[-1] if fs else None


def clip(x, n=300):
    return (lambda s: s[:n] + ("…" if len(s) > n else ""))(re.sub(r"\s+", " ", str(x)).strip())


def norm(s):
    return re.sub(r"[^a-z0-9]", "", str(s).lower())


def gt_list(a):
    try:
        v = ast.literal_eval(a) if isinstance(a, str) and a.startswith("[") else a
        return [str(x) for x in v] if isinstance(v, (list, tuple)) else [str(v)]
    except Exception:
        return [str(a)]


def firstnum(s):
    m = re.findall(r"-?\d+\.?\d*", str(s))
    return m[0] if m else None


def correctness(bench, row):
    if bench in MCQ:
        return str(row.get("hit")).lower() in ("1", "1.0", "true")
    if bench in YN:
        return str(row.get("score")).lower() in ("1", "1.0", "true")
    if bench in VQA:
        v = row.get("eval_score", row.get("eval_match"))
        try:
            return float(v) >= 0.5
        except (TypeError, ValueError):
            return str(v).lower() in ("1", "1.0", "true")
    if bench == "OCRBench":
        pred = norm(row.get("prediction"))
        return any(norm(g) and norm(g) in pred for g in gt_list(row.get("answer")))
    if bench == "CountBenchQA":
        return firstnum(row.get("prediction")) == firstnum(row.get("answer"))
    return None


def result_file(O, M, B):
    if B in MCQ:
        return latest(f"{O}/{M}/T*/{M}_{B}_gpt-4o-mini*result*.xlsx",
                      f"{O}/{M}/T*/{M}_{B}_exact_matching_result.xlsx")
    if B in YN:
        return latest(f"{O}/{M}/T*/{M}_{B}_auxmatch.xlsx")
    if B in VQA:
        return latest(f"{O}/{M}/T*/{M}_{B}_results.xlsx")
    return latest(f"{O}/{M}/T*/{M}_{B}.xlsx")  # OCRBench, CountBenchQA


out = {}
for M in MODELS:
    out[M] = {}
    for B in ALL:
        f = result_file(O, M, B)
        if not f:
            continue
        try:
            df = pd.read_excel(f)
        except Exception as e:
            out[M][B] = {"error": str(e)}; continue
        if B == "MMMU_DEV_VAL" and "split" in df.columns:
            df = df[df["split"].astype(str) == "validation"]
        rec = {"file": os.path.basename(f), "correct": [], "wrong": []}
        for _, r in df.iterrows():
            c = correctness(B, r)
            if c is None:
                continue
            item = {"q": clip(r.get("question", ""), 170), "gt": clip(r.get("answer", ""), 60),
                    "pred": clip(r.get("prediction", ""))}
            (rec["correct"] if c else rec["wrong"]).append(item) if \
                len(rec["correct" if c else "wrong"]) < N else None
            if len(rec["correct"]) >= N and len(rec["wrong"]) >= N:
                break
        out[M][B] = rec
print(json.dumps(out, ensure_ascii=False, indent=1))
