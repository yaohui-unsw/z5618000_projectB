# AI workflow record — Project B input data contract

**Date:** 2026-08-14 (Australia/Sydney)  
**Stage:** Workflow Stage 3B — data-contract documentation only  
**Status:** Pending student review — no implementation authorised

## Objective

Record the student's final acceptance of Stage 3A, independently confirm the accepted source benchmarks through the protected Project B loader, perform the authorised bounded internal-consistency review of the 69 extreme adjusted-close movements, and document a proposed frozen input contract. This stage did not implement ETL, tests, portfolios, sentiment, a finance lexicon, fusion, Streamlit, results, figures, or report content.

## Student authorisation

The student stated exactly:

> “I accept the Stage 3A audit and its candidate classifications. I approve the seven decisions outlined above and authorise Stage 3B to finalise the Project B data contract. Codex is permitted to record my acceptance at the end of `ai/02_project_a_handoff_audit.md`. Only two files may be created: `docs/data_contract.md` and `ai/03_data_contract_freeze.md`. No authorisation is granted for modifying source code, generating model outputs, or commencing work on portfolios, sentiment analysis, fusion strategies, or Streamlit.”

## Roles and provenance

- **ChatGPT:** helped structure the staged workflow and operational prompt supplied in this chat.
- **Student:** accepted the Stage 3A audit and classifications, made the seven data-governance decisions, authorised the exact documentation scope, and retains approval authority for the proposed contract and every later stage.
- **Codex:** verified the local Project B boundary, read the governing and accepted-audit evidence, performed read-only in-memory checks through the protected Project B loader, appended the authorised Stage 3A closure, drafted the proposed contract and this log, and did not inspect Project A or implement source code.

## Seven student decisions

1. Accept the Stage 3A audit and its candidate classifications.
2. Recompute Project B inputs through protected `src/data_access.py`; copy no Project A code, CSV, or panel.
3. Use `ticker + normalised UTC source timestamp + exact title` as news identity; preserve `source_row_order` and auditable UTC timestamp; use UTC calendar date separately for mapping.
4. Exclude the six AMD endpoint headlines from trading-day-aligned and trading uses, while permitting disclosed non-trading corpus descriptions.
5. Retain all 69 adjusted-close extremes; do not delete, winsorise, replace, or alter base data; complete the bounded internal review now and defer portfolio sensitivity analysis.
6. Do not repair, import, or depend on Project A's `fintools.figures`; create Project B figures only in a later authorised stage.
7. Freeze input schemas, keys, ordering, dates, missingness semantics, and gates only; approve no portfolio, sentiment, fusion, app, or empirical conclusion.

## Complete operational prompt received

````text
You are working on FINS5545 Project B.

This is Workflow Stage 3B only: record the student's Stage 3A acceptance and finalise a proposed Project B input data contract for student review.

This is not DFF Station 3 implementation. Do not implement or modify ETL, portfolio, sentiment, finance lexicon, fusion, Streamlit, results, figures, tests, or report content.

## Student acceptance and authorisation

The student stated exactly:

“I accept the Stage 3A audit and its candidate classifications. I approve the seven decisions outlined above and authorise Stage 3B to finalise the Project B data contract. Codex is permitted to record my acceptance at the end of `ai/02_project_a_handoff_audit.md`. Only two files may be created: `docs/data_contract.md` and `ai/03_data_contract_freeze.md`. No authorisation is granted for modifying source code, generating model outputs, or commencing work on portfolios, sentiment analysis, fusion strategies, or Streamlit.”

The seven approved decisions are:

1. Accept the Stage 3A audit and its candidate classifications.
2. Project B will recompute its inputs through the protected official `src/data_access.py`; do not copy Project A code, CSVs, or panels.
3. The canonical news duplicate identity is:
   `ticker + normalised UTC source timestamp + exact title`.
   Preserve `source_row_order` and the original/auditable UTC source timestamp. Use the UTC calendar date separately for trading-day mapping.
