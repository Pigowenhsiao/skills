---
name: kami
description: AI 文件生成工具。當需要生成簡報、履歷、求職信、產品文件、一頁紙報告、變更日誌等正式文件時使用。基於 tw93/Kami（8.4K GitHub stars），使用約束語言 + 9 種模板，確保每次輸出都是可交付的專業文件。
version: 1.0.0
platforms: [linux, macos, telegram]
metadata:
  hermes:
    tags: [document, pdf, resume, slides, writing, template]
    trigger: ["生成文件", "做一份簡報", "寫履歷", "kami", " kami"]
---

# Kami — AI Document Generation

## 觸發條件

當需要生成以下類型文件時觸發：
- 履歷（Resume / CV）
- 求職信（Cover Letter / Recommendation Letter）
- 產品簡報（Product Brief / One-Pager）
- 投影片（Slides / Keynote）
- 變更日誌（Changelog / Release Notes）
-  equity report / 財務報告
- 投資備忘錄（Memo）
- landing page 內容

## 核心概念

**為什麼需要 Kami**：AI 生產的文件多數比人類手動寫的更好，但缺乏的是限制而非能力——沒有設計系統，每次输出去向都飄到灰色的通用格式。

Kami 的解法：一個約束語言 + 九個模板，足夠簡單讓 Agent 可靠運行，足夠嚴格讓每次輸出都是真正想交付的東西。

**三部曲**：
- [Kaku](https://github.com/tw93/Kaku)（書く）→ 寫代碼
- [Waza](https://github.com/tw93/Waza）（技）→ 訓練習慣
- **Kami**（紙）→ 交付文件

## 模板清單

| 模板 | 用途 | 語言 |
|------|------|------|
| Resume | 創辦人/工程師履歷，2頁 | EN/KO/中文 |
| Equity Report | 股權/財務報告 | 中文 |
| Slides | 主題演講投影片，6頁 | EN |
| One-Pager | 產品簡介，1頁 | EN |
| Letter | 求職/推薦信，1頁 | 中文/EN |
| Changelog | 產品發布日誌 | EN |
| Portfolio | 作品集 | 日語 |
| Landing Page | 產品 landing page | 多語言 |

## 使用方式

### 直接使用（無需安裝）

提供原始素材（純文字 markdown），說明語言和文件類型，Kami 會用約束語言生成對應模板的結構化文件。

### 必要輸入

1. **原始素材**：想轉換的內容（可以是混亂的 markdown 筆記、大綱、bullet points）
2. **語言**：簡體中文 / 繁體中文 / 英文 / 韓文 / 日文
3. **文件類型**：履歷 / 簡報 / 求職信 / 產品簡報 / 其他

### 輸出格式

結構化的 markdown 文件，可直接轉換為 PDF。包含：
- 統一的視覺層次
- 約束語言定義的字體、間距、色彩系統
- 對應模板的版面結構

## 約束語言核心要素

每個模板的約束系統包含：
- 字體規範（標題/內文/強調的具體字體）
- 間距規則（段落/章節/頁面間距）
- 色彩系統（主色/輔助色/強調色，HEX 值）
- 版面網格（欄數、邊界、對齊方式）
- 元件規範（抬頭/正文/引用塊/表格的具體樣式）

## 與其他技能的分工

| 場景 | 使用技能 |
|------|---------|
| 生成可交付的正式文件（履歷/簡報/報告） | **kami** |
| 生成投影片（Nano Banana Pro 格式） | ppt-master |
| 將文章寫成長文 | Article-writer |
| 推文寫作與優化 | tweet-writer / tweet-polish |

## 參考資源

- GitHub: https://github.com/tw93/Kami (8.4K stars)
- 作者: @HiTw93 / @tw93
- 三部曲: Kaku (代碼) + Waza (習慣) + Kami (文件)

## 範例輸出場景

**輸入**：一份混亂的個人經歷 bullet points
**處理**：指定「Resume + 繁體中文 + 工程師履歷」
**輸出**：符合約束語言的 2 頁專業履歷，可直接轉 PDF

**輸入**：產品功能列表 + 目標用戶描述
**處理**：指定「One-Pager + 英文」
**輸出**：結構化的 1 頁產品簡報模板

---

*Kami（紙, かみ）= 日語「紙」——好的想法最終落地的載體。*
