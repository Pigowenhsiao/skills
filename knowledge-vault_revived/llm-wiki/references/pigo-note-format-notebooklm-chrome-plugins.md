# Pigo Preferred Note Format

這份文件是 `10-LLM-Wiki` 在 `PigoVault` 中的優先整理模板。

適用於：

- NotebookLM 相關文章
- Chrome plugin / browser extension 文章
- 工具型長文整理
- 需要寫成可讀、可追溯、可回收的繁體中文知識筆記

## 使用原則

- 保留原始來源可追溯性
- 摘要必須可驗證，不要憑空補寫
- 先寫結論，再展開分析
- 新來源與新文章預設先進 `00-Inbox/`
- 整理完成後，內容要能移入 `08-Learning/<topic>`、`09-Article-Notes/<kind>`、`03-Resources/Concept-Hubs` 或工作區

## 推薦章節

```md
# <標題>

## 核心摘要

<用 1-2 段交代主要結論與最值得保留的重點>

## 文章分析

### 核心論點

<拆解主張、論證、方法或工作流>

### 風險與限制

<指出不可驗證處、資料邊界、外部依賴、偏誤來源>

## 關鍵知識點

- <知識點 1>
- <知識點 2>
- <知識點 3>

## 我會怎麼用這篇內容

- <實際落地方式 1>
- <實際落地方式 2>
- <下一步行動>

## 全文（繁中重寫）

<在不扭曲原意的前提下，重寫成流暢的繁體中文版本>

## 原文區塊

> <只保留可驗證、必要的原文摘錄>

## Source

- Source URL: <url>
- Source Type: <article / video / repo / notion / thread>
- Captured At: <ISO time>
- Tags: <...>

## 關聯筆記

- [[相關筆記 1]]
- [[相關筆記 2]]
- [[相關 index 或 hub]]
```

## 最低要求

若來源較短，不一定每篇都要寫到很長，但至少要保留：

- 標題
- 核心摘要
- 關鍵知識點
- Source
- 關聯筆記

## Frontmatter 建議

至少包含：

- `title`
- `source`
- `source_url`
- `created`
- `type`
- `tags`

若是影片，建議再補：

- `video_id`
- `channel`

若是 repo / 工具，建議再補：

- `repo`
- `platform`

## 適用邊界

這份模板適合：

- 長文整理
- 教學內容
- 方法論筆記
- 工具介紹

不適合：

- 純會議紀錄
- 很短的提醒型 memo
- 只做快速收件而不做正式整理的 Inbox 暫存

## 一句話總結

這份模板的目標不是把來源逐字搬進 vault，而是把來源轉成「可讀、可用、可回收」的繁體中文知識筆記。
