---
name: paper
description: 解读一篇 AI 论文并归档到知识库。当用户给出 arXiv ID/链接、PDF 或论文 URL，想要结构化中文解读时使用。
---

# /paper — 解读并归档论文

输入：arXiv ID / abs 链接 / PDF 链接 / 任意论文 URL（在 `$ARGUMENTS` 或对话中给出）。

## 步骤

1. **规范化来源**：若是 arXiv，统一成 `https://arxiv.org/abs/<id>`。记下 PDF/HTML 地址。
2. **读原文**：用 `WebFetch` 读 abstract 和正文要点（intro / method / experiments / limitations）。
   - 读不全时如实记录读到了哪些部分，不要凭记忆补全。
   - arXiv 全文可尝试 ar5iv：`https://ar5iv.org/abs/<id>`。
3. **填模板**：复制 `templates/paper-note.md`，逐项填写。
   - TL;DR ≤ 3 句；结论/数字附原文出处；"我的评价"要有判断（亮点/存疑/价值）。
4. **归档**：写到 `papers/<YYYY>/<归档日期 YYYY-MM-DD>-<slug>.md`。
   - `<slug>` 用核心方法名，小写连字符。今天日期见对话中的 currentDate。
5. **更新索引**：在 `INDEX.md` 对应主题下加一行，并更新顶部统计与"最后更新"。
   - 若该论文属于某个 `topics/` 主题，也在对应主题文件的追踪记录里标注"已解读"。
6. **回复用户**：给 TL;DR + 关键贡献 + 你的评价，附归档路径。

## 注意
- 不臆造。遵守 `CLAUDE.md` 的黄金规则。
- 一次只认真解读一篇；多篇时先确认顺序或逐篇处理。
