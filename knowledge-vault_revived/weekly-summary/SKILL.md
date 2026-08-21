---
name: weekly-summary
description: Use when ingesting one or more weekly report files into Pigo's Obsidian vault, especially Lumentum SAG or TAK weekly updates, when the output should be page-by-page notes with English slide titles retained, Traditional Chinese rewritten content, structured extraction for table-like pages, summary extraction for narrative pages, and no Notion sync.
---

# Weekly Summary


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
- If a folder has no `README.md`, do not invent rules for it. Infer conservatively from `AGENTS.md`, nearby `index.md`, existing notes, and the user's explicit instruction.
- If folder guidance conflicts, follow this priority: user instruction, vault root `AGENTS.md`, nearest folder `README.md`, parent folder `README.md`, then this skill.
- If the correct folder is still ambiguous after reading context, pause and ask Pigo instead of filing the note into a guessed location.

## Core Use

這個 skill 用來把「單份或整批週報」整理成可累積的 Obsidian 工作知識，而且是逐頁整理，不是只做整份摘要。

目前預設目標是 Pigo 的 Lumentum 週報工作流：

- 來源目錄：
  - `C:\Users\hsi67063\Box\3DS Quality Taiwan\Pigo\Weekly report\SAG Weekly report`
- Obsidian vault：
  - `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- 輸出目錄：
  - `Lumentum/Weekly Reports/<year-or-fiscal-year>/`

## When To Use

- 使用者要把整個週報資料夾批次匯入 wiki
- 使用者要把單份 `pptx` / `pdf` 週報整理成標準筆記
- 需要保留逐頁脈絡，而不是只留下高層摘要
- 匯入後需要重建 `Lumentum/index.md` 與 `Lumentum/log.md`
- 已有週報筆記被錯分成錯的 team/title，需要批次修正
- 需要保留週次索引，即使來源檔損壞也不能讓時間線斷掉

不要用在：

- 一般學習內容整理
- 非週報類的 meeting minutes / article / Twitter thread
- 需要正式管理報告文風的重寫任務

## Output Rules

### 1. 英文標題保留

- 每一頁保留原始英文頁面標題
- 英文標題可以直接作為：
  - `## Page N - <English Title>`
  - `### 頁面主題`

### 2. 內容全部改寫成繁體中文

- 內文不可直接貼整段英文
- 內容必須改寫成可讀的繁體中文
- 可保留的英文僅限：
  - 專有名詞
  - 客戶名
  - 料號
  - 製程名
  - 縮寫，例如 `RMA`、`BI`、`8D`、`FA`

### 3. 不同步 Notion

- `weekly-summary` 只輸出到 Obsidian
- 不建立 Notion input
- 不同步 Notion database
- 若使用者要求 Notion，應明確指出那是 `llm-wiki` 或其他 Notion skill 的範圍，不是本 skill 的標準流程

### 4. 不是每一頁都要保留

- 若頁面內容只有一句話、只有分隔用途、或只是空白標題頁，直接跳過
- 典型例子：
  - `Backup Slide`
  - 單純章節分隔頁
  - 幾乎沒有可用資訊的圖像頁

## Page Classification

在整理每一頁前，先判斷頁面屬於哪一類：

### A. 結構化頁面

符合以下任一特徵時，視為結構化頁面：

- 有明確表格
- 有固定欄位
- 有 action matrix / disposition table
- 有 8D / CAPA / Risk Assessment / Problem Statement 這種框架
- 有 lot / owner / date / risk / corrective action 這類可拆欄位資訊

這類頁面要整理成結構化筆記，不只做摘要。

### B. 一般內容頁面

若頁面有實質內容，但不是明確表格型，則整理成摘要模式：

- `### 摘要`
- `### 報告細節`
- `### 應注意事項`

### C. 跳過頁面

若頁面只有一句話、只有標題、或只有過場用途，則不需要寫進筆記。

## Structured Page Format

對於結構化頁面，輸出格式以這種風格為準：

- `## Page N - <English Title>`
- `### 頁面主題`
- `### 一、...`
- `### 二、...`
- `### 三、...`

欄位名稱可以依原頁內容調整，但要維持可掃讀的結構化格式。

常見欄位包括：

- `一、狀態概述`
- `二、問題分類`
- `三、流程 / 進度框架`
- `四、問題主題`
- `五、問題描述`
- `六、影響批次`
- `七、根因分析`
- `八、風險與影響評估`
- `九、暫時圍堵措施`
- `十、改善措施`
- `十一、預防措施`
- `十二、負責人`

如果原頁是表格，也可以直接整理成中文表格，但內容仍要以繁體中文重寫。

