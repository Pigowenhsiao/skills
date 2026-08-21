#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x-note-inbox-upgrade
批次將 00-Inbox 中已 CDP 抓取的 ## 推文快照 格式檔案，
以 MiniMax-M3 評分（0-50 分制）+ 生成完整 x-note2 body，
依 score>=35 閥門寫入乾淨輸出。

路徑動態解析：優先讀取 ~/.codex/AGENTS.md 的 Vault/Agent 設定，
fallback 到 Path.home() 拼接，支援多電腦環境。

Usage:
    python xnote_inbox_upgrade.py

Config:
    BATCH_SIZE      = 8   tweets per API call
    MAX_WORKERS     = 4   parallel API calls
    SCORE_THRESHOLD = 35  HARD RULE: skip if score < 35 (0-50 scale)
    API_TIMEOUT     = 240 seconds
    MODEL           = "MiniMax-M3"
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# ── 動態路徑解析（支援多電腦）───────────────────────────────────────────────
def load_workspace_paths():
    """從 ~/.codex/AGENTS.md 讀取 Vault 與 Agent 路徑，fallback 到 home 目錄拼接。"""
    agents_md = Path.home() / ".codex" / "AGENTS.md"
    vault_path = None
    agent_path = None
    if agents_md.exists():
        content = agents_md.read_text(encoding="utf-8")
        for line in content.split("\n"):
            ls = line.strip()
            if ls.startswith("Vault:"):
                vault_path = Path(ls.split("Vault:", 1)[1].strip().replace("\\", "/")).resolve()
            elif ls.startswith("Agent:"):
                agent_path = Path(ls.split("Agent:", 1)[1].strip().replace("\\", "/")).resolve()
    if not vault_path:
        vault_path = Path.home() / "Box" / "00-home-pigo.hsiao" / "VBA" / "Pigo_Obsidian"
    if not agent_path:
        agent_path = Path.home() / "Box" / "00-home-pigo.hsiao" / "VBA" / "Agent"
    return vault_path, agent_path

VAULT, AGENT = load_workspace_paths()
INBOX = VAULT / "00-Inbox"
LLM_WIKI = AGENT / "skills" / "llm-wiki" / "SKILL.md"

# ── Config ──────────────────────────────────────────────────────────────────
API_URL = "https://api.minimax.io/anthropic/v1/messages"

BATCH_SIZE = 8          # tweets per MiniMax-M3 API call
MAX_WORKERS = 4         # parallel API calls
SCORE_THRESHOLD = 35    # HARD RULE（0-50 分制，>=35 才寫入）
API_TIMEOUT = 240       # seconds per call

MODEL = "MiniMax-M3"
THINKING_BUDGET = 3000
MAX_TOKENS = 15000

UTC8 = timezone(timedelta(hours=8))
NOW = datetime.now(UTC8)
DATE_STR = NOW.strftime("%Y-%m-%d")
NOW_STR = NOW.strftime("%Y-%m-%d %H:%M:%S+08:00")

# ── API Key ─────────────────────────────────────────────────────────────────
def load_api_key() -> str:
    p = Path.home() / ".pi" / "agent" / "auth.json"
    if p.exists():
        auth = json.loads(p.read_text(encoding='utf-8'))
        return auth.get("minimax", {}).get("key") or auth.get("MiniMax", {}).get("key", "")
    return ""

# 模組層級賦值：score_and_curate_batch() 在執行時需要 API_KEY
API_KEY = load_api_key()


# ── Parse ───────────────────────────────────────────────────────────────────
def parse_inbox_file(fpath: Path) -> Dict:
    """Parse a ## 推文快照 inbox file, return structured tweet data."""
    text = open(fpath, encoding='utf-8').read()

    # Frontmatter
    front = {}
    in_fm = False
    for line in text.split('\n'):
        ls = line.strip()
        if ls == '---':
            in_fm = not in_fm
            continue
        if in_fm and ':' in line:
            k, v = line.split(':', 1)
            front[k.strip()] = v.strip().strip('"')

    # Tweet block
    m = re.search(r'## 推文快照\s*\n+(.*?)(?=\n## |\n#|\Z)', text, re.DOTALL)
    block = m.group(1).strip() if m else ''

    # Filename parsing: 2026-06-14_<handle>_<tweet_id>.md
    name = fpath.name
    parts = name.replace('.md', '').split('_')
    if len(parts) >= 4:
        tweet_id = parts[-1]
        handle = parts[2].lstrip('@')
    else:
        tweet_id = front.get('tweet_id', '')
        handle = front.get('handle', '').lstrip('@')

    # Skip if already processed by this script
    if front.get('processed_by') == 'x-note-inbox-upgrade':
        return None

    return {
        'filepath': str(fpath),
        'filename': fpath.name,
        'handle': handle,
        'tweet_id': tweet_id,
        'author': front.get('author', handle),
        'source_url': front.get('source_url', f"https://x.com/{handle}/status/{tweet_id}"),
        'captured_at': front.get('captured_at', DATE_STR),
        'capture_method': front.get('capture_method', 'baoyu-fetch + CDP'),
        'tweet_block': block,
        'title_candidate': front.get('title', ''),
    }


