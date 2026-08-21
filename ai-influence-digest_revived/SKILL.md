---
name: ai-influence-digest
description: 生成「AI影响力信息汇总」周报：在不使用 X API 的前提下，用 Google 搜索批量扫描指定 X 账号过去7天推文（偏工具/工作流/教程/Prompt），过滤出对内容创作者立刻可用的高价值内容，产出结构化中文周报 Markdown，并生成多页截图海报（用于 Telegram/知识星球/Notion）。当你需要做每周 AI Builder 账号扫描、实用推文精选、工作流/方法论周报、周报截图生成时使用。
---

# AI影响力信息汇总（AI Influence Digest）

目标：把“刷一周 X”变成可复用的内容雷达流水线。

约束（强制）：
- **绝对禁止使用 X API**（包括任何 X API 搜索/时间线拉取）。
- 允许：Google 搜索（opencli）+ 公开页面抓取（r.jina.ai/web_fetch）+ 本地整理与截图。

## 快速流程（推荐）

### 0) 准备账号清单
- 默认账号列表：`references/accounts_65.txt`
- 可以按需删减/追加（每行一个 handle，不带 @）。

### 1) 扫描候选推文（收集阶段）
使用脚本抓“过去 N 天”候选推文（只拿 URL + 公开网页文本，不走 X API）。

```bash
python3 scripts/scan_x_weekly.py \
  --accounts references/accounts_65.txt \
  --days 7 \
  --batch-size 10 \
  --per-search 20 \
  --outdir ./output/ai-influence-digest
```

输出：
- `candidates.json`：候选列表（url/handle/text/score）
- `candidates.md`：便于快速人工扫读

> 如果遇到搜索源封锁/挑战：降低 batch-size、减少 per-search，或改用浏览器自动化（pinchtab/agent reach）分批搜。

### 2) 按标准筛选 5-10 条高价值内容（编辑阶段）
筛选规则见：`references/filters.md`

产出要求（每条 150-200 字，必须含 Why it’s useful + 推文链接）：

- 标题用中文强调“实用价值”
- 结构固定：
  - Title
  - Account
  - Type（🛠️ 可复用方法｜💡 工作流优化｜📝 小技巧｜🚀 新工具）
  - Core Methods/Techniques：3 条可执行项
  - Why it’s useful：1-2 句解释“为什么内容创作者立刻能用”
  - Tweet Link：必须是原始推文 URL

### 3) 生成周报截图（发布物阶段）
把最终周报 Markdown 渲染成多页截图（默认小红书文字海报风格，适合发 TG/星球）。

```bash
bash scripts/render_weekly_screenshots.sh \
  ./output/ai-influence-digest/weekly_report.md \
  /Volumes/T7/OpenClaw/Output/workspace-output/AI影响力信息汇总 \
  "2026年04月15日"
```

输出目录会生成 `01.png` `02.png` ...

## 常见坑

### Playwright Python API 完全替代方案（2026-04-17 實測成功）

當所有搜尋 API 和 opencli 都失效時，直接用 Playwright Python 爬新聞源效果最好。

**為什麼不用 `playwright open` CLI**：`playwright open` 會開啟 GUI 瀏覽器視窗，在無頭環境（headless）中會超時。**要用 Python API**：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('https://techcrunch.com/category/artificial-intelligence/', timeout=20000)
    page.wait_for_timeout(3000)
    
    # TechCrunch 文章列表用 .loop-card CSS class
    cards = page.query_selector_all('.loop-card')
    for c in cards[:20]:
        txt = c.inner_text()[:200].replace('\n', ' | ')
        hrefs = c.query_selector_all('a')
        link = hrefs[0].get_attribute('href') if hrefs else ''
        print(f'{txt}\n  -> {link}')
    browser.close()
