# Project A hand-off audit

**Audit date:** 2026-08-14 (Australia/Sydney)  
**Workflow stage:** Stage 3A — read-only hand-off audit  
**Status:** **Pending student review — no hand-off approved**

## 1. Scope and non-implementation statement

This audit assesses whether the student's final local FINS5545 Project A data foundation is trustworthy enough to inform a later Project B data contract. It does not migrate code or data, approve a method, implement a Project B module, or begin Stage 3B. Project A was treated as a read-only source. The only Project B outputs created for this stage are this audit and its AI provenance record.

The student confirmed that `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectA` is the same version as the final submitted `z5618000_projectA(4).zip`. That is a student-confirmed source identity, not an independent byte-for-byte ZIP comparison: the ZIP path and hash were unavailable.

## 2. Provenance and evidence hierarchy

Project B's `AGENTS.md` and official Project B requirements govern this audit. Project A's agent file and AI logs are historical evidence only. Findings use the following evidence order:

1. Project B official requirements and protected helper;
2. direct inspection of Project A source code;
3. direct, read-only measurements from the official loader and existing outputs;
4. focused test and checker results;
5. Project A report and AI logs;
6. student confirmation or code inference, explicitly labelled.

The Project A and Project B copies of `PROJECT_BRIEF.md`, all three official `context/` files, and `src/data_access.py` have matching SHA-256 hashes. The protected loader hash in both projects is `928887403C34407C99B02984CB0600CBCF2CB9F88D7404D8E81A4B40E778B710`. This is direct verification that Project A did not materially replace the official loader. It does not prove the local folder is byte-identical to the unavailable ZIP.

## 3. Project A source and artifact inventory

### Pipeline architecture

| Layer | Project A evidence | Main functions and role |
|---|---|---|
| Official loading | `src/data_access.py` | `load_equity_prices`, `load_crypto_prices`, `load_news_headlines`; official hosted ZIP, in-memory reads |
| Station 1 ETL | `src/etl.py` | `clean_price_panel`, `clean_news_headlines`, `build_dataset_inventory`, `run_station1` |
| Station 2A returns | `src/features.py` | `daily_returns`, `build_equity_calendar`, `align_crypto_returns_to_equity_calendar`, `run_station2a` |
| Station 2B news panel | `src/features.py` | `map_headlines_to_equity_calendar`, `aggregate_mapped_headlines`, `build_complete_headline_panel`, `build_news_alignment_summary`, `assemble_headline_panel` |
| Exhibits | `src/visualization.py` | Descriptive tables and four Part A figures; vocabulary membership only, no headline sentiment score |
| Orchestration | `scripts/run_part_a.py` | Calls Stations 1, 2A, 2B and exhibit writers; deliberately not executed in Stage 3A |

### Submitted artifacts inspected

- Six tables under `results/tables/`: inventory, integrity summary, return statistics, news alignment, text summary, and exhibit manifest.
- Two deterministic samples under `results/data/`: return panels and headline mapping examples.
- Four PNG exhibits under `results/figures/`, opened and inspected directly.
- The 13-page `report/report.pdf`, text-extracted and visually inspected page by page without modifying it.
- All five test modules, the read-only hand-in checker, and the materially relevant AI records `ai/01` through `ai/07` plus `ai/AI_NOTES.md`.

One architecture issue is material: `src/visualization.py` imports `fintools.figures`, while the submitted Project A folder contains no `fintools/` package and `requirements.txt` has no `fintools` dependency. Because `scripts/run_part_a.py` imports `src.visualization`, the submitted folder is not self-contained for a clean full-pipeline rerun. This issue does not affect the inspected core `src/etl.py` and `src/features.py` logic, but it prevents treating the complete Project A runner as a direct hand-off dependency.

## 4. Dataset and grain summary

All measurements below came from a read-only, in-memory load through the protected helper. No source data were saved.

