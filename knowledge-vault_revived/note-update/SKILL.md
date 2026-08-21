---
name: note-update
description: Use when one existing note, especially a note in `00-Inbox`, should be upgraded into a formal vault note, moved into the correct category, linked to the current vault structure, indexed, and minimally backfilled into nearby notes without doing batch inbox triage or full-vault ingest.
version: 2.5.0-pigo
author: Hermes Agent
license: MIT
---

所有輸出內容一律使用繁體中文。

# Note Update


## Folder Context Before Placement

Before creating, moving, reclassifying, or updating any durable note, study the local folder context first so the note lands in the correct place.

Required reading order:
1. Read the vault root `AGENTS.md`.
2. Read the `README.md` in the candidate destination folder when it exists.
3. Walk upward from the candidate destination folder to the vault root and read each available parent `README.md`.
4. When comparing multiple candidate folders, read each candidate folder's local `README.md` before choosing.

Placement rules:
- Treat `AGENTS.md` as the global control plane and folder `README.md` files as local placement contracts.
- Use folder `README.md` content to understand purpose, accepted note types, naming conventions, index expectations, and sensitive-content boundaries.
- Classify by the note's actual article/content meaning and durable knowledge purpose first; source platform is only metadata, not the default destination.
- Do not file a note under `twitter`, `youtube`, or another source-platform folder merely because the source came from that platform.
- If a folder has no `README.md`, do not invent rules for it. Infer conservatively from `AGENTS.md`, nearby `index.md`, existing notes, and the user's explicit instruction.
- If folder guidance conflicts, follow this priority: user instruction, vault root `AGENTS.md`, nearest folder `README.md`, parent folder `README.md`, then this skill.
- If the correct folder is still ambiguous after reading context, pause and ask Pigo instead of filing the note into a guessed location.

## 08-Learning Topic Classification Architecture

`note-update` must use the 2026-05-02 `08-Learning` reshape as the current routing contract.

### Canonical Learning Root

The durable learning root is:

- `08-Learning/`

Do not route new durable notes to a bare `Learning/` path. Older references to `Learning/` in this skill mean `08-Learning/` inside PigoVault.

### Core Principle

Route by the note's durable knowledge purpose, not by the source platform.

This is a Pigo hard rule. When formalizing or moving a note, never choose the destination primarily from `source`, `source_url`, `original_platform`, filename prefix, tweet ID, video ID, or repo URL. These fields are provenance only. The folder decision must come from the note's content category and future retrieval use.

Source folders have been retired as top-level durable destinations. Keep unsynthesized source material under:

- `08-Learning/90_Source-Inbox/articles/`
- `08-Learning/90_Source-Inbox/twitter/`
- `08-Learning/90_Source-Inbox/youtube/`
- `08-Learning/90_Source-Inbox/news/`

For methods, workflows, frameworks, tools, prompts, research notes, creative workflows, business analysis, personal learning, health, or finance, route into the topic-first folders below.

### Canonical Topic Folders

| Destination | Use for |
|---|---|
| `08-Learning/01_AI-Agent/` | Agent workflows, harness engineering, evals, multi-agent systems, Claude Code, Codex, OpenClaw, MCP, tool use, automation architecture |
| `08-Learning/02_Knowledge-Systems/` | Obsidian, Notion, NotebookLM, RAG, LLM Wiki, knowledge-base design, information architecture |
| `08-Learning/03_Prompt-Context-Engineering/` | Prompt patterns, context engineering, system prompts, Skill prompt design |
| `08-Learning/04_AI-Engineering-Tools/` | Models, AI platforms, SDKs, repos, developer tools, Gemini, OpenAI, Anthropic platform notes, Ollama, LM Studio, Magika |
| `08-Learning/05_Research-Papers/` | Papers, benchmarks, evals, research workflow, paper reading, source collection, AI research methods |
| `08-Learning/07_Business-Finance/` | Business models, industry analysis, company strategy, AI economics, finance, investment, trading, financial markets |
| `08-Learning/08_Creative-Applications/` | Design references, brand examples, UI/product style references, writing, presentation, video, audio, content generation, publishing workflows |
| `08-Learning/09_General-Learning/` | Courses, learning methods, personal growth, habits, reflection, health, body, lifestyle, daily habits, useful notes not yet classifiable into a stronger topic |
| `08-Learning/90_Source-Inbox/` | Unread or unsynthesized source material from articles, X/Twitter, YouTube, newsletters, and news digests |
| `08-Learning/99_Maintenance/` | Import logs, classification reports, audit output, legacy indexes, and maintenance records |

