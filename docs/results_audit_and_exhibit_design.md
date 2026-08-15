# Results Audit and Canonical Exhibit Design

**Review status:** `Pending student review`

## 1. Scope and authority

Stage 6C was closed by the student's 2026-08-14 acceptance of all 24 sentiment-overlay results, including favourable and unfavourable outcomes, with no ex-post tuning. Stage 7 was authorised to audit the frozen canonical CSVs independently and create reproducible report-facing figures from them. It did not authorise a model rerun, parameter change, result replacement, selective filtering, report prose, application work, deployment, publication, submission, or Git operation.

This document is an evidence and exhibit specification, not a report chapter. It separates measured findings from interpretation and limitations so the student retains authorship of the final economic analysis.

## 2. Audited immutable inputs

All hashes are SHA-256 values measured before the Stage 7 audit. The final boundary check reconfirmed these files byte-for-byte.

| Frozen canonical file | Rows / role | SHA-256 |
|---|---:|---|
| `results/data/fund_returns.csv` | 12 base-fund daily net/gross paths | `7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84` |
| `results/data/fund_weights.csv` | Base rebalance holdings and trades | `F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8` |
| `results/tables/performance_metrics.csv` | 12 base-fund metrics | `5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19` |
| `results/tables/portfolio_solver_diagnostics.csv` | Base solver evidence | `ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C` |
| `results/tables/extreme_sensitivity_metrics.csv` | Separate +/-25% return sensitivity | `40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151` |
| `results/data/ticker_sentiment_daily.csv` | 50 x 1,006 ticker-day panel | `CC9DDF834EF43B9B07240A40949716BA573A14E6ADDCD1997DFF83C125E26FCD` |
| `results/data/sector_sentiment_index.csv` | 10 x 1,006 sector-day panel | `D7670369187E3FF6909A88F6459204284A45D07941DC395CE239D8E304E8E96E` |
| `results/data/fusion_returns.csv` | 24 overlay daily paths | `5A868D15E4D649FEDCB7BF9A0D58657F1729D6F35A2A62A2DF148622EA8CEBC5` |
| `results/data/fusion_weights.csv` | Overlay rebalance holdings and audit fields | `13941551A0D3D9A07290235CCEF7C8AB389D2F78EAF36D81CE661A915F485058` |
| `results/tables/finance_lexicon.csv` | 23 student-approved/edited entries | `5E6EE31DADC6C754DD465E825FBA5F25B3BD26E5E0AA846B3A578619D444C5DB` |
| `results/tables/sentiment_diagnostics.csv` | Coverage, scoring, lag, reliability, and tilt diagnostics | `3C7842ED0F955DCA29E1E728EFD51C46AA12D4B93999DC9C72D47C436AC179B5` |
| `results/tables/fusion_performance_metrics.csv` | 24 overlay metric rows | `B75FA251E385E3709D3EC1380367D0257285D249AF742965C8FD993FCA770A07` |
| `results/tables/fusion_comparison.csv` | 24 overlay-minus-base rows | `B51DF470AEAB5932356037DF72FCF0044729C6F9F88C117E6C4B90F4922C3946` |

## 3. Independent audit methods and reconciliation

Stage 7 calculated evidence directly from the frozen daily returns, weights, ticker-day data, sector-day data, diagnostics, lexicon, and comparison tables. It did not call `run_part_b.py`, VADER, a loader, an optimiser, or a fusion model.

### Portfolio paths and metrics

- Grouped daily fund paths by unique `date + fund_id` and independently compounded `net_return` to reconstruct growth of $1 and cumulative return.
- Recomputed annualised geometric return, sample annualised volatility, zero-risk-free-rate Sharpe, and maximum drawdown from each daily net-return path.
- Confirmed Equity and Combined use 753 observations from 2021-01-04 to 2023-12-29 with annualisation 252; Crypto uses 1,095 observations from 2021-01-01 to 2023-12-31 with annualisation 365.
- Confirmed 12 required funds, 36 first-eligible monthly rebalances per fund, unique keys, long-only targets, the 20% cap, and fully invested weights.
- Reconciled gross/net arithmetic to `net = (1 - cost) * (1 + gross) - 1`, turnover only at rebalances, zero inception cost, 5-bps cost, and the solver diagnostics.
- Reconciled the separate extreme-return sensitivity deltas without treating clipped returns as corrected data. Economic/event verification of the accepted 69 extreme observations is outside the frozen CSV evidence.

