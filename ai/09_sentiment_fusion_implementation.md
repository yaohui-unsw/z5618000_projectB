# Stage 6C — Frozen sentiment and fusion implementation

**Date:** 2026-08-14  
**Status:** Pending student review

## Objective and authority

Implement, test, validate, and generate the eight canonical sentiment/fusion outputs using only the Stage 6B-frozen lexicon and pre-result methodology. Weak, negative, and inconvenient results remain in the published output universe. Figures, report writing, Streamlit, deployment, publication, and Git operations were outside scope.

ChatGPT presented the complete Chinese Stage 6B acceptance statement. The student's only authoritative verbatim reply was:

> “我确认了，来吧！”

That reply accepted and closed Stage 6B and authorised Stage 6C only. The earlier English paraphrase was not a verbatim student quotation and is deliberately omitted from this provenance record at the student's instruction.

Before any Project B read or edit, the workspace guard passed. Codex detected apparently conflicting quotation language and stopped. The student clarified the authoritative quotation. No Project B file had been read or edited and no command, model, or output had run before that clarification. This was a quotation-provenance clarification only, not a methodological change or correction to a model.

## Roles and provenance

- **Student:** retained final authority; accepted the Stage 6B transcription, exact 23-entry lexicon, four rejections, frozen method, complete reporting rule, and Stage 6C boundary.
- **ChatGPT:** assisted with staged workflow design, reviewed the Stage 6B transcription with the student, and presented the complete Chinese acceptance statement.
- **Codex:** performed the authorised local reconciliation, implementation, tests, model execution, output validation, deterministic rerun, and boundary audit.

No AI system is credited with student approval. No return or portfolio result was used to change a lexicon value, method, threshold, sample, or reporting universe.

## Workspace, environment, resource, and pre-edit evidence