### Retired / Non-Canonical Folders

Do not create or route notes into these retired folders:

- `08-Learning/articles/`
- `08-Learning/twitter/`
- `08-Learning/youtube/`
- `08-Learning/news/`
- `08-Learning/repos/`
- `08-Learning/courses/`
- `08-Learning/status/`
- `08-Learning/notion-knowledge/`
- `08-Learning/notion-knowledge/03_模型平台/`
- `08-Learning/notion-knowledge/99_雜記/`

If an existing note or link references them, map it forward:

- `articles`, `twitter`, `youtube`, `news` -> `90_Source-Inbox/<source-type>`
- `repos` -> `04_AI-Engineering-Tools/repos`
- `courses` -> `09_General-Learning/courses`
- `status` -> `99_Maintenance/status`
- `notion-knowledge/01_知識系統` -> `02_Knowledge-Systems`
- `notion-knowledge/02_AI工程` -> `01_AI-Agent`
- `notion-knowledge/03_模型_工具與平台` and `03_模型平台` -> `04_AI-Engineering-Tools`
- `notion-knowledge/04_提示詞` -> `03_Prompt-Context-Engineering`
- `notion-knowledge/04_商業財經` and `07_金融財經` -> `07_Business-Finance`
- `notion-knowledge/05_學習研究` -> `05_Research-Papers`
- `notion-knowledge/06_創作應用` -> `08_Creative-Applications`
- `notion-knowledge/05_學習成長`, `08_健康生活`, `99_其他`, and `99_雜記` -> `09_General-Learning`

### Frontmatter

When moving or formalizing a note under `08-Learning/`, ensure frontmatter contains or updates:

```yaml
classification_path: 08-Learning/<canonical-topic-path>
```

Keep source metadata (`source`, `source_url`, `tweet_id`, `video_id`, `repo_url`, `original_platform`) as provenance, not as the main folder decision.

### Indexing

After routing a note, update the nearest destination `index.md`. For large subclusters, prefer the subfolder index over only the top-level topic index.

Examples:

- Agent workflow note -> `08-Learning/01_AI-Agent/Agent-Workflow/index.md`
- Claude Code / Codex note -> `08-Learning/01_AI-Agent/Claude-Codex/index.md`
- Design reference note -> `08-Learning/08_Creative-Applications/Design-Reference/index.md`
- Media / writing / PPT note -> `08-Learning/08_Creative-Applications/Media-Content/index.md`

## 03-Resources Resource Classification Architecture

`03-Resources/` is not a general inbox and not a source-material dump. Use it only for reusable reference assets that Pigo or future agents will look up across multiple projects, notes, articles, workflows, or learning topics.

### Canonical Resources Root

The durable resources root is:

- `03-Resources/`

Use this exact capitalization in durable wikilinks and `classification_path` values.

### Root Folder Rule

Do not leave ordinary resource notes directly under `03-Resources/`.

Allowed root-level files are only navigation/control files such as:

- `README.md`
- `index.md`

If a note belongs in `03-Resources/`, place it into a numbered child folder.

### Numbered Folder Rule

Every direct durable content category under `03-Resources/` should use this pattern:

```text
NNN-Descriptive-Category
```

Examples:

- `001-Prompt-Engineering`
- `002-Media-Production-Workflows`

When a suitable numbered category already exists, reuse it. Create a new numbered category only when the note's reusable purpose does not fit existing folders.

When creating a new numbered category:

1. Choose the next available three-digit prefix.
2. Use a concise English slug after the prefix.
3. Create both `README.md` and `Index.md` inside the folder.
4. Add the folder to `03-Resources/README.md`.
5. Add the folder to `03-Resources/index.md`.

### Required Files In Each Resource Category

Each numbered `03-Resources` category must include:

- `README.md`: local placement contract, scope, exclusions, and navigation.
- `Index.md`: MOC for notes inside that category.

Use `Index.md` with uppercase `I` for these category-level resource indexes. Keep the root landing page as `03-Resources/index.md` to match the existing Vault convention.

