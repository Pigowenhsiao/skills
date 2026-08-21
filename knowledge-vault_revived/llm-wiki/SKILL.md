---
name: llm-wiki
description: "在 PigoVault 中維護可持續累積的 markdown 知識庫。llm-wiki 只保留 runtime 與 references，正式內容一律寫入既有 vault 結構。"
version: 2.4.1
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, obsidian]
    category: research
    related_skills: [note-update, inbox-check, vault-check]
    config:
      - key: wiki.path
        description: Path to the active vault root
        default: "E:/obsidian/PigoVault"
        prompt: Vault root path
---

# LLM Wiki for PigoVault

在這個 workspace 中，`10-LLM-Wiki` 不是內容主樹，而是 runtime package。

- `10-LLM-Wiki/` 只保留 `SKILL.md` 與 `references/`
- 正式知識內容必須落到現有 vault 結構
- 所有輸出內容一律使用繁體中文

## Active Vault Root

目前正式 Vault root：

`E:\obsidian\PigoVault`

若其他文件仍提到 `Pigo_Obsidian`、`Learning/`、`Lumentum/` 舊 root，除非使用者明確指定，應以 `12-Meta/vault-structure.md` 和本文件為準。

## 核心原則：先 capture，再 organize

**筆記優先放 00-Inbox，再慢慢整理到正確位置。**

這是 Pigo 的個人偏好：
- 來源進來，先快速放到 00-Inbox
- 避免纠结分类而耽误 capture
- 後續有時間再整理到 `08-Learning/...`、`09-Article-Notes/...`、`03-Resources/Concept-Hubs/...` 或工作區

## Vault-first, Notion-second

當使用者要求 `llm-wiki` 整理文章、逐字稿、PDF、repo、URL 或本機檔案，且同時要求「放到 Notion」或「put in Notion」時，流程必須是：

1. 先在 Vault 建立或更新一份 Markdown 筆記。
2. 預設先放 `00-Inbox/`，除非使用者明確指定正式分類或現有規則能安全判斷目的地。
3. 更新 `00-Inbox/index.md`、`00-Inbox/log.md`、`08-Learning/99_Maintenance/status/LLM-Wiki-Index.md` 與 `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`。
4. Vault 筆記完成並驗證後，才建立或更新 Notion 頁面。
5. Notion 頁面必須保留 Vault 筆記路徑、來源路徑 / URL、hash 或其他可追溯 metadata。

不可只建立 Notion 頁面而不在 Vault 留 Markdown 版本。若 Notion 工具可用但 Vault 寫入失敗，停止 Notion 建頁並回報 blocker；若 Notion 建頁失敗但 Vault 已成功，回報 Notion blocker 並保留 Vault 筆記。

## 何時使用

當使用者要你做以下事情時使用這個 skill：

- 整理外部來源進 vault
- 把文章、影片、repo、工具整理成可持續更新的知識筆記
- 查詢既有學習內容並做交叉整理
- 檢查 llm-wiki 輸出是否放錯位置
- 整理 `08-Learning`、`09-Article-Notes`、`03-Resources/Concept-Hubs` 或工作區的知識

## 本 workspace 的硬規則

### 1. `10-LLM-Wiki/` 不是內容目錄

`10-LLM-Wiki/` 只用來放：

- `SKILL.md`
- `references/`

不得再把正式內容寫入以下舊位置：

- `10-LLM-Wiki/index.md`
- `10-LLM-Wiki/log.md`
- `10-LLM-Wiki/entities/`
- `10-LLM-Wiki/00-Inbox/`

### 2. 正式內容的 canonical 目的地

**預設目的地：**
- 所有新攝入的筆記 -> `00-Inbox/`