| Dataset | Raw measurement | Cleaned measurement and grain | Key integrity result |
|---|---|---|---|
| Equity prices | 50,300 rows; 9 columns; 50 tickers; 10 sectors; 2020-01-02 to 2023-12-29; raw date `datetime64[s]` | 50,300 rows; unique `ticker + date`; 1,006 rows per ticker | No required-field missingness, invalid key, or duplicate ticker-date row measured |
| Crypto prices | 14,620 rows; 8 columns; 10 tickers; 2020-01-01 to 2024-01-01 | 14,610 rows after the `2023-12-31` cutoff; unique `ticker + date`; 1,461 daily rows per ticker | Exactly 10 rows occurred on 2024-01-01; 1,461/1,461 calendar dates present; 4,180 cleaned weekend rows confirm a native seven-day calendar |
| News headlines | 149,683 rows; 6 columns; 50 tickers; 10 sectors; 2020-01-01 to 2023-12-31; `datetime64[us, UTC]` | 146,836 rows; 8 columns after `source_row_order` and `source_timestamp`; grain `ticker + normalised UTC timestamp + exact title` | 23 full-row duplicate copies plus 2,824 later duplicate-key copies removed; 0 final duplicate keys; original titles preserved |

News key fields `date`, `ticker`, `sector`, `title`, and `url` had zero missing or blank values. `publisher` had 140,255 missing values and 9,428 present values; no blank strings were measured. This agrees with the official warning that publisher is often absent, and Project A retained the missingness rather than imputing it. There were 575 non-midnight timestamps. In this dataset, the measured duplicate count was still 2,847 whether the key used the full UTC timestamp or its UTC calendar date.

## 5. Checks performed

- Read the governing Project B files and all relevant Project A code in full.
- Read every submitted CSV and inspected all four PNGs.
- Extracted and visually reviewed all 13 report pages.
- Compared official-file and loader hashes across Projects A and B.
- Loaded the three official datasets in memory and independently measured schemas, counts, ranges, missingness, keys, calendars, duplicate treatment, publisher coverage, and sector mappings.
- Executed Station 1, Station 2A, and Station 2B functions in memory without calling any writer.
- Recomputed the six core CSV artifacts in memory and compared their serialised contents with the submitted files; all six matched exactly.
- Ran 32 focused ETL, return, and news-alignment tests with bytecode and pytest cache disabled; all passed.
- Ran the inspected read-only Project A hand-in checker; it reported 16 checks passed with exit code 0. This is mechanical evidence only.
- Reconciled source, generated outputs, report claims, and materially relevant AI correction logs.
- Did not run `scripts/run_part_a.py`, generate an output, import or inspect Project A's parent-repository `fintools`, install a package, or test/download a VADER resource.

## 6. Evidence-backed findings

