---
name: yao-chatgpt-crawler
description: "Use when a user provides ChatGPT web AI-search keywords, repeat count, target entity, entity type, OpenCLI profile, and crawl interval preference, then needs repeated crawls aggregated into JSON plus a Kami HTML GEO report. Not for generic crawling, ChatGPT API chat, SEO writing, or one-off answers."
---

# Yao ChatGPT Crawler

## Inputs

Keywords/questions, repeat count, target entity, entity type (`person/company/product`), browser profile, single-query interval preset, and optional output directory. Competitors must match the target type.

Default interval is a random `30s-1m` between fresh samples. For lower request frequency, use `1-3m` or `3-10m`; `--safe-random-delay` maps to `3-10m`. Slower intervals reduce account-risk pressure but do not guarantee that ChatGPT will not throttle or challenge the session.

## Workflow

1. Read `references/user-setup-and-usage.md`, `references/chatgpt-crawl-workflow.md`, and `references/report-contract.md` as needed.
2. Run `node scripts/preflight.mjs --profile <profile>` before fresh crawling.
3. Stage 1: run `scripts/chatgpt_batch_crawl.mjs` with questions, repeat, profile, target entity/type, interval preset, and output dir.
4. Stage 2: run `scripts/analyze_chatgpt_results.py` with target entity/type, optional brands file, optional semantic review, and report output dir.
5. Return crawl JSON, summary, structured Markdown/Excel, HTML report, optional semantic-review cache, and failed logs.

## Honest Boundaries

- Reuses local ChatGPT web automation; does not bypass login, bot checks, or hidden data.
- ChatGPT references come from visible citation pills, the ChatGPT source flyout, markdown links, and bare URLs; missing visible links limit source analysis.
- Probability metrics are repeated-sample estimates, not ground truth.
- Inferred competitors are heuristic; review aliases before external use. Formal reports can require `--semantic-review required`.
- Preserve raw answers, reference titles, URLs, and logs so every conclusion can be audited.
