<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-design
Created by: 姚金刚
Date: 2026-06-23
X: https://x.com/yaojingang
-->

# GEOFlow Upgrade Self-Check

Date: 2026-06-23

## Verdict

`yao-geoflow-design` needs an upgrade. The previous skill contract was still centered on hero, featured articles, latest articles, article cards, and pagination. Current GEOFlow has enough homepage and theme-editing surface to support richer homepage composition without backend changes.

## Evidence

- Current GEOFlow workspace: `/Users/laoyao/AI Coding/01-Projects/OpenSource/GEOFlow`
- `app/Http/Controllers/Site/HomeController.php` now passes `hotArticles` and `homepageCarouselSlides` in addition to `featuredArticles`, `articles`, `cardSummaries`, site copy, SEO fields, and pagination.
- `app/Http/Controllers/Admin/SiteThemeEditorController.php` and `app/Services/Admin/SiteThemeEditorService.php` provide theme page editing, draft saving, preview rendering, backup, and publish flow for `home`, `category`, and `article`.
- Current runtime themes use `public/themes/{theme_id}/theme.css` and optional `theme.js`, while the skill contract still overemphasized only `resources/views/theme/{theme_id}/assets/theme.css`.
- Existing generated themes already use hot-article rails and lead-story home layouts, which means richer homepage composition is consistent with current frontend practice.

## Gap

The skill could previously say "add a display module only when it can be built from existing GEOFlow data," but it did not define:

- which homepage variables are now safe
- how to compose enterprise/corporate homepage sections from existing data
- how to handle charts, metrics, text modules, large images, CTA bands, and article-derived case/resource modules
- how to keep search/category states clean while making the default homepage fuller
- how to package and evaluate homepage-enrichment outputs

## Upgrade Direction

Upgrade the skill to add a `homepage_enrichment` capability that:

- detects `hotArticles`, `homepageCarouselSlides`, public theme assets, and theme-editor support
- adds a homepage composition guide for corporate portal, content hub, and knowledge hub patterns
- updates the safe boundary so rich modules are allowed when they derive from current variables or clearly labeled static theme copy
- updates package outputs with `homepage-composition-plan.md`, module mapping, data-source notes, and fallback behavior
- updates trigger/eval artifacts so route quality includes richer homepage optimization requests
