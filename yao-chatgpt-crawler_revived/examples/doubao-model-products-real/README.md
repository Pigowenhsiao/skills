<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-chatgpt-crawler
Created by: 姚金刚
Date: 2026-06-25
X: https://x.com/yaojingang
-->

# Doubao Model Product Real ChatGPT Test

This is a sanitized public example from a real ChatGPT Web Search run.

## Inputs

- Target entity: `豆包`
- Target aliases: `Doubao`, `豆包大模型`, `豆包模型`
- Entity type: model product
- Questions: 5
- Repeat count: 3
- Planned samples: 15
- Completed valid samples: 15
- Source mode: ChatGPT Web Search with visible source extraction
- Semantic review mode: `auto`, local heuristic fallback

Files:

- `questions.txt`: the five user questions.
- `brands-model-products.txt`: reviewed target aliases and same-type competitor candidates.
- `chatgpt-crawl.json`: sanitized aggregate crawl dataset.
- `report/summary.json`: machine-readable analysis result.
- `report/structured-data.md`: structured Markdown export.
- `report/report.html`: visual report.

## Result Snapshot

| Metric | Value |
|---|---:|
| Valid samples | 15 |
| Target mention rate | 73.3% |
| Target Top 3 rate | 26.7% |
| Target Top 5 rate | 40.0% |
| Target average rank | 4.91 |
| Target reference mentions | 27 |
| Unique referenced URLs | 105 |
| Unique referenced domains | 79 |

Top same-type competitor by this run was `通义千问`, with 100.0% mention rate, 93.3% Top 3 rate, 100.0% Top 5 rate, and 1.73 average rank.

## Public Sanitization

The private run preserved raw answers and logs. This public example removes local OpenCLI profile names, ChatGPT conversation URLs, raw command excerpts, and absolute filesystem paths. It keeps answer text, extracted citations, source metadata, semantic labels, and aggregate metrics so the report remains auditable without exposing the local browser session.

## Reproduction Notes

This example used a short controlled test interval. For normal fresh crawls, use the skill default random `30s-1m` interval, or `--delay-preset 1-3m` / `--delay-preset 3-10m` for slower account usage.
