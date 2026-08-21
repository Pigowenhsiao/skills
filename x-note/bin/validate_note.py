"""
validate_note.py
================
Validate x-note notes against llm-wiki spec.

Fix #3: Uses MiniMax-M3 inline validation by default (replaces Subagent reviewer).

Inputs:
    {{VAULT_ROOT}}/00-Inbox/YYYY-MM-DD_x-note_*.md

Outputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_status_YYYY-MM-DD.json

Usage:
    python validate_note.py --date 2026-08-19
    python validate_note.py --date 2026-08-19 --use-rules
    python validate_note.py --date 2026-08-19 --auto-prune
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
from config_loader import load_config, paths
from curator import (
    validate_note_with_llm,
    _fallback_validate_note,
    PLACEHOLDER_PATTERNS,
)

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


def validate_note_rule_based(note_path: Path, threshold: float) -> dict:
    """
    Rule-based validation (fast, no LLM call).
    Used as fallback when MiniMax-M3 is unavailable or --use-rules is set.
    """
    issues = []
    passed = []
    text = note_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)

    # Frontmatter fields
    missing = REQUIRED_FM_FIELDS - set(fm.keys())
    if missing:
        issues.append(f"missing frontmatter fields: {sorted(missing)}")
    else:
        passed.append("[OK] all required frontmatter fields")

    # Required sections
    for s in REQUIRED_SECTIONS:
        if s in body:
            passed.append(f"[OK] {s}")
        else:
            issues.append(f"[FAIL] missing section: {s}")

    # Content hash
    m = re.search(r"### Complete X Post Text\s*\n```text\s*\n(.*)\n```\s*$",
                  body, re.DOTALL | re.MULTILINE)
    if not m:
        issues.append("could not locate Complete X Post Text block")
        captured_text = ""
    else:
        captured_text = m.group(1).rstrip()
        expected_hash = hashlib.sha256(captured_text.encode("utf-8")).hexdigest()
        if fm.get("content_hash", "") != expected_hash:
            issues.append(f"content_hash mismatch: got={fm.get('content_hash', '')[:8]}... "
                          f"expected={expected_hash[:8]}...")
        else:
            passed.append("[OK] content_hash matches")

    # text_length
    try:
        fm_len = int(fm.get("text_length", "0"))
        if abs(fm_len - len(captured_text)) > 5:
            issues.append(f"text_length mismatch: fm={fm_len} actual={len(captured_text)}")
        else:
            passed.append("[OK] text_length matches")
    except Exception:
        issues.append(f"text_length not integer: {fm.get('text_length')}")

    # Score threshold
    try:
        score_val = float(fm.get("score", "0"))
        if score_val < threshold:
            issues.append(f"score {score_val} below threshold {threshold}")
        else:
            passed.append(f"[OK] score {score_val} >= {threshold}")
    except Exception:
        issues.append(f"score not numeric: {fm.get('score')}")

    # Core Summary quality
    m = re.search(r"## Core Summary\s*\n\s*\n?(.+?)(?=\n##\s|\Z)", body, re.DOTALL)
    if not m:
        issues.append("[FAIL] no Core Summary content")
    else:
        summary = m.group(1).strip()
        if len(summary) < 50:
            issues.append(f"[FAIL] Core Summary too short: {len(summary)} chars")
        else:
            passed.append(f"[OK] Core Summary length={len(summary)}")

        for ph in PLACEHOLDER_PATTERNS:
            if ph in summary.lower() or ph in summary:
                issues.append(f"[FAIL] Core Summary contains placeholder: '{ph}'")
                break

    # Why It Matters quality
    m = re.search(r"## Why It Matters\s*\n\s*\n?(.+?)(?=\n##\s|\Z)", body, re.DOTALL)
    if m:
        wim = m.group(1).strip()
        if len(wim) < 30:
            issues.append(f"[WARN] Why It Matters too short: {len(wim)} chars")
        else:
            passed.append(f"[OK] Why It Matters length={len(wim)}")

    # Key Points >= 3
    m = re.search(r"## Key Points\s*\n(.*?)(?=\n##\s|\Z)", body, re.DOTALL)
    if m:
        points = [line for line in m.group(1).splitlines()
                  if line.strip().startswith("-")]
        if len(points) < 3:
            issues.append(f"[FAIL] only {len(points)} key points (need >= 3)")
        else:
            passed.append(f"[OK] Key Points {len(points)} >= 3")
            short_points = [p for p in points
                            if len(p.strip().lstrip("-").strip()) < 10]
            if short_points:
                issues.append(f"[WARN] {len(short_points)} key points too short (<10 chars)")
    else:
        issues.append("[FAIL] no Key Points section")

    # source_url format
    url = fm.get("source_url", "")
    if not re.match(r"^https://x\.com/[^/]+/status/\d+$", url):
        issues.append(f"[WARN] source_url malformed: {url}")
    else:
        passed.append("[OK] source_url format valid")

    valid = len([i for i in issues if i.startswith("[FAIL]")]) == 0
    rule_score = 100.0 if valid else max(0, 100 - len(issues) * 10)

    return {
        "path": str(note_path),
        "filename": note_path.name,
        "issues": issues,
        "passed_checks": passed,
        "valid": valid,
        "score": rule_score,
        "score": fm.get("score"),
        "handle": fm.get("handle"),
        "tweet_id": fm.get("tweet_id"),
        "validation_method": "rule-based",
    }


def main():
    parser = argparse.ArgumentParser(description="x-note validator (Fix #3: MiniMax-M3)")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument(
        "--use-rules",
        action="store_true",
        help="Force rule-based validation (skip MiniMax-M3)",
    )
    parser.add_argument(
        "--auto-prune",
        action="store_true",
        default=False,
        help="Auto-delete truncated notes when truncation rate < 10%%",
    )
    parser.add_argument(
        "--prune-threshold",
        type=float,
        default=10.0,
        help="Truncation rate (%%) below which auto-prune activates",
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
    print(f"[INFO] Method: {'Rule-based' if args.use_rules else 'MiniMax-M3 inline'}")

    results = []
    for note in notes:
        # Read note text and frontmatter
        note_text = note.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(note_text)

        # Reconstruct minimal post dict for LLM validation
        original_post = {
            "text": "",
            "handle": fm.get("handle", "").lstrip("@"),
            "author_display": fm.get("author_display", ""),
            "score": float(fm.get("score", 0)),
            "status_id": fm.get("tweet_id", ""),
            "content_hash": fm.get("content_hash", ""),
            "text_length": int(fm.get("text_length", 0)),
            "time_utc": fm.get("created", ""),
            "likes": 0, "reposts": 0, "replies": 0,
        }

        # Extract original text from the Reference block
        m = re.search(r"### Complete X Post Text\s*\n```text\s*\n(.*)\n```\s*$",
                      body, re.DOTALL | re.MULTILINE)
        if m:
            original_post["text"] = m.group(1).rstrip()

        if args.use_rules:
            r = validate_note_rule_based(note, threshold)
        else:
            # Fix #3: MiniMax-M3 inline validation
            r = validate_note_with_llm(note_text=note_text, original_post=original_post, cfg=cfg)
            r["filename"] = note.name
            r["path"] = str(note)

        results.append(r)

        status = "OK" if r.get("valid", False) else f"FAIL ({len(r.get('issues', []))} issues)"
        v_score = r.get("score", 0)
        v_method = r.get("validation_method", "MiniMax-M3")
        print(f"  [{status} v={v_score:.0f}%] {note.name} [{v_method}]")
        for issue in r.get("issues", []):
            print(f"          - {issue}")

    passed = sum(1 for r in results if r.get("valid", False))
    failed_total = len(results) - passed

    # Truncation auto-prune
    truncated = [
        r for r in results
        if not r.get("valid", False)
        and any("truncated" in i.lower() for i in r.get("issues", []))
    ]
    truncation_rate = (
        (len(truncated) / len(results) * 100) if results else 0.0
    )
    prune_decision = None

    if truncated:
        print(f"\n[!] {len(truncated)} truncated notes (rate={truncation_rate:.1f}%%)")
        if args.auto_prune and truncation_rate < args.prune_threshold:
            print(f"    [AUTO-PRUNE] Deleting {len(truncated)} truncated notes...")
            for r in truncated:
                np = Path(r["path"])
                if np.exists():
                    np.unlink()
                    print(f"    DELETED: {np.name}")
                r["auto_pruned"] = True
            prune_decision = "pruned"
        else:
            print(f"    [SKIP] Keeping {len(truncated)} truncated notes")
            prune_decision = "kept"

    if prune_decision == "pruned":
        remaining = {n.name for n in notes if Path(n).exists()}
        results = [r for r in results if Path(r["path"]).name in remaining]
        passed = sum(1 for r in results if r.get("valid", False))
        failed_total = len(results) - passed

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
        "validation_method": "rule-based" if args.use_rules else "MiniMax-M3",
        "results": results,
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\n{'='*60}")
    print(f"[RESULT] Passed: {passed}/{len(results)}")
    print(f"         Failed: {failed_total}")
    print(f"         Validation: {'Rule-based' if args.use_rules else 'MiniMax-M3 inline'}")
    print(f"         Status: {out}")
    print(f"{'='*60}")

    if failed_total > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