### Sentiment, lag, and fusion

- Reconciled 146,836 cleaned headlines as 146,830 mapped/scored plus six disclosed endpoint-unmapped exclusions.
- Confirmed 50,300 ticker-days: 37,962 with news and 12,338 with no news; no-news sentiment fields remain missing rather than neutral zero.
- Confirmed 10,060 sector-days, ten sectors, 1,006 observed equity dates, and equal weighting across news-bearing ticker-days.
- Confirmed exactly 23 operational lexicon entries and absence of `inflow`, `inflows`, `outflow`, and `outflows`.
- Verified each populated trading signal points to the immediately preceding observed trading date, never the current or a future date, and is missing when that prior date has no usable value. There is no older-signal carry-forward.
- Reconciled 34,789 usable same-date signals with 34,788 lagged signals. The single-row difference is the last usable score at the sample boundary, for which no next trading date exists; it is not look-ahead.
- Confirmed 24 overlays (eight Equity/Combined bases times three variants), no Crypto-only overlay, complete coverage, fixed monthly base schedules, and all negative outcomes retained.
- Reconciled capped projections, weight drift, turnover, 5-bps costs, daily gross/net returns, overlay performance metrics, and every overlay-minus-base delta.
- For Combined overlays, crypto targets match their frozen base values to numerical tolerance and the equity-sleeve total is preserved before trading.

## 4. Audit status, warnings, and confidence

**Audit outcome:** `PASS with three disclosed limitations; no BLOCK.` Confidence is high for arithmetic, schema, key, timing, projection, and reported-comparison reconciliation because the tests recomputed these from daily/path-level frozen outputs.

Warnings and boundaries:

- Plain-analyser isolation passed the accepted Stage 6C validator. A CSV-only Stage 7 audit cannot reconstruct in-memory analyser state, so it verifies lexicon content and score-path evidence rather than re-instantiating VADER.
- The +/-25% sensitivity reconciles mechanically, but frozen outputs cannot economically validate the 69 underlying extreme market observations.
- No significance test was prespecified. Comparisons are descriptive out-of-sample evidence for the frozen sample and specification, not statistical proof.

Genuine Stage 7 corrections:

- The first exhibit audit incorrectly compared an absent no-news sector aggregation with published zero counts/coverage as `NaN` versus zero. The audit representation was corrected to fill expected count and coverage with zero; no canonical data or method changed.
- After direct visual inspection, fixed annotation offsets and leader lines were added to the risk-return map to separate overlapping labels. No result, axis, or encoding changed.
- The builder initially treated that intentional reporting-code revision as a deterministic-rerun failure. The predicate was narrowed so an expected visual revision is a warning on the revision build; an immediate unchanged rebuild then had identical hashes.

## 5. Exact audited findings

### Base funds

| Fund | Net ann. return | Ann. volatility | Sharpe | Max drawdown |
|---|---:|---:|---:|---:|
| Equity / Equal Weight | 12.6244% | 16.1176% | 0.8183 | -20.2566% |
| Equity / Minimum Variance | 5.3610% | 12.6903% | 0.4750 | -15.2878% |
| Equity / Maximum Sharpe | 5.8266% | 17.3033% | 0.4140 | -22.6213% |
| Equity / Risk Parity | 9.8905% | 14.5279% | 0.7219 | -18.5005% |
| Crypto / Equal Weight | 40.4560% | 81.8900% | 0.8284 | -81.5802% |
| Crypto / Minimum Variance | 67.6388% | 78.6819% | 1.0518 | -74.1993% |
| Crypto / Maximum Sharpe | 34.6857% | 78.2779% | 0.7733 | -77.1637% |
| Crypto / Risk Parity | 44.2385% | 79.8936% | 0.8619 | -79.8854% |
| Combined / Equal Weight | 15.1093% | 21.5999% | 0.7598 | -27.8878% |
| Combined / Minimum Variance | 5.3561% | 12.7149% | 0.4739 | -15.4409% |
| Combined / Maximum Sharpe | 16.5059% | 23.3386% | 0.7710 | -22.7276% |
| Combined / Risk Parity | 13.9420% | 16.2014% | 0.8868 | -19.4839% |

