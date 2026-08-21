---
title: "每日新聞簡報系統"
date: 2026-04-30
tags:
  - llm-wiki
  - workflow
  - news
  - automation
  - rss
source: Hermes internal
source_url: null
processed: true
classification_path: 10-LLM-Wiki/references/daily-news-briefing-system.md
---

# 每日新聞簡報系統

## 概述

Hermes 每日新聞簡報系統是 Pigo 的自動化新聞攝入流程：每天 08:00 與 20:00 自動從 20 個 RSS 頻道抓取新聞，AI 嚴選 40 則優質內容，寫入 Vault 並推送到 GitHub，同時傳送摘要到 Telegram。

> 建置日期：2026-04-30

---

## 系統架構

```
RSS Feeds (20 channels)
    ↓
Python Fetcher (news-fetch.py)
    ↓ 266 articles/day
AI Filter + Summarizer (Hermes/minimax)
    ↓ 40 curated articles
Obsidian Vault (Daily/YYYY-MM-DD_每日精華.md)
    ↓
GitHub (auto push)
    ↓
Telegram (summary delivery)
```

---

## 數據源（20 個 RSS 頻道）

### 🇺🇸 美國財經（6 頻道）
| 頻道 | URL |
|---|---|
| Bloomberg Markets | `https://feeds.bloomberg.com/markets/news.rss` |
| CNBC Top News | `https://www.cnbc.com/id/100003114/device/rss/rss.html` |
| Reuters Business | `https://feeds.reuters.com/reuters/businessNews` |
| WSJ Markets | `https://feeds.a.dj.com/rss/RSSMarketsMain.xml` |
| Yahoo Finance | `https://finance.yahoo.com/news/rssindex` |
| MarketWatch | `http://feeds.marketwatch.com/marketwatch/topstories/` |

### 🤖 AI 發展（6 頻道）
| 頻道 | URL |
|---|---|
| TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/feed/` |
| VentureBeat AI | `https://venturebeat.com/category/ai/feed/` |
| MIT Tech Review | `https://www.technologyreview.com/feed/` |
| The Verge AI | `https://www.theverge.com/rss/ai-artificial-intelligence/index.xml` |
| Ars Technica | `https://feeds.arstechnica.com/arstechnica/technology-lab` |
| Import AI | `https://importai.substack.com/feed` |

### 🌍 國際新聞（5 頻道）
| 頻道 | URL |
|---|---|
| BBC World | `http://feeds.bbci.co.uk/news/world/rss.xml` |
| Reuters World | `https://feeds.reuters.com/reuters/worldNews` |
| AP News | `https://feeds.apnews.com/apnews/topnews` |
| NPR | `https://feeds.npr.org/1001/rss.xml` |
| Al Jazeera | `https://www.aljazeera.com/xml/rss/all.xml` |

### 🔥 熱門話題（3 頻道）
| 頻道 | URL |
|---|---|
| Hacker News | `https://hnrss.org/frontpage` |
| Reddit r/worldnews | `https://www.reddit.com/r/worldnews/.rss` |
| Reddit r/technology | `https://www.reddit.com/r/technology/.rss` |

---

## 執行腳本

**位置**：`~/.hermes/scripts/news-fetch.py`

**功能**：
- 抓取 20 個 RSS 頻道
- 過濾 24 小時內新文章
- 輸出 Markdown 格式（`-- ARTICLES START --` 到 `-- ARTICLES END --`）
- 擷取：source、title、link、summary、published

**依賴**：`feedparser`（需 `pip3 install feedparser`）

**效能**：約 15-20 秒完成，約 266 篇文章/天

---

## Cron 排程

| Job | 時間 | Job ID | 狀態 |
|---|---|---|---|
| 每日精選新聞簡報（早） | 00:08 UTC（+8 = 08:00 CST） | `e80cb72f` | active |
| 每日精選新聞簡報（晚） | 12:00 UTC（+8 = 20:00 CST） | `3dae937e` | active |

---

## 輸出格式

每天產出 `Daily/YYYY-MM-DD_每日精華.md`，格式：

```markdown
---
title: "每日精華"
date: YYYY-MM-DD
tags:
  - 每日精華
  - 新聞摘要
categories: Daily
---

# 每日精華 YYYY-MM-DD

📊 今日共攔截 N 篇，嚴選 40 則優質新聞

## 🇺🇸 美國財經（10則）
[10則嚴選新聞：標題 + 1-2句摘要 + 原文連結]

## 🤖 AI 發展（10則）
[10則]

## 🌍 國際新聞（10則）
[10則]

## 🔥 熱門話題（10則）
[10則]

## 💡 今日觀察
[2-3句宏觀趨勢總結，信號銳利]
```

---

## AI 嚴選標準

過濾原則：
- ❌ 廣告、贊助內容
- ❌ 純號召性標題（無實質資訊）
- ❌ 重複事件的不同來源報導（保留最完整的一則）
- ✅ 有具體數據、事件、人物的新聞
- ✅ 趨勢信號（宏觀影響）
- ✅ 技術深度內容

每個分類固定 10 則。

---

## 維護日誌

| 日期 | 事件 |
|---|---|
| 2026-04-30 | 初版建置：20 頻道、news-fetch.py、早晚兩支 cron |

---

## 相關連結

- 腳本：`~/.hermes/scripts/news-fetch.py`
- 今日簡報：[[Daily/2026-04-30_每日精華]]
- Cron 管理：見 Hermes cronjob list
