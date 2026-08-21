---
name: notion-youtube-ai-database-ingest
description: 將 YouTube 影片自動寫入 Notion「Ai DataBase View」，填入欄位、標籤、摘要與影片嵌入；若 notion MCP 當前會話授權失敗，改走 codex exec 通道完成。
---

# Notion YouTube AI Database Ingest

## Overview

把單支 YouTube 影片完整落地到 Notion `Ai DataBase View`：

1. 填入資料庫欄位（標題、URL、Tag、多選欄位、處理旗標）
2. 產生可讀摘要（含重點、流程、風險、建議）
3. 在頁面中放可嵌入影片連結
4. 立即做寫回驗證

此 Skill 適用於使用者要求：
- 「把這支 YouTube 放進 Notion 資料庫」
- 「幫我填標題 / tags / 欄位並做摘要」
- 「要把影片嵌入頁面」

## Fixed Target (Default)

- Database: `Ai DataBase View`
- `database_id`: `039bbec4-bfc0-44e8-854a-6239c80d8182`
- `data_source_id`: `6c262f43-ffdb-4b3b-b5a5-38c02ac8a2e1`

如果使用者明確指定其他資料庫，先改走 `notion-search + notion-fetch` 重新定位，不能硬套本預設。

## Execution SOP

### Step 1: Resolve Notion Path and Auth

1. 先嘗試直接使用 `notion-search` / `notion-fetch`。
2. 若回 `Auth required`，先執行 Cookie-first：
   - 先向使用者索取 cookie 匯出檔（優先 `cookies.txt`）。
   - 先嘗試用 cookie 恢復 Notion 會話。
   - 恢復後再重試 `notion-search` / `notion-fetch`。
3. 若 Cookie 恢復仍失敗，再改走 fallback：
   - 以 `codex exec` 在可授權通道呼叫 Notion MCP。
   - 只保留結構化 JSON 輸出做後續流程。

### Step 2: Fetch Schema and Allowed Options

1. 讀取 data source schema，確認至少以下欄位存在：
   - `Name`, `URL`, `Website`, `Tags`
   - `內容類型`, `平台/環境`, `整合對象`, `標籤`
   - `已下載字幕`, `已處理`, `文字`
2. 讀取 multi-select 可用選項。
3. 寫入值必須優先用既有選項；若無可用選項，再與使用者確認是否新增。

### Step 3: Collect Video Signals

1. 影片基本資訊：
   - 用 `yt-dlp` 取 `title/uploader/duration/upload_date`
2. 字幕/逐字稿：
   - 優先 `youtube_transcript_api`
   - 優先語系順序：`zh-Hans`, `zh-Hant`, `zh-TW`, `zh`, `en`
3. 若拿不到字幕：
   - 仍可建立頁面，但要在內容中標註「摘要為 metadata 推定，非逐字稿驗證」。

### Step 4: Compose Notion Payload

建立頁面時至少填：

- `Name`: 可讀、可檢索的標題（建議含主題與用途）
- `URL`, `Website`: 影片 URL
- `Tags`: 選 4-8 個高辨識度標籤
- `內容類型`: 通常 `工具整合` / `工作流` / `案例` 等
- `平台/環境`: 依影片內容填實際平台（如 `Windows`, `Docker`, `Web UI`）
- `整合對象`: 依內容填（如 `Codex`, `Claude Code`, `MCP`）
- `標籤`: 用較高階分類（如 `資料來源`, `筆記`）
- `已下載字幕`: 若拿到字幕則 `checked`
- `已處理`: 完成摘要與寫入後 `checked`
- `文字`: 一句話描述核心價值

### Step 5: Page Content Template (Traditional Chinese)

內文使用以下結構：

1. `影片連結（可嵌入）`
   - 單獨一行放 YouTube URL
2. `影片摘要`（5-7 句）
3. `關鍵重點`（至少 6 點）
4. `方法/流程`（若內容有步驟，列 1..N）
5. `局限與風險`（至少 3 點）
6. `實作建議`（至少 4 點）

### Step 6: Verify Write-back

建立完成後必做驗證：

1. `notion-fetch` 該 page
2. 回報以下結果：
   - page id / url
   - 主要欄位是否寫入成功
   - `has_youtube_url_in_content`
   - 主要 heading 清單

若驗證失敗，需指出是哪個欄位不一致並重試修正。

## Output Contract

對使用者最終回覆至少包含：

- 新頁面 URL
- 已寫入欄位摘要（Name/Tags/主要分類欄位）
- 是否完成嵌入與摘要
- 是否完成驗證
- 若使用 fallback（`codex exec`），需明確標註

## Safety Rules

1. 不覆蓋既有頁面，除非使用者明確要求 update 指定 page。
2. 不猜測不存在的資料庫 schema。
3. 任何「已完成」都必須以 fetch 驗證為準。
4. Notion 連線失敗時，優先切換通道，不要卡在空重試。
