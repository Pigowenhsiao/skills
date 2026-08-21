<!-- BEGIN AGENT_DIRECTORY_README -->
# Directory: skills\ppt-master\templates\charts

## Purpose
Skill collection area. Directories here usually group SKILL.md workflows, references, scripts, and assets that AI agents can load selectively.

## Provenance
- provided_by_agent: Codex
- provided_by_computer: Pigo Windows workstation
- processing_skill: directory-readme-generation
- processed_at: 2026-05-19T21:19:16+09:00

## AI Reading Guide
- Start with the files or child folders listed in Primary read targets.
- Prefer nearby AGENTS.md, SKILL.md, README.md, and Readme.md files when present.
- Treat archived or vendored content as reference material unless a task explicitly targets it.

## Primary Read Targets
- `Readme.md`
- `README.md`
- `CHART_STYLE_GUIDE.md`
- `charts_index.json`

## Immediate Child Directories
- None detected.

## Immediate Files
- `agenda_list.svg`
- `ansoff_matrix.svg`
- `area_chart.svg`
- `bar_chart.svg`
- `basic_table.svg`
- `bcg_matrix.svg`
- `box_plot_chart.svg`
- `bubble_chart.svg`
- `bullet_chart.svg`
- `butterfly_chart.svg`
- `CHART_STYLE_GUIDE.md`
- `charts_index.json`
- `chevron_process.svg`
- `client_server_flow.svg`
- `comparison_columns.svg`
- `comparison_table.svg`
- `concentric_circles.svg`
- `consulting_table.svg`
- `cycle_diagram.svg`
- `donut_chart.svg`
- `dual_axis_line_chart.svg`
- `dumbbell_chart.svg`
- `feature_matrix_table.svg`
- `financial_statement_table.svg`
- `fishbone_diagram.svg`
- `flywheel_diagram.svg`
- `funnel_chart.svg`
- `gantt_chart.svg`
- `gauge_chart.svg`
- `grouped_bar_chart.svg`

## Parent
- $parent
<!-- END AGENT_DIRECTORY_README -->

---

# SVG Visualization Template Library

This directory contains the standardized SVG visualization templates used by PPT Master â€” charts, infographics, process diagrams, relationship diagrams, and strategic frameworks. The directory name `charts/` is kept for backward compatibility; the library scope is broader than charts.

## Source of truth

[`charts_index.json`](./charts_index.json) is the single source of truth for the library: total count, categories, per-template purpose / use cases / size hints, and quick-lookup keywords. Both human readers and AI roles should consume it directly.

To browse the library, open `charts_index.json` â€” its `categories` block groups every template, and `quickLookup` maps common intents (ranking, comparison, trend, composition, etc.) to recommended templates.

## Style rules

See [`CHART_STYLE_GUIDE.md`](./CHART_STYLE_GUIDE.md) for color palette, typography, and SVG authoring conventions all templates must follow.

## Usage

Before generating a chart page, open the corresponding `<key>.svg` file to read its structure and layout. Files are named after the `key` field in `charts_index.json` (e.g. `bar_chart.svg`, `bcg_matrix.svg`).

