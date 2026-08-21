"""
fetch_timeline.py
==================
Fetch X/Twitter timeline for each handle via CDP.

For every handle:
1. Open https://x.com/<handle>
2. Wait for tweets to render
3. Scroll using JavaScript, NOT bb-browser scroll down
4. Extract [data-testid=tweet] elements
5. Capture: handle, time_utc, status_id, text_preview, likes, reposts, replies

Outputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_fetch_YYYY-MM-DD.json

Usage:
    python fetch_timeline.py --start 2026-08-08 --end 2026-08-09
    python fetch_timeline.py --start 2026-08-08 --end 2026-08-09 --limit 3
    python fetch_timeline.py --start 2026-08-08 --end 2026-08-08 --handles dotey,op7418
"""
import argparse
import json
import logging
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cdp_client import CDPClient
from config_loader import load_config, paths

logger = logging.getLogger(__name__)
UTC8 = timezone(timedelta(hours=8))


def parse_taipei_date(time_utc: str) -> str | None:
    """Convert UTC ISO timestamp to Asia/Taipei date YYYY-MM-DD."""
    if not time_utc:
        return None
    try:
        s = time_utc.replace("Z", "+00:00")
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(UTC8).strftime("%Y-%m-%d")
    except Exception:
        return None


def extract_tweets_js() -> str:
    """JavaScript to extract tweet cards using data-testid (current X.com DOM)."""
    return r"""
(function() {
    const cards = document.querySelectorAll('article[data-testid="tweet"]');
    const out = [];
    const seen = new Set();
    cards.forEach(card => {
        try {
            // Get status ID from link
            const links = card.querySelectorAll('a[href*="/status/"]');
            let status_id = null;
            for (const l of links) {
                const m = l.getAttribute("href").match(/\/status\/(\d+)/);
                if (m) { status_id = m[1]; break; }
            }
            if (!status_id || seen.has(status_id)) return;
            seen.add(status_id);

            const url = "https://x.com/i/status/" + status_id;
            const time = card.querySelector("time");
            const time_iso = time ? time.getAttribute("datetime") : null;
            const taipei_date = time_iso ? new Date(time_iso).toLocaleDateString("en-CA", {timeZone: "Asia/Taipei"}) : null;

            // Text: prefer data-testid=tweetText, fallback to div[lang]
            const textEl = card.querySelector('[data-testid="tweetText"]');
            const text = textEl ? textEl.textContent : (card.querySelector('div[lang]')?.textContent || "");

            // Author
            const handleEl = card.querySelector('[data-testid="User-Name"]') || card;
            const handleLink = handleEl.querySelector('a[href*="/"]');
            const handle = handleLink ? handleLink.getAttribute("href").replace("/", "") : "";
            const displayName = handleEl.querySelector("span")?.textContent || "";

            // Counts from data-testid keys
            const stats = card.querySelectorAll('[data-testid]');
            let likes = 0, reposts = 0, replies = 0;
            stats.forEach(el => {
                const key = el.getAttribute('data-testid');
                const txt = el.textContent || "";
                const n = txt.match(/[\d,]+/);
                const num = n ? parseInt(n[0].replace(/,/g, ""), 10) : 0;
                if (key === 'like') likes = num;
                if (key === 'retweet') reposts = num;
                if (key === 'reply') replies = num;
            });

            out.push({
                status_id: status_id,
                url: url,
                time_utc: time_iso,
                taipei_date: taipei_date,
                text_preview: text.substring(0, 300),
                author_display: displayName,
                author_handle: handle,
                likes: likes,
                reposts: reposts,
                replies: replies,
            });
        } catch (e) { /* skip */ }
    });
    return out;
})()
"""


def scroll_page_js() -> str:
    """Scroll the page to bottom."""
    return "window.scrollTo({top: document.body.scrollHeight, behavior: 'instant'}); " \
           "return document.body.scrollHeight;"


