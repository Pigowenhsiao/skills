# Output Patterns

## Mandatory section intent

### 關鍵概念定義

Use this section to normalize meaning before analysis.
Include:

- term definition
- abbreviation expansion
- unit and currency normalization
- scope boundaries
- competing definitions if they materially change the answer

### 收集背景知識

This is the largest section.
Use it to gather everything that later execution may need.
When relevant, include:

- actor map
- chronology
- institutional background
- domain mechanics
- formulas
- legal structure
- datasets and studies
- fact versus stereotype distinction
- assumptions requiring validation

### 重大影響的具體事件

Prefer dated events such as:

- law passed or amended
- regulator guidance changed
- large funding or bankruptcy event
- geopolitical disruption
- public health shock
- major model, product, or standards release

### 輔助視覺化

Add Mermaid only if the topic includes process, interaction, timeline, or positioning.

## Mermaid selection rule

- `flowchart`: rules, process, decision path, pipeline
- `sequenceDiagram`: actor interaction, request-response, negotiation, handoff
- `gantt`: real dated chronology, project timeline, policy evolution
- `quadrantChart`: market map, positioning, tradeoff map

## Annotation rule

For important claims, prefer short inline annotations such as:

- source organization
- publication or page title
- publication date
- link if available in the surrounding environment

## Completeness heuristic

If a later writer would likely ask “what are we missing before we can safely execute?”, the answer belongs in concept alignment.
