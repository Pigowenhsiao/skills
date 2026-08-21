---
name: weekly-summary
description: Use when ingesting one or more weekly report files into Pigo's Obsidian vault, especially Lumentum SAG or TAK weekly updates, when the output should be page-by-page notes with English slide titles retained, Traditional Chinese rewritten content, structured extraction for table-like pages, summary extraction for narrative pages, and no Notion sync.
---

# Weekly Summary

## Description

`weekly-summary` 用來把週報、月報或同型工作簡報整理成逐頁可追溯的 Obsidian 筆記，保留英文頁標、以繁體中文重寫內容，並依頁面型態決定要做結構化整理、逐項完整轉寫，或摘要式整理。

## Core Use

這個 skill 用來把「單份或整批週報」整理成可累積的 Obsidian 工作知識，而且是逐頁整理，不是只做整份摘要。

目前預設目標是 Pigo 的 Lumentum 週報工作流：

- 來源目錄：
  - `C:\Users\hsi67063\Box\3DS Quality Taiwan\Pigo\Weekly report\SAG Weekly report`
- Obsidian vault：
  - `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- 輸出目錄：
  - `Lumentum/Weekly Reports/<year-or-fiscal-year>/`

## Vault Index Usage

`weekly-summary` 應先用 vault index 取得跨週脈絡，再決定哪些內容值得回填。

- Vault root：
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian`
- Query tool：
  `C:\Users\hsi67063\Box\00-home-pigo.hsiao\VBA\Pigo_Obsidian\.vault-index\query_vault.py`

### Before Ingest

先查：

- `fts`
- `by-classification`
- 必要時用 `related-notes`

用途：

- 找 recurring issue / customer / topic 的歷史筆記
- 確認該週報最可能回填到哪些既有頁面
- 找同 team、同分類下的週報與知識頁

### After Ingest

再查：

- `related-notes`
- `links-to`
- `links-from`

用途：

- 找 issue / customer / topic 回填候選
- 判斷是否值得建立 trend note / comparison note
- 檢查本次週報是否仍孤立於既有知識頁之外

### Fallback Rule

只有在以下情況才 fallback 到 `rg` 或直接掃檔：

- `query_vault.py` 不存在
- `notes.db` 暫時不可用
- index 查不到足夠的 cross-week 脈絡

## Compiled Knowledge Update

`weekly-summary` 不只是在 vault 裡新增一份週報筆記，也是在把新的工作訊息編譯回既有 wiki。

處理週報時要有這個順序：

1. 先整理出當週逐頁筆記
2. 再判斷哪些內容值得最小回填到既有知識頁
3. 只更新直接相關的 issue / customer / topic 頁面，不做大規模重構

原則：

- 週報筆記是當週原始紀錄層
- issue / customer / topic 頁面是跨週累積知識層
- 不要每次都從原始週報重新找脈絡

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

### D. 混合總覽頁面

若頁面雖然看起來像 overview / update page，但同一頁內其實包含多個完整 issue、audit、system improvement、RMA 或 action item，則不能只抓紅字或高層摘要。

這類頁面要：

- 逐項保留每個區塊的完整內容
- 依原頁項目拆成 `### 一、...`、`### 二、...` 等段落
- 保留 owner、數字、客戶、時程、風險與後續動作
- 不可只留下 `summary / highlights / updates in red`

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

### Structured Full-Item Page Variant

若頁面不是典型表格，但一頁內含多個完整條目，輸出格式仍應採結構化寫法，且每個條目都要完整保留：

- `## Page N - <English Title>`
- `### 頁面主題`
- `### 一、<Item 1>`
- `### 二、<Item 2>`
- `### 三、<Item 3>`

這種情況下：

- 不可只保留紅字更新
- 不可壓成單段摘要
- 不可把條目內容折疊成一句結論
- 應把每個 item 的背景、現況、數字、owner、風險、next step 寫完整

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
4. ingest 前先用 vault index 查 recurring issue / customer / topic 歷史
5. 逐頁判斷屬於：
   - 結構化頁面
   - 一般內容頁面
   - 跳過頁面
6. 依頁面類型輸出筆記
7. 將所有保留頁面合併成單一週報筆記
8. 重建 `Lumentum/index.md`
9. 更新 `Lumentum/log.md`
10. 重建 `llm-wiki` 關聯索引：
   - `Lumentum/Issues/index.md`
   - `Lumentum/Customers/index.md`
   - 各 issue key / customer key 關聯頁
11. 重新建置整個 vault 的 `graphify-out/`
12. 寫入對應 `STATUS_*.md`

## Significance Threshold for Cross-Page Updates

不是每一個週報 item 都值得回填到既有頁面。

只有在符合以下情況時，才做最小 cross-page update：

- recurring issue，已跨多週持續追蹤
- customer escalated issue
- audit finding / CAPA / system improvement 會跨週演進
- KPI 趨勢已形成可比較的脈絡
- 新週報明確推翻或更新了既有說法

若只是單週短暫 update，保留在當週週報筆記即可。

## Derived Analysis Can Be Filed Back

若整理週報的過程中產生可重用分析，這些結果不應只留在 chat 或單次摘要中。

可回寫的內容包括：

- issue evolution comparison
- customer-to-customer handling comparison
- trend note
- recurring problem synthesis

若分析結果本身有長期價值，可建立獨立筆記，並從當週週報與相關主題頁面連回去。

## Optional Weekly Health Check

完成 ingest 後，可做一輪最小 health check：

- 是否有 recurring issue 已值得獨立成頁但還沒有頁面
- 是否有 customer / issue 頁面應連到本週更新但尚未連結
- 是否有 stale claim 應被本週資料更新
- 是否有 data gap 值得下週補查或向團隊追問

這不是全域 lint，只是針對本次週報相關主題做比例適當的維護。

## Index and Log Roles

- `index.md`：內容導航用，讓人或 agent 知道有哪些週報與知識頁可讀
- `log.md`：時間序列用，記錄本次 ingest、修正、補寫與重要處理結果

不要把 `index.md` 寫成流水帳，也不要把 `log.md` 當成分類目錄。

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
