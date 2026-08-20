"""
update_indexes.py
=================
Update Vault indexes after x-note run.

Updates:
  - {{VAULT_ROOT}}/00-Inbox/index.md
  - {{VAULT_ROOT}}/08-Learning/99_Maintenance/status/LLM-Wiki-Index.md
  - {{VAULT_ROOT}}/08-Learning/99_Maintenance/status/LLM-Wiki-Ingest-Log.md
  - {{VAULT_ROOT}}/STATUS_ALL.md

Usage:
    python update_indexes.py --date 2026-08-08
"""
import argparse
import json
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths

UTC8 = timezone(timedelta(hours=8))


def update_inbox_index(inbox: Path, date: str) -> int:
    """Append x-note entries to 00-Inbox/index.md. Returns number of new entries."""
    pattern = f"{date}_x-note_*.md"
    notes = sorted(inbox.glob(pattern))
    index_path = inbox / "index.md"
    if not index_path.exists():
        return 0

    text = index_path.read_text(encoding="utf-8")
    added = 0
    for note in notes:
        link = f"- [[{note.stem}]]"
        if link in text:
            continue
        # Try to insert under a "## x-note" section, else append
        if "## x-note" in text:
            text = text.replace("## x-note", f"## x-note\n{link}", 1)
        else:
            text += f"\n## x-note ({date})\n{link}\n"
        added += 1
    if added:
        index_path.write_text(text, encoding="utf-8")
    return added


def update_llm_wiki_index(status: dict, vault_root: Path) -> None:
    """Update LLM-Wiki-Index.md with new entries."""
    inbox = vault_root / "00-Inbox"
    notes = sorted(inbox.glob(f"{status['date']}_x-note_*.md"))
    if not notes:
        return

    target = vault_root / "08-Learning" / "99_Maintenance" / "status" / "LLM-Wiki-Index.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text("# LLM-Wiki Index\n\n", encoding="utf-8")

    text = target.read_text(encoding="utf-8")
    added = 0
    for note in notes:
        link = f"- [[{note.stem}]]"
        if link in text:
            continue
        section = f"\n## x-note {status['date']}\n{link}\n"
        text += section
        added += 1
    if added:
        target.write_text(text, encoding="utf-8")


def update_ingest_log(status: dict, vault_root: Path) -> None:
    """Append to LLM-Wiki-Ingest-Log.md."""
    target = vault_root / "08-Learning" / "99_Maintenance" / "status" / "LLM-Wiki-Ingest-Log.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text("# LLM-Wiki Ingest Log\n\n", encoding="utf-8")

    timestamp = datetime.now(UTC8).strftime("%Y-%m-%d %H:%M:%S +08:00")
    entry = f"""
## x-note run {status['date']} — {timestamp}

- Threshold: {status.get('threshold', 'N/A')}
- Total kept: {status.get('total', 0)}
- Passed: {status.get('passed', 0)}
- Failed: {status.get('failed', 0)}
- Skill: x-note (Pigo rewrite)
"""
    text = target.read_text(encoding="utf-8") + entry
    target.write_text(text, encoding="utf-8")


def update_status_all(status: dict, vault_root: Path) -> None:
    """Update root STATUS_ALL.md."""
    target = vault_root / "STATUS_ALL.md"
    if not target.exists():
        return
    text = target.read_text(encoding="utf-8")
    timestamp = datetime.now(UTC8).strftime("%Y-%m-%d %H:%M:%S +08:00")
    note = (f"\n## x-note run {status['date']} — {timestamp}\n"
            f"- captured: {status.get('total', 0)} posts at threshold {status.get('threshold', 'N/A')}\n"
            f"- passed validation: {status.get('passed', 0)}\n"
            f"- failed: {status.get('failed', 0)}\n")
    if f"## x-note run {status['date']}" not in text:
        text += note
    target.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True)
    parser.add_argument("--status-file", default=None, help="Path to xnote_status JSON")
    args = parser.parse_args()

    cfg = load_config()
    p = paths(cfg)
    inbox = p["inbox"]
    vault_root = p["vault_root"]

    # Read status
    status_file = Path(args.status_file) if args.status_file else (inbox / f"xnote_status_{args.date}.json")
    if not status_file.exists():
        print(f"[WARN] Status file not found: {status_file}")
        status = {"date": args.date, "total": 0, "passed": 0, "failed": 0, "threshold": cfg["X2_MIN_SCORE"]}
    else:
        status = json.loads(status_file.read_text(encoding="utf-8"))

    # Update indexes
    added_inbox = update_inbox_index(inbox, args.date)
    update_llm_wiki_index(status, vault_root)
    update_ingest_log(status, vault_root)
    update_status_all(status, vault_root)

    print(f"[OK] Inbox index: +{added_inbox} entries")
    print(f"[OK] LLM-Wiki-Index updated")
    print(f"[OK] LLM-Wiki-Ingest-Log updated")
    print(f"[OK] STATUS_ALL.md updated")


if __name__ == "__main__":
    main()