def collect_inbox_tweets() -> List[Dict]:
    """Collect all ## 推文快照 files from inbox."""
    tweets = []
    for f in sorted(os.listdir(INBOX)):
        if not f.endswith('.md'):
            continue
        # Skip non-note files
        skip_names = {'index.md', 'log.md'}
        if f in skip_names or 'STATUS' in f:
            continue
        path = INBOX / f
        td = parse_inbox_file(path)
        if td and td['tweet_block']:
            tweets.append(td)
    return tweets


# ── M3 API ─────────────────────────────────────────────────────────────────
def strip_thinking_blocks(text: str) -> str:
    """
    Remove thinking/scratchpad blocks that would interfere with separator parsing.
    Handles: <thinking>...</thinking>, [TOKENS_THINKING]...[/TOKENS_THINKING],
    markdown ## Thinking / ## 分析 sections, and Claude-style thinking.
    """
    # Remove XML-style thinking tags
    text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL)
    text = re.sub(r'\[TOKENS_THINKING\].*?\[/TOKENS_THINKING\]', '', text, flags=re.DOTALL)

    # Remove markdown ## Thinking / ## 分析 sections (until next ## header or end)
    lines = text.split('\n')
    clean_lines = []
    skip = False
    for line in lines:
        ll = line.strip()
        # Detect thinking block headers
        if re.match(r'^#{1,3}\s*(thinking|分析|推理|reasoning)', ll, re.IGNORECASE):
            skip = True
            continue
        # Exit skip mode at next top-level section
        if skip and re.match(r'^##\s+\w', ll):
            skip = False
        if skip:
            continue
        clean_lines.append(line)
    return '\n'.join(clean_lines)


def score_and_curate_batch(tweets_batch: List[Dict]) -> List[Dict]:
    """
    Send one batch to MiniMax-M3; return list of {score, score_reason, body, api_success}.
    Score is 0-50 (0-50 scale, threshold 35).
    """
    if not tweets_batch:
        return []

    messages = []
    for i, t in enumerate(tweets_batch):
        tweet_text = t['tweet_block'][:2500]
        messages.append({
            "role": "user",
            "content": (
                f"=== Tweet {i+1}\n"
                f"Handle: @{t['handle']}\n"
                f"Tweet ID: {t['tweet_id']}\n"
                f"Content:\n{tweet_text}\n"
                f"=== END Tweet {i+1}\n"
            )
        })

    # 評分制：0-50 分，門檻 35
    system_prompt = (
        "你是專業的來源導向知識整理助手，同時也是X推文評分員。\n"
        "評分制：0-50 分（0=無價值/純連結/重複貼文，50=極高價值原創概念+完整工作流）。\n"
        "門檻：>=35 分才值得寫入 vault，<35 分請給予低分並從簡描述。\n"
        "請對每一則推文評分（0-50）並說明理由，再根據評分與內容整理成高品質 x-note2 筆記主體。\n"
        "輸出語言：繁體中文（台灣用語）。\n"
        "不可使用簡體中文，不可空泛稱讚，不可編造原文未提及的內容。\n"
        "**嚴格按照以下輸出格式，每則推文獨立一段，格式一致，不可省略任何區塊**：\n\n"
        "TWEET_Separator_START\n"
        "SCORE: <數字0-50>\n"
        "SCORE_REASON: <繁中理由，40字以內>\n"
        "BODY_START\n"
        "## Core Summary（BLUF格式）\n"
        "[結論一句話]\n\n"
        "[2-3句支撐]\n\n"
        "[實踐意義]\n\n"
        "## Detailed Analysis\n"
        "### 1. <分析要點一>\n"
        "...\n\n"
        "### 2. <分析要點二>\n"
        "...\n\n"
        "## Key Knowledge Points\n"
        "- **<術語/方法/工具>**：<具體說明>\n\n"
        "## Why It Matters\n"
        "- **<價值連接>**：<具體說明>\n"
        "BODY_END\n"
        "TWEET_Separator_END\n"
    )

    payload = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "thinking": {"type": "enabled", "budget_tokens": THINKING_BUDGET},
        "system": system_prompt,
        "messages": messages,
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }

    try:
        import urllib.request
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        content = result.get("content", [])
        text_parts = []
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
        full_resp = "\n".join(text_parts)

    except Exception as e:
        print(f"  [API ERROR] {e}")
        full_resp = ""

    # Strip thinking before parsing separators
    clean_resp = strip_thinking_blocks(full_resp)

    # Split by separator
    raw_entries = re.split(r'TWEET_Separator_START', clean_resp)
    raw_entries = [e.strip() for e in raw_entries if e.strip() and 'SCORE:' in e]

    results = []
    for i, t in enumerate(tweets_batch):
        score = 0
        reason = "API失敗，請參考原文"
        body = ""

        if i < len(raw_entries):
            entry = raw_entries[i]
        else:
            entry = ""

        # 0-50 分制：支持多位數字
        sm = re.search(r'SCORE:\s*(\d+)', entry)
        if sm:
            score = int(sm.group(1))
            # 防止 M3 返回舊制的 1-5 分（極少見）
            if score <= 5:
                score = score * 10  # 1-5 → 10-50

        rm = re.search(
            r'SCORE_REASON:\s*(.+?)(?=\nBODY_START|\nTWEET_Separator_END)',
            entry, re.DOTALL
        )
        if rm:
            reason = rm.group(1).strip()[:80]
        else:
            reason = "評分失敗，請參考原文"

        bm = re.search(r'BODY_START\s*(.*?)BODY_END', entry, re.DOTALL)
        if bm:
            body = bm.group(1).strip()

        if not body:
            body = _fallback_body(t['handle'], t['tweet_block'][:500], score, reason)

        results.append({
            'score': score,
            'score_reason': reason,
            'body': body,
            'api_success': bool(bm),
        })

    return results


