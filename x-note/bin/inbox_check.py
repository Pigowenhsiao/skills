"""
inbox_check.py
===============
Read x-note files from 00-Inbox, classify with MiniMax-M3, move to correct vault folder.

Usage:
    python inbox_check.py                        # classify all inbox notes
    python inbox_check.py --date 2026-08-01     # only notes from specific date
    python inbox_check.py --dry-run              # show what would happen without moving
    python inbox_check.py --status-only          # just list notes without classifying
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from curator import classify_with_llm, CLASSIFICATION_MAP
from config_loader import load_config, paths


def extract_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML frontmatter. Returns (fm_dict, body)."""
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return {}, text
    fm = yaml.safe_load(m.group(1)) or {}
    body = text[m.end():]
    return fm, body


def update_frontmatter(text: str, updates: dict) -> str:
    """Update frontmatter fields in note text."""
    def _replace_value(fm_text: str, key: str, value) -> str:
        lines = fm_text.split('\n')
        new_lines = []
        found = False
        for line in lines:
            if line.startswith(f"{key}:"):
                if isinstance(value, str):
                    new_lines.append(f'{key}: "{value}"')
                else:
                    new_lines.append(f'{key}: {value}')
                found = True
            else:
                new_lines.append(line)
        if not found:
            # Insert before closing ---
            new_lines.insert(-1, f'{key}: {value}')
        return '\n'.join(new_lines)

    m = re.match(r'^(---\n)(.*?\n)(---\n)(.*)', text, re.DOTALL)
    if not m:
        return text
    prefix, fm_text, sep, body = m.group(1), m.group(2), m.group(3), m.group(4)
    for k, v in updates.items():
        fm_text = _replace_value(fm_text, k, v)
    return f"{prefix}{fm_text}{sep}{body}"


def remove_from_inbox_index(index_path: Path, note_stem: str) -> bool:
    """Remove a note's wikilink entry from 00-Inbox/index.md."""
    if not index_path.exists():
        return False
    text = index_path.read_text(encoding="utf-8")
    # Match: - [[stem]] or - [[stem|...]]
    pattern = rf'\n- \[\[{re.escape(note_stem)}(\|.*?)?\]\](.*?)(?=\n|$)'
    new_text = re.sub(pattern, '', text)
    if new_text == text:
        return False
    index_path.write_text(new_text, encoding="utf-8")
    return True


def main():
    parser = argparse.ArgumentParser(description="Classify and file inbox notes")
    parser.add_argument("--date", default=None, help="Filter by date prefix (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Show moves without executing")
    parser.add_argument("--status-only", action="store_true", help="List notes without classifying")
    args = parser.parse_args()

    cfg = load_config()
    p = paths(cfg)
    vault_root = Path(p["vault_root"])
    inbox_dir = vault_root / "00-Inbox"
    index_path = inbox_dir / "index.md"

    # Find all x-note files with status=inbox
    notes = sorted(inbox_dir.glob("20*_x-note_*.md"))
    to_process = []
    for f in notes:
        if args.date and not f.stem.startswith(args.date):
            continue
        text = f.read_text(encoding="utf-8")
        fm, body = extract_frontmatter(text)
        if fm.get("status") == "inbox":
            to_process.append((f, fm, body))

    print(f"[INFO] Found {len(to_process)} inbox notes to process")
    if args.status_only:
        for f, fm, body in to_process:
            print(f"  - {f.name}")
        return

    if not to_process:
        print("[OK] Nothing to process")
        return

    if args.dry_run:
        print("[DRY RUN] Would classify and move:")
    else:
        print("Classifying and moving:")

    results = {"moved": [], "skipped": [], "errors": []}

    for f, fm, body in to_process:
        handle = fm.get("handle", "?")
        author = fm.get("author_display", handle)
        note_stem = f.stem

        # Classify
        try:
            cls_result = classify_with_llm(body, handle, author, cfg=cfg)
        except Exception as e:
            results["errors"].append({"file": f.name, "error": str(e)})
            print(f"  [ERROR] {f.name}: {e}")
            continue

        cls_key = cls_result.get("classification", "")
        target_folder = CLASSIFICATION_MAP.get(cls_key, CLASSIFICATION_MAP.get("", "01-Daily/01_AI"))
        target_dir = vault_root / target_folder

        print(f"  {'[DRY] ' if args.dry_run else ''}{f.name}")
        print(f"       → {target_folder} (key='{cls_key}', confidence={cls_result.get('confidence', '?')})")
        print(f"       reasoning: {cls_result.get('reasoning', '?')[:80]}...")

        if args.dry_run:
            results["moved"].append({"file": f.name, "target": str(target_dir)})
            continue

        # Create target dir
        target_dir.mkdir(parents=True, exist_ok=True)

        # Move file
        new_path = target_dir / f.name
        new_text = update_frontmatter(f.read_text(encoding="utf-8"), {
            "status": "filed",
            "classification_path": target_folder,
        })
        new_path.write_text(new_text, encoding="utf-8")
        f.unlink()

        # Remove from inbox index
        removed = remove_from_inbox_index(index_path, note_stem)

        results["moved"].append({
            "file": f.name,
            "target": str(target_dir),
            "classification": target_folder,
            "removed_from_index": removed,
        })

    # Summary
    print(f"\n{'='*60}")
    if args.dry_run:
        print(f"[DRY RUN] Would move {len(results['moved'])} notes")
    else:
        print(f"[OK] Moved {len(results['moved'])} notes")
        if results["errors"]:
            print(f"[WARN] Errors: {len(results['errors'])}")
            for e in results["errors"]:
                print(f"  - {e['file']}: {e['error']}")


if __name__ == "__main__":
    main()
