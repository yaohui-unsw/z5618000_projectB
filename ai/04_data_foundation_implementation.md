# Stage 4A — Data Foundation Implementation and Contract Tests

**Date:** 2026-08-14  
**Status:** Pending student review

## Objective and authorisation

Implement and test only the Project B input-data foundation against the student-accepted contract. No portfolio optimisation, sentiment scoring, finance lexicon, fusion, model output, figure, Streamlit, report, deployment, Git operation, or Stage 4B work was authorised or performed.

The student stated exactly:

> “I accept `docs/data_contract.md` as the frozen Project B input data contract. I accept the Stage 3B benchmarks, source/display sector mapping, news identity and mapping rules, six-unmapped policy, no-news versus neutral-news semantics, lag rule, and retention of the 69 extreme observations. I authorise Stage 4A only: implement and test the Project B data foundation against the frozen contract. This does not authorise portfolio optimisation, sentiment scoring, a finance lexicon, fusion, model outputs, figures, Streamlit, report writing, deployment, Git operations, or Stage 4B.”

## Complete operational prompt

The following is the complete prompt received for this cycle:

```text
You are working on FINS5545 Project B.

The student has reviewed the Stage 3B artifacts and states exactly:

“I accept `docs/data_contract.md` as the frozen Project B input data contract. I accept the Stage 3B benchmarks, source/display sector mapping, news identity and mapping rules, six-unmapped policy, no-news versus neutral-news semantics, lag rule, and retention of the 69 extreme observations. I authorise Stage 4A only: implement and test the Project B data foundation against the frozen contract. This does not authorise portfolio optimisation, sentiment scoring, a finance lexicon, fusion, model outputs, figures, Streamlit, report writing, deployment, Git operations, or Stage 4B.”

This is Workflow Stage 4A only: Data Foundation Implementation and Contract Tests.

## Exact workspace and interpreter

Project root and terminal working directory must both resolve exactly to:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Use only:

C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe

Do not create an environment or install dependencies. Do not inspect Project A, sibling folders, or the broader repository.

## File boundary

Existing files authorised for modification:

- `docs/data_contract.md`
- `ai/03_data_contract_freeze.md`
- `src/etl.py`
- `src/features.py`

New files authorised:

- `src/validation.py`
- `scripts/validate_data_contract.py`
- `tests/test_data_contract.py`
- `tests/test_data_foundation.py`
- `ai/04_data_foundation_implementation.md`

Do not modify or create anything else. In particular, do not modify:

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `context/*`
- `src/data_access.py`
- `src/portfolios.py`
- `src/sentiment.py`
- `src/fusion.py`
- `scripts/run_part_b.py`
- `streamlit_app.py`
- requirements files
- `results/*`
- `report/*`
- `.idea/*`
- Git state

Do not create raw-data files, model outputs, placeholder outputs, caches, bytecode, temporary project scripts, or environments.

## Required reading

Read completely:

- `AGENTS.md`
- `docs/data_contract.md`
- `ai/03_data_contract_freeze.md`
- `context/DATA_GUIDE.md`
- relevant Station 1–3 and rubric sections of `PROJECT_BRIEF.md`
- `src/data_access.py`
- current `src/etl.py`
- current `src/features.py`
- current tests
- `scripts/check_handin.py`

The frozen data contract controls the implementation. Do not silently revise it to fit code.

## Close Stage 3B

After recording the student’s exact acceptance:

1. Change the status in `docs/data_contract.md` from pending review to:
   `Accepted and frozen by student — 2026-08-14`
2. Preserve the substantive contract unchanged.
3. Append a chronological closure section to `ai/03_data_contract_freeze.md`.
4. Record that Stage 4A data-foundation implementation only was authorised.

## Implementation requirements

### `src/etl.py`

Implement deterministic functions for:

- clean equity prices;
- clean crypto prices with the exact `date <= 2023-12-31` cutoff;
- cleaned news with:
  - zero-based `source_row_order` assigned before sorting;
  - auditable UTC `source_timestamp`;
  - separate UTC calendar `source_date_utc`;
  - exact-title preservation;
  - duplicate identity `ticker + source_timestamp + exact title`;
  - retention of the smallest `source_row_order`.

Always make a deep copy of loader-returned DataFrames before mutation because the official loader caches mutable frames.

Do not save raw or cleaned data.

### `src/features.py`

Implement pure, deterministic functions for:

- simple decimal returns using `adjClose`;
- returns within ticker with no filling;
- equity returns;
- native-calendar crypto returns;
- selection of already-calculated crypto returns onto the equity calendar;
- the combined 60-asset matrix in frozen order;
- same-or-next-observed-equity-date headline mapping;
- explicit `same_day`, `forward`, and `unmapped_end_of_sample` statuses;
- mapped headline table;
- complete 50-ticker × 1,006-trading-day coverage panel;
- `headline_count` and `has_news` without fabricating a zero sentiment score.

Use stable sorting. Preserve the starter public function names where practical, while adding clearly named functions where necessary.

Never calculate crypto returns after first restricting prices to equity dates.

### `src/validation.py`

Create reusable validation logic implementing the frozen `BLOCK`, `WARN`, and `PASS` rules.

Requirements:

- a BLOCK condition raises or produces a deterministic failing status;
- WARN conditions remain visible and never delete observations;
- validation results must be machine-readable Python objects;
- centralise frozen ticker order, sector values/display mapping, benchmark counts, dates, and six-record identifiers;
- validate uniqueness, schemas, membership, ordering, missingness, boundaries, mapping direction, reconciliation, deterministic reruns, and extreme retention;
- do not implement sentiment-lag validation that requires an unauthorised sentiment model; record it as deferred to that stage.

### `scripts/validate_data_contract.py`

Create a lightweight, reproducible input-validation command that:

- loads only through `src/data_access.py`;
- runs the implemented input and feature pipeline;
- prints a concise PASS/WARN/BLOCK summary;
- exits non-zero on any BLOCK;
- supports machine-readable JSON output to stdout if practical;
- writes no data or results files.

Do not add machine-specific absolute paths to committed code.

## Tests

### Real-data contract tests

Test at least:

- all frozen schemas, dtypes, counts, date boundaries and memberships;
- price and news key uniqueness;
- crypto cutoff and exact ten-row removal;
- 50 and 10 legitimate first-return missing values;
- 10,060 aligned crypto rows with no missing returns;
- combined 1,006 × 60 structure and fixed asset order;
- 146,836 cleaned headlines;
- 146,830 mapped plus exactly six unmapped;
- exact source orders 14659–14664 and their endpoint status;
- 50,300 coverage rows and 12,338 no-news rows;
- headline-count reconciliation;
- 4 equity and 65 crypto extreme observations retained.

### Synthetic tests

Test at least:

1. Native-calendar crypto return calculation, proving Monday uses Sunday-to-Monday rather than Friday-to-Monday.
2. Same-day, weekend, weekday-holiday and end-of-sample headline mapping.
3. Never-backward mapping.
4. Exact-title duplicate identity and earliest-source-row retention.
5. Preservation of casing, punctuation and whitespace.
6. No-news rows represented as missing information rather than a fabricated neutral score.
7. Deterministic output ordering and rerun equality.
8. No mutation of cached/raw input DataFrames.

Do not create a fake sentiment score merely to test neutral sentiment. Full neutral-score and trading-lag tests remain deferred to the authorised sentiment stage.

## Validation commands

Use the explicit interpreter and `-B`.

Run:

& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q

& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_data_contract.py

& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py

If pytest is unavailable, stop and report it; do not install anything.

A network/sandbox access failure is not a data discrepancy. Retry only through the unchanged official loader pathway. Do not patch URLs or bypass `src/data_access.py`.

## AI workflow record

Create `ai/04_data_foundation_implementation.md` containing:

- date, objective and exact student authorisation;
- complete operational prompt;
- files read and changed;
- ChatGPT, student and Codex roles;
- implementation decisions;
- commands and exact exit codes;
- test inventory and results;
- genuine errors and corrections, if any;
- unresolved or deferred tests;
- manifest boundary evidence;
- status `Pending student review`.

Do not invent an AI error or student correction.

## Efficiency instruction

Prioritise executable correctness and tests over prose polishing. One pre-edit and one final boundary audit are sufficient. Do not repeat already accepted Stage 3B exploratory analysis unnecessarily.

## Final response

Report:

- guard result;
- Stage 3B closure;
- functions implemented;
- real and synthetic test results;
- validation-script result;
- checker result;
- exact files modified and created;
- boundary result;
- limitations and deferred tests;
- status:
  `Stage 4A data foundation implemented; pending student review. No model work authorised.`

Stop after Stage 4A. Do not begin portfolios, sentiment, fusion, outputs, figures, Streamlit, report writing, or deployment.
```

## Roles and provenance

- **Student:** reviewed and accepted the Stage 3B contract, supplied the exact authorisation, limited the scope, and retains review and progression control.
- **ChatGPT:** its earlier prompt-structuring and review assistance is recorded in the preceding Stage 2–3 logs; it did not execute the local implementation or independently approve these results.
- **Codex:** verified the exact local workspace and interpreter, read the governing files, implemented only the authorised data foundation, ran local and protected-loader checks, corrected an identified validation gap, and recorded the evidence.

## Files read

- `AGENTS.md`
- `docs/data_contract.md`
- `ai/03_data_contract_freeze.md`
- `context/DATA_GUIDE.md`
- the relevant Station 1–3 and rubric sections of `PROJECT_BRIEF.md`
- `src/data_access.py`
- the pre-edit `src/etl.py` and `src/features.py`
- the pre-edit test suite (`tests/test_smoke.py`)
- `scripts/check_handin.py`

Project A, sibling projects, the broader repository, `.git`, and unlisted external files were not inspected.

## Files changed

Modified as authorised:

- `docs/data_contract.md`
- `ai/03_data_contract_freeze.md`
- `src/etl.py`
- `src/features.py`

Created as authorised:

- `src/validation.py`
- `scripts/validate_data_contract.py`
- `tests/test_data_contract.py`
- `tests/test_data_foundation.py`
- `ai/04_data_foundation_implementation.md`

No other authored project file was deliberately changed or created.

## Implementation decisions and evidence

- All three official loader returns are detached with deep copies before mutation.
- Equity and crypto cleaners enforce canonical schemas, semantic dtypes, stable date/ticker order, and the accepted crypto endpoint.
- News cleaning assigns source order before sorting, normalises a separate UTC timestamp/date, preserves exact titles, and keeps the earliest canonical duplicate identity.
- Returns are simple decimals calculated by ticker on native rows with no fill. Crypto returns are calculated before selecting equity-calendar dates.
- The combined matrix has the accepted equity-then-crypto order.
- Headline mapping uses the same or next observed equity date, never maps backward, and exposes all three accepted statuses and calendar-day distance.
- The coverage grid represents no news with `headline_count = 0` and `has_news = false`; it contains no score or fabricated neutral value.
- `ValidationResult` and `ValidationReport` provide deterministic machine-readable PASS/WARN/BLOCK results. Constants centralise accepted universes, display mapping, boundaries, counts, and six endpoint identifiers.
- The command supports human-readable output and `--json`, writes nothing, and exits nonzero if any BLOCK exists.

## Test inventory

The real-data tests cover schemas and dtypes; counts, keys, dates, memberships, and ordering; the ten-row crypto cutoff; native and aligned return missingness; the 1,006 × 60 combined matrix; exact news deduplication; 146,830 mapped plus the six endpoint records; the 50,300-row coverage grid and 12,338 no-news rows; count reconciliation; source/display sectors; and retention/internal consistency of the 4 equity and 65 crypto extremes.

The synthetic tests cover Sunday-to-Monday crypto returns before equity alignment; same-day, weekend, weekday-holiday, endpoint, and never-backward mapping; exact-title duplicate identity and earliest-row retention; casing, punctuation, and whitespace preservation; no-news without a fake score; fixed ordering and deterministic reruns; and non-mutation of source frames.

Neutral-score and trading-lag tests that require an actual sentiment score remain deliberately deferred. No fake score was introduced.

## Commands, outputs, and exit codes

The PyCharm environment was queried before every Python command and consistently returned Python 3.13.13 at the authorised executable.

### Pytest — first sandboxed attempt

Exact Python command (pytest cache disabled through `PYTEST_ADDOPTS=-p no:cacheprovider`):

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q
```

Exit code: `1`

Exact summary:

```text
1 failed, 8 passed, 7 errors in 1.98s
EXIT_CODE=1
```

All failures/errors came from the protected loader's HTTPS request being denied by the sandbox (`WinError 10013`). The eight synthetic tests passed. This was an access failure, not a measured data discrepancy.

### Pytest — authorised network retry and final run

The unchanged command and unchanged official loader pathway were retried with network permission. The final post-correction result was:

```text
................                                                         [100%]
16 passed in 28.14s
EXIT_CODE=0
```

An earlier successful retry before the final dtype-gate refinement also returned `16 passed in 32.15s`, exit code `0`.

### Standalone contract validation — final

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_data_contract.py
```

Exit code: `0`

Exact stdout:

```text
Data contract validation: PASS=82 WARN=6 BLOCK=0
WARN missing_publishers_retained: Missing publisher is allowed and does not remove a headline.
WARN legitimate_first_returns: First native return per ticker remains missing; no fill was applied.
WARN no_news_rows_retained: No-news ticker-days remain explicit missing-information states.
WARN equity_extremes_retained: Extreme returns are retained unchanged and require later, separately labelled sensitivity evidence.
WARN crypto_extremes_retained: Extreme returns are retained unchanged and require later, separately labelled sensitivity evidence.
WARN sentiment_lag_deferred: Sentiment-score neutrality and decision-date lag validation are deferred until an authorised sentiment stage; Stage 4A creates no score.
CONTRACT STATUS: PASS
EXIT_CODE=0
```

Streamlit's cache wrapper also emitted benign “No runtime found, using MemoryCacheStorageManager” warnings to stderr because the protected loader was invoked outside Streamlit. They did not alter the data or exit status. An earlier pre-refinement validation run returned `PASS=64 WARN=6 BLOCK=0`, exit code `0`.

### Hand-in checker — final

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exit code: `0`

Exact output:

```text
17 checks passed.
6 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
  [WARN] results/ has no figures or tables yet - save your exhibits there
  [WARN] expected output results/data/fund_returns.csv not found - use this exact name so markers can find it
  [WARN] expected output results/data/fund_weights.csv not found - use this exact name so markers can find it
  [WARN] expected output results/data/sector_sentiment_index.csv not found - use this exact name so markers can find it
  [WARN] expected output results/tables/performance_metrics.csv not found - use this exact name so markers can find it
All checks passed - ready to zip and deploy.
EXIT_CODE=0
```

This checker result is mechanical structure evidence only. It is not substantive project completion, and the six expected unfinished-output reminders were not suppressed with placeholders.

## Genuine errors and corrections

1. The initial sandboxed real-data test run could not reach either official loader host. Codex did not patch the URL or bypass `src/data_access.py`; the same command was retried with authorised network access and passed.
2. After the first passing execution, Codex's focused review found that real-data tests checked the contracted dtypes but the reusable validator did not yet produce a BLOCK for every dtype mismatch. Codex added explicit dtype and required-field gates, tightened mapping/news ordering gates, and made the coverage ticker dtype conform to the frozen string schema. The complete suite and validator were rerun successfully.

No AI error, student correction, or test result was invented.

## Manifest and boundary evidence

The pre-edit read-only manifest included `.idea`, excluded `.git`, environments, caches, bytecode, and compiled files, and recorded:

- file count: `41`;
- canonical SHA-256 manifest digest: `54ACC186E478B0A738F55279150BE42D17DEB2FF490AEEBF355677C0AD702EE1`;
- reparse points: `0`.

Immediately before creating this provenance file, the matching 45-file snapshot had digest `D777962E1E824337840764F8B922BE3ABE72087C471ED4423C86BB770FB6A146`. Path/hash comparison showed only the four authorised existing files modified and the first four authorised new files added. No existing file was removed; `.idea` hashes were unchanged; and no raw data, result, placeholder, cache, bytecode, environment, or temporary script appeared.

This log is the fifth authorised new file. Its own final hash cannot be embedded without changing that hash; the authoritative final 46-file post-edit manifest and complete pre/post path comparison will therefore be calculated after this last edit and reported to the student without another project mutation.

## Limitations and deferred work

- The official source bundle remains remotely loaded and in memory; availability depends on its hosts. No raw or cleaned source data was persisted.
- The 69 extreme observations pass internal source-row checks and remain unchanged, but are not economically/event verified. Later portfolio sensitivity evidence remains required.
- No sentiment score exists, so a genuine neutral-news score and the decision-date trading lag cannot yet be tested. The validator records this as deferred rather than manufacturing a score.
- Model-dependent output schemas and tests remain deferred to their separately authorised implementation stages.
- No portfolio, sentiment, lexicon, fusion, result, figure, Streamlit, report, deployment, Git, or Stage 4B work was performed.

## Student-review status and next action

**Pending student review.** The student must review the implementation, tests, and evidence and explicitly accept, reject, or request corrections. No later stage is authorised automatically.

## Final student acceptance — Stage 4A closed

**Date:** 2026-08-14

The student stated exactly:

> “I accept the Stage 4A implementation, test evidence, validation results, genuine error-and-correction record, and file-boundary audit. I authorise Workflow Stage 4B only: document and freeze the out-of-sample portfolio and backtest design before any portfolio result is calculated. No implementation, optimisation run, model output, figure, sentiment work, fusion, Streamlit, report writing, deployment, or Git operation is authorised.”

This acceptance closes Stage 4A without approving any portfolio method result, implementation output, or empirical conclusion.

**Final status:** Stage 4A accepted and closed; Stage 4B authorised for pre-result portfolio-design documentation only.
