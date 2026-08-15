# Stage 7 — Independent Results Audit, Canonical Exhibit Generation, and Report-Evidence Design

**Date:** 2026-08-14  
**Status:** `Pending student review`

## Objective and authority

The objective was to audit the frozen Stage 5A/6C outputs independently, reconcile report-facing claims to daily/path-level evidence, and generate eight deterministic canonical PNG exhibits. The stage did not authorise model execution, parameter changes, selective filtering, report prose, application work, deployment, publication, submission, or Git operations.

The student stated exactly:

> “I have reviewed and accept the implementation of Stage 6C, all 24 complete results and audit records. I accept both favourable and unfavourable outcomes and confirm no ex-post parameter tuning is permitted. Stage 6C accepted and closed. The next stage is authorised to conduct result auditing and design figures and supporting evidence for the report; no authorisation is granted to modify the frozen models or parameters.”

This statement was appended chronologically to `ai/09_sentiment_fusion_implementation.md`. Stage 6C is closed; Stage 7 is limited to the audit and exhibit work recorded here.

## Roles and provenance

- **Student:** accepted Stage 6C, authorised the Stage 7 boundary, retains final authority over interpretation, exhibit selection, report authorship, and any later stage.
- **ChatGPT:** independently reviewed the Stage 6C audit log and three summary CSVs, checked their schemas, hashes, 24-row coverage, arithmetic identities, base-delta consistency, and headline diagnostic ratios, identified the innovation/trade-off interpretation, and presented the acceptance wording. ChatGPT did not independently inspect the full local daily-return and weight paths.
- **Codex:** verified the exact local workspace, read the governing materials, hashed the frozen evidence, independently reconciled daily/path-level results, implemented CSV-only reporting helpers and tests, generated and visually inspected the eight exhibits, recorded genuine corrections, and performed the boundary audit.

AI-generated interpretations remain evidence suggestions, not the student's report prose. Student review is pending.

## Complete operational prompt

<details>
<summary>Verbatim Stage 7 prompt received by Codex</summary>

