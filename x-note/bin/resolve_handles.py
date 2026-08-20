"""
resolve_handles.py
==================
Read X/Twitter handles from configured sources.

Order of fallback:
1. config['TWITTER_HANDLE_FILE'] (default: E:/python_Code/Agent/name.md)
2. {{VAULT_ROOT}}/_config/x-note-handles.md

Accepted formats:
  - @dotey
  - dotey
  - @wshuyi (profile link)

Deduplicate, normalize, and return unique list.

Usage:
    python resolve_handles.py                  # print all handles
    python resolve_handles.py --limit 5        # first N (for testing)
    python resolve_handles.py --json           # output as JSON
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths


HANDLE_RE = re.compile(r"^[a-zA-Z0-9_]{1,15}$")


def parse_handles_from_text(text: str) -> list:
    """Extract handles from markdown text.

    Recognized patterns:
      - @handle
      - @handle (description)
      - 裸 handle 後接空白
      - https://x.com/handle
    """
    handles = set()
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        # Skip headers / comments / metadata
        if s.startswith("#") or s.startswith("<!--"):
            continue
        # Skip generated metadata lines
        if s.startswith("_Generated") or s.startswith("_") or s.startswith("Score"):
            continue
        # Match explicit @handle patterns
        for m in re.finditer(r"@([a-zA-Z0-9_]{1,15})", s):
            token = m.group(1)
            if HANDLE_RE.match(token):
                handles.add(token.lower())
        # Match x.com/handle links
        for m in re.finditer(r"x\.com/([a-zA-Z0-9_]{1,15})", s):
            token = m.group(1)
            if token in ("i", "home", "search", "compose", "messages"):
                continue
            if HANDLE_RE.match(token):
                handles.add(token.lower())
    return sorted(handles)


def resolve_file(cfg: dict) -> tuple:
    """Resolve handle source file (path, label)."""
    p = paths(cfg)

    # 1. Configured file
    f = Path(cfg.get("TWITTER_HANDLE_FILE", ""))
    if f and f.exists():
        return f, "configured"

    # 2. Vault fallback
    alt = p["vault_root"] / "_config" / "x-note-handles.md"
    if alt.exists():
        return alt, "vault-fallback"

    raise FileNotFoundError(
        "No handle file found. Set TWITTER_HANDLE_FILE in .path-config.json "
        "or create {{VAULT_ROOT}}/_config/x-note-handles.md"
    )


def load_handles(cfg: dict, limit: int | None = None) -> list:
    """Load and normalize handles."""
    f, label = resolve_file(cfg)
    text = f.read_text(encoding="utf-8")
    handles = parse_handles_from_text(text)
    if limit:
        handles = handles[:limit]
    return {
        "source": str(f),
        "source_label": label,
        "total_count": len(parse_handles_from_text(text)),
        "selected": handles,
        "selected_count": len(handles),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Limit to N handles")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    cfg = load_config()
    result = load_handles(cfg, limit=args.limit)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"# Source: {result['source']} ({result['source_label']})")
        print(f"# Total: {result['total_count']}, Selected: {result['selected_count']}")
        for h in result["selected"]:
            print(f"@{h}")


if __name__ == "__main__":
    main()
