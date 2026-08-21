<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-design
Created by: 姚金刚
Date: 2026-06-23
X: https://x.com/yaojingang
-->

# GEOFlow Homepage Builder Self-Check

## Verdict

`yao-geoflow-design` needed another upgrade. The previous `0.4.0` iteration knew about richer homepage composition from current view variables, but it still treated admin-editable homepage modules as a system-change boundary. Current GEOFlow now exposes a real homepage module and style contract, so the skill must prefer that contract when available.

## Evidence From Current GEOFlow

- `app/Support/Site/HomepageModuleBuilder.php` defines module types, style tokens, presets, import alias normalization, URL/color validation, and sanitized `custom_html`.
- `app/Http/Controllers/Site/HomeController.php` passes `homepageModules`, `homepageStyle`, and `showHomepageModules` into the home view.
- `resources/views/site/home.blade.php` includes `resources/views/site/partials/homepage-modules.blade.php`.
- `resources/views/site/partials/homepage-modules.blade.php` renders `hero`, `rich_text`, `image_band`, `metric_band`, `chart_band`, `feature_grid`, `article_collection`, `cta_band`, and `custom_html`.
- `routes/web.php` exposes admin routes for save, preset, and import under the configurable admin prefix.
- `app/Http/Controllers/Admin/SiteSettingsController.php` persists `homepage_modules` and `homepage_style`, applies presets, and imports design JSON with `replace` or `append` behavior.

## Skill Changes Required

- Detect `HomepageModuleBuilder` and homepage import support during theme discovery.
- Add homepage builder JSON as a first-class output: `homepage-design.json`.
- Update boundaries so admin-editable homepage modules are allowed when the current system already exposes the builder.
- Keep the review gate: do not apply import or preset routes until the operator confirms the exact payload and mode.
- Preserve existing safety rules around route contracts, SEO/schema, search/category states, fake claims, forms, logos, and backend-only data.

## Remaining Boundary

The new builder supports configurable content modules and style tokens. It still does not make customer logos, lead forms, pricing, testimonials, products, or analytics real unless the system has data for them or the user explicitly expands scope to backend work.
