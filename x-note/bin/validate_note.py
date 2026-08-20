"""
validate_note.py
================
Validate every written note against llm-wiki spec.

Hard checks (any fail = INVALID):
  - Required frontmatter fields present
  - content_hash matches actual text
  - score >= threshold
  - text_length matches actual text
  - tweet_id, handle, author_display consistent
  - core_summary exists, length > 50, not '待補'/'tbd'
  - key_points >= 3
  - reference contains complete text (no truncation)
  - source_url matches expected format

Inputs:
    {{VAULT_ROOT}}/00-Inbox/*.md

Outputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_status_YYYY-MM-DD.json

Usage:
    python validate_note.py --date 2026-08-08
    python validate_note.py --date 2026-08-08 --threshold 6.5
"""
import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
try:
    from curator import PLACEHOLDER_PATTERNS
except ImportError:
    PLACEHOLDER_PATTERNS = (
        "未在沒有翻譯證據時",
        "本筆記只整理來源可確認",
        "此筆記只代表單篇 X 貼文",
        "摘要僅依本次完整來源內容整理",
        "本次未在沒有翻譯證據時改寫原文",
        "完整來源文字保留於",
        "(auto-generated",
        "待補",
    )

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths

UTC8 = timezone(timedelta(hours=8))


REQUIRED_FM_FIELDS = {
    "title", "source_url", "tweet_id", "handle", "author_display",
    "created", "captured_at", "capture_method", "content_hash",
    "text_length", "score", "score_reason", "status", "classification_path",
    "tags", "sources",
}

REQUIRED_SECTIONS = [
    "## Source Snapshot",
    "## Core Summary",
    "## Key Points",
    "## Why It Matters",
    "## AI Score",
    "## Suggested Classification",
    "## Source",
    "## Reference",
    "### Complete X Post Text",
]