## Summary Page Format

對於非表格型但有實質內容的頁面，輸出格式固定為：

- `## Page N - <English Title>`
- `### 頁面主題`
- `### 摘要`
- `### 報告細節`
- `### 應注意事項`

其中：

- `摘要`：講這頁在說什麼
- `報告細節`：保留數字、客戶、料號、時間點、結論
- `應注意事項`：指出風險、限制、需要回看原圖、或後續應追的點

## Workflow

1. 確認來源是否為週報檔案，辨識 `CY/FY + week`
2. 優先使用較完整的 `pptx`；若沒有，再使用 `pdf`
3. 以 `markitdown` 轉出可讀文字
4. 逐頁判斷屬於：
   - 結構化頁面
   - 一般內容頁面
   - 跳過頁面
5. 依頁面類型輸出筆記
6. 將所有保留頁面合併成單一週報筆記
7. 重建 `Lumentum/index.md`
8. 更新 `Lumentum/log.md`
9. 重建 `llm-wiki` 關聯索引：
   - `Lumentum/Issues/index.md`
   - `Lumentum/Customers/index.md`
   - 各 issue key / customer key 關聯頁
10. 重新建置整個 vault 的 `graphify-out/`
11. 寫入對應 `STATUS_*.md`

## Routing Rules

- `SAG Quality Weekly Update*` -> `SAG Quality`
- `SAG-TAK Quality Weekly Update*` -> `SAG-TAK Quality`
- `TAK Quality Weekly Update*` -> `TAK Quality`
- `Weekly SAG-Ops Report*` -> `SAG Ops`

輸出檔名格式：

- `CY25W10 - SAG Quality Weekly Update.md`
- `FY24W24 - TAK Quality Weekly Update.md`

年度資料夾規則：

- `CY25` -> `2025/`
- `FY24` -> `FY24/`

## Failure Handling

- 若來源檔是 `0 bytes` 或 `markitdown` 無法讀取：
  - 仍要建立 placeholder 筆記
  - frontmatter 保留 `source_file` / `source_path`
  - `extraction_confidence: failed`
  - 在內容中寫清楚失敗原因

## Bundled Script

批次匯入與修正使用：

`scripts/batch_ingest_lumentum_weeklies.py`

執行方式：

```powershell
python C:\Users\hsi67063\.codex\skills\weekly-summary\scripts\batch_ingest_lumentum_weeklies.py
```

如果要同步 Agent 版 skill，也要保持同一份腳本：

```powershell
python C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Agent\weekly-summary\scripts\batch_ingest_lumentum_weeklies.py
```

週報整理完成後，必須再執行：

```powershell
python C:\Users\hsi67063\.codex\skills\llm-wiki\scripts\build_lumentum_weekly_relation_index.py
python C:\Users\hsi67063\.codex\skills\weekly-summary\scripts\refresh_pigo_vault_graphify.py
```

注意：

- 目前 bundled script 仍可能輸出舊版高層摘要格式
- 若要完全自動化符合本規格，必須再把腳本重構為逐頁分類輸出

## Verification

完成後至少驗證：

- `Lumentum/Weekly Reports/` 下筆記數量是否合理
- 新產出的單份週報是否保留英文頁面標題
- 內文是否已改寫成繁體中文
- 結構化頁面是否使用 `一、二、三...` 的格式
- 非表格頁面是否使用 `摘要 / 報告細節 / 應注意事項`
- `Backup Slide` 這類單句頁面是否已被跳過
- `Lumentum/index.md` 是否可正常列出新筆記
- `Lumentum/log.md` 是否有本次匯入紀錄
- `Lumentum/Issues/index.md` 是否已更新
- `Lumentum/Customers/index.md` 是否已更新
- `graphify-out/graph.json` 是否已更新
- `graphify-out/graph.html` 是否已更新
- `graphify-out/GRAPH_REPORT.md` 是否已更新

## Current Implementation Note

這個 skill 在 2026-04-09 更新為「逐頁整理」版本。核心原則是：

- 保留英文標題
- 內文改寫為繁體中文
- 表格型頁面做結構化整理
- 非表格型頁面做摘要整理
- 單句分隔頁直接跳過
- 不同步 Notion

若之後要支援其他公司或其他週報格式，應先擴充腳本與 routing，而不是直接改掉現有的 Lumentum 規則。

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical weekly-summary Skill after Agent dedupe on 2026-04-29.

Archived duplicate variants:
- Obsidian_skill_set/weekly-summary/SKILL.merged.md
- skills/weekly-summary/SKILL.merged.md
<!-- /AGENT_SKILL_DEDUPE_NOTE -->