### Existing Resource Categories

| Destination | Use for |
|---|---|
| `03-Resources/001-Prompt-Engineering/` | Reusable prompt engineering, context engineering, deep research prompting, anti-sycophancy, AI writing, and task design resources |
| `03-Resources/002-Media-Production-Workflows/` | Reusable media production, video creation, creator operations, content workflow, production pipeline, and AI-assisted media ops resources |
| `03-Resources/Concept-Hubs/` | Canonical cross-domain concept wrappers and durable concept hubs |
| `03-Resources/Weekly Reports Inbox/` | Weekly report or review-material staging only; still respect sensitive/local-only rules |

### Placement Decision Rules

Classify by durable reuse purpose:

- A note that is primarily a learning article, research note, tool analysis, or source summary should usually stay under `08-Learning/`.
- A note that has been distilled into a reusable method, reference card, workflow pattern, checklist, or cross-project asset may belong under `03-Resources/`.
- A source platform such as YouTube, X, Substack, GitHub, or Notion is provenance only. It is not a `03-Resources` category.
- If a resource is concept-level and should be reused broadly across many areas, consider `03-Resources/Concept-Hubs/`.
- If a resource is a concrete reusable method collection, workflow example, or reference note, prefer a numbered `03-Resources/NNN-*` category.

When Pigo explicitly asks to put a note in `03-Resources/`, still read `03-Resources/README.md`, inspect existing numbered category `README.md` files, and route into the most specific category instead of leaving the note at the root.

### Frontmatter

When moving or formalizing a note under `03-Resources/`, ensure frontmatter contains or updates:

```yaml
classification_path: "03-Resources/<category-path>"
status: "filed"
```

Preserve source metadata such as `source`, `source_url`, `tweet_id`, `video_id`, `repo_url`, `notion_url`, `transcript_hash`, and `sources`.

### Indexing

After routing a note under `03-Resources/`:

