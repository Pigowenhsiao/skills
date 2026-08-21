---
name: fermi-estimate
description: Solve appropriate tasks using Fermi estimation by defining the target quantity, decomposing it into smaller subproblems, making reasonable assumptions from limited information, combining the assumptions mathematically, validating the order of magnitude, and providing a final estimate range. Use when the user asks for 費米估計, 粗估, 大概有多少, quick sizing, approximate counts, market sizing without full data, or other questions where exact data is unavailable but a defensible estimate is still valuable.
---

# 費米估計

## Objective

透過費米估計的方法論完成使用者交付的估算任務。
如果題型不適合費米估計，直接告知使用者並婉拒回答。

## Applicability Rule

Use this skill only when the task is fundamentally an estimation problem under uncertainty.
Do not force it onto exact factual lookup, legal interpretation, or tasks that already have precise data available.

## Required Workflow

1. 定義問題
   - state the core quantity to estimate
   - specify unit, geography, time period, and currency if relevant
2. 分解問題
   - break the estimate into simpler connected subproblems
3. 假設數據
   - state assumptions using experience, literature, or conservative middle estimates
4. 數據組合
   - combine the assumptions explicitly
   - show formulas where helpful
5. 驗證與調整
   - check whether the order of magnitude is plausible
   - revise assumptions if obviously unreasonable
6. 提供範圍
   - provide a reasonable range, not just one number

## Assumption Rule

For each major assumption, explain:

- what value is assumed
- why that value is reasonable
- whether it is based on experience, external information, or a neutral guess

## Output Style

- Keep the arithmetic visible.
- Separate assumptions from calculations.
- Prefer low/base/high or range-based reporting.
- End with a concise final estimate statement.

## References

- For decomposition patterns and validation checks, read [references/sanity-checks.md](references/sanity-checks.md).
- For a reusable low/base/high multiplication table, use [scripts/three_case_table.py](scripts/three_case_table.py).

## Example Requests

- `用費米估計粗估台北有多少家獨立咖啡店`
- `估一下台灣每年可能購買 AI 法務工具的中型企業數量`
- `幫我做一版市場規模粗估，不需要精確，只要合理`
