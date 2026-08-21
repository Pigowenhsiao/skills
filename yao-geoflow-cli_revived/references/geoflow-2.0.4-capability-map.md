<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-cli
Created by: 姚金刚
Date: 2026-06-21
X: https://x.com/yaojingang
-->

# GEOFlow 2.0.4 Capability Map

This reference maps GEOFlow 2.0.4 operations to the supported automation surface. Use it after `SKILL.md` selects this skill and before taking a mutating action.

## Source Of Truth

For the target workspace, inspect current routes instead of relying on stale prose:

```bash
php artisan route:list --path=api/v1
php artisan route:list --path=admin
```

For Docker deployments, run the same commands inside the PHP container, for example:

```bash
docker exec geoflow-app php artisan route:list --path=api/v1
docker exec geoflow-app php artisan route:list --path=admin
```

If a route is missing in the target workspace, report that the capability is unavailable in that deployment.

## Operation Surfaces

- `CLI`: use `bin/geoflow` only when it exists and `--help` confirms the action.
- `API v1`: use bearer auth, `Accept: application/json`, JSON payloads, and `X-Idempotency-Key` for writes.
- `Admin web`: use an authenticated admin session, CSRF token, cookies, and route-specific form semantics. Verify by reading the resulting page, JSON status endpoint, or generated artifact.
- `Super-admin web`: same as admin web, but first verify super-admin access. Many operations also require the current admin password.

Never replace an admin-web capability with direct SQL.

## API v1 Coverage

API v1 covers the scriptable content operations:

- Authentication: `POST /api/v1/auth/login`
- Catalog: `GET /api/v1/catalog`
- Tasks: list, create, show, update, delete, start, stop, enqueue, and task jobs
- Jobs: show one task run via `GET /api/v1/jobs/{id}`
- Materials: summary, typed CRUD, typed item list/create/delete
- Articles: list, create, show, update, review, publish, trash

API v1 does not expose distribution channel CRUD, Analytics, URL Import, System Updates, Theme Replication, API Token admin, admin-user admin, site settings, security settings, or AI model/prompt configuration in the current 2.0.4 public surface.

## Task Contract

Create requires:

- `name`
- `title_library_id`
- `prompt_id`
- `ai_model_id`

Common optional task fields:

- `author_id`
- `image_library_id`
- `image_count`
- `knowledge_base_id`
- `knowledge_base_ids` up to five IDs; when present, it takes precedence over `knowledge_base_id`
- `fixed_category_id`
- `status`: `active` or `paused`
- `category_mode`: `smart` or `fixed`
- `model_selection_mode`: `fixed` or `smart_failover`
- `publish_scope`: `local_and_distribution`, `distribution_only`, or `local_only`
- `distribution_strategy`: `broadcast`, `round_robin`, or `random_balanced`
- `draft_limit`
- `article_limit`
- `publish_interval` in seconds for API v1
- `need_review`
- `is_loop`
- `auto_keywords`
- `auto_description`

Admin task forms also accept `distribution_channel_ids[]`; this is an admin-web-only channel binding flow. API v1 can set `publish_scope` and `distribution_strategy`, but it cannot list, select, or sync `task_distribution_channels` unless the target deployment adds a dedicated API route.

After create/update, inspect `GET /api/v1/tasks/{id}`. Current task responses may include:

- `knowledge_base_ids`
- `knowledge_bases`
- `distribution_strategy`
- `distribution_cursor`
- `image_count`
- `need_review`
- `auto_keywords`
- `auto_description`
- `is_loop`
- `schedule_enabled`
- `task_progress`
- `queue_overview`
- distribution counters: `distribution_total_count`, `distribution_synced_count`, `distribution_failed_count`

## Admin Web Coverage

Use admin web routes for these 2.0.4 capabilities.

### Dashboard And Analytics

- Dashboard: `GET /admin/dashboard`
- Analytics: `GET /admin/analytics`
- Filters include date range, quick range, distribution channel, task, category, article, traffic type, and log source when present.
- Report metrics from the rendered page or backing service data only; do not invent trend values.

### Tasks

- List and monitoring page: `GET /admin/tasks`
- Create/update/delete/toggle: `/admin/tasks/*`
- Health snapshot: `GET /admin/tasks/health-check`
- Batch start/stop: `POST /admin/tasks/batch/start`
- Admin-only extras: channel selection, distribution strategy, local-only channel disabling, multi-knowledge-base UI, task monitoring panels, worker/queue snapshots.

