# Project B input data contract

**Status:** **Accepted and frozen by student — 2026-08-14**  
**Date:** 2026-08-14 (Australia/Sydney)  
**Scope:** Project B input data only; no model or implementation approval

## 1. Authority and scope

`PROJECT_BRIEF.md` and the official files under `context/` control this contract. The student has accepted the Stage 3A audit in `docs/project_a_handoff_audit.md` as hand-off evidence. All sources must load through the protected Project B `src/data_access.py`; its verified SHA-256 is `928887403C34407C99B02984CB0600CBCF2CB9F88D7404D8E81A4B40E778B710`.

Project B will recompute every clean input and feature from the official loader. It will not copy Project A code, CSVs, panels, figures, or its `fintools.figures` dependency. Raw data must remain loader-managed and must never be committed. This contract governs source identity, schemas, keys, order, dates, missingness, mapping, and validation gates only. It approves no portfolio, sentiment method, lexicon, fusion rule, app behaviour, model output, or empirical conclusion.

## 2. Canonical raw/clean schemas and grain

Types below are pandas semantic types after deterministic conversion. Trading dates are timezone-naive `datetime64[ns]`; source news timestamps remain UTC-aware. `string?` means a nullable string. Counts and boundaries are blocking benchmarks unless this contract is revised through student review.

| Input | Canonical columns in order | Grain and key | Count, dates, and permitted missingness |
|---|---|---|---|
| Clean equity prices | `ticker` string; `date` `datetime64[ns]`; `open`, `high`, `low`, `close`, `adjClose` float64; `volume` int64; `sector` string | One row per `ticker + date`; that key must be unique | 50,300 rows; 50 tickers; 10 source sectors; 1,006 dates; 2020-01-02–2023-12-29; no missing required field |
| Clean crypto prices | `ticker` string; `date` `datetime64[ns]`; `open`, `high`, `low`, `close`, `adjClose` float64; `volume` int64 | One row per `ticker + date`; that key must be unique | 14,610 rows after cutoff; 10 tickers; 1,461 native daily dates; 2020-01-01–2023-12-31; no missing required field |
| Cleaned news | Original fields `date` `datetime64[us, UTC]`, `ticker`, `sector`, `title`, `url` string, `publisher` string?; audit fields `source_row_order` int64, `source_timestamp` `datetime64[ns, UTC]`, `source_date_utc` `datetime64[ns]` | One row per `ticker + source_timestamp + exact title`; keep the smallest `source_row_order` | 146,836 rows from 149,683; 2,847 later duplicate identities removed; 50 tickers; 10 source sectors; source dates 2020-01-01–2023-12-31. Missing publisher is allowed; required identity/text fields are not missing |
| Equity returns | `date` `datetime64[ns]`; `ticker` string; `sector` string; `adjClose` float64; `return` float64? | One row per `date + ticker`; 50,300 rows | Same 1,006 equity dates; exactly 50 missing returns—one first observation per ticker—and no other return missingness |
| Native-calendar crypto returns | `date` `datetime64[ns]`; `ticker` string; `adjClose` float64; `return` float64? | One row per `date + ticker`; 14,610 rows | Same 1,461 native dates; exactly 10 missing returns—one first observation per ticker—and no other return missingness |
| Equity-calendar-aligned crypto returns | `date` `datetime64[ns]`; `ticker` string; `return` float64 | One row per `date + ticker`; 10,060 rows | 1,006 equity dates × 10 crypto tickers; 2020-01-02–2023-12-29; zero missing returns |
| Combined return matrix | `date` `datetime64[ns]` plus 60 float64 asset columns in the order fixed in Section 3 | One row per equity date; `date` is unique | 1,006 rows × 60 assets; 2020-01-02–2023-12-29; exactly 50 missing values, all legitimate first equity returns on the first equity date |
| Mapped headlines | All cleaned-news columns plus `map_status` string, `mapped_trade_date` `datetime64[ns]`, `mapping_day_distance` int64 | One row per cleaned-news identity; only statuses `same_day` or `forward` | 146,830 rows; mapped dates lie on the 1,006-date equity calendar; distance 0–3 calendar days; no missing mapped date |
| Complete ticker-trading-day headline panel | `date` `datetime64[ns]`; `ticker` string; `sector` string; `headline_count` int64; `has_news` bool | One row per `date + ticker`; 50,300 rows | 1,006 dates × 50 equities; 12,338 rows have `headline_count = 0` and `has_news = false`; headline counts sum to 146,830 |

