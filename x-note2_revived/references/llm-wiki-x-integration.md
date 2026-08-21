# llm-wiki 與 x-note2 的整合原則

## 兩個 Skill 的分工

| | llm-wiki | x-note2 |
|---|---|---|
| **觸發時機** | 任何外部來源（URL/文章/影片/PDF/repo） | X/Twitter 推文的專門整理 |
| **核心職責** | 把外部來源組織成可持續累積的知識筆記 | 將 X 推文的抓取資料組織成混合知識筆記 |
| **適配來源** | 文章、網頁、影片、Repo、PDF、工具說明 | X/Twitter 推文（含 thread、附屬連結、圖片） |

**x-note2 不是新的抓取工具。抓取仍走 x-note 流程；x-note2 只負責整理。**

## x-note2 繼承的 llm-wiki 原則

1. **Source 溯源**：每篇 x-note2 的 frontmatter 必须有 `sources[]`，含原始 URL + JSON 檔案路徑
2. **Prompt 保留硬規則**：完整原文不可截斷（含 Prompt）
3. **繁體中文輸出**：所有內容使用繁體中文
4. **capture_method**：標明抓取方式（bb-browser/CDP / jina-read / manual）
5. **索引更新**：完成後更新 `00-Inbox/index.md`、`log.md`、`LLM-Wiki-Ingest-Log.md`

## x-note2 對 llm-wiki 的新增貢獻

| 新增欄位 | llm-wiki 是否有 | x-note2 帶來什麼 |
|---------|--------------|----------------|
| `tweet_id` | 無 | X 推文的身分識別 |
| `handle` / `author` | 無 | 作者資訊（llm-wiki 用 `author` 但無 `handle`） |
| `engagement{}` | 無 | 社群互動數據（views/likes/reposts/bookmarks） |
| `media_ids[]` | 無 | X 圖片/影片 ID 清單 |
| `score` / `score_reason` | 無 | 品質評分機制 |
| `## Source Snapshot` | 無 | 統一呈現時間/互動/抓取方式 |
| `capture_method` | 無（sources[] 無此欄位） | 明確標示抓取技術 |

## Frontmatter 對照

```yaml
# llm-wiki 標準格式
---
title: "<標題>"
source: "<來源>"
source_url: "<URL>"
sources: ["<URL>", "<本地路徑>"]
created: "<ISO>"
type: "article"
tags: [...]
---

# x-note2 格式（llm-wiki 超集 + X 特有欄位）
---
title: "<標題>"
source: "X"                          # llm-wiki 有，但無 "X" 固定值
source_url: "https://x.com/..."      # llm-wiki 有
tweet_id: "<status_id>"              # X 新增
author: "<display name>"             # X 新增
handle: "@handle"                    # X 新增
captured_at: "<ISO +08:00>"          # X 新增（llm-wiki 用 created）
capture_method: "bb-browser/CDP"     # X 新增
content_hash: "<sha256>"              # X 新增
engagement:                           # X 新增（結構化）
  views: 150700
  likes: 342
  reposts: 121
  replies: 2000
  bookmarks: 1500
media_ids: ["<media_id>"]            # X 新增
score: 5                             # X 新增
score_reason: "<理由>"               # X 新增
tags: [x-note2, <topic>, <author>]   # x-note2 必含
sources: ["<URL>", "<JSON>"]          # llm-wiki 有，x-note2 延伸
type: "x-post-summary"                # llm-wiki 有
classification_path: "00-Inbox"       # x-note2 新增
status: "inbox"                       # x-note2 新增
---
```

## 從既有的 x-note 升級到 x-note2 的步驟

1. 讀取 `00-Inbox/YYYY-MM-DD_x-note_<slug>.md`
2. 補完 frontmatter（新增欄位如上）
3. 重寫 body 為 x-note2 結構（Source Snapshot / Core Summary(BLUF) / Detailed Analysis / Key Points / Why It Matters / Reference / Related Notes）
4. 寫入新檔案：`00-Inbox/YYYY-MM-DD_x-note2_<slug>.md`
5. **不刪舊檔案**
6. 更新 index / log / LLM-Wiki-Ingest-Log

## 從 JSON 直接生成 x-note2 的步驟

1. 讀取 `xnote_complete_YYYY-MM-DD.json`
2. 提取 tweet_id、author、handle、engagement、media_ids、full_text
3. 一次生成完整 x-note2 格式
4. 寫入 `00-Inbox/YYYY-MM-DD_x-note2_<slug>.md`

## 常見 Tags 建議（x-note2 專用）

```yaml
tags:
  - x-note2          # 必含，系統識別
  - <platform>        # AI-video / AI-image / AI-coding / AI-agent
  - <author>          # @MrLarus / @yaojingang / @xiaoxiaodong01
  - <type>            # workflow / observation / prompt / case-study / trend
  - <extra>           # prompt（含完整 Prompt）/ method / tool
```

## 分類路徑（正式歸檔時）

| 內容類型 | 路徑 |
|---------|------|
| AI 影片/Prompt 工作流 | `08-Learning/04_AI-Engineering-Tools/AI-Video-Prompts/` |
| AI 圖片生成 Prompt | `08-Learning/04_AI-Engineering-Tools/Visual-Prompt-Design/` |
| AI Coding / Agent 工具 | `08-Learning/04_AI-Engineering-Tools/AI-Agent-Tools/` |
| 商用落地案例 | `08-Learning/04_AI-Engineering-Tools/Case-Studies/` |
| 團隊/個人工作模式觀察 | `08-Learning/04_AI-Engineering-Tools/Workflow-Patterns/` |
| Prompt 模板（通用） | `08-Learning/04_AI-Engineering-Tools/Prompt-Templates/` |
| 尚待分類 | `00-Inbox/` |

## 禁止事項（與 llm-wiki 一致）

- 不要修改舊 x-note 檔案
- 不要在 `## Reference` 省略 Prompt
- 不要在沒有完整原文的情況下聲稱「完整保留」
- 不要跳過 index / log 更新
- 不要只放 Notion 而不先在 Vault 建立 Markdown 版本

## 一句話總結

x-note2 = x-note 的抓取資料 + llm-wiki 的組織結構 + X 特有的 social_signals；llm-wiki 保持不動，x-note2 獨立運行；舊 x-note 不改，x-note2 產出為新檔案。