<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-cli
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEOFlow Operations

`yao-geoflow-cli` is a local operations skill for controlling an existing GEOFlow 2.0.x system through the project CLI, Laravel API v1 fallback, or authenticated admin web flows when newer capabilities are only exposed in the Blade admin.

Public project repository:

- [GEOFlow](https://github.com/yaojingang/GEOFlow)

## Primary Use

- first-time login with GEOFlow admin credentials
- inspect catalog and material IDs
- create, update, delete, and inspect material libraries and supported material items
- create, start, stop, enqueue, monitor, and batch operate tasks
- configure task publish scope, distribution strategy, image count, multi-knowledge-base, review, loop, and auto metadata settings
- delete tasks through API v1 when supported
- inspect jobs
- upload article drafts
- review and publish articles
- run article batch actions, editor image upload, restore, force-delete, trash emptying, and WeChat HTML export through admin web
- configure Distribution Management for GEOFlow Agent, WordPress REST, and generic HTTP API channels through admin web
- inspect Analytics, run URL Import, manage System Updates, operate Site Settings and Theme Replication
- manage AI models/prompts, security settings, API tokens, admin users, and activity logs when permissions allow
- run Laravel `/api/v1` fallback preflight when the CLI wrapper is absent
- run admin login-page preflight when operating admin-only flows
- diagnose Docker/base-URL problems when API fallback returns HTML instead of JSON

## Boundary

This skill does not implement GEOFlow backend code and does not write directly to the database. It prefers `bin/geoflow` only when present and when `--help` confirms the requested action. If the current Laravel rewrite has no CLI wrapper, it operates through `/api/v1` with bearer auth and idempotency keys. First-time access should use `geoflow login` when the CLI exists, or `/api/v1/auth/login` when using API fallback.

GEOFlow 2.0.4 Distribution Management, target-site package download, Analytics, URL Import, System Updates, Theme Replication, AI configuration, site settings, API tokens, and admin-user management are admin web flows unless the target workspace exposes a matching API route. This skill may operate those flows through an authenticated admin session, but it must not claim they are API v1 endpoints.

High-risk actions such as force-delete, empty trash, secret reveal/rotation, package download, API token revoke, admin-user deletion, password update, system update apply/retry/rollback, and theme publish require explicit target confirmation and post-action verification. Secrets are redacted in summaries.

## Package Map

- `SKILL.md`: trigger boundary and operating workflow
- `agents/interface.yaml`: canonical interface metadata
- `agents/openai.yaml`: OpenAI-friendly interface metadata
- `references/operation-boundary.md`: safety and scope rules
- `references/command-map.md`: capability-to-command mapping
- `references/laravel-api-v1-docker.md`: Laravel API v1 fallback, Docker checks, scopes, and non-JSON diagnostics
- `references/geoflow-2.0.4-capability-map.md`: API/admin coverage map for all current GEOFlow 2.0.4 capabilities
- `scripts/geoflow_preflight.sh`: deterministic CLI/config or API fallback preflight
- `evals/trigger_cases.json`: trigger boundary checks