**整理後的目的地（手動或定時整理）：**
- 學習型知識主儲區 -> `08-Learning/` topic-first 子目錄
- 未萃取來源材料 -> `08-Learning/90_Source-Inbox/`
- evergreen article note、主題 hub、來源拆解 -> `09-Article-Notes/`
- 跨域概念 wrapper -> `03-Resources/Concept-Hubs/`
- 工作責任區精煉入口 -> `02-Areas/Work/`
- Lumentum / LGIT 原始工作脈絡與歷史材料 -> `17-WorkNotes/`
- 正式會議紀錄 -> `06-Meetings/`
- LLM-Wiki 索引與 ingest 歷史 -> `08-Learning/99_Maintenance/status/`

### 3. 新 Vault 架構摘要

- `00-Inbox/`：唯一正式收集箱；新來源與新文章先放這裡
- `01-Projects/`：跨域專案的精煉輸出
- `02-Areas/`：穩定責任區入口，不作大量內容主儲區
- `03-Resources/Concept-Hubs/`：跨域 canonical concept wrappers
- `04-Archive/`：封存內容
- `05-People/`：人物與關係索引
- `06-Meetings/`：正式會議紀錄
- `07-Daily/`：每日記錄
- `08-Learning/`：topic-first 學習知識主儲區
- `09-Article-Notes/`：主題化 article / source note / hub 系統
- `10-LLM-Wiki/`：runtime / references，不放正式知識內容
- `11-MOC/`：全 Vault 導航層
- `12-Meta/`：規則、狀態、報告、產物與治理文件
- `13-Templates/`：模板
- `14-Skills/`：Vault 內技能文件
- `15-Docs/`：工具、流程與方法論文件
- `16-Assets/`：媒體與附件
- `17-WorkNotes/`：工作知識與原始工作筆記

### 4. 導覽檔案

本 workspace 的 llm-wiki 主要導覽點是：

- `00-Inbox/index.md` - 收集箱索引
- `08-Learning/index.md` - 學習區索引
- `09-Article-Notes/index.md` - Article note 系統入口
- `09-Article-Notes/Vault-Classification-Index.md` - Article 分類索引
- `11-MOC/Index.md` - 全 Vault 導航
- `12-Meta/vault-structure.md` - Vault 架構 SSOT
- `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md` - LLM-Wiki 全域索引
- `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md` - 攝入日誌

必要時再同步更新：

- 對應 `08-Learning/<topic>/index.md`
- 對應 `09-Article-Notes/<kind>/README.md` 或 hub index
- `00-Inbox/log.md`
- `08-Learning/99_Maintenance/status/index.md`

## Session 開始時的檢查

在做 ingest、query、lint 之前，先讀：

1. `00-Inbox/index.md`
2. `08-Learning/index.md`
3. `09-Article-Notes/index.md`
4. `12-Meta/vault-structure.md`
5. `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
6. `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md` 的最近幾筆

目的：

- 避免重複建檔
- 避免把內容寫回舊 `10-LLM-Wiki/` 骨架
- 先理解目前索引與分類習慣

## Purpose（目的導引）

每次 ingest 和 query 前，讀取 `08-Learning/purpose.md`（若存在）以理解：

- 當前 wiki 的核心目標
- 正在研究的關鍵問題
- 語言與術語偏好

### Purpose 範本

若 `08-Learning/purpose.md` 不存在，建議建立：

```md
# Purpose

## 目標
- 建立可持續累積的繁體中文 AI 知識庫
- 所有內容來源可追溯
- 追蹤 AI 領域的最新發展

## 核心問題
- 哪些 AI 工具值得學習？
- 如何組織個人知識？
- 技術趨勢與應用場景？