```text
You are working on FINS5545 Project B.

This is Workflow Stage 7 only: Independent Results Audit, Canonical Exhibit Generation, and Report-Evidence Design.

Work efficiently. Do not split this into unnecessary micro-stages, repeatedly reread unchanged files, or rerun expensive model pipelines. Use one pre-edit manifest, one final manifest, and concise progress updates. Ask no question unless a genuine BLOCK or authority conflict occurs.

## 1. Student acceptance and authority

The student states exactly:

“I have reviewed and accept the implementation of Stage 6C, all 24 complete results and audit records. I accept both favourable and unfavourable outcomes and confirm no ex-post parameter tuning is permitted. Stage 6C accepted and closed. The next stage is authorised to conduct result auditing and design figures and supporting evidence for the report; no authorisation is granted to modify the frozen models or parameters.”

Record that quotation verbatim at the chronological end of:

`ai/09_sentiment_fusion_implementation.md`

This closes Stage 6C and authorises Stage 7 only.

Interpret “design figures and supporting evidence” as permission to audit existing canonical outputs and generate reproducible report-facing figures from those frozen outputs. It does not authorise recomputing, modifying, replacing, tuning, or selectively filtering any model result.

## 2. Workspace and environment guard

Before reading project contents:

1. Confirm the resolved PyCharm project root and terminal working directory both equal exactly:

`C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`

2. Use only:

`C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`

3. Do not create another environment or install, remove, or upgrade a dependency.

4. Do not inspect Project A, sibling folders, the broader repository, another student’s work, or Git history.

5. Do not access external sources or download data. If an existing validator requires the official loader, use only the unchanged protected loader and its existing official URLs.

Stop before reading or editing project content if the workspace guard fails.

## 3. Exact authorised file boundary

After the guard, capture one pre-edit SHA-256 manifest of Project B, including `.idea`.

Authorised modification:

* append only `ai/09_sentiment_fusion_implementation.md`.

Authorised new implementation/documentation files:

* `src/reporting.py`
* `scripts/build_report_exhibits.py`
* `tests/test_report_exhibits.py`
* `docs/results_audit_and_exhibit_design.md`
* `ai/10_results_audit_and_exhibit_generation.md`

Authorised new figures:

* `results/figures/fund_growth_comparison.png`
* `results/figures/combined_drawdowns.png`
* `results/figures/combined_weights_over_time.png`
* `results/figures/fund_risk_return_map.png`
* `results/figures/sector_sentiment_timeseries.png`
* `results/figures/fusion_before_after.png`
* `results/figures/sentiment_innovation_diagnostics.png`
* `results/figures/fusion_turnover_tradeoff.png`

Confirm every new target is absent before implementation. Stop on a collision.

No other file may be modified or created. In particular, do not modify:

* frozen data, portfolio, sentiment, fusion, ETL, feature, or validation logic;
* any existing CSV under `results/`;
* existing tests;
* `streamlit_app.py`;
* report Word, PDF, or Markdown prose;
* requirements;
* governance contracts;
* model parameters, thresholds, lexicon entries, lag rules, lambda, constraints, transaction costs, universes, samples, schemas, or output inclusion rules.

Do not perform Git, deployment, publication, or submission operations.

If `.idea/workspace.xml` changes independently while PyCharm is open, inspect it read-only, disclose it separately, and do not restore or normalise it. Any other unexpected change is a BLOCK.

## 4. Required reading

Read completely:

* `AGENTS.md`
* the Part B requirements, common mistakes, required exhibits, rubric, AI policy, and technical requirements in `PROJECT_BRIEF.md`
* `context/verify_ai_output.md`
* `docs/data_contract.md`
* `docs/portfolio_backtest_design.md`
* `docs/sentiment_innovation_design.md`
* `docs/finance_lexicon_review.md`
* the final evidence/status sections of the accepted data, portfolio, lexicon, and Stage 6C audit records
* current reporting-relevant output schemas and existing validation scripts

Read these frozen canonical outputs as immutable evidence:

Portfolio:

* `results/data/fund_returns.csv`
* `results/data/fund_weights.csv`
* `results/tables/performance_metrics.csv`
* `results/tables/portfolio_solver_diagnostics.csv`
* `results/tables/extreme_sensitivity_metrics.csv`

Sentiment/fusion:

* `results/data/ticker_sentiment_daily.csv`
* `results/data/sector_sentiment_index.csv`
* `results/data/fusion_returns.csv`
* `results/data/fusion_weights.csv`
* `results/tables/finance_lexicon.csv`
* `results/tables/sentiment_diagnostics.csv`
* `results/tables/fusion_performance_metrics.csv`
* `results/tables/fusion_comparison.csv`

Record SHA-256 hashes for all thirteen frozen canonical outputs before audit. Do not rewrite them.

## 5. Independent result-audit gate

Before generating any figure, independently recompute from the frozen daily return and weight outputs wherever possible.

Do not merely repeat Stage 6C’s summary.

Verify:

### Portfolio results

* expected fund universe, families, methods, dates, observations, annualisation factors and unique keys;
* growth of $1 from daily net returns;
* annualised return;
* annualised volatility;
* zero-risk-free-rate Sharpe ratio;
* maximum drawdown;
* monthly rebalance schedule;
* target-weight sums, long-only bounds, caps and solver status;
* turnover and 5-bps transaction costs;
* correct equity/crypto calendar treatment;
* extreme-observation sensitivity evidence;
* reported metrics reconcile to daily paths within numerical tolerance.

### Sentiment and fusion

* 146,836 cleaned headlines;
* 146,830 mapped/scored headlines;
* exactly six disclosed endpoint-unmapped exclusions;
* 50,300 ticker-days and 10,060 sector-days;
* 12,338 no-news ticker-days and 37,962 news-bearing ticker-days;
* exact 23-row operational finance lexicon and exclusion of the four ETF-flow terms;
* no-news remains distinct from neutral sentiment;
* plain VADER remains isolated from the customised lexicon;
* every active trading signal uses a strictly earlier source date;
* no current-date or future information;
* no unauthorised carry-forward;
* the one-row difference between usable-signal count and lagged-signal count is reconciled as a boundary consequence of the one-trading-day lag, not look-ahead;
* exactly 24 overlays: eight eligible base funds × three frozen variants;
* no Crypto-only sentiment overlay;
* all weak and negative outcomes retained;
* Combined crypto sleeve unchanged;
* Combined equity sleeve preserved before the authorised tilt;
* weights, projection, turnover, costs, gross/net returns and all base deltas reconcile.

### Expected result benchmarks

Recompute rather than hard-code these. If independently measured values materially disagree, stop before figure creation.

Expected summary relationships:

* Finance VADER has a positive Sharpe delta versus the frozen base in 5 of 8 eligible funds.
* Plain VADER has a positive Sharpe delta in 4 of 8.
* Evidence-aware finance has a positive Sharpe delta in 4 of 8.
* Finance VADER has higher Sharpe than plain VADER in 6 of 8 comparisons.
* Finance VADER has higher annualised return than plain VADER in 7 of 8 comparisons.
* Evidence-aware finance has lower average rebalance turnover than naive Finance VADER in all 8 comparisons.
* Evidence-aware finance has lower annualised return and Sharpe than naive Finance VADER in all 8 comparisons.
* Best base-relative result: `equity_maximum_sharpe__finance_vader_naive`, approximately +0.0034188 annualised return and +0.0191935 Sharpe.
* Weakest base-relative result: `equity_equal_weight__evidence_aware_finance`, approximately −0.0011572 annualised return and −0.0058965 Sharpe.
* Overall custom-finance-term hit share is approximately 12.8053%.
* Finance scoring changes approximately 12.7760% of mapped headline scores.
* Utilities and Energy have unusually high custom-term hit shares and must be disclosed as sector-concentration/context risks.
* Evidence-aware active-tilt frequency is approximately 50.11%, versus approximately 74.67% for each naive variant.

Treat minor floating-point differences as tolerance-level differences. A definition, population, direction, date, count, key, lag, or material metric discrepancy is a BLOCK.

Do not add a new significance test, confidence interval, bootstrap, sample split, alternative parameter, or robustness specification after observing results. The absence of a prespecified significance test is a limitation, not permission for ex-post testing.

## 6. Required interpretation boundaries

Freeze the following distinction:

### Verified findings

* The student-reviewed finance lexicon materially changes headline scoring.
* Finance VADER performs better than plain VADER in most, but not all, paired comparisons.
* Finance VADER does not improve every fund.
* The reliability layer reduces signal activity and turnover.
* The reliability layer also weakens performance relative to naive Finance VADER across all eight eligible bases.
* Transaction costs are included.
* No result was selectively omitted.

### Permitted interpretation

The evidence supports a transparent finance-domain lexicon as the strongest of the tested sentiment extensions. The evidence-aware mechanism reveals a genuine selectivity-versus-signal-strength trade-off.

### Prohibited claims

Do not claim:

* statistical significance;
* causality;
* guaranteed investor benefit;
* universal outperformance;
* robustness beyond the frozen sample and specification;
* that reliability measures truth or news quality;
* that a neutral VADER score means no information;
* that the innovation “proves” market predictability;
* that the finance lexicon is universally valid.

Describe all comparisons as descriptive out-of-sample evidence under the frozen design.

## 7. Reporting implementation

Create `src/reporting.py` with pure plotting and reporting helpers that:

* read no raw data;
* mutate no input frame;
* use only the frozen canonical CSVs;
* return Matplotlib figure objects or deterministic derived frames;
* contain no model, optimiser, VADER, lexicon, lag, or fusion calculation;
* use no network;
* use no `plt.show()`;
* close figures after saving;
* fail clearly on a missing column, duplicate key, non-finite plotted value, or unsupported category.

Create `scripts/build_report_exhibits.py` that:

1. validates required input schemas and hashes;
2. performs the independent audit;
3. blocks all figure writes if the audit has any BLOCK;
4. builds all eight figures in a staging directory outside Project B;
5. validates every staged figure;
6. atomically places only the eight authorised PNGs after all checks pass;
7. prints machine-readable `PASS/WARN/BLOCK` totals;
8. exits non-zero on BLOCK.

The script must not run `scripts/run_part_b.py`, VADER, a portfolio optimiser, or any model pipeline.

## 8. Custom visual system

Use an original, coherent, professional investment-research style—not the starter template.

Minimum rules:

* white or very light background;
* colour-blind-conscious palette;
* consistent fonts available in the environment;
* clear hierarchy and restrained gridlines;
* no 3D;
* no dual axes;
* no decorative gradients;
* no misleading truncated axes;
* delta bars include a visible zero line;
* units and date range stated;
* line styles and markers reinforce colour distinctions;
* captions/titles state only what the evidence supports;
* minimum 300 DPI;
* readable when inserted into a Word/PDF report;
* consistent figure dimensions and naming;
* sensible precision: percentages/basis points for small return differences, decimals only where technically necessary.

Recommended method palette:

* Equal Weight: neutral grey
* Minimum Variance: blue
* Maximum Sharpe: orange
* Risk Parity: green

Recommended overlay encoding:

* Base: dark charcoal solid
* Plain VADER: blue dashed
* Finance VADER: orange solid
* Evidence-aware Finance: teal dash-dot

Where method and overlay appear together, use colour for method and line style/marker for variant so encodings do not conflict.

## 9. Eight canonical figures

### 1. `fund_growth_comparison.png`

* Required growth-of-$1 exhibit.
* Use frozen base `fund_returns.csv`.
* Small multiples by family, with all methods displayed consistently.
* Use net returns.
* Include first live date, final date, “Growth of $1”, and transaction-cost status.
* Avoid an unreadable single panel.

### 2. `combined_drawdowns.png`

* Required drawdown exhibit.
* Use all frozen Combined base methods, chosen because Combined is the required investable product rather than because it won ex post.
* Recompute drawdown from daily net return paths.
* Use percentage units and a zero reference.

### 3. `combined_weights_over_time.png`

* Required weights-over-time exhibit.
* Show the Combined family across the frozen methods in small multiples.
* If the full asset set is unreadable, use a deterministic rule fixed before plotting: the eight assets with highest time-averaged target weight across the displayed Combined funds, with every remaining asset aggregated as “Other”.
* State that aggregation explicitly.
* Do not omit or renormalise weights silently.

### 4. `fund_risk_return_map.png`

* Required cross-fund comparison.
* Plot annualised volatility against annualised net return for all frozen base funds.
* Encode family and method clearly.
* Label funds without severe overlap.
* Include Sharpe information through annotation, marker size, or a clearly described secondary visual encoding—not a second axis.

### 5. `sector_sentiment_timeseries.png`

* Required standalone sector-sentiment time series.
* Show all ten sectors using readable small multiples with common y-scale and zero reference.
* Use the frozen Finance VADER sector index as the primary series.
* A clearly labelled 21-trading-day rolling mean may be added solely for visual readability while retaining the underlying daily series faintly.
* State that smoothing is visual only and never used for trading.

### 6. `fusion_before_after.png`

* Required base-versus-sentiment figure.
* Show all eight eligible base funds and all three variants.
* Use two aligned panels: annualised-return delta in basis points and Sharpe delta.
* Every value is overlay minus corresponding frozen base.
* Include zero lines and retain negative outcomes.
* Do not rank or hide funds selectively.

### 7. `sentiment_innovation_diagnostics.png`

Create an innovation-evidence figure with:

* plain versus finance exact-zero and neutral-band rates;
* overall custom-term hit share and changed-score share;
* sector-level custom-term hit share;
* visible annotation that sector hit rate measures exposure to reviewed terms, not sentiment accuracy.

Call out the high Utilities and Energy exposure without declaring it erroneous.

### 8. `fusion_turnover_tradeoff.png`

* Plot change in average rebalance turnover against change in Sharpe for all 24 overlays.
* Encode the three variants consistently.
* Include zero reference lines.
* Annotate only the strongest positive and strongest negative observations plus the evidence-aware cluster if needed.
* The purpose is to show the selectivity/turnover/performance trade-off—not to claim an efficient frontier or causality.

## 10. Exhibit and claim specification

Create `docs/results_audit_and_exhibit_design.md` containing:

1. review status: `Pending student review`;
2. Stage 6C authority and closure;
3. audited input inventory and hashes;
4. methodology and calculation reconciliation;
5. any genuine discrepancies or warnings;
6. exact audit findings;
7. distinction between verified result, interpretation, and limitation;
8. required-exhibit coverage matrix;
9. one specification for each figure:

   * filename;
   * rubric/brief requirement;
   * question answered;
   * exact source file and fields;
   * population and sample;
   * visual form;
   * encodings;
   * units;
   * key annotation;
   * required caveat;
   * proposed report section;
   * proposed Streamlit use;
10. report evidence matrix:

* proposed claim;
* exact supporting number;
* source file and key;
* exhibit/table;
* caveat;
* verification status;

11. visual design system;
12. appendix-versus-main-report placement;
13. matters deferred to report writing and app implementation.

Do not write report paragraphs for the student. Provide evidence bullets and interpretation boundaries so the student retains authorship of the written economic interpretation.

The design must cover every required Part B exhibit and clearly identify the two custom innovation exhibits.

## 11. Tests and visual QA

Create `tests/test_report_exhibits.py` covering:

* immutable source hashes;
* required input schemas;
* unique keys;
* exact expected fund/overlay coverage;
* metric reconciliation;
* no-look-ahead source dates;
* all eight filenames;
* non-empty files;
* PNG validity;
* consistent dimensions where appropriate;
* minimum resolution and DPI;
* no blank or near-blank render;
* deterministic rebuild hashes;
* figure title/axis/unit metadata supplied by the reporting functions;
* no canonical CSV modified.

Render and visually inspect all eight figures. Check:

* clipped labels;
* unreadable legends;
* overlapping annotations;
* inconsistent scales;
* misleading axes;
* missing units/date range;
* excessive precision;
* poor contrast;
* empty panels;
* visual claims that exceed the evidence.

If direct image inspection is unavailable, state that honestly and require student visual inspection; do not invent that visual QA occurred.

## 12. Commands

Use the exact shared interpreter and `-B`.

Do not rerun the model pipeline.

Run only what is needed:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_sentiment_fusion.py
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/build_report_exhibits.py
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_report_exhibits.py
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

If the existing validator encounters only a restricted-network failure through the unchanged official loader, one identical authorised-network retry is permitted. Do not alter URLs, data, code, or parameters to make it pass.

Run the exhibit builder a second unchanged time only to verify deterministic figure hashes. Do not repeat other successful commands.

Expected checker wording may still include only the unfinished report reminder. Treat checker success as mechanical evidence, not completion.

## 13. AI provenance

Create `ai/10_results_audit_and_exhibit_generation.md`.

Record:

* date and status;
* exact student acceptance quotation;
* authority and prohibited work;
* ChatGPT’s role;
* Codex’s role;
* student’s final authority;
* complete operational prompt verbatim;
* files read;
* frozen input hashes;
* audit methods;
* independently recomputed findings;
* all commands and exact exit codes;
* every genuine error, false positive, correction, warning and limitation;
* figure specifications and generated hashes;
* visual QA actually performed;
* deterministic rerun evidence;
* checker output;
* pre/post manifest;
* separately disclosed IDE metadata;
* confirmation that frozen CSVs, models and parameters remained unchanged.

Record ChatGPT’s role accurately:

ChatGPT independently reviewed the Stage 6C audit log and three summary CSVs, checked their schemas, hashes, 24-row coverage, arithmetic identities, base-delta consistency and headline diagnostic ratios, identified the innovation/trade-off interpretation, and presented the acceptance wording. It did not independently inspect the user’s full local daily-return and weight files; Codex must perform that path-level verification in Stage 7.

Do not describe AI-generated interpretation as the student’s own writing. Student review remains pending.

## 14. Final boundary audit and response

After all work:

1. confirm the thirteen frozen canonical CSV hashes are unchanged;
2. compare the final manifest with the pre-edit manifest;
3. confirm exactly one authorised file was modified;
4. confirm exactly five authorised implementation/documentation files and eight figures were added;
5. confirm nothing was removed;
6. report any independent `.idea/workspace.xml` change separately;
7. confirm no cache, bytecode, raw data, environment, temporary project script, report, app, deployment, publication, or Git artifact appeared.

The final response must concisely report:

* workspace;
* Stage 6C closure;
* audit result and confidence;
* any BLOCK/WARN findings;
* verified headline results;
* all eight figures and their purpose;
* visual QA result;
* commands and exit codes;
* deterministic hashes;
* files changed/created;
* boundary audit;
* limitations;
* exact pending-review status.

End exactly:

`Stage 7 results independently audited and canonical report exhibits generated; pending student review. Frozen models, parameters, and canonical analytical outputs remained unchanged. No report prose, app, deployment, publication, submission, or Git work was authorised or commenced.`
```

