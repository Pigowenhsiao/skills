---
name: x-note
description: 將 X/Twitter 帳號清單的指定日期區間貼文轉為高密度、可追溯的 Vault 學習筆記。CDP（cookies + Chrome profile）+ fxtwitter 抓全文；AI 評分過濾 > 6.5；llm-wiki 格式寫入 Vault 00-Inbox；Subagent 驗證後才算完成。
triggers:
  - "x-note"
  - "X daily"
  - "X archive"
  - "X 帳號抓取"
  - "X 帳號歸檔"
---

# x-note

## Purpose

把 X/Twitter 帳號的**指定日期區間貼文**轉成**可沉澱、可追溯、可重新驗證**的 Vault 學習筆記。

**與舊 `x-note` 的差異**：
- 只保留**最高品質**內容（> 6.5 分）
- 階段分離：CDP 抓取 metadata → fxtwitter 抓全文 → AI 評分 → 寫入
- 強調 **Reference 完整原文** 與 **AI Score 透明度**
- 不接受「待補」或無實際內容的 summary

---

## Environment

### Skill locations

| 角色 | 路徑 |
|------|------|
| Canonical（主檔） | `E:\python_Code\Agent\skills\x-note\` |
| Codex runtime 熱載入 | `C:\Users\pigow\.codex\skills\01-Knowledge-System\x-note\` |

腳本均在 **skill 本地** `bin/`（不在 `$AGENT_ROOT/bin/`）。執行前先 `cd` 到 skill 目錄，或用 skill-relative path。

### Paths (machine-specific)

`.path-config.json` 位於 **`VAULT_ROOT`**（不在 `AGENT_ROOT`）。
`bin/config_loader.py` 會從 CWD parents / `X2_VAULT_ROOT` / 常見路徑搜尋該檔。詳見 `config/schema.md`。

| 變數 | 預設值 | 用途 |
|------|--------|------|
| `VAULT_ROOT` | `E:\obsidian` | Vault 根；`.path-config.json` 所在 |
| `AGENT_ROOT` | `E:\python_Code\Agent` | Agent 根 |
| `DOWNLOADS` | `C:\Users\pigow\Downloads` | 預設 cookies 目錄 |
| `CDP_PORT` | `19825` | Chrome Debug Port |
| `CHROME_PROFILE_NAME` | `Hsiaopigo` | 預設 Profile 名稱 |
| `CHROME_EXE` | `C:\Program Files\Google\Chrome\Application\chrome.exe` | Chrome 路徑 |
| `TWITTER_HANDLE_FILE` | `{{AGENT_ROOT}}/name.md` | 帳號清單 |
| `X_COOKIES_FILE` | `{{DOWNLOADS}}/x_cookies_logged_in.json` | 已登入 cookies |

### Outputs
```
{{VAULT_ROOT}}/00-Inbox/YYYY-MM-DD_x-note_<handle>_<slug>.md
{{VAULT_ROOT}}/00-Inbox/xnote_fetch_YYYY-MM-DD.json   ← timeline+IDs
{{VAULT_ROOT}}/00-Inbox/xnote_full_YYYY-MM-DD.json    ← 完整內容
{{VAULT_ROOT}}/00-Inbox/xnote_score_YYYY-MM-DD.json   ← 評分
{{VAULT_ROOT}}/00-Inbox/xnote_skip_YYYY-MM-DD.json    ← 跳過 reasons
{{VAULT_ROOT}}/00-Inbox/xnote_status_YYYY-MM-DD.json  ← 抓取/驗證狀態
{{VAULT_ROOT}}/08-Learning/99_Maintenance/status/LLM-Wiki-Index.md
{{VAULT_ROOT}}/08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md
{{VAULT_ROOT}}/STATUS_ALL.md
```

### CDP 行為
- **首次**：有頭瀏覽器 + 預設 Profile → 用戶手動登入 → 匯出 cookies
- **之後**：無頭瀏覽器 + 預設 Profile + 載入 cookies → 自動抓取
- **Profile 找不到**：fallback 任何可用的 profile → 都找不到 → 未登入狀態

---

## Workflow

### Step 1: Resolve Profile & Start CDP

```bash
cd {{AGENT_ROOT}}/skills/x-note   # 或 Codex runtime 對應 skill 目錄
python bin/resolve_profile.py --profile Hsiaopigo
# 找到 profile → 啟動 headless Chrome
# 找不到 → 掃描 fallback → 找到 → 啟動
# 都找不到 → 啟動未登入 chrome，提醒 Pigo
```

### Step 2: Read Handles

```bash
python bin/resolve_handles.py --handles name.md
# 順序：.path-config.json → handle 設定 → Vault _config 設定 → Agent name.md
```

格式：
```md
- @dotey
xiaoxiaodong01
@wshuyi
```

### Step 3: 抓取 Timeline（CDP）

```bash
python bin/fetch_timeline.py --start 2026-08-08 --end 2026-08-09 --limit 5 --output xnote_fetch_YYYY-MM-DD.json
```

每個帳號：
1. 開啟 `https://x.com/<handle>`
2. 等待 tweet cards 渲染
3. 抓取 `[data-testid=tweet]` 元素
4. 提取：`handle`, `time_utc`, `status_id`, `text_preview`, `likes`, `reposts`, `replies`
5. **不用截斷的 timeline 文字**