## 語言規則
- 所有輸出使用繁體中文
- 優先使用台灣術語
```

## 筆記格式

整理文章、影片、網頁、repo 或工具時，優先參考：

- `10-LLM-Wiki/references/pigo-note-format-notebooklm-chrome-plugins.md`

至少要保留：

- 清楚標題
- 可追溯來源
- 核心摘要
- 關鍵知識點
- 與現有筆記的關聯

### Prompt 保留硬規則

若來源文章、貼文、逐字稿、repo 文件或附件中包含 **可直接複用的 Prompt**（例如 system prompt、instruction prompt、template prompt、workflow prompt、style prompt、image prompt、agent prompt、rubric prompt），則：

1. **必須完整複製原文 Prompt** 到輸出筆記。
2. 預設放在 `## Reference` 區塊；若有多段 Prompt，可用 `## Prompt Inventory` + `## Reference` 整理。
3. 不可只保留摘要、改寫版或節錄版，除非原文來源本身殘缺。
4. 若 Prompt 很長，正文可先分析與摘要，但 `## Reference` 仍必須保留完整可見文本，方便直接複製。
5. 若 Prompt 來自圖片、截圖或掃描件，應優先 OCR / DOM / 可見文字擷取；若仍無法完整取得，必須明確標註缺失範圍，不可假裝完整。

### X/Twitter 完整原文與非繁體中文重寫硬規則

當來源為 X/Twitter 貼文或推文串（Thread）時，為了確保知識的可追溯性與語系統一：

1. **必須將 X 貼文的原始全文完整複製** 並貼入輸出筆記中。
2. 完整原文必須寫入該筆記的 `## Reference` 區塊底下的 `### Complete X Post Text` 子段落中，並以 ` ```text ` 程式碼區塊包裹。
3. **【非繁體中文重寫規則】**：如果原始貼文包含非繁體中文的內容（如英文、簡體中文、日文等），在匯入筆記前，**必須使用流暢且符合台灣習慣的繁體中文（台灣專業術語優先）進行完整重寫與翻譯**，並將重寫後的繁體中文內容匯入 `### Complete X Post Text` 代碼塊中。
4. 嚴禁僅使用 Timeline 擷取的截斷文字或單純的 AI 摘要，必須是從單篇 Status 網頁中獲取的完整可見原文。
5. 若貼文中包含任何可直接複用的 Prompt 或操作指令，必須以最高完整度完整保留（若原 Prompt 為英文，可採英文原文與繁體中文翻譯對照方式呈現），不得進行任何省略、閹割或改寫。

Frontmatter 至少應包含常見欄位：

- `title`
- `source`
- `source_url`
- `created`
- `type`
- `tags`

## 兩步驟 Chain-of-Thought Ingest

每次攝入時採用兩步驟流程，確保高品質產出：

### Step 1：分析（Analysis）

先分析來源，不要直接生成：

```
輸入：來源內容（URL / 文字 / 檔案）
輸出：
  - 關鍵實體（人物、公司、產品、概念）
  - 核心論點或價值主張
  - 與現有 wiki 的關聯判斷
  - 矛盾與张力（與現有知識的衝突點）
  - 建議的 wiki 結構（新建頁面、更新頁面、連結關系）
  - 是否需要 human review
```

### Step 2：生成（Generation）

根據分析結果生成 wiki 頁面：

```
輸入：Step 1 的分析結果 + 來源內容
輸出：
  - Source summary 頁面（含 frontmatter 的 sources[]）
  - 對應的實體頁面或概念頁面
  - 交叉連結（wikilinks）
  - 更新 00-Inbox/index.md
  - 寫入 LLM-Wiki-Ingest-Log.md
```

### 增量快取（Incremental Cache）

每次攝入前：

1. 計算來源檔案的 SHA256 hash
2. 比對 `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md` 中的上次記錄
3. 只有 hash 變動的檔案才重新處理
4. unchanged 的檔案自動跳過

```bash
# 計算 hash
shasum -a 256 /path/to/source.md
```

### Source 溯源性

每個生成的 wiki 頁面必須在 frontmatter 中記錄來源：

```yaml
---
title: <標題>
sources:
  - /path/to/raw/source.md
  - <URL>
created: <ISO time>
type: article
tags: [...]
---
```

## Ingest Workflow

