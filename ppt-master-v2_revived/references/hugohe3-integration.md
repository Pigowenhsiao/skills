# hugohe3/ppt-master Integration Reference

> **Created**: 2026-06-26 (Pigo 21:06 UTC 指示)
> **Source**: https://github.com/hugohe3/ppt-master v2.11.0 (Hugo He, Taiwan)
> **License**: MIT (requires attribution + copyright notice)
> **Purpose**: 從 hugohe3/ppt-master 抽 5 個 workflow 概念，看是否整合進 ppt-master-v2
> **Status**: Reference only — **未 commit、未 git add**，等你 review

---

## 為什麼這個 reference 存在

- hugohe3/ppt-master（公開 MIT，3 萬 stars）跟我們內部 `ppt-master-v2` **功能重疊 60-70%**
- 兩個**技術路線完全不同**：hugohe3 用 **DrawingML**（Python + python-pptx 寫原生 XML），我們用 **SVG → python-pptx**（包裝 SVG 進 PPTX）
- hugohe3 強調「**real PowerPoint**」（每個元素可直接編輯），我們強調「**SVG 視覺優先**」
- Pigo 想看是否能**部分借鑑**而不 clone / fork

---

## 5 個 workflow 概念（從 hugohe3 README 抽出）

### 1. Native DrawingML 概念（**最關鍵**）

**hugohe3 怎麼做**：
- output 是 **DrawingML 原生形狀**（不是包進 PPTX 的 SVG/PNG）
- 每個 element（text box、shape、chart）都是 **PowerPoint 原生對象**
- 用 python-pptx 直接寫 OOXML（`prs.slides[0].shapes.add_shape(...)` 這類 API）
- 結果：在 PowerPoint 裡**每個元素可直接點選編輯**

**我們 ppt-master-v2 怎麼做**：
- SVG → 圖片 → 用 python-pptx `add_picture()` 嵌進 PPTX
- 結果：投影片是**圖片**，**不能**直接在 PowerPoint 編輯

**整合方向**（**大改**）：
- 把 SVG 渲染階段保留（**視覺資產**）+ 加 DrawingML 輸出階段（**可編輯骨架**）
- 難度：高，需要重寫主要 pipeline

**是否值得**：**取決於 Pigo 是否常用 PowerPoint 手動後製**。如果常用，**值得**；如果只是「生 deck 就走」，**不必**。

---

### 2. Template 機制（用戶自帶 .pptx）

**hugohe3 怎麼做**：
- 用戶可**指定自己已有的 .pptx** 當 template
- hugohe3 讀 template 的 master slides + theme colors + fonts
- 然後用 AI 生成內容，**套進** template 的視覺風格

**我們 ppt-master-v2 怎麼做**：
- 內建多套 template（`templates/layouts/`）
- 用戶**不能**帶自己的 .pptx

**整合方向**（**中改**）：
- 加 `user_template_path` 參數
- 寫一個 template parser：讀 master slides、theme、fonts
- 改產出：把 SVG 套進用戶的 theme 而不是內建的

**是否值得**：**取決於 Pigo 是否要「同一個 deck 但每次套不同公司 brand」**。要的話，**值得**。

---

### 3. Audio Narration 完整 workflow

**hugohe3 怎麼做**：
- speaker notes → ElevenLabs TTS → 嵌入 PPTX 的 audio track
- 投影片播放時**自動讀出 speaker notes**
- MIT license 允許這種商業整合

**我們 ppt-master-v2 怎麼做**：
- 有 `workflows/generate-audio.md` 但**未確認完整度**
- workflow 提了 ElevenLabs 整合但**沒實際生成**

**整合方向**（**小改**）：
- 補完 `workflows/generate-audio.md`
- 寫實際的 `scripts/generate-audio.py`（用 ElevenLabs API）
- 測試 PPTX 是否能嵌入 audio

**是否值得**：**取決於 Pigo 是否要 podcast-style 簡報**。如果只是會議簡報，**不必**。

---

### 4. Semantic Versioning（v2.11.0）