| Classification | Finding | Evidence and Project B implication |
|---|---|---|
| **Verified pass** | Official loading pathway | Project A and Project B `src/data_access.py` are SHA-256 identical. Later Project B work should call its protected local copy rather than bypass it. |
| **Verified pass** | Equity and crypto cleaning | Counts, schemas, cutoff, completeness, missingness, and key uniqueness match code, CSVs, report, and AI records. |
| **Verified pass** | Return construction | `daily_returns` sorts by ticker/date and uses `adjClose_t / adjClose_(t-1) - 1` within ticker, with no fill and a missing first return. |
| **Verified pass** | Native-calendar crypto logic | Crypto returns were calculated on 1,461 native dates before selection of 1,006 equity dates. On 2020-01-06, the aligned ADA-USD return was the Sunday-to-Monday 7.3471406%, not the Friday-to-Monday 9.0462211%. |
| **Verified pass** | News cleaning and mapping | Titles, casing, punctuation, source timestamps, and source order are retained. UTC dates are mapped using all observed equity dates, not a weekend-only rule. Of 12,551 shifted records, 1,610 began on weekdays and 10,941 on weekends. |
| **Verified pass** | No sentiment model in Part A | The daily panel has no sentiment/VADER field. Existing word-list counts are explicitly vocabulary coverage, not headline scores or a trading signal. |
| **Verified pass** | Output reconciliation | The inventory, integrity, return-statistics, alignment-summary, return-sample, and headline-sample CSVs exactly matched in-memory regeneration. Reported core counts agree with those files. |
| **Verified issue — high for standalone Project A reproducibility; moderate for the Project B hand-off** | Undeclared external figure helper | `src/visualization.py:24` imports `fintools.figures`; Project A contains no local `fintools`, and its requirements do not declare it. `run_part_a.py` imports that module. The full submitted folder therefore cannot be assumed reproducible from its own requirements. Smallest later remediation: do not reuse the runner or visualization module as a Project B dependency; separately package/replace the helper if the student elects to repair Project A reproducibility. |
| **Verified issue — medium** | Extreme-movement review is overstated in the report | `data_integrity_summary.csv` retains 4 equity and 65 crypto adjusted-close movements of at least 25%, each with `remaining_issue_count` unchanged and `requires_later_review=True`. The report says no unresolved price problem remained and says related prices/volumes were consistent, but the submitted machine-readable evidence contains no complete row-level resolution. Smallest later remediation: review all 69 records or keep them as an explicit unresolved limitation and run sensitivity checks; never delete them merely for being large. |
| **Inconclusive** | Byte identity with final ZIP | The source identity is student-confirmed. The ZIP path and hash were unavailable, so Codex did not perform a byte comparison. |
| **Student decision required** | Approval of any hand-off | Verified logic is only a candidate baseline. No code, schema, exclusion policy, or output is approved for Project B until the student reviews this audit and authorises Stage 3B. |

## 7. Six-unmapped-observation investigation

The independent result is exactly **six** observations:

- six in the 149,683-row raw source;
- six after full-row exact duplicate removal;
- six after the final `ticker + UTC timestamp + title` deduplication.

Thus, the inherited count is not an artifact of duplicate removal. All six have valid keys, belong to AMD/Tech, and occur after the final observed equity trading date of 2023-12-29. The forward-only search therefore has no valid date inside the sample.

| Zero-based `source_row_order` | Ticker | Original UTC date | Sector | Title / deterministic identifier |
|---:|---|---|---|---|
| 14659 | AMD | 2023-12-30 | Tech | These 3 Tech Stocks Could Outperform the S&P 500 in 2024 |
| 14660 | AMD | 2023-12-30 | Tech | Is It Too Late to Buy Nvidia Stock? |
| 14661 | AMD | 2023-12-30 | Tech | 24 Spectacular Stocks to Buy Hand Over Fist for 2024 (Including Growth Stocks and Dividend Stocks) |
| 14662 | AMD | 2023-12-31 | Tech | Here's Why Nvidia and AMD Are Set to Skyrocket in 2024 |
| 14663 | AMD | 2023-12-31 | Tech | Guru Fundamental Report for AMD |
| 14664 | AMD | 2023-12-31 | Tech | Trillion-Dollar Titans: Top 3 Stocks to Grab Before They Explode in Value |

Project A code, `news_alignment_summary.csv`, the report, and AI logs agree on the count and reason. The six are excluded from the trading-day-aligned headline panel, its 146,830-headline reconciliation total, and the monthly news-volume figure. They remain in the corpus-level descriptive vocabulary calculation, whose sample is all 146,836 cleaned headlines. That use-case-specific treatment is coherent: an unmapppable record cannot enter a trading-date signal, but it can remain in a non-trading corpus description. Project B must preserve this distinction rather than apply a blanket deletion.

## 8. Code-output-report reconciliation