### Step 4: 抓取全文（fxtwitter）

```bash
python bin/fetch_full_post.py --input xnote_fetch_YYYY-MM-DD.json --output xnote_full_YYYY-MM-DD.json
```

每個 post ID：
1. 呼叫 `https://api.fxtwitter.com/status/<id>`
2. 提取原文 + 圖片描述 + 影片 + 卡片
3. **fallback**：如果 fxtwitter 失敗 → 開 `https://x.com/<handle>/status/<id>` 用 CDP 抓
4. **再次失敗**：記錄 blocker，跳過

### Step 5: AI 評分（0-10）

```bash
python bin/score_posts.py --input xnote_full_YYYY-MM-DD.json --output xnote_score_YYYY-MM-DD.json
```

每篇依據：
- **內容長度**（< 50 字：扣分）
- **實用性**（教學、Prompt、工具、案例：高分）
- **可參考性**（可複製貼上，立刻能用：高分）
- **內容豐富度**（含 prompt、link、code：高分）
- **無內容**（純情緒、感想、聊天 → 0-3 分）
- **廣告、轉推、spam** → 0-1 分

> 6.5 才保留。

### Step 6: 寫入 Vault（llm-wiki 格式）

```bash
python bin/write_to_inbox.py --input xnote_score_YYYY-MM-DD.json --threshold 6.5
```

輸出檔名：
```
{{VAULT_ROOT}}/00-Inbox/YYYY-MM-DD_x-note_<handle>_<slug>.md
```

**必填 frontmatter**：
```yaml
---
title: "..." 
sources:
  - "https://x.com/<handle>/status/<status_id>"
  - "00-Inbox/xnote_full_YYYY-MM-DD.json"
source: "X"
source_url: "https://x.com/<handle>/status/<status_id>"
tweet_id: "<status_id>"
author_display: "..."
handle: "@handle"
created: "YYYY-MM-DDTHH:mm:ss+08:00"
captured_at: "YYYY-MM-DD HH:mm:ss +08:00"
capture_method: "fxtwitter/CDP-fallback"
type: "x-post-summary"
tags: [x-note, llm-wiki, social-intel]
score: 7.5
score_reason: "..."
content_hash: "..."
text_length: 1234
status: inbox
classification_path: "00-Inbox"
---
```

**必填 sections**：
1. `# <title>`
2. `## Source Snapshot`
3. `## Core Summary`（不可空、不可「待補」、不可無意義）
4. `## Key Points`（至少 3 點）
5. `## Why It Matters`
6. `## AI Score`
7. `## Suggested Classification`
8. `## Source`
9. `## Reference`
   - `### Complete X Post Text (繁中重寫)`（x-note 自 2026-08-11 起自動由 `translate_full_text()` 產生繁體中文翻譯）
   - `### Complete X Post Text (原文)`（```text``` 包裹的原始英文或非繁中文字）

### Step 7: Subagent 驗證

```bash
python bin/validate_note.py --input xnote_score_YYYY-MM-DD.json --output xnote_status_YYYY-MM-DD.json
```

必過檢查：
- [ ] 必填 frontmatter 欄位齊全
- [ ] `core_summary` 不為空、長度 > 50 字
- [ ] `key_points` ≥ 3 項
- [ ] `reference` 含完整原文
- [ ] `content_hash` 對應實際內文
- [ ] `score ≥ 6.5`
- [ ] 筆名、handle、tweet_id 一致

**任何一項失敗 = 整批失敗**，要求重新整理。

### Step 8: 更新 Index / Log

```bash
python bin/update_indexes.py --date YYYY-MM-DD
```

更新：
- `00-Inbox/index.md`
- `LLM-Wiki-Index.md`
- `LLM-Wiki-Ingest-Log.md`
- `STATUS_ALL.md`

記錄：
- 帳號數
- 抓取 post 數
- > 6.5 數
- 驗證通過數
- 失敗數
- 輸出檔案
- 限制

### Step 9: Boundary Check

```bash
python {{VAULT_ROOT}}/12-Meta/scripts/check-vault-boundary.py
```

通過後才算完成。

---

## Failure Handling

| 失敗 | 處理 |
|------|------|
| CDP 啟動失敗 | 記 log，提示手動重啟 |
| Profile 找不到 | fallback 掃描 → 都找不到 → 未登入 |
| Timeline 抓失敗 | 跳過該帳號，繼續下一個 |
| fxtwitter 失敗 | 自動 fallback x.com CDP |
| x.com CDP 失敗 | 跳過，記 blocker |
| 評分 < 6.5 | 跳過，記 reason |
| Subagent 驗證失敗 | 整批失敗，**不**寫入 Vault |
| 全部失敗 | 不建立任何筆記，回報錯誤 |

---

## Idempotency

**目前不做**。每次執行都會處理當日全部 post。

> 將來可加 `--incremental` 開關（開發中）。

---

## Output Contract

回報 Pigo：
- 處理帳號數 / 失敗帳號數
- 日期區間
- 抓取 post 數
- 評分 > 6.5 數
- 跳過數 + 原因
- 完整抓取數 / 失敗數
- 驗證通過 / 失敗
- 輸出檔案清單
- Boundary check 結果
