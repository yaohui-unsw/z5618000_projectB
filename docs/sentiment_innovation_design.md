# Sentiment innovation and fusion design

**Student reviewed and accepted — methodology frozen before sentiment and fusion implementation.**

## 1. Authority, scope, and pre-result status

This proposal is governed by `PROJECT_BRIEF.md`, the official `context/` files, the accepted Project B data contract, and `AGENTS.md`, in that order. It freezes a transparent sentiment baseline, a student-controlled finance-lexicon extension, an evidence-reliability diagnostic, and three prespecified portfolio overlays before any full-period sentiment or fusion result is calculated.

Stage 6A authorises design documentation and a 2020-only lexicon-candidate review. It does not authorise an operational lexicon, full-corpus scoring, a sector index, fusion, portfolio regeneration, result files, figures, an application, or an empirical conclusion. A term is operational only after the student has individually accepted or edited it and its final value.

The lexicon calibration corpus is the cleaned headline corpus with inclusive UTC source dates `2020-01-01` through `2020-12-31`. Candidate selection and proposed values must not use 2021–2023 frequencies, returns, portfolio weights, fund performance, or fusion outcomes.

## 2. Sentiment models and text preservation

The proposed models are:

1. `plain_vader`: unchanged NLTK VADER.
2. `finance_vader`: plain VADER plus only student-approved finance terms and student-approved final values.
3. `evidence_aware_finance`: finance-VADER with evidence reliability applied after past-only standardisation for the tradable signal. `finance_score × reliability` is retained only as a raw diagnostic; it is not a separately tuned trading signal.

Every headline is scored separately using its exact cleaned title. Casing, punctuation, whitespace, and text remain unchanged. The workflow must not strip stopwords, stem, lemmatise, concatenate unrelated headlines, overwrite the source title, or convert a no-news observation to neutral. A plain and finance compound score is calculated for each real headline before aggregation.

Diagnostics must report both:

- exact-zero compound rate: fraction with `compound == 0`;
- neutral-band rate: fraction with `abs(compound) < 0.05`.

These rates answer different questions and must not be conflated.

## 3. Ticker-day aggregation and missingness

For ticker `i` on an aligned equity trading date `d` with `n >= 1` mapped headlines:

- `plain_score` is the equal-weight mean of the separate headline plain-VADER compounds;
- `finance_score` is the equal-weight mean of the separate headline finance-VADER compounds;
- `headline_count = n` and `has_news = true`.

For a ticker-day without news, `headline_count = 0`, `has_news = false`, and all sentiment scores, reliability fields, and current-day z-scores are missing. No score is set to zero and no older score is carried forward. A genuine compound score of exactly zero when `has_news = true` remains scored-neutral news and is distinct from no news.

## 4. Evidence reliability

For each news-bearing ticker-day:

- `n` is headline count;
- `covered_headline_share` is the fraction of headlines containing at least one token with non-zero valence in the active finance-VADER lexicon;
- `m` is the number of finance-model non-neutral headlines, using `abs(compound) >= 0.05`;
- if `m > 0`, `directional_agreement = abs(sum(sign(compound_j))) / m`, where the sum contains only those `m` non-neutral headlines;
- if `m == 0`, `directional_agreement = 0`;
- `volume_evidence = n / (n + 1)`;
- `reliability = covered_headline_share × directional_agreement × volume_evidence`.

Reliability must be finite and lie in `[0,1]`. The raw diagnostic is:

`evidence_aware_compound = finance_score × reliability`.

Token matching for coverage uses the same deterministic token-shaped unigram rule frozen for the lexicon review: lowercase only for matching, while source titles remain unchanged. The active finance lexicon means vanilla VADER plus only student-approved custom entries. Separately report:

`custom_finance_term_hit_share = headlines containing at least one approved custom term / headlines`.

This custom-term measure must not replace `covered_headline_share` in reliability.

Limitations are substantive: directional agreement is not truth; article count is not information quality; repeated or syndicated coverage may inflate evidence; lexicon coverage does not prove contextual accuracy; and reliability scaling can suppress valid low-volume information.

## 5. Sector index

Within each raw sector and aligned date, equally weight the ticker-day observations for tickers that actually have news. Do not insert no-news tickers with zero scores and do not include them in the score denominator.

