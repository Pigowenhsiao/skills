---
name: inbox-check
version: 2.2.0-darwin
description: >
  Use when multiple notes in 00-Inbox should be processed, or when the user asks in
  plain language to clean up, sort, or triage the inbox. This skill owns batch inbox
  scanning, safe routing, and deferred-item reporting, not single-note deep
  formalization. Triggers:
  EN: "triage the inbox", "clean up the inbox", "sort my notes", "empty inbox", "file my notes", "process the inbox".
  IT: "smista l'inbox", "svuota l'inbox", "ordina le note", "triage dell'inbox", "processa l'inbox".
  FR: "trier la boite de reception", "vider l'inbox", "classer mes notes".
  ES: "clasificar la bandeja de entrada", "vaciar el inbox", "ordenar mis notas".
  DE: "Inbox sortieren", "Inbox leeren", "Notizen einordnen".
  PT: "triagem da inbox", "esvaziar a inbox", "organizar minhas notas".

  Language policy (inherits llm-wiki v3.1.0-darwin absolute policy B): All triage reports, suggestions, file move notes, and review comments must be Traditional Chinese (zh-TW, Taiwan usage). Run OpenCC s2twp post-processing on any agent-generated text before commit.
author: Pi Port、Darwin-2.0 優化
license: MIT
---

# Inbox Check — Darwin-2.0 Edition (v2.1.0)

## 一句話原則

**Capture 優先 → 分類排程 → 雙評委驗證 → 顯性人工卡口；搬錯比不搬更糟，低信心時留在 Inbox。**

---

## Folder Context Before Placement

Before creating, moving, reclassifying, or updating any durable note, study the local folder context first so the note lands in the correct place.

Required reading order:
1. Read `12-Meta/vault-structure.md` — **取得最新 vault 分類結構**
2. Read the vault root `AGENTS.md`.
3. Read the `README.md` in the candidate destination folder when it exists.
4. Walk upward from the candidate destination folder to the vault root and read each available parent `README.md`.
5. When comparing multiple candidate folders, read each candidate folder's local `README.md` before choosing.


**Topic-first 分類原則**：
- 來源平台（YouTube、Twitter、x-note）**不作為一級分類**
- 根據筆記內容主題分類到對應 topic folder
- 例：Claude Code 相關 → `08-Learning/01_AI-Agent/`，財經新聞 → `08-Learning/07_Business-Finance/`

Placement rules:
- Treat `AGENTS.md` and `vault-structure.md` as the global control plane and folder `README.md` files as local placement contracts.
- Use folder `README.md` content to understand purpose, accepted note types, naming conventions, index expectations, and sensitive-content boundaries.
- If a folder has no `README.md`, do not invent rules for it. Infer conservatively from `AGENTS.md`, nearby `index.md`, existing notes, and the user's explicit instruction.
- If folder guidance conflicts, follow this priority: user instruction, vault root `AGENTS.md`, `vault-structure.md`, nearest folder `README.md`, parent folder `README.md`, then this skill.
- If the correct folder is still ambiguous after reading context, pause and ask Pigo instead of filing the note into a guessed location.

Always respond to the user in their language. Match the language the user writes in.

---

## Hard Rules（達爾文 2.0 強化版）

### 嚴禁軟化措辭（Actionable Specificity 強制執行）

以下五類措辭全部禁止。出現三處以上，該分類決策評分上限為 5 分；本文件本身不得出現任何一處：

| 禁止措辭 | 說明 |
|---|---|
| 「建議」 | 改成明確指令或不提 |
| 「可以考慮」 | 改成具體行動或不提 |
| 「根據情況」 | 改成具體分支判斷 |
| 「靈活把握」 | 改成明確定義的觸發條件 |
| 「視情況而定」 | 改成 if-then-else 結構 |

### 失敗模式編碼（Failure Mechanism Encoding）

每個分類決策步驟必須寫：「如果 X 發生就做 Y；否則做 Z」的明確分支。

- **禁止**只寫「把筆記放到正確位置」而不寫「什麼情況下會放錯」
- **禁止**只寫「檢查目的地是否存在」而不寫「目的地不存在時的處理」
- 若某步驟確實無需失敗分支，必須寫「（此步驟無已知失敗模式）」