</details>

## Workspace and environment guard

- Resolved project root: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Terminal working directory: the same exact path.
- Interpreter: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`
- Python: 3.13.13, existing shared virtual environment.
- No environment or dependency was created, installed, removed, or upgraded.
- No Project A, sibling folder, broader-repository file, other student's work, Git history, or external source was inspected.

## Files read

- `AGENTS.md`
- Relevant Part B, common-mistake, exhibit, rubric, AI, and technical sections of `PROJECT_BRIEF.md`
- `context/verify_ai_output.md`
- `docs/data_contract.md`
- `docs/portfolio_backtest_design.md`
- `docs/sentiment_innovation_design.md`
- `docs/finance_lexicon_review.md`
- Final evidence/status sections of the accepted data-foundation, portfolio, lexicon, and Stage 6C AI records
- Reporting-relevant schemas and `src/portfolio_validation.py`, `src/sentiment_validation.py`
- `scripts/validate_portfolios.py`, `scripts/validate_sentiment_fusion.py`, and `scripts/check_handin.py`
- The thirteen immutable canonical CSVs listed below

## Pre-edit manifest and frozen hashes

The pre-edit SHA-256 manifest included `.idea`, excluded `.git`, environments, caches, and bytecode, and was held outside the project working files.

- File count: **76**
- Manifest digest: `80CEFE3668DD08D32638E501E6DC51AFBDDDDE682657471DFEDF47D14C7E36E6`
- `.idea/workspace.xml`: 8,223 bytes; `4AD5F2898A59666D28858279505797447E01364D4A13A16381932B8DC0CB27E8`
- All thirteen authorised new targets were absent.

| Frozen file | SHA-256 |
|---|---|
| `results/data/fund_returns.csv` | `7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84` |
| `results/data/fund_weights.csv` | `F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8` |
| `results/tables/performance_metrics.csv` | `5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19` |
| `results/tables/portfolio_solver_diagnostics.csv` | `ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C` |
| `results/tables/extreme_sensitivity_metrics.csv` | `40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151` |
| `results/data/ticker_sentiment_daily.csv` | `CC9DDF834EF43B9B07240A40949716BA573A14E6ADDCD1997DFF83C125E26FCD` |
| `results/data/sector_sentiment_index.csv` | `D7670369187E3FF6909A88F6459204284A45D07941DC395CE239D8E304E8E96E` |
| `results/data/fusion_returns.csv` | `5A868D15E4D649FEDCB7BF9A0D58657F1729D6F35A2A62A2DF148622EA8CEBC5` |
| `results/data/fusion_weights.csv` | `13941551A0D3D9A07290235CCEF7C8AB389D2F78EAF36D81CE661A915F485058` |
| `results/tables/finance_lexicon.csv` | `5E6EE31DADC6C754DD465E825FBA5F25B3BD26E5E0AA846B3A578619D444C5DB` |
| `results/tables/sentiment_diagnostics.csv` | `3C7842ED0F955DCA29E1E728EFD51C46AA12D4B93999DC9C72D47C436AC179B5` |
| `results/tables/fusion_performance_metrics.csv` | `B75FA251E385E3709D3EC1380367D0257285D249AF742965C8FD993FCA770A07` |
| `results/tables/fusion_comparison.csv` | `B51DF470AEAB5932356037DF72FCF0044729C6F9F88C117E6C4B90F4922C3946` |

## Implementation and independent audit

Created:

- `src/reporting.py`: frozen-hash/schema contracts, independent path-level audit routines, deterministic derived frames, and pure Matplotlib figure constructors. It has no loader, VADER, optimiser, model pipeline, network call, or `plt.show()`.
- `scripts/build_report_exhibits.py`: validates hashes and schemas; runs the independent audit; stages all images outside Project B; validates PNG resolution/DPI/content; atomically commits the complete eight-file set only after zero BLOCKs.
- `tests/test_report_exhibits.py`: independent schema/key/hash/metric/lag/coverage/PNG/determinism/source-immutability tests.
- `docs/results_audit_and_exhibit_design.md`: evidence inventory, findings, interpretation boundaries, exhibit specifications, and report-evidence matrix.

The audit independently recomputed growth, annualised return, volatility, Sharpe, maximum drawdown, schedules, weight/cost arithmetic, headline/panel reconciliation, sector aggregation, lag source dates, Combined sleeve preservation, overlay metrics, and base deltas from the frozen CSVs. It did not run or reproduce model estimation.

## Independently measured findings

- 12 base funds; Equity/Combined 753 observations from 2021-01-04 to 2023-12-29 at 252; Crypto 1,095 observations from 2021-01-01 to 2023-12-31 at 365.
- 146,836 cleaned = 146,830 mapped/scored + six endpoint-unmapped headlines.
- 50,300 ticker-days = 37,962 news-bearing + 12,338 no-news; 10,060 sector-days.
- 23 operational terms; all four ETF-flow exclusions absent.
- 34,789 usable current-date signals and 34,788 lagged signals; the one-row difference is the final-date boundary after the mandatory one-trading-day lag.
- 24 complete overlays; eight base funds x three variants; no Crypto-only overlay.
- Positive Sharpe deltas: Plain 4/8, Finance 5/8, Evidence-aware 4/8.
- Finance exceeds Plain in Sharpe 6/8 and annualised return 7/8.
- Evidence-aware has lower turnover than naive Finance 8/8, but lower return and Sharpe 8/8.
- Best delta: `equity_maximum_sharpe__finance_vader_naive`, +0.0034188173 annualised return and +0.0191935447 Sharpe.
- Weakest delta: `equity_equal_weight__evidence_aware_finance`, -0.0011571521 annualised return and -0.0058965098 Sharpe.
- Custom-term hit share 18,802 / 146,830 = 12.805285%; changed-score share 18,759 / 146,830 = 12.775999%.
- Utilities custom-term exposure 40.085457% and Energy 21.972631%, versus 12.805285% overall; disclosed as context/concentration risk rather than accuracy or error.
- Reliability: n=37,962, mean 0.243373, SD 0.216862, median 0.250000, q90 0.500000, range 0--0.937500.
- Active-tilt frequency: 74.6667% for each naive variant and 50.1111% for Evidence-aware.

## Commands, outputs, and exit codes

All Python commands used `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe` with `-B`; pytest cache was disabled. PyCharm's configured environment was rechecked before each Python invocation.

### Accepted Stage 6C validator

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_sentiment_fusion.py
```

