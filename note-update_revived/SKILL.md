---
name: note-update
description: Use when one existing note, especially a note in `00-Inbox`, should be upgraded into a formal vault note, moved into the correct category, linked to the current vault structure, indexed, and minimally backfilled into nearby notes without doing batch inbox triage or full-vault ingest.
version: 2.4.0-pigo
author: Hermes Agent
license: MIT
triggers:
  - "note-update"

---

所有輸出內容一律使用繁體中文。

# Note Update

## Vault 架構（2026-05-03 更新）

```
Pigo_Obsidian/
├── 00-Inbox/           # 新筆記預設放這裡（鐵則！）
├── 01-Projects/        # 專案
├── 02-Areas/           # 領域
├── 03-Resources/       # 資源
├── 04-Archive/         # 封存
├── 05-People/          # 人物
├── 06-Meetings/        # 會議
├── 07-Daily/           # 日記
├── 08-Learning/        # 學習（整理後的筆記）
├── 09-Article-Notes/   # 文章筆記
├── 10-LLM-Wiki/        # LLM Wiki 系統
├── 11-MOC/             # Map of Content
├── 12-Meta/            # 中繼資料
├── 13-Templates/       # 範本
├── 14-Skills/          # Skills 說明
├── 15-Docs/            # 文件
├── 16-Assets/          # 資產
├── 17-WorkNotes/       # 工作筆記
└── Learning/           # 舊位置，漸漸遷移到 08-Learning
```

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

## Description

`note-update` 是給 Pigo vault 的單篇筆記升級技能。

它的主要工作不是抓新來源，而是把**已經存在於 vault 裡的筆記**，尤其是 `00-Inbox/` 的半成品筆記，整理成可長期使用的正式知識筆記，並放到正確的 vault 類別。

這個 skill 的核心責任是：

- 讀懂現有筆記，而不是直接重寫
- 判斷該筆記應落到哪個正式類別（優先：`00-Inbox/` → `08-Learning/`、`09-Article-Notes/`、`10-LLM-Wiki/`）
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
- 更新 `10-LLM-Wiki/`、`00-Inbox/` 的索引

`note-update` 處理：

- 單篇既有筆記升級
- 從 `00-Inbox` 轉正式筆記
- 類別重判
- 單篇移動
- 補 `[[wikilinks]]`
- 補分類 `index.md`
- 做最小必要的反向補鏈

一句話：

- `llm-wiki` 是把資料送進 vault（預設放 `00-Inbox/`）
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

## Current Vault Structure（2026-05-03 更新版）

這個 skill 必須依據 **Pigo 現在的 vault 結構** 做分類。

### 預設目的地（鐵則）

| 情況 | 目的地 |
|------|--------|
| **新筆記或未整理** | `00-Inbox/` |
| **整理到正式區** | `08-Learning/`、`09-Article-Notes/`、`10-LLM-Wiki/` |

### 整理後的放置規則

| 內容類型 | 建議目錄 |
|----------|----------|
| 文章、部落格、長文 | `09-Article-Notes/` 或 `08-Learning/` |
| YouTube、影片 | `08-Learning/` |
| Repo、產品、工具 | `08-Learning/repos/` |
| 主題知識、方法論 | `08-Learning/notion-knowledge/` |
| X/Twitter thread（值得保留原文格式） | `08-Learning/twitter/` |
| 工作相關 | `17-WorkNotes/` 或 `01-Projects/` |
| 封存 | `04-Archive/` |

### `08-Learning/` 建議結構

```
08-Learning/
├── articles/        # 文章整理
├── repos/           # 工具、repo
├── youtube/         # 影片筆記
├── twitter/         # Twitter 存檔
├── notion-knowledge/ # 方法論、知識主題
│   ├── 02_AI工程/
│   ├── 03_模型_工具與平台/
│   ├── 04_提示詞/
│   ├── 05_學習研究/
│   └── ...
└── status/          # 系統狀態
```

## 分類原則（更新）

不要迷信來源平台。

真正要問的是：

- 這篇筆記未來會怎麼被找回？
- 它解決的是哪一類知識問題？
- 它應該掛在哪個主題脈絡下才最容易重用？

### 預設判斷規則

- 來源是 YouTube，但主題是方法論或 workflow：
  - 優先考慮 `08-Learning/notion-knowledge/`
- 來源是 X，但主題是工具、框架、產品：
  - 優先考慮 `08-Learning/repos/` 或 `08-Learning/notion-knowledge/`
- 來源是文章，但主題是某個 repo / tool：
  - 可直接進 `08-Learning/repos/`
- 內容和工作直接相關：
  - 進 `17-WorkNotes/` 或對應專案

## Vault Index Usage

更新單篇筆記前，優先用 vault index。

### Before Update

先查 vault 中的相關筆記，確認：
- 是否有重複內容
- 是否有可合併的目標
- 應該放到哪個分類

### After Update

確認：
- 是否已補必要的 `[[wikilinks]]`
- 是否已更新目標分類的 `index.md`
- 是否已處理 `00-Inbox` 入口（若原本在 Inbox）

## Two-Phase Workflow

`note-update` 必須遵守兩階段流程。

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
- 若本次變更明顯影響 `llm-wiki` 可發現性，可同步補到 `10-LLM-Wiki/` 的索引

### 不要做

- 不要把 `index.md` 寫成操作日誌
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

- [ ] 這篇是否已移到更合理的正式類別？
- [ ] 是否已從摘錄升級成可重用知識？
- [ ] 是否已補 `Source` 與追溯資訊？
- [ ] 是否已補 `sources: []` 或等效來源欄位？
- [ ] 是否已補 `[[wikilinks]]`？
- [ ] 是否已有 `## 關聯筆記`？
- [ ] 是否已更新目標 `index.md`？
- [ ] 若原本在 `00-Inbox`，是否已處理 Inbox 入口？
- [ ] 是否只做了最小必要的反向補鏈？

## Example

情境：

- 一篇放在 `00-Inbox/` 的筆記
- 來源是 X 或 YouTube
- 但主題其實是 AI engineering、prompt 方法論、repo 工具分析，或工作相關內容

正確做法：

- 不要機械式依來源平台歸類
- 先判斷它在 Pigo vault 裡的長期用途
- 再移到對應目錄（如 `08-Learning/`、`09-Article-Notes/`、`10-LLM-Wiki/`）
- 重寫成正式知識筆記
- 補上與現有主題的關聯
- 更新對應索引

## 禁止事項

- **絕對不要**把新筆記直接放到正式目錄（除非明確認知分類）
- 不要跳過 index 更新
- 不要生成沒有 source 溯源的頁面
- 不要過度強調分類而耽誤 capture

<!-- AGENT_SKILL_DEDUPE_NOTE -->
## Duplicate Consolidation

This is the canonical note-update Skill after Agent dedupe on 2026-04-29.
<!-- /AGENT_SKILL_DEDUPE_NOTE -->