**hugohe3 怎麼做**：
- 用 [Semantic Versioning](https://semver.org/)
- README 開頭有 `[![Version](https://img.shields.io/badge/version-v2.11.0-blue.svg)]`
- 有 `https://github.com/hugohe3/ppt-master/releases`

**我們 ppt-master-v2 怎麼做**：
- **沒**版本系統
- 內部 skill，沒有 release process

**整合方向**（**小改**）：
- 在 SKILL.md frontmatter 加 `version` 欄位
- 開始追蹤 `ppt-master-v2-vX.Y.Z`

**是否值得**：**取決於 Pigo 是否要在多台機器 / 多個 OpenClaw session sync skill**。要的話，**值得**。

---

### 5. Audience Segmentation（設計風格分類）

**hugohe3 怎麼做**：
- 6 個範例 deck 分類：
  - **Editorial Magazine**（Pritzker 2026 architecture review）
  - **Data Journalism**（Bloomberg-style dark dashboard）
  - **Swiss Grid**（modular grid, restrained type）
  - **Glassmorphism SaaS**（translucent layers）
  - **Memphis Pop**（bold primaries, geometric patterns）
  - **Risograph Zine**（duotone print）
- 每個是**獨立 audience + 視覺風格**

**我們 ppt-master-v2 怎麼做**：
- 內建 templates 有類似分類但**沒**明確 audience 標籤

**整合方向**（**小改**）：
- 把 `templates/layouts/` 重新整理成 audience-based metadata
- 加 frontmatter：`audience: data-journalism`, `style: dark-dashboard`

**是否值得**：**視覺效果提升有限**，但**管理方便**。**可有可無**。

---

## 整合的 3 個選擇（**不繞 Q**，給最佳解）

### 🅐 0 改動（**推薦**）

**只**留這份 reference。**不**改 ppt-master-v2。理由：
- ppt-master-v2 剛 dedupe 完（commit `f9639da78`，2026-06-26）
- 改它要再走一次 dedupe 流程
- 改之前**至少**要 clone hugohe3 進來讀 source code（不是只讀 README）

### 🅑 部分整合（**中期**）

選 1-2 個概念實際整合進 ppt-master-v2，例如：
- **#3 audio workflow**（小改，1 個 workflow + 1 個 script）
- **#4 versioning**（小改，1 個 SKILL.md frontmatter 加 `version`）

**時間成本**：半天到一天

### 🅢 全面整合（**長期**，**不建議**）

把 hugohe3 的 **DrawingML pipeline** 整個 pull 進來，重寫我們的 SVG → PPTX。**時間成本**：一週以上，且**會失去 SVG 視覺風格的優勢**。

---

## 不做的事（明確記錄）

- ❌ **不** clone `hugohe3/ppt-master` 到 `~/Downloads/`（clone 失敗 2 次，SIGKILL）
- ❌ **不** git add 這個 reference（待 Pigo review）
- ❌ **不**碰 `~/Documents/Agent/skills/ppt-master-v2/` 的 SKILL.md / scripts / templates
- ❌ **不** commit 到 Agent repo
- ❌ **不** push 到 remote

---

## 來源 / 證據

- hugohe3 README: https://raw.githubusercontent.com/hugohe3/ppt-master/main/README.md (fetched 2026-06-26 21:06 UTC)
- 我們 ppt-master-v2 結構: `~/Documents/Agent/skills/ppt-master-v2/` (52MB, 11637 icons, 5 workflows, 12 references)
- MEMORY P2 [2026-06-26] ppt-master dedupe + 11 PPT skills 索引

---

## License 注意

hugohe3/ppt-master 是 **MIT License**。如果未來真要整合：
- ✅ MIT 允許 fork / 修改 / 商用
- ⚠️ MIT 要求保留 **copyright notice** + **license text**
- ⚠️ 整合時要在 SKILL.md 或 references/ 加：
  ```
  Based on hugohe3/ppt-master (MIT License)
  Copyright (c) Hugo He
  https://github.com/hugohe3/ppt-master
  ```

---

## Next action

- **讀完**這份 reference → 決定要不要實際整合哪個 workflow 概念
- 如果**要**整合 → 先 `git clone` 進 `~/Downloads/` 讀 source code（網路穩定後）
- 如果**不**整合 → 這份 reference 留在 `references/`，未來需要時複習