1. Add the note to the nearest category `Index.md`.
2. Add or update the category entry in `03-Resources/index.md`.
3. If the note moved from `00-Inbox/`, update `00-Inbox/index.md` and `00-Inbox/log.md`.
4. If the note was created by `llm-wiki` or affects source discoverability, update:
   - `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
   - `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`

Do not use `index.md` as an operation log. Use it only for navigation and collection.

### Minimal Backfill For 03-Resources

For `03-Resources/` moves, minimal backfill usually means:

- Add one backlink from a directly related concept hub or formal note when it already exists.
- Update stale links that still point to the old `00-Inbox/` or root `03-Resources/` path.
- Do not reorganize all of `03-Resources/` unless Pigo explicitly asks for a broader `vault-reshape` or `vault-GPS` pass.

## Description

`note-update` 是給 Pigo vault 的單篇筆記升級技能。

它的主要工作不是抓新來源，而是把**已經存在於 vault 裡的筆記**，尤其是 `00-Inbox/` 的半成品筆記，整理成可長期使用的正式知識筆記，並放到正確的 vault 類別。

這個 skill 的核心責任是：

- 讀懂現有筆記，而不是直接重寫
- 判斷該筆記應落到哪個正式類別
- 把內容改寫成可重用知識，而不是單純摘錄
- 補上 `[[wikilinks]]`、`Source`、索引入口與最小反向關聯
- 讓這篇筆記進入目前 vault 結構，而不是繼續卡在 `00-Inbox`

## 這個 skill 的定位

`note-update` 專管「單篇或極少數明確指定筆記」的正式化與歸檔。

它不負責：

- 從 URL / YouTube / X / PDF 抓原始來源
- 整批處理 `00-Inbox`
- 全 vault lint
- Notion sync
- git sync

這些工作仍然交給：

- `llm-wiki`：外部來源 ingest、wiki 路由、全域維護
- `inbox-check`：整批 `00-Inbox` 清理
- `vault-check`：全庫健康檢查

## 主要使用情境

在以下情況使用：

- 使用者要把 `00-Inbox` 某篇筆記轉正
- 使用者要把某篇既有筆記移到更正確的分類
- 使用者要補這篇筆記的關聯筆記與索引入口
- 使用者要把摘錄型筆記升級成可重用知識筆記
- `llm-wiki` ingest 完後，還要進一步把單篇內容整理成正式筆記

不要在以下情況使用：

- 還沒有本地筆記，只有原始來源
- 使用者要一次整理整個 `00-Inbox`
- 要批次重抓或重建大量來源

## 與 llm-wiki 的分工

`llm-wiki` 處理：

- 外部來源進 vault
- 路由到對的內容區
- 更新 `LLM-Wiki-Index`、`LLM-Wiki-Ingest-Log`、`Purpose`、`Overview`

`note-update` 處理：

- 單篇既有筆記升級
- 從 `00-Inbox` 轉正式筆記
- 類別重判
- 單篇移動
- 補 `[[wikilinks]]`
- 補分類 `index.md`
- 做最小必要的反向補鏈

一句話：

- `llm-wiki` 是把資料送進 vault
- `note-update` 是把某篇筆記整理成 vault 裡真正可用的節點

## 與 inbox-check 的分工

`note-update` 只處理：

- 一篇筆記
- 或極少數、使用者明確點名的幾篇筆記

如果使用者是在說：

- 「幫我整理整個 `00-Inbox`」
- 「把 Inbox 全部歸類」
- 「全部判斷哪些該進 Learning」

這是 `inbox-check`，不是 `note-update`。

## Control Plane

更新任何筆記前，優先遵守：

1. user instruction
2. `AGENTS.md`
3. `SCHEMA.md`
4. 本 skill

若規則衝突，先遵守高優先層，並只做最小安全更新。

## Current Vault Structure

這個 skill 必須依據 **Pigo 現在的 vault 結構** 做分類，不要自己發明新內容樹。

### 暫存區

- `00-Inbox/`
  - 只放待整理或使用者明示先暫存的筆記
  - 一旦內容已整理完成，應移出

### Learning 正式區

- `08-Learning/01_AI-Agent/`
  - 適合 Agent、harness、Claude Code、Codex、MCP、multi-agent、tool use
- `08-Learning/02_Knowledge-Systems/`
  - 適合 Obsidian、Notion、NotebookLM、LLM Wiki、RAG、知識庫設計
- `08-Learning/03_Prompt-Context-Engineering/`
  - 適合 prompt、context engineering、system prompt、skill prompt
- `08-Learning/04_AI-Engineering-Tools/`
  - 適合 repo、產品、工具、framework、套件、CLI、模型平台
- `08-Learning/05_Research-Papers/`
  - 適合 paper、benchmark、eval、研究方法與 paper reading
- `08-Learning/07_Business-Finance/`
  - 適合商業、產業、公司策略、財經、投資
- `08-Learning/08_Creative-Applications/`
  - 適合寫作、簡報、設計、影音與內容生成
- `08-Learning/09_General-Learning/`
  - 適合課程、學習法、個人成長、健康生活與一般學習
- `08-Learning/90_Source-Inbox/`
  - 只放未萃取的 articles、twitter、youtube、news 來源材料
- `08-Learning/99_Maintenance/`
  - 只放匯入報告、分類紀錄、audit、legacy index

### 工作區

- `Lumentum/`
  - 與工作、客戶、專案、會議、供應鏈、週報直接相關的內容

## 分類原則

### 內容優先分類硬規則

分類筆記時，**先讀文章/筆記內容，再決定主題分類**。來源平台只能作為 `Source`、`source_url`、`tweet_id`、`video_id` 等追溯 metadata，不能作為預設分類依據。

禁止以下錯誤：

- 因為來源是 X / Twitter，就直接放 `08-Learning/90_Source-Inbox/twitter/`
- 因為來源是 YouTube，就直接放 `08-Learning/90_Source-Inbox/youtube/`
- 因為來源是 Substack / Blog，就只按文章媒介放 `08-Learning/90_Source-Inbox/articles/`

只有在內容本身的長期用途就是「來源平台歸檔、thread 集合、影片筆記、文章來源索引」時，才使用來源型資料夾。

真正要問的是：

- 這篇筆記未來會怎麼被找回？
- 它解決的是哪一類知識問題？
- 它應該掛在哪個主題脈絡下才最容易重用？
- 如果移除來源平台資訊，只看內容本身，它最像哪一類知識？

### 預設判斷規則

- 來源是 YouTube，但主題是方法論或 workflow：
  - 優先考慮對應 topic-first 目標，例如 `08-Learning/01_AI-Agent/` 或 `08-Learning/02_Knowledge-Systems/`
  - 不一定留在 `08-Learning/90_Source-Inbox/youtube/`
- 來源是 X，但主題其實是工具、框架、產品：
  - 優先考慮 `08-Learning/04_AI-Engineering-Tools/`
  - 不一定留在 `08-Learning/90_Source-Inbox/twitter/`
- 來源是 X / YouTube，但內容其實是 prompt、設計方法、簡報生成、創作 workflow：
  - 優先考慮 `08-Learning/03_Prompt-Context-Engineering/` 或 `08-Learning/08_Creative-Applications/`
- 來源是文章，但主題是某個 repo / tool：
  - 可直接進 `08-Learning/04_AI-Engineering-Tools/`
- 內容和 Lumentum 工作直接相關：
  - 進 `Lumentum/` 對應區，而不是 `08-Learning/`

### `08-Learning/` topic-first 的優先使用方向

當內容屬於「知識主題」而不是單純媒介歸檔時，優先放入對應主題資料夾。

常見方向：

- `01_AI-Agent/`
  - agent workflow
  - coding workflow
  - evaluation / harness / tooling methods
- `02_Knowledge-Systems/`
  - Obsidian / Notion / NotebookLM / LLM Wiki
  - RAG / knowledge-base design
- `03_Prompt-Context-Engineering/`
  - prompt pattern
  - system prompt
  - context engineering
- `04_AI-Engineering-Tools/`
  - 模型平台
  - AI 工具
  - NotebookLM / Claude / Codex / Gemini 類平台
- `05_Research-Papers/`
  - paper、benchmark、eval、研究法、知識工作流
- `08_Creative-Applications/`
  - 寫作、內容生成、發布工作流
- `07_Business-Finance/`
  - 商業或投資內容
- `09_General-Learning/`
  - 課程、學習法、健康、生活、習慣與一般學習

## Vault Index Usage

更新單篇筆記前，優先用 vault index，而不是直接掃全庫。

- Vault root:
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query tool:
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`