4. The six verified AMD end-of-sample headlines are excluded from trading-day-aligned features, sentiment signals, and trading uses, but may remain in non-trading corpus-level vocabulary descriptions, with disclosure.
5. Retain all 69 flagged extreme adjusted-close movements. Do not delete, winsorise, replace, or alter base data merely because returns are large. Perform a bounded automated internal-consistency review now; reserve portfolio sensitivity analysis for a later authorised model stage.
6. Do not repair, import, or depend on Project A’s `fintools.figures`; Project B will create its own figures later.
7. Stage 3B freezes input schemas, keys, ordering, boundary dates, missingness semantics, and validation thresholds only. It does not approve or implement a portfolio, sentiment method, fusion rule, app, or empirical conclusion.

## Exact workspace

Project B root and terminal working directory must both resolve exactly to:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Verified interpreter:

C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe

Do not inspect Project A again, any sibling folder, or the broader `fins-agent` repository. Stage 3A already provides the approved audit evidence.

If the workspace guard fails, stop without reading or editing project files.

## Authorised file boundary

One existing file may be appended only:

- `ai/02_project_a_handoff_audit.md`

Exactly two new files may be created:

- `docs/data_contract.md`
- `ai/03_data_contract_freeze.md`

Before editing, verify that both new paths do not already exist. If either exists, stop rather than overwrite it.

Do not modify any other file, including:

- `AGENTS.md`
- `ai/01_project_governance_and_baseline.md`
- official files under `context/`
- `PROJECT_BRIEF.md`
- `README.md`
- `src/*`
- `scripts/*`
- `tests/*`
- `results/*`
- `report/*`
- `.idea/*`
- requirements files
- Streamlit files
- Git state

Do not create project-local temporary scripts, caches, bytecode, raw data, placeholder outputs, environments, or dependency files. Temporary validation code may exist only outside the project and must not write data.

## Required reading

Read completely:

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `context/verify_ai_output.md`
- `docs/project_a_handoff_audit.md`
- `ai/02_project_a_handoff_audit.md`
- `src/data_access.py`
- `scripts/check_handin.py`

Use the official Project B files as the requirements authority and the accepted Stage 3A audit as evidence. Do not infer additional Project A facts.

## Pre-edit evidence

Before editing:

1. Capture a read-only SHA-256 manifest of all existing Project B files, including `.idea`, while excluding `.git`, caches, bytecode, and environments.
2. Store working manifest material outside the project.
3. Run:

& "C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe" -B scripts/check_handin.py

Record the exact exit code and output.

## Close Stage 3A

Append a concise section to `ai/02_project_a_handoff_audit.md` titled:

`Final student acceptance — Stage 3A closed`

Record:

- the student’s exact acceptance and authorisation above;
- acceptance of the Stage 3A audit and candidate classifications;
- the seven approved decisions;
- that this does not approve implementation or empirical conclusions;
- final status:
  `Stage 3A accepted and closed; Stage 3B authorised for data-contract documentation only.`

Do not rewrite earlier history.

## Bounded data verification

Use the protected Project B `src/data_access.py` only, with the verified interpreter, `-B`, and in-memory operations.

No raw data may be saved.

Confirm the accepted Stage 3A benchmarks:

- equity: 50,300 rows, 50 tickers, 10 sectors, 1,006 dates, 2020-01-02 to 2023-12-29;
- crypto: 14,620 raw rows, ten 2024-01-01 rows, 14,610 after cutoff, 10 tickers and 1,461 native dates;
- news: 149,683 raw rows, 146,836 after deterministic deduplication, 2,847 removed, 50 tickers and 10 sectors;
- mapped headlines: 146,830;
- exactly six end-of-sample unmapped records;
- equity returns: one missing first return per ticker;
- native crypto returns: one missing first return per ticker;
- aligned crypto long panel: 10,060 ticker-date rows.

If a benchmark differs, do not force it. Record the discrepancy and stop Stage 3B without declaring the contract frozen.

For the 69 extreme observations identified by:

`abs(adjClose_t / adjClose_(t-1) - 1) >= 0.25`

perform a bounded automated internal-consistency review:

- confirm the measured split of 4 equity and 65 crypto observations;
- ticker/date uniqueness;
- finite and strictly positive current and previous `adjClose`;
- finite/non-negative volume where present;
- finite calculated returns;
- no evidence that the observation arose from filling missing prices;
- retain every observation regardless of result.