The first sandboxed attempt exited **1** with a local `PermissionError` while reading the existing `sector_sentiment_index.csv`; this was an execution-permission restriction, not a data or model discrepancy. The identical authorised retry exited **0**:

```text
Sentiment/fusion output validation: PASS=56 WARN=2 BLOCK=0
WARN lexicon_context_limit: Lexicon coverage does not prove contextual accuracy; all weak results remain reportable.
WARN evidence_reliability_limit: Directional agreement, volume, and coverage are evidence diagnostics rather than truth or causality.
SENTIMENT/FUSION OUTPUT STATUS: PASS
```

The command also emitted benign Streamlit no-runtime-context warnings; no app was run or changed.

### Exhibit builder history

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/build_report_exhibits.py
```

First run exited **1** before any figure write:

```text
Report exhibit audit: PASS=53 WARN=3 BLOCK=1
BLOCK sector_aggregation: Sector aggregation, coverage, or display mapping does not reconcile.
REPORT EXHIBIT STATUS: BLOCK
```

The defect was in the new audit representation: a sector-day absent from grouped news had expected count/coverage `NaN` while the frozen complete panel correctly publishes zero. Filling only the audit's expected count/coverage with zero implemented the contract; no canonical file, method, or result changed.

The corrected build exited **0** with `PASS=57 WARN=3 BLOCK=0` and generated all eight staged/validated figures atomically.

Direct visual inspection then found overlapping labels in the risk-return map. Fixed fund-specific label offsets and leader lines were added. No data value, sample, axis, or analytical result changed.

The first post-revision build exited **1** before changing an output because the new deterministic-build predicate treated the intentional reporting-code revision as nondeterminism:

```text
Report exhibit audit: PASS=56 WARN=3 BLOCK=2
BLOCK deterministic_rebuild: At least one unchanged figure rebuild hash differs.
BLOCK figure_generation: Figure generation/commit failed: RuntimeError: staged audit produced a BLOCK
REPORT EXHIBIT STATUS: BLOCK
```

The predicate was corrected to warn on an expected visual-code revision and reserve deterministic failure for a subsequent unchanged rebuild. This changed neither a model nor evidence. The revision build then exited **0** with `PASS=57 WARN=4 BLOCK=0`.

The required immediate unchanged rebuild exited **0**:

```text
Report exhibit audit: PASS=58 WARN=3 BLOCK=0
WARN plain_analyzer_runtime_boundary: Plain-analyzer isolation passed the accepted Stage 7 validator, but analyzer state is not inferable from CSVs alone; the independent exhibit audit checks lexicon content and score-path evidence only.
WARN extreme_event_limit: The +/-25% scenario reconciles mechanically, but frozen CSVs cannot economically validate the 69 underlying market moves.
WARN descriptive_inference_only: No significance test was prespecified; all comparisons remain descriptive OOS evidence under the frozen sample and specification.
Headline reconciliation: cleaned=146836 mapped=146830 unmapped=6
Paired Sharpe improvements: plain=4/8 finance=5/8 evidence-aware=4/8
Best base-relative overlay: equity_maximum_sharpe__finance_vader_naive
Weakest base-relative overlay: equity_equal_weight__evidence_aware_finance
REPORT EXHIBIT STATUS: PASS
```

### Focused tests

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_report_exhibits.py
```