These rows are descriptive OOS outcomes. Large Crypto returns coexist with 74%-82% maximum drawdowns; neither side may be omitted.

### Sentiment innovation and paired outcomes

- Custom-term hit share: 18,802 / 146,830 = **12.805285%**.
- Finance lexicon changed-score share: 18,759 / 146,830 = **12.775999%**.
- Plain exact-zero / neutral-band rates: **48.845604% / 49.571613%**.
- Finance exact-zero / neutral-band rates: **50.673568% / 51.330791%**. A neutral score is not equivalent to no news.
- Reliability across 37,962 news-bearing ticker-days: mean **0.243373**, standard deviation **0.216862**, median **0.250000**, 90th percentile **0.500000**, range **0 to 0.937500**.
- Custom-term exposure is highest in Utilities (**40.085457%**) and Energy (**21.972631%**), versus **12.805285%** overall. This is a sector-context/concentration risk, not evidence of error or accuracy.
- Finance VADER has a positive Sharpe delta versus base in **5/8** eligible funds; Plain VADER in **4/8**; Evidence-aware Finance in **4/8**.
- Finance VADER exceeds Plain VADER in Sharpe for **6/8** pairs and in annualised return for **7/8** pairs. It does not improve every fund.
- Evidence-aware Finance has lower average rebalance turnover than naive Finance VADER in **8/8**, but lower annualised return and Sharpe in **8/8**.
- Active-tilt frequency is **74.6667%** for each naive variant and **50.1111%** for Evidence-aware Finance.
- Best base-relative outcome: `equity_maximum_sharpe__finance_vader_naive`, annualised-return delta **+0.0034188173** and Sharpe delta **+0.0191935447**.
- Weakest base-relative outcome: `equity_equal_weight__evidence_aware_finance`, annualised-return delta **-0.0011571521** and Sharpe delta **-0.0058965098**.

### Complete overlay delta evidence

Values are overlay minus its corresponding frozen base; return and turnover deltas are percentage points (pp), while Sharpe is unitless.

| Base fund | Variant | Ann. return delta (pp) | Sharpe delta | Avg turnover delta (pp) |
|---|---|---:|---:|---:|
| Equity Equal Weight | Plain | -0.0628 | -0.002350 | +2.5019 |
| Equity Equal Weight | Finance | -0.0647 | -0.002470 | +2.4704 |
| Equity Equal Weight | Evidence-aware | -0.1157 | -0.005897 | +0.6814 |
| Equity Minimum Variance | Plain | +0.0925 | +0.007334 | +1.0449 |
| Equity Minimum Variance | Finance | +0.1909 | +0.014698 | +1.0594 |
| Equity Minimum Variance | Evidence-aware | +0.0391 | +0.003157 | +0.2325 |
| Equity Maximum Sharpe | Plain | +0.1107 | +0.006795 | +0.7401 |
| Equity Maximum Sharpe | Finance | +0.3419 | +0.019194 | +0.6732 |
| Equity Maximum Sharpe | Evidence-aware | +0.1740 | +0.009854 | +0.2550 |
| Equity Risk Parity | Plain | -0.0221 | -0.001008 | +2.2877 |
| Equity Risk Parity | Finance | -0.0165 | -0.000657 | +2.2415 |
| Equity Risk Parity | Evidence-aware | -0.0913 | -0.005525 | +0.6127 |
| Combined Equal Weight | Plain | -0.0473 | -0.001265 | +1.9680 |
| Combined Equal Weight | Finance | -0.0466 | -0.001314 | +1.9456 |
| Combined Equal Weight | Evidence-aware | -0.0922 | -0.003474 | +0.5123 |
| Combined Minimum Variance | Plain | +0.0948 | +0.007502 | +1.0524 |
| Combined Minimum Variance | Finance | +0.1999 | +0.015362 | +1.0595 |
| Combined Minimum Variance | Evidence-aware | +0.0431 | +0.003450 | +0.2235 |
| Combined Maximum Sharpe | Plain | +0.0404 | +0.002243 | +0.6884 |
| Combined Maximum Sharpe | Finance | +0.2681 | +0.010225 | +0.6577 |
| Combined Maximum Sharpe | Evidence-aware | +0.1450 | +0.005709 | +0.2362 |
| Combined Risk Parity | Plain | -0.0115 | -0.000211 | +2.0662 |
| Combined Risk Parity | Finance | +0.0003 | +0.000389 | +2.0387 |
| Combined Risk Parity | Evidence-aware | -0.0768 | -0.003974 | +0.5660 |