def _fallback_body(handle: str, text: str, score: int, reason: str) -> str:
    return (
        f"## Core Summary（BLUF格式）\n\n"
        f"[結論一句話]\n"
        f"這是來自 @{handle} 的推文分享。\n\n"
        f"[2-3句支撐]\n"
        f"推文內容涵蓋該領域的具體觀點或技術實踐。評分原因：{reason}。\n\n"
        f"[實踐意義]\n"
        f"讀者可參考原文進行日常開發或知識積累。\n\n"
        f"## Detailed Analysis\n\n"
        f"### 1. 內容定位\n"
        f"這則推文提供了可供後續整理的觀點或實作線索。\n\n"
        f"### 2. 使用邊界\n"
        f"若要將其升級為正式知識筆記，仍需補足作者背景、上下文與適用限制。\n\n"
        f"## Key Knowledge Points\n\n"
        f"- **@{handle}**: [Twitter 主頁](https://x.com/{handle})\n\n"
        f"## Why It Matters\n\n"
        f"- **應用場景**：可作為後續 `llm-wiki`、`note-update` 或 `inbox-triage` 的來源入口。\n"
    )


# ── Build Note ──────────────────────────────────────────────────────────────
def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).strip().hexdigest()[:16]

def yaml_quote(val) -> str:
    if val is None:
        return ""
    return str(val).replace('\\', '\\\\').replace('"', '\\"').replace('\r', ' ').replace('\n', ' ').strip()

def extract_title(block: str, handle: str, fallback: str = "") -> str:
    """Extract meaningful title from tweet block."""
    if fallback and len(fallback) >= 5:
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', fallback)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
        if len(clean) >= 5:
            return clean[:80]
    lines = [l.strip() for l in block.split('\n') if l.strip()]
    for line in lines:
        if len(line) < 5:
            continue
        if re.match(r'^[@#*_`]', line):
            continue
        if re.match(r'^https?://', line):
            continue
        if 'Published' in line[:20]:
            continue
        clean = re.sub(r'\*\*(.+?)\*\*', r'\1', line)
        clean = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', clean)
        if len(clean) >= 5:
            return clean[:80]
    return f"@{handle} 的推文"

