---
name: x-note-inbox-upgrade
description: >
  將 00-Inbox 中所有已用 CDP 抓取的 ## 推文快照 格式檔案，
  以 MiniMax-M3 批次評分（0-50 分制）、生成完整 x-note2 body（Core Summary / Detailed Analysis / 
  Key Knowledge Points / Why It Matters），並嚴格依 score>=35 閥門寫入乾淨的單一輸出檔案。
  適用時機：所有 inbox 推文已完成 CDP 抓取、需要一次性完成評分+格式化+去重的場合。
version: 1.0.0
author: Pigo Pi Agent
tags: [x-note2, batch, scoring, inbox, social-intel]
category: knowledge-capture
related_skills: [x-note, llm-wiki]
triggers:
  - "x-note-inbox-upgrade"
  - "x-note 批次評分"
  - "將 inbox 推文評分寫入"
  - "批次升級 x-note2"
---

# x-note-inbox-upgrade

## Purpose

將已 CDP 抓取的 `## 推文快照` 格式 inbox 筆記，批次執行：

1. **評分**（MiniMax-M3，0-50 分制）
2. **評語生成**（繁體中文，40 字內）
3. **完整 body 生成**（Core Summary / Detailed Analysis / Key Knowledge Points / Why It Matters）
4. **嚴格閥門寫入**（score >= 35 才寫入，< 35 一律略過）
5. **去重**（同一 tweet_id 只保留最高分檔案）

## Prerequisites

- CDP Chrome 運行於 `http://127.0.0.1:9222`（抓取用，評分腳本本身不依賴）
- `MINIMAX_API_KEY`（從 `~/.pi/agent/auth.json` 讀取）
- 目標檔案必須具 `## 推文快照` 區塊（CDP 已抓取過的檔案）

## Output Format

每次執行產出 **一個日期前綴的資料夾**：

```
00-Inbox/
  2026-06-16_x-note2_/
    2026-06-16_x-note2_<handle>_<slug>_<tweet_id_last6>.md   ← 評分寫入
    STATUS_x-note-inbox-upgrade_YYYY-MM-DD.md                  ← 執行狀態
```

## Frontmatter Schema（每個輸出檔必備）

```yaml
---
title: "<從推文內容提取的描述性標題，80字以內>"
source: "X.com @<handle>"
source_url: "https://x.com/<handle>/status/<tweet_id>"
tweet_id: "<status_id>"
author: "<display name>"
handle: "@<handle>"
captured_at: "YYYY-MM-DDTHH:mm:ss+08:00"
capture_method: "baoyu-fetch + CDP"    # 繼承原檔
content_hash: "sha256:<sha256 of tweet text>"
engagement:
  views: 0          # CDP 尚未提供互動數據時填 0
  likes: 0
  reposts: 0
  replies: 0
  bookmarks: 0
media_ids: []
score: <1-5>       # MiniMax-M3 評分
score_reason: "<繁體中文理由，30字以內>"
tags:
  - x-note2
  - social-intel
  - "@<handle>"
sources:
  - "https://x.com/<handle>/status/<tweet_id>"
  - "00-Inbox/xnote_complete_YYYY-MM-DD.json"  # ← 本地原始資料路徑（HARD：必填）
type: "x-post-summary"
classification_path: "00-Inbox"
status: "inbox"
date: "YYYY-MM-DD"
processed_by: "x-note-inbox-upgrade"
---
```

## Body Sections（必備 7 區塊）

```markdown
# <title>

## Source Snapshot

- **Source URL**: https://x.com/<handle>/status/<tweet_id>
- **Author**: <display name>
- **Handle**: @<handle>
- **Post time**: <captured_at>
- **Engagement**:
  - Views: <N>
  - Likes: <N>
  - Reposts: <N>
  - Replies: <N>
  - Bookmarks: 0
- **Content hash**: sha256:<hash>
- **Capture method**: baoyu-fetch + CDP

<MiniMax-M3 生成的 body content>

## Reference

### Complete X Post Text

```text
<完整推文原文，一字不漏>
```

### 相關資源與出處
- <source_url>

## Related Notes

- [[AGENTS.md|Pigo 專屬操作規範與路由規則]]
- [[14-Skills/llm-wiki/SKILL|llm-wiki 技能文檔]]
```

## Batch Processing Config

| 參數 | 值 | 說明 |
|------|-----|------|
| `BATCH_SIZE` | 8 | 每個 MiniMax-M3 API call 的 tweet 數量 |
| `MAX_WORKERS` | 4 | 並行 API call 數 |
| `SCORE_THRESHOLD` | 35 | **HARD RULE**：score < 35 一律不寫入（0-50 分制） |
| `API_TIMEOUT` | 240s | 每個 API call 的超時 |
| `API_MODEL` | MiniMax-M3 | 評分 + body 生成模型 |
| `thinking_budget` | 3000 tokens | M3 推理預算 |
| `max_tokens` | 15000 | M3 输出限額 |

## Execution Workflow

### Phase 1：Collect & Parse