Do not conduct external event/news searches. Do not claim the movements are economically verified. Classify them as internally valid observations retained for base analysis, with economic/event validation unavailable and later sensitivity analysis required.

## Create `docs/data_contract.md`

Write concise professional English. Mark it:

`Proposed frozen input contract — pending student review`

It must contain the following.

### 1. Authority and scope

- Project B official files control.
- Stage 3A audit is accepted evidence.
- All data load through protected Project B `src/data_access.py`.
- Project B recomputes; nothing is copied from Project A.
- No raw data is committed.
- This contract governs inputs only and approves no model.

### 2. Canonical raw/clean schemas and grain

Define exact column names, types, keys, expected counts and date boundaries for:

- clean equity prices;
- clean crypto prices;
- cleaned news;
- equity returns;
- native-calendar crypto returns;
- equity-calendar-aligned crypto returns;
- combined return matrix;
- mapped headlines;
- complete ticker-trading-day headline panel.

Use actual official source column names such as `adjClose`; do not silently rename protected raw fields.

### 3. Deterministic ordering

Record the exact measured ticker and sector lists.

Freeze:

- equity tickers in deterministic lexicographic order;
- crypto tickers in deterministic lexicographic order;
- combined assets as equity tickers followed by crypto tickers;
- dates ascending;
- long panels ordered by date then ticker unless a specific operation requires ticker then date;
- sector display order explicitly listed from the official guide.

Do not leave ordering dependent on dataframe encounter order.

### 4. Price and return rules

- Crypto cutoff: `date <= 2023-12-31`.
- Use `adjClose`.
- Simple decimal return:
  `adjClose_t / adjClose_(t-1) - 1`.
- Calculate within ticker, sorted by date.
- Use no fill, backward fill, or forward fill.
- Preserve the first missing return per native ticker.
- Calculate crypto returns on the 1,461-date native calendar before selecting them onto the 1,006-date equity calendar.
- Combined panel uses the equity trading calendar.
- Never merge price levels first and then calculate crypto returns.

### 5. News identity, preservation and mapping

Freeze:

- retain `source_row_order`;
- retain an auditable UTC `source_timestamp`;
- preserve title casing, punctuation, whitespace and exact text;
- deterministic duplicate key:
  `ticker + normalised UTC source timestamp + exact title`;
- retain the earliest `source_row_order`;
- derive a separate UTC calendar date for mapping;
- map to the same observed equity trading date or the next observed equity trading date;
- never map backward;
- include explicit `map_status`, `mapped_trade_date`, and mapping-day distance;
- disclose the six verified AMD end-of-sample records.

Do not deduplicate using mapped date or ticker-date alone.

### 6. No-news, neutral-news and lag semantics

Freeze these distinct states:

- `has_news = false`, `headline_count = 0`: no information; future sentiment value must be missing, not zero;
- `has_news = true` with a future score of exactly zero: scored-neutral news;
- missing publisher remains missing and is not a reason to discard a headline;
- sentiment scoring remains unauthorised in Stage 3B;
- any later tradable sentiment signal must be shifted by at least one observed equity trading day;
- information aligned to Monday is first usable for Tuesday’s decision;
- no feature for decision date `t` may use a source aligned later than the previous observed trading date.

### 7. Six-unmapped policy

List the six deterministic source orders and dates from the accepted audit.

Freeze:

- exclusion from mapped headline panels, sentiment, news-volume aligned to trading dates, fusion, and trading signals;
- retention in valid non-trading corpus-level descriptions such as vocabulary counts;
- reconciliation:
  `146,836 cleaned = 146,830 mapped + 6 unmapped`;
- no forced mapping beyond 2023-12-29.

### 8. Extreme-observation policy

Record:

- threshold and measured 4/65 split;
- results of the bounded consistency review;
- all 69 remain in canonical base data;
- no winsorisation or deletion in base results;
- they remain a disclosed limitation;
- later portfolio work must include sensitivity evidence, clearly labelled and separate from canonical results.

### 9. Validation gates

