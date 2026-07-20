#!/usr/bin/env python3
"""按 ZwZ 论文 Table 2 结构汇总套件结果。
GP: ZoomBench(MCQ+Blank 加权 621:224) HR-4K HR-8K VStar CV-B MME-RW-en(Lite) MME-RW-cn -> GP-Avg
Specific: CountQA ColorBench(缺=N/A)   OOD: MMStar BabyVision(MCQ+Blank 加权 135:253)
用法: python suite_merge.py <outputs>"""
import sys, os, glob, json, csv, re

O = sys.argv[1]
MODELS = ["Qwen3-VL-8B-Instruct-vllm", "ZwZ-8B-vllm", "GLM4_1VThinking-9b-vllm",
          "Ovis2-8B-vllm", "Qwen2.5-VL-7B-vllm", "InternVL3-8B-vllm",
          "LLaVA-OneVision-7B-vllm", "Idefics3-8B-vllm", "Pixtral-12B-vllm", "molmo-7B-D-0924"]


def _num(x):
    try: return float(x)
    except (TypeError, ValueError): return None


def find_metric(model, bench):
    for d in sorted(glob.glob(f"{O}/{model}/T*"), reverse=True):
        base = os.path.join(d, f"{model}_{bench}")
        p = base + "_acc.csv"
        if os.path.exists(p):
            rows = list(csv.DictReader(open(p, encoding="utf-8")))
            if rows:
                r = rows[0]
                for c in ("Overall", "overall", "acc", "accuracy"):
                    v = _num(r.get(c))
                    if v is not None:
                        return v * 100 if v <= 1.0 else v
        p = base + "_rating.json"
        if os.path.exists(p):
            v = _num(json.load(open(p)).get("Overall"))
            if v is not None:
                return v * 100 if v <= 1.0 else v
    return None


def weighted(model, parts):
    tot_n, tot = 0, 0.0
    for b, n in parts:
        v = find_metric(model, b)
        if v is None: return None
        tot += v * n; tot_n += n
    return tot / tot_n


SUITE = [
    ("ZoomBench*", lambda m: weighted(m, [("ZoomBench", 621), ("ZoomBench_Blank", 224)])),
    ("HR-4K", lambda m: find_metric(m, "HRBench4K")),
    ("HR-8K", lambda m: find_metric(m, "HRBench8K")),
    ("VStar", lambda m: find_metric(m, "VStarBench")),
    ("CV-B.", lambda m: find_metric(m, "CVBench")),
    ("MME-RW-en†", lambda m: find_metric(m, "MME-RealWorld-Lite")),
    ("MME-RW-cn", lambda m: find_metric(m, "MME-RealWorld-CN")),
]
SPEC = [("CountQA", lambda m: find_metric(m, "CountBenchQA")),
        ("ColorB.", lambda m: None)]
OOD = [("MMStar", lambda m: find_metric(m, "MMStar")),
       ("BabyVis*", lambda m: weighted(m, [("BabyVision", 135), ("BabyVision_Blank", 253)]))]

hdr = [n for n, _ in SUITE] + ["GP-Avg"] + [n for n, _ in SPEC] + [n for n, _ in OOD] + ["Avg"]
table = {}
for m in MODELS:
    row, gp = [], []
    for _, f in SUITE:
        v = f(m); row.append(v)
        if v is not None: gp.append(v)
    row.append(sum(gp) / len(gp) if gp else None)
    vals_all = list(gp)
    for _, f in SPEC + OOD:
        v = f(m); row.append(v)
        if v is not None: vals_all.append(v)
    row.append(sum(vals_all) / len(vals_all) if vals_all else None)
    table[m] = row

disp = {m: re.sub(r"(-Instruct-vllm|-vllm|-0924)$", "", m) for m in MODELS}
out = os.path.join(O, "summary_zwz_suite.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Model"] + hdr)
    for m in MODELS:
        w.writerow([disp[m]] + [("" if v is None else round(v, 2)) for v in table[m]])
print(f"wrote {out}\n")
print("Model".ljust(20), *[h.ljust(9) for h in hdr])
for m in sorted(MODELS, key=lambda x: -(table[x][-1] or 0)):
    print(disp[m].ljust(20), *[("N/A" if v is None else f"{v:.1f}").ljust(9) for v in table[m]])
print("\n* = MCQ+Blank 加权; † = Lite 子集")
