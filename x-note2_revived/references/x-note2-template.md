# x-note2 模板

x-note2 混合知識筆記的標準格式。

---

## Frontmatter Template

```yaml
---
title: "<清楚描述的標題>"
source: "X"
source_url: "https://x.com/<handle>/status/<id>"
tweet_id: "<status_id>"
author: "<display name>"
handle: "@handle"
captured_at: "YYYY-MM-DD HH:mm:ss +08:00"
capture_method: "bb-browser/CDP single-status DOM"
content_hash: "<sha256 of post text>"
engagement:
  views: <N>
  likes: <N>
  reposts: <N>
  replies: <N>
  bookmarks: <N>
media_ids: ["<media_id>", ...]
score: 5
score_reason: "<為什麼值得保留>"
tags: [x-note2, <topic>, <author>, <type>]
sources:
  - "https://x.com/<handle>/status/<id>"
  - "00-Inbox/xnote_complete_YYYY-MM-DD.json"
type: "x-post-summary"
classification_path: "00-Inbox"
status: "inbox"
---

# <title>
```

---

## Body Template（完整版）

```markdown
# <title>

## Source Snapshot

- **Source URL**: https://x.com/<handle>/status/<id>
- **Author**: <display name>
- **Handle**: @handle
- **Post time (UTC)**: <ISO UTC>
- **Post time (Taipei)**: <YYYY-MM-DD HH:mm +08:00>
- **Engagement**:
  - Views: <N>
  - Likes: <N>
  - Reposts: <N>
  - Replies: <N>
  - Bookmarks: <N>
- **Media**: <有/無>
- **Content hash**: <sha256>
- **Capture method**: <抓取方式>

## Core Summary（BLUF格式）

[一句話結論。盡可能包含具體數字或效果]

[支撐這結論的2-3個關鍵點]

[對讀者的實踐意義——誰會用到、如何用到]

## Detailed Analysis

### 背景脈絡

[<帳號背景> — <該帳號的定位與專長>]
[<這則推文的語境：回應什麼/獨立分享/系列的一部分>]

### 與現有知識的關係

[<與 vault 中其他相關筆記的連結>]
[<與同作者其他推文的關聯>]
[<張力或矛盾點（若有）>]

### 實際應用場景

[<什麼情境下會需要這則知識>]
[<目標讀者是誰>]
[<如何使用：直接抄用/改編/啟發>]

## Key Knowledge Points

- **<主題1>**: <說明>
- **<主題2>**: <說明>
- **<Prompt（若有）>**: <位置在 Reference 中，此處標註摘要>

## Why It Matters

[<戰略價值>]
[<趨勢信號>]
[<對哪些人最有價值>]

## 風險與限制

[指出不可驗證處、資料邊界、外部依賴、偏誤來源]
[X 平台限制：推文可能被刪除、作者可能修改內容、演算法可能影響可見度]
[時效性：特定時間的觀察可能已過時]

## 我會怎麼用這篇內容

### 實際落地方式

[<具體應用場景1>]
[<具體應用場景2>]

### 下一步行動

- [ ] <行動項目1>
- [ ] <行動項目2>
- [ ] <行動項目3>

## Reference

### Complete X Post Text

```text
<完整推文原文，一字不漏，包括所有標點符號與emoji>
```

### Media References（若無附圖則略過）

- `<media_id>` → https://pbs.twimg.com/media/<media_id>.jpg

### Related Links

- <說明>: <URL>

## Related Notes

- [[<相關筆記標題>|<標籤描述>]]
```

---

## 縮減版（內容較短時使用）

若推文本身已極簡（無 Prompt、無背景脈絡），可用縮減版：

```markdown
## Core Summary（BLUF格式）

<一句話結論>

## Key Knowledge Points

- <要點1>
- <要點2>

## 我會怎麼用這篇內容

- <實際落地方式1>
- <下一步行動>

## Reference

### Complete X Post Text

```text
<完整原文>
```
```

---

## 含 Prompt 的變體

當推文含可直接複用的 Prompt 時，在 `## Reference` 下加 `### Prompt Inventory`：

```markdown
### Prompt Inventory

| 用途 | Prompt 類型 | 關鍵參數 |
|------|-----------|---------|
| 圖像生成 | GPT-Image2 | 主體描述、風格、比例 |

---

## 含附屬連結的變體

```markdown
### Related Links

- 完整工作流文章: https://t.co/xxx（指向附屬URL）
- @MrLarus 主頁: https://x.com/MrLarus
```

---

## 歸檔版（從 00-Inbox 移出時）

將 frontmatter 中的 `status: inbox` 改為 `status: archived`，並補上：

```yaml
archived_at: "YYYY-MM-DD"
classification_path: "08-Learning/04_AI-Engineering-Tools/x-note2/<category>/"
```

---

## 必要章節說明

| 章節 | 必要性 | 說明 |
|------|--------|------|
| `## Source Snapshot` | 必填 | 來源元數據、互動數據 |
| `## Core Summary` | 必填 | BLUF 格式，一句話結論 |
| `## Detailed Analysis` | 建議填寫 | 背景脈絡、應用場景 |
| `## Key Knowledge Points` | 建議填寫 | bullet 格式知識點 |
| `## Why It Matters` | 建議填寫 | 戰略價值 |
| `## 風險與限制` | **必填** | llm-wiki 傳承，不可省略 |
| `## 我會怎麼用這篇內容` | **必填** | llm-wiki 傳承，含落地方式與下一步行動 |
| `## Reference` | 必填 | 原文一字不漏 |
| `## Related Notes` | 建議填寫 | wikilinks 交叉連結 |