| Material claim | Code | Output/report/log comparison | Classification |
|---|---|---|---|
| Crypto cutoff | `CRYPTO_CUTOFF`, `clean_price_panel` | 10 raw 2024-01-01 rows; 14,610 final rows everywhere | **Verified pass** |
| Returns use adjusted close within ticker | `daily_returns` | Saved statistics and deterministic sample match regenerated values | **Verified pass** |
| Crypto is aligned only after returns | `run_station2a`, `align_crypto_returns_to_equity_calendar` | 14,610 native rows and 10,060 aligned rows; manual Monday check passes | **Verified pass** |
| News duplicates use ticker/date/title identity | `clean_news_headlines` | 23 full-row copies plus 2,824 later key copies; 2,847 total, 0 remaining | **Verified pass** |
| Holidays and weekends map forward | `calendar.searchsorted(..., side="left")` | 1,610 weekday and 10,941 weekend shifts; maximum 3 days; no backward mapping | **Verified pass** |
| Six end-of-sample headlines | `unmapped_end_of_sample` status | Code, CSV, PDF, AI logs, and independent raw-data measurement agree | **Verified pass** |
| Monthly volume versus corpus vocabulary | `build_monthly_headline_volume`; `build_news_text_outputs` | 146,830 mapped headlines in volume; all 146,836 in vocabulary | **Verified pass** |
| Complete clean-check resolution | Integrity writer versus report narrative | 69 records remain marked for later review despite report's stronger wording | **Verified issue** |
| Full-folder rerun from submitted requirements | Runner imports visualization and `fintools.figures` | Missing local/declared helper conflicts with the report's clean-folder reproduction instruction | **Verified issue** |

The Project A checker passing is not evidence against either issue: it checks structure and required filenames, not import closure or empirical validation.

## 9. Handoff candidate assessment

These are recommendations for student review, not migration approval.

| Component | Project A source/function | Evidence inspected | Observed behaviour | Candidate status | Reason, risk, and student decision still required |
|---|---|---|---|---|---|
| Official data loading | `src/data_access.py::load_*` | Hash, source, in-memory load | Exact protected helper; raw data not committed | `reuse candidate` | Use Project B's protected identical copy. Student must approve the future data contract. |
| Equity cleaning | `src/etl.py::clean_price_panel` | Source, raw measurements, inventory/integrity | Unique complete panel; deterministic types/order | `adapt/recompute candidate` | Recompute through Project B; resolve or disclose the four extreme flags. |
| Crypto cutoff | `CRYPTO_CUTOFF`; `clean_price_panel` | Source and raw dates | Removes exactly ten 2024-01-01 rows | `reuse candidate` | Rule is verified; student must approve its explicit Project B assertion. |
| Native-calendar returns | `daily_returns`; `run_station2a` | Source, tests, manual value, CSV match | `adjClose`, within ticker, no fill, first return missing | `adapt/recompute candidate` | No full return artifact is submitted for copying; recompute and add Project B regression checks. |
| Combined calendar alignment | `align_crypto_returns_to_equity_calendar` | Source, tests, 10,060-row measurement | Selects already-calculated crypto returns on equity dates | `reuse candidate` | Preserve asset ordering and native-return semantics; student approval required. |
| Headline deduplication | `clean_news_headlines` | Source, raw/clean counts, title comparison | 2,847 total key duplicates removed deterministically; text preserved | `reuse candidate` | Freeze the normalised UTC timestamp/date key in the future contract. |
| Timezone normalisation | `_normalise_news_timestamps` | Source and dtypes | Raw microsecond UTC to nanosecond UTC; source representation retained | `reuse candidate` | Preserve both normalised timestamp and auditable source field. |
| Forward trading-date mapping | `map_headlines_to_equity_calendar` | Source, tests, raw measurement | Same observed date or next observed date; covers holidays; never backward | `reuse candidate` | Part B must still apply its separately governed information lag. |
| Six-unmapped handling | Mapping, panel, text exhibit functions | All six rows, outputs, report, logs | Excluded from aligned/volume uses; retained for corpus description | `adapt/recompute candidate` | Student must approve use-case-specific treatment and disclosure wording. |
| Headline text preservation | `clean_news_headlines`; aggregation | Source-to-clean comparison and tests | Casing, punctuation, whitespace, and order retained | `reuse candidate` | Required for later scoring; no score or text normalisation approved. |
| Validation tests | `tests/test_etl.py`, `test_features.py`, `test_news_alignment.py` | Source and independent run | 32 core tests passed; mostly synthetic | `adapt/recompute candidate` | Add real-data assertions, six-row regression, leakage/lag, schema, and deterministic-output tests in Project B. |
| Derived schemas | Station 1/2 dataclasses and CSV samples | Source, tables, samples | Schemas are clear, but only small data samples were saved | `adapt/recompute candidate` | Stage 3B must specify and regenerate full in-memory/derived inputs; no copying is approved. |
| Part A runner and figures | `scripts/run_part_a.py`; `src/visualization.py` | Source, requirements, folder inventory | Writes Part A outputs and relies on undeclared external helper | `reject` | Not a Project B dependency; resolve separately only if the student authorises a Project A repair. |

