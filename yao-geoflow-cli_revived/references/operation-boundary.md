<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geoflow-cli
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Operation Boundary

This skill is for operating a running GEOFlow system, not for developing the system itself. GEOFlow 2.0.4 has two operation surfaces: API v1 for scriptable content operations and the Blade admin for newer management workflows.

## Allowed Actions

- Run `bin/geoflow` commands when the CLI exists
- Use Laravel `/api/v1` fallback when the current GEOFlow rewrite has no CLI wrapper
- Use authenticated admin web routes for capabilities not exposed through CLI or API v1
- Read command output
- Build JSON payload files when needed for task, material, or article operations
- Inspect resulting material, task, job, and article state through the CLI or API v1
- Submit admin forms with the current CSRF token and session cookies
- Download generated packages only when the user explicitly requests the target resource

## Disallowed Actions

- Direct SQL against the project database
- Editing backend PHP just to complete an operations request
- Replacing the CLI with raw `curl` when the CLI exists and already supports the action
- Exposing a full bearer token in user-facing summaries
- Claiming admin-only Distribution Management, Analytics, URL import, system updates, theme replication, API tokens, admin users, site settings, or async title generation flows are available through API v1 unless the target workspace exposes matching routes
- Bypassing admin authentication, CSRF validation, super-admin checks, current-password checks, or configured update-center gates
- Printing distribution secrets, WordPress Application Passwords, generic API secrets, full API tokens, or downloaded package secret contents in final summaries

## Required Checks

Before the first mutating command in a workspace:

1. Verify whether `bin/geoflow` exists. If it does not, verify the workspace is a Laravel GEOFlow app with `artisan` and `routes/api.php`.
2. If CLI configuration is missing, run `geoflow login` first. If using API fallback, obtain a bearer token through `/api/v1/auth/login` or the provided token source.
3. If configuration exists but authenticated reads return `401`, `403`, or token-invalid output, refresh login/token.
4. If authenticated reads fail for another reason, report that failure instead of assuming login is the fix.
5. Verify the CLI resolves configuration, or verify the API base URL responds.
6. Verify an authenticated read such as `catalog` succeeds. `config show` or a public homepage check by itself is not sufficient.
7. For material operations, verify `materials:read` and `materials:write` through `GET /api/v1/materials` before writing.
8. For admin web operations, verify the admin login page, authenticate to an admin session, and read the target form/page before posting.
9. For super-admin operations, verify super-admin-only routes are accessible before attempting writes.
10. For high-risk actions, ensure the user has explicitly identified the action and target resource.

After any mutating command:

1. Re-read the target resource.
2. Report the final persisted state.
3. If the action triggered a background job, inspect the job separately.
4. If the action published an article locally, verify the final frontend URL and report the `/article/{slug}` route rather than an `article.php?id=...` compatibility link.
5. For generated articles, the final article slug should be an 8-character short ASCII token such as `bc7af3fb`. User-supplied slugs may differ; report the persisted value.
6. If the action used admin web, verify by reading the redirected page, JSON status endpoint, listing page, detail page, or artifact metadata.
7. If the action touched a remote channel, separate local GEOFlow success from remote target success.

## High-Risk Admin Web Actions

Proceed only when the user's request explicitly names the target action/resource:

- force-delete articles or empty trash
- delete admin users, revoke API tokens, or change passwords
- reveal or rotate distribution secrets
- download target-site packages containing generated credentials
- apply, retry, mark failed, or roll back system updates
- publish theme replication output
- delete generated theme replication drafts

For these operations, report the route, target ID, verification result, and any remaining manual step. Redact secrets.

## Error Interpretation

Keep these failure classes separate:

- CLI/runtime failure: command missing, config missing, permission problem, malformed args
- API fallback setup failure: missing `GEOFLOW_BASE_URL`, missing bearer token, wrong `/api/v1` base path
- API fallback routing failure: `/api/v1/catalog` returns HTML, proxy errors, login pages, or Laravel web pages instead of JSON
- API failure: 401, 403, 404, 409, 422, 500
- Admin web failure: missing login session, CSRF mismatch, validation redirect, super-admin denial, password-confirmation failure
- Business-data failure: task inactive, missing titles, invalid category, review state conflict
- Remote target failure: WordPress authorization/capability error, generic API mapping failure, GEOFlow Agent health/sync failure
- System-update failure: preflight failure, missing backup, active run conflict, stale run, manual command not executed, disabled update/rollback config
- Route-surface mismatch: requested capability exists in admin web but not API v1, or is absent from the target deployment

Do not conflate a downstream job-data failure with a CLI failure.
If a task is blocked by business data and the user only needs a publish smoke test, stop the task before switching to a direct article-create fallback.