### 高風險行動黑名單（High-Risk Action Blacklist）

每個 triage 工作流必須有獨立章節 `## 禁止事項` 明確列出：

- 不得刪除筆記（只能搬遷）
- 不得在目的地未確認前搬遷筆記
- 不得在單輪內做多個高風險分類決策
- 不得跳過 `status: inbox` → `status: filed` 的 frontmatter 更新
- 不得忽略「是否已存在類似筆記」的檢查

---

## 達爾文 2.0 評分標準（9 維）

對每個 triage 分類決策，依以下 9 維評估。最低維度優先避免。

| # | 維度 | 說明 | 評分（1-10） |
|---|---|---|---|
| 1 | **意圖清晰度** | 筆記標題能一眼看出「這篇是什麼」，不模糊、不過長 | |
| 2 | **來源完整性** | 含 `sources[]` frontmatter；原文 URL 可達；抓取時間記錄 | |
| 3 | **內容密度** | 核心摘要 < 200 字涵蓋要點；無填充廢話；行動項目有明確歸屬 | |
| 4 | **組織結構** | Heading 層級合理；資訊順序符合認知邏輯；wikilinks 正確 | |
| 5 | **可執行具體性** | 分類決策有 if-then-else；禁止五類軟化措辭；無模糊表述 | |
| 6 | **失敗模式編碼** | 有獨立章節描述「什麼情況下會放錯、放錯了怎麼救」 | |
| 7 | **交叉連結** | 至少三個 outbound wikilinks；無孤立頁面 | |
| 8 | **語言一致性** | 全篇繁體中文（zh-TW）；無簡中殘留（OCR 後必校對） | |
| 9 | **高風險行動黑名單** | 有獨立 `## 禁止事項` 章節且覆蓋完整 | |

### 維度評分標準（1-10）

| 分數 | 意義 |
|---|---|
| 10 | 該維度無可改進空間 |
| 8-9 | 接近完美，少量細節可微調 |
| 6-7 | 有明顯改進空間但不影響使用 |
| 4-5 | 存在顯著缺陷，需盡快修正 |
| 1-3 | 幾乎失效，優先重寫該維度 |

### 維度相關簇

失敗模式、分類邏輯、wikilinks 三維不是獨立維度，是**一簇**。改一個會帶動相鄰的。

---

## 雙評委驗證流程（Darwin-2.0）

### 核心原則

- **多評委獨立審查**：每個高風險分類決策由兩個獨立評委同時評估
- **共識分數才算數**：兩個評委的共識分數才作為最終分數
- **評委不復用**：下一輪啟動兩個全新評委，避免錨定效應（anchoring effect）
- **早停機制**：單輪漲幅 < 1 分，自動停手，不強行繼續分類

### 驗證步驟

```
Step 1: 分類決策草稿（分析 → 目的地建議）
Step 2: 評委 A（獨立）評 9 維 → 給出共識分數與最低維度
Step 3: 評委 B（獨立）評 9 維 → 給出共識分數與最低維度
Step 4: 比對 A/B 的最低維度是否一致
         → 一致：接受該維度為優先避免目標
         → 不一致：取較低分維度 + 參考另一評委次低維度
Step 5: 🔴 CHECKPOINT（顯性人工卡口）
         → 使用者確認是否接受當前分類決策
Step 6: 若使用者確認 → 執行搬遷 → 回到 Step 2 驗證
Step 7: 🛑 STOP（漲幅 < 1 分 → 早停）
```

### 顯性人工卡口（Human-in-the-Loop）

| 符號 | 意義 | 動作 |
|---|---|---|
| 🔴 | CHECKPOINT | 暫停，等使用者確認後才繼續 |
| 🛑 | STOP | 漲幅低於閾值，流程終止 |

每個 🔴 都是顯性人工介入點。流程能自動跑，但關鍵決策永遠交回給人。

---

## 反例黑名單（Darwin-2.0 實戰總結）

以下八條為 `inbox-check` 特有的實戰反模式，寫入本 SKILL.md 的同時，也嚴禁在任何 triage 產出中出現：

### 1. 同一個 agent 又分類又審查
單一 agent 同時負責分類決策和 quality review。分類結果不可信。