Exit **0**:

```text
........                                                                 [100%]
8 passed in 6.65s
```

### Hand-in checker

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exit **0**:

```text
22 checks passed.
1 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
All checks passed - ready to zip and deploy.
```

This is mechanical checker evidence only. The report, application, deployment, publication, and submission remain incomplete and unauthorised in Stage 7.

## Canonical figure evidence and deterministic hashes

| Figure | Purpose | Pixels | Bytes | SHA-256 |
|---|---|---:|---:|---|
| `fund_growth_comparison.png` | Growth of $1 for all 12 base funds in family small multiples | 3600x3000 | 864,999 | `9CEECFAC66C7842710CC9B2A37B2E3007D85920152194AA8B43D3F200FBA1BAB` |
| `combined_drawdowns.png` | All Combined base-method drawdown paths | 3600x2100 | 736,304 | `DAA1415C7406098E61E250122A5B1AC11240B8858C2949A482EC453308D59C81` |
| `combined_weights_over_time.png` | Combined targets; deterministic top eight plus exact Other aggregation | 3600x2700 | 425,784 | `984F9D8AED831D6D6F3B7F0A46FBD0692FE10394F8BE6493F0811AB2A7FC1A68` |
| `fund_risk_return_map.png` | All base funds' annualised risk, net return, Sharpe, family, and method | 3600x2100 | 262,309 | `C7CF65BF38BA38214659F28D0CA84B1BD7528C1D74BCCD2B62BBDCA18BC721E8` |
| `sector_sentiment_timeseries.png` | Ten-sector Finance VADER daily and visual-only 21-day mean | 3600x4200 | 1,171,033 | `7A210A89713955EAB7C459F4C3D8044E5317D49733142A9D1B652669A6012FB7` |
| `fusion_before_after.png` | All 24 return/Sharpe deltas with negative evidence retained | 3600x2400 | 211,830 | `7789948051C8FBDA8A0E9659C066086C301D972E956465B7EB49156041A994DF` |
| `sentiment_innovation_diagnostics.png` | Zero/neutral rates, overall hit/change, and sector term exposure | 3900x2400 | 372,630 | `2BA27F54DC2D4A7E26D99D3B171A246203A91CF37402976E876BC20B50A57988` |
| `fusion_turnover_tradeoff.png` | All 24 turnover-versus-Sharpe deltas | 3600x2100 | 271,461 | `719D18E59D256050EAC6A31EACB2425E5E7560D710494F6A87322CEA39A0D61A` |