1. 掃描 `00-Inbox/`，收集所有含 `## 推文快照` 的 `.md` 檔案
2. 從每個檔案解析：`tweet_id`、`handle`、`tweet_block`（`## 推文快照` 區塊全文）
3. 跳過：已處理過的（`processed_by: x-note-inbox-upgrade`）、STATUS/index/log 檔

### Phase 2：Batch Scoring + Curation（MiniMax-M3）

1. 將 tweets 分批（每批 `BATCH_SIZE` 個）
2. 每批發送一個 M3 API call，system prompt 包含完整格式規範
3. M3 對每個 tweet 輸出：SCORE + SCORE_REASON + BODY_START...BODY_END
4. **正則解析前**：先 strip `thinking` block（防止干擾分隔符匹配）
5. 解析結果依序對齊輸入順序
6. API 失敗時使用 static fallback body

### Phase 3：Write + Filter

1. 遍歷所有 tweets：
   - **score >= 3** → 寫入新檔案，slug = `<前4詞>_<tweet_id末6位>`
   - **score < 3** → 跳過（不寫入，附 reason 到 STATUS）
2. **去重**：同 `tweet_id` 只保留最高分，其餘刪除

### Phase 4：STATUS Report

寫入 `00-Inbox/STATUS_x-note-inbox-upgrade_YYYY-MM-DD.md`，包含：
- 執行摘要（檔案數、API 成功率、寫入/略過數）
- 評分分佈
- 略過清單（score < 3，附 reason）
- 寫入清單（score >= 3）

### Phase 5：Post-Processing（必做）

1. 刪除已合併入新版的所有 legacy 原始檔（`2026-06-14_*`、`2026-06-15_*` 等）
2. 更新 `Learning/status/LLM-Wiki-Ingest-Log.md`

## API Prompt Template

MiniMax-M3 接收的 system + user prompt 結構：

**System**：你是專業來源導向知識整理助手 + X 推文評分員，繁體中文輸出。

**User**：每批包含 N 個 tweet block，以 `=== Tweet N`...`=== END Tweet N` 分隔。

**Expected output per tweet**：

```
TWEET_Separator_START
SCORE: <數字1-5>
SCORE_REASON: <繁中理由，30字以內>
BODY_START
## Core Summary（BLUF格式）
[結論一句話]

[2-3句支撐]

[實踐意義]

## Detailed Analysis
### 1. <分析要點一>
...

### 2. <分析要點二>
...

## Key Knowledge Points
- **<術語/方法/工具>**：<具體說明>

## Why It Matters
- **<價值連接>**：<具體說明>
BODY_END
TWEET_Separator_END
```

## Score Rubric（0-50 分制）

| 分數 | 標準 | 繁中關鍵詞 |
|------|------|-----------|
| 45-50 | 完整提示詞+工作流+可重用模式，高密度原創技術 | 原創概念、策略深度、實戰避坑、極高價值 |
| 40-44 | 可重用提示詞（完整規格）；或多步驟工作流+具體工具 | 可複製框架、具體構想、實用性高 |
| 35-39 | 具實質內容的工作流/洞察；清晰洞察+合理互動 | 工作流、洞察、實用內容 |
| 25-34 | 有一定價值但完整度不足 | 深度有限、缺乏論證、資訊密度低 |
| 0-24 | 短片段/一般評論/僅媒體或連結 | 無實質內容、重複貼文、純連結 |

**閥門：score >= 35 才寫入 vault（0-50 分制）**

## 路徑解析

路徑**動態解析**，優先讀取 `~/.codex/AGENTS.md` 的 `Vault:` 與 `Agent:` 設定，
支援多電腦執行而不需要修改任何腳本。

若 AGENTS.md 不存在或格式不符，fallback 到 `Path.home() / "Box" / "00-home-pigo.hsiao" / "VBA"` 拼接。

## Key Files

| 檔案 | 用途 |
|------|------|
| `scripts/xnote_inbox_upgrade.py` | 主執行脚本（Python，含動態路徑） |
| `references/score_rubric.md` | 評分對照表（0-50 分制） |

## Hard Rules

1. **SCORE_THRESHOLD = 35（HARD）**：不得低於此閥門寫入（0-50 分制）
2. **正則解析前必 strip thinking block**
3. **同一 tweet_id 只保留最高分檔案**
4. **Legacy 原始檔案完成合併後必須刪除**
5. **每次執行後必須更新 LLM-Wiki-Ingest-Log.md**
6. **路徑從 ~/.codex/AGENTS.md 動態讀取，不得 hardcode**
7. **`sources:` 必須 ≥ 2 項（HARD）**：第 1 項是 X URL，第 2 項是本地原始資料 json 的 vault-relative path。**只寫 URL 一項的 note 一律壞掉**，會被 validator 抓出。
8. **原始資料保留義務**：每次跑之前必須先把 `xnote_complete_YYYY-MM-DD.json` 從 `~/Downloads/` 或 fetch 輸出複製到 vault 的 `00-Inbox/`，讓 note 內的相對路徑能找到。**不能跑完即丟**——這個 bug 在 2026-06-16 已經發生過一次（v2 full-processor 跑完 raw json 沒留下），造成 14/20 個 note 的原始資料永久遺失。
