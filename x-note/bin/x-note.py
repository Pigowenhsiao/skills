"""
x-note.py
==========
Main entry point for the x-note skill.

Usage:
    python x-note.py --start 2026-08-08 --end 2026-08-09
    python x-note.py --start 2026-08-08 --end 2026-08-08 --limit 5
    python x-note.py --start 2026-08-08 --end 2026-08-08 --handles dotey,op7418
    python x-note.py --start 2026-08-08 --end 2026-08-08 --no-launch

Pipeline:
  1. Resolve profile & launch Chrome (CDP)
  2. Resolve handles (from config or file)
  3. Fetch timeline (CDP)
  4. Fetch full posts (fxtwitter + x.com fallback)
  5. Score posts (0-10)
  6. Write notes to 00-Inbox
  7. Validate notes
  8. Update indexes
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths

UTC8 = timezone(timedelta(hours=8))


def run_step(name: str, cmd: list, cwd: Path | None = None) -> int:
    """Run a subprocess step, return exit code."""
    print(f"\n========== {name} ==========")
    print(f"$ {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=cwd, capture_output=False)
    if proc.returncode != 0:
        print(f"[FAIL] {name} returned {proc.returncode}")
    return proc.returncode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=None, help="Limit handles")
    parser.add_argument("--handles", type=str, default=None)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--no-launch", action="store_true",
                        help="Skip launching Chrome (assume CDP already running)")
    parser.add_argument("--headed", action="store_true", help="Launch Chrome with UI")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--skip-fetch", action="store_true",
                        help="Skip timeline+full fetch (use existing JSON)")
    parser.add_argument("--skip-write", action="store_true",
                        help="Skip writing notes (validation only)")
    args = parser.parse_args()

    cfg = load_config()
    p = paths(cfg)
    bin_dir = Path(__file__).parent
    inbox = p["inbox"]
    inbox.mkdir(parents=True, exist_ok=True)

    port = args.port or cfg["CDP_PORT"]
    threshold = args.threshold or cfg["X2_MIN_SCORE"]

    failed = []
    fetch_file = inbox / f"xnote_fetch_{args.start}.json"
    full_file = inbox / f"xnote_full_{args.start}.json"
    score_file = inbox / f"xnote_score_{args.start}.json"
    status_file = inbox / f"xnote_status_{args.start}.json"

    # Step 1: Profile + CDP
    if not args.no_launch:
        rc = run_step("Step 1: Resolve profile & launch Chrome", [
            "python", str(bin_dir / "resolve_profile.py"),
            "--launch" if not args.headed else "--launch-headed",
            "--port", str(port),
        ])
        if rc != 0:
            print("[FATAL] Chrome failed to launch. Use --no-launch if Chrome is already running.")
            sys.exit(rc)

    # Step 2: Timeline
    if not args.skip_fetch:
        cmd = [
            "python", str(bin_dir / "fetch_timeline.py"),
            "--start", args.start, "--end", args.end,
            "--port", str(port),
        ]
        if args.limit:
            cmd.extend(["--limit", str(args.limit)])
        if args.handles:
            cmd.extend(["--handles", args.handles])
        rc = run_step("Step 3: Fetch timeline", cmd)
        if rc != 0:
            failed.append("fetch_timeline")
            if not fetch_file.exists():
                print("[FATAL] No fetch file produced. Exiting.")
                sys.exit(rc)

    # Step 3: Full post
    if not args.skip_fetch:
        cmd = [
            "python", str(bin_dir / "fetch_full_post.py"),
            "--input", str(fetch_file),
            "--port", str(port),
        ]
        rc = run_step("Step 4: Fetch full post (fxtwitter + x.com fallback)", cmd)
        if rc != 0:
            failed.append("fetch_full_post")

    # Step 4: Score
    cmd = [
        "python", str(bin_dir / "score_posts.py"),
        "--input", str(full_file),
        "--threshold", str(threshold),
    ]
    rc = run_step("Step 5: Score posts", cmd)
    if rc != 0:
        failed.append("score_posts")

    # Step 5: Write notes
    if not args.skip_write:
        cmd = [
            "python", str(bin_dir / "write_to_inbox.py"),
            "--input", str(score_file),
            "--date", args.start,
        ]
        rc = run_step("Step 6: Write notes to 00-Inbox", cmd)
        if rc != 0:
            failed.append("write_to_inbox")

    # Step 6: Validate
    cmd = [
        "python", str(bin_dir / "validate_note.py"),
        "--date", args.start,
        "--threshold", str(threshold),
    ]
    rc = run_step("Step 7: Validate notes", cmd)
    if rc != 0:
        failed.append("validate_note")

    # Step 7: Update indexes
    cmd = [
        "python", str(bin_dir / "update_indexes.py"),
        "--date", args.start,
    ]
    rc = run_step("Step 8: Update indexes", cmd)
    if rc != 0:
        failed.append("update_indexes")

    # Summary
    print("\n" + "=" * 60)
    print(f"x-note run complete for {args.start}")
    if failed:
        print(f"[WARN] Failed steps: {failed}")
        sys.exit(1)
    else:
        print("[OK] All steps completed")
    print("=" * 60)


if __name__ == "__main__":
    main()