The long mapped-headline table, rather than a concatenated text field, is the canonical source for later headline-level operations. The complete panel is the canonical coverage grid. Any future aggregation must remain traceable to the contributing cleaned-news identities.

## 3. Deterministic membership and ordering

### Tickers

Equity tickers, lexicographically ordered:

`ABBV, ABT, ADBE, AEP, AMD, AMGN, AMT, BA, CAT, CCI, CMCSA, COP, CVX, D, DD, DIS, DOW, DUK, EA, GE, GILD, GS, INTC, KO, MMM, MRK, MS, NEE, NEM, NKE, NUE, NVDA, O, OXY, PLD, PSA, QCOM, SBUX, SHW, SLB, SO, T, TMUS, TTWO, UPS, USB, V, WFC, WMT, XOM`

Crypto tickers, lexicographically ordered:

`ADA-USD, BCH-USD, BTC-USD, EOS-USD, ETC-USD, ETH-USD, LTC-USD, TRX-USD, XLM-USD, XRP-USD`

Combined asset order is exactly the 50 equity tickers above followed by the 10 crypto tickers above. Encounter order must never determine columns or solver input.

### Sectors

The exact measured source values are:

`Comm, Consumer, Energy, Financials, Healthcare, Industrials, Materials, RealEstate, Tech, Utilities`

The protected source `sector` field retains those values. The official guide's display order and explicit display-only mapping are:

| Order | Source value | Display label |
|---:|---|---|
| 1 | `Tech` | Tech |
| 2 | `Financials` | Financials |
| 3 | `Energy` | Energy |
| 4 | `Consumer` | Consumer |
| 5 | `Industrials` | Industrials |
| 6 | `Healthcare` | Healthcare |
| 7 | `Comm` | Comm/Telecom |
| 8 | `Materials` | Materials |
| 9 | `Utilities` | Utilities |
| 10 | `RealEstate` | Real Estate |

This mapping reconciles source nomenclature with the official guide; it does not rename or mutate the protected raw `sector` field.

### Row order

- Dates are ascending.
- Canonical long price, return, mapping, and coverage panels are ordered by date then ticker. News ties are ordered by `source_timestamp`, then `source_row_order`.
- Return calculation may temporarily order by ticker then date, but its canonical output returns to date then ticker order.
- Duplicate retention is decided by the smallest `source_row_order` before any presentation sort.
- Wide return matrices use the fixed asset columns above. Reruns must reproduce keys, values, dtypes, and order deterministically.

## 4. Price and return rules

1. Retain crypto rows only where `date <= 2023-12-31`; this removes exactly ten 2024-01-01 rows.
2. Use the protected field `adjClose`; do not silently substitute `close` or rename the source field.
3. Calculate simple decimal return within ticker after sorting by date:

   `return_t = adjClose_t / adjClose_(t-1) - 1`

4. Do not fill, backfill, or forward-fill a price or return. Preserve the first missing return for every native ticker.
5. Calculate crypto returns on all 1,461 native dates first. Only then select those calculated returns onto the 1,006-date equity calendar.
6. The combined panel uses the observed equity trading calendar. Never merge equity and crypto price levels first and calculate crypto returns afterward.

## 5. News identity, preservation, and mapping

