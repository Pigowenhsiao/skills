# Source Mapping

這份文件用來把原始 `mattpocock/skills` 的工程 workflow，映射成新的寫作 workflow。

## 設計原則

- 保留原 skill 的「流程骨架」
- 改寫成寫作場景的輸入、輸出與驗收條件
- 避免只做名稱翻譯，卻保留不合適的工程假設

## Mapping Table

| 原始 Matt Skill | 新研究版 Skill | 主要用途 | 主要調整 |
| --- | --- | --- | --- |
| `grill-me` | `topic-grill` | 問清楚題目、受眾、目的、文風、交付格式 | 從功能需求訪談，改成寫作 brief 訪談 |
| `grill-with-docs` | `source-grill` | 問清楚來源、術語、可推論邊界、引用規則 | 從技術文件審問，改成 source-bound 寫作約束 |
| `to-prd` | `to-outline` / `paper-to-brief` | 把模糊想法轉成大綱或摘要 brief | 從產品需求文件改成文章／論文結構文件 |
| `to-issues` | `article-to-outline` / `novel-arc-outline` | 拆成章節、段落、情節 arc 任務 | 從工程 issue 拆解改成寫作段落與章節拆解 |
| `tdd` | `evidence-first-drafting` | 先列主張，再補證據，再寫段落 | 從 test-first 改成 evidence-first |
| `diagnose` | `draft-diagnose` / `novel-continuity-diagnose` | 找出草稿問題與一致性問題 | 從 bug 診斷改成文本診斷 |
| `zoom-out` | `argument-zoom-out` | 拉高視角看整篇結構與論證線 | 從系統層視角改成論述結構視角 |
| `improve-codebase-architecture` | `improve-article-architecture` | 優化文章結構、段落順序、訊息密度 | 從程式架構改成文章架構 |
| `write-a-skill` | `write-a-writing-skill` | 後續把研究結果正式寫成 skill | 保留 skill authoring，但加寫作驗收規範 |
| `ubiquitous-language` | `writing-glossary` | 建立作者／研究者共享術語表 | 從 DDD 語言表改成文稿用語一致性 |

## 額外新增，不直接對應 Matt

這些是因為寫作場景本身需要，尤其是論文與長篇小說，而新增的能力：

- `claim-evidence-check`
- `paper-summary-expand`
- `novel-world-grill`
- `novel-to-bible`
- `novel-long-drafting`

## 與 story-long-write 的整合點

長篇小說線不是只靠 Matt skill 改寫，還會吸收 `story-long-write` 的幾個關鍵方法：

- 長篇寫作是工程，不是單次靈感輸出
- 要有世界觀、人設、情節線、時間線、伏筆管理
- 要把單章寫作放進整體卷綱與節奏控制裡
- 每次續寫前要先確認上一章狀態與未回收伏筆
