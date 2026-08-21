---
name: source-grill
description: Constrain a writing task to its evidence sources by clarifying references, citation boundaries, allowed inference, and unsupported claims. Use when summarizing papers, turning links into notes, or writing source-grounded analysis.
---

# Source Grill

## Description

這顆 skill 用來先把「資料邊界」問清楚，避免後面寫作時超譯、亂補、把自己的判斷冒充成原文主張。

## Workflow

1. 列出目前有哪些來源：
   - 論文
   - 網頁
   - 影片
   - repo
   - 使用者自己的筆記
2. 逐一確認每個來源的角色：
   - 主來源
   - 補充來源
   - 背景來源
3. 明確界定三種內容：
   - 可以直接忠實轉述
   - 可以合理推論，但要標示為分析
   - 不能主張，因為來源不足
4. 若有引用要求，先決定格式與精度：
   - 要不要逐段對照
   - 要不要保留章節名
   - 要不要附原始連結
5. 產出 source-bound brief，給後續摘要或寫作使用。

## Guardrails

- 不要把缺失資訊用常識自動補滿。
- 不要把外部背景知識混成來源原文。
- 只要證據不夠，就明說「來源不足」。

## Output

輸出：
- 來源清單
- 各來源角色
- 允許推論邊界
- 不可超譯的紅線
