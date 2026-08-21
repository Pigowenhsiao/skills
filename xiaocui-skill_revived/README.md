<!-- BEGIN AGENT_DIRECTORY_README -->
# xiaocui-skill

## Purpose

蒸餾自「小翠時政財經」頻道的思維作業系統 skill。基於 31 個本地語料直播文字稿（2022-09-23 ~ 2026-11-06，約 101 萬字）反覆出現的真信念提煉。

## 蒸餾方法

採用 [nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 的「**本地語料模式**」（Phase 0A → Phase 0.5 → Phase 1），4 個並行 subagent 分析：

| Agent | 任務 | 輸出檔案 |
|-------|------|---------|
| 1 | 核心心智模型 | `references/research/01-mental-models.md` |
| 2 | 決策啟發式 | `references/research/02-decision-heuristics.md` |
| 3 | 表達 DNA | `references/research/03-expression-dna.md` |
| 4 | 議題光譜 | `references/research/04-topic-spectrum.md` |

## 目錄結構

```
xiaocui-skill/
├── SKILL.md                                    # 主要 skill 入口（325 行）
├── README.md                                   # 本檔案
├── scripts/                                    # 預留：未來工具腳本
└── references/
    ├── research/                               # 4 個並行 Agent 的調研結果
    │   ├── 01-mental-models.md                 # 7 個心智模型（347 行）
    │   ├── 02-decision-heuristics.md           # 12 條啟發式（450 行）
    │   ├── 03-expression-dna.md                # 25 詞 + 8 句式（413 行）
    │   └── 04-topic-spectrum.md                # 28 場議題分布（414 行）
    └── sources/
        └── transcripts/                        # 31 個原始直播文字稿（2.9MB）
```

## 主要發現

### 7 個核心心智模型
1. **資本主義底層邏輯**：美聯儲永遠為流動性兜底
2. **看穿口號**：銀行帳本是經濟的 X 光片
3. **逆向思維**：物理稀缺才是最大的稀缺
4. **火眼金睛**：底層徵信術
5. **人礦模型**：利益結構決定行為
6. **系統性裹挾**：第一步最危險
7. **底層邏輯**：看穿碎片信息

### 12 條決策啟發式
- **底層框架（4 條）**：H1 誰能掙錢、H2 數字 vs 口號、H3 趨勢外推、H11 圈子污染
- **投資操作（5 條）**：H4 遠期 PE、H5 不追高、H6 現金流防禦、H7 板塊輪動、H8 集中持倉
- **分析識別（2 條）**：H9 常識判斷、H10 大外宣四步識別法
- **表達紀律（1 條）**：H12 拒絕模糊 + 數字張力

### 議題轉型（重要時代訊號）
- **2022-2024**：中國金融批判為主（100%）
- **2025-2026**：美股投資 + 宏觀為主（64%）
- **轉型訊號**：小翠已從「中國批判者」轉型為「美股陪伴者」

## 與其他 Skill 的關係

| 既有 skill | 關係 |
|----------|------|
| `xiaocui-thinking-distill/` | 早期版本（2026-04，基於 2026-01~04 影片，20 部）以中國金融批判為主 |
| `小翠-perspective/SKILL.md` | 另一版本（基於 5 個語音直播），投資思維框架 |
| **`xiaocui-skill/`（本檔）** | **2026-06 最新版，基於 31 個 transcript 完整 4 年時序，呈現成熟期美股+宏觀雙核視角** |

## 使用方式

### 觸發詞
- 「用小翠的視角」
- 「小翠會怎麼看」
- 「小翠思維」「小翠 perspective」
- 「xiaocui」
- 「看穿口號」「物理稀缺」「美聯儲兜底」
- 「銀行 X 光片」

### 應用場景
- 美股投資策略分析
- 央行政策解讀
- 中國金融系統批判
- AI 概念股泡沫判斷
- 外宣文/官方宣傳識別
- 反脆弱個人資產配置

## Provenance

- provided_by_agent: nuwa-skill (local source mode)
- provided_by_computer: Pigo workstation
- processing_skill: nuwa-skill
- processed_at: 2026-06-15
- source_count: 31 transcripts, 1,012,415 chars
- time_span: 2022-09-23 ~ 2026-11-06
<!-- END AGENT_DIRECTORY_README -->