Record headline count, ticker count with news, ticker coverage, plain compound, finance compound, mean reliability, raw evidence-aware compound, and custom finance-term hit share. Ticker coverage is:

`sector tickers with news / total eligible tickers in that sector`.

Use the accepted raw-to-display sector mapping. The required `sector_sentiment_index.csv` column list supplied for this stage omits `custom_finance_term_hit_share` even though the methodology requires that sector diagnostic. The proposed resolution is to preserve the exact required sector-index schema below and store the sector-level custom-term diagnostic in `sentiment_diagnostics.csv`. This remains an explicit student-review item rather than a silent schema change.

## 6. Past-only standardisation

For ticker `i` on aligned equity trading date `d`, calculate `plain_z` from `plain_score` and `finance_z` from `finance_score` as follows:

1. take non-missing observations in the previous 252 observed equity trading dates only;
2. exclude date `d`;
3. require at least 60 prior non-missing observations;
4. use the sample mean and sample standard deviation (`ddof=1`);
5. require a finite standard deviation greater than `1e-8`;
6. calculate the current score against those past-only parameters;
7. clip only the resulting z-score to `[-3,+3]`;
8. otherwise leave the z-score missing.

Do not clip headline scores or canonical asset returns. Define the current aligned-date ticker signal:

`evidence_aware_signal = finance_z × reliability`.

Do not separately standardise `finance_score × reliability` for portfolio formation; doing so would create an unintended second evidence-aware trading model.

For sector diagnostics only, apply the same past-only rule separately within each sector to `plain_compound`, `finance_compound`, and `evidence_aware_compound`, yielding sector `plain_z`, `finance_z`, and `evidence_aware_z`. Sector z-scores are diagnostics and must not replace ticker-level portfolio signals.

## 7. Trading lag

A ticker score aligned to `d` becomes tradable only on the next observed equity trading date. At decision date `t`, no signal may use a headline aligned on `t` or later. The evidence-aware lag uses both `finance_z` and reliability from the same prior observed trading date.

If the immediately previous observed trading day has no usable score, preserve the missing signal and use multiplier one operationally. Never carry older sentiment forward. Later tests must cover ordinary weekdays, weekends, and exchange holidays.

## 8. Fusion variants and fixed tilt

Apply three variants to every accepted Equity and Combined base fund across all four portfolio methods:

- `plain_vader_naive`: lagged ticker-level `plain_z`;
- `finance_vader_naive`: lagged ticker-level `finance_z`;
- `evidence_aware_finance`: lagged ticker-level `finance_z × reliability`.

This produces `8 equity-bearing base funds × 3 variants = 24 overlay strategies`. Crypto-only funds are excluded. Use the same monthly rebalance dates as the accepted base portfolios; sentiment does not introduce daily trading.

Freeze `lambda = 0.10`. For equity asset `i`:

`u_i = base_target_weight_i × exp(lambda × signal_i)`.

A missing signal uses multiplier one. Lambda, clipping, coverage, history, reliability, lag, fund selection, and reporting sample must not be tuned after performance is observed.

### Equity projection

For an Equity fund, calculate raw tilted values, normalise to one, and use the accepted deterministic Euclidean capped-simplex projection:

`minimise sum_i (w_i - u_i)^2`

subject to `0 <= w_i <= 0.20` and `sum_i w_i = 1`.

### Combined projection

For a Combined fund, keep every crypto target weight numerically unchanged. Let the base equity-sleeve total be `E`; preserve both `E` and the original crypto-sleeve total. Apply multipliers only to equities, normalise raw equity values to `E`, and project the equity sleeve subject to `0 <= w_i <= 0.20` and `sum_i w_i = E`.

Projection infeasibility or validation failure is a `BLOCK`. Do not relax the cap, alter crypto weights, or substitute equal/base weights. A failed rebalance must not produce portfolio results. Reuse Stage 5A weight drift, inception convention, turnover, 5-bps transaction cost, net-return calculation, and performance definitions unchanged.

## 9. Prespecified comparisons and interpretation

Report every overlay against its corresponding frozen base fund using net annualised return, annualised volatility, Sharpe ratio, maximum drawdown, cumulative return, average turnover, total turnover, and transaction-cost drag.

Across the full evidence set, also report exact-zero and neutral-band rates; active lexicon coverage; custom-term hit share; plain-to-finance score changes; sector and ticker coverage; reliability distribution; multiplier-one frequency from missing signals; and active-tilt frequency and magnitude.