當使用者提供 URL、文章、影片、repo、工具說明或貼上內容時：

1. **讀取 Purpose**（若存在）
2. **增量檢查**：計算 hash，比對上次記錄
3. **Step 1 分析**：理解來源結構與現有知識的關係
4. **Step 2 生成**：根據分析生成對應頁面
5. **預設目的地**：00-Inbox/（根據 Pigo 偏好）
6. **搜尋既有 Learning 內容**，若有高度相關的，決定是否直接放到正確分類
7. **建立或更新對應筆記**
8. **若使用者要求同步 Notion**：先完成 Vault 筆記與索引，再建立或更新 Notion 頁面
9. **補上 wikilinks 與必要索引**
10. **更新**：
   - `00-Inbox/index.md`（收集箱索引）
   - `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
   - `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`
   - `08-Learning/overview.md`（全局摘要，自動更新）

### Prompt-First 補充規則

- 若來源含有 Prompt，`Step 2 生成` 階段除了摘要與分析外，**必須額外輸出完整 Prompt 原文**。
- 預設寫入同一篇筆記的 `## Reference` 區塊，必要時可再補 `## 可複用的 Prompt 結構` 分析。
- 使用者若明確要求「保留全部 prompt detail」或類似語意，視為不能省略任何可見 Prompt 內容。
- 若 Notion 也要同步，Vault 版先保留完整 Prompt，Notion 再以同等完整度同步；不可出現 Vault 有全文、Notion 只有摘要的落差，除非明確回報同步 blocker。

### 放置規則

| 情況 | 目的地 |
|------|--------|
| **新筆記（預設）** | `00-Inbox/` |
| **未萃取來源材料** | `08-Learning/90_Source-Inbox/` |
| **已確認的學習知識** | `08-Learning/<topic-first 子目錄>/` |
| **已整理成 article / hub / source note** | `09-Article-Notes/<kind>/<topic>/` |
| **跨域概念入口** | `03-Resources/Concept-Hubs/` |
| **工作知識或 LGIT 歷史材料** | `17-WorkNotes/` |
| **來源不完整** | `00-Inbox/` |
| **還無法確定分類** | `00-Inbox/` |
| **使用者明示正式歸檔** | 對應 canonical 目錄 |

### 整理時機

使用者在以下情況會主動整理：

- 使用 `inbox-check` skill 批次整理
- 週末或有空時回顧
-  Explicitly 說「整理」

## Query Workflow

當使用者問問題且答案應來自既有 llm-wiki / Learning 內容時：

1. **讀取 Purpose**（若存在）
2. **先查 `00-Inbox/index.md` 和 `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`**
3. **再查相關目錄**：
   - `00-Inbox/`
   - `08-Learning/`
   - `09-Article-Notes/`
   - `03-Resources/Concept-Hubs/`
   - `17-WorkNotes/`（工作脈絡相關問題才查）
4. **圖譜擴展**（可選）：從 seed nodes 出發，透過 wikilinks 擴展相關頁面
5. **讀取相關筆記並整合回答**
6. **若這次回答值得保存**，寫到 00-Inbox 或既有類別

### 圖譜擴展信號（4-Signal Relevance）

當需要擴展查詢範圍時，參考以下信號：

| 信號 | 權重 | 說明 |
|------|------|------|
| Direct link | ×3.0 | 頁面間有 `[[wikilinks]]` 連結 |
| Source overlap | ×4.0 | 共享同一個 source 的頁面 |
| Type affinity | ×1.0 | 同類型頁面（entity↔entity） |
| Path proximity | ×1.5 | 同一目錄下的頁面 |

## Lint / Health Check Workflow

當使用者要你檢查 llm-wiki 結構時，重點不是檢查 `10-LLM-Wiki/` 底下有多少內容，而是檢查：

