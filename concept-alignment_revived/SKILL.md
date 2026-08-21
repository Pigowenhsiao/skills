---
name: concept-alignment
description: Perform concept alignment before executing a task by collecting as much downstream-relevant information as possible, using first-principles analysis, recent web research, sourced notes, concept definitions, background knowledge, major recent events, and Mermaid visualizations. Use when the user asks for 概念對齊, 釐清概念, 先做背景研究, 先整理筆記, 先不要直接做, or when a task is ambiguous, research-heavy, current-events-sensitive, legally or medically sensitive, or likely to benefit from a detailed pre-execution brief.
---

# Concept Alignment

## Core Mission

Collect as much information as possible that may become useful in later execution of the user's task.
Do not jump straight to solving the final task unless the user explicitly asks for that after the alignment notes are complete.

## Required Startup Behavior

1. If canvas is available and not yet started, start canvas and use it for drafting and editing notes.
2. Print `## Concept Alignment`.
3. Analyze the user's task using first-principles thinking.
4. Infer the deeper motivation, intended decision, or real-world objective behind the task.
5. Immediately research the topic, especially when definitions, current events, laws, data, pricing, company facts, technical specs, or public figures are involved.

## Required Output Sections

Present the notes under these exact third-level headings:

- `### 關鍵概念定義`
- `### 收集背景知識`
- `### 重大影響的具體事件`
- `### 輔助視覺化`

Add `### 待確認事項` only when unresolved ambiguity could materially change later execution.

## Section Rules

### 關鍵概念定義

- Define key concepts, domain terms, and proper nouns from the user's task.
- If the task involves numbers, specify the unit.
- If money is involved, specify the currency.
- If a term is ambiguous, overloaded, or disputed, explain the competing definitions.

### 收集背景知識

Collect diverse, execution-relevant background knowledge with source annotations.
Include, when relevant:

- clarifying questions for ambiguous definitions
- event chronology and the people, places, organizations, and objects involved
- key knowledge points and sub-concepts with explanation
- technical terms with explanation
- facts versus bias, stereotype, or conventional wisdom
- formulas in LaTeX
- laws, regulations, and specific clauses with sources
- historical events with timeline context
- data, datasets, statistics, and studies

### 重大影響的具體事件

- Focus on recent concrete events that materially change the topic.
- Prefer specific laws, regulatory changes, macro shocks, geopolitical events, scientific breakthroughs, or technology shifts over vague trend language.
- Use dates.

### 輔助視覺化

- Add Mermaid only when it genuinely compresses understanding.
- Use:
  - flowchart for process
  - sequence diagram for interaction
  - gantt for real timeline
  - quadrant chart for market positioning

## Research Standard

- Always use first-principles reasoning.
- Prefer primary or official sources for laws, standards, specs, and research.
- Treat recent or unstable facts as mandatory-to-verify.
- Annotate sources for all high-stakes or time-sensitive claims.
- Mark inference as inference instead of presenting it as settled fact.
- Keep the content detailed, concrete, and truthful.

## Clarification Rule

If the user's request is too vague to research responsibly, ask targeted clarifying questions.
Otherwise proceed with explicit assumptions and label them.

## Output Style

- Write in Traditional Chinese unless the user clearly prefers another language.
- Use detailed notes, not shallow bullet dumps.
- Keep the structure readable, but prioritize completeness where it changes downstream success.

## References

- For detailed section guidance and Mermaid selection, read [references/output-patterns.md](references/output-patterns.md).

## Example Requests

- `先做概念對齊，再來幫我寫提案：智慧醫療資料治理平台`
- `不要直接回答，先整理台灣長照、照護保險、外籍看護政策的背景知識`
- `先釐清生成式 AI 採購評估會用到的關鍵概念、風險、法規與近期事件`