Negative, weak, or insignificant results remain reportable. Do not select only favourable funds, methods, dates, sectors, variants, or diagnostics, and do not alter the design to manufacture improvement.

## 10. Frozen future output schemas

These files are documented only; none is created in Stage 6A. Dates serialize as ISO `YYYY-MM-DD`. `string` fields are non-empty unless a missing meaning is explicitly stated. Float missingness is CSV `NA`; infinities are forbidden. All outputs require exact column order, unique primary keys, stable sorting, deterministic reruns, and no placeholder rows.

### `results/data/sector_sentiment_index.csv`

Purpose: required sector-level sentiment index. Grain/key: one raw sector per observed equity trading date; primary key `(date, sector)`. Sort: `date` ascending, then accepted raw-sector order.

| Order | Column | Dtype | Missing-value meaning |
|---:|---|---|---|
| 1 | `date` | date | Never missing; aligned equity date. |
| 2 | `sector` | string | Never missing; accepted raw sector. |
| 3 | `sector_display` | string | Never missing; accepted display label. |
| 4 | `headline_count` | int64 | Zero means no sector headlines. |
| 5 | `ticker_count_with_news` | int64 | Zero means no sector ticker had news. |
| 6 | `ticker_coverage` | float64 | Zero when no ticker had news; must be `[0,1]`. |
| 7 | `plain_compound` | float64 | Missing when no ticker has news. |
| 8 | `finance_compound` | float64 | Missing when no ticker has news. |
| 9 | `mean_reliability` | float64 | Missing when no ticker has news. |
| 10 | `evidence_aware_compound` | float64 | Missing when no ticker has news. |
| 11 | `plain_z` | float64 | Missing until history/dispersion gate passes or current score is absent. |
| 12 | `finance_z` | float64 | Same gate as `plain_z`. |
| 13 | `evidence_aware_z` | float64 | Same gate, applied to raw sector evidence-aware compound. |

Validation must reconcile headline/ticker counts to ticker-day data, coverage to the frozen sector universe, equal-weight aggregation independently, past-only z-score windows, no-news missingness, and the accepted sector mapping.

### `results/data/ticker_sentiment_daily.csv`

Purpose: complete ticker-level daily sentiment, diagnostics, standardised signals, and explicitly lagged tradable values. Grain/key: one equity ticker per observed equity trading date; key `(date, ticker)`. Sort: date ascending then frozen equity-ticker order.

Exact columns: `date` (date), `ticker` (string), `sector` (string), `headline_count` (int64), `has_news` (bool), `plain_score` (float64), `finance_score` (float64), `covered_headline_share` (float64), `nonneutral_headline_count` (int64), `directional_agreement` (float64), `volume_evidence` (float64), `reliability` (float64), `custom_finance_term_hit_share` (float64), `evidence_aware_compound` (float64), `plain_z` (float64), `finance_z` (float64), `evidence_aware_signal` (float64), `signal_source_date` (date), `lagged_plain_signal` (float64), `lagged_finance_signal` (float64), `lagged_evidence_aware_signal` (float64).

For no-news rows, counts are zero, `has_news=false`, and current-day score/reliability/z/signal fields are missing. `evidence_aware_compound` is the raw `finance_score × reliability`; `evidence_aware_signal` is the unlagged aligned-date `finance_z × reliability`. The three `lagged_*` fields are usable on row `date` and come only from `signal_source_date`, the immediately prior observed date; they are missing if that source date has no usable value. Validation must reconcile the complete `50 × 1,006` grid, headline totals, formulas, history gates, source dates, and no-news/scored-neutral distinction.

### `results/data/fusion_returns.csv`

Purpose: OOS returns for all overlays. Grain/key: one overlay per live date; key `(date, overlay_id)`. Sort: date, then deterministic overlay order.

Exact columns: `date` (date), `overlay_id` (string), `base_fund_id` (string), `family` (string), `method` (string), `variant` (string), `gross_return` (float64), `turnover` (float64), `transaction_cost` (float64), `net_return` (float64), `is_rebalance` (bool).

No field is missing. Validation requires exactly 24 overlay IDs, Equity/Combined only, accepted base calendars, monthly rebalance keys, finite returns greater than `-1`, and independent cost/turnover reconciliation.