1. Assign zero-based `source_row_order` from the official loader's row order before sorting or deduplication.
2. Preserve the loaded `date` and create an auditable `source_timestamp` normalised to nanosecond UTC without changing the instant. Derive `source_date_utc` separately as the UTC calendar date for mapping.
3. Preserve title casing, punctuation, whitespace, and exact text. Do not strip or normalise title content for duplicate identity.
4. The canonical duplicate key is `ticker + source_timestamp + exact title`. Retain the smallest `source_row_order`. Never deduplicate on mapped date or ticker-date alone.
5. For each cleaned headline, find the same observed equity trading date or the next observed equity trading date using the complete calendar—not a weekend-only rule. Never map backward.
6. Mapping must expose `map_status`, `mapped_trade_date`, and non-negative `mapping_day_distance`. Allowed statuses are `same_day`, `forward`, and `unmapped_end_of_sample` in the full mapping audit; the 146,830-row tradable mapped table contains only the first two.
7. Missing publisher remains missing and is not a deletion criterion. In the Stage 3B measurement, 137,447 cleaned headlines had missing publisher values.

## 6. No-news, neutral-news, and lag semantics

- `has_news = false` and `headline_count = 0` means no information. A future sentiment value for that ticker-day must be missing, not zero.
- `has_news = true` with a later score exactly equal to zero means scored-neutral news. It is not the same state as no news.
- Sentiment scoring is not authorised by this contract.
- Any later tradable sentiment signal must be shifted by at least one observed equity trading day. Information aligned to Monday is first usable for Tuesday's decision.
- A feature used for decision date `t` may use no source aligned later than the previous observed equity trading date. Later implementation must test this invariant at boundaries, weekends, and holidays.

## 7. Six-unmapped policy

The accepted deterministic exclusions are all AMD/Tech:

| `source_row_order` | UTC source date |
|---:|---|
| 14659 | 2023-12-30 |
| 14660 | 2023-12-30 |
| 14661 | 2023-12-30 |
| 14662 | 2023-12-31 |
| 14663 | 2023-12-31 |
| 14664 | 2023-12-31 |

They occur after the final observed equity date, 2023-12-29, and must not be force-mapped. Exclude them from mapped headline panels, trading-day-aligned news volume, sentiment signals, fusion inputs, and all trading uses. They may remain in valid, disclosed, non-trading corpus descriptions such as vocabulary counts.

Required reconciliation:

`146,836 cleaned headlines = 146,830 mapped headlines + 6 unmapped headlines`

## 8. Extreme-observation policy

An extreme is defined by:

`abs(adjClose_t / adjClose_(t-1) - 1) >= 0.25`

The bounded Stage 3B review measured:

| Asset class | Extremes | Share of observed native returns | Ticker distribution |
|---|---:|---:|---|
| Equity | 4 | 0.007960% | COP 1; OXY 2; SLB 1 |
| Crypto | 65 | 0.445205% | ADA-USD 4; BCH-USD 8; BTC-USD 1; EOS-USD 7; ETC-USD 13; ETH-USD 4; LTC-USD 4; TRX-USD 4; XLM-USD 7; XRP-USD 13 |

All 69 have unique ticker-date keys; finite, strictly positive current and previous `adjClose`; finite, non-negative current and previous volume; finite calculated returns; and an observed prior source row. Base price panels have no missing `adjClose`, and the review used no fill. Equity predecessor gaps are one or three calendar days, consistent with an observed equity calendar; crypto predecessor gaps are one day.

These checks establish internal source-row consistency only. They do not economically or event-verify a movement. All 69 remain in canonical base data: no deletion, replacement, winsorisation, or alteration is permitted in canonical results merely because a return is large. They remain a disclosed limitation, and later authorised portfolio work must present separately labelled sensitivity evidence without replacing canonical results.

## 9. Validation gates

`BLOCK` stops future execution before model use. `WARN` preserves the observation and records the condition. `PASS` records affirmative evidence but does not replace downstream tests.