## 6. Interpretation boundaries

| Category | Evidence boundary |
|---|---|
| Verified result | The reviewed finance lexicon materially changes headline scoring; Finance VADER performs better than Plain VADER in most, not all, paired comparisons; reliability scaling reduces activity and turnover; it also weakens performance versus naive Finance VADER in all eight eligible bases; transaction costs are included; no overlay is omitted. |
| Permitted interpretation | Within this frozen descriptive OOS design, the transparent finance-domain lexicon is the strongest tested sentiment extension. Reliability scaling exposes a selectivity-versus-signal-strength trade-off. |
| Required limitation | No prespecified significance test; one frozen sample/specification; lexicon coverage is not contextual accuracy; reliability is not truth or news quality; repeated reporting can inflate evidence; sector custom-term exposure is uneven; extreme returns remain economically unverified here. |
| Prohibited claim | Statistical significance, causality, guaranteed investor benefit, universal outperformance, universal lexicon validity, robustness beyond the frozen design, or that neutral sentiment means no information. |

## 7. Required-exhibit coverage

| Brief/rubric evidence need | Canonical evidence | Coverage |
|---|---|---|
| Portfolio performance metrics | Existing `performance_metrics.csv`; all 12 funds | Existing canonical table; independently reconciled |
| Growth of $1 / cumulative performance | `fund_growth_comparison.png` | Main-report candidate |
| Drawdown | `combined_drawdowns.png` | Main or appendix, depending page budget |
| Portfolio weights over time / current construction | `combined_weights_over_time.png`; existing `fund_weights.csv` | Main or appendix; deterministic top-eight + Other display |
| Risk/return/Sharpe comparison | `fund_risk_return_map.png` | Main-report candidate |
| Standalone sector sentiment index | `sector_sentiment_timeseries.png`; required sector CSV | Main-report candidate |
| Base-versus-fusion comparison | Existing `fusion_comparison.csv`; `fusion_before_after.png` | Main-report candidate |
| Innovation evidence | `sentiment_innovation_diagnostics.png` and `fusion_turnover_tradeoff.png` | Two custom innovation exhibits |
| Complete unfavourable evidence | All 24 rows in comparison table and figures, with negative bars/points retained | Covered; no selective omission |
| Fact-sheet inputs | Frozen metrics, weights, growth, drawdown, and dates | Evidence prepared; fact-sheet/app design deferred |

## 8. Figure specifications

### `fund_growth_comparison.png`

- **Requirement/question:** required cumulative-performance exhibit; how did $1 invested in each base method evolve within each family?
- **Sources/fields:** `fund_returns.csv`: `date`, `fund_id`, `family`, `method`, `net_return`.
- **Population/sample:** all 12 base funds; Equity/Combined 2021-01-04--2023-12-29, Crypto 2021-01-01--2023-12-31.
- **Form/encoding:** three family small multiples; method colour plus line style/markers; y-axis Growth of $1.
- **Annotation/caveat:** live dates and costs included; descriptive OOS paths, not guaranteed returns.
- **Placement:** main performance section; Streamlit overview/fund comparison.