**正確做法**：明確區分「執行 triage」與「reviewer」的職責邊界。

### 2. 為湊分而在 MOC 裡塞冗餘
在 `## Notes` 段落填充重複的 wikilinks 或無效字元。降低內容密度維度分數。

**正確做法**：每個 MOC 條目必須有獨立資訊價值，無重複、無填充。

### 3. 跳過目的地存在性檢查
沒有確認目標資料夾存在就直接搬遷筆記。

**正確做法**：每個搬遷前必須正則比對目標路徑存在性，目的地不存在時 🔴 暫停。

### 4. 一輪內做多個高風險分類決策
同時改「目的地 A」和「目的地 B」兩個維度，無法判斷哪個搬遷有效。

**正確做法**：單輪只執行一個高風險分類決策，驗證後再執行下一個。

### 5. 乾跑模式比例超過 30%
連續三次 checkpoint 都選擇「跳過實際行動，只做文本修飾」。

**正確做法**：三個連續 checkpoint 中至少一個要有實際檔案系統動作（搬遷/創建資料夾/更新 index），否則觸發告警。

### 6. 靜默跳過異常
某個搬遷失敗但只在 log 裡寫一行，不通知使用者。

**正確做法**：任何搬遷失敗都必須寫入 `00-Inbox/log.md` 的 `issues` 區塊，並在 daily digest 中標記。

### 7. 忽視維度相關簇
只看最低維度分數，不考慮它是否與其他維度形成叢集。

**正確做法**：當最低維度屬於失敗模式/分類邏輯/wikilinks 簇時，優先改該簇，單輪收益最大化。

### 8. 忽視軟化措辭超標
在 `## 分類決策` 段落中出現五類禁止措辭（「建議」「可以考慮」等），卻沒有替換為具體指令。

**正確做法**：每次寫完分類決策章節後，用以下正則檢查：
```
建議|可以考慮|根據情況|靈活把握|視情況而定
```
若出現 ≥ 3 次，該決策評分上限為 5 分。

---

## Boundary with `note-update`

`inbox-check` owns **batch inbox triage**.

- It scans multiple notes and decides which ones can be safely filed now.
- It leaves ambiguous or high-touch notes in `00-Inbox/` when needed.
- It may identify notes that deserve deeper single-note formalization.

`note-update` owns **one-note-at-a-time formalization**.

- Do not perform `note-update`-grade deep rewriting inline for every inbox note.
- Do not turn a batch triage request into a full single-note editorial pass.
- When a note should be formally upgraded after triage, surface it as follow-up guidance instead of assuming the dispatcher will auto-run another skill.

### Follow-up format for deeper single-note work

Use this advisory section when triage finds notes that should later go through `note-update`:

```markdown
### Recommended follow-up skill
- **Skill**: note-update
- **Reason**: This note needs deep formalization, not just safe routing
- **Context**: [[Note Title]] — suggested destination: 03-Resources/Topic/
```

---

## User Profile

Before processing any notes, read `Meta/user-profile.md` to understand the user's context, active projects, and preferences. Use this to make better filing decisions.

---

## Vault Index Usage

使用 vault index 來減少猜測、快速定位：

- Vault root：`E:\obsidian\PigoVault`
- Query tool：`E:\obsidian\PigoVault\.vault-index\query_vault.py`

### Before Filing Each Note

必查：
- `duplicate-candidates`
- `by-classification`
- 必要時使用 `related-notes`

用途：
- 避免重複分類錯誤
- 發現可橫向連結的現有筆記
- 探索相似的領域筆記

### During Batch Triage

可用：
- `fts`
- `links-to`
- `links-from`

用途：
- 發現已存在的相關筆記
- 確認wikilinks 更新範圍
- 確保分類 MOC / 索引現狀

### Fallback Rule

僅使用以下 fallback 搜尋工具時：
- `rg` 全域搜尋
- 目的地資料夾 walk

---

## Inter-Agent Coordination

> **You do NOT communicate directly with other agents. The dispatcher handles all orchestration.**

When you detect work that another agent should handle, include a `### Suggested next agent` section at the end of your output.

### When to suggest another agent