def build_note(tweet_data: Dict, scored: Dict) -> Tuple[str, str]:
    """Build complete x-note2 markdown file content."""
    handle = tweet_data['handle']
    tweet_id = tweet_data['tweet_id']
    block = tweet_data['tweet_block']
    url = tweet_data['source_url'] or f"https://x.com/{handle}/status/{tweet_id}"
    author = tweet_data['author'] or handle
    captured_at = tweet_data['captured_at'] or DATE_STR
    capture_method = tweet_data['capture_method'] or "baoyu-fetch + CDP"

    score = scored['score']
    reason = scored['score_reason']
    body = scored['body']
    chash = content_hash(block)

    title = extract_title(block, handle, tweet_data.get('title_candidate', ''))
    slug_words = re.findall(r'[\w\u4e00-\u9fff]+', title)[:4]
    slug = ''.join(slug_words)[:25].strip('-_')
    slug_safe = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\-]', '', slug)
    if not slug_safe:
        slug_safe = tweet_id[-8:]
    filename = f"{DATE_STR}_x-note2_{handle}_{slug_safe}_{tweet_id[-6:]}.md"

    md = f"""---
title: "{yaml_quote(title)}"
source: "X.com @{handle}"
source_url: "{url}"
tweet_id: "{tweet_id}"
author: "{yaml_quote(author)}"
handle: "@{handle}"
captured_at: "{captured_at}"
capture_method: "{capture_method}"
content_hash: "sha256:{chash}"
engagement:
  views: 0
  likes: 0
  reposts: 0
  replies: 0
  bookmarks: 0
media_ids: []
score: {score}
score_reason: "{yaml_quote(reason)}"
tags:
  - x-note2
  - social-intel
  - "@{handle}"
sources:
  - "{url}"
type: "x-post-summary"
classification_path: "00-Inbox"
status: "inbox"
date: "{DATE_STR}"
processed_by: "x-note-inbox-upgrade"
---

# {title}

## Source Snapshot

- **Source URL**: {url}
- **Author**: {author}
- **Handle**: @{handle}
- **Post time**: {captured_at}
- **Engagement**:
  - Views: 0
  - Likes: 0
  - Reposts: 0
  - Replies: 0
  - Bookmarks: 0
- **Content hash**: sha256:{chash}
- **Capture method**: {capture_method}

{body}

## Reference

### Complete X Post Text

```text
{block}
```

### 相關資源與出處
- {url}

## Related Notes

- [[AGENTS.md|Pigo 專屬操作規範與路由規則]]
- [[file:///{LLM_WIKI}|llm-wiki 技能文檔]]
"""
    return filename, md


