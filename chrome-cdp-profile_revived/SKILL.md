---
name: chrome-cdp-profile
version: 1.0.0
description: >
  Use Chrome with user's real profile + CDP to access authenticated X.com content
  (Articles, Notes, full tweet threads). Triggers: "X article", "X 付費內容",
  "login X CDP", "chrome profile CDP".
---

# Chrome CDP Profile — 取得已登入的 X.com 內容

## 核心問題

X.com 的付費 Article、Super Follows 內容、某些 NoteTweet 無法透過 fxtwitter / vxtwitter / jina.ai 取得全文。這些內容需要**有效的 X.com 登入 session** 才能讀取。

## 解決方案

使用 Pigo 實際 Chrome 瀏覽器的 profile（已登入 X.com），透過 CDP (Chrome DevTools Protocol) 直接抓取內容。

## Chrome Profile 路徑

| Profile | 路徑 | X.com Cookies | 用途 |
|---------|------|---------------|------|
| **Chrome Profile 1** | `~/.config/google-chrome/Profile 1` | 部分（guest/metrics） | 主要 CDP |
| **baoyu-skills** | `~/.local/share/baoyu-skills/chrome-profile` | ✅ 有 X.com cookies | 有 cookies 但無付費 session |
| **bb-browser (port 19825)** | `/tmp/bb-browser-chrome-19825` | ✅ 有 X.com guest | Headless，無付費內容 |

## 啟動已登入的 CDP Chrome

### 方法 1：使用 Chrome Profile 1（有你的完整 session）

```bash
# 殺掉舊的（如果有的話）
kill $(pgrep -f "remote-debugging-port=19926") 2>/dev/null

# 啟動，綁定你的實際 Chrome profile
/opt/google/chrome/chrome \
  --user-data-dir=~/.config/google-chrome/Profile\ 1 \
  --profile-directory=Default \
  --remote-debugging-port=19926 \
  --no-first-run \
  --no-default-browser-check \
  --disable-translate \
  --disable-extensions \
  --disable-background-networking \
  --disable-sync \
  --no-sandbox &

sleep 6
```

### 方法 2：使用 baoyu-skills profile（有 cookies）

```bash
BAOYU_PROFILE=~/.local/share/baoyu-skills/chrome-profile

/opt/google/chrome/chrome \
  --user-data-dir="$BAOYU_PROFILE" \
  --profile-directory=Default \
  --remote-debugging-port=19925 \
  --no-first-run \
  --no-default-browser-check \
  --disable-translate \
  --disable-extensions \
  --disable-background-networking \
  --disable-sync \
  --no-sandbox &
```

## 確認 CDP 是否正常

```bash
curl -s http://localhost:19926/json/version | python3 -c "
import sys, json
d = json.load(sys.stdin)
print('Browser:', d.get('Browser'))
print('WS:', d.get('webSocketDebuggerUrl'))
"
```

## 用 Playwright 連線並抓取 X.com 文章

```python
import asyncio
from playwright.async_api import async_playwright

async def fetch_x_article(article_url):
    async with async_playwright() as p:
        # 1. 確認 WS URL
        import json, urllib.request
        with urllib.request.urlopen("http://localhost:19926/json/version") as r:
            data = json.loads(r.read())
            ws_url = data["webSocketDebuggerUrl"]

        # 2. 連線到 CDP Chrome
        browser = await p.chromium.connect_over_cdp(ws_url)

        # 3. 找到已登入的 tab（x.com/home）
        page = None
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if 'x.com/home' in pg.url or 'x.com' in pg.url:
                    page = pg
                    break
            if page:
                break

        # 4. 沒有就開新 page
        if not page:
            page = await browser.new_page()

        # 5. 導航到目標 URL
        await page.goto(
            article_url,
            timeout=45000,
            wait_until="domcontentloaded"
        )
        await page.wait_for_timeout(8000)

        # 6. 取得完整文章文字
        txt = await page.inner_text('article')

        # 7. 截圖確認
        ss = await page.screenshot(full_page=True)
        with open('/tmp/x_article.png', 'wb') as f:
            f.write(ss)

        await browser.close()
        return txt
```

## 完整腳本：抓取 X.com Article 內容

```python
#!/usr/bin/env python3
"""fetch_x_article.py — 用 CDP Chrome 抓取已登入的 X.com 內容"""
import asyncio, sys
from playwright.async_api import async_playwright

ARTICLE_URL = sys.argv[1] if len(sys.argv) > 1 else "https://x.com/eng_khairallah1/status/2069341916798369801"
CDP_PORT = 19926

async def main():
    async with async_playwright() as p:
        # Get WS URL
        import json, urllib.request
        try:
            with urllib.request.urlopen(f"http://localhost:{CDP_PORT}/json/version") as r:
                data = json.loads(r.read())
                ws_url = data["webSocketDebuggerUrl"]
        except Exception as e:
            print(f"CDP not available on port {CDP_PORT}: {e}")
            return

        browser = await p.chromium.connect_over_cdp(ws_url)

        # Find existing x.com tab
        page = None
        for ctx in browser.contexts:
            for pg in ctx.pages:
                if 'x.com/home' in pg.url or 'x.com' in pg.url:
                    print(f"Using existing tab: {pg.url}")
                    page = pg
                    break
            if page:
                break

        if not page:
            page = await browser.new_page()

        await page.goto(ARTICLE_URL, timeout=45000, wait_until="domcontentloaded")
        await page.wait_for_timeout(8000)

        print(f"URL: {page.url}")

        # Get article text
        try:
            txt = await page.inner_text('article')
            print(f"\nArticle ({len(txt)} chars):\n{txt}")
        except Exception as e:
            print(f"article error: {e}")

        # Screenshot
        ss = await page.screenshot(full_page=True)
        out = '/tmp/x_article_fetch.png'
        with open(out, 'wb') as f:
            f.write(ss)
        print(f"\nScreenshot: {len(ss)} bytes -> {out}")

        await browser.close()

asyncio.run(main())
```

## CDP Port 對照表

| Port | Chrome 版本 | Profile | 狀態 |
|------|------------|---------|------|
| **19825** | Chrome/149.0.7827.102 (Headless) | bb-browser | Headless，X.com 擋 Article |
| **19925** | Chrome/149.0.7827.200 | baoyu-skills | 有 cookies，無付費 session |
| **19926** | Chrome/149.0.7827.200 | Chrome Profile 1 | ✅ 有完整登入 session，優先使用 |

## 已知限制

1. **Chrome Profile 1 是 `--no-sandbox` 啟動**：某些 Linux 環境需要 `--no-sandbox`，這表示它是隔離的 profile 實例
2. **Article 點擊後跳轉到登入牆**：某些付費 Article 點擊後仍需要 X Premium session，不是所有內容都能用這個方法取得
3. **CDP Port 必須手動指定**：每次啟動後要從 `/json/version` 取 WS URL，不能用 `ws://localhost:PORT/` 必須帶完整 UUID
4. **不可用 `browser.new_page()`**：用 `connect_over_cdp` 後已有 context，直接用現有 tab 即可

## One Line

**用你自己的 Chrome Profile + CDP = 等於在你的瀏覽器上操控，繞過 X.com 的付費牆。**
