#!/usr/bin/env python3
"""汇总 VLMEvalKit outputs/ 下各模型 × 各基准的头条指标成一张对比表（0-100 百分制）。
用法: python merge_results.py outputs/  ->  outputs/summary.csv (行=基准, 列=模型)

要点:
* 一个模型可能有多个时间戳目录（--mode eval 重评会新建目录）: 每个基准取"最新含该指标文件"的目录。
* 不同基准头条指标不同:
    MMMU_DEV_VAL : _acc.csv, split==validation 行, Overall 列（0-1 -> ×100）
    MMStar/RealWorldQA/DocVQA_VAL/ChartQA_TEST/CountBenchQA : _acc.csv, Overall/accuracy
    OCRBench     : _score.json, Final Score Norm
    POPE         : _score.csv, Overall
    HallusionBench: _score.csv, aAcc（题级准确率）
* 全部归一到 0-100（<=1 的分数 ×100）。模型名去 -vllm 后缀。
"""
import sys, csv, glob, os, json, collections, re

root = sys.argv[1] if len(sys.argv) > 1 else "outputs"
BENCHES = ["MMMU_DEV_VAL", "MMStar", "RealWorldQA", "DocVQA_VAL", "ChartQA_TEST",
           "OCRBench", "POPE", "HallusionBench", "CountBenchQA"]


def _num(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return None


def _norm(v):
    if v is None:
        return None
    return round(v * 100 if v <= 1.0 else v, 2)


def _pick_row(rows, prefer):
    for want in prefer:
        for r in rows:
            key = (r.get("split") or r.get("Category") or r.get("category") or "").strip().lower()
            if key == want:
                return r
    return rows[0] if rows else {}


def read_metric(path_noext, bench):
    p = path_noext + "_acc.csv"
    if os.path.exists(p):
        with open(p, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if rows:
            prefer = ["validation"] if bench == "MMMU_DEV_VAL" else ["overall", "none", "all", ""]
            r = _pick_row(rows, prefer)
            for col in ("Overall", "overall", "acc", "accuracy", "score", "hit"):
                if col in r and _num(r[col]) is not None:
                    return _norm(_num(r[col]))
            for v in reversed(list(rows[0].values())):
                if _num(v) is not None:
                    return _norm(_num(v))
    p = path_noext + "_score.csv"
    if os.path.exists(p):
        with open(p, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if rows:
            r = _pick_row(rows, ["overall", "none", "all", ""])
            cols = (("aAcc", "qAcc", "Overall") if bench == "HallusionBench"
                    else ("Overall", "overall", "acc", "score"))
            for col in cols:
                if col in r and _num(r[col]) is not None:
                    return _norm(_num(r[col]))
    p = path_noext + "_score.json"
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            d = json.load(f)
        for col in ("Final Score Norm", "Overall", "acc", "score"):
            if col in d and _num(d[col]) is not None:
                return _norm(_num(d[col]))
    return None


# 收集每个模型的所有时间戳目录（新->旧）
model_dirs = collections.defaultdict(list)  # raw_model -> [dirs newest first]
for d in sorted(glob.glob(os.path.join(root, "*", "T*")), reverse=True):
    raw = os.path.basename(os.path.dirname(d))
    if raw in ("logs", "cache", "_exact_backup"):
        continue
    model_dirs[raw].append(d)

table = collections.defaultdict(dict)   # bench -> disp_model -> score
disp_of = {}
for raw, dirs in model_dirs.items():
    disp = re.sub(r"-vllm$", "", raw)
    disp_of[raw] = disp
    for bench in BENCHES:
        for d in dirs:  # 新目录优先
            s = read_metric(os.path.join(d, f"{raw}_{bench}"), bench)
            if s is not None:
                table[bench][disp] = s
                break

models = sorted({disp_of[r] for r in model_dirs
                 if any(disp_of[r] in table[b] for b in BENCHES)})
out = os.path.join(root, "summary.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["benchmark"] + models)
    for bench in BENCHES:
        w.writerow([bench] + [table[bench].get(m, "") for m in models])

print(f"wrote {out}  (scores in 0-100)\n")
wb = max(len(b) for b in BENCHES)
print("benchmark".ljust(wb), *[m[:24].ljust(24) for m in models])
for bench in BENCHES:
    print(bench.ljust(wb), *[str(table[bench].get(m, "-")).ljust(24) for m in models])
