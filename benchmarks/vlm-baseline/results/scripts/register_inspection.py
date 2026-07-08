#!/usr/bin/env python3
"""把 Inspection 巡检数据集注册进 VLMEvalKit 的 Y/N 数据集类（幂等）。
用法: python register_inspection.py <VLMEvalKit根> <LMUData下的Inspection.tsv>"""
import sys, os, re, hashlib

ROOT, TSV = sys.argv[1], sys.argv[2]
name = os.path.splitext(os.path.basename(TSV))[0]
md5 = hashlib.md5(open(TSV, "rb").read()).hexdigest()
p = os.path.join(ROOT, "vlmeval", "dataset", "image_yorn.py")
src = open(p, encoding="utf-8").read()

# 清掉旧注册行再插入（幂等 + md5 可更新）
src = re.sub(rf"\n\s*'{name}': '[^']*',(?=\n)", "", src)

anchor_url = "'POPE': "
anchor_md5 = "'POPE': "
iu = src.index("DATASET_URL")
im = src.index("DATASET_MD5")
# 在 DATASET_URL dict 的 POPE 行后插 URL（本地文件已就位，URL 仅占位）
pos = src.index(anchor_url, iu)
eol = src.index("\n", pos)
src = src[:eol + 1] + f"        '{name}': 'local://{name}.tsv',\n" + src[eol + 1:]
# 在 DATASET_MD5 dict 的 POPE 行后插 md5
pos = src.index(anchor_md5, src.index("DATASET_MD5"))
eol = src.index("\n", pos)
src = src[:eol + 1] + f"        '{name}': '{md5}',\n" + src[eol + 1:]

open(p, "w", encoding="utf-8").write(src)
print(f"registered {name} (md5={md5}) in image_yorn.py")