### Before Update

先查：

- `duplicate-candidates`
- `exact-source`
- `by-classification`

用途：

- 找 merge target
- 判斷是否已有正式版本
- 找同分類下最值得互連的候選筆記

### After Update

再查：

- `related-notes`
- `links-to`
- `links-from`

用途：

- 補 `## 關聯筆記`
- 檢查是否仍是 orphan
- 找最小必要的反向補鏈候選

### Fallback Rule

只有在以下情況才 fallback 到 `rg` 或直接掃檔：

- `query_vault.py` 不存在
- `notes.db` 暫時不可用
- index 結果不足以判斷分類、重複或連結

## Two-Phase Workflow

`note-update` 必須遵守和 `llm-wiki` 對齊的兩階段流程。

### Phase 1: Analysis Pass

先做判斷，不急著改檔。

至少判斷以下事情：

- 這篇筆記目前是摘錄、半成品，還是已有正式結構
- 它的正確目的地在哪裡
- 是否已有可合併的正式筆記
- 這篇應保留獨立頁，還是合併到既有頁面
- 是否需要補 `sources: []`
- 是否需要補 `Source`
- 是否需要寫入 `## 關聯筆記`
- 是否需要更新哪些 `index.md`
- 是否需要最小反向補鏈

### Phase 2: Generation Pass

分析完成後才真正改檔。

這一階段包含：

- 重寫內容
- 補 frontmatter
- 移動檔案到正確類別
- 更新分類索引
- 視需要更新來源區索引或 Inbox 入口
- 補最小必要的反向連結

## Duplicate Resolution Policy

若發現來源重複、內容高度重疊，或 vault 已有等效正式筆記，優先做合併，而不是再生成競爭版本。

判斷原則：

- 同來源、同主題、內容高度重疊：
  - 合併到既有正式筆記
- 同主題但角度不同、用途不同：
  - 保留獨立頁，但補強互連

合併時要：

- 保留來源追溯
- 保留新增的有效補充內容
- 避免同主題留下兩篇平行正式版

## Formalization Standard

升級後的筆記，應該從「摘錄」變成「可重用知識」。

至少應包含：

- 清楚標題
- `Source` 或等效來源區塊
- 可追溯的 `sources: []` 或明確來源欄位
- `## 核心摘要`
- `## 關鍵知識點`
- `## 關聯筆記`