### `results/data/fusion_weights.csv`

Purpose: rebalance-level overlay holdings and projection audit. Grain/key: one asset per overlay rebalance; key `(date, overlay_id, ticker)`. Sort: date, overlay order, then frozen family asset order.

Exact columns: `date` (date), `overlay_id` (string), `base_fund_id` (string), `family` (string), `method` (string), `variant` (string), `ticker` (string), `base_target_weight` (float64), `pretrade_weight` (float64), `signal_source_date` (date), `signal_value` (float64), `multiplier` (float64), `raw_tilted_value` (float64), `target_weight` (float64), `trade_weight` (float64), `turnover` (float64), `projection_success` (bool), `projection_status` (string).

For Combined crypto rows, signal date/value and raw equity tilt are missing, multiplier is exactly one, and target weight equals the base crypto target within tolerance. Missing equity signal has a missing `signal_value`, multiplier one, and a present raw value equal to the base target. Validation must enforce cap/sum constraints, Combined sleeve preservation, deterministic projection, and no failed projection row in a published result.

### `results/tables/sentiment_diagnostics.csv`

Purpose: auditable summary diagnostics without widening canonical daily schemas. Grain/key: one `(scope, entity, model, metric)` row; key includes `start_date` and `end_date` when the metric is window-specific. Sort: scope, entity, model, metric, start date, end date.

Exact columns: `scope` (string: `headline`, `ticker`, or `sector`), `entity` (string; `ALL` or a ticker/raw sector), `model` (string), `metric` (string), `value` (float64), `numerator` (float64), `denominator` (float64), `start_date` (date), `end_date` (date), `notes` (string).

`numerator`/`denominator` may be missing for distribution statistics; dates may be missing only for genuinely timeless lexicon metadata. It must include exact-zero, neutral-band, active coverage, custom-term hit share (including the sector-level diagnostic omitted from the required index schema), score-change, reliability, missing-signal, and tilt diagnostics. Rates must reconcile to their numerators and denominators.

### `results/tables/finance_lexicon.csv`

Purpose: operational provenance for approved custom entries only. Grain/key: one approved term; key `term`. Sort: term ascending.

Exact columns: `term` (lowercase string), `candidate_class` (string), `vanilla_vader_value` (float64, missing only for additions), `approved_finance_value` (float64), `direction` (string), `student_decision` (string), `decision_date` (date), `rationale` (string).

Pending or rejected terms must never appear. Values must be in `[-3,+3]` on 0.5 increments and reconcile exactly to the student-reviewed record.

### `results/tables/fusion_performance_metrics.csv`

Purpose: full performance metrics for all 24 overlays. Grain/key: one overlay; key `overlay_id`. Sort: deterministic overlay order.

Exact columns: `overlay_id`, `base_fund_id`, `family`, `method`, `variant` (strings); `start_date`, `end_date` (dates); `observations`, `annualisation` (int64); `transaction_cost_bps`, `net_cumulative_return`, `net_annualised_return`, `net_annualised_volatility`, `net_sharpe_ratio`, `net_max_drawdown`, `gross_cumulative_return`, `gross_annualised_return`, `gross_sharpe_ratio`, `average_rebalance_turnover`, `total_turnover`, `transaction_cost_drag` (float64); and `rebalance_count` (int64).

No values may be missing. Metrics must independently reconcile to `fusion_returns.csv` using Stage 5A definitions.

### `results/tables/fusion_comparison.csv`

Purpose: complete base-versus-overlay comparison. Grain/key: one overlay; key `overlay_id`. Sort: deterministic overlay order.

Exact columns: `overlay_id`, `base_fund_id`, `family`, `method`, `variant` (strings); `delta_net_annualised_return`, `delta_annualised_volatility`, `delta_net_sharpe_ratio`, `delta_net_max_drawdown`, `delta_net_cumulative_return`, `delta_average_turnover`, `delta_total_turnover`, `delta_transaction_cost_drag` (float64).

All 24 rows and all deltas are required; none may be omitted because performance is weak. Each delta is overlay minus corresponding base and must reconcile to the two metric sources.

## 11. Required future tests

Later authorised implementation must use independent synthetic calculations where practical and cover:

