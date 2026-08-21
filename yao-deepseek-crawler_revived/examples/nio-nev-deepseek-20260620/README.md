# NIO New Energy Vehicle DeepSeek Crawl Example

This folder contains a real DeepSeek web crawl example generated on 2026-06-20 with `yao-deepseek-crawler`.

## Input

- Keywords: 4
- Repeat count: 5 per keyword
- Planned samples: 20
- Successful samples: 20
- Failed samples: 0
- Target entity: `蔚来`
- Analysis aliases: `蔚来ES8`, `蔚来ES6`, `蔚来EC6`, `NIO`, and related NIO model names

## File Map

- `questions.txt`: input questions.
- `brands.txt`: reviewed brand and competitor alias table used for the brand/company report.
- `deepseek-crawl.json`: canonical crawl dataset with all samples.
- `raw/`: one raw DeepSeek result JSON per sample.
- `logs/`: one execution log per sample.
- `report-brand-company/`: recommended report for this example because the keywords ask about new energy vehicle brands.
- `report/`: product-entity report generated from the same raw dataset.

## Recommended Report

Open `report-brand-company/report.html` for the visual report. The same cleaned data is exported as `report-brand-company/structured-data.md` and `report-brand-company/structured-data.xlsx`.
