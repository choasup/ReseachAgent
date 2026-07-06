#!/usr/bin/env python3
"""汇总 VLMEvalKit outputs/ 下各模型的 *_acc.csv 成一张对比表。
用法: python merge_results.py outputs/  →  summary.csv (行=基准, 列=模型)
"""
import sys, csv, glob, os, collections

root = sys.argv[1] if len(sys.argv) > 1 else "outputs"
table = collections.defaultdict(dict)   # bench -> model -> score

for path in glob.glob(os.path.join(root, "*", "*_acc.csv")):
    model = os.path.basename(os.path.dirname(path))
    fname = os.path.basename(path)                     # <model>_<BENCH>_acc.csv
    bench = fname[len(model) + 1: -len("_acc.csv")]
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        continue
    # 取 Overall 行（不同基准列名不一：Overall / none / 首行兜底）
    score = None
    for r in rows:
        key = (r.get("split") or r.get("Category") or r.get("category") or "").lower()
        if key in ("overall", "none", "all", ""):
            for col in ("Overall", "overall", "acc", "score", "hit"):
                if col in r and r[col]:
                    score = r[col]; break
        if score: break
    if score is None:  # 兜底：首行最后一个数值列
        for v in reversed(list(rows[0].values())):
            try: float(v); score = v; break
            except (ValueError, TypeError): continue
    table[bench][model] = score

models = sorted({m for b in table.values() for m in b})
out = os.path.join(root, "summary.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["benchmark"] + models)
    for bench in sorted(table):
        w.writerow([bench] + [table[bench].get(m, "") for m in models])

print(f"wrote {out}")
w = max((len(b) for b in table), default=10)
print("benchmark".ljust(w), *[m[:24].ljust(24) for m in models])
for bench in sorted(table):
    print(bench.ljust(w), *[str(table[bench].get(m, "-"))[:24].ljust(24) for m in models])
