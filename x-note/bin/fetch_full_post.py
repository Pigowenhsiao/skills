"""
fetch_full_post.py
==================
Fetch full post text for each status_id using fxtwitter API.
Fallback: open x.com/<handle>/status/<id> via CDP and extract DOM.

Inputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_fetch_YYYY-MM-DD.json

Outputs:
    {{VAULT_ROOT}}/00-Inbox/xnote_full_YYYY-MM-DD.json

Usage:
    python fetch_full_post.py --input xnote_fetch_2026-08-08.json
    python fetch_full_post.py --input xnote_fetch_2026-08-08.json --limit 5
"""
import argparse
import hashlib
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from config_loader import load_config, paths


def fxtwitter_get(handle: str, status_id: str, host: str, timeout: float = 30.0) -> dict | None:
    """Fetch post from fxtwitter API.

    fxtwitter returns normalized tweet data including full text and media.
    API: https://api.fxtwitter.com/<handle>/status/<id>
    """
    url = f"{host.rstrip('/')}/{handle}/status/{status_id}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "x-note/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read())
    except Exception as e:
        return {"__error__": str(e), "__url__": url}

    if data.get("code") != 200:
        return {"__error__": f"fxtwitter code {data.get('code')}: {data.get('message')}", "__url__": url}

    tweet = data.get("tweet", {})
    if not tweet:
        return {"__error__": "No tweet data", "__url__": url}

    text = tweet.get("text", "") or tweet.get("full_text", "")
    author = tweet.get("author", {})
    return {
        "source": "fxtwitter",
        "status_id": status_id,
        "handle": handle,
        "url": url,
        "text": text,
        "text_length": len(text),
        "author_display": author.get("name", ""),
        "author_screen_name": author.get("screen_name", handle),
        "time_utc": tweet.get("created_at", ""),
        "likes": tweet.get("likes", 0),
        "reposts": tweet.get("retweets", 0),
        "replies": tweet.get("replies", 0),
        "views": tweet.get("views", 0),
        "language": tweet.get("lang", ""),
        "media": tweet.get("media", {}),
        "content_hash": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "captured_at": time.strftime("%Y-%m-%d %H:%M:%S +08:00", time.localtime()),
    }


def cdp_extract_single(ws, url: str, msg_id: int, max_retries: int = 2) -> dict | None:
    """Fallback: open single status page and extract DOM with retry."""
    import websocket
    js = """
(function() {
    const article = document.querySelector('article');
    if (!article) return null;
    const text = article.querySelector('[data-testid=tweetText]')?.innerText || '';
    const time = article.querySelector('time')?.getAttribute('datetime') || '';
    return {text: text, time_utc: time};
})()
"""
    last_error = None
    for attempt in range(1, max_retries + 1):
        nav_id = msg_id
        cdp_send_basic(ws, "Page.navigate", {"url": url}, msg_id=nav_id)
        time.sleep(8)
        eval_id = msg_id + 1
        res = cdp_send_basic(ws, "Runtime.evaluate", {
            "expression": js, "returnByValue": True, "awaitPromise": True
        }, msg_id=eval_id)
        if not res:
            last_error = f"attempt {attempt}: CDP eval returned None"
            if attempt < max_retries:
                time.sleep(3)
                continue
            return None
        val = res.get("result", {}).get("result", {}).get("value", "")
        if not val:
            last_error = f"attempt {attempt}: empty eval result"
            if attempt < max_retries:
                time.sleep(3)
                continue
            return None
        if isinstance(val, str):
            try:
                d = json.loads(val)
            except Exception as e:
                last_error = f"attempt {attempt}: JSON parse failed: {e}"
                if attempt < max_retries:
                    time.sleep(3)
                    continue
                return None
        elif isinstance(val, dict):
            d = val
        else:
            last_error = f"attempt {attempt}: unexpected value type {type(val)}"
            if attempt < max_retries:
                time.sleep(3)
                continue
            return None
        if not d.get("text"):
            last_error = f"attempt {attempt}: no tweet text found"
            if attempt < max_retries:
                time.sleep(3)
                continue
            return None
        return {
            "source": "x.com-cdp",
            "url": url,
            "text": d["text"],
            "text_length": len(d["text"]),
            "time_utc": d.get("time_utc", ""),
            "content_hash": hashlib.sha256(d["text"].encode("utf-8")).hexdigest(),
            "captured_at": time.strftime("%Y-%m-%d %H:%M:%S +08:00", time.localtime()),
        }
    # All retries exhausted - return None with last error stored in calling context
    return None