視內容性質可再補：

- `## 文章分析`
- `## 我的整理`
- `## 我會怎麼用這篇內容`
- `## 後續問題 / 待驗證點`
- `## 全文（繁中重寫）`

## Full-Item Preservation Rule

如果原始筆記本身是一頁內含多個完整條目，不要急著壓成單段 highlights。

常見情況：

- weekly report 首頁列多個 issue / audit / RMA
- 一頁同時列多個 customer case
- 一頁包含多個 action item / owner / due date

這種情況下應：

- 逐項整理
- 保留每個 item 的數字、owner、時程、風險與後續動作
- 不要只留高層摘要

## Relationship Rules

每次正式化，至少做這四件事：

1. 在正文內補必要的 `[[wikilinks]]`
2. 寫 `## 關聯筆記`
3. 更新目標分類的 `index.md`
4. 對 1 到 3 篇直接相關筆記做最小反向補鏈

不要失控擴張成大規模 wiki 重構。

## Index and Log Rules

### 必做

- 新目標分類若有 `index.md`，要把這篇筆記補進去
- 若筆記從 `00-Inbox` 移出，應更新 `00-Inbox/index.md` 的狀態或入口
- 若本次變更明顯影響 `llm-wiki` 可發現性，可同步補到：
  - `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
  - `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`

### 不要做

- 不要把 `index.md` 寫成操作日誌
- 不要把 `log.md` 寫成分類清單
- 不要每次都順手改一大片無關索引

## Minimal Backfill Policy

允許的最小補寫：

- 補一兩個直接相關 `[[wikilinks]]`
- 在同主題 `index.md` 補入口
- 在直接相關筆記裡補一行 related note

不允許：

- 掃全 vault
- 一次改十幾篇舊筆記
- 順手重命名整個分類
- 把單篇更新做成全庫重構

原則：

**讓這篇筆記變得可發現、可連回、可重用，就停。**

## Output Standard

- 一律使用繁體中文
- 保留來源追溯
- 若原文資訊不足，明確寫出不足，不要補造內容
- 檔名與標題以未來搜尋與重用為優先
- 不要把平台名稱誤當分類名稱

## Quick Checklist

完成前確認：

- 這篇是否已移到更合理的正式類別？
- 是否已從摘錄升級成可重用知識？
- 是否已補 `Source` 與追溯資訊？
- 是否已補 `sources: []` 或等效來源欄位？
- 是否已補 `[[wikilinks]]`？
- 是否已有 `## 關聯筆記`？
- 是否已更新目標 `index.md`？
- 若原本在 `00-Inbox`，是否已處理 Inbox 入口？
- 是否只做了最小必要的反向補鏈？

## Mini Lint After Update

完成單篇更新後，至少再檢查一次：

- 這篇是否仍是 orphan
- 是否與既有正式筆記重複
- 是否已被正確索引收錄
- 是否缺少最重要的 2 到 5 個關聯頁
- 是否有明顯 stale wording 應順手修正

若 vault index 可用，優先用：

- `duplicate-candidates`
- `related-notes`
- `links-to`
- `links-from`

## Example

情境：

- 一篇放在 `00-Inbox/` 的筆記
- 來源是 X 或 YouTube
- 但主題其實是 Obsidian workflow、AI engineering、prompt 方法論、repo 工具分析，或 Lumentum 工作內容

正確做法：

- 不要機械式依來源平台歸類
- 先判斷它在 Pigo vault 裡的長期用途
- 再移到：
  - `08-Learning/01_AI-Agent/...`
  - `08-Learning/02_Knowledge-Systems/...`
  - `08-Learning/03_Prompt-Context-Engineering/...`
  - `08-Learning/04_AI-Engineering-Tools/...`
  - `08-Learning/05_Research-Papers/...`
  - `08-Learning/07_Business-Finance/...`
  - `08-Learning/08_Creative-Applications/...`
  - `08-Learning/09_General-Learning/...`
  - `08-Learning/90_Source-Inbox/...`
  - `Lumentum/...`
- 重寫成正式知識筆記
- 補上與現有主題的關聯
- 更新對應索引

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical note-update Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/note-update/SKILL.merged.md
- skills/note-update/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