All eight hashes were identical on the immediate unchanged second builder run.

## Visual QA actually performed

All eight PNGs were copied read-only to a Windows temporary directory outside Project B and inspected directly as rendered images. Checks covered clipping, legends, annotation overlap, scale consistency, axes and units, precision, contrast, empty panels, and claim discipline.

- Growth, drawdown, weights, sector, fusion-delta, innovation-diagnostic, and turnover-trade-off figures passed first direct inspection.
- The first risk-return map had overlapping fund labels. It was revised with fixed offsets/leader lines and re-inspected; the revised labels were separated and readable.
- A first PowerShell QA-copy attempt used unsupported `New-Item -LiteralPath` syntax and copied nothing; the corrected `-Path` invocation copied the eight images outside the project. No project file changed from this tool syntax issue.
- The temporary QA directory was removed after inspection.

## Genuine errors, corrections, warnings, and limitations

1. **Local read restriction:** identical validator retry with authorised local read access; no code/data change.
2. **Sector aggregation false BLOCK:** corrected the audit-only no-news zero representation; no analytical change.
3. **Risk-map overlap:** adjusted presentation-only label placement; no result change.
4. **Over-broad deterministic predicate:** corrected reporting validation to distinguish an intentional code revision from an unchanged rerun; subsequent hashes proved determinism.
5. **PowerShell QA-copy syntax:** corrected `-LiteralPath` to supported `-Path`; no project effect.
6. **Read-only evidence command:** a sandboxed PowerShell read later accessed the small base metrics but was denied for two protected sentiment/fusion CSVs; an authorised read-only retry succeeded. No file changed.
7. **Limitations:** no prespecified significance test; CSV-only audit cannot re-observe in-memory plain-analyser isolation; reliability is not truth/news quality; 69 extremes are mechanically but not economically validated; results are limited to the frozen sample/design.