def cdp_send_basic(ws, method: str, params: dict, msg_id: int, timeout: float = 30.0):
    """Send CDP command and wait for response by id."""
    import websocket
    payload = json.dumps({"id": msg_id, "method": method, "params": params})
    ws.send(payload)
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            ws.settimeout(timeout)
            r = json.loads(ws.recv())
        except Exception:
            return None
        if r.get("id") == msg_id:
            return r
    return None


def get_cdp_ws(port: int) -> str:
    """Get main tab WebSocket URL."""
    with urllib.request.urlopen(f"http://localhost:{port}/json", timeout=5) as r:
        pages = json.loads(r.read())
    for p in pages:
        if p.get("type") == "page" and "webSocketDebuggerUrl" in p:
            return p["webSocketDebuggerUrl"]
    raise RuntimeError(f"No usable page tab on port {port}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input fetch JSON")
    parser.add_argument("--output", default=None, help="Output file path")
    parser.add_argument("--limit", type=int, default=None, help="Limit total posts")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--no-cdp", action="store_true", help="Skip CDP fallback")
    args = parser.parse_args()

    cfg = load_config()
    p = paths(cfg)
    in_path = Path(args.input)
    if not in_path.is_absolute():
        in_path = p["inbox"] / in_path
    fetch_data = json.loads(in_path.read_text(encoding="utf-8"))

    # Build flat list of (handle, status_id, url, meta)
    posts = []
    for handle, tweets in fetch_data.get("handles", {}).items():
        for t in tweets:
            posts.append({
                "handle": handle,
                "status_id": t["status_id"],
                "url": t.get("url", f"https://x.com/{handle}/status/{t['status_id']}"),
                "time_utc": t.get("time_utc"),
                "taipei_date": t.get("taipei_date"),
                "text_preview": t.get("text_preview", ""),
                "likes": t.get("likes", 0),
                "reposts": t.get("reposts", 0),
                "replies": t.get("replies", 0),
            })
    if args.limit:
        posts = posts[: args.limit]
    print(f"[INFO] Fetching full text for {len(posts)} posts")

    # Connect CDP
    use_cdp = not args.no_cdp
    ws = None
    if use_cdp:
        try:
            import websocket
            ws_url = get_cdp_ws(args.port or cfg["CDP_PORT"])
            ws = websocket.create_connection(ws_url, timeout=60)
            print(f"[INFO] CDP connected for fallback")
        except Exception as e:
            print(f"[WARN] CDP not available: {e}")
            ws = None
            use_cdp = False

    # Fetch each
    full_data = {
        "fetched_at": time.strftime("%Y-%m-%d %H:%M:%S +08:00", time.localtime()),
        "source": "fetch_timeline",
        "posts": [],
        "errors": [],
    }
    msg_id = 1000
    for i, post in enumerate(posts, 1):
        handle = post["handle"]
        sid = post["status_id"]
        print(f"[{i}/{len(posts)}] @{handle}/{sid} ... ", end="", flush=True)

        # Try fxtwitter first
        full = fxtwitter_get(handle, sid, cfg["X2_FXTWITTER_HOST"], cfg["X2_FET_TIMEOUT"])
        if full and not full.get("__error__"):
            full["meta"] = post
            full_data["posts"].append(full)
            print(f"fxtwitter OK ({full['text_length']} chars)")
        elif ws is not None:
            # Fallback to CDP (with retry: max_retries=2, 3s delay)
            try:
                fb = cdp_extract_single(ws, post["url"], msg_id, max_retries=2)
                msg_id += 100
                if fb:
                    fb["handle"] = handle
                    fb["meta"] = post
                    full_data["posts"].append(fb)
                    print(f"CDP fallback OK ({fb['text_length']} chars)")
                else:
                    err = f"Both fxtwitter and x.com failed after 2 retries: {full.get('__error__', 'unknown')}"
                    full_data["errors"].append({"handle": handle, "status_id": sid, "error": err})
                    print(f"FAIL: {err}")
            except Exception as e:
                full_data["errors"].append({"handle": handle, "status_id": sid, "error": str(e)})
                print(f"FAIL: {e}")
        else:
            err = full.get("__error__", "unknown") if full else "unknown"
            full_data["errors"].append({"handle": handle, "status_id": sid, "error": err})
            print(f"FAIL: {err}")

        time.sleep(cfg["X2_RATE_LIMIT_SLEEP"])

    if ws:
        ws.close()

    # Write output
    out = Path(args.output) if args.output else p["inbox"] / f"xnote_full_{fetch_data['start']}.json"
    out.write_text(json.dumps(full_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[OK] Saved to: {out}")
    print(f"     Posts: {len(full_data['posts'])}")
    print(f"     Errors: {len(full_data['errors'])}")


if __name__ == "__main__":
    main()