Create a compact table of `BLOCK`, `WARN`, and `PASS` rules.

At minimum, block future execution for:

- wrong workspace or loader;
- missing required columns;
- invalid/null ticker or date keys;
- duplicate price keys;
- duplicate cleaned-news keys;
- non-positive or non-finite `adjClose`;
- unexpected cutoff rows;
- unexpected ticker/sector membership;
- wrong expected benchmark counts;
- title mutation;
- backward headline mapping;
- mapped date outside the equity calendar;
- six-record reconciliation failure;
- future information or lag failure;
- nondeterministic order or rerun mismatch.

Warnings—not automatic deletion—include:

- missing publisher;
- no-news ticker-days;
- the 69 retained extremes;
- legitimate first-return missingness.

### 10. Future test matrix

Specify the minimum real-data and synthetic tests later implementation must create:

- schema/count/key tests;
- boundary dates;
- native crypto return regression;
- six-record regression;
- weekend and weekday-holiday forward mapping;
- no-news versus neutral-news;
- one-trading-day lag and leakage;
- asset ordering;
- deterministic rerun;
- extreme-value retention;
- output schema checks.

Do not create those tests now.

### 11. Deferred model and output decisions

Record the four required filenames:

- `results/data/fund_returns.csv`
- `results/data/fund_weights.csv`
- `results/data/sector_sentiment_index.csv`
- `results/tables/performance_metrics.csv`

State that their detailed model-dependent schemas will be frozen only in their authorised implementation stages. Do not invent portfolio methods, parameter values, sentiment scores, or results now.

### 12. Contract status

End with:

`Pending student review — no implementation authorised.`

## Create `ai/03_data_contract_freeze.md`

Include:

- date and objective;
- student’s exact authorisation;
- complete operational prompt verbatim;
- files read;
- roles and provenance;
- the seven student decisions;
- in-memory commands, exit codes and measured benchmarks;
- the 69-record review evidence;
- all proposed contract rules;
- discrepancies, genuine AI/tool errors and corrections, if any;
- pre/post checker results;
- manifest boundary evidence;
- limitations;
- student-review status;
- next action requiring explicit student approval.

Do not invent an error merely for the AI workflow mark.

## Post-edit validation

Run the Project B checker again using the same explicit interpreter.

Capture a post-edit manifest and prove:

- only `ai/02_project_a_handoff_audit.md` changed;
- only `docs/data_contract.md` and `ai/03_data_contract_freeze.md` were added;
- no other existing file or `.idea` metadata changed;
- nothing was removed;
- no raw data, cache, bytecode, result, placeholder, or environment artifact appeared.

## Final response

Report:

- guard result;
- Stage 3A closure;
- exact measured benchmarks;
- 69-record validation result;
- major frozen rules;
- exactly one modified and two created files;
- checker exit codes and exact output;
- manifest result;
- limitations;
- status:
  `Stage 3B documentation completed; pending student review. No implementation authorised.`

Stop. Do not proceed to source-code work.
````

## Files read

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `context/verify_ai_output.md`
- `docs/project_a_handoff_audit.md`
- `ai/02_project_a_handoff_audit.md`
- `src/data_access.py`
- `scripts/check_handin.py`

Project A, sibling folders, the broader repository, Git metadata, and unrelated files were not inspected.

## Workspace, interpreter, and pre-edit manifest

- PyCharm opened root and terminal working directory: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- PyCharm interpreter: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`
- Python version: 3.13.13
- Protected loader hash: `928887403C34407C99B02984CB0600CBCF2CB9F88D7404D8E81A4B40E778B710`
- Pre-edit manifest: 39 files; canonical SHA-256 `287264F04761E165CC479D018F15024E93DD0EFE309A0F093820903939641B64`; `.idea` included; zero reparse points.

Both proposed new paths were absent before editing. No manifest was written inside the project.

## Pre-edit checker

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Working directory: exact Project B root  
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
```

The final sentence is checker boilerplate, not substantive completion evidence. No reminder was suppressed with a placeholder.

## Bounded in-memory verification

### Commands and tool results