- **Architect** — **MANDATORY.** Before filing any note, classify the missing-destination case correctly:
  - If the parent area or project already exists in `Meta/vault-structure.md` and only a low-risk obvious subfolder is missing, you may create that local destination yourself.
  - If a new area, new project structure, new MOC system, new `_index.md`, new template family, or any architecture-level design is needed, you MUST leave the note in `00-Inbox/` and include a `### Suggested next agent` for the Architect explaining the missing structure.
- **Librarian** — when you find duplicates, broken links, or frontmatter issues that go beyond this triage session
- **Connector** — when you file a batch of notes that seem highly interconnected and should be cross-linked
- **Seeker** — when you need to verify if a similar note already exists before creating wikilinks

### Output format for suggestions

```markdown
### Suggested next agent
- **Agent**: architect
- **Reason**: Destination folder does not exist for "Machine Learning" notes
- **Context**: 3 notes left in 00-Inbox/. Suggest creating 08-Learning/AI-Papers/ with sub-folders and MOC.
```

---

## Standard Triage Workflow（含失敗分支）

### Mode Extensions (Autonomy-First, Non-Blocking)

#### Smart Batch
1. Scan all inbox notes and identify natural groupings (same project, same topic, same day, same person)
2. Classify each cluster by filing risk (low-risk clear destination vs ambiguous/unsafe destination)
3. File low-risk clusters immediately, ensuring related notes are cross-linked
4. Leave ambiguous or unsafe clusters in `00-Inbox/` with explicit reasons, then continue the rest of the batch
5. End with a cluster summary report (processed clusters, deferred clusters, and why)

#### Priority Triage
1. Scan all inbox notes
2. Classify by urgency and filing risk:
   - **Critical**: tasks with deadlines today/tomorrow, flagged items, messages requiring response
   - **High**: project-related notes for active projects, time-sensitive references
   - **Medium-risk**: normal-priority notes with ambiguous or conflicting destinations
   - **Low**: quotes, lists, archivable content with clear low-risk destinations
3. File `Critical` and `High` items first, ensuring action items are visible
4. Also file clear low-risk items in the same run
5. Leave ambiguous and medium-risk items in `00-Inbox/` with reasons, mark them for review, and continue without asking to pause

#### Project Pulse
1. Complete triage actions first (file what is safe, defer what is unsafe)
2. Then analyze which projects/areas received the most new notes
3. Generate a project activity report as a reporting layer, never as a filing gate

---

### Step 1: Scan the Inbox 🔴

🔴 **Checkpoint：確認本次 triage 的範圍與優先順序**
- 列出所有 `00-Inbox/` 檔案
- 讀取每個檔案的 YAML frontmatter 與內容
- 建立 triage queue（按日期排序，最舊優先）
- 識別高風險分類（跨領域、多專案、含糊目的地）→ 🔴 報告給使用者確認

```python
# 失敗分支：若 vault-index query_vault.py 不可用
→ fallback: 使用 rg 全域搜尋 + 目的地資料夾 walk
→ 若目的地不存在：🔴 暫停，等使用者確認是否創建
```

### Step 2: Dual-Reviewer Classify & Route 🔴

🔴 **Checkpoint：雙評委驗證高風險分類決策**
- 評委 A（獨立）評 9 維 → 記錄共識分數與最低維度
- 評委 B（獨立）評 9 維 → 記錄共識分數與最低維度
- 比對 A/B 最低維度是否一致
- 一致則接受；不一致取較低分維度
- 🔴 展示評分結果，等使用者確認是否繼續

**分類路由表（9維評分前執行）：**

**⚠️ 重要原則：Topic-first 分類，來源平台（YouTube、Twitter）不作為一級分類。**

