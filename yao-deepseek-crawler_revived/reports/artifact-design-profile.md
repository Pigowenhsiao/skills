# Artifact Design Profile

Skill: `yao-deepseek-crawler`
Design system: `metric editorial`

## Primary Artifact Direction

**Code, CLI, or implementation guide**

Execution-focused technical artifact with environment assumptions, copyable commands, expected outputs, and side effects made explicit.

## Matched Artifact Families

### Code, CLI, or implementation guide
- Matched keywords: code, cli, script, api, command
- Score: `5`
- Direction: Execution-focused technical artifact with environment assumptions, copyable commands, expected outputs, and side effects made explicit.

### Dashboard or metrics page
- Matched keywords: dashboard, metric, chart, table
- Score: `4`
- Direction: Metric-first dashboard with stable dimensions, short labels, visible deltas, and narrative callouts only where they change interpretation.

### Report or brief
- Matched keywords: report, analysis, summary
- Score: `3`
- Direction: High-trust editorial report with a clear first-screen thesis, compact evidence blocks, and decisions separated from supporting detail.

### Tutorial or guide
- Matched keywords: tutorial
- Score: `1`
- Direction: Progressive instructional layout with domain-specific section names, short success checks, and examples close to the user's real input.

### Review viewer
- Matched keywords: review
- Score: `1`
- Direction: Side-by-side reviewer studio with explicit tradeoffs, evidence readiness, and fast paths for approving, blocking, or requesting one focused fix.

## Layout Patterns To Prefer

- prerequisites
- commands
- expected output
- failure handling
- rollback or cleanup
- metric board
- ranked signals
- comparison rows

## Design Tokens

### Type
- Use a distinctive display face or serif for major claims when the artifact is editorial.
- Use a restrained sans for dense body text and technical details.
- Use mono only for metadata, paths, commands, labels, and evidence tags.

### Color
- Choose colors from the artifact's domain, brand, or evidence mood.
- Do not default to Kami parchment, purple gradients, or generic SaaS blue unless the content justifies it.
- Keep accent color limited to decisions, active states, risk, or section anchors.

### Spacing
- Prefer clear grid rhythm over floating decorative cards.
- Increase whitespace around decisions and shrink whitespace around supporting metadata.
- Split dense content instead of shrinking type or adding scroll traps.

### Components
- Use cards for grouped evidence, tables for comparisons, callouts for decisions, and timelines for sequence.
- Avoid cards inside cards.
- Keep reviewer-only detail visible but visually quieter than user-facing guidance.

## Quality Gates

- Name the working directory and required inputs for commands.
- Mark destructive, networked, or external side-effect operations.
- Prefer the smallest runnable snippet over broad framework scaffolding.
- Avoid paragraph-heavy table cells.
- Keep charts tied to one analytical question each.
- Preserve stable color meaning across metrics and entities.
- Keep the first screen useful without requiring the reader to parse every detail.
- Use tables only for comparisons; move explanations below the table.

## Anti-Patterns

- Do not copy Kami's fixed parchment background as a default.
- Do not use generic purple gradients, glass cards, or stock SaaS hero sections unless the content calls for them.
- Do not let Markdown tables become the default shape for every comparison or explanation.
- Do not turn reviewer evidence into user-facing clutter.
- Do not invent screenshots, citations, charts, or UI states.

## Reviewer Note

Use this profile to judge whether the generated artifacts feel designed for their job, not merely rendered.