### `combined_drawdowns.png`

- **Requirement/question:** required drawdown evidence; how severe and persistent were losses for the investable Combined products?
- **Sources/fields:** `fund_returns.csv`: Combined `date`, `method`, `net_return`; drawdown independently derived from compounded wealth.
- **Population/sample:** all four Combined methods, 2021-01-04--2023-12-29.
- **Form/encoding:** one aligned percentage panel, method colour/line styles, common zero reference.
- **Annotation/caveat:** Combined chosen by prespecified product relevance, not ex-post performance.
- **Placement:** performance-risk section or appendix; Streamlit risk tab.

### `combined_weights_over_time.png`

- **Requirement/question:** required weight-dynamics exhibit; how did Combined targets change across methods?
- **Sources/fields:** `fund_weights.csv`: Combined `date`, `method`, `ticker`, `target_weight`.
- **Population/sample:** all Combined rebalances and assets.
- **Form/encoding:** four method small multiples; deterministic eight assets with highest mean target weight across displayed funds; all remaining weights summed as `Other` without omission or renormalisation.
- **Annotation/caveat:** display aggregation only; canonical asset-level holdings remain in the CSV.
- **Placement:** construction section or appendix; Streamlit holdings tab.

### `fund_risk_return_map.png`

- **Requirement/question:** cross-fund risk-return/Sharpe comparison; what return accompanied each fund's volatility?
- **Sources/fields:** `performance_metrics.csv`: annualised net return, volatility, Sharpe, family, method.
- **Population/sample:** all 12 base funds over their complete OOS periods.
- **Form/encoding:** volatility x-axis, net annualised return y-axis; method colour, family marker, Sharpe-informed marker size; fixed label offsets and leader lines.
- **Annotation/caveat:** different 252/365 family calendars are explicitly identified; risk-return position is not investment advice.
- **Placement:** main performance section; Streamlit comparison view.

### `sector_sentiment_timeseries.png`

- **Requirement/question:** required standalone sector-sentiment series; how did Finance VADER sentiment vary across all sectors?
- **Sources/fields:** `sector_sentiment_index.csv`: `date`, `sector_display`, `finance_compound`.
- **Population/sample:** all ten sectors and 1,006 equity dates, 2020-01-02--2023-12-29.
- **Form/encoding:** ten small multiples with common y-scale and zero line; faint daily values plus a 21-trading-day rolling mean.
- **Annotation/caveat:** smoothing is visual only and was never used for trading; no-news sector dates remain missing.
- **Placement:** main sentiment section; Streamlit sentiment view.

### `fusion_before_after.png`

- **Requirement/question:** required base-versus-sentiment comparison; which frozen overlays improved or reduced annualised return and Sharpe?
- **Sources/fields:** `fusion_comparison.csv`: base, variant, annualised-return and Sharpe deltas.
- **Population/sample:** all eight eligible bases and all three variants (24 rows).
- **Form/encoding:** aligned horizontal delta-bar panels; annualised-return delta in basis points and Sharpe delta; zero lines; method grouping and variant encoding.
- **Annotation/caveat:** overlay minus base; all negative values retained; no significance claim.
- **Placement:** main fusion section; Streamlit comparison view.

### `sentiment_innovation_diagnostics.png`

- **Requirement/question:** custom innovation evidence; how did the finance lexicon change scoring and where were reviewed terms concentrated?
- **Sources/fields:** `sentiment_diagnostics.csv`: exact-zero, neutral-band, overall hit, changed-score, and sector hit-share metrics.
- **Population/sample:** all 146,830 mapped headlines and all ten sectors, 2020-01-02--2023-12-29.
- **Form/encoding:** three coordinated panels: plain/finance score rates, overall hit/change rates, and sector custom-term hit shares.
- **Annotation/caveat:** Utilities and Energy called out; term exposure is not sentiment accuracy.
- **Placement:** main innovation section; Streamlit methodology/diagnostics view.

### `fusion_turnover_tradeoff.png`