```

**實測可用新聞源**：
- TechCrunch AI：`techcrunch.com/category/artificial-intelligence/`（`.loop-card`）
- TechCrunch 分頁：`/category/artificial-intelligence/page/2/`（第 2 頁，以此類推）
- VentureBeat AI：`venturebeat.com/ai/`（`article` 標籤 + `h2` 標題）
- VentureBeat 文章內文：`venturebeat.com/technology/<slug>`（`p` 標籤取段落）

**注意事項**：
- TechCrunch 的 `.loop-card` 連結有時指向首頁（要用 href 裡的實際網址），要人工檢查
- 部分文章頁面讀取會超時（20s），建議用 try/except 包住每篇文章
- Bing/Google 搜尋全部被 captcha 擋死，Playwright Python API 是目前最穩定的替代方案

### opencli google search 静默失败（2026-04-17 实测）
**症状**：`opencli google search` 命令返回 exit code 0 但输出为空，`scan_x_weekly.py` 跑完 `candidates.json` 为空数组。

**根因**：opencli 的 `google search` 命令需要 Chrome Browser Bridge extension（`github.com/jackwener/opencli/releases`），未安装时静默失败（不报错）。

**解法**：
1. 安装 Browser Bridge extension：Chrome → `chrome://extensions` → 开启「开发者模式」→ 加载 `opencli` 包
2. 或者用上方 Playwright Python API 方案爬新聞源（主要推薦）

### CloakBrowser API 正確用法（2026-05-10 實測）
**症狀**：`ModuleNotFoundError: No module named 'cloakbrowser'` 或 `ImportError: cannot import name 'CloakBrowser'`

**正確 import**：
```python
from cloakbrowser import launch

# 非 async 腳本中直接用
browser = launch(headless=False)
page = browser.new_page()
page.goto("https://x.com/i/flow/login", timeout=30000)
```

**禁止在 asyncio 迴圈內直接呼叫 `launch()`** — `launch()` 內部啟動 sync Playwright，會炸：
```
playwright._impl._errors.Error: It looks like you are using Playwright Sync API inside the asyncio loop.
Please use the Async API instead.
```
解法：把 `launch()` 放在 async 函式外部，或用標準 `playwright.sync_api` 代替。

**有頭模式需要 xvfb-run**（Linux 無頭環境）：
```bash
xvfb-run python3 -c "
from cloakbrowser import launch
browser = launch(headless=False)
# ...
"
```
錯誤 `Missing X server or $DISPLAY` = 沒有虛擬顯示，必須用 xvfb-run 包住。

**Twitter 登入網址**：`https://x.com/i/flow/login`

**CloakBrowser vs Playwright**：CloakBrowser 回傳的是標準 Playwright Browser 物件，所以 `.new_page()`、`.goto()` 等方法都相同，只是啟動方式不同。

### r.jina.ai 對 x.com 抓取被封鎖
**症状**：`requests.get("https://r.jina.ai/" + tweet_url)` 返回空文本或超时。

**解法**：改用 Playwright Python API → 直接访问 `x.com/<handle>/status/<id>` 手动读取内容，或从新闻源（TechCrunch、VentureBeat、IT之家）获取同类资讯。

### 候选过多时
- 先按 score 排序 + 手动筛掉"硬件/融资/纯 benchmark"。

## 替代工作流（当 opencli 不可用时）

当 `opencli google search` 失败，且 r.jna.ai 也被封时，用浏览器直接从新闻源收集 AI 週报素材：

```bash
# 1. 用 agent-browser 打开 AI 新闻聚合页
browser_navigate url="https://techcrunch.com/category/artificial-intelligence/"

# 2. 逐篇阅读感兴趣的文章，记录链接和摘要
# 3. 对于 X 账号推文，直接 browser_navigate 到 x.com/<handle>/status/<id>

# 4. 整理成周报 Markdown
```

实测可用的新闻源：
- TechCrunch AI（`techcrunch.com/category/artificial-intelligence/`）— 无 bot 检测
- VentureBeat AI（`venturebeat.com/category/ai/`）
- IT之家 AI（`ithome.com.tw/tags/AI`）

## 资源
- `scripts/scan_x_weekly.py`：批量收集候选推文（Google 搜索 + 公开抓取）
- `scripts/render_weekly_screenshots.sh`：把 Markdown 周报分页截图
- `references/accounts_65.txt`：默认 65 账号清单
- `references/filters.md`：筛选标准（内容创作者视角）
