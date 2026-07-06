# 业务数据集保存格式模板

> 提炼自 Molmo/PixMo 数据工程实践（见 digests/2026-07-06-molmo-series-analysis.md）。
> 原则：标注 JSONL、图像存引用、切分进数据、模板与数据分离、坐标归一化。

## 目录结构
```
my-dataset/
├── README.md              # 数据卡：能力定义、采集协议、许可、统计
├── templates.json          # 各 task 的问题措辞模板（与数据分离，训练时随机套）
├── annotations/
│   ├── train.jsonl
│   ├── val.jsonl           # 内部 held-out（同分布）
│   └── test.jsonl          # 锁箱评测集，训练配置禁止读取
├── images/                 # 或对象存储 URL
└── stats.json              # 发版自动生成：各 task/split 计数
```

## 样本 schema（JSONL，一行一样本）
```json
{"id": "qc-2026-000123",
 "image": "images/line3/20260702_1432_cam2.jpg",
 "image_sha256": "a3f9c2...",
 "task": "defect_pointing",
 "question_slot": {"label": "焊点虚焊"},
 "answer": {"points": [{"x": 41.2, "y": 30.8}, {"x": 63.5, "y": 44.1}], "count": 2},
 "answer_text": null,
 "split": "train",
 "source": "产线3-相机2",
 "annotator": "a017",
 "annotated_at": "2026-07-02",
 "review": "passed",
 "license": "internal",
 "version": "v1.2"}
```

## 字段规则
- `task`：一种能力一个名（= PixMo 的 style），mixture 配比与能力审计的键。
- `question_slot`：只存槽位；整句措辞在 templates.json（每 task ≥10 种变体）。
- 坐标：全库统一归一化（0–100 或 0–1 二选一），点按 x 排序；答案存**结构化字段**，
  渲染格式（如 `<point x y>`）训练时生成，禁存渲染后字符串。
- `image_sha256`：对账用；`split` 写死进数据（防泄漏靠数据不靠随机种子）。
- 溯源：source / annotator / annotated_at / review 必填，坏批次可定位可回滚。

## 规模升级
- <50 万：JSONL + 图像文件（HF load_dataset 直接吃）
- 百万级：标注转 Parquet（列式过滤/统计快）
- 训练吞吐瓶颈：WebDataset tar 分片（图+标注打包顺序读）
- schema 定对了，格式转换是一行脚本；第一天把 schema 定对最重要。

## 禁忌
1. ❌ 答案存渲染后字符串（改协议=重标注）
2. ❌ 图像 base64 进 JSON（存引用）
3. ❌ 切分靠随机种子（split 进数据）