No parameter, lexicon term, sample, method, lag, reliability rule, lambda, cost, output row, or canonical CSV changed after results were observed.

## Final boundary evidence

The final SHA-256 comparison was performed after the last authored edit. Its complete manifest digest is reported in the Codex final response because embedding the hash of this log inside the log itself is self-referential. The path-level comparison confirmed:

- exactly one pre-existing authored file changed: `ai/09_sentiment_fusion_implementation.md` (append only);
- exactly five authorised implementation/documentation files were added: `src/reporting.py`, `scripts/build_report_exhibits.py`, `tests/test_report_exhibits.py`, `docs/results_audit_and_exhibit_design.md`, and this AI record;
- exactly eight authorised PNG exhibits were added;
- no file was removed;
- all thirteen canonical CSV hashes remained identical to their pre-stage values;
- no frozen model, validation, test, requirement, report, application, raw-data, environment, cache, bytecode, deployment, publication, submission, or Git artifact changed or appeared;
- `.idea/workspace.xml` was compared read-only and is disclosed separately in the final response; no IDE file was edited by Codex.

## Review status and next authority

`Pending student review`

Stage 7 evidence and figures require student review. No report prose, application, deployment, publication, submission, Git operation, or later stage is authorised by this record.

## Visual Correction Cycle 1 — ChatGPT review and HD-report corrections

**Date:** 2026-08-14  
**Status:** `Stage 7 remains pending student review`

### Review provenance and authority

The student had not accepted Stage 7. ChatGPT independently reviewed all eight rendered figures, found no analytical blocker, and required four presentation corrections for HD-quality reporting. The student authorised changes only to `src/reporting.py`, `tests/test_report_exhibits.py` where needed, append-only additions to this audit and `docs/results_audit_and_exhibit_design.md`, and the four affected PNGs. No new file or analytical change was authorised.

Codex used the existing CSV-only exhibit builder and did not run or modify any portfolio, sentiment, fusion, ETL, feature, lexicon, optimiser, or model pipeline. No canonical CSV was rewritten.

### Pre-correction boundary

- Project root and terminal working directory both resolved exactly to `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`.
- Interpreter remained `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`, Python 3.13.13.
- Pre-edit manifest: 89 files; digest `93803E57C0ADC433CFC38D97A51FDED5309D587B68E57155EE5014777DAA0C8D`.
- `.idea/workspace.xml`: `4AD5F2898A59666D28858279505797447E01364D4A13A16381932B8DC0CB27E8`.
- All thirteen frozen canonical CSV hashes matched the accepted Stage 7 inventory.

Pre-correction figure hashes:

| Figure | SHA-256 |
|---|---|
| `fund_growth_comparison.png` | `9CEECFAC66C7842710CC9B2A37B2E3007D85920152194AA8B43D3F200FBA1BAB` |
| `combined_drawdowns.png` | `DAA1415C7406098E61E250122A5B1AC11240B8858C2949A482EC453308D59C81` |
| `combined_weights_over_time.png` | `984F9D8AED831D6D6F3B7F0A46FBD0692FE10394F8BE6493F0811AB2A7FC1A68` |
| `fund_risk_return_map.png` | `C7CF65BF38BA38214659F28D0CA84B1BD7528C1D74BCCD2B62BBDCA18BC721E8` |
| `sector_sentiment_timeseries.png` | `7A210A89713955EAB7C459F4C3D8044E5317D49733142A9D1B652669A6012FB7` |
| `fusion_before_after.png` | `7789948051C8FBDA8A0E9659C066086C301D972E956465B7EB49156041A994DF` |
| `sentiment_innovation_diagnostics.png` | `2BA27F54DC2D4A7E26D99D3B171A246203A91CF37402976E876BC20B50A57988` |
| `fusion_turnover_tradeoff.png` | `719D18E59D256050EAC6A31EACB2425E5E7560D710494F6A87322CEA39A0D61A` |

### Exact changes

- `plot_fund_growth`: added family-specific padded y-ranges, an explicit dashed `$1` line in each panel, and visible scale/date/cost disclosure.
- `combined_weight_frame` and `plot_combined_weights`: ranked equities only, retained the six leading equities, summed all ten crypto tickers as `Crypto sleeve`, summed the remaining 44 equities as `Other equities`, and retained exact stack totals.
- `plot_sentiment_diagnostics`: clarified `not contextual accuracy`, changed the threshold to `≥1`, added the neutralisation interpretation boundary, and wrapped that note after direct QA found clipping.
- `plot_fusion_turnover_tradeoff`: added reader-facing names, signed Sharpe deltas, the authorised x-axis wording, and the exact evidence-aware trade-off statement without moving any data point or changing any scale.
- `tests/test_report_exhibits.py`: updated the deterministic aggregation contract and added tests for all four presentation rules, source immutability, stack reconciliation, and reader-facing text.
- The design document and this record were appended chronologically; earlier Stage 7 evidence was not rewritten.

### Commands, exact results, and corrections

Every Python command used the verified interpreter with `-B`; pytest cache was disabled.

Builder command, used unchanged:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/build_report_exhibits.py
```

Initial corrected build: exit **0**, `PASS=57 WARN=4 BLOCK=0`. The fourth warning was the expected `visual_revision_hash_change`. Immediate unchanged build: exit **0**, `PASS=58 WARN=3 BLOCK=0`; all eight hashes matched that first corrected build.

The first focused test attempt used:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_report_exhibits.py
```