# ── Main ────────────────────────────────────────────────────────────────────
def main():
    sys.stdout.reconfigure(encoding='utf-8')
    print(f"=== x-note-inbox-upgrade | {DATE_STR} | threshold: >={SCORE_THRESHOLD} (0-50 scale) ===")
    print(f"VAULT: {VAULT}")
    print(f"AGENT: {AGENT}")
    print()

    tweets = collect_inbox_tweets()
    print(f"Collected: {len(tweets)} inbox tweets")
    for t in tweets:
        print(f"  @{t['handle']} | block={len(t['tweet_block'])} | {t['tweet_id']} | {t['filename'][:50]}")

    batches = [tweets[i:i+BATCH_SIZE] for i in range(0, len(tweets), BATCH_SIZE)]
    print(f"\nBatches: {len(batches)} x ~{BATCH_SIZE}")

    all_results: Dict[int, Dict] = {}
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {}
        for bi, batch in enumerate(batches):
            print(f"  Submitting batch {bi+1}/{len(batches)} ({len(batch)} tweets)...")
            fut = ex.submit(score_and_curate_batch, batch)
            futures[fut] = (bi, batch)

        for fut in as_completed(futures):
            bi, batch = futures[fut]
            try:
                results = fut.result()
                for i, res in enumerate(results):
                    all_results[bi * BATCH_SIZE + i] = res
                ok = sum(1 for r in results if r.get('api_success'))
                print(f"  Batch {bi+1}/{len(batches)} OK | {len(results)} scored | {ok} API OK")
            except Exception as e:
                print(f"  Batch {bi+1}/{len(batches)} ERROR: {e}")
                for i in range(len(batch)):
                    idx = bi * BATCH_SIZE + i
                    t = batch[i]
                    all_results[idx] = {
                        'score': 0,
                        'score_reason': f"批次錯誤: {e}",
                        'body': _fallback_body(t['handle'], t['tweet_block'][:500], 0, "批次錯誤"),
                        'api_success': False,
                    }

    # ── Write + Filter ───────────────────────────────────────────────────────
    print(f"\n=== Write + Filter (score >={SCORE_THRESHOLD}, 0-50 scale) ===")
    # 評分分佈（0-50 分制）
    bands = {"40-50": 0, "35-39": 0, "30-34": 0, "20-29": 0, "0-19": 0}
    written = []
    skipped = []

    for idx, t in enumerate(tweets):
        res = all_results.get(idx, {
            'score': 0,
            'score_reason': "No result",
            'body': _fallback_body(t['handle'], t['tweet_block'][:500], 0, "No result"),
            'api_success': False,
        })
        s = res['score']
        if s >= 40: bands["40-50"] += 1
        elif s >= 35: bands["35-39"] += 1
        elif s >= 30: bands["30-34"] += 1
        elif s >= 20: bands["20-29"] += 1
        else: bands["0-19"] += 1

        if res['score'] < SCORE_THRESHOLD:
            skipped.append((t, res))
            print(f"  [SKIP @{t['handle']}] score={res['score']} | {res['score_reason'][:40]}")
            continue

        filename, md = build_note(t, res)
        out_path = INBOX / filename
        out_path.write_text(md, encoding='utf-8')
        written.append((t, res, filename))
        api_tag = "OK" if res['api_success'] else "FALLBACK"
        print(f"  [WRITE @{t['handle']}] score={res['score']} | {api_tag} | {filename}")

    # ── Deduplicate by tweet_id ─────────────────────────────────────────────
    print(f"\n=== Deduplicate by tweet_id ===")
    by_tid = {}
    for t, res, fname in written:
        by_tid.setdefault(t['tweet_id'], []).append((t, res, fname))

    dedup_removed = 0
    for tid, entries in by_tid.items():
        if len(entries) <= 1:
            continue
        entries.sort(key=lambda x: x[1]['score'], reverse=True)
        winner = entries[0]
        for t, res, fname in entries[1:]:
            (INBOX / fname).unlink()
            print(f"  DEL(dup) @{t['handle']} tweet={tid} score={res['score']} | {fname[:50]}")
            dedup_removed += 1

    # ── STATUS ──────────────────────────────────────────────────────────────
    total_api = sum(1 for r in all_results.values() if r.get('api_success'))
    status_md = f"""# x-note-inbox-upgrade STATUS — {DATE_STR}

## 執行摘要

| 項目 | 值 |
|------|-----|
| 輸入檔案 | {len(tweets)} |
| 寫入檔案（score>={SCORE_THRESHOLD}） | {len(written) - dedup_removed} |
| 略過檔案（score<{SCORE_THRESHOLD}） | {len(skipped)} |
| 去重移除 | {dedup_removed} |
| API 成功率 | {total_api}/{len(tweets)} |
| 評分模型 | {MODEL} |
| 評分制 | 0-50 分 |
| 處理時間 | {NOW_STR} +08:00 |
| 閥門 | score >= {SCORE_THRESHOLD}（HARD RULE） |
| VAULT | {VAULT} |
| AGENT | {AGENT} |

## 評分分佈（0-50 分制）

| 分數區間 | 數量 | 寫入 |
|----------|------|------|
| 40-50 | {bands["40-50"]} | {'是' if bands["40-50"] >= SCORE_THRESHOLD else '否'} |
| 35-39 | {bands["35-39"]} | {'是' if bands["35-39"] >= SCORE_THRESHOLD else '否'} |
| 30-34 | {bands["30-34"]} | 否（<{SCORE_THRESHOLD}）|
| 20-29 | {bands["20-29"]} | 否 |
| 0-19  | {bands["0-19"]}  | 否 |

## 略過清單（score < {SCORE_THRESHOLD}）

| Handle | Tweet ID | Score | Reason |
|--------|----------|-------|--------|
"""
    for t, res, _ in skipped:
        status_md += f"| @{t['handle']} | {t['tweet_id']} | {res['score']} | {res['score_reason'][:60]} |\n"

    status_md += f"""
## 寫入清單（score >= {SCORE_THRESHOLD}）

| # | Handle | Tweet ID | Score | Reason | Body |
|---|--------|----------|-------|--------|------|
"""
    wi = 0
    for tid, entries in by_tid.items():
        entries.sort(key=lambda x: x[1]['score'], reverse=True)
        t, res, fname = entries[0]
        wi += 1
        body_tag = "OK" if res.get('api_success') else "FALLBACK"
        status_md += f"| {wi} | @{t['handle']} | {t['tweet_id'][-6:]} | {res['score']} | {res['score_reason'][:50]} | {body_tag} |\n"

    status_path = INBOX / f"STATUS_x-note-inbox-upgrade_{DATE_STR}.md"
    status_path.write_text(status_md, encoding='utf-8')
    print(f"\nSTATUS: {status_path}")

    print(f"\n=== Complete ===")
    print(f"Written: {len(written) - dedup_removed} | Skipped: {len(skipped)} | Dedup: {dedup_removed}")
    print(f"Score bands: {bands}")
    print(f"API success: {total_api}/{len(tweets)}")

    return status_md


if __name__ == "__main__":
    if not API_KEY:
        print("FATAL: No MINIMAX_API_KEY in ~/.pi/agent/auth.json")
        sys.exit(1)
    main()