- Project root and terminal directory: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB` (exact match).
- Interpreter: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`.
- Python: 3.13.13. PyCharm reported the environment as a `venv` with `pip`.
- Existing VADER resource: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\nltk_data\sentiment\vader_lexicon.zip`.
- VADER resource was already available; no download or package/environment change occurred.
- Pre-edit manifest: 62 included Project B files; digest `265B4694B1F7EE091D1412BB0568C8D46A29A954FB7BBC01F0821546C147239A`.
- Pre-edit `.idea/workspace.xml`: 8,223 bytes; SHA-256 `4AD5F2898A59666D28858279505797447E01364D4A13A16381932B8DC0CB27E8`.
- All six authorised code/test/log targets and all eight output targets were absent before editing.

The configured-environment check was run before every Python invocation. Python commands used `-B`, and pytest disabled its cache provider.

## Files read

Codex read completely the governing and implementation evidence required by the prompt:

- `AGENTS.md`;
- relevant sentiment, fusion, innovation, AI-workflow, output, common-mistake, and rubric sections of `PROJECT_BRIEF.md`;
- `context/DATA_GUIDE.md`, `context/project_context.md`, and `context/verify_ai_output.md`;
- `docs/data_contract.md`, `docs/portfolio_backtest_design.md`, `docs/finance_lexicon_review.md`, and `docs/sentiment_innovation_design.md`;
- `ai/07_sentiment_design_and_lexicon_candidates.md` and `ai/08_student_lexicon_review_and_freeze.md`;
- all current `src/*.py` modules relevant to data, features, validation, portfolios, sentiment, and fusion;
- `scripts/run_part_b.py`, current validation scripts, and `scripts/check_handin.py`;
- every existing test;
- the five accepted Stage 5A CSVs as immutable inputs/comparison evidence.

Project A, sibling folders, broader-repository content, other students' work, report files, figures, app files, and Git internals were not inspected.

## Frozen-input reconciliation

The three governance sources reconciled after correcting three overly literal read-only predicates:

```text
FROZEN_INPUT_RECONCILIATION=PASS
CANDIDATES=27
ACCEPT=17
EDIT=6
REJECT=4
OPERATIONAL=23
REJECTED_TERMS=inflow,inflows,outflow,outflows
METHODOLOGY_AND_EIGHT_SCHEMAS=CONSISTENT
EXIT_CODE=0
```

The initial read-only attempts exited 1 because they assumed 13 rather than 12 candidate-table fields, required literal `finance VADER` rather than the documented hyphenated/case variant, and required every future output filename to be repeated in the Stage 6B provenance log. The corrected predicates tested the actual contract semantics. These changes modified no project file, student decision, method, or result.

## Frozen operational finance lexicon

Exactly these 23 entries were implemented; the decision date is `2026-08-14`.

| Term | Value | Decision | Term | Value | Decision |
|---|---:|---|---|---:|---|
| shares | 0.0 | ACCEPT | energy | 0.0 | ACCEPT |
| alert | 0.0 | ACCEPT | rally | 1.0 | ACCEPT |
| active | 0.0 | ACCEPT | beat | 1.5 | ACCEPT |
| rebound | 0.5 | EDIT | downgrades | -1.0 | EDIT |
| asset | 0.0 | ACCEPT | beats | 1.5 | ACCEPT |
| outperform | 1.0 | EDIT | miss | -1.0 | EDIT |
| overweight | 1.0 | ACCEPT | bullish | 1.5 | ACCEPT |
| slump | -1.5 | ACCEPT | misses | -1.5 | ACCEPT |
| plunge | -1.5 | ACCEPT | downgraded | -1.5 | ACCEPT |
| tumble | -1.5 | ACCEPT | underweight | -1.0 | ACCEPT |
| plunges | -1.5 | ACCEPT | underperform | -1.0 | EDIT |
| layoffs | -1.0 | EDIT |  |  |  |

Rejected and absent: `inflow`, `inflows`, `outflow`, and `outflows`. No other term was added. Zero overrides remain custom-term hits but do not count as non-zero active-lexicon coverage.

## Implementation

### `src/sentiment.py`

- isolated plain and finance VADER analyzers and verified vanilla lexicon immutability;
- exact 23-entry metadata and operational table;
- exact frozen token regex and case-normalised matching without title mutation;
- per-headline plain/finance scoring, non-zero coverage, and custom-hit flags;
- complete ticker-day aggregation with explicit no-news missingness;
- frozen reliability components and raw evidence-aware diagnostic;
- previous-252-observed-date, current-excluded, minimum-60, `ddof=1`, `std > 1e-8`, z-only clipping;
- immediate-previous-trading-date lag with no carry-forward;
- equal-weight sector aggregation and separate sector custom-hit diagnostics;
- auditable sentiment diagnostic and finance-lexicon tables.

### `src/fusion.py`

- deterministic enumeration of 24 overlays from eight Equity/Combined base funds and three variants;
- fixed `lambda = 0.10` multipliers and missing-signal multiplier one;
- deterministic Euclidean capped-simplex projection;
- Combined crypto-target identity and equity-sleeve preservation;
- exact Stage 5A inception, drift, turnover, 5-bps cost, gross/net return, and performance conventions;
- complete performance and base-delta tables; no Crypto-only overlay.

### Validation and orchestration

- `src/sentiment_validation.py`: machine-readable PASS/WARN/BLOCK checks for lexicon, schemas, counts, keys, missingness, formulas, lag, sector aggregation, overlays, projections, sleeves, source returns, drift, costs, metrics, and deltas.
- `scripts/validate_sentiment_fusion.py`: validates precomputed outputs without rerunning scoring or optimisation; source-return checks load only through the protected official pathway.
- `scripts/run_part_b.py --stage sentiment-fusion`: builds all artifacts in memory, blocks all writes on any BLOCK, stages all eight CSVs outside Project B, and replaces only the authorised destinations after successful validation. Portfolio-stage behaviour remains available and was not invoked.

## Exact output contracts

- `sector_sentiment_index.csv`: `date, sector, sector_display, headline_count, ticker_count_with_news, ticker_coverage, plain_compound, finance_compound, mean_reliability, evidence_aware_compound, plain_z, finance_z, evidence_aware_z`.
- `ticker_sentiment_daily.csv`: `date, ticker, sector, headline_count, has_news, plain_score, finance_score, covered_headline_share, nonneutral_headline_count, directional_agreement, volume_evidence, reliability, custom_finance_term_hit_share, evidence_aware_compound, plain_z, finance_z, evidence_aware_signal, signal_source_date, lagged_plain_signal, lagged_finance_signal, lagged_evidence_aware_signal`.
- `fusion_returns.csv`: `date, overlay_id, base_fund_id, family, method, variant, gross_return, turnover, transaction_cost, net_return, is_rebalance`.
- `fusion_weights.csv`: `date, overlay_id, base_fund_id, family, method, variant, ticker, base_target_weight, pretrade_weight, signal_source_date, signal_value, multiplier, raw_tilted_value, target_weight, trade_weight, turnover, projection_success, projection_status`.
- `sentiment_diagnostics.csv`: `scope, entity, model, metric, value, numerator, denominator, start_date, end_date, notes`.
- `finance_lexicon.csv`: `term, candidate_class, vanilla_vader_value, approved_finance_value, direction, student_decision, decision_date, rationale`.
- `fusion_performance_metrics.csv`: the frozen 22-column overlay performance schema.
- `fusion_comparison.csv`: the frozen 13-column base-delta schema.

## Test inventory and command evidence

The new tests cover analyzer isolation, exact lexicon/rejections/zero overrides, text preservation, separate-headline scoring, token matching, coverage/custom-hit distinction, exact-zero/no-news distinction, reliability, sector equal weighting, past-only z-scores, lag/no carry/future perturbation, overlay enumeration, variant selection, projection feasibility/determinism/BLOCK behavior, Combined sleeves, drift, turnover, cost, performance, exact outputs, immutable input hashes, and source reconciliation.

Material command record:

1. Initial sandboxed baseline pytest: exit 1, `19 passed, 4 failed, 7 errors`; every failure was the official loader receiving Windows `WinError 10013` for both frozen URLs. The identical authorised-network retry exited 0 with `30 passed in 40.71s`.
2. Pre-edit data validator: exit 0, `PASS=82 WARN=6 BLOCK=0`.
3. Pre-edit portfolio validator: exit 0, `PASS=14 WARN=0 BLOCK=0`.
4. VADER check: exit 0, resource available, 7,502 vanilla entries, no download.
5. First source/synthetic suite: exit 1, `39 passed, 1 failed`. The synthetic no-news assertion accidentally required the legitimate count `nonneutral_headline_count = 0` to be missing. The assertion was restricted to sentiment-valued fields; no production code or method changed.
6. Corrected source/synthetic suite: exit 0, `40 passed`.
7. First canonical attempt: exit 1 after `zscore_bounds` blocked all eight writes. A read-only diagnostic found ticker and sector z-score minima/maxima exactly `-3.0/+3.0`, with zero observations outside the range. `DataFrame.stack()` missing-value behavior caused the false positive. The validator was changed to an explicit finite-array predicate; no score, signal, method, or parameter changed and no output had been written.
8. Post-correction source/synthetic suite: exit 0, `40 passed`.
9. First successful canonical run: exit 0, data gate `82/6/0`; Stage 6C gate `PASS=56 WARN=2 BLOCK=0`; all eight outputs written.
10. Persisted-output validator: exit 0, `PASS=56 WARN=2 BLOCK=0`.
11. Complete suite after first write: exit 0, `47 passed in 57.32s`.
12. Unchanged deterministic rerun: exit 0; all eight hashes exactly unchanged.
13. Post-rerun persisted validator: exit 0, `PASS=56 WARN=2 BLOCK=0`.
14. Post-rerun complete suite: exit 0, `47 passed in 57.83s`.
15. Hand-in checker: exit 0; exact output:

```text
22 checks passed.
1 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
All checks passed - ready to zip and deploy.
```

The checker result is mechanical evidence only. The report, application, deployment, and submission are not complete.

## Canonical corpus and sentiment diagnostics

- Cleaned headlines: 146,836; mapped/scored: 146,830; endpoint-unmapped exclusions: 6.
- Ticker panel: 50,300 rows; 50 tickers; 1,006 dates; 12,338 no-news rows and 37,962 news-bearing rows.
- Sector panel: 10,060 rows; ten raw sectors; 1,006 dates.
- Plain exact-zero: 71,720 / 146,830 = 0.488456; finance exact-zero: 74,404 / 146,830 = 0.506736.
- Plain neutral band: 72,786 / 146,830 = 0.495716; finance neutral band: 75,369 / 146,830 = 0.513308.
- Non-zero active-lexicon coverage: 71,773 / 146,830 = 0.488817.
- Approved custom-term hit share: 18,802 / 146,830 = 0.128053.
- Plain-to-finance score changes: 18,759 / 146,830 = 0.127760.
- Reliability on all 37,962 news-bearing ticker-days: mean 0.243373; standard deviation 0.216862; min 0; Q25 0; median 0.25; Q75 0.428571; Q90 0.5; Q95 0.6; max 0.9375.
- Lagged-signal availability for each variant: 34,788 / 50,300 = 0.691610. All lag checks used only the immediately preceding observed trading date.
- At rebalance equity-asset grain, missing-signal multiplier one: 3,648 / 14,400 = 0.253333 for each variant.
- Active tilt rates: plain 0.746667, finance 0.746667, evidence-aware 0.501111. Conditional mean absolute multiplier changes: 0.074467, 0.073762, and 0.037613 respectively.

These are coverage/reliability diagnostics, not contextual-accuracy, causal, or investment-value claims.

## Output rows, sizes, and hashes

| Output | Rows | Bytes | SHA-256 |
|---|---:|---:|---|
| `results/data/sector_sentiment_index.csv` | 10,060 | 1,767,370 | `D7670369187E3FF6909A88F6459204284A45D07941DC395CE239D8E304E8E96E` |
| `results/data/ticker_sentiment_daily.csv` | 50,300 | 9,747,819 | `CC9DDF834EF43B9B07240A40949716BA573A14E6ADDCD1997DFF83C125E26FCD` |
| `results/data/fusion_returns.csv` | 18,072 | 3,172,105 | `5A868D15E4D649FEDCB7BF9A0D58657F1729D6F35A2A62A2DF148622EA8CEBC5` |
| `results/data/fusion_weights.csv` | 47,520 | 14,085,713 | `13941551A0D3D9A07290235CCEF7C8AB389D2F78EAF36D81CE661A915F485058` |
| `results/tables/sentiment_diagnostics.csv` | 70 | 11,224 | `3C7842ED0F955DCA29E1E728EFD51C46AA12D4B93999DC9C72D47C436AC179B5` |
| `results/tables/finance_lexicon.csv` | 23 | 3,640 | `5E6EE31DADC6C754DD465E825FBA5F25B3BD26E5E0AA846B3A578619D444C5DB` |
| `results/tables/fusion_performance_metrics.csv` | 24 | 9,139 | `B75FA251E385E3709D3EC1380367D0257285D249AF742965C8FD993FCA770A07` |
| `results/tables/fusion_comparison.csv` | 24 | 7,144 | `B51DF470AEAB5932356037DF72FCF0044729C6F9F88C117E6C4B90F4922C3946` |

## Complete 24-overlay performance evidence

Values below are net, except cost drag. `AnnRet`, `AnnVol`, `MDD`, and `CumRet` are decimal returns.

| Overlay | CumRet | AnnRet | AnnVol | Sharpe | MDD | AvgTurn | Cost drag |
|---|---:|---:|---:|---:|---:|---:|---:|
| equity_equal_weight__plain_vader_naive | .424160 | .125616 | .160902 | .815969 | -.203057 | .052258 | .001303 |
| equity_equal_weight__finance_vader_naive | .424091 | .125598 | .160906 | .815850 | -.203201 | .051944 | .001295 |
| equity_equal_weight__evidence_aware_finance | .422161 | .125087 | .161056 | .812423 | -.202748 | .034054 | .000848 |
| equity_minimum_variance__plain_vader_naive | .171949 | .054535 | .126754 | .482304 | -.150770 | .153911 | .003161 |
| equity_minimum_variance__finance_vader_naive | .175220 | .055519 | .126753 | .489668 | -.151487 | .154056 | .003173 |
| equity_minimum_variance__evidence_aware_finance | .170178 | .054002 | .126821 | .478127 | -.152322 | .145787 | .002989 |
| equity_maximum_sharpe__plain_vader_naive | .188088 | .059373 | .172503 | .420752 | -.231696 | .303537 | .006328 |
| equity_maximum_sharpe__finance_vader_naive | .195853 | .061685 | .172668 | .433151 | -.229416 | .302867 | .006356 |
| equity_maximum_sharpe__evidence_aware_finance | .190212 | .060006 | .172787 | .423811 | -.226784 | .298685 | .006238 |
| equity_risk_parity__plain_vader_naive | .324747 | .098685 | .145184 | .720887 | -.186006 | .054691 | .001269 |
| equity_risk_parity__finance_vader_naive | .324947 | .098741 | .145184 | .721238 | -.186414 | .054229 | .001258 |
| equity_risk_parity__evidence_aware_finance | .322255 | .097993 | .145229 | .716371 | -.185541 | .037940 | .000878 |
| combined_equal_weight__plain_vader_naive | .520790 | .150619 | .215743 | .758506 | -.277924 | .058253 | .001551 |
| combined_equal_weight__finance_vader_naive | .520818 | .150626 | .215774 | .758457 | -.277215 | .058029 | .001545 |
| combined_equal_weight__evidence_aware_finance | .519020 | .150171 | .215904 | .756297 | -.278295 | .043696 | .001162 |
| combined_minimum_variance__plain_vader_naive | .171862 | .054509 | .126995 | .481436 | -.152210 | .155534 | .003194 |
| combined_minimum_variance__finance_vader_naive | .175357 | .055560 | .126992 | .489295 | -.152936 | .155605 | .003205 |
| combined_minimum_variance__evidence_aware_finance | .170146 | .053992 | .127065 | .477383 | -.153799 | .147245 | .003019 |
| combined_maximum_sharpe__plain_vader_naive | .580173 | .165464 | .233058 | .773245 | -.232920 | .310074 | .008599 |
| combined_maximum_sharpe__finance_vader_naive | .589416 | .167741 | .233229 | .781227 | -.230643 | .309767 | .008640 |
| combined_maximum_sharpe__evidence_aware_finance | .584413 | .166509 | .233225 | .776711 | -.227927 | .305551 | .008496 |
| combined_risk_parity__plain_vader_naive | .476541 | .139305 | .161921 | .886582 | -.195230 | .058516 | .001513 |
| combined_risk_parity__finance_vader_naive | .476999 | .139423 | .161930 | .887182 | -.195589 | .058241 | .001506 |
| combined_risk_parity__evidence_aware_finance | .474013 | .138652 | .161970 | .882819 | -.195035 | .043514 | .001123 |

## Complete base-versus-overlay reconciliation

Every value is `overlay − corresponding frozen base`. `dRet`, `dVol`, `dSharpe`, `dMDD`, and `dCum` are the principal metric deltas; the canonical CSV also preserves turnover and cost deltas shown here.

| Overlay | dRet | dVol | dSharpe | dMDD | dCum | dAvgTurn | dTotalTurn | dCostDrag |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| equity_equal_weight__plain_vader_naive | -.000628 | -.000274 | -.002350 | -.000491 | -.002376 | .025019 | .875663 | .000623 |
| equity_equal_weight__finance_vader_naive | -.000647 | -.000269 | -.002470 | -.000635 | -.002446 | .024704 | .864650 | .000615 |
| equity_equal_weight__evidence_aware_finance | -.001157 | -.000120 | -.005897 | -.000182 | -.004375 | .006814 | .238506 | .000168 |
| equity_minimum_variance__plain_vader_naive | .000925 | -.000150 | .007334 | .002108 | .003068 | .010449 | .365712 | .000223 |
| equity_minimum_variance__finance_vader_naive | .001909 | -.000150 | .014698 | .001390 | .006340 | .010594 | .370802 | .000234 |
| equity_minimum_variance__evidence_aware_finance | .000391 | -.000083 | .003157 | .000556 | .001298 | .002325 | .081372 | .000051 |
| equity_maximum_sharpe__plain_vader_naive | .001107 | -.000530 | .006795 | -.005483 | .003705 | .007401 | .259047 | .000174 |
| equity_maximum_sharpe__finance_vader_naive | .003419 | -.000365 | .019194 | -.003203 | .011470 | .006732 | .235606 | .000201 |
| equity_maximum_sharpe__evidence_aware_finance | .001740 | -.000246 | .009854 | -.000571 | .005828 | .002550 | .089235 | .000084 |
| equity_risk_parity__plain_vader_naive | -.000221 | -.000095 | -.001008 | -.001001 | -.000795 | .022877 | .800710 | .000530 |
| equity_risk_parity__finance_vader_naive | -.000165 | -.000095 | -.000657 | -.001410 | -.000594 | .022415 | .784538 | .000520 |
| equity_risk_parity__evidence_aware_finance | -.000913 | -.000050 | -.005525 | -.000536 | -.003287 | .006127 | .214432 | .000140 |
| combined_equal_weight__plain_vader_naive | -.000473 | -.000256 | -.001265 | .000954 | -.001871 | .019680 | .688810 | .000523 |
| combined_equal_weight__finance_vader_naive | -.000466 | -.000226 | -.001314 | .001663 | -.001843 | .019456 | .680969 | .000517 |
| combined_equal_weight__evidence_aware_finance | -.000922 | -.000095 | -.003474 | .000582 | -.003641 | .005123 | .179305 | .000134 |
| combined_minimum_variance__plain_vader_naive | .000948 | -.000154 | .007502 | .002199 | .003145 | .010524 | .368356 | .000224 |
| combined_minimum_variance__finance_vader_naive | .001999 | -.000157 | .015362 | .001473 | .006639 | .010595 | .370822 | .000235 |
| combined_minimum_variance__evidence_aware_finance | .000431 | -.000084 | .003450 | .000611 | .001429 | .002235 | .078229 | .000050 |
| combined_maximum_sharpe__plain_vader_naive | .000404 | -.000329 | .002243 | -.005644 | .001638 | .006884 | .240951 | .000200 |
| combined_maximum_sharpe__finance_vader_naive | .002681 | -.000157 | .010225 | -.003367 | .010881 | .006577 | .230205 | .000242 |
| combined_maximum_sharpe__evidence_aware_finance | .001450 | -.000161 | .005709 | -.000651 | .005877 | .002362 | .082655 | .000097 |
| combined_risk_parity__plain_vader_naive | -.000115 | -.000093 | -.000211 | -.000391 | -.000446 | .020662 | .723168 | .000534 |
| combined_risk_parity__finance_vader_naive | .000003 | -.000084 | .000389 | -.000750 | .000012 | .020387 | .713562 | .000527 |
| combined_risk_parity__evidence_aware_finance | -.000768 | -.000043 | -.003974 | -.000196 | -.002974 | .005660 | .198103 | .000144 |

No overlay was omitted. No statistical-significance claim is made.

## Projection, constraints, lag, turnover, and cost evidence

- Target-weight minimum `0`; maximum `0.20000000000000001`; maximum group sum residual `6.39e-12`.
- Projection failures: 0.
- Maximum Combined crypto target difference from base: `1.01e-16`.
- Maximum Combined equity-sleeve difference from base: `3.77e-15`.
- Maximum 5-bps cost-formula residual: `9.95e-17`.
- Maximum gross/net multiplicative-formula residual: `3.18e-16`.
- Aggregate published transaction cost across overlay dates: `0.058589726507755097` (sum across 24 separate strategies, not an investor portfolio total).
- Validator independently reconciled every source return, drifted pretrade vector, turnover, cost, performance metric, and base delta.
- Future-headline, current-date, immediate-prior-date, no-carry, weekend/holiday, and perturbation behavior were tested.

## Immutable accepted portfolio evidence

All five Stage 5A files remained byte-identical:

| File | SHA-256 before and after |
|---|---|
| `results/data/fund_returns.csv` | `7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84` |
| `results/data/fund_weights.csv` | `F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8` |
| `results/tables/performance_metrics.csv` | `5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19` |
| `results/tables/portfolio_solver_diagnostics.csv` | `ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C` |
| `results/tables/extreme_sensitivity_metrics.csv` | `40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151` |

## Genuine errors and corrections

Only genuine issues are recorded:

1. Three pre-edit read-only reconciliation predicates were too literal about Markdown width, hyphenation, and provenance-log repetition. Corrected predicates passed without changing a record.
2. The initial baseline ran inside a restricted network sandbox and the protected loader was blocked. The identical command was rerun with authorised network access; no URL or loader changed.
3. One synthetic no-news assertion included a legitimate zero count among missing sentiment values. Only that test predicate changed.
4. The first canonical attempt was blocked before any output write by a `DataFrame.stack()`-based z-range false positive. Direct measurement proved all finite extrema exactly inside `[-3,+3]`; only the validator predicate changed.
5. A sandboxed PowerShell hash read encountered access denial for outputs created by the authorised external process. The already printed hashes were independently re-extracted read-only with the verified interpreter; no artifact was altered.

No correction changed the frozen lexicon, reliability formula, standardisation, neutral threshold, history rule, lag, lambda, eligible funds, monthly schedule, projection, costs, sample, output inclusion, or performance definitions. No parameter changed after results were observed.

## Limitations

- Lexicon polarity is transparent and student-approved but still context-insensitive; zero/custom coverage is not proof of accuracy.
- Reliability is evidence quantity/agreement, not truth, causality, independence, or information quality; syndicated headlines may inflate it.
- Missing prior-day signals intentionally produce multiplier one; no older signal is carried forward.
- The six endpoint headlines remain excluded from trading alignment but disclosed.
- Results are OOS backtests, not guaranteed investor returns, and include no prespecified significance test.
- Figures, report interpretation, app consumption, deployment, publication, and final submission remain unperformed and unauthorised.

## Files changed or created

Modified only:

- `ai/08_student_lexicon_review_and_freeze.md` (chronological Stage 6B closure and quotation clarification);
- `src/sentiment.py`;
- `src/fusion.py`;
- `scripts/run_part_b.py`.

Created only:

- `src/sentiment_validation.py`;
- `scripts/validate_sentiment_fusion.py`;
- `tests/test_sentiment.py`;
- `tests/test_fusion.py`;
- `tests/test_sentiment_outputs.py`;
- `ai/09_sentiment_fusion_implementation.md`;
- the eight authorised output CSVs listed above.

No figure, report, app, raw-data extract, cache, bytecode, environment artifact, or temporary project script was created. No Git operation occurred.

## Boundary audit

The complete comparison captured immediately before this boundary paragraph was written contained 76 included files and digest `61A22D1F6543FA444044925F53B8869D389BAC36BFD106CE9A3E63F04330F493`, versus 62 files and pre-edit digest `265B4694B1F7EE091D1412BB0568C8D46A29A954FB7BBC01F0821546C147239A`. The only differences were the four authorised modifications and 14 authorised additions listed above. No file was removed; 58 pre-existing files were byte-identical.

The 14 additions reconcile exactly to six authorised code/test/log files plus eight canonical CSVs. No cache, bytecode, raw-data extract, environment, temporary script, figure, report, app, placeholder, or unexpected file appeared. All five accepted portfolio files retained their pre-stage hashes.

`.idea/workspace.xml` remained unchanged at 8,223 bytes and SHA-256 `4AD5F2898A59666D28858279505797447E01364D4A13A16381932B8DC0CB27E8`; no other `.idea` file changed. It was not edited, restored, or normalised by Codex. The manifest excluded `.git`, environments, caches, and compiled bytecode as prespecified, while including `.idea`. No file was removed and no Git operation occurred.

The first two PowerShell digest expressions used APIs unavailable in the host PowerShell/.NET combination and returned a null digest; the entry-by-entry comparison still completed. A portable `SHA256.Create().ComputeHash()` plus `BitConverter` expression produced the digest above. This was a read-only manifest-tool correction and changed no project file.

Because this paragraph is itself inside the authorised new AI log, writing it necessarily changes the complete-manifest digest. The final response reports the final post-paragraph manifest digest and repeats the unchanged path-level comparison; this avoids pretending that a file can contain its own final hash without altering that hash.

## Operational prompt record

The Stage 6C prompt is reproduced below with the non-authoritative English quotation omitted on the student's explicit instruction. All modelling, file-boundary, validation, and prohibition language remains operative. The subsequent clarification prompt is reproduced verbatim after it.

<details>
<summary>Stage 6C operational prompt (quotation-provenance corrected)</summary>

```text
You are working on FINS5545 Project B.

This is Workflow Stage 6C only: Frozen Sentiment and Fusion Implementation, Validation, and Canonical Result Generation.

Student verification and authority

ChatGPT independently reviewed the completed Stage 6B transcription with the student and verified all 27 candidate decisions; 17 ACCEPT, 6 EDIT, and 4 REJECT; all 23 final operational values; the four rejected ETF-flow terms; the accepted sentiment/fusion methodology; the sector custom-term diagnostic resolution; the AI-workflow role attribution; and the recorded validator false positive and correction.

ChatGPT presented the complete Chinese Stage 6B acceptance statement. The student replied exactly: “我确认了，来吧！” That reply constitutes acceptance and closure of Stage 6B and limited authorisation of Stage 6C.

The student therefore accepts and closes Stage 6B; confirms the complete Stage 6B transcription; authorises Stage 6C only; authorises implementation and execution of the already frozen sentiment and fusion design; authorises creation of the eight already documented canonical sentiment/fusion outputs; does not authorise changing the lexicon, methodology, thresholds, lag, standardisation, reliability formula, lambda, portfolio universe, costs, reporting universe, or output schemas after observing results; and does not authorise figures, report writing, Streamlit, deployment, publication, or Git operations. Weak, negative, insignificant, inconvenient, or counterintuitive results must be retained and reported.

1. Workspace and interpreter guard

Verify both project root and terminal directory exactly equal C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB. Use only C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe. Do not inspect Project A, siblings, the broader repository, or another student's work. Use the configured Python-environment guidance and data-quality workflow. Do not install, remove, or upgrade a package; use the existing VADER resource.

2. Frozen-input reconciliation gate

Read completely AGENTS.md; relevant brief and context files; frozen data, portfolio, finance-lexicon, and sentiment design documents; Stage 6A/6B logs; current protected loader, ETL, feature, validation, portfolio, sentiment, fusion, orchestration, validation scripts, tests, and checker. Read the five portfolio CSVs only as immutable inputs and hash them. Reconcile 27 candidates, 17/6/4 decisions, 23 exact values, exact four rejections, no pending/rejected operational term, and consistent method/output schemas. Stop on discrepancy.

3. Frozen operational finance lexicon

Implement exactly: shares 0.0; energy 0.0; alert 0.0; rally +1.0; active 0.0; beat +1.5; rebound +0.5; downgrades -1.0; asset 0.0; beats +1.5; outperform +1.0; miss -1.0; overweight +1.0; bullish +1.5; slump -1.5; misses -1.5; plunge -1.5; downgraded -1.5; tumble -1.5; underweight -1.0; plunges -1.5; underperform -1.0; layoffs -1.0. Exclude inflow, inflows, outflow, outflows. Add nothing. Zero overrides are intentional custom hits but not non-zero coverage. Decision date 2026-08-14.

4. Authorised file boundary

Append only ai/08_student_lexicon_review_and_freeze.md. Modify only src/sentiment.py, src/fusion.py, scripts/run_part_b.py. Create only src/sentiment_validation.py, scripts/validate_sentiment_fusion.py, tests/test_sentiment.py, tests/test_fusion.py, tests/test_sentiment_outputs.py, ai/09_sentiment_fusion_implementation.md, and the eight authorised output CSVs. Verify targets absent. Do not modify any other file. .idea/workspace.xml may change independently but must remain read-only and separately disclosed. Temporary material must stay outside Project B.

5. Close Stage 6B

Append “Final student verification — Stage 6B accepted and closed”; record ChatGPT review, authoritative Chinese reply, 17/6/4, 23 values, four rejections, accepted methodology/schema resolution, and limited Stage 6C authority. End: Stage 6B accepted and closed; Stage 6C authorised only for implementation, validation, and canonical result generation under the frozen design.

6. Baseline validation before edits

Capture pre-edit manifest and run the complete current pytest suite, data validator, and portfolio validator using the explicit interpreter and -B. Stop on a substantive baseline failure; identical official-loader retry is permitted for a network sandbox.

7. Implement src/sentiment.py

Use isolated vanilla and finance VADER analyzers; never mutate vanilla; preserve exact headline text; score each headline separately; use exact regex (?<![A-Za-z0-9])[A-Za-z]+(?:['-][A-Za-z]+)*(?![A-Za-z0-9]); calculate non-zero active coverage and 23-term custom hits separately; use 146,830 mapped headlines and disclose six exclusions; create complete 50-by-1,006 ticker panel with no-news sentiment missing; implement the frozen reliability formula; standardise by ticker on previous 252 observed dates, exclude current, require 60 non-missing, ddof=1 and std >1e-8, clip only z; define evidence_aware_signal=finance_z*reliability; lag exactly one observed equity date with no carry; create complete ten-sector-by-1,006 equal-weight news-bearing-ticker index; keep sector custom-hit share in diagnostics only.

8. Implement src/fusion.py

Use eight accepted Equity/Combined base funds and three variants, 24 overlays, deterministic IDs and order. Use immutable base targets, accepted returns, lagged ticker signals; never rerun optimisation; fixed lambda 0.10; missing signal multiplier one. Equity projection preserves sum one under 0.20 cap. Combined projection leaves every crypto target numerically unchanged and preserves equity sleeve E. Projection failure is BLOCK. Reuse Stage 5A first-live dates, drift, inception, turnover, 5-bps costs, gross/net returns, and metrics.

9. Update scripts/run_part_b.py

Add --stage sentiment-fusion. Verify lexicon, load protected data, create sentiment and all 24 overlays in memory, validate, then safely write all eight outputs only on zero BLOCK. Do not alter portfolio-stage behavior or existing portfolio files.

10. Exact output contracts

Follow the frozen exact schemas, dtypes, keys, grain, missingness, and sort orders. Required rows: ticker sentiment 50,300; sector index 10,060; lexicon 23; fusion returns 18,072; fusion weights 47,520; fusion performance 24; comparison 24; diagnostics non-empty and uniquely keyed. Include exact diagnostic numerators/denominators and all 24 comparisons. Do not claim significance.

11. Implement validation

Create machine-readable PASS/WARN/BLOCK checks and a persisted-output validator. Block on lexicon, schema, count, key, mapping, missingness, reliability, sector, z-score, lag, overlay, schedule, lambda, constraint, crypto/sleeve, projection, turnover, cost, metric, delta, or selective-reporting failure.

12. Required tests

Create independent sentiment, fusion, and output tests for every frozen text, lexicon, missingness, aggregation, reliability, standardisation, lag/leakage, overlay, projection, sleeve, drift, turnover, cost, metric, schema, count, hash, and deterministic-rerun risk. Do not weaken valid tests; preserve and explain a wrong-test correction.

13. Execution order

Run the specified source/synthetic suite; generate outputs; run dedicated validator; run complete suite; record eight hashes; rerun unchanged stage; confirm identical hashes; rerun validator and suite; run hand-in checker. Use explicit interpreter, -B, and no pytest cache. Retry only unchanged official loader for a restricted network sandbox.

14. Result discipline

After first complete results, do not change any lexicon, sentiment, reliability, standardisation, clipping, lag, lambda, universe, schedule, projection, cost, sample, output inclusion, or performance definition. Only demonstrable implementation/schema/arithmetic/validation defects may be corrected, with failed evidence retained and affected checks rerun. Poor performance is not a defect.

15. AI workflow log

Record date/status, authority, prompt, roles, files, reconciliation, hashes, environment/VADER, implementation, lexicon, tests, commands/exits, genuine errors, counts/schemas/hashes, diagnostics, all 24 results and comparisons, integrity evidence, deterministic rerun, preserved portfolio hashes, limitations, no tuning, and boundary. Status Pending student review.

16. Boundary audit

Verify only the authorised four existing files changed and six code/test/log plus eight outputs were created; nothing else changed or was removed; five portfolio outputs byte-identical; no figure/report/app/cache/bytecode/raw/environment/temp/Git artifact; disclose independent .idea/workspace.xml only.

17. Final response

Report guard, closure, reconciliation, lexicon/exclusions, VADER, counts/hashes/diagnostics/reliability/lag, complete 24 performance and deltas, constraints/costs/tests/validators/rerun/checker/files/hashes/manifest/errors/limitations/no tuning/no later-stage work. End with the mandated Stage 6C status and stop.
```

</details>

<details>
<summary>Student quotation-provenance clarification (verbatim)</summary>

```text
The authoritative verbatim student reply is:

“我确认了，来吧！”

The sentence:

“I have finished reviewing everything and find no issues. We may proceed to the next stage.”

is not an exact student quotation. Do not record it in quotation marks or attribute it to the student verbatim. Omit it from the provenance record.

The accurate provenance is:

1. ChatGPT presented the complete Chinese Stage 6B acceptance statement for the student to confirm.
2. The student confirmed that statement by replying exactly: “我确认了，来吧！”
3. That exact Chinese reply constitutes the student’s acceptance of Stage 6B and limited authorisation of Stage 6C.

You are authorised to resume the existing Stage 6C prompt from the point immediately after the workspace guard. Preserve the original file boundary, frozen lexicon, methodology, validation requirements, and prohibitions unchanged.

Record this pre-execution stop as a genuine provenance clarification:

- the workspace guard passed;
- Codex detected apparently conflicting quotation language;
- Codex stopped before reading or editing Project B;
- the student clarified that “我确认了，来吧！” is the only authoritative verbatim reply;
- no file, command, model, or output existed before the clarification.

Do not present the clarification as a methodological change or student correction to the model. It resolves quotation provenance only.

Proceed with Stage 6C exactly as previously authorised.
[@08_student_lexicon_review_and_freeze.md](file:///C:/Users/24116/Documents/GitHub/fins-agent/fins2026/z5618000_projectB/ai/08_student_lexicon_review_and_freeze.md)
```

</details>

<details>
<summary>Complete Stage 6C implementation requirements (original wording after the quotation clarification)</summary>

The inaccurate English sentence from the first authority preamble is omitted here by the student's later explicit instruction. The authoritative Chinese reply and clarification are preserved above and below. The remaining operational instruction is recorded in full:

```text
This is Workflow Stage 6C only: Frozen Sentiment and Fusion Implementation, Validation, and Canonical Result Generation.

By sending this prompt, the student therefore:

1. accepts and closes Stage 6B;
2. confirms the complete Stage 6B transcription;
3. authorises Stage 6C only;
4. authorises implementation and execution of the already frozen sentiment and fusion design;
5. authorises creation of the eight already documented canonical sentiment/fusion outputs;
6. does not authorise changing the lexicon, methodology, thresholds, lag, standardisation, reliability formula, lambda, portfolio universe, costs, reporting universe, or output schemas after observing results;
7. does not authorise figures, report writing, Streamlit, deployment, publication, or Git operations.

Weak, negative, insignificant, inconvenient, or counterintuitive results must be retained and reported.

## 1. Workspace and interpreter guard

Before reading project contents, verify that both the opened PyCharm project root and terminal working directory resolve exactly to:

`C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`

Use only:

`C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`

Do not inspect:

* Project A;
* sibling folders;
* the broader repository;
* another student’s work.

Stop without editing if either guard fails.

Use the configured Python-environment guidance for every Python invocation and the data-quality workflow for all result reconciliation.

Do not install, remove, or upgrade any package. The existing VADER resource must be used. Do not download another resource unless the existing frozen record is contradicted, in which case stop and report rather than downloading automatically.

## 2. Frozen-input reconciliation gate

Before editing source code, read completely:

* `AGENTS.md`
* relevant sentiment, fusion, innovation, AI-workflow, output, and rubric sections of `PROJECT_BRIEF.md`
* `context/DATA_GUIDE.md`
* `context/project_context.md`
* `context/verify_ai_output.md`
* `docs/data_contract.md`
* `docs/portfolio_backtest_design.md`
* `docs/finance_lexicon_review.md`
* `docs/sentiment_innovation_design.md`
* `ai/07_sentiment_design_and_lexicon_candidates.md`
* `ai/08_student_lexicon_review_and_freeze.md`
* current `src/data_access.py`
* current `src/etl.py`
* current `src/features.py`
* current `src/validation.py`
* current `src/portfolios.py`
* current `src/portfolio_validation.py`
* current `src/sentiment.py`
* current `src/fusion.py`
* current `scripts/run_part_b.py`
* current validation scripts
* all current tests
* `scripts/check_handin.py`

Read the five existing portfolio CSVs only as accepted immutable inputs and comparison evidence:

* `results/data/fund_returns.csv`
* `results/data/fund_weights.csv`
* `results/tables/performance_metrics.csv`
* `results/tables/portfolio_solver_diagnostics.csv`
* `results/tables/extreme_sensitivity_metrics.csv`

Record their pre-stage SHA-256 hashes. They must remain byte-for-byte unchanged.

Before implementation, reconcile the three frozen governance sources:

* `docs/finance_lexicon_review.md`
* `docs/sentiment_innovation_design.md`
* `ai/08_student_lexicon_review_and_freeze.md`

Verify exactly:

* 27 reviewed candidates;
* 17 `ACCEPT`;
* 6 `EDIT`;
* 4 `REJECT`;
* 23 operational entries;
* all operational values match the table below;
* rejected terms are exactly `inflow`, `inflows`, `outflow`, and `outflows`;
* no rejected or pending term is operational;
* the methodology and output schemas agree across the documents.

If any frozen-input discrepancy exists, stop before editing. Do not choose one version silently.

## 3. Frozen operational finance lexicon

Implement exactly these 23 entries and values:

| Term | Final value | Student decision |
|---|---:|---|
| `shares` | 0.0 | ACCEPT |
| `energy` | 0.0 | ACCEPT |
| `alert` | 0.0 | ACCEPT |
| `rally` | +1.0 | ACCEPT |
| `active` | 0.0 | ACCEPT |
| `beat` | +1.5 | ACCEPT |
| `rebound` | +0.5 | EDIT |
| `downgrades` | -1.0 | EDIT |
| `asset` | 0.0 | ACCEPT |
| `beats` | +1.5 | ACCEPT |
| `outperform` | +1.0 | EDIT |
| `miss` | -1.0 | EDIT |
| `overweight` | +1.0 | ACCEPT |
| `bullish` | +1.5 | ACCEPT |
| `slump` | -1.5 | ACCEPT |
| `misses` | -1.5 | ACCEPT |
| `plunge` | -1.5 | ACCEPT |
| `downgraded` | -1.5 | ACCEPT |
| `tumble` | -1.5 | ACCEPT |
| `underweight` | -1.0 | ACCEPT |
| `plunges` | -1.5 | ACCEPT |
| `underperform` | -1.0 | EDIT |
| `layoffs` | -1.0 | EDIT |

Do not include `inflow`, `inflows`, `outflow`, or `outflows`. Do not add any other term.

Zero-valued overrides are intentional and operational. They neutralise inappropriate vanilla values but still count as approved custom-term hits. They do not count as non-zero active-lexicon coverage.

The operational lexicon decision date is `2026-08-14`.

## 4. Authorised file boundary

Append only `ai/08_student_lexicon_review_and_freeze.md`.

Modify only `src/sentiment.py`, `src/fusion.py`, and `scripts/run_part_b.py`.

Create only `src/sentiment_validation.py`, `scripts/validate_sentiment_fusion.py`, `tests/test_sentiment.py`, `tests/test_fusion.py`, `tests/test_sentiment_outputs.py`, and `ai/09_sentiment_fusion_implementation.md`.

Create only these canonical outputs:

* `results/data/sector_sentiment_index.csv`
* `results/data/ticker_sentiment_daily.csv`
* `results/data/fusion_returns.csv`
* `results/data/fusion_weights.csv`
* `results/tables/sentiment_diagnostics.csv`
* `results/tables/finance_lexicon.csv`
* `results/tables/fusion_performance_metrics.csv`
* `results/tables/fusion_comparison.csv`

Verify that all six new code/test/log targets and all eight result targets are absent before the first edit or run. After a successful first write, an unchanged deterministic rerun may overwrite only these same eight authorised outputs.

Do not modify or create anything else, including official files, other docs/logs, protected data/ETL/features/validation/portfolio files, existing tests/outputs, README, requirements, report, figures, Streamlit, Git state, environments, caches, or bytecode.

`.idea/workspace.xml` may change independently as PyCharm session metadata. Treat it read-only and disclose its hashes separately. Do not edit, restore, delete, or normalise it. No other `.idea` change is permitted.

Any temporary manifest or diagnostic script must exist outside Project B and be deleted afterward. Do not save headline-level extracts, raw data, temporary CSVs, pickles, caches, or token dumps inside Project B.

## 5. Close Stage 6B

Append a chronological section to `ai/08_student_lexicon_review_and_freeze.md` titled `## Final student verification — Stage 6B accepted and closed`.

Record ChatGPT’s independent transcription review; the authoritative Chinese reply; the 17/6/4 reconciliation; 23 final values; four ETF-flow rejections; frozen methodology/schema resolution; and limited Stage 6C authorisation. Do not rewrite earlier history.

End with: `Stage 6B accepted and closed; Stage 6C authorised only for implementation, validation, and canonical result generation under the frozen design.`

## 6. Baseline validation before edits

Capture the pre-edit manifest and run:

`& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider`

`& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_data_contract.py`

`& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_portfolios.py`

Record exact commands, outputs, and exits. Stop on a substantive baseline failure. A restricted-network retry may use the identical command and loader only.

## 7. Implement `src/sentiment.py`

Create independent plain and finance VADER analyzers; never mutate plain; verify vanilla before/after; use existing resource; preserve exact title text; score each headline separately; do not preprocess text or use returns.

Use regex `(?<![A-Za-z0-9])[A-Za-z]+(?:['-][A-Za-z]+)*(?![A-Za-z0-9])`, lowercasing only match keys. Calculate per headline plain compound, finance compound, non-zero active-finance coverage, and any-23-term custom hit. Zero overrides count only for custom hits. Do not save headline-level results.

Use 146,830 mapped headlines, disclose six endpoint exclusions, and treat count discrepancies as BLOCK. Build the full 50-by-1,006 ticker-day panel. On news days, equal-weight headline scores and calculate frozen reliability. On no-news days, keep sentiment/evidence/z fields missing with no carry-forward. Preserve scored-neutral news.

Reliability: covered headline share times directional agreement times n/(n+1), with non-neutral defined by abs(finance compound)>=0.05 and m=0 agreement zero. Raw evidence-aware compound is finance score times reliability. All components finite in [0,1].

For ticker z-scores, use previous 252 observed equity dates, exclude current, use non-missing values within that date window, require 60 and sample std>1e-8, clip only z to [-3,+3]. Tradable evidence-aware signal is finance_z times reliability; do not standardise the raw evidence-aware compound for trading.

Lag only to the immediately next observed trading date; store source date; no same-day, future, or older carried signal.

Create a complete ten-sector-by-1,006 panel. Equal-weight news-bearing ticker days, exclude no-news from score denominators, calculate coverage and diagnostic z-scores under the same past-only rule. Store sector custom-term hit share only in diagnostics.

## 8. Implement `src/fusion.py`

Use four Equity and four Combined base funds, exclude Crypto-only, and apply `plain_vader_naive`, `finance_vader_naive`, and `evidence_aware_finance` for 24 deterministic overlays.

Use immutable canonical base target weights, accepted asset returns, and lagged ticker signals. Do not rerun optimisation, alter base targets/files, use sector z-scores, or use unlagged sentiment. Trade only on each base fund’s monthly rebalance dates.

Use `lambda=0.10` and `multiplier=exp(0.10*signal)`, with missing signal preserved and multiplier one.

For Equity, normalise raw tilted weights and solve the Euclidean capped simplex under 0<=w<=0.20 and sum one. For Combined, keep every crypto target numerically unchanged, preserve crypto/equity totals, tilt/project equities only to E. A failure is BLOCK with no fallback.

Reuse Stage 5A first-live dates, calendars, drift, inception, pretrade weights, turnover, 5-bps cost, gross/net returns, and performance metrics exactly. Preserve all audit columns and initial-formation convention.

## 9. Update `scripts/run_part_b.py`

Add `--stage sentiment-fusion`. It must verify lexicon, load through protected data, create sentiment and all 24 overlays in memory, create all eight outputs in memory, run blocking validation, and write all eight only on zero BLOCK in exact deterministic schemas/orders. Preserve portfolio-stage behavior. Avoid partial result sets and remove any same-stage temporary files.

## 10. Exact output contracts

Follow exactly the already frozen column order, dtypes, keys, grain, missingness, and sort order. Do not widen, rename, reorder, or omit columns.

Required row gates: ticker sentiment 50,300; sector index 10,060; finance lexicon 23; fusion returns 18,072; fusion weights 47,520; fusion performance 24; fusion comparison 24. Diagnostics must be non-empty, uniquely keyed, and complete.

Include only 23 approved/edited lexicon rows with original class/vanilla value, final value/direction/decision/date/rationale, term-sorted, and no rejection.

Diagnostics must cover mapped/unmapped counts; exact-zero and neutral-band rates; non-zero coverage; custom hits; score changes; ticker/sector coverage; reliability/agreement/volume distributions; usable/missing z and lag; multiplier-one missingness; active tilt frequency/magnitude; and sector custom hits, with explicit numerators/denominators.

Compute all 24 performance and comparison rows. Every delta is overlay minus corresponding frozen base. Omit no weak overlay and make no unauthorised significance claim.

## 11. Implement validation

Create machine-readable PASS/WARN/BLOCK in `src/sentiment_validation.py` and a precomputed-output validator in `scripts/validate_sentiment_fusion.py` that exits nonzero on BLOCK without rerunning optimisation.

Blocking checks must cover exact lexicon/values/classes/decisions/rejections/plain isolation; exact schemas/dtypes/counts/keys/order/membership/dates/mapping/no-news/neutral/reliability/sector/z/lag/schema resolution; exact 24 overlays and no Crypto; dates/monthly schedule/lambda/missing multiplier/constraints/crypto identity/sleeve preservation/projection/turnover/cost/gross-net/metrics/deltas/no selective reporting.

## 12. Required tests

Create independent synthetic calculations where possible. Sentiment tests must cover exact vanilla reproduction, isolation, lexicon, zero overrides, rejections, text preservation, separate scoring, token matching, coverage/custom distinction, zero/neutral/no-news, aggregation, reliability, m=0, sector weighting/no-news, fixed-date standardisation, current exclusion, 60 minimum, ddof=1, dispersion, z-only clipping, evidence formulas, ticker/sector separation, next-date lag across weekdays/weekends/holidays, no carry, and future perturbation.

Fusion tests must cover 24 IDs/order, no Crypto, lambda, signal selection, missing multiplier, monthly schedule, projections, Combined identities/sleeves, deterministic/failure behavior, all-missing base reproduction, drift, inception, turnover, cost, gross/net, metrics, and deltas.

Output tests must cover exact eight files/schemas/dtypes/keys/rows/order, lexicon/rejections, panels, overlays, performance/comparison, projection success, immutable portfolio hashes, and deterministic rerun hashes.

Do not weaken a correct test. Preserve a failed wrong-test attempt and explain the correction.

## 13. Execution order

Use the explicit interpreter, `-B`, and no pytest cache. Run the specified source/synthetic suite; generate `--stage sentiment-fusion`; run dedicated validator; run complete suite; record all eight hashes; rerun unchanged stage once; confirm all hashes identical; rerun validator and suite; finally run checker.

Retry only the unchanged loader command when a network sandbox blocks it. Record every genuine failure, root cause, correction, and exit.

## 14. Result discipline

After first complete results, do not change terms/values/rejections, sentiment models, reliability, coverage, neutral threshold, 252-date/60-observation rules, standardisation, clipping, lag, mapping, lambda, funds, schedule, projection, costs, sample, output inclusion, or performance definitions.

Only implementation, schema, arithmetic, or validation defects inconsistent with the frozen design may be corrected. Preserve failed evidence, explain why the fix implements rather than changes the method, rerun checks, and report hash effects. Poor performance is not a defect.

## 15. AI workflow log

Create `ai/09_sentiment_fusion_implementation.md` with date/status/objective/authority/prompt/roles/files/reconciliation/manifests/hashes/environment/VADER/design/lexicon/functions/tests/commands/exits/errors/counts/schemas/hashes/diagnostics/all 24 results/all 24 comparisons/integrity/determinism/immutable portfolio hashes/limitations/no tuning/boundary and status Pending student review. Do not invent success, significance, error, correction, causal evidence, deployment, report, or app completion.

## 16. Boundary audit

Modified only ai/08, src/sentiment.py, src/fusion.py, scripts/run_part_b.py. Created only six code/test/log files and eight outputs. Verify nothing else changed or was removed, five portfolio outputs byte-identical, and no figure/report/app/cache/bytecode/raw/environment/temp/Git artifact. Separately disclose independently changed workspace.xml only; no other `.idea` change.

## 17. Final response

Report workspace, Stage 6B closure, reconciliation, exact lexicon/rejections, VADER, mapped/unmapped and panel counts, all eight rows/hashes, diagnostics/reliability/lag, complete 24 performance and deltas, projection/constraints/cost, tests/validators/rerun/checker, exact files, portfolio hashes, manifest, errors/corrections, limitations, no tuning, and no later-stage work.

End with:

`Stage 6C frozen sentiment and fusion models implemented, validated, and generated; pending student review. All 24 overlays and unfavourable results are retained. No post-result tuning, figure, report, application, deployment, or Git work authorised.`

Stop. Do not begin result interpretation, figure creation, report writing, Streamlit, deployment, publication, submission packaging, or Git operations.
```

</details>

## Review status

`Pending student review`

No next stage is authorised.

## Final student acceptance — Stage 6C closed

**Date:** 2026-08-14

The student stated exactly:

> “I have reviewed and accept the implementation of Stage 6C, all 24 complete results and audit records. I accept both favourable and unfavourable outcomes and confirm no ex-post parameter tuning is permitted. Stage 6C accepted and closed. The next stage is authorised to conduct result auditing and design figures and supporting evidence for the report; no authorisation is granted to modify the frozen models or parameters.”

This acceptance closes Stage 6C and authorises Stage 7 only: independent audit of the existing canonical results and reproducible generation of report-facing exhibits from those frozen outputs. It does not authorise recomputation, replacement, tuning, or selective filtering of any model result, and it does not authorise report prose, application work, deployment, publication, submission, or Git operations.

`Stage 6C accepted and closed; Stage 7 authorised for independent results audit, canonical exhibit generation, and report-evidence design only.`