It exited **1** with `1 failed, 8 passed`: the new test applied `np.allclose` to both the 753/1,095-point fund paths and the two-point `$1` reference, causing a shape-broadcast error. The test-only predicate was narrowed to two-point lines. No figure, result, or method changed. The rerun exited **0** with `9 passed in 7.19s`.

Direct inspection then found that the newly added diagnostics interpretation note extended beyond the canvas. Codex added a line break and reserved bottom margin. Because this changed a rendered figure, the unchanged builder was run twice again: the revision build exited **0**, `PASS=57 WARN=4 BLOCK=0`; the immediate unchanged build exited **0**, `PASS=58 WARN=3 BLOCK=0`, with identical final hashes.

The next focused test run exited **1** with `1 failed, 8 passed` because the assertion still expected `not lower information coverage`, while the approved visible wording had been refined to `does not imply lower information coverage`. Aligning that test-only literal changed no figure or evidence. The final run exited **0**:

```text
.........                                                                [100%]
9 passed in 7.20s
```

Hand-in checker command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exit **0**:

```text
22 checks passed.
1 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
All checks passed - ready to zip and deploy.
```

This remains mechanical evidence only; Stage 7 is not accepted and report/app/deployment work remains unauthorised.

### Final deterministic figure hashes

| Figure | Cycle result | SHA-256 |
|---|---|---|
| `fund_growth_comparison.png` | Corrected | `68AA156B18AACC824346C8820C1B941623FA0D13BA6627AAFB17848EF1F625BE` |
| `combined_drawdowns.png` | Unaffected, unchanged | `DAA1415C7406098E61E250122A5B1AC11240B8858C2949A482EC453308D59C81` |
| `combined_weights_over_time.png` | Corrected | `04A8B663D6C1CB29F6E9D8D7CB2A6DD16C90A1C31D9920543E6A2364CC74F1E6` |
| `fund_risk_return_map.png` | Unaffected, unchanged | `C7CF65BF38BA38214659F28D0CA84B1BD7528C1D74BCCD2B62BBDCA18BC721E8` |
| `sector_sentiment_timeseries.png` | Unaffected, unchanged | `7A210A89713955EAB7C459F4C3D8044E5317D49733142A9D1B652669A6012FB7` |
| `fusion_before_after.png` | Unaffected, unchanged | `7789948051C8FBDA8A0E9659C066086C301D972E956465B7EB49156041A994DF` |
| `sentiment_innovation_diagnostics.png` | Corrected | `1A1F2DAC8AE4330D01B6DAA19FC9D18461A55919A276AD27B12826755D2F97C8` |
| `fusion_turnover_tradeoff.png` | Corrected | `9D483E2247EE05DC8E90451F63A77F035D586BDC04137BBE1965737CA30B641B` |

### Visual QA actually performed

The project PNGs were copied read-only to a temporary Windows directory because direct image access to the protected result paths was denied. Codex inspected all four corrected final images and then deleted the temporary copies. The final inspection confirmed:

- panel-specific growth scales are proportionate, every series remains visible, and each panel includes the `$1` reference;
- weight panels preserve 100% stacks and make the Crypto sleeve explicit without omitting the residual equity sleeve;
- the diagnostics subtitle, `≥1` label, neutralisation note, and sector caveat are readable and unclipped;
- trade-off labels are reader-facing, signed deltas and callout are readable, and points/scales are unchanged.

No analytical blocker, clipped label, overlapping annotation, misleading axis, incomplete note, or empty panel remained.

### Final boundary evidence

The post-edit manifest was compared with the pre-edit manifest after the last authored edit. The full digest is reported in the Codex response because this audit file cannot contain its own final hash without self-reference. The path-level result confirmed:

- only `src/reporting.py`, `tests/test_report_exhibits.py`, `docs/results_audit_and_exhibit_design.md`, and this audit record changed as authored files;
- only the four authorised corrected PNGs changed;
- the other four PNGs remained byte-identical;
- all thirteen frozen canonical CSVs remained byte-identical;
- no file was added or removed;
- no model, parameter, analytical output, source-data artifact, cache, bytecode, environment, report, app, deployment, publication, submission, or Git artifact appeared;
- `.idea/workspace.xml` was inspected read-only and disclosed separately; Codex did not edit it.

`Stage 7 Visual Correction Cycle 1 completed; pending student review. Four reporting figures were corrected without changing any frozen model, parameter, canonical analytical output, or result.`

## Final student acceptance — Stage 7 closed

**Date:** 2026-08-14

The student visually reviewed and accepted all eight Stage 7 figures, including
the four corrected figures, and accepted the complete result audit, exhibit
design, visual corrections, limitations, and both favourable and unfavourable
results. The student specifically confirmed that the final diagnostics subtitle
reads `not contextual accuracy` and stated that no further figure correction is
required.

The student's exact relevant replies were:

> `其实没有问题，是not，我核验了`

> `looks good,lets do it`

ChatGPT assisted the student by reviewing the Project Brief, Week 10 revision
material and lecture transcript, the canonical exhibits, and the teacher's
iShares/BlackRock example. The student retained final decision authority and,
by the Stage 8 operational prompt, approved the product name **MAIA —
Multi-Asset Investment Assistant** and a separately disclosed **0.50% p.a.
illustrative management fee** for the user-facing Allocation Studio.

The Stage 7 acceptance preserves every weak and negative analytical result and
confirms that no frozen analytical output changed during the visual correction.
It authorises local Streamlit design, implementation, testing, documentation,
and student-review handoff only. It does not authorise model or parameter
changes, report writing, Git operations, deployment, publication, packaging, or
submission.

`Stage 7 accepted and closed; Stage 8 authorised only for local MAIA Streamlit implementation, validation, and student-review handoff.`