### Distribution

Routes under `/admin/distribution` cover:

- Channel list, create, show, edit, update
- Channel pause and activate
- Health check
- Secret rotation and super-admin password-gated reveal
- Target-site package download
- Remote settings sync
- Distribution jobs list
- Remote distribution job edit/update/delete
- Failed job retry

Channel types:

- `geoflow_agent`
- `wordpress_rest`
- `generic_http_api`

Rules:

- GEOFlow Agent channels can use target package, static/rewrite front mode, secret reveal/rotation, and settings sync.
- WordPress REST channels use WordPress username and Application Password. Do not reveal the password after save. Health failures should mention username, Application Password, HTTPS, and WordPress user capabilities.
- Generic HTTP API channels support configurable auth (`none`, `bearer`, `basic`, `header_key`, `hmac`), request methods/paths, success statuses, response mapping, health checks, and optional settings sync path.
- For `local_only` tasks, ignore stale channel IDs and verify no `task_distribution_channels` binding is created.
- For `distribution_only`, local articles may become `private` while remaining eligible for distribution.

### URL Import

Routes under `/admin/url-import` cover:

- Create import job from URL
- Run queued/failed job
- Poll JSON status
- Show job details and logs
- Commit result into knowledge base, keyword library, and title library outputs
- View history

Before running, verify an analysis model is configured. If missing, direct the operation to AI model setup instead of retrying the job.

### System Updates

Routes under `/admin/system-updates` cover:

- Check latest version metadata
- Create update plan
- Mark manual commands as executed
- Create backups
- Apply queued updates
- Inspect runs and run status
- Mark stale/failed runs
- Retry runs
- Inspect backups
- Roll back all backup files
- Roll back a single file

These are high-risk super-admin operations. Before `apply`, `rollback`, `rollback-file`, `retry`, or `mark-failed`, verify:

- update center is enabled in config
- logged-in user is super admin
- active run state
- backup/run UUID
- current admin password when the form requires it
- preflight and plan state shown by the UI

Never run raw updater commands from memory when the update center has generated a manual-command list. Report the command list and wait for explicit user confirmation before marking a command as executed.

### Site Settings And Theme Replication

Routes under `/admin/site-settings` cover:

- Global site settings
- Theme activation
- Article detail image ads
- Article detail text ads
- Sensitive words
- Theme replication create/show/status/preview/assets/retry/iterate/publish/copy/archive/delete-drafts/package

Theme replication is an admin web workflow. Verify generated preview pages (`home`, `category`, `article`) before publish. If package download is requested, verify the replication ID and do not treat the archive as proof of publication.

### Articles

Admin article routes cover:

- List, create, edit, update
- Batch status update
- Batch review update
- Batch delete, restore, force-delete
- Empty trash
- Per-article restore and force-delete
- Editor image upload
- WeChat HTML export

Prefer API v1 for simple scriptable draft/review/publish/trash. Use admin web for editor uploads, WeChat HTML export, batch actions, restore, force-delete, and trash emptying.

### Materials

Admin web extends material work beyond API v1:

- Category CRUD
- Author CRUD and detail page
- Keyword library CRUD, detail update, keyword add/delete, import
- Title library CRUD, title add/delete, import, AI title generation
- Image library CRUD, image upload/delete, detail update
- Knowledge base CRUD, file upload, chunk refresh, detail update
- Unified materials index

Prefer API v1 for simple typed material CRUD. Use admin web for uploads, imports, AI title generation, chunk refresh, and detail pages.

### AI Configuration

Admin routes cover:

- AI configurator
- AI model CRUD
- Model connection test
- Default embedding model
- Chunking config
- Content prompt CRUD
- Special keyword and description prompts

Verify model status after writes. Never print encrypted API keys or full provider secrets.

### Admin, Security, And Tokens

Admin web covers:

- Login, logout, locale switch, welcome dismiss
- Admin users create/update/toggle/delete, super-admin only
- Admin activity logs, super-admin only
- API token create/revoke, super-admin only
- Security password update
- Sensitive words create/delete

API token creation returns the token once. Redact it in summaries unless the user explicitly asked to receive the token in the current private thread.

## Reporting Standard

For each operation, report:

- surface used: CLI, API v1, admin web, or super-admin web
- route or command
- resource IDs touched
- verification readback
- final state
- redacted secret handling, when relevant

For failed operations, classify the failure as authentication/session, CSRF, permission, route missing, validation, business data, queue/worker, remote target, or system update preflight.
