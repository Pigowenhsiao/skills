---
name: tw-stock-growth-investing
description: Analyze Taiwan and US stocks by first extracting a stock-picking framework from a user-provided note, transcript, or checklist, or by using a default moat/cash-flow/management/growth/valuation framework, then validating candidates with current official market, filing, and company-investor-relations data. Use when the user asks which Taiwan or US companies are suitable for investment, wants a stock shortlist based on a document's investing method, asks for 股票分析, 個股分析, 台股分析, 基本面分析, 財報分析, or 價值投資分析, or wants current evidence-backed stock research rather than generic opinions.
---

# Tw Stock Growth Investing

## Description

The `tw-stock-growth-investing` skill is for analyzing Taiwan and US stocks by first extracting a stock-picking framework from a user-provided note, transcript, or checklist, or by using a default moat/cash-flow/management/growth/valuation framework, then validating candidates with current official market, filing, and company-investor-relations data.

Analyze Taiwan and US stocks by first extracting a stock-picking framework from a user-provided note, transcript, or checklist, or by using a default moat/cash-flow/management/growth/valuation framework, then validating candidates with current official market, filing, and company-investor-relations data. Use it when the user asks which Taiwan or US companies are suitable for investment, wants a stock shortlist based on a document's investing method, asks for 股票分析, 個股分析, 台股分析, 基本面分析, 財報分析, or 價值投資分析, or wants current evidence-backed stock research rather than generic opinions.

## Overview

Use this skill when the task is about Taiwan or US equities and the goal is to turn a qualitative investing framework into a current, source-backed shortlist. Default to official exchange, filing, and investor-relations data, and state clearly when a judgment is an inference rather than a reported fact.

## Workflow

### 1. Extract the framework

- If the user provides a document, read it first and extract repeated principles instead of quoting long passages.
- Convert the document into 4-6 screenable rules.
- Good default rules:
  - prefer leaders or niche leaders
  - prefer strong moat
  - prefer at least one stable cash-flow-generating business
  - check management quality and shareholder alignment
  - compare EPS growth with PE
  - for heavy-asset businesses, inspect cash flow and debt before trusting PE
- If a local document is part of the method, cite the file path in the answer.

### 2. Build a current dataset

- Use current official data. Prefer the endpoints listed in [references/tw-stock-sources.md](references/tw-stock-sources.md) for Taiwan stocks and [references/us-stock-sources.md](references/us-stock-sources.md) for US stocks.
- Minimum fields:
  - code
  - name
  - market
  - industry
  - latest monthly revenue YoY
  - latest annual or trailing EPS
  - PE
  - PB
  - yield
- Always state the exact dates or periods used, such as valuation date, revenue month, and report period.

### 2A. Taiwan stock data rules

- Prioritize TWSE, TPEx, and MOPS.
- Monthly revenue is a core signal for Taiwan names and should be included whenever available.
- For Taiwan hardware names, do not confuse one strong revenue month with a durable moat. Use the second-pass moat test.

### 2B. US stock data rules

- Prioritize SEC filings, official investor-relations releases, and primary market data sources.
- Core fields for US names:
  - revenue growth
  - EPS growth
  - gross margin or operating margin trend
  - free cash flow trend
  - net debt or cash position
  - valuation such as PE, forward PE, EV/FCF, or EV/EBIT when relevant
- For US platform or software companies, emphasize recurring revenue, switching costs, pricing power, and operating leverage.
- For US heavy-asset businesses, emphasize cash flow conversion, capex burden, and balance-sheet strength.

### 3. Screen for growth worth researching

- Start from growth, not deep value.
- A practical default screen:
  - exclude obvious cyclical industries unless the user explicitly wants them
  - latest monthly revenue YoY >= 10%
  - EPS > 0
  - ROE or proxy ROE >= 12% when available
  - PE should be explainable by growth; do not reject solely because PE > 20
- For US names without monthly revenue:
  - recent quarterly revenue growth should usually be positive
  - EPS or operating profit trend should be improving
  - free cash flow should be positive or clearly approaching positive with a defensible reason
- Then do a manual second pass:
  - keep leaders or niche leaders
  - keep businesses with at least one stable cash-flow base
  - remove names where the recent spike is mostly cycle-driven or investment-value noise

### 4. Rank and explain

- Prefer 5-10 names, not large dumps.
- Separate the output into:
  - first-priority research names
  - good companies but valuation-rich names
  - names with strong numbers that still fail the moat or cash-flow test
- For each kept name, explain in 1-2 sentences:
  - why it fits the framework
  - why it is not an obvious trap
  - what the main risk is

### 5. Output format

- Use Traditional Chinese unless the user requests another language.
- For non-trivial answers, use this structure:
  - Core summary
  - Detailed analysis
  - Key data
  - Risks and limits
- Put the shortlist first and keep the source list compact at the end.

## Judgment Rules

- Treat "適合投資" as suitable for further research or staged accumulation, not an automatic buy-now instruction.
- Treat management quality as partially unobservable from screen data. If not verified through annual reports, conference calls, or insider ownership, say that second-round diligence is still required.
- If a company is world-class but clearly expensive, say so directly. Do not force it into a cheap-growth bucket.
- If a company passes the numbers but depends heavily on memory, shipping, steel, or other cycle-heavy drivers, flag that clearly.
- If two data sources conflict materially, stop the inference and show both numbers.
- For US names, prefer 10-K, 10-Q, earnings release, shareholder letter, and IR presentation over third-party summaries whenever practical.

## Read Reference Files When Needed

- Read [references/tw-stock-sources.md](references/tw-stock-sources.md) for official data sources, practical metrics, and common red flags.
- Read [references/us-stock-sources.md](references/us-stock-sources.md) for US filing sources, practical metrics, and common red flags.

## Trigger Examples

- "股票分析"
- "個股分析"
- "台股分析"
- "基本面分析"
- "財報分析"
- "價值投資分析"
- "參考這份投資筆記，找出台股成長股"
- "參考這份筆記，幫我做美股分析"
- "用護城河和現金流的方式分析哪些台股適合投資"
- "先不要看便宜股，找成長中且值得研究的公司"
