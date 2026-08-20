"""
score_posts.py
==============
Score each post using MiniMax-M3 semantic scoring (Fix #1).

Fallback to rule-based scoring when LLM is unavailable.

Inputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_full_YYYY-MM-DD.json

Outputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_score_YYYY-MM-DD.json
    {{VAULT_ROOT}}/00-Inbox/xnote_skip_YYYY-MM-DD.json

Usage:
    python score_posts.py --input xnote_full_2026-08-19.json
    python score_posts.py --input xnote_full_2026-08-19.json --threshold 6.5
    python score_posts.py --input xnote_full_2026-08-19.json --use-rules  # force rule-based
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths
from curator import score_post_with_llm, _fallback_rule_score


def main():
    parser = argparse.ArgumentParser(description="Score posts with MiniMax-M3 (Fix #1)")
    parser.add_argument("--input", required=True)
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument(
        "--use-rules",
        action="store_true",
        help="Force rule-based scoring (skip MiniMax-M3)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=5,
        help="MiniMax-M3 batch size (default: 5)",
    )
    args = parser.parse_args()

    cfg = load_config()
    p = paths(cfg)
    threshold = args.threshold or cfg["X2_MIN_SCORE"]
    print(f"[INFO] Threshold: {threshold}")
    print(f"[INFO] Mode: {'rule-based' if args.use_rules else 'MiniMax-M3 semantic'}")

    in_path = Path(args.input)
    if not in_path.is_absolute():
        in_path = p["inbox"] / in_path
    full_data = json.loads(in_path.read_text(encoding="utf-8"))

    scored = []
    skipped = []
    posts = full_data.get("posts", [])

    for i, post in enumerate(posts):
        handle = post.get("handle") or post.get("meta", {}).get("handle", "?")
        sid = post.get("status_id") or post.get("meta", {}).get("status_id", "?")
        text = post.get("text", "")
        author = post.get("author_display") or post.get("meta", {}).get("author_display", "")
        likes = post.get("likes", 0) or post.get("meta", {}).get("likes", 0)
        reposts = post.get("reposts", 0) or post.get("meta", {}).get("reposts", 0)
        replies = post.get("replies", 0) or post.get("meta", {}).get("replies", 0)
        views = post.get("views", 0)

        if args.use_rules:
            result = _fallback_rule_score(text, likes)
            score = result["score"]
            reasons = [result.get("reasoning", "")]
            content_type = result.get("content_type", "unknown")
            usefulness = result.get("usefulness", "unknown")
            tags = result.get("tags", [])
        else:
            result = score_post_with_llm(
                text=text,
                handle=handle,
                author_display=author,
                likes=likes,
                reposts=reposts,
                replies=replies,
                views=views,
                cfg=cfg,
            )
            score = result.get("score", 0)
            reasons = [result.get("reasoning", "")]
            content_type = result.get("content_type", "unknown")
            usefulness = result.get("usefulness", "unknown")
            tags = result.get("tags", [])

        record = {
            **post,
            "score": score,
            "score_reasons": reasons,
            "content_type": content_type,
            "usefulness": usefulness,
            "tags": tags,
            "keep": score >= threshold,
            "scoring_method": "rule" if args.use_rules else "MiniMax-M3",
        }

        print(f"  [{i+1}/{len(posts)}] @{handle}/{str(sid)[:8]} "
              f"→ score={score:.1f} type={content_type} useful={usefulness} "
              f"{'✓ KEEP' if score >= threshold else '✗ SKIP'}")

        if score >= threshold:
            scored.append(record)
        else:
            skipped.append(record)

    scored.sort(key=lambda r: -r["score"])

    out_dir = p["inbox"]
    date_str = in_path.stem.replace("xnote_full_", "")
    out_scored = out_dir / f"xnote_score_{date_str}.json"
    out_skipped = out_dir / f"xnote_skip_{date_str}.json"

    def _serialize(obj):
        """Remove non-serializable fields before JSON dump."""
        if isinstance(obj, dict):
            return {k: _serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_serialize(i) for i in obj]
        if isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        return str(obj)

    scored_s = _serialize(scored)
    skipped_s = _serialize(skipped)

    out_scored.write_text(json.dumps({
        "threshold": threshold,
        "scoring_method": "rule" if args.use_rules else "MiniMax-M3",
        "fetched_at": full_data.get("fetched_at"),
        "kept": scored_s,
        "total_kept": len(scored_s),
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    out_skipped.write_text(json.dumps({
        "threshold": threshold,
        "scoring_method": "rule" if args.use_rules else "MiniMax-M3",
        "fetched_at": full_data.get("fetched_at"),
        "skipped": skipped_s,
        "total_skipped": len(skipped_s),
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    # Summary
    scores_kept = [r["score"] for r in scored]
    print(f"\n{'='*60}")
    print(f"[SUMMARY] Scoring complete")
    print(f"  Mode: {'MiniMax-M3' if not args.use_rules else 'Rule-based'}")
    print(f"  Kept (≥{threshold}): {len(scored)}  |  Score range: {min(scores_kept):.1f}–{max(scores_kept):.1f}")
    print(f"  Skipped: {len(skipped)}")
    print(f"  Saved: {out_scored.name} ({len(scored)} records)")
    print(f"  Saved: {out_skipped.name} ({len(skipped)} records)")
    print(f"{'='*60}")

    # Content type distribution for kept
    from collections import Counter
    type_dist = Counter(r.get("content_type", "?") for r in scored)
    print(f"\n[Content Type Distribution — kept posts]")
    for ct, cnt in type_dist.most_common():
        print(f"  {ct}: {cnt}")

    print(f"\nTop 5 by score:")
    for r in scored[:5]:
        print(f"  [{r['score']:.1f}] @{r.get('handle','?')} | "
              f"type={r.get('content_type','?')} | {r.get('score_reasons',['?'])[0][:60]}")


if __name__ == "__main__":
    main()
