---
name: yao-geoflow-design
description: Discover, preview, clone, and edit GEOFlow Laravel Blade themes, including rich homepage composition and GEOFlow homepage module/style JSON for corporate, portal, and content-site front pages, by selecting an existing template or mapping a reference site, then applying safe frontend changes without changing business logic or data contracts. Use for theme discovery, target-theme editing, homepage enrichment, homepage module builder design, cloning, optimization, and theme iteration. Not for raw HTML copying, backend refactors, or direct live activation.
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-design
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEOFlow Design

Use this skill to discover, preview, clone, or improve a GEOFlow frontend without breaking its Laravel Blade rendering contract.

## What This Skill Owns

- GEOFlow theme discovery and target selection
- preview-first theme edit sessions for existing templates
- reference-site cloning into GEOFlow-compatible modules
- current-template optimization and incremental design adjustment
- rich homepage composition using existing GEOFlow data such as hero/carousel slides, featured articles, hot articles, latest articles, site copy, and current theme assets
- homepage module builder design payloads using `homepage_modules`, `homepage_style`, presets, and import-safe JSON when the current GEOFlow workspace exposes that contract
- confirmation flow for replace-base vs publish-as-new decisions

## What This Skill Does Not Cover

- direct deployment of a new frontend into production
- unreviewed homepage builder imports, homepage presets, or live homepage settings changes
- arbitrary page scraping and raw HTML copying
- changing GEOFlow data queries, routing, or SEO contracts

## Required Preconditions

1. Confirm the target workspace is a GEOFlow Laravel codebase with `artisan`, `routes/web.php`, `resources/views/site`, and `resources/views/theme`.
2. Read [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md), [references/template-boundary.md](references/template-boundary.md), and [references/homepage-composition-guide.md](references/homepage-composition-guide.md) before proposing homepage changes.
3. Discover available themes in `resources/views/theme` before editing. Default to the user-selected theme, otherwise use the active theme if known.
4. Preserve the existing module/data contract unless the user explicitly asks for a system change.
5. Never hard-code the admin base path. Current GEOFlow can customize the admin URL path; frontend themes should use public routes and route helpers only.
6. Choose a work mode:
   - `edit_theme`: adjust a specified existing theme
   - `clone`: map a reference site into a new GEOFlow theme
   - `hybrid`: use a reference site to guide edits on a specified existing theme
7. When the homepage is in scope, choose a homepage strategy:
   - `editorial_home`: lead story, featured/hot/latest, topic rails
   - `corporate_portal`: hero, value statements, metrics/chart blocks, services/categories, cases/resources, CTA
   - `knowledge_hub`: text modules, taxonomy entrances, reading paths, latest resources
8. When `HomepageModuleBuilder` and the admin `homepage-modules/import` route exist, prefer a reviewed `homepage-design.json` payload for module/style configuration before editing Blade markup for the same need.
9. Treat preview, import, activation, and replacement as separate steps. Never edit the live target first when a preview fork or reviewed import payload can be created.

## Default Workflow

1. Identify the GEOFlow workspace and confirm the canonical frontend and theme-system files.
2. Run `scripts/discover_themes.py` to list existing themes, preview routes, editable files, public assets, theme-editor support, homepage data signals, and homepage module builder support.
3. Resolve a `target_theme_id` or decide to create a brand-new theme from a reference site.
4. For `edit_theme` or `hybrid`, create a preview fork with `scripts/prepare_theme_edit_session.py` instead of editing the target live.
5. For `clone` or `hybrid`, inspect the reference URL for tokens, layout rhythm, and homepage section grammar. For `edit_theme` or `hybrid`, audit the target theme for hierarchy, spacing, density, responsiveness, module consistency, and homepage fullness.
6. For homepage enrichment, create a section plan before editing: hero/media, metrics or chart-lite blocks, text/value blocks, category/service entries, featured/hot/latest article treatments, visual CTA bands, and empty-state behavior. Use only current GEOFlow variables, current homepage builder fields, or static theme copy that remains editable in the theme.
7. If the homepage builder is available, output `homepage-design.json` with explicit `style` and `modules` fields, import mode guidance (`replace` or `append`), and a preview/review note before any admin import.
8. Edit only the allowed theme files and design artifacts: `*.blade.php`, `partials/*.blade.php`, `assets/theme.css`, public theme assets when present, `manifest.json`, optional `tokens.json` / `mapping.json`, and reviewed homepage design JSON.
9. Preserve SEO/meta/schema output, markdown-rendered article HTML, image rendering rules, footer copyright, and public language behavior unless the user explicitly asks to change them.
10. Keep the work in preview status until the operator reviews the generated preview URLs or homepage design JSON.
11. After confirmation, choose one finalize path:
   - `publish_as_new_theme`: keep or rename the preview fork so it becomes a selectable admin theme
   - `replace_base_theme`: back up the target theme, then replace it from the confirmed preview fork
   - `activate_after_confirmation`: perform activation only after preview approval
   - `import_homepage_design_after_confirmation`: submit or hand off the reviewed homepage JSON only after the operator accepts the exact payload
12. Call out safe restyle surface, fixed contracts, and live-risk warnings before any finalize step.

## Reference Map

- [references/geoflow-frontend-map.md](references/geoflow-frontend-map.md): authoritative frontend module and variable map
- [references/laravel-theme-contract.md](references/laravel-theme-contract.md): current Laravel Blade theme contract
- [references/template-boundary.md](references/template-boundary.md): safe and unsafe modification boundaries
- [references/homepage-composition-guide.md](references/homepage-composition-guide.md): rich homepage module patterns for corporate, portal, and content-site themes
- [references/theme-package-contract.md](references/theme-package-contract.md): expected output shape for theme edit sessions and clone flows
- [references/design-optimization-playbook.md](references/design-optimization-playbook.md): optimization heuristics and preferred outputs
- [references/theme-edit-workflow.md](references/theme-edit-workflow.md): end-to-end workflow for discover -> preview -> adjust -> finalize
