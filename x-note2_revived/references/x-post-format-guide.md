# X 推文特有的 capture_method 與 social_signals 說明

## capture_method 的取值

| 值 | 意義 |
|----|------|
| `bb-browser/CDP single-status DOM` | 用 CDP 從單篇頁面 DOM 抓取（x-note 標準方式） |
| `bb-browser/CDP timeline DOM` | CDP timeline 抓取（僅候選，不可當最終摘要） |
| `jina-read` | 用 jina.ai 讀取（x-note 補充或 fallback） |
| `manual` | 手動貼上，無自動化抓取 |
| `ADHX API` | 用 ADHX API 抓取（KAW 流程） |
| `logged-in Chrome CDP DOM` | 已登入 Chrome 的 CDP 抓取 |

原則：只用 `single-status` 或 `jina-read` / `manual`；嚴禁把 `timeline DOM` 當成完整原文。

## engagement{} 的來源

engagement 數據來自：

1. **xnote_complete_*.json** 中的 `likes` / `reposts` / `replies` / `views`（CDP single-status）
2. **xnote_fetch_*.json** 中的 timeline 可見數據（不完整，只能當參考）
3. **jina-read** 抓取的頁面（視頁面是否有暴露互動數據）

若 JSON 中無 engagement 數據，`engagement{}` 欄位仍需保留但標註來源：

```yaml
engagement:
  views: null   # timeline 可見，數字可能不準
  likes: null
  reposts: null
  replies: null
  bookmarks: null
```

## media_ids 的處理

X 推文中的圖片/影片有 `media_key` 或 `media_id`，格式如 `HJfBibdXYAMr7Wy`。

從 JSON 取得後，寫入 `media_ids[]`，並在 `## Reference` 的 `### Media References` 中提供可解析的 URL：

```
https://pbs.twimg.com/media/<media_id>.<ext>
https://video.twimg.com/ext_tw_video/<media_id>.mp4
```

副檔名（jpg/png/mp4）無法從 media_id 直接推斷，若未知可寫 `ext: unknown`。

## content_hash 的計算

用來確認原文未經竄改。從 `xnote_complete_*.json` 的 `text` 欄位計算：

```python
import hashlib
hash = hashlib.sha256(post_text.encode('utf-8')).hexdigest()
```

若無法從 JSON 取回原文，可填空字串，但需在 `score_reason` 中說明。

## score_reason 的撰寫原則

| 元素 | 說明 |
|------|------|
| **內容類型** | 工作流分享 / Prompt 模板 / 實地觀察 / 商用案例 |
| **原創性** | 是否原創拆解 vs 轉發評論 |
| **實用性** | 可直接複用 vs 僅供參考 |
| **數字/證據** | 具體數字增加可信度 |
| **長期價值** | evergreen vs 時效性 |

範例：

```
高傳播量（150K+ 瀏覽）、原創工作流拆解，
商用落地 demonstration，具體數字（10萬+）提供可信度，
Prompt 完整可複用，屬於 AI 影片生成商用落地標竿案例。
```

## 與 llm-wiki 最大的不同

| | llm-wiki | x-note2 |
|---|---|---|
| **frontmatter** | `sources[]` + `type` + `tags` | 上述全部 + `tweet_id` + `engagement{}` + `media_ids[]` + `capture_method` |
| **Reference** | `## Reference` 含原文 | 同上，但多了 `### Media References` |
| **Source Snapshot** | 無 | 有，統一呈現時間/互動/抓取方式 |
| **score/scoring** | 無 | 有，承繼 x-note 的 1-5 機制 |
| **互動數據** | 無 | `engagement{}` 結構化呈現 |

## 從既有的 x-note 轉換時的對照表

| 舊欄位 | x-note2 對應 |
|--------|------------|
| frontmatter `score` | 直接保留 |
| frontmatter `score_reason` | 直接保留 |
| frontmatter `tweet_id` | 直接保留 |
| frontmatter `content_hash` | 需重新計算（若舊值為空） |
| frontmatter `capture_method` | 需補充（jina-read / CDP） |
| `## 原始貼文（完整原文）` | → `## Reference` + `### Complete X Post Text` |
| `<!-- yaml ... engagement -->` | → `engagement{}` frontmatter block |
| `## 相關標籤` | → frontmatter `tags[]` |
| `## 與現有知識的關聯` | → `## Detailed Analysis` + `## Related Notes` |
| （無對應） | → 新增 `## Source Snapshot` + `## Why It Matters` |
