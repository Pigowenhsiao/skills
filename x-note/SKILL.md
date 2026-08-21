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

**⚠️ CDP 成功關鍵：Chrome 必須保持運行，不要重啟！**
每次 CDP fetch 前確認 Chrome 已運行（`tasklist | grep chrome`），且 CDP port 可達（`curl http://127.0.0.1:19825/json`）。
重啟 Chrome 會丟失登入狀態，導致 timeline 抓到的 text 為空。

```bash
cd E:/python_Code/Agent/skills/x-note/bin
python fetch_timeline.py --start 2026-08-08 --end 2026-08-09 --limit 5
# 輸出自動寫入 {{VAULT_ROOT}}/00-Inbox/xnote_fetch_YYYY-MM-DD.json
```

每個帳號：
1. 開啟 `https://x.com/<handle>`
2. 等待 tweet cards 渲染
3. 抓取 `[data-testid=tweet]` 元素
4. 提取：`handle`, `time_utc`, `status_id`, `text_preview`, `likes`, `reposts`, `replies`

每個帳號：
1. 開啟 `https://x.com/<handle>`
2. 等待 tweet cards 渲染
3. 抓取 `[data-testid=tweet]` 元素
4. 提取：`handle`, `time_utc`, `status_id`, `text_preview`, `likes`, `reposts`, `replies`
5. **不用截斷的 timeline 文字**

### Step 4: 抓取全文（fxtwitter）

```bash
python fetch_full_post.py --input xnote_fetch_YYYY-MM-DD.json --output xnote_full_YYYY-MM-DD.json
```
輸出自動寫入 `{{VAULT_ROOT}}/00-Inbox/xnote_full_YYYY-MM-DD.json`（如 `fetch_timeline.py` 的輸出在同一目錄）。

每個 post ID：
1. 呼叫 `https://api.fxtwitter.com/status/<id>`
2. 提取原文 + 圖片描述 + 影片 + 卡片
3. **fallback**：如果 fxtwitter 失敗 → 開 `https://x.com/<handle>/status/<id>` 用 CDP 抓
4. **再次失敗**：記錄 blocker，跳過

### Step 5: AI 評分（0-10）

```bash
python score_posts.py --input xnote_full_YYYY-MM-DD.json
# 預設使用 MiniMax-M3 semantic scoring
# 輸出自動寫入 xnote_score_YYYY-MM-DD.json（於 VAULT_ROOT/00-Inbox）
# 也可加 --use-rules 強制使用規則引擎
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

### Step 7: 驗證（MiniMax-M3 inline，無 Subagent）

Validation 在 `write_to_inbox.py` 內 inline 完成（Fix #3），不需 separate Subagent。
Pass/fail 依賴 rule-based validation（穩定），MiniMax-M3 分數僅作參考。

```bash
python write_to_inbox.py --input xnote_score_YYYY-MM-DD.json --date YYYY-MM-DD
# Validation 自動在 write_to_inbox 內完成
# 輸出寫入 {{VAULT_ROOT}}/00-Inbox/YYYY-MM-DD_x-note_*.md
# 狀態寫入 {{VAULT_ROOT}}/00-Inbox/xnote_status_YYYY-MM-DD.json
```

**已知行為**：MiniMax-M3 對短文推文（< 200 chars）傾向保守評分（62-82/100）。Rule validation 對結構合格的 notes 穩定給 100。

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
| CDP 啟動失敗 | 確認 Chrome 已運行且 CDP port 可達；**不要重啟 Chrome**（會丟失登入狀態） |
| Profile 找不到 | fallback 掃描 → 都找不到 → 未登入 |
| Key Points 少於 3 項 | 檢查 `curate_sections()` 是否正確解析 curator body；確認 curator cache 未損壞 |
| Validation 一直失敗 | 清除 curator cache (`~/.cache/x-note-curator/*.md`) 讓 curator 重新生成 |
| fxtwitter 全文截斷 | CDP fallback 會自動補全；但需注意 CDP text 可能不完整 |

## Known Issues

| Issue | 原因 | Workaround |
|-------|------|-------------|
| CDP fetch text 為空 | Chrome 重啟後丟失登入狀態 | 不要重啟 Chrome；維持 CDP port 19825 運行 |
| 評分 > 6.5 但寫入失敗 | MiniMax-M3 validation 保守評分短文 | 改用 `--skip-validation` 或手動審查 |
| 同一帳號多篇 note 檔名相同 | `slugify()` 衝突 | 手動重命名 |
| `text_length` 與原文不符 | fxtwitter API 截斷；CDP 可補全但有長度限制 | 記錄在 note；人工確認 |

## 技術筆記（M3 Enhancement）

### Curator 架構
- `curate_sections()` 返回 `dict`：`{summary: str, key_points: list[str], why_it_matters: str}`
  - `key_points` 必須是 list，每個 element 是一個要點字串
  - curator body 格式：`## Key Points\n- 要點1\n- 要點2\n...`
- `score_with_llm()`：一次 call 輸出 score + content_type + usefulness + tags
- `classify_with_llm()`：輸出 classification_path + confidence + reasoning
- `validate_note_with_llm()`：MiniMax-M3 評估 note 品質（pass/fail 由 rule validation 決定）
- `_fallback_validate_note()`：規則 engine fallback（穩定，用於 pass/fail 決策）

### CDP 成功模式（實測 2026-08-20）
```bash
# 1. 確認 Chrome 運行（不重啟！）
tasklist | grep chrome
# → 應有多個 chrome.exe 進程

# 2. 確認 CDP port 可達
curl -s http://127.0.0.1:19825/json | head -3
# → 應返回 WebSocket URL

# 3. 執行 fetch（用 --limit 控制帳號數）
cd E:/python_Code/Agent/skills/x-note/bin
python fetch_timeline.py --start YYYY-MM-DD --end YYYY-MM-DD --limit 15
# 輸出：{{VAULT_ROOT}}/00-Inbox/xnote_fetch_YYYY-MM-DD.json

# 4. 抓全文
python fetch_full_post.py --input xnote_fetch_YYYY-MM-DD.json

# 5. 評分（MiniMax-M3）
python score_posts.py --input xnote_full_YYYY-MM-DD.json

# 6. 寫入（自動 validation + 分類）
python write_to_inbox.py --input xnote_score_YYYY-MM-DD.json --date YYYY-MM-DD
```
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
