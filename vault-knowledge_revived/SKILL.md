---
name: vault-knowledge
description: "Vault 每日知識融合 — 每天 8:30（或手動）自動執行。讀取過去 7 天寫入 vault（00-Inbox）的所有 .md 筆記，產生四段式融合分析（Connections / Patterns / Contradictions / Highest-value）。不摘要，要融合。只處理文字，不下載圖片。交付目標：Telegram。"
triggers:
  - "vault 知識融合"
  - "vault knowledge"
  - "vault 每週總結"
  - "知識融合"
  - "每週知識融合"
  - "vault synthesis"
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [vault, synthesis, knowledge-fusion, daily]
    category: note-taking
  vault:
    scan_path: "/home/pigo/Documents/Pigo_Obsidian/00-Inbox"
    time_window: "7days"
    delivery: "telegram"
---

# Vault 每日知識融合

## 觸發

每日 8:30 自動執行（由 cron job 觸發），或手動呼叫 `vault-knowledge`。

## 目的

讀取過去 7 天寫入 vault 的所有筆記，產生融合分析。**不摘要，強調融合**——找出筆記之間的非顯而易見連結、主題規律、矛盾之處，以及最值得發展的單篇筆記。

## 執行流程

### Step 1：抓取過去 7 天的新筆記

```bash
cd /home/pigo/Documents/Pigo_Obsidian
# 抓取 00-Inbox 過去 7 天修改過的 .md 檔案
find 00-Inbox -name "*.md" -mtime -7 | grep -v "index.md\|log.md\|README.md\|STATUS"
```

### Step 2：讀取每篇筆記的 frontmatter + 正文

對每個檔案：
- 讀取 `title`、`source`、`source_url`、`created`、`tags`（從 frontmatter）
- 讀取「核心摘要」章節 + 「文章分析」章節（跳過「完整原文」章節，太冗長）

### Step 3：餵給 LLM 執行融合分析

把以下 prompt 連同所有筆記內容一起送給 LLM：

```
Read all notes added to my vault in the last 7 days.
Produce a daily synthesis with four sections:
1. Connections: two or three non-obvious links between notes captured separately. Reference specific note titles. If the connection is obvious it does not qualify.
2. Patterns: any theme appearing across three or more notes. Name it in one sentence.
3. Contradictions: any two notes where my stated positions conflict. Quote the relevant line from each.
4. Highest-value capture: the single note most worth developing further and why.
Do not summarise. Synthesise.
```

**重要**：
- 餵給 LLM 的格式：**每篇筆記的 title + tags + 核心摘要章節內容**（不是完整全文，會太長）
- 如果正文有「完整原文」章節，跳過這章（太冗長）
- 重點章節：核心摘要、文章分析、我會怎麼用

### Step 4：格式化輸出

產出格式：

```markdown
# 📊 Vault 知識融合 — {日期}

> 掃描範圍：過去 7 天，共 N 篇新筆記

---

## 🔗 Connections（連結）

（兩個非顯而易見的連結，引用具體筆記標題）

---

## 🧩 Patterns（規律）

（三個以上筆記出現的主題，一句話命名）

---

## ⚡ Contradictions（矛盾）

（兩篇筆記中立場衝突，引用雙方原文）

---

## 💎 Highest-value Capture（最高價值捕獲）

（最值得發展的單篇筆記 + 原因）

---

_由 Hermes 自動生成 | 資料來源：00-Inbox_
```

### Step 5：交付

- **Telegram**：send_message 發給 Pigo（home channel）
- 主題：`📊 Vault 知識融合 — {今天日期}`

## 限制

- 只處理 `.md` 檔案
- 不處理 index.md、log.md、README.md、STATUS.md 等系統檔案
- 正文只讀「核心摘要」和「文章分析」章節（控制 token 用量）
- 圖片不下載，只做文字分析
- 如果 7 天內沒有新筆記，輸出「過去 7 天無新筆記」並停止

## 錯誤處理

| 錯誤 | 處理 |
|------|------|
| 找不到任何新筆記 | 發送「過去 7 天無新筆記」並結束 |
| LLM 回應失敗 | 發送「融合分析暫時無法生成，請稍後再試」 |
| find 找不到檔案 | 發送錯誤並附上完整錯誤訊息 |

## Cron Job 設定參考

若要將此 skill 設為每日 8:30 自動執行：

```json
{
  "id": "<自動生成>",
  "name": "Vault 每日知識融合（8:30）",
  "prompt": "執行 vault-knowledge skill。\n\n目標：讀取過去 7 天寫入 vault（/home/pigo/Documents/Pigo_Obsidian/00-Inbox）的所有 .md 筆記，產生四段式融合分析（Connections / Patterns / Contradictions / Highest-value）。\n\n嚴格遵守以下流程：\n\n1. 用 find 抓取過去 7 天修改的檔案（排除 index.md、log.md、README.md、STATUS.md）\n2. 對每篇筆記讀取：frontmatter（title、tags）+ 核心摘要章節 + 文章分析章節（跳過「完整原文」章節）\n3. 組合成一個 context 餵給 LLM\n4. 輸出的格式標題使用繁體中文：\n   - 🔗 Connections（連結）\n   - 🧩 Patterns（規律）\n   - ⚡ Contradictions（矛盾）\n   - 💎 Highest-value Capture（最高價值捕獲）\n5. 用 send_message 發送完整結果給 Pigo\n\n如果 7 天內無新筆記，發送：「過去 7 天沒有新筆記。」\n\n不要只做摘要，要做融合分析！Connections 要是非顯而易見的連結！",
  "skills": ["vault-knowledge"],
  "skill": "vault-knowledge",
  "schedule": {"kind": "cron", "expr": "30 8 * * *", "display": "30 8 * * *"},
  "schedule_display": "30 8 * * *",
  "deliver": "origin",
  "enabled": true
}
```