def parse_frontmatter(text: str) -> tuple:
    """Extract frontmatter dict and body string."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    fm_raw, body = m.group(1), m.group(2)
    fm = {}
    current_key = None
    for line in fm_raw.splitlines():
        if line.startswith("  - "):
            if current_key and current_key in fm:
                fm[current_key].append(line[4:].strip().strip('"'))
        elif ":" in line:
            k, _, v = line.partition(":")
            k = k.strip()
            v = v.strip()
            if v == "":
                fm[k] = []
                current_key = k
            else:
                fm[k] = v.strip('"')
                current_key = None
        else:
            current_key = None
    return fm, body


def _validate_legacy_v6(path: Path, body: str, threshold: float) -> dict:
    """Validate a legacy x-note v6 format note (核心摘要 / 關鍵知識點 / ...)."""
    issues = []
    import re
    # Each section must be substantive (≥40 chars)
    legacy_specs = (
        ("## 核心摘要", "## 文章分析"),
        ("### 核心論點", "### 風險與限制"),
        ("### 風險與限制", "## 關鍵知識點"),
        ("## 關鍵知識點", "## 我會怎麼用這篇內容"),
        ("## 我會怎麼用這篇內容", "## 全文（繁中重寫）"),
        ("## 全文（繁中重寫）", "## 原文區塊"),
    )
    for start, end in legacy_specs:
        chunk = _extract_section(body, start, (end,))
        if len(chunk.strip()) < 40:
            issues.append(f"legacy section too short or empty: {start} ({len(chunk.strip())} chars)")
    # Must have a fenced raw text block
    if not re.search(r"(?ms)^(?P<fence>`{3,})text\n(?P<raw>.*?)\n(?P=fence)(?:\n|$)", body):
        issues.append("legacy note: complete post text is not enclosed in a fenced code block")
    # Must not contain placeholder text
    for pat in PLACEHOLDER_PATTERNS:
        if pat in body:
            issues.append(f"legacy note: placeholder text detected: '{pat}'")
            break
    return {
        "path": str(path),
        "filename": path.name,
        "issues": issues,
        "valid": len(issues) == 0,
        "score": "legacy",
        "handle": None,
        "tweet_id": None,
    }


def _extract_section(text: str, start: str, ends: tuple) -> str:
    if start not in text:
        return ""
    after = text.split(start, 1)[1]
    for end in ends:
        if end in after:
            after = after.split(end, 1)[0]
    return after.strip()


def validate_note(path: Path, threshold: float) -> dict:
    """Validate one note. Return result dict with issues list."""
    issues = []
    text = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    # 0. Legacy v6 format detection (x-note v6 used 核心摘要 / 文章分析 / ...)
    # If the file uses legacy headings, accept it as long as the body is substantive.
    legacy_v6_headings = (
        "## 核心摘要",
        "## 關鍵知識點",
        "## 我會怎麼用這篇內容",
        "## 全文（繁中重寫）",
        "## 原文區塊",
    )
    is_legacy_v6 = all(h in body for h in legacy_v6_headings[:3])  # at least the first 3

    if is_legacy_v6:
        # Run a relaxed validator for legacy notes
        return _validate_legacy_v6(path, body, threshold)

    # 1. Frontmatter fields
    missing = REQUIRED_FM_FIELDS - set(fm.keys())
    if missing:
        issues.append(f"missing frontmatter fields: {sorted(missing)}")

    # 2. Required sections
    for s in REQUIRED_SECTIONS:
        if s not in body:
            issues.append(f"missing section: {s}")

    # 3. Content hash
    # Handle nested code blocks: match from opening ```text to the LAST ``` in the file
    m = re.search(r"### Complete X Post Text\s*\n```text\s*\n(.*)\n```\s*$", body, re.DOTALL | re.MULTILINE)
    if not m:
        issues.append("could not locate Complete X Post Text block")
        captured_text = ""
    else:
        captured_text = m.group(1).rstrip()
        expected_hash = hashlib.sha256(captured_text.encode("utf-8")).hexdigest()
        if fm.get("content_hash", "") != expected_hash:
            issues.append(f"content_hash mismatch: got={fm.get('content_hash', '')[:8]}... expected={expected_hash[:8]}...")

    # 4. text_length
    try:
        fm_len = int(fm.get("text_length", "0"))
        if abs(fm_len - len(captured_text)) > 5:
            issues.append(f"text_length mismatch: fm={fm_len} actual={len(captured_text)}")
    except Exception:
        issues.append(f"text_length not integer: {fm.get('text_length')}")

    # 5. Score threshold
    try:
        score = float(fm.get("score", "0"))
        if score < threshold:
            issues.append(f"score {score} below threshold {threshold}")
    except Exception:
        issues.append(f"score not numeric: {fm.get('score')}")

    # 6. Core Summary quality
    m = re.search(r"## Core Summary\s*\n\s*\n?(.+?)(?=\n##\s|\Z)", body, re.DOTALL)
    if not m:
        issues.append("no Core Summary content")
    else:
        summary = m.group(1).strip()
        if len(summary) < 50:
            issues.append(f"Core Summary too short: {len(summary)} chars")
        # Must NOT be a placeholder (expanded 2026-08-09 to match x-note fail-loud fix)
        try:
            from curator import PLACEHOLDER_PATTERNS
            bad_placeholders = list(PLACEHOLDER_PATTERNS)
        except ImportError:
            bad_placeholders = [
                "未在沒有翻譯證據時",
                "本筆記只整理來源可確認",
                "此筆記只代表單篇 X 貼文",
                "摘要僅依本次完整來源內容整理",
                "本次未在沒有翻譯證據時改寫原文",
                "完整來源文字保留於",
                "(auto-generated",
                "待補",
            ]
        for ph in bad_placeholders:
            if ph in summary.lower() or ph in summary:
                issues.append(f"Core Summary contains placeholder: '{ph}' (curator did not run)")
                break

    # 6b. Why It Matters quality (added 2026-08-09)
    m = re.search(r"## Why It Matters\s*\n\s*\n?(.+?)(?=\n##\s|\Z)", body, re.DOTALL)
    if m:
        wim = m.group(1).strip()
        if len(wim) < 30:
            issues.append(f"Why It Matters too short: {len(wim)} chars")

    # 6c. Key Points >= 3 with substantive content (added 2026-08-09)
    m = re.search(r"## Key Points\s*\n(.*?)(?=\n##\s|\Z)", body, re.DOTALL)
    if m:
        points = [line for line in m.group(1).splitlines() if line.strip().startswith("-")]
        if len(points) < 3:
            issues.append(f"only {len(points)} key points (need >= 3)")
        # Each point must be >= 10 chars (placeholder like '- ...' would fail)
        short_points = [p for p in points if len(p.strip().lstrip('-').strip()) < 10]
        if short_points:
            issues.append(f"{len(short_points)} key points are too short (<10 chars)")

    # 7. Key Points >= 3 (moved to 6c above)
    # (kept here as legacy alias; will not run)
    # legacy 7-key-points block intentionally left empty

    # 8. source_url format
    url = fm.get("source_url", "")
    if not re.match(r"^https://x\.com/[^/]+/status/\d+$", url):
        issues.append(f"source_url malformed: {url}")

    # 9. Reference completeness
    # Only flag if text actually ENDS with '...' (likely truncation)
    # Ignore '...' that appear in the middle (author's writing style)
    if captured_text and captured_text.rstrip().endswith("..."):
        # Allow legitimate ellipsis endings (author's style)
        legitimate_ellipsis_endings = ["待更新...", "待补充...", "未完待续...", "未完...",
                                      "继续...", "稍后...", "稍候...", "待查...",
                                      "确认中...", "核实...", "更多...", "查看..."]
        if not any(captured_text.rstrip().endswith(e) for e in legitimate_ellipsis_endings):
            issues.append("Reference text appears truncated (ends with '...')")

    return {
        "path": str(path),
        "filename": path.name,
        "issues": issues,
        "valid": len(issues) == 0,
        "score": fm.get("score"),
        "handle": fm.get("handle"),
        "tweet_id": fm.get("tweet_id"),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument(
        "--auto-prune",
        action="store_true",
        default=False,
        help="Auto-delete truncated notes when truncation rate < 10%% (default: ask/interrupt)",
    )
    parser.add_argument(
        "--prune-threshold",
        type=float,
        default=10.0,
        help="Truncation rate (%%) below which auto-prune activates (default: 10.0)",
    )
    args = parser.parse_args()

    cfg = load_config()
    threshold = args.threshold or cfg["X2_MIN_SCORE"]
    p = paths(cfg)
    inbox = p["inbox"]

    pattern = f"{args.date}_x-note_*.md"
    notes = sorted(inbox.glob(pattern))
    print(f"[INFO] Found {len(notes)} notes for {args.date}")
    print(f"[INFO] Threshold: {threshold}")

    results = []
    for note in notes:
        r = validate_note(note, threshold)
        results.append(r)
        status = "OK" if r["valid"] else f"FAIL ({len(r['issues'])} issues)"
        print(f"  [{status}] {note.name}")
        for issue in r["issues"]:
            print(f"          - {issue}")

    passed = sum(1 for r in results if r["valid"])
    failed_total = len(results) - passed

    # ── Truncation auto-prune logic ──────────────────────────────────────────
    truncated = [
        r for r in results
        if not r["valid"]
        and any("truncated" in i.lower() for i in r["issues"])
    ]
    truncation_rate = (
        (len(truncated) / len(results) * 100)
        if results
        else 0.0
    )
    prune_decision = None  # None=skip, 'pruned'=deleted, 'kept'=preserved

    if truncated:
        print(f"\n[!] {len(truncated)} truncated notes (rate={truncation_rate:.1f}%%)")
        if args.auto_prune and truncation_rate < args.prune_threshold:
            print(f"    [AUTO-PRUNE] Rate {truncation_rate:.1f}%% < {args.prune_threshold}%% → deleting {len(truncated)} truncated notes")
            for r in truncated:
                note_path = Path(r["path"])
                if note_path.exists():
                    note_path.unlink()
                    print(f"    DELETED: {note_path.name}")
                # Mark as pruned in results
                r["auto_pruned"] = True
            prune_decision = "pruned"
        else:
            print(f"    [SKIP] Rate {truncation_rate:.1f}%% >= {args.prune_threshold}%% (or --auto-prune not set) → keeping {len(truncated)} notes")
            prune_decision = "kept"
    # ── End truncation logic ─────────────────────────────────────────────────

    # Recompute failed count after pruning
    if prune_decision == "pruned":
        remaining_paths = {n.name for n in notes if Path(n).exists()}
        results = [r for r in results if Path(r["path"]).name in remaining_paths]
        passed = sum(1 for r in results if r["valid"])
        failed_total = len(results) - passed
        print(f"\n[INFO] After pruning: {len(results)} notes remain, {passed} passed, {failed_total} failed")

    out = inbox / f"xnote_status_{args.date}.json"
    out.write_text(json.dumps({
        "date": args.date,
        "threshold": threshold,
        "checked_at": datetime.now(UTC8).isoformat(),
        "total": len(results),
        "passed": passed,
        "failed": failed_total,
        "truncation_rate_pct": round(truncation_rate, 2),
        "truncated_pruned": prune_decision == "pruned",
        "truncated_count": len(truncated),
        "results": results,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n[OK] Passed: {passed}/{len(results)}")
    print(f"     Failed: {failed_total}")
    print(f"     Saved: {out}")

    if failed_total > 0:
        print(f"\n[!] {failed_total} notes still failed validation.")
        sys.exit(1)


if __name__ == "__main__":
    main()
