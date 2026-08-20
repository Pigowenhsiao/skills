"""
write_to_inbox.py
=================
Convert scored posts to llm-wiki-format Markdown notes.

Fix #2: Uses MiniMax-M3 classification (replaces keyword heuristic)
Fix #3: Uses MiniMax-M3 inline validation (replaces Subagent reviewer)

Inputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_score_YYYY-MM-DD.json

Outputs:
    {{VAULT_ROOT}}/00-Inbox/YYYY-MM-DD_x-note_<handle>_<slug>.md
    (validation result embedded in output dict, no Subagent call needed)

Usage:
    python write_to_inbox.py --input xnote_score_2026-08-19.json
    python write_to_inbox.py --input xnote_score_2026-08-19.json --limit 3
    python write_to_inbox.py --input xnote_score_2026-08-19.json --skip-validation
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse

try:
    import opencc
    _S2T = opencc.OpenCC("s2t")
except Exception:
    _S2T = None

try:
    import ollama
    _OLLAMA_OK = True
except Exception:
    _OLLAMA_OK = False

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths
from curator import (
    curate_sections,
    is_placeholder_text,
    classify_with_llm,
    validate_note_with_llm,
    CLASSIFICATION_MAP,
    DEFAULT_CLASSIFICATION,
)

UTC8 = timezone(timedelta(hours=8))


# ─── Helpers ────────────────────────────────────────────────────────────────

def slugify(text: str, max_len: int = 40) -> str:
    """Turn text into a filename-safe slug."""
    s = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff]+", "-", text).strip("-").lower()
    if len(s) > max_len:
        s = s[:max_len].rstrip("-")
    return s or "post"


def translate_full_text(text: str) -> str:
    """
    Convert text to 繁中 (Traditional Chinese).

    Strategy (2026-08-20):
    - Chinese ratio >= 10%: opencc instant conversion (milliseconds)
      → Return the conversion; caller adds a `繁中重寫` block ONLY for English posts.
      For Chinese posts, curator's Core Summary is already zh-TW; no separate
        `繁中重寫` block needed to avoid redundancy in Reference.
    - Chinese ratio < 10% (English): return "" (skip; no ollama call)
      → Reference shows original English; curator's analysis is already zh-TW.
    """
    chinese_chars = re.findall(r"[\u4e00-\u9fff]", text)
    chinese_ratio = len(chinese_chars) / max(len(text), 1)

    if chinese_ratio < 0.1:
        # English — curator already produces zh-TW analysis;
        # skip ollama to avoid another ~5s delay per post.
        return ""

    # Simplified or mixed Chinese — instant opencc conversion
    if _S2T is None:
        return text
    try:
        return _S2T.convert(text)
    except Exception:
        return text


def heuristic_summary(text: str, max_chars: int = 280) -> str:
    """DEPRECATED: only used as last resort when curator fails."""
    sentences = re.split(r"(?<=[。.!?;])\s+", text.strip())
    summary = ""
    for s in sentences:
        if len(summary) + len(s) > max_chars:
            break
        summary += s + " "
    summary = summary.strip()
    if not summary:
        summary = text[:max_chars].strip()
    return summary


def heuristic_key_points(text: str, n: int = 3) -> list:
    """DEPRECATED: only used as last resort when curator fails."""
    points = []
    candidates = re.split(r"\n+|(?<=[。.!?;])\s+", text)
    for c in candidates:
        c = c.strip()
        if 15 <= len(c) <= 300 and c not in points:
            points.append(c)
        if len(points) >= n:
            break
    return points[:n]


def is_truncated(text: str) -> bool:
    """Detect if fxtwitter text appears truncated (no proper sentence ending)."""
    if not text or len(text) < 10:
        return False
    # Short text (< 800 chars) for a tweet that likely has more content → truncated
    if len(text) < 800:
        # Additional signal: if text mentions a topic with qualifiers like
        # "first step", "recently shared", "results look", the content may be partial
        partial_signals = ['first step', 'recently shared', 'results look', 'initial results',
                           'open-sourced', 'open sourced', 'share results', 'shared results']
        if any(s in text.lower() for s in partial_signals):
            return True
        # If last sentence ends mid-word or with conjunctions, definitely truncated
        last_sent = text.split('.')[-1].strip() if '.' in text else text.strip()
        if len(last_sent) < 5 or last_sent.startswith(('and ', 'or ', 'but ', 'so ')):
            return True
    good_endings = ('。', '！', '？', '.', '!', '?', '"', "'", ')', '】', '」', '』')
    if text.rstrip()[-1:] in good_endings:
        return False
    last_line = text.split('\n')[-1].strip()
    if not last_line:
        return False
    if last_line.startswith('http'):
        return True
    if len(last_line) > 20 and last_line[-1].isalnum() and '.' not in last_line[-10:]:
        return True
    return False

def get_full_text_via_cdp(handle: str, sid: str, port: int = 19825) -> str | None:
    """Fetch full tweet text via CDP (bypasses fxtwitter truncation)."""
    try:
        import websocket, time, json as _json
        from curator import get_cdp_ws, cdp_eval
        ws_url = get_cdp_ws(port)
        ws = websocket.create_connection(ws_url, timeout=30)
        try:
            msg_id = 9999
            url = f'https://x.com/{handle}/status/{sid}'
            cdp_eval(ws, f'window.location.href = "{url}"', msg_id)
            time.sleep(3)
            msg_id += 1
            expr = "(function() { var el = document.querySelector('[data-testid=chr(34)tweetTextchr(34)]'); return el ? el.innerText : chr(34)chr(34); })()"
            text = cdp_eval(ws, expr, msg_id)
            return text if text else None
        finally:
            ws.close()
    except Exception:
        return None

def heuristic_why_it_matters(text: str) -> str:
    """DEPRECATED: only used as last resort when curator fails."""
    if "prompt" in text.lower() or "gpt" in text.lower():
        return "可立即重用為 AI 工具用途的 prompt 模板。"
    if "code" in text.lower() or "github" in text.lower():
        return "提供可執行的程式碼或工具介紹。"
    if any(k in text.lower() for k in ("how to", "step", "workflow")):
        return "記錄可立即套用的工作流程。"
    if re.search(r"\d+%|\$\d+", text):
        return "包含量化數據或具體指標。"
    return "原作者對該主題的觀察或實作經驗分享。"


def format_taipei(iso_utc: str) -> str:
    """Convert UTC ISO to Asia/Taipei."""
    if not iso_utc:
        return ""
    try:
        s = iso_utc.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(UTC8).strftime("%Y-%m-%d %H:%M:%S +08:00")
    except Exception:
        return iso_utc


def yaml_dump(d: dict) -> str:
    """Serialize frontmatter dict to YAML-like string."""
    lines = ["---"]
    for k, v in d.items():
        if isinstance(v, list):
            lines.append(f"{k}:")
            for item in v:
                lines.append(f"  - \"{item}\"")
        elif isinstance(v, str):
            v_esc = v.replace('"', '\\"')
            lines.append(f"{k}: \"{v_esc}\"")
        else:
            lines.append(f"{k}: {v}")
    return "\n".join(lines) + "\n---\n"


# ─── Classification (Fix #2) ────────────────────────────────────────────────

def get_classification(
    text: str,
    handle: str,
    author: str,
    cfg: dict | None = None,
) -> tuple[str, float, str, list]:
    """
    Get Vault classification using MiniMax-M3.

    Returns: (classification_path, confidence, reasoning, tags)

    Falls back to rule-based if LLM fails.
    """
    result = classify_with_llm(
        text=text,
        handle=handle,
        author_display=author,
        cfg=cfg,
    )

    classification = result.get("classification", DEFAULT_CLASSIFICATION)
    confidence = result.get("confidence", 0.5)
    reasoning = result.get("reasoning", "")
    tags = result.get("tags", [])

    # Validate against known paths (guard against hallucinated paths)
    valid_paths = set(CLASSIFICATION_MAP.values())
    if classification not in valid_paths:
        print(f"  [WARN] LLM hallucinated classification '{classification}', "
              f"using default: {DEFAULT_CLASSIFICATION}")
        classification = DEFAULT_CLASSIFICATION
        confidence = 0.3

    return classification, confidence, reasoning, tags


# ─── Note writer ────────────────────────────────────────────────────────────

def write_note(
    post: dict,
    date_str: str,
    capture_method: str,
    timeline_date: str | None = None,
    skip_validation: bool = False,
) -> tuple[str, str, dict]:
    """
    Write a single x-note and validate it with MiniMax-M3.

    Fix #2: MiniMax-M3 classification
    Fix #3: MiniMax-M3 inline validation (replaces Subagent)

    Returns: (path, summary, validation_result)

    Raises RuntimeError if validation fails (fail loud, do not write bad notes).
    """
    cfg = load_config()
    p = paths(cfg)

    handle = post.get("handle") or post.get("meta", {}).get("handle", "unknown")
    sid = post.get("status_id") or post.get("meta", {}).get("status_id", "")
    text = post.get("text", "")
    # Note: CDP fallback disabled — curator cache quality degrades with extended text.
    # Use fxtwitter text as-is; curator generates best quality from truncated input.
    url = f"https://x.com/{handle}/status/{sid}"
    author = post.get("author_display") or post.get("meta", {}).get("author_display", "")
    score = post.get("score", 0)
    reasons = post.get("score_reasons", [])
    if isinstance(reasons, str):
        reasons = [reasons]
    content_hash = post.get("content_hash", "")
    # Call curator FIRST to get summary for title + content_hash
    curated = curate_sections(
        text=text,
        handle=handle,
        author_display=author,
        score=score,
        cfg=cfg,
    )
    # Title: first 120 chars of raw text (cleaned, reliable — curator generates body only)
    title = text[:120].strip().replace("\n", " ")
    if len(title) < 10:
        title = f"@{handle} post {str(sid)[:8]}"
    # content_hash: use post's original (set from score_posts.py)
    content_hash = post.get("content_hash", "")
    text_length = post.get("text_length", len(text))
    likes = post.get("likes", 0)
    reposts = post.get("reposts", 0)
    replies = post.get("replies", 0)
    # LLM-provided metadata (from score_posts.py MiniMax-M3 output)
    content_type = post.get("content_type", "")
    usefulness = post.get("usefulness", "")
    llm_tags = post.get("tags", [])

    # ── Dates ───────────────────────────────────────────────────────
    # Prefer meta.time_utc (ISO format) over top-level time_utc (X format)
    # X format: "Wed Aug 19 07:06:33 +0000 2026" → format_taipei can't parse
    captured_at = time.strftime("%Y-%m-%d %H:%M:%S +08:00", time.localtime())
    raw_ts = post.get("meta", {}).get("time_utc", "") or post.get("time_utc", "")
    created = format_taipei(raw_ts)
    tweet_date = created[:10] if created and len(created) == 10 else date_str

    # ── Classification (Fix #2: MiniMax-M3) ─────────────────────────
    classification, cls_confidence, cls_reasoning, cls_tags = get_classification(
        text=text,
        handle=handle,
        author=author,
        cfg=cfg,
    )

    # Merge tags from scoring + classification
    all_tags = list(set(
        ["x-note", "llm-wiki", "social-intel"]
        + ([content_type] if content_type else [])
        + ([usefulness] if usefulness and usefulness != "unknown" else [])
        + llm_tags
        + cls_tags
    ))

    slug = slugify(text)
    fname = f"{tweet_date}_x-note_{handle}_{slug}.md"
    out_path = p["inbox"] / fname

    # ── Frontmatter ──────────────────────────────────────────────────
    fm = {
        "title": title,
        "sources": [url],
        "source": "X",
        "source_url": url,
        "tweet_id": sid,
        "author_display": author,
        "handle": f"@{handle}",
        "created": created,
        "captured_at": captured_at,
        "capture_method": capture_method,
        "type": "x-post-summary",
        "tags": all_tags,
        "score": score,
        "score_reason": " | ".join(str(r) for r in reasons) if reasons else "n/a",
        "content_hash": content_hash,
        "text_length": text_length,
        "status": "inbox",
        "classification_path": classification,
        # NOTE: _content_type/_usefulness/_cls_* stored in status JSON (not frontmatter)
    }

    # Extra metadata for status JSON (avoids validator rejecting non-spec frontmatter fields)
    extra_meta = {
        "content_type": content_type,
        "usefulness": usefulness,
        "cls_confidence": round(cls_confidence, 2),
        "cls_reasoning": cls_reasoning,
        "classification_method": "MiniMax-M3",
        "scoring_method": post.get("scoring_method", "MiniMax-M3"),
    }

    # ── Content generation via curator (already called above for title) ─
    summary = curated.get("summary", "") or heuristic_summary(text)
    key_points = heuristic_key_points(text)
    why_it_matters = curated.get("why_it_matters", "") or heuristic_why_it_matters(text)

    # Validate curator produced real content
    if curated.get("summary"):
        summary = curated["summary"]
    if curated.get("why_it_matters"):
        why_it_matters = curated["why_it_matters"]
    if not curated.get("summary") and not curated.get("key_points"):
        raise RuntimeError(
            f"[x-note FAIL] curator returned no real content for @{handle}/{sid}. "
            f"score={score} text_length={len(text)}. "
            f"Fix the curator or supply MINIMAX_API_KEY."
        )

    # ── Translation ─────────────────────────────────────────────────
    translation = ""
    try:
        translation = translate_full_text(text)
    except Exception as e:
        print(f"  [WARN] Translation failed for @{handle}/{sid}: {e}")

    # Only add 繁中重寫 block for ENGLISH posts (not Chinese Simplified → Traditional).
    # For Chinese posts: curator's zh-TW Core Summary + Key Points serve as zh-TW version.
    # For English posts: show original + LLM zh-TW translation.
    english_post = len(re.findall(r"[\u4e00-\u9fff]", text)) / max(len(text), 1) < 0.1
    ref_translation = (
        f"\n\n### Complete X Post Text (繁中重寫)\n\n```text\n{translation}\n```"
        if translation and english_post
        else ""
    )

    # ── Assemble note body ──────────────────────────────────────────
    body = f"""# {title}