| Level | Rule and required response |
|---|---|
| BLOCK | Workspace is not the exact Project B root, data did not load through the protected local loader, or loader hash/path is unexpected. |
| BLOCK | A required column or contracted dtype is absent, or a ticker/date key is null or invalid. |
| BLOCK | Any price or return panel has duplicate `ticker + date` keys, or cleaned news has a duplicate `ticker + source_timestamp + exact title` key. |
| BLOCK | `adjClose` is non-finite or non-positive. Volume invalidity must be investigated; it must not be silently coerced. |
| BLOCK | A crypto row later than 2023-12-31 survives, or the cutoff does not remove exactly ten 2024-01-01 rows. |
| BLOCK | Ticker or source-sector membership, benchmark counts, or boundary dates differ from Sections 2–3. Do not force a match; stop and document the discrepancy. |
| BLOCK | A retained title differs from its official source title in casing, punctuation, whitespace, or text. |
| BLOCK | A headline maps backward, maps outside the observed equity calendar, or a non-endpoint record lacks the same-or-next observed date. |
| BLOCK | `146,836 = 146,830 + 6` fails, or the six deterministic source orders/dates differ. |
| BLOCK | A decision-date feature contains information aligned after the previous observed trading date, or the required one-trading-day lag fails. |
| BLOCK | Asset/sector/row order is nondeterministic, or a controlled rerun differs in schema, keys, order, or values. |
| WARN | Publisher is missing; retain the headline and disclose missingness. |
| WARN | A ticker-day has no news; retain the complete panel row with `headline_count = 0`, `has_news = false`, and future sentiment missing. |
| WARN | One of the 69 retained extremes is present; retain it and carry the limitation/sensitivity requirement forward. |
| WARN | The first native return per ticker is missing; retain it. Any additional unexplained return missingness is a BLOCK. |
| PASS | Current Stage 3B in-memory verification matches every benchmark, preserves titles, maps no record backward or off-calendar, and passes every bounded extreme consistency check. |

## 10. Future test matrix

No tests are created in Stage 3B. A later authorised implementation must include at least:

| Test family | Minimum cases |
|---|---|
| Schema, counts, and keys | Exact columns/dtypes; row and distinct counts; non-null keys; price/news/panel uniqueness |
| Boundary dates | Equity start/end; crypto raw 2024 rows and cutoff; clean news end; no mapping after 2023-12-29 |
| Native crypto returns | Synthetic and real regression proving native-calendar calculation before equity-date selection, including a Monday value |
| Six-record regression | Exact source orders 14659–14664, dates, status, exclusion uses, and `146,836 = 146,830 + 6` |
| Forward mapping | Same day, weekend, weekday holiday, maximum observed shift, end-of-sample failure, and never-backward assertions |
| No-news versus neutral-news | Separate missing no-information state from a genuine zero score on a news-bearing day |
| Lag and leakage | Monday-to-Tuesday use, weekend/holiday boundaries, first tradable date, and no source newer than `t-1` |
| Asset ordering | Exact 50-equity, 10-crypto, 60-combined column order and sector display mapping |
| Deterministic rerun | Identical schema, keys, row/column order, missingness, and numeric values on repeated controlled runs |
| Extreme retention | Reproduce the 4/65 split and prove no canonical deletion, winsorisation, replacement, or fill |
| Output schemas | Validate each required output only after its model-dependent schema is approved in its implementation stage |

## 11. Deferred model and output decisions

The required future filenames remain:

- `results/data/fund_returns.csv`
- `results/data/fund_weights.csv`
- `results/data/sector_sentiment_index.csv`
- `results/tables/performance_metrics.csv`

Their detailed, model-dependent schemas will be frozen only in their separately authorised implementation stages. This contract invents no portfolio method, estimation window, constraint, parameter, sentiment score, lexicon value, fusion rule, output value, or result.

## 12. Contract status

**Accepted and frozen by student — 2026-08-14**