def fetch_handle(client: CDPClient, handle: str, start_date: str, end_date: str, max_scrolls: int = 12) -> tuple:
    """Fetch tweets for one handle. Returns (tweets_list, error_message)."""
    url = f"https://x.com/{handle}"
    client.send("Page.navigate", {"url": url})
    time.sleep(8)  # initial render: modern X.com needs more time for SPAs

    all_tweets = {}
    last_card_count = 0
    no_change = 0

    for scroll_n in range(max_scrolls):
        # Extract tweets
        js = extract_tweets_js()
        res_json = client.eval(js)
        if not res_json:
            no_change += 1
        else:
            try:
                tweets = json.loads(res_json)
                for t in tweets:
                    sid = t.get("status_id")
                    if sid and sid not in all_tweets:
                        all_tweets[sid] = t
            except Exception as e:
                logger.warning(f"WARN parse error: {e}")

        # Stop early if all tweets are before start_date
        if all_tweets:
            valid_dates = [t.get("taipei_date") or "" for t in all_tweets.values() if t.get("taipei_date")]
            if valid_dates:
                min_date = min(valid_dates)
                if min_date < start_date:
                    break

        # Stop if no new tweets
        if len(all_tweets) == last_card_count:
            no_change += 1
            if no_change >= 2:
                break
        else:
            no_change = 0
        last_card_count = len(all_tweets)

        # Scroll with retry: 2 attempts with 2s delay
        scroll_success = False
        for scroll_attempt in range(2):
            scroll_result = client.eval(scroll_page_js())
            if scroll_result:
                scroll_success = True
                break
            if scroll_attempt < 1:  # Don't delay after last attempt
                time.sleep(2)

        if not scroll_success:
            logger.warning(f"Scroll failed after 2 attempts for @{handle}")

        time.sleep(2)

    # Filter by date range - keep only tweets with valid date in range
    filtered = []
    for t in all_tweets.values():
        td = t.get("taipei_date")
        if not td:
            continue
        if start_date <= td <= end_date:
            filtered.append(t)
    return filtered, None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=None, help="Limit handles")
    parser.add_argument("--handles", type=str, default=None, help="Comma-separated handle list")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--max-scrolls", type=int, default=12)
    args = parser.parse_args()

    cfg = load_config()
    port = args.port or cfg["CDP_PORT"]

    if args.handles:
        handles = [h.strip().lstrip("@") for h in args.handles.split(",")]
    else:
        from resolve_handles import load_handles
        h = load_handles(cfg, limit=args.limit or cfg["X2_LIMIT_HANDLES"])
        handles = h["selected"]
    print(f"[INFO] {len(handles)} handles to fetch")

    # Create CDPClient and connect
    client = CDPClient(port=port)
    if not client.connect():
        logger.error(f"Failed to connect to CDP on port {port}")
        sys.exit(1)
    print(f"[INFO] CDP connected: {client.ws_url[:60]}...")

    results = {"start": args.start, "end": args.end, "handles": {}, "errors": []}
    for i, handle in enumerate(handles, 1):
        print(f"[{i}/{len(handles)}] @{handle} ... ", end="", flush=True)
        try:
            # Health check before each handle
            health = client.health_check()
            if not health["cdp_ok"]:
                logger.warning(f"CDP unhealthy before @{handle}, attempting reconnect...")
                if not client._reconnect():
                    raise ConnectionError(f"CDP reconnect failed for @{handle}")

            tweets, err = fetch_handle(client, handle, args.start, args.end, args.max_scrolls)
            if err:
                results["errors"].append({"handle": handle, "error": err})
                print("ERROR")
            else:
                results["handles"][handle] = tweets
                print(f"{len(tweets)} tweets")
        except (ConnectionError, ConnectionResetError) as e:
            logger.warning(f"Connection error for @{handle}: {e}, attempting reconnect...")
            if client._reconnect():
                logger.info(f"Reconnected successfully, retrying @{handle}...")
                try:
                    tweets, err = fetch_handle(client, handle, args.start, args.end, args.max_scrolls)
                    if err:
                        results["errors"].append({"handle": handle, "error": err})
                        print("ERROR")
                    else:
                        results["handles"][handle] = tweets
                        print(f"{len(tweets)} tweets (after reconnect)")
                except Exception as retry_err:
                    results["errors"].append({"handle": handle, "error": str(retry_err)})
                    print(f"FAIL: {retry_err}")
            else:
                results["errors"].append({"handle": handle, "error": str(e)})
                print(f"FAIL: {e}")
        except Exception as e:
            results["errors"].append({"handle": handle, "error": str(e)})
            print(f"FAIL: {e}")

    client.close()

    p = paths(cfg)
    out_dir = p["inbox"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"xnote_fetch_{args.start}.json"
    out.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] Saved to: {out}")
    print(f"     Total tweets: {sum(len(v) for v in results['handles'].values())}")
    print(f"     Errors: {len(results['errors'])}")


if __name__ == "__main__":
    main()
