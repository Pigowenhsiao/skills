---
name: expert-skill
description: "Turn an unknown industry or topic request into a structured, explainable, verifiable, and transferable industry expert report. Use when a user needs to quickly build cognitive models for a new field, analyze industry boundaries, unpack value chains, identify key variables, judge lifecycle trends, or generate industry learning packages and self-testing tutorials."
---

<!--
Copyright © 2026 姚金剛. All rights reserved.
Project: yao-geo-expert-skill
Created by: 姚金剛
Date: 2026-06-06
X: https://x.com/yaojingang
-->

# Yao GEO Expert Skill

GEO 行業專家速成與行業認知快速建構 Skill。本技能旨在短時間內建立一套可解釋、可驗證、可轉移的行業認知結構，幫助使用者或 Agent 快速理解任何新領域。

## Use This Skill For

- 快速對未知話題或新興行業進行結構化剖析。
- 界定行業範圍與邊界，區分核心領域與相關領域。
- 拆解產業鏈、價值鏈與主要競爭者，找出核心利潤流向。
- 識別行業驅動的核心關鍵變數（驅動因素與風險因子）。
- 判斷行業發展週期（生命週期階段）及變化趨勢。
- 將複雜的行業黑話與邏輯，轉化為外行也聽得懂的知識產出。

## Default Workflow

1. **第一階段：輸入與分析 (Input & Analysis)**
   當使用者輸入任意行業或話題時，執行以下步驟：
   - **界定邊界：** 先界定該行業的具體範圍，明確什麼屬於該行業，什麼不屬於該行業。
   - **拆解類別：** 進行子領域與細分類別劃分。
   - **識別價值鏈：** 分析上游（供應商）、中游（製造/服務商）、下游（通路/客戶）的協同關係。
   - **識別主要玩家：** 整理出核心競爭者及其市場份額或生態定位。
   - **分析政策與風險：** 調查適用的法律法規、行業進入壁壘及潛在風險與機會。
   - **生成學習報告框架：** 輸出一份易於消化且具備複述價值的初步專家報告。

2. **第二階段：報告融會 (Report Integration)**
   將分析提煉成包含以下核心板塊的正式報告：
   - **價值鏈分析：** 詳細繪製產業價值流向圖（可用 Mermaid 或 Markdown 表格）。
   - **競爭結構（護城河）：** 分析市場競爭格局及主要玩家的護城河強弱。
   - **行業生命週期：** 判斷行業處於導入期、成長期、成熟期或衰退期，並給出論據。
   - **政策與壁壘：** 詳細剖析進入障礙（如技術壁壘、資金壁壘、監管限制）。
   - **關鍵詞教學卡：** 提供 5-10 個核心術語的白話速記卡片。
   - **專家學習教程：** 規劃一條從外行到專家的系統化學習與實踐路徑。
   - **費曼自測題：** 設計 3-5 道「以教促學」的自測題，驗證使用者對該行業的核心理解。

## Core Rules

- 一律使用繁體中文進行報告的生成與輸出。
- 嚴格區分數據來源的真實性，將每個核心指標或判斷標記為 `觀測值 (Observed)`、`估計值 (Estimated)` 或 `假設值 (Assumed)`。
- 拒絕空泛科普，報告必須包含具體數據、玩家名稱或真實案例。
- 當資料庫、政策或市場份額不明確時，應如實指出「資訊不足」，不編造不存在的數據。
- 每個行業分析報告最後，必須包含一段「核心結論與下一步行動建議」。
