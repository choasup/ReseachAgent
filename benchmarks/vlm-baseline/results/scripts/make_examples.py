#!/usr/bin/env python3
"""从各基准抽代表性用例做 demo 示例。输出 examples.json（图 data URI + 题面）。
用法: python make_examples.py <LMUData目录> <输出路径>"""
import pandas as pd, os, sys, json, base64, io, ast, string
from PIL import Image

L = sys.argv[1]
OUT = sys.argv[2]

# (基准, 维度标签, 是否MCQ需补选项, 图像最小宽度阈值)
SPEC = [
    ("CountBenchQA", "计数", False, 200),
    ("OCRBench", "OCR", False, 60),
    ("ChartQA_TEST", "图表", False, 200),
    ("DocVQA_VAL", "文档", False, 200),
    ("HallusionBench", "幻觉", False, 150),
    ("MMMU_DEV_VAL", "综合推理", True, 150),
]


def img_from_row(row, box=384):
    b64 = row.get("image")
    if not isinstance(b64, str):
        return None
    if b64.startswith("["):
        try: b64 = ast.literal_eval(b64)[0]
        except Exception: return None
    try:
        im = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")
    except Exception:
        return None
    w = im.width
    im.thumbnail((box, box))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=82)
    return w, "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def build_prompt(bench, row, mcq):
    q = str(row.get("question", "")).strip()
    if mcq:
        opts = []
        for c in string.ascii_uppercase[:8]:
            v = row.get(c)
            if isinstance(v, str) and v.strip() and v.strip().lower() != "nan":
                opts.append(f"{c}. {v.strip()}")
        if opts:
            q = q + "\n" + "\n".join(opts) + "\n请选择正确选项。"
    if bench == "HallusionBench":
        q = q + "（请回答 yes 或 no）"
    return q


examples = []
for bench, label, mcq, minw in SPEC:
    p = f"{L}/{bench}.tsv"
    if not os.path.exists(p):
        print(f"skip {bench}: no tsv"); continue
    df = pd.read_csv(p, sep="\t")
    if bench == "MMMU_DEV_VAL" and "split" in df.columns:
        df = df[df["split"].astype(str) == "validation"]
    picked = None
    # 跳过前若干条，取中段一个图像够大、题面适中的
    for _, row in df.iloc[5:400].iterrows():
        q = str(row.get("question", "")).strip()
        if not (8 <= len(q) <= 180):
            continue
        r = img_from_row(row)
        if r and r[0] >= minw:
            picked = (row, r[1]); break
    if not picked:  # 放宽
        for _, row in df.iloc[5:200].iterrows():
            r = img_from_row(row)
            if r:
                picked = (row, r[1]); break
    if not picked:
        print(f"skip {bench}: no usable image"); continue
    row, uri = picked
    examples.append({"bench": bench.replace("_DEV_VAL", "").replace("_TEST", "").replace("_VAL", ""),
                     "label": label, "prompt": build_prompt(bench, row, mcq), "img": uri})
    print(f"ok {bench}: {label} | prompt[:40]={examples[-1]['prompt'][:40]!r}")

json.dump(examples, open(OUT, "w", encoding="utf-8"), ensure_ascii=False)
tot = sum(len(e["img"]) for e in examples)
print(f"wrote {OUT}: {len(examples)} examples, {tot//1024} KB base64")