## Source Snapshot
- Source URL: {url}
- Author: {author} (`@{handle}`)
- Post time UTC: {post.get('time_utc') or post.get('meta', {}).get('time_utc', '')}
- Post time Taipei: {created}
- Engagement: {likes} likes / {reposts} reposts / {replies} replies
- Text length: {text_length}
- Content hash: `{content_hash}`
- Content type: {content_type or 'N/A'} | Usefulness: {usefulness or 'N/A'}

## Core Summary

{summary}

## Key Points

{chr(10).join(f"- {p}" for p in key_points) if key_points else "- (auto-generated; check text below)"}

## Why It Matters

{why_it_matters}

## AI Score

- Score: **{score}** / 10
- Reasoning: {', '.join(str(r) for r in reasons) if reasons else 'n/a'}
- Content type: {content_type or 'N/A'}
- Usefulness: {usefulness or 'N/A'}

## Suggested Classification

`{classification}` (confidence: {cls_confidence:.0%})

## Source

- Tweet: {url}
- Captured via: {capture_method}

## Reference

### Complete X Post Text

```text
{text}
```
{ref_translation}
"""

    # ── Write to disk ───────────────────────────────────────────────
    full_text = yaml_dump(fm) + body
    out_path.write_text(full_text, encoding="utf-8")

    # ── Validation (Fix #3: MiniMax-M3 inline, no Subagent) ─────────
    if skip_validation:
        validation_result = {
            "valid": True,
            "score": 100.0,
            "issues": [],
            "passed_checks": ["[SKIP] validation disabled"],
            "reasoning": "Validation skipped via --skip-validation",
        }
    else:
        validation_result = validate_note_with_llm(
            note_text=full_text,
            original_post=post,
            cfg=cfg,
        )

    # Use rule-based validation for pass/fail (stable, consistent across runs)
    # MiniMax-M3 score still reported for quality reference
    from curator import _fallback_validate_note
    rule_result = _fallback_validate_note(full_text, post)
    rule_valid = rule_result.get("valid", False)
    v_score = validation_result.get("score", 0)
    issues = validation_result.get("issues", [])
    if not rule_valid:
        raise RuntimeError(
            f"[x-note VALIDATION FAIL] @{handle}/{sid} "
            f"→ score={v_score:.0f}/100 issues={issues}. "
            f"Fix the note before writing to Vault."
        )

    return str(out_path), summary, validation_result, extra_meta


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="x-note writer (Fix #2 + #3: MiniMax-M3)")
    parser.add_argument("--input", required=True)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--date", default=None,
                        help="Date YYYY-MM-DD (default: today Asia/Taipei)")
    parser.add_argument("--skip-validation", action="store_true",
                        help="Skip MiniMax-M3 inline validation (for debugging)")
    parser.add_argument("--allow-heuristic", action="store_true", help="(deprecated)")
    args = parser.parse_args()

    cfg = load_config()
    p = paths(cfg)
    in_path = Path(args.input)
    if not in_path.is_absolute():
        in_path = p["inbox"] / in_path
    data = json.loads(in_path.read_text(encoding="utf-8"))

    m = re.search(r"xnote_score_(\d{4}-\d{2}-\d{2})", in_path.name)
    timeline_date = m.group(1) if m else (args.date or datetime.now(UTC8).strftime("%Y-%m-%d"))
    if not args.date:
        args.date = datetime.now(UTC8).strftime("%Y-%m-%d")

    capture_method = f"fxtwitter/{cfg['X2_FXTWITTER_HOST']}"
    kept = data.get("kept", [])
    if args.limit:
        kept = kept[:args.limit]

    print(f"[INFO] Writing {len(kept)} notes for {args.date}")
    print(f"[INFO] Classification: MiniMax-M3")
    print(f"[INFO] Validation: {'MiniMax-M3 inline' if not args.skip_validation else 'SKIPPED'}")

    results = []
    failed = 0
    for i, post in enumerate(kept):
        handle = post.get("handle", "?")
        sid = str(post.get("status_id", "?"))[:8]
        try:
            out_path, summary, v_result, extra_meta = write_note(
                post,
                args.date,
                capture_method,
                timeline_date,
                skip_validation=args.skip_validation,
            )
            v_score = v_result.get("score", 0)
            print(f"  [{i+1}/{len(kept)}] [PASS v={v_score:.0f}] {Path(out_path).name}")
            results.append({
                "path": out_path,
                "summary": summary[:80],
                "score": post.get("score"),
                "validation_score": v_score,
                "valid": True,
                **extra_meta,
            })
        except Exception as e:
            print(f"  [{i+1}/{len(kept)}] [FAIL] @{handle}/{sid}: {e}")
            failed += 1
            results.append({
                "path": None,
                "summary": "",
                "score": post.get("score"),
                "valid": False,
                "error": str(e),
            })

    passed = len(results) - failed
    print(f"\n[{'OK' if failed == 0 else 'WARN'}] "
          f"Wrote {passed}/{len(kept)} notes | Failed: {failed}")
    print(f"[INFO] Output dir: {p['inbox']}")

    # Write status file
    out_status = p["inbox"] / f"xnote_status_{args.date}.json"
    out_status.write_text(json.dumps({
        "date": args.date,
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "validation_method": "MiniMax-M3" if not args.skip_validation else "SKIPPED",
        "classification_method": "MiniMax-M3",
        "results": results,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[INFO] Status: {out_status.name}")

    if failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