- 是否還有正式內容誤放在 `10-LLM-Wiki/`
- `00-Inbox/` 是否有需要整理的筆記
- `08-Learning` 內容是否有壞連結
- `LLM-Wiki-Index` 是否落後
- `LLM-Wiki-Ingest-Log` 是否缺漏
- `08-Learning`、`09-Article-Notes`、`03-Resources/Concept-Hubs` 是否有明顯錯放
- 是否有孤島頁面（無任何 wikilinks 連入）

### 在這個 workspace 中，以下都視為結構錯誤

- 新內容被寫到 `10-LLM-Wiki/index.md`
- 新內容被寫到 `10-LLM-Wiki/log.md`
- 新內容被寫到 `10-LLM-Wiki/entities/`
- 新內容被寫到 `10-LLM-Wiki/00-Inbox/` 且沒有後續回收
- 內容仍連到不存在的舊分類，例如 `08-Learning/articles/`、`08-Learning/youtube/`、`08-Learning/repos/`、`08-Learning/papers/` 或 `08-Learning/videos/`
- 頁面缺少 `sources[]` frontmatter

### 知識缺口偵測

定期檢查並報告：

- **孤島頁面**：無任何 inbound wikilinks 的頁面
- **過時來源**：source 檔案已不存在的頁面
- **未更新狀態**：很久沒更新的 overview 或 index
- **積壓過多**：00-Inbox 超過一定數量需要整理

## Review System

當 ingest 過程中遇到需要 human judgment 的情況：

- 建立 `08-Learning/99_Maintenance/status/LLM-Wiki-Review.md` 記錄待決事項
- 預定義行動：Create Page、Deep Research、Skip
- 讓使用者在方便的時候處理，不阻塞 ingest

## Deep Research（可選功能）

當偵測到知識缺口且 Tavily API 可用時：

1. LLM 生成優化的搜索關鍵字
2. 使用 Tavily 或其他搜尋工具獲取內容
3. 將研究結果攝入 00-Inbox
4. 自動更新相關 index

## 與其他 skill 的邊界

- 單篇既有筆記升級、補分類、微調 -> 優先考慮 `note-update`
- 批次整理 `00-Inbox` -> 優先考慮 `inbox-check`
- 全 vault 健檢 -> 優先考慮 `vault-check`
- 本 skill 負責的是：把外部來源或 llm-wiki 流程整理進正確的知識骨架

## 更新後必做

每次完成 llm-wiki 相關修改後，至少驗證：

1. 新筆記落在 00-Inbox/（預設）
2. 沒有把內容寫回 `10-LLM-Wiki/`
3. 新頁面包含 `sources[]` frontmatter
4. `00-Inbox/index.md` 已更新
5. `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md` 已更新
6. `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md` 已更新
7. `08-Learning/overview.md` 已更新（若有的話）
8. 相關 index 或 landing page 沒有壞連結
9. 若同步 Notion，Vault Markdown 版本已先存在且 Notion 頁面有回指 Vault 路徑

## 禁止事項

- 不要把 `10-LLM-Wiki/` 當成內容主樹
- 不要再創建新的 `10-LLM-Wiki/entities/`、`concepts/`、`comparisons/`、`queries/`
- 不要再使用 `08-Learning/articles/`、`08-Learning/youtube/`、`08-Learning/repos/`、`08-Learning/papers/` 或 `08-Learning/videos/` 這種當前不存在的舊分類
- 不要跳過 index / log 更新
- 不要生成沒有 source 溯源的頁面
- 不要只放 Notion 而沒有先在 Vault 建立 Markdown 筆記
- 不要過度強調分類，capture 優先

## 一句話原則

在 `PigoVault` 中，`10-LLM-Wiki` 是整理流程，不是內容目的地；**筆記優先進 00-Inbox**，後續再整理到 `08-Learning`、`09-Article-Notes`、`03-Resources`、`17-WorkNotes` 與既有 vault 骨架；若同步 Notion，必須先有 Vault Markdown 版本，再處理 Notion。