The first attempt used an inline PowerShell here-string piped to the verified interpreter with `-B`. Exit code: `1`. It reached the protected loader, but the sandbox blocked both official hosts with `WinError 10013`. This was an access restriction, not a benchmark discrepancy; nothing was saved or changed.

A temporary read-only validation script was then created at `C:\Users\24116\AppData\Local\Temp\fins5545_stage3b_validation.py`, outside the project. Its first escalated execution exited `1` because Python sets `sys.path[0]` to the temporary script directory, so `src.data_access` was not importable. Codex corrected only that temporary script by inserting the already-verified exact Project B root into `sys.path`; no project file was changed.

Exact successful command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B 'C:\Users\24116\AppData\Local\Temp\fins5545_stage3b_validation.py'
```

Working directory: exact Project B root  
Exit code: `0`

Streamlit emitted its documented `No runtime found, using MemoryCacheStorageManager` warnings. The script used the protected Project B loader and in-memory pandas operations only. It contained no writer and saved no raw or derived data.

### Measured benchmarks

| Benchmark | Observed |
|---|---|
| Equity | 50,300 rows; 50 tickers; 10 sectors; 1,006 dates; 2020-01-02–2023-12-29 |
| Crypto | 14,620 raw rows; ten 2024-01-01 rows; 14,610 after cutoff; 10 tickers; 1,461 native dates |
| News | 149,683 raw rows; 146,836 cleaned; 2,847 removed; 50 tickers; 10 sectors |
| Mapping | 134,279 same-day; 12,551 forward; 146,830 mapped; six end-of-sample unmapped; no backward or off-calendar mapping |
| Returns | 50 missing first equity returns; 10 missing first native crypto returns; 10,060 aligned crypto rows with zero missing returns |
| Combined matrix | 1,006 dates × 60 assets; 50 legitimate first-equity-date missing values |
| Complete headline panel | 50,300 ticker-days; 12,338 no-news rows; headline counts sum to 146,830 |

Every accepted Stage 3A benchmark matched. Titles were preserved exactly and zero cleaned duplicate identities remained.

### Source/display sector nomenclature

Direct Stage 3B measurement found exact source values `Comm, Consumer, Energy, Financials, Healthcare, Industrials, Materials, RealEstate, Tech, Utilities`. The official guide displays `Comm/Telecom` and `Real Estate`. The proposed contract resolves this without mutating source data: retain source values and apply explicit display-only labels/order. This is a clarified contract rule, not a benchmark failure.

### Six endpoint records

The unmapped set again comprised source orders 14659–14664, all AMD/Tech, dated 2023-12-30 or 2023-12-31. The reconciliation `146,836 = 146,830 + 6` passed. No record was force-mapped beyond 2023-12-29.

## Review of 69 extreme adjusted-close movements

Threshold: `abs(adjClose_t / adjClose_(t-1) - 1) >= 0.25`.

- Equity: 4 of 50,250 observed returns (0.007960%): COP 1, OXY 2, SLB 1; dates 2020-03-09–2020-06-05.
- Crypto: 65 of 14,600 observed returns (0.445205%): ADA-USD 4, BCH-USD 8, BTC-USD 1, EOS-USD 7, ETC-USD 13, ETH-USD 4, LTC-USD 4, TRX-USD 4, XLM-USD 7, XRP-USD 13; dates 2020-01-14–2023-07-13.

All 69 had unique ticker-date keys; finite, strictly positive current and previous `adjClose`; finite, non-negative current and previous volume; finite calculated return; and an observed prior source row. Neither base price panel had missing `adjClose`, and no fill was used. All were retained.

This is internal source-row validation only. No external event/news search or economic verification occurred. The observations remain a disclosed limitation and later authorised portfolio work must include separate sensitivity evidence.

## Proposed contract rules

The proposed contract in `docs/data_contract.md` freezes:

- official-loader-only recomputation and no raw-data commitment or Project A copying;
- exact source/clean schemas, grains, counts, keys, dates, and permitted missingness;
- lexicographic equity and crypto membership, equity-then-crypto combined order, ascending dates, date-then-ticker long order, and source-to-display sector mapping;
- `adjClose` simple returns within native ticker calendars with no fill and first returns missing;
- crypto cutoff and native-calendar calculation before equity-date selection;
- exact news identity/text/timestamp preservation, earliest-source-row retention, and forward-only observed-calendar mapping;
- distinct no-news, neutral-news, and at-least-one-trading-day lag semantics;
- use-specific exclusion of the six endpoint records and their exact reconciliation;
- retention and later sensitivity treatment of all 69 extremes;
- `BLOCK`, `WARN`, and `PASS` validation gates and the minimum future test matrix;
- deferral of every model-dependent output schema and modelling choice.

No test, ETL function, portfolio, sentiment score, lexicon, fusion rule, app behaviour, model output, or empirical conclusion was created or approved.

## Discrepancies, genuine tool errors, and corrections

- **No benchmark discrepancy:** all accepted counts and boundaries matched.
- **Source/display label clarification:** source sectors `Comm` and `RealEstate` differ from official display labels; the contract preserves source values and adds an explicit display mapping.
- **Sandbox access failure:** the first loader call was blocked by the sandbox. The authorised network retry was required and succeeded.
- **Temporary import-path error:** the first execution of the external temporary script could not import the project-local `src` package. Codex added only the exact project root to that temporary script's `sys.path` and reran it successfully.

No error, correction, student decision, test, or approval was invented.

## Post-edit checker

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Working directory: exact Project B root  
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
```

