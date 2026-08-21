# Taiwan Stock Sources

## Official Data Priority

Use official sources first. Prefer this order:

1. TWSE official data
2. TPEx official data
3. MOPS / company filings
4. Company IR sites for business descriptions

Do not rely on news articles for core financial numbers when official data is available.

## Recommended Official Endpoints

- TWSE valuation:
  - `https://www.twse.com.tw/rwd/zh/afterTrading/BWIBBU_d?date=YYYYMMDD&selectType=ALL&response=csv`
- TWSE listed company basic info:
  - `https://openapi.twse.com.tw/v1/opendata/t187ap03_L`
- TPEx mainboard valuation:
  - `https://www.tpex.org.tw/openapi/v1/tpex_mainboard_peratio_analysis`
- TPEx mainboard quotes:
  - `https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes`
- TWSE monthly revenue:
  - `https://openapi.twse.com.tw/v1/opendata/t187ap05_L`
- TPEx monthly revenue:
  - `https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap05_O`
- TWSE income statement:
  - `t187ap06_L_ci`
  - `t187ap06_L_basi`
  - `t187ap06_L_fh`
  - `t187ap06_L_ins`
  - `t187ap06_L_bd`
  - `t187ap06_L_mim`
- TPEx income statement:
  - `mopsfin_t187ap06_O_ci`
  - `mopsfin_t187ap06_O_basi`
  - `mopsfin_t187ap06_O_fh`
  - `mopsfin_t187ap06_O_ins`
  - `mopsfin_t187ap06_O_bd`
  - `mopsfin_t187ap06_O_mim`
- TWSE balance sheet:
  - `https://openapi.twse.com.tw/v1/opendata/t187ap07_L_ci`
- TPEx balance sheet:
  - `https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap07_O_ci`

## Default Practical Metrics

- Growth signal:
  - latest monthly revenue YoY
  - latest annual or trailing EPS
- Quality signal:
  - ROE or proxy ROE
  - industry position
  - whether at least one core business has stable cash flow
- Valuation signal:
  - PE
  - PB
  - yield

If official BPS is unavailable, a rough proxy is:

`proxy_bvps = price / PB`

`proxy_roe = EPS / proxy_bvps * 100`

State clearly that proxy ROE is a screening approximation, not the final audited ROE.

## Common Cyclical Filters

Unless the user explicitly asks for cyclical opportunities, treat these industries as higher-risk:

- memory-related names
- shipping
- steel
- cement
- plastics
- paper
- textiles
- building materials and construction
- tourism

Passing screen numbers is not enough if the result is mostly a cycle rebound.

## Manual Second-Pass Questions

After the numeric screen, ask:

1. Is this a leader or a niche leader?
2. What is the moat: scale, brand, certification, ecosystem, distribution, switching costs, or data?
3. Is there at least one business line that can consistently generate cash flow?
4. Is the current growth broad-based or just a one-cycle rebound?
5. Is the valuation still explainable by the growth rate?

## Output Checklist

Before finalizing, ensure the answer includes:

- exact data dates
- a shortlist of 5-10 names
- a distinction between stronger and weaker fits
- at least one key risk per company or per group
- source links
