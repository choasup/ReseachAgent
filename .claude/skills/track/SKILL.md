---
name: track
description: 追踪某个 AI 研究方向的最新论文。当用户想了解某个主题近期有什么新进展、或定期盯一个方向时使用。
---

# /track — 追踪主题新论文

输入：主题名或关键词（`$ARGUMENTS`）。未给则读 `topics/topics.yaml` 逐个追踪。

## 步骤

1. **定位主题**：在 `topics/topics.yaml` 找该主题；没有就新建一条（slug + keywords + cadence）。
2. **搜新论文**：用 `WebSearch` + arXiv 检索该方向最近的工作（默认近 1–3 个月）。
   - 组合 keywords，关注 arXiv、知名实验室、顶会。去掉明显不相关或太旧的。
3. **写入主题文件**：`topics/<slug>.md`（无则用 `templates/topic.md` 新建）。
   在"追踪记录"顶部追加一条 `### <今天日期>`，列出：标题 / 链接 / 一句话结论。
4. **更新 `last_tracked`** 和"当前判断"。
5. **回复用户**：精简清单 + 你认为最值得深读的 1–2 篇，问是否要 `/paper` 解读。

## 注意
- 一句话结论基于 abstract 即可，不必读全文（深读交给 /paper）。
- 标注哪些是新发现、哪些库里已有，避免重复。