- exact title preservation and vanilla VADER reproducibility;
- isolation of approved custom entries; pending/rejected terms excluded;
- no 2021–2023 information in candidate selection, counts, examples, or polarity;
- candidate thresholds, deterministic ordering, and earliest/lower-median example selection;
- exact-zero versus neutral-band classification and no-news versus scored-neutral states;
- separate-headline scoring and equal-weight ticker/sector aggregation;
- coverage calculations, reliability bounds, and independent manual reliability cases;
- previous-252-observed-date standardisation, current-date exclusion, minimum 60 observations, `ddof=1`, and zero/near-zero dispersion;
- ticker-versus-sector z-score separation and exact `evidence_aware_signal = finance_z × reliability`;
- one-trading-day lag across ordinary days, weekends, and holidays; no same-day/future headline use;
- future-headline perturbations leaving earlier scores, signals, and weights unchanged;
- exactly 24 overlays and exclusion of Crypto-only funds;
- fixed `lambda=0.10`, monthly-only trading, and missing-signal multiplier one;
- Equity and Combined projection feasibility, determinism, cap/sum constraints, failure as `BLOCK`, unchanged Combined crypto weights, and preserved equity sleeve;
- Stage 5A drift, inception, turnover, transaction-cost, and net-return reconciliation;
- complete base-versus-overlay reporting, exact output schemas/keys/order, and deterministic reruns.

## 12. Deferred matters and change control

Deferred pending explicit approval are individual lexicon decisions; sentiment implementation and full-corpus scoring; the sector index; all 24 overlays; results, figures, fact sheets, app, report, and deployment; empirical interpretation; and any change to this proposal.

If the student later changes a term, value, threshold, reliability component, z-score rule, lag, lambda, projection, portfolio set, or output schema, the change requires a dated rationale before results are used and the original frozen proposal must remain auditable.

**Stage 6A historical status:** Pending student review; no sentiment implementation, lexicon entry, fusion strategy, or result was authorised at that point.

## Student acceptance and Stage 6B freeze

On 2026-08-14, after ChatGPT reviewed the complete Stage 6A documents and recommendations with the student, the student exercised final authority and accepted this pre-result methodology. The accepted finance lexicon is limited to the 23 `ACCEPT` or `EDIT` entries and final values recorded in `docs/finance_lexicon_review.md`. The four rejected ETF-flow terms and every pending or previously rejected term are excluded.

The student specifically accepts and freezes:

- `plain_vader` as the unchanged baseline;
- `finance_vader` using only the 23 approved or edited entries and their student-approved final values;
- exclusion of rejected and pending terms from the operational lexicon;
- raw `evidence_aware_compound = finance_score × reliability` as a diagnostic only;
- tradable `evidence_aware_signal = finance_z × reliability`;
- past-only standardisation over the previous 252 observed equity trading dates;
- at least 60 prior non-missing observations and finite sample standard deviation greater than `1e-8`;
- exclusion of the current date from every standardisation window;
- a one-observed-trading-day lag before a signal is usable;
- no sentiment carry-forward when the immediately preceding observed trading date has no usable score;
- all 24 Equity/Combined overlays and no Crypto-only overlay;
- fixed `lambda = 0.10` and monthly-only overlay trading;
- deterministic Euclidean capped-simplex projection and `BLOCK` on failure;
- numerically unchanged Combined crypto weights and preservation of the Combined equity-sleeve total;
- unchanged Stage 5A weight drift, inception, turnover, 5-bps transaction cost, net-return, and performance rules;
- complete reporting of favourable, weak, negative, and insignificant results without result-driven parameter changes.

The sector diagnostic resolution is accepted exactly as follows:

- keep the required `sector_sentiment_index.csv` schema unchanged;
- store sector-level `custom_finance_term_hit_share` in `sentiment_diagnostics.csv`;
- do not silently add that diagnostic to the required sector-index schema.

The distinction between the raw evidence-aware diagnostic and the tradable standardised signal remains mandatory. No parameter, lexicon entry, history rule, lag, overlay rule, projection rule, cost assumption, output schema, or other methodology may be changed after performance is observed without a dated, student-approved correction record that preserves the original frozen specification.

This acceptance freezes documentation only. No sentiment scoring, full-corpus computation, sector-index generation, fusion, portfolio regeneration, output generation, figure, application, report, deployment, publication, or Git action is authorised in Stage 6B.