## 10. Risks, limitations, and unresolved conflicts

- The final ZIP identity is student-confirmed, not hash-verified.
- No full cleaned or return dataset was submitted under `results/`; only samples and summaries exist. A later hand-off must recompute rather than copy a purported final panel.
- The 69 extreme-movement flags remain machine-readably unresolved despite stronger report wording.
- The full Project A runner is not self-contained because of its undeclared `fintools.figures` import. Full tests and the runner were not executed because Stage 3A forbade broader-repository inspection and output regeneration.
- The loader's first sandboxed attempt failed because network access to both official hosts was blocked. An explicitly authorised network retry succeeded in memory. Streamlit reported its documented memory-cache warning; no data file was saved.
- Project A's tests validate core transformations well, but they do not substitute for Project B leakage, lag, decision-date, and schema tests.
- VADER-resource availability and any sentiment methodology were deliberately not tested in Stage 3A.

## 11. Proposed inputs for a future Project B data contract

Subject to student approval, Stage 3B could freeze these inputs and assertions:

1. Project B loads all three sources through its protected `src/data_access.py`.
2. Equity keys are unique `ticker + date`, with 50 tickers, 10 sectors, 1,006 observed equity dates, and `adjClose` retained.
3. Crypto is capped at 2023-12-31, remains on 1,461 native calendar dates for return calculation, and is only then selected onto the 1,006 equity dates.
4. Returns are decimal simple returns calculated within ordered ticker panels with no fill and one missing first return per native ticker.
5. Cleaned news retains `date`, `ticker`, `sector`, `title`, `url`, `publisher`, `source_row_order`, and `source_timestamp`; title values remain exact.
6. Headline identity and retention order are explicit and tested. Current evidence supports `ticker + normalised UTC timestamp + exact title`, whose measured result equals the UTC-calendar-date variant in this dataset.
7. Mapping uses the UTC calendar date and the same-or-next observed equity-date rule. No mapped date precedes its source date.
8. The six identified AMD records remain disclosed and absent from trading-date features, while non-trading corpus descriptions may retain them.
9. Full schema, row-count, key, order, boundary-date, and deterministic-rerun assertions are machine-readable.
10. The 69 extreme observations are either revalidated or explicitly carried as a limitation with sensitivity evidence.

## 12. Student decisions required before Stage 3B

1. Accept, reject, or correct this audit and its classifications.
2. Decide whether Stage 3B may recompute Project B inputs from the official loader using the audited Station 1/2 logic as a design reference; direct copying remains unauthorised.
3. Approve the exact news duplicate key and deterministic retention rule for the Project B data contract.
4. Approve the use-case-specific treatment of the six end-of-sample records.
5. Decide whether the 69 extreme movements require a complete targeted validation before portfolio work.
6. Decide whether Project A's standalone `fintools.figures` dependency should be repaired separately; it must not silently become a Project B dependency.
7. Approve the final Project B input schemas and validation thresholds. No sentiment, portfolio, fusion, app, or innovation choice is part of this decision.

## 13. Status

**Pending student review — no hand-off approved.** Stage 3B has not been authorised or started.