| 內容類型 | 目的地 | 評分維度重點 |
|---------|--------|------------|
| AI Agents / Claude Code | `08-Learning/01_AI-Agent/` | 主題分類 |
| AI Tools / Engineering | `08-Learning/04_AI-Engineering-Tools/` | 主題分類 |
| Papers / Research | `08-Learning/05_Papers/` | 主題分類 |
| Business / Finance / Economy | `08-Learning/07_Business-Finance/` | 主題分類 |
| Creative / Design | `08-Learning/08_Creative-Applications/` 或 `03_Design/` | 主題分類 |
| Prompt Engineering | `08-Learning/03_Prompt-Context-Engineering/` | 主題分類 |
| People / KOL | `08-Learning/05_People/` | 主題分類 |
| Meeting notes | `06-Meetings/{{YYYY}}/{{MM}}/` | 意圖清晰度、來源完整性 |
| Project-related | `01-Projects/{{Project Name}}/` | 交叉連結、內容密度 |
| Area-related | `02-Areas/{{Area Name}}/` | 組織結構、wikilinks |
| Reference material | `03-Resources/{{Topic}}/` | 可執行具體性、來源完整性 |
| Task/To-do | Extract to daily note or project | 行動項目明確性 |
| Archivable | `04-Archive/{{Year}}/` | 時間衰減評估 |
| Unclear | 留在 Inbox，標記 `Needs Review` | 含糊不安全 → 記錄原因後繼續 |

**分類前必讀**：`12-Meta/vault-structure.md` 取得最新 vault 分類結構。

```python
# 失敗分支：目的地資料夾不存在
→ 若為現有 area/project 下的低風險子資料夾：自行創建
→ 若為新 area / 新 project 結構 / 新 MOC：🔴 暫停，escalate to Architect
```

### Step 3: Pre-Move Checklist（每個 note）

在搬遷每個 note 前：

1. **驗證目的地存在** — 若不存在：🔴 暫停，等使用者確認
2. **檢查重複** — 搜尋目的地是否有標題或內容相似的筆記
3. **更新 frontmatter**：`status: inbox` → `status: filed`，加 `filed-date` 與 `location`
4. **創建 wikilinks**：People / Projects / Areas / 相關 notes
5. **提取行動項目**：確認任務已capture到相關 Daily Note 或 project note

### Step 4: Update MOC Files

在搬遷筆記後更新相關 MOC：

1. **檢查相關 MOC 是否存在**於 `MOC/`
2. **若有**：在適當章節加入新 note 的 wikilink
3. **若無**：評估是新 MOC 系統的需求還是僅搬遷問題。🔴 若需架構層級 MOC，escalate to Architect

### Step 5: Generate Daily Digest

完成 triage 後，產生摘要：

```
Triage Complete — {{date}}

Filed:
- "[[Note Title]]" -> 目的地/
- ...

MOCs Updated:
- MOC/Topic

Archive Candidates:
- [[Note]] — 上次更新 {{date}}

Needs Review（留在 Inbox，含原因）：
- "[[Note]]" — 原因：含糊目的地；safe routing 未建立

Stats: {{N}} notes filed, {{N}} MOCs updated, {{N}} links created
```

### Step 6: 🛑 Archive Candidates + Post-it

🛑 **早停檢查**：單輪漲幅 < 1 分則停止 further triage。

掃描 30+ 天未觸及的筆記：
1. 檢查 `date`、`updated`、檔案修改時間
2. 列出候選並標記原因
3. 回報給使用者確認，不要自動歸檔

### Step 7: Write Post-it（必填）

在 `Meta/states/sorter.md` 寫入狀態：

```markdown
---
agent: sorter
last-run: "{{ISO timestamp}}"
---

## Post-it

[最多 30 行：仍留在 inbox 的檔案、不確定的筆記與推理、觀察到的分類模式、快速成長的領域]
```

---

## 禁止事項

- 不要刪除筆記，只搬遷
- 不要在目的地未確認前搬遷筆記
- 不要在單輪內做多個高風險分類決策
- 不要跳過 `status: inbox` → `status: filed` 的 frontmatter 更新
- 不要忽略「是否已存在類似筆記」的檢查
- 不要在同一個 agent session 裡既執行 triage 又做 quality review（雙評委強制分流）
- 不要在分類決策章節使用「建議」「可以考慮」「根據情況」「靈活把握」「視情況而定」
- 不要在單輪內改多個維度
- 不要讓三個連續 checkpoint 都是乾跑（告警觸發實際檔案系統寫入）
- 不要靜默跳過搬遷失敗（必須寫入 issues 區塊）
- **不要使用來源平台（YouTube、Twitter、x-note）作為分類標準**
- **不要把新筆記放進 `90_Source-Inbox/`（已刪除）**