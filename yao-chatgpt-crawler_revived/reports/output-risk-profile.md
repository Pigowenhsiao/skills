<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-chatgpt-crawler
Created by: 姚金刚
Date: 2026-06-25
X: https://x.com/yaojingang
-->

# Output Risk Profile

## Data Risk

Fresh crawls can contain ChatGPT conversation URLs, local OpenCLI profile names, local output directories, raw terminal excerpts, and account-specific UI state. Keep full `raw/` and `logs/` artifacts private unless the user explicitly approves publication after review.

## Public Example Rule

Before committing examples:

- Replace local crawler paths with `scripts/chatgpt_browser_crawl.mjs`.
- Replace local output directories with the example directory.
- Replace profile names with `<connected-opencli-profile>`.
- Remove ChatGPT conversation IDs and page URLs.
- Remove `result.raw` command excerpts from public aggregate JSON.
- Replace absolute report paths with relative example paths.

## Interpretation Risk

The report estimates repeated-sample visibility in one ChatGPT account, time window, language, and prompt set. It is not an official ChatGPT ranking, a market-share metric, or a guarantee of future answer behavior.
