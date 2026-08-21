# LLM Wiki Architecture for PigoVault

這份文件描述 `PigoVault` 中 `10-LLM-Wiki` 的實際架構，而不是通用的獨立 wiki 模型。

## 核心原則

- `10-LLM-Wiki/` 是 runtime package，不是內容主樹
- 新來源、新文章、新筆記預設先進 `00-Inbox/`
- 正式知識內容整理後寫入既有 vault 結構
- `08-Learning/` 是 topic-first 學習知識主儲區
- `09-Article-Notes/` 是主題化 article note、source note 與 hub 系統
- `03-Resources/Concept-Hubs/` 是跨域 canonical concept wrapper 區
- `17-WorkNotes/` 保留工作知識與原始工作脈絡

## 實際架構

```text
PigoVault/
|- 00-Inbox/                          # 新輸入、待整理內容、預設 capture 入口
|- 01-Projects/                       # 跨域專案的精煉輸出
|- 02-Areas/                          # 穩定責任區入口，不作大量內容主儲區
|- 03-Resources/
|  `- Concept-Hubs/                   # 跨域概念入口
|- 04-Archive/                        # 封存內容
|- 05-People/                         # 人物與關係索引
|- 06-Meetings/                       # 正式會議紀錄
|- 07-Daily/                          # 每日記錄
|- 08-Learning/                       # topic-first 學習主儲區
|  |- 01_AI-Agent/
|  |- 02_Knowledge-Systems/
|  |- 03_Prompt-Context-Engineering/
|  |- 04_AI-Engineering-Tools/
|  |- 05_Research-Papers/
|  |- 07_Business-Finance/
|  |- 08_Creative-Applications/
|  |- 09_General-Learning/
|  |- 90_Source-Inbox/
|  `- 99_Maintenance/
|     `- status/
|        |- LLM-Wiki-Index.md
|        `- LLM-Wiki-Ingest-Log.md
|- 09-Article-Notes/                  # article/source/hub 分類系統
|- 10-LLM-Wiki/                       # runtime 規格與 references
|- 11-MOC/                            # 全 Vault 導航
|- 12-Meta/                           # 規則、狀態、報告、治理文件
|- 13-Templates/
|- 14-Skills/
|- 15-Docs/
|- 16-Assets/
`- 17-WorkNotes/                      # 工作知識與原始工作筆記
```

## 與舊模型的差異

這個 vault 不再使用以下舊結構作為正式內容目的地：

- `10-LLM-Wiki/index.md`
- `10-LLM-Wiki/log.md`
- `10-LLM-Wiki/00-Inbox/`
- `10-LLM-Wiki/entities/`
- `10-LLM-Wiki/concepts/`
- `10-LLM-Wiki/comparisons/`
- `10-LLM-Wiki/queries/`
- `08-Learning/articles/`
- `08-Learning/youtube/`
- `08-Learning/repos/`
- `08-Learning/status/`

如果發現新內容被寫到這些位置，應視為結構錯誤並回收。

## 三層模型

### Layer 1: Capture

來源剛進來、尚未整理完成時，預設放：

- `00-Inbox/`

適用情境：

- 新文章或新來源首次 ingest
- 來源不完整
- 還無法判斷類型
- 使用者明示先暫存不要正式歸檔

### Layer 2: Canonical Knowledge

完成整理後，再依用途進入既有類別：

- 學習型知識 -> `08-Learning/<topic-first 子目錄>/`
- 未萃取來源材料 -> `08-Learning/90_Source-Inbox/`
- article note / source note / hub -> `09-Article-Notes/<kind>/<topic>/`
- concept wrapper -> `03-Resources/Concept-Hubs/`
- 工作責任區入口 -> `02-Areas/Work/`
- 工作原始脈絡或歷史材料 -> `17-WorkNotes/`
- 正式會議紀錄 -> `06-Meetings/`

### Layer 3: Runtime and Rules

`10-LLM-Wiki/` 本身只負責：

- skill 規則
- reference templates
- workflow guidance

它不直接承載正式知識內容。

## 導覽入口

每次使用 `10-LLM-Wiki` 前，優先讀這些入口：

1. `00-Inbox/index.md`
2. `08-Learning/index.md`
3. `09-Article-Notes/index.md`
4. `12-Meta/vault-structure.md`
5. `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
6. `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`

必要時再讀：

- 對應 `08-Learning/<topic>/index.md`
- 對應 `09-Article-Notes/<kind>/README.md`
- `09-Article-Notes/Vault-Classification-Index.md`
- `11-MOC/Index.md`

## 內容更新責任

每次 ingest 或結構調整後，至少要同步：

- 正確的 canonical 筆記檔
- 對應目錄的 index 或 README
- `00-Inbox/index.md` 或 `00-Inbox/log.md`
- `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md`
- `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md`

## 結構錯誤判定

以下情況都應視為錯誤：

- 正式筆記被寫回 `10-LLM-Wiki/`
- 新文章未經使用者要求就跳過 `00-Inbox/`
- 筆記仍連到不存在的舊分類，例如 `08-Learning/articles/`、`08-Learning/youtube/`、`08-Learning/repos/`、`08-Learning/papers/` 或 `08-Learning/videos/`
- 有新內容只有主筆記，沒有更新 `LLM-Wiki-Index` 或 `Ingest-Log`
- 大量暫存內容長期滯留在 `00-Inbox/` 沒有整理計畫

## 一句話總結

在 `PigoVault` 中，`10-LLM-Wiki` 是整理與規則層；**新來源先進 `00-Inbox`**，整理後再回收到 `08-Learning`、`09-Article-Notes`、`03-Resources`、`17-WorkNotes` 與既有 vault 骨架。
