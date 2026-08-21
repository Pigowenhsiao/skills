---
name: x-note2
description: "將 X/Twitter 推文轉化為混合知識筆記：保留 x-note 的原始抓取資料（tweet_id、互動數據、完整原文），嫁接 llm-wiki 的組織結構（BLUF摘要、多維分類、Source Snapshot、可追溯性）。適用於 AI 工具分享、Prompt 模板、實地觀察、商用案例等高價值推文。**注意：筆記格式必須遵循 llm-wiki 格式要求，`## 風險與限制` 與 `## 我會怎麼用這篇內容` 為必填章節。**"
version: 1.0.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [x-note2, twitter, knowledge-base, social-intel, prompt-preservation]
    category: knowledge-capture
    related_skills: [llm-wiki, x-note]
    vault_root: "E:/obsidian/PigoVault"
    output_default: "00-Inbox/"
    canonical_output: "08-Learning/04_AI-Engineering-Tools/x-note2/"
  format_requirements:
    required_sections:
      - "## 風險與限制"
      - "## 我會怎麼用這篇內容"
    reference: "references/x-note2-template.md"
triggers:
  - "x-note2"
  - "x-note 2"
  - "xnote2"
  - "將 x-note 整理成 llm-wiki"
  - "整合 x-note 與 llm-wiki"
---

# x-note2

將 X/Twitter 推文轉化為混合知識筆記。

## 核心定位

x-note2 是 x-note（抓取層）與 llm-wiki（組織層）的整合：

- **x-note 貢獻**：tweet_id、互動數據（views/likes/reposts/bookmarks）、完整原文、附屬連結、media ID、capture_method、score/scoring
- **llm-wiki 貢獻**：BLUF 摘要、Source Snapshot、Why It Matters、多維 tags、Related Notes 連結、Source 溯源原則

x-note2 **不是新的抓取工具**。抓取仍走 x-note 流程；x-note2 只負責把抓到的資料組織成更高品質的知識筆記。

## 與 x-note 的關係

| | x-note | x-note2 |
|---|---|---|
| **職責** | 抓取（CDP timeline → single-status） | 組織（原始資料 → 知識筆記） |
| **觸發時機** | 「抓 @handle 今天推文」 | 「整理成 x-note2」「把 x-note 升級」 |
| **存放位置** | 00-Inbox/ | 00-Inbox/（預設），正式歸檔至 08-Learning/04_AI-Engineering-Tools/x-note2/ |
| **是否修改** | 維持現有抓取流程 | 新流程，不動 x-note 舊檔案 |

**原則：x-note 舊檔案維持現況不動。x-note2 產出為新檔案。**

## 適用場景

- 將既有的 x-note（`00-Inbox/YYYY-MM-DD_x-note_*.md`）轉換為 x-note2 格式
- 直接從 x-note 的抓取資料（`xnote_complete_*.json`）生成 x-note2 格式筆記
- 對高價值推文（score >= 4）做深度整理

## Vault 路徑

- Vault root: `E:/obsidian/PigoVault`
- 預設輸出: `E:/obsidian/PigoVault/00-Inbox/`
- 正式歸檔: `E:/obsidian/PigoVault/08-Learning/04_AI-Engineering-Tools/x-note2/`
- 抓取原始資料: `E:/obsidian/PigoVault/00-Inbox/xnote_complete_*.json`

## Frontmatter Schema

