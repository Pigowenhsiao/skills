---
name: novel-continuity-diagnose
description: Diagnose continuity problems in long-form fiction by checking character consistency, world rules, timeline, unresolved setups, and chapter-to-chapter logic. Use when revising serialized fiction or validating a continuation draft.
---

# Novel Continuity Diagnose

## Description

這顆 skill 用來抓長篇小說最容易累積的慢性錯誤：人設飄移、設定衝突、時間線混亂、伏筆失聯。

## Workflow

1. 先讀：
   - story bible
   - 當前章節或新草稿
   - 必要時讀上一章與上一個 arc 摘要
2. 用五個面向檢查：
   - 人設是否穩定
   - 世界規則是否被破壞
   - 時間線是否對得上
   - 伏筆是否遺漏、誤回收或矛盾
   - 劇情承接是否自然
3. 對每個問題標示：
   - 問題位置
   - 問題類型
   - 影響程度
   - 建議修法
4. 若問題來自 bible 不完整，要回退到 `novel-to-bible` 補資料。
5. 若問題來自單章節奏，不一定重寫整章，先局部修補。

## Guardrails

- 不要只抓大 bug；小的人設漂移累積久了也會壞。
- 不要用「讀者可能不會注意」當放過理由。
- 如果需要 retcon，要明確標示是 retcon，不是假裝沒事。

## Output

輸出 continuity report：
- 問題列表
- 嚴重度
- 修補建議
- 是否要回退到 bible 或 arc 層修正