This is mechanical structure evidence only. The six expected reminders remained, no placeholder was created, and the final sentence is not substantive readiness evidence. The same command will be run once more after this log is frozen; that confirmation will be reported without another project edit.

## Manifest and boundary evidence

The matching post-edit snapshot contained 41 files and had canonical SHA-256 digest `9E446F28A935A4328984BD964D7D314107917FAFBD0244B13CF09DF3ED2F97B8`, with `.idea` included and zero reparse points. A direct path/hash/size comparison against the complete 39-file pre-edit manifest proved:

- modified as authorised: `ai/02_project_a_handoff_audit.md` only;
- added as authorised: `ai/03_data_contract_freeze.md` and `docs/data_contract.md` only;
- removed: none;
- unexpectedly added or changed: none;
- `.idea` changes: none;
- project-local raw data, result output, placeholder, cache, bytecode, environment, or temporary script: none.

This new AI log cannot embed its own final hash without changing that hash. The path-level comparison of all pre-existing files is conclusive; the final response will therefore report the authoritative full-project digest calculated after the last edit.

## Limitations

- The loader verification depended on access to the official hosted ZIP; no raw data were persisted.
- The 69 extremes are internally consistent, not economically/event verified.
- Proposed validation tests are specified but deliberately not implemented.
- VADER-resource availability, sentiment scoring, portfolio sensitivity, all modelling, output schemas, and application work remain deferred and unauthorised.

## Student-review status

**Pending student review — no implementation authorised.** Stage 3A is accepted and closed, but the proposed Stage 3B input contract has not yet received final student acceptance.

## Next action — explicit student approval required

The student must review `docs/data_contract.md`, request any corrections, and explicitly accept or reject the proposed contract. No source-code or model stage may begin automatically.

## Final student acceptance — Stage 3B closed

**Date:** 2026-08-14

The student stated exactly:

> “I accept `docs/data_contract.md` as the frozen Project B input data contract. I accept the Stage 3B benchmarks, source/display sector mapping, news identity and mapping rules, six-unmapped policy, no-news versus neutral-news semantics, lag rule, and retention of the 69 extreme observations. I authorise Stage 4A only: implement and test the Project B data foundation against the frozen contract. This does not authorise portfolio optimisation, sentiment scoring, a finance lexicon, fusion, model outputs, figures, Streamlit, report writing, deployment, Git operations, or Stage 4B.”

This accepts the Stage 3B contract and its recorded benchmarks and rules. It authorises only the Stage 4A data-foundation implementation and contract tests. It does not approve a portfolio method, sentiment or lexicon method, fusion rule, model output, figure, application, report content, empirical conclusion, deployment, Git operation, or Stage 4B.

**Final status:** Stage 3B accepted and closed; Stage 4A data-foundation implementation only authorised.
