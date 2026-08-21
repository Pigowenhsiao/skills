---
name: x-twitter-watch
description: Track selected X/Twitter accounts for new status IDs and X Articles, capturing raw metadata for later llm-wiki ingestion.
triggers:
  - "x-twitter-watch"

---

# x-twitter-watch

## Description

Use this skill when Pigo wants to track new X/Twitter posts from a specific account, especially accounts that publish AI workflow, prompt, design, or GPT2 visual-generation content. The skill discovers candidate status IDs, enriches them through public fxtwitter/vxtwitter endpoints, and writes raw watchlist outputs that can later be converted into Vault notes through `llm-wiki summary <url>`.

This skill is intentionally a watchlist and capture workflow, not a full ingestion workflow. It should not automatically create long-form Vault notes for every discovered post. Curated notes should still be created through `llm-wiki` after Pigo or an agent decides the source is worth keeping.

## Current Default Account

- `xiaoxiaodong01`

## Run

From the Agent repo root:

```powershell
& "skills\x-twitter-watch\Invoke-XWatchlist.ps1" -Account "xiaoxiaodong01" -UpdateState -WriteReport
```

If a new X URL is already known, pass the status ID directly:

```powershell
& "skills\x-twitter-watch\Invoke-XWatchlist.ps1" -Account "xiaoxiaodong01" -CandidateStatusIds "2056412276593410537" -UpdateState -WriteReport
```

## Outputs

When run inside a Vault-shaped workspace, the script writes:

- Raw run JSON: `08-Learning/90_Source-Inbox/twitter/raw/`
- Watchlist state/report: `08-Learning/90_Source-Inbox/twitter/watchlists/`

## Limits

- Public discovery sources can lag, miss posts, or return 403/503.
- Use `-CandidateStatusIds` as a manual fallback when Pigo sees a new post before public search indexes it.
- Notion sync is outside this skill; use `llm-wiki` after source selection.