```yaml
---
title: "<清楚描述的標題>"
source: "X"

# Source identity
source_url: "https://x.com/<handle>/status/<id>"
tweet_id: "<status_id>"
author: "<display name>"
handle: "@handle"

# Capture metadata
captured_at: "YYYY-MM-DD HH:mm:ss +08:00"
capture_method: "bb-browser/CDP single-status DOM"  # 或 jina-read / manual
content_hash: "<sha256 of post text>"

# Social signals（來自 X 互動數據）
engagement:
  views: 150700
  likes: 342
  reposts: 121
  replies: 2000
  bookmarks: 1500
media_ids: ["HJfBibdXYAMr7Wy", ...]  # X 圖片/影片 media ID

# llm-wiki-style scoring
score: 5
score_reason: "<為什麼值得保留>"
tags: [<topic>, <author>, <type>, ...]

# Source traceability
sources:
  - "https://x.com/<handle>/status/<id>"
  - "00-Inbox/xnote_complete_YYYY-MM-DD.json"
  - "<附屬連結URL>"   # 若有

# Output metadata
type: "x-post-summary"
classification_path: "00-Inbox"
status: "inbox"   # 或 "archived"
---

# <title>
```

### Frontmatter 欄位說明

| 欄位 | 必要性 | 說明 |
|------|--------|------|
| `title` | 必填 | 清楚描述，標題化 |
| `source` | 必填 | 固定 "X" |
| `source_url` | 必填 | 單篇推文 URL |
| `tweet_id` | 必填 | status ID |
| `author` | 必填 | 顯示名稱 |
| `handle` | 必填 | @handle |
| `captured_at` | 必填 | 抓取時間（+08:00） |
| `capture_method` | 必填 | 抓取方式 |
| `content_hash` | 必填 | 原文 SHA256，防止內容被竄改 |
| `engagement{}` | 必填 | 互動數據，統一結構 |
| `score` | 必填 | 1-5 |
| `score_reason` | 必填 | 保留理由 |
| `tags` | 必填 | 含 `x-note2` + topic + author |
| `sources[]` | 必填 | URL + JSON 路徑 |
| `media_ids[]` | 選填 | 有附圖時填寫 |
| `classification_path` | 選填 | 存放路徑 |
| `type` | 選填 | 固定 "x-post-summary" |

## Body 結構

```markdown
# <title>

## Source Snapshot

- **Source URL**: https://x.com/...
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
- **Media**: <有/無，列出 media IDs>
- **Content hash**: <sha256>
- **Capture method**: <抓取方式>

## Core Summary（BLUF格式）

[一句話結論]
[2-3句支撐]
[實踐意義]

## Detailed Analysis

[背景與脈絡]
[與現有知識的關係或張力]
[對讀者的價值]

## Key Knowledge Points

- **<主題1>**: <說明>
- **<主題2>**: <說明>
- ...

## Why It Matters

[戰略價值或長期影響]
[目標讀者是誰]
[什麼情境下會用到這則知識]

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
<完整推文原文，一字不漏>
```

### Media References

- `HJfBibdXYAMr7Wy` → https://pbs.twimg.com/media/HJfBibdXYAMr7Wy.jpg
- （若無附圖則略過此節）

### Related Links

- <附屬連結說明>: <URL>
- <@MrLarus 主頁>: https://x.com/MrLarus

## Related Notes

- [[<相關筆記標題>|<標籤描述>]]
- [[<同一作者其他筆記>|<作者其他工作流>]]
```

## Workflow

### 模式一：Overlay（轉換既有的 x-note）

當已有 `00-Inbox/YYYY-MM-DD_x-note_*.md` 時：

1. **讀取原始檔案**，確認有完整原文（`## Reference` 或 `## 原始貼文`）
2. **對照 `xnote_complete_*.json`**，補充 engagement 數據（views/likes/reposts）
3. **按 x-note2 template 重寫 frontmatter**：
   - 統一 engagement{} 結構
   - 補 `content_hash`
   - 補 `capture_method`
   - 統一 tags 含 `x-note2`
4. **調整 body 結構**：
   - 建立 `## Source Snapshot`（來自 JSON 或 frontmatter）
   - 保留原文（`## Reference`）不刪
   - 若原文含 Prompt，確保在 `## Reference` 中完整呈現
   - 補 `## Why It Matters` 和 `## Related Notes`