- **Requirement/question:** custom innovation evidence; what turnover reduction and Sharpe trade-off accompanied each overlay?
- **Sources/fields:** `fusion_comparison.csv`: `delta_average_turnover`, `delta_net_sharpe_ratio`, base, family, method, variant.
- **Population/sample:** all 24 overlays.
- **Form/encoding:** turnover delta x-axis in percentage points, Sharpe delta y-axis; fixed variant colours/markers, zero reference lines; only strongest positive/negative and evidence-aware cluster annotated.
- **Annotation/caveat:** descriptive trade-off, not an efficient frontier or causal effect.
- **Placement:** main innovation/limitations section or appendix; Streamlit diagnostics view.

## 9. Report evidence matrix

| Proposed evidence bullet (not report prose) | Exact support | Source/key | Exhibit/table | Caveat | Status |
|---|---|---|---|---|---|
| Finance VADER changes a material subset of headlines. | 18,759 / 146,830 = 12.775999% | `sentiment_diagnostics.csv`, headline/plain_to_finance/changed_score_share | Innovation diagnostics | Change is not proof of greater accuracy. | Verified |
| Reviewed-term exposure is uneven by sector. | Utilities 40.085457%; Energy 21.972631%; overall 12.805285% | `sentiment_diagnostics.csv`, sector and headline hit-share rows | Innovation diagnostics | Ticker tagging and context can concentrate exposure. | Verified |
| Finance beats Plain on most paired comparisons, not all. | Sharpe 6/8; annualised return 7/8 | `fusion_comparison.csv`, paired base/variant keys | Fusion before/after | Descriptive; no significance test. | Verified |
| Finance is not universally beneficial versus base. | Positive Sharpe delta 5/8 | `fusion_comparison.csv`, finance variant | Fusion before/after | Three funds do not improve. | Verified |
| The strongest base-relative result is modest. | +0.0034188173 annualised return; +0.0191935447 Sharpe | `equity_maximum_sharpe__finance_vader_naive` | Fusion before/after | No guarantee or significance claim. | Verified |
| The weakest result is retained. | -0.0011571521 annualised return; -0.0058965098 Sharpe | `equity_equal_weight__evidence_aware_finance` | Fusion before/after | Poor performance is not an implementation defect. | Verified |
| Reliability scaling is more selective. | Active tilts 50.1111% vs 74.6667%; lower turnover in 8/8 | diagnostic variant rows and comparison rows | Turnover trade-off | Reliability is not truth or quality. | Verified |
| Selectivity weakened these results. | Evidence-aware return and Sharpe below naive Finance in 8/8 | paired comparison rows | Turnover trade-off | Frozen formula/sample only. | Verified |
| Crypto outcomes require risk context. | Base maximum drawdowns range -74.1993% to -81.5802% | `performance_metrics.csv`, Crypto rows | Growth/risk-return; performance table | High return does not negate severe drawdown. | Verified |
| Lag boundary is reconciled without look-ahead. | 34,789 usable vs 34,788 lagged; one final-boundary signal | diagnostics and ticker-day immediate-prior mapping | Methodology/appendix | Boundary loss is expected from one-day lag. | Verified |

## 10. Visual design system

- White/light background, restrained horizontal grids, no 3D, gradients, dual axes, or truncated delta baselines.
- Colour-blind-conscious method palette: Equal Weight grey, Minimum Variance blue, Maximum Sharpe orange, Risk Parity green.
- Overlay palette/markers: Base charcoal solid, Plain blue dashed/circle, Finance orange solid/square, Evidence-aware teal dash-dot/diamond.
- DejaVu Sans family for environment portability; consistent title/subtitle hierarchy.
- Percentage or basis-point units for small differences; technical decimals only when needed for reconciliation.
- Zero references on drawdown and delta plots; line style/marker reinforces colour.
- All PNGs are 300 DPI and at least 3,600 pixels wide, suitable for Word/PDF insertion.

## 11. Main-report versus appendix placement

Suggested main-report evidence, subject to the ten-page narrative constraint and student judgement:

- `fund_growth_comparison.png`
- `fund_risk_return_map.png`
- `sector_sentiment_timeseries.png`
- `fusion_before_after.png`
- `sentiment_innovation_diagnostics.png`

Suggested appendix/supporting evidence:

- `combined_drawdowns.png` if page space requires (otherwise retain in the main risk discussion)
- `combined_weights_over_time.png`
- `fusion_turnover_tradeoff.png` if the main report already contains both innovation exhibits; otherwise it is a strong main innovation/limitation exhibit
- Complete base and 24-overlay metric tables, solver diagnostics, and extreme-sensitivity table

Placement does not authorise omission: every required exhibit and all unfavourable numerical evidence must remain accessible in the hand-in/app materials.

## 12. Deferred matters and student decisions

- Student review of every figure, evidence bullet, caveat, and proposed placement.
- Selection of which exhibits fit the main ten-page narrative versus appendix, while retaining all brief-required exhibits.
- Student-authored economic interpretation, three recommendations, and limitations in the student's own analytical voice.
- Fact-sheet design, Streamlit integration, report drafting, citations, deployment, publication, and submission packaging.
- No further model, parameter, robustness, or significance-test work is authorised by this design.

`Pending student review — frozen models and canonical analytical outputs were not changed.`

## Stage 7 visual review — Correction Cycle 1

**Date:** 2026-08-14  
**Review status:** `Pending student review`

ChatGPT independently reviewed all eight rendered Stage 7 figures and found no analytical blocker. Before student acceptance, it requested four presentation-only corrections for HD report use. Codex implemented and visually verified them without changing a frozen model, parameter, canonical CSV, calculation, result, or sample.

### Corrected visual contracts

1. **Sentiment innovation diagnostics**
   - The subtitle now states unambiguously that exposure to reviewed terms is **not** contextual accuracy.
   - The custom-term threshold uses the polished `≥1` symbol.
   - A two-line source note explains that the higher Finance-VADER exact-zero/neutral-band rate partly reflects intentional neutralisation of generic finance words with inappropriate vanilla polarity and does not imply lower information coverage.

2. **Combined weights through time**
   - The former global top-eight-plus-Other display was replaced with the six equity tickers having the highest mean target weight across all Combined funds, plus `Crypto sleeve` and `Other equities`.
   - The deterministic equities are `MRK`, `WMT`, `ABBV`, `PSA`, `GILD`, and `KO`.
   - `Crypto sleeve` sums all ten frozen crypto tickers; `Other equities` sums the remaining 44 equities. Every method-date stack reconciles to one without omission or renormalisation.

3. **Fusion turnover trade-off**
   - Raw overlay IDs were replaced by `Equity Maximum Sharpe + Finance VADER` and `Equity Equal Weight + Evidence-aware Finance`.
   - Their signed Sharpe deltas, `+0.0192` and `-0.0059`, are displayed.
   - The x-axis now reads `Incremental average rebalance turnover vs base (percentage points)`.
   - The evidence-aware callout states: `Lower incremental turnover, but lower Sharpe than naive Finance in all 8 paired comparisons.`

4. **Fund growth comparison**
   - Equity, Crypto, and Combined panels now use honest family-specific y-ranges rather than an unnecessary zero baseline.
   - Each panel retains all observations and displays a dashed `$1` reference.
   - The subtitle and source note disclose panel-specific scales, separate family dates, and net-of-cost status.

### Validation and visual QA

- Final unchanged builder rerun: `PASS=58 WARN=3 BLOCK=0`.
- Focused exhibit tests: `9 passed in 7.20s`.
- Direct inspection of the four final 300-DPI images confirmed readable labels and legends, complete notes, visible references, honest scales, clear aggregation, and no clipped or empty panel.
- An intermediate visual inspection found the new diagnostics note extending beyond the right edge; it was wrapped to two lines and re-inspected. This was a presentation correction only.
- Four unaffected figure hashes remained unchanged. The four corrected figures received new deterministic hashes, recorded in the chronological AI audit.

`Stage 7 Visual Correction Cycle 1 completed; pending student review. No analytical method or result changed.`
