---
name: llm-wiki
description: PigoVault 知識庫攝入與健康維護系統。支援 X Posts（x-note）和 YouTube 影片的結構化攝入、frontmatter 驗證、增量緩存、SHA256 去重、health check、index 更新。
triggers:
  - "llm-wiki"
  - "vault health"
  - "ingest"
  - "knowledge base"
  - "update index"
---

# llm-wiki Knowledge System

## Overview

llm-wiki 是 PigoVault 的核心知識庫系統，負責：
1. **結構化攝入** — 驗證和持久化 x-note / YouTube 筆記
2. **增量緩存** — SHA256 去重，避免重複處理相同內容
3. **健康檢查** — 孤島頁面、壞連結、缺失來源、YouTube 轉錄狀態
4. **索引維護** — 自動更新 LLM-Wiki-Index.md、Ingest-Log.md

## Architecture

```
llm-wiki/
├── SKILL.md          ← 本文件
├── __init__.py       ← 匯出介面
├── config.py         ← 路徑解析 + 設定
├── utils.py          ← 核心函式（session check, cache, index, health）
├── youtube_handler.py ← YouTube 專用處理
└── tests/
    └── test_utils.py ← 單元測試
```

## Configuration

### Path Resolution (Priority Order)

1. `LLM_WIKI_VAULT_ROOT` 環境變數
2. `{{VAULT_ROOT}}/.path-config.json` 中的 `vault_root` 欄位
3. 向上搜尋父目錄（`CWD` → parents），找 `.git` + `00-Inbox`
4. Fallback: `E:/obsidian`

```json
// {{VAULT_ROOT}}/.path-config.json
{
  "vault_root": "E:/obsidian",
  "youtube": {
    "lcz_me_base": "https://lcz.me/topic/",
    "ytdlp_format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
  }
}
```

### Required Files

| 檔案 | 用途 |
|------|------|
| `00-Inbox/index.md` | 收件匣索引 |
| `08-Learning/index.md` | 學習區索引 |
| `08-Learning/99_Maintenance/status/LLM-Wiki-Index.md` | 知識庫統計 |
| `08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md` | 攝入日誌（JSON + Markdown） |

## Source Types

### X Posts (x-note)

Frontmatter 必填欄位：
```yaml
title, sources, source_url, tweet_id, handle, author_display,
created, captured_at, capture_method, content_hash, text_length,
score, score_reason, status, classification_path, tags
```

`type: x-post-summary`

### YouTube Videos

Frontmatter 必填欄位：
```yaml
title, sources, type: youtube-note,
source-completeness, transcribed,
created, tags
```

Completeness 等級：
| 等級 | `source-completeness` | 意義 |
|------|----------------------|------|
| L1 | `full-transcript` + `transcribed: true` | Whisper 全文轉譯 |
| L2 | `full-transcript` 或 `external-transcript` | 有外部文稿（lcz.me 等）|
| L3 | `description-only` | 只有 YouTube 描述 |

**Git pre-commit 限制**：L3 等級的 `_x-note_youtube_*.md` 檔案在 `transcribed: true` 或 `source-completeness: full-transcript/external-transcript` 之前不得 commit。

## Core Functions

### `check_session_start() -> Dict`
驗證 vault 必要檔案是否存在。開機時呼叫。

### `load_config() -> LlmWikiConfig`
解析設定，優先順序：env > json > auto-detect。

### `check_incremental_cache(source: Path) -> Tuple[bool, str]`
- 檔案：SHA256 hash
- URL：字串 hash（`source_url` 字面值）
- 回傳：`(needs_processing, previous_hash)`

### `update_ingest_log(source, hash_value, notes=None) -> bool`
同時寫入 JSON log 和 Markdown log（雙格式）。

### `fetch_youtube_metadata(url: str) -> Dict`
抓取 YouTube 影片元資料：
- video_id, title, channel, duration, thumbnail
- 透過 oEmbed API（不需要 API key）

### `fetch_lcz_me_transcript(url: str) -> str | None`
嘗試從 lcz.me 抓取文稿（`source-completeness: external-transcript` 的主要來源）。

### `check_youtube_completeness(filepath: Path) -> Dict`
檢查 YouTube 筆記的轉譯狀態：
- `transcribed: true` → L1
- `source-completeness: full-transcript/external-transcript` → L2
- `source-completeness: description-only` → L3

### `find_youtube_orphans() -> List[Dict]`
找出 transcription 級別低於 L2 且超過 7 天未更新的 YouTube 筆記。

### `health_check() -> Dict`
完整健康檢查，包含 YouTube 專用檢查：
- orphans, broken_links, missing_sources
- youtube_transcription_status
- youtube_stale_l3_notes
- lcz_me_link_validation

### `generate_report(health: Dict) -> str`
產生 Markdown 格式健康報告。

### `update_indexes(notes_created: List[Path]) -> Dict`
更新所有索引：`inbox_index`、`llm_wiki_index`（包含 YouTube 統計）、`ingest_log`。

## Usage

```python
from llm_wiki import (
    check_session_start, check_incremental_cache,
    update_ingest_log, fetch_youtube_metadata,
    health_check, generate_report, update_indexes,
    fetch_lcz_me_transcript, check_youtube_completeness,
)

# 開機檢查
session = check_session_start()
print(f"Required files: {session['found_count']}/{session['found_count']+session['missing_count']}")

# YouTube 元資料
meta = fetch_youtube_metadata("https://www.youtube.com/watch?v=k_PjTWpXP10")
print(f"Title: {meta['title']}, Channel: {meta['channel']}")

# lcz.me 文稿
transcript = fetch_lcz_me_transcript("https://lcz.me/topic/1187")
if transcript:
    print(f"Transcript length: {len(transcript)} chars")

# 健康檢查
health = health_check()
print(generate_report(health))

# YouTube 完整性檢查
from llm_wiki import check_youtube_completeness
result = check_youtube_completeness(Path("E:/obsidian/00-Inbox/2026-08-20_x-note_youtube_qwen3.md"))
print(f"Level: {result['level']}, Status: {result['status']}")
```

## Output Files

| 檔案 | 位置 | 更新時機 |
|------|------|---------|
| LLM-Wiki-Index.md | 08-Learning/99_Maintenance/status/ | 每次 `update_indexes()` |
| LLM-Wiki-Ingest-Log.md | 08-Learning/99_Maintenance/status/ | 每次新筆記寫入 |
| 00-Inbox/index.md | 00-Inbox/ | 每次 `update_indexes()` |
| health-reports/*.md | 12-Meta/health-reports/ | 每次 `health_check()` 報告 |

## Idempotency

所有寫入操作都是增量+追加的，可安全重複執行。