5. **寫入新檔案**：`00-Inbox/YYYY-MM-DD_x-note2_<slug>.md`
6. **不刪舊檔案**，新舊並存；舊檔案加 frontmatter 標註 `status: legacy`

### 模式二：Direct Generation（從 JSON 直接生成）

當有 `xnote_complete_*.json` 但無對應 x-note 時：

1. 讀取 `xnote_complete_*.json`
2. 依 x-note2 template 一次產出
3. 寫入 `00-Inbox/YYYY-MM-DD_x-note2_<slug>.md`

## 輸出後必做

每次完成 x-note2 產出後，必須更新：

1. `00-Inbox/index.md`（Current Inbox Files）
2. `00-Inbox/log.md`（Inbox Log）
3. `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`

格式：

```markdown
## 2026-05-30 x-note2（<N>篇）

| 日期 | 帳號 | 標題 | 檔案 |
|------|------|------|------|
| YYYY-MM-DD | @handle | <title> | 00-Inbox/YYYY-MM-DD_x-note2_<slug>.md |

- Source: x-note → x-note2 格式升級 / 直接生成
- Score: <分數>
- 備註: <特色說明>
```

## Prompt 保留規則

若推文含 **可直接複用的 Prompt**：

- 必須完整保留原文於 `## Reference` 區塊
- 正文 `## Key Knowledge Points` 可做分析摘要
- 若 Prompt 極長（>500 字），可在 `## Reference` 下另開 `### Prompt Inventory` 整理結構
- 不可聲稱「完整保留」但實際省略 Prompt 細節

## 分類與 Tags 建議

### 常見 Tags

```
x-note2          # 必含，系統識別
<platform>       # AI-video / AI-image / AI-coding / AI-agent
<author>         # @MrLarus / @yaojingang / @xiaoxiaodong01
<prompt>         # 含完整 Prompt 時
<workflow>       # 工作流分享
<observation>    # 實地觀察
<tool-demo>      # 工具演示
<case-study>     # 商用案例
<trend>          # 趨勢判斷
<methodology>    # 方法論
```

### 分類路徑建議

| 內容類型 | 正式歸檔路徑 |
|---------|------------|
| AI 影片/Prompt 工作流 | `08-Learning/04_AI-Engineering-Tools/AI-Video-Prompts/` |
| AI 圖片生成 Prompt | `08-Learning/04_AI-Engineering-Tools/Visual-Prompt-Design/` |
| AI Coding / Agent 工具 | `08-Learning/04_AI-Engineering-Tools/AI-Agent-Tools/` |
| 商用落地案例 | `08-Learning/04_AI-Engineering-Tools/Case-Studies/` |
| 團隊/個人工作模式觀察 | `08-Learning/04_AI-Engineering-Tools/Workflow-Patterns/` |
| Prompt 模板（通用） | `08-Learning/04_AI-Engineering-Tools/Prompt-Templates/` |
| 尚待分類 | `00-Inbox/`（不搶先歸檔） |

## 禁止事項

- 不要修改舊 x-note 檔案內容（只做 Overlay 時寫入新檔案）
- 不要在 `## Reference` 省略 Prompt 或部分截斷
- 不要把 `score` 當成決定性標準；score低的實用內容仍可整理
- 不要在沒有完整原文的情況下聲稱「完整保留」
- 不要跳過 index / log 更新
- **不要省略 `## 風險與限制`** — llm-wiki 傳承，必須指出不可驗證處、資料邊界、X 平台限制
- **不要省略 `## 我會怎麼用這篇內容`** — llm-wiki 傳承，必須含實際落地方式與下一步行動（checkbox list）

## 一句話原則

**x-note2 = x-note 的抓取資料 + llm-wiki 的組織結構 + 風險與落地意識；舊 x-note 不動，x-note2 產出為新檔案；Prompt 原文必須完整保留；`## 風險與限制` 與 `## 我會怎麼用這篇內容` 為必填章節。**
