#!/usr/bin/env python3
"""从 AI快速检查/ 的目录标注构建巡检 Y/N benchmark（VLMEvalKit TSV 格式）。
GT 规则：异常分类目录 -> yes，无异常目录 -> no。每场景正负均衡采样，异常按子类分层。
用法: python build_inspection.py <AI快速检查目录> <输出tsv> [每场景每极性张数=25]
"""
import os, sys, io, csv, base64, hashlib, random
import numpy as np
import cv2
from PIL import Image

ROOT = sys.argv[1]
OUT = sys.argv[2]
N_PER = int(sys.argv[3]) if len(sys.argv) > 3 else 25
random.seed(20260708)

# 场景: (正样本[异常]目录, 负样本[无异常]目录, 固定问题)
SCENES = [
    ("垃圾桶", ["垃圾桶检测/垃圾桶满溢"], ["垃圾桶检测/垃圾桶满溢-无异常"],
     "这是餐饮门店的监控画面。图中垃圾桶是否存在满溢、未加盖或盖板未闭合等异常？请回答 yes 或 no。"),
    ("客区清洁", ["客区清洁/客区清洁分类"], ["客区清洁/tencent_clean"],
     "这是餐饮门店客区的监控画面。图中客区的桌面或地面是否存在垃圾未清理的情况？请回答 yes 或 no。"),
    ("制作区清洁", ["制作区清洁/制作区清洁分类"], ["制作区清洁/制作区清洁-无异常"],
     "这是餐饮门店制作区的监控画面。图中制作区台面、清洗池或洗手池是否存在垃圾未清洁的情况？请回答 yes 或 no。"),
    ("仪容仪表", ["员工仪容仪表/分类"], ["员工仪容仪表/仪容仪表-无异常"],
     "这是餐饮门店的监控画面。图中员工的仪容仪表是否存在不规范（如未戴工帽、未戴工牌、着装颜色不符）？请回答 yes 或 no。"),
    ("人员状态", ["人员工作状态/员工个人物品放置于制作区"], ["人员工作状态/人员工作状态-无异常"],
     "这是餐饮门店的监控画面。图中是否存在员工个人物品放置在制作区的情况？请回答 yes 或 no。"),
    ("摄像头质检", ["摄像头质检/摄像头质检分类"], ["摄像头质检/摄像头质检-无异常"],
     "这是餐饮门店的监控画面。该摄像头画面是否存在异常（如角度不当、画面遮挡、无法观察到关键区域）？请回答 yes 或 no。"),
    ("物料摆放", ["物料摆放规范/物料摆放分类"], ["物料摆放规范/物料摆放-无异常"],
     "这是餐饮门店的监控画面。图中物料摆放是否存在不规范（如物料未离地、扫把或垃圾放置在客区、存放杂乱）？请回答 yes 或 no。"),
]

IMG_EXT = (".jpg", ".jpeg", ".png")


def list_images(d):
    out = []
    for r, _, fs in os.walk(d):
        for f in fs:
            if f.lower().endswith(IMG_EXT):
                out.append(os.path.join(r, f))
    return sorted(out)


def stratified(pos_dirs, n):
    """按一级子目录（异常子类）分层采样。"""
    groups = {}
    for pd in pos_dirs:
        full = os.path.join(ROOT, pd)
        if not os.path.isdir(full):
            continue
        subs = [s for s in sorted(os.listdir(full)) if os.path.isdir(os.path.join(full, s))]
        if not subs:                       # 无子类，整目录一组
            groups[os.path.basename(pd)] = list_images(full)
        for s in subs:
            groups[s] = list_images(os.path.join(full, s))
    groups = {k: v for k, v in groups.items() if v}
    if not groups:
        return []
    picked, keys = [], sorted(groups)
    i = 0
    while len(picked) < n and any(groups.values()):
        k = keys[i % len(keys)]
        if groups[k]:
            picked.append((k, groups[k].pop(random.randrange(len(groups[k])))))
        i += 1
        if i > n * 30:
            break
    return picked


def remove_red_marks(bgr):
    """去掉人工画的红色圈/框标注（细线状），避免模型走'见红圈答yes'捷径。
    只处理线状红色连通域（空心圈占其 bbox 面积比低），保留红色实物（灭火器/衣服等）。
    返回 (处理后图, 是否检测到标注)。"""
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    red = ((hsv[..., 0] <= 10) | (hsv[..., 0] >= 170)) & (hsv[..., 1] >= 110) & (hsv[..., 2] >= 90)
    red = red.astype(np.uint8)
    n, lab, stats, _ = cv2.connectedComponentsWithStats(red, 8)
    mask = np.zeros_like(red)
    found = False
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if w < 25 and h < 25:            # 噪点
            continue
        fill = area / max(w * h, 1)
        if fill < 0.30 and max(w, h) >= 30:   # 线状（空心圈/框）
            mask[lab == i] = 1
            found = True
    if not found:
        return bgr, False
    mask = cv2.dilate(mask, np.ones((7, 7), np.uint8))
    out = cv2.inpaint(bgr, mask, 6, cv2.INPAINT_TELEA)
    return out, True


STATS = {"marked": 0, "unmarked_pos": []}


def to_b64(path, box=1024, deredact=False):
    im = Image.open(path).convert("RGB")
    if deredact:
        bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        bgr, found = remove_red_marks(bgr)
        if found:
            STATS["marked"] += 1
        else:
            STATS["unmarked_pos"].append(path)
        im = Image.fromarray(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    im.thumbnail((box, box))
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode()


rows, idx = [], 0
print(f"{'场景':8} {'正(异常)':>8} {'负(正常)':>8}")
for scene, pos_dirs, neg_dirs, q in SCENES:
    pos = stratified(pos_dirs, N_PER)
    neg_imgs = []
    for nd in neg_dirs:
        neg_imgs += list_images(os.path.join(ROOT, nd))
    random.shuffle(neg_imgs)
    neg = [("无异常", p) for p in neg_imgs[:N_PER]]
    print(f"{scene:8} {len(pos):>8} {len(neg):>8}")
    for sub, path in pos:
        rows.append((idx, to_b64(path, deredact=True), q, "Yes", scene, sub, os.path.basename(path))); idx += 1
    for sub, path in neg:
        rows.append((idx, to_b64(path), q, "No", scene, sub, os.path.basename(path))); idx += 1

random.shuffle(rows)
with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["index", "image", "question", "answer", "category", "subcat", "srcfile"])
    for i, (_, b64, q, a, cat, sub, src) in enumerate(rows):
        w.writerow([i, b64, q, a, cat, sub, src])
ys = sum(1 for r in rows if r[3] == "Yes")
print(f"\nwrote {OUT}: {len(rows)} 题 (yes={ys}, no={len(rows)-ys}), "
      f"{os.path.getsize(OUT)//1048576} MB")
print(f"红圈修复: {STATS['marked']}/{ys} 正样本检测到并去除标注; "
      f"未检出标注的正样本 {len(STATS['unmarked_pos'])} 张")
for p in STATS["unmarked_pos"][:8]:
    print("  未检出:", p)
