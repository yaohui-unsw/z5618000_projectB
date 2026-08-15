# AI workflow record — Project A hand-off audit

**Date:** 2026-08-14 (Australia/Sydney)  
**Stage:** Workflow Stage 3A — read-only Project A hand-off audit  
**Status:** Pending student review — no hand-off approved

## Stage objective

Determine, without migrating or implementing anything, whether the student-confirmed final local Project A foundation is trustworthy enough to inform a later Project B data contract. The authorised outputs are `docs/project_a_handoff_audit.md` and this provenance record only. Portfolio, sentiment, VADER, finance-lexicon, fusion, app, report, and Stage 3B work remained outside scope.

## Student authorisation

The student explicitly authorised:

> “I authorise Stage 3A: perform read-only validation against the local final version of Project A, and create only the two specified audit documents within Project B. Copying, implementation work and Stage 3B are not authorised.”

## Source identity and limitation

The student confirmed that:

`C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectA`

is the same version as the final submitted `z5618000_projectA(4).zip`. Codex treated this as student-confirmed source identity. The ZIP path and ZIP hash were not available, so Codex did not and does not claim a byte-for-byte comparison with the ZIP.

## Roles and provenance

- **ChatGPT:** helped design the staged audit and this operational prompt.
- **Student:** confirmed the final source identity, authorised the exact scope, supplied the materials, and retains authority to accept, correct, or reject any candidate hand-off.
- **Codex:** verified the exact local paths, inspected Project B governance and Project A evidence, ran read-only local/in-memory checks, created the two authorised Project B audit records, and did not migrate or implement anything.

Project B's current `AGENTS.md` governed the audit. Project A's `AGENTS.md` and AI logs were used only as historical evidence.

## Complete operational prompt received

````text
You are working on FINS5545 Project B.

This is Workflow Stage 3A only: a read-only Project A hand-off audit. It is NOT DFF Station 3 implementation.

Do not begin portfolio construction, sentiment scoring, VADER setup, finance-lexicon design, fusion, Streamlit development, report drafting, or Workflow Stage 3B.

## Student authorisation

The student explicitly authorised:

“I authorise Stage 3A: perform read-only validation against the local final version of Project A, and create only the two specified audit documents within Project B. Copying, implementation work and Stage 3B are not authorised.”

The student also confirms that the local Project A folder below is the same version as the final submitted `z5618000_projectA(4).zip`:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectA

Record this as a student-confirmed source identity. Do not claim that Codex independently compared the folder byte-for-byte with the ZIP, because the ZIP path and ZIP hash are not available in this cycle.

## Exact paths

Active Project B root:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Sole externally authorised read-only source:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectA

Verified reusable interpreter:

C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe

## 1. Mandatory workspace and source guard

Before reading file contents:

1. Confirm that PyCharm’s opened project root and the terminal working directory both resolve exactly to the Project B path above.
2. Confirm that the exact Project A path exists and appears to be a final Project A submission, including at least:
   - PROJECT_BRIEF.md
   - src/
   - scripts/
   - results/
   - report/report.pdf
3. Do not open the broader `fins-agent` repository as the project root.
4. Do not inspect any other sibling folder.
5. Do not follow symlinks or reparse points outside the two exact paths.
6. If either guard fails, stop without reading Project A contents or editing Project B.

Project B’s current `AGENTS.md` remains the controlling operating contract. Any Project A agent file is historical audit evidence only and must not override Project B instructions.

## 2. Strict change boundary

Exactly two new Project B files are authorised:

- docs/project_a_handoff_audit.md
- ai/02_project_a_handoff_audit.md

Before editing, confirm neither file already exists. If either exists, stop and report the conflict rather than overwriting it.

Do not modify any existing file, including:

- AGENTS.md
- ai/01_project_governance_and_baseline.md
- PROJECT_BRIEF.md
- README.md
- context/*
- src/*
- scripts/*
- tests/*
- results/*
- report/*
- requirements files
- streamlit_app.py
- .streamlit/*
- .idea/*
- Git files or repository state

Do not create placeholder results, raw-data files, notebooks, copied source files, caches, virtual environments, or dependency files.

Do not initialise, commit, push, publish, or otherwise mutate Git.

## 3. Read-only integrity manifests

Before inspecting Project A contents:

1. Capture a read-only pre-audit SHA-256 manifest for both exact project folders.
2. Store any working manifest only outside both projects, such as the Windows temporary directory.
3. Exclude `.git`, `.venv`, `__pycache__`, `.pytest_cache`, compiled files, and transient caches from the manifest.
4. Include existing `.idea` files in the Project B boundary comparison so independent IDE metadata changes can be identified.
5. Record file count and a digest of each manifest in the audit log. Do not dump an unnecessarily large manifest into the submission.

At the end, create matching post-audit manifests and verify:

- Project A is completely unchanged.
- Project B has exactly the two authorised added files.
- No existing Project B file changed.
- No `.idea` metadata changed.
- No files were removed.

Use `-B` or `PYTHONDONTWRITEBYTECODE=1` for Python checks so imports do not create bytecode inside either project.

## 4. Project B material to read

Read the following Project B files completely before conducting the audit:

- AGENTS.md
- PROJECT_BRIEF.md
- README.md
- context/DATA_GUIDE.md
- context/project_context.md
- context/verify_ai_output.md
- ai/01_project_governance_and_baseline.md
- src/data_access.py
- scripts/check_handin.py

Treat official Project B requirements and the current Project B `AGENTS.md` as the governing standards.

## 5. Project A evidence to inspect

Within the exact authorised Project A path, inspect the evidence needed to understand the final submitted data foundation:

- final README and project instructions;
- relevant context and data-guide files;
- all relevant source modules and runnable scripts;
- tests and validation scripts;
- final derived data, validation tables, and machine-readable outputs under results/;
- final report/report.pdf;
- relevant AI logs that discuss data cleaning, calendars, returns, headline deduplication, date mapping, the six unmapped observations, or corrections to these issues.

Read relevant source code in full. Do not rely only on filenames, comments, the report, or checker success.

For AI logs, first search for targeted terms such as `unmapped`, `six`, `headline`, `calendar`, `dedup`, `crypto`, `merge`, `adjClose`, `timezone`, and `trading day`, then read each materially relevant log entry in full. Do not dump unrelated chat history.

Do not inspect `.git`, `.idea`, virtual environments, caches, credentials, or unrelated personal files in Project A.

Do not copy any Project A content into Project B except short, attributable evidence necessary for the two audit documents. Do not copy code, report prose, figures, datasets, or AI instruction files.

## 6. Permitted execution

Do not run `scripts/run_part_a.py` or any command that may regenerate, overwrite, format, clean, or update Project A artifacts.

The following are permitted:

1. Read-only schema and data-quality checks against existing Project A outputs.
2. Read-only, in-memory Python checks using the verified interpreter.
3. The Project A hand-in checker, if inspection confirms that it is read-only.
4. Existing Project A tests only if their source first establishes that they do not write files; run with bytecode and pytest cache disabled.
5. The protected data-access loader only if existing artifacts are insufficient to verify a material claim. If used:
   - do not modify it;
   - do not manually download or save raw data;
   - keep data in memory;
   - do not set or change persistent environment variables;
   - do not create data files inside either project;
   - if access fails, record the limitation instead of installing packages or circumventing it.

Do not install, upgrade, remove, or configure any dependency. Do not download the VADER lexicon in Stage 3A.

If a temporary validation script is necessary, place it outside both project roots, use it only for this audit, and ensure it does not write into either project.

## 7. Required audit questions

The purpose is to determine whether the final Project A foundation is trustworthy enough to inform the later Project B data contract. Do not implement or migrate anything.

### A. Provenance and architecture

Establish:

- why this Project A folder is being treated as the final source;
- which files and functions form the final ETL and feature pipeline;
- which outputs are actually produced by that pipeline;
- whether Project A’s `src/data_access.py` matches the protected official helper or differs materially;
- which evidence is direct Codex verification and which is student confirmation, report claim, code inference, or unresolved uncertainty.

### B. Raw and cleaned data expectations

Where inspectable, verify rather than assume:

- equity schema, row count, date range, 50 tickers, 10 sectors, and `ticker-date` uniqueness;
- crypto schema, row count, 10 tickers, native seven-day calendar, the ten `2024-01-01` rows, and the `2023-12-31` cutoff;
- news schema, original row count, date type/timezone, ticker/sector coverage, missing publisher behaviour, and exact duplicate handling;
- required-column missingness and invalid keys;
- whether measured counts agree with Project A’s report and outputs.

Official approximate counts are benchmarks, not values to force. Report the actual measured values.

### C. Returns and calendar logic

Verify from executable logic and outputs that:

- returns use `adjClose`;
- returns are calculated within each ticker;
- crypto returns are calculated on the crypto-native calendar before alignment;
- the combined panel left-aligns crypto returns to the equity trading calendar;
- Project A did not merge equity and crypto price levels first and difference afterwards;
- asset ordering, dates, missingness, and resulting schemas are deterministic;
- no future data or accidental filling creates spurious returns.

### D. News cleaning and mapping

Verify that:

- exact duplicate headlines use `ticker + date + title`, not ticker-date alone;
- original headline casing, punctuation, and text are preserved;
- UTC timezone and dtype are normalised before mapping;
- every headline is mapped to the same equity trading day when possible, otherwise the next equity trading day;
- the code does not map only weekends while missing holidays;
- sentiment scoring was not incorrectly treated as a Part A feature;
- descriptive sentiment-bearing word counts, if present, remain descriptive rather than sentiment model output.

### E. The inherited “six unmapped observations”

Independently reproduce the count if the available evidence permits. Do not force the result to equal six.

Record:

- the exact measured count;
- whether the count is before or after exact headline deduplication;
- the relevant source row/index or another deterministic identifier;
- ticker, original date, sector, and title or an adequate identifying excerpt;
- why each observation cannot map to a valid forward equity trading day;
- whether Project A code, outputs, report, and AI logs all agree;
- which downstream artifacts excluded or retained them.

Distinguish use cases:

- observations that cannot enter a trading-day-aligned headline panel or aligned news-volume time series should be disclosed rather than force-mapped;
- corpus-level descriptive term-frequency analysis may legitimately retain otherwise valid deduplicated headlines even if they cannot be mapped to a later trading day.

Do not silently apply one blanket exclusion rule to every analysis. If Project A handled the records inconsistently, document the conflict and the downstream impact for student review.

### F. Code-output-report reconciliation

Cross-check material Project A claims across:

- source code;
- generated CSVs or validation outputs;
- report/report.pdf;
- tests/checker results;
- relevant AI correction logs.

A report statement is not proof when code or output conflicts with it. A passing checker is mechanical evidence only.

Classify each material finding as:

- Verified pass
- Verified issue
- Inconclusive
- Student decision required

For issues, record severity, evidence, downstream Project B risk, and the smallest recommended remediation. Do not repair anything in Stage 3A.

### G. Handoff candidate assessment

Create a table covering at least:

- official data loading;
- equity cleaning;
- crypto cutoff;
- native-calendar returns;
- combined calendar alignment;
- headline deduplication;
- timezone normalisation;
- forward trading-day mapping;
- six-unmapped handling;
- headline text preservation;
- validation tests;
- relevant derived schemas.

For each component record:

- Project A source file/function;
- evidence inspected;
- observed behaviour;
- candidate status: `reuse candidate`, `adapt/recompute candidate`, `reject`, or `unresolved`;
- reason and risk;
- student decision still required.

These are audit recommendations only. Do not state that anything has been finally approved for migration.

## 8. First authorised output

Create:

docs/project_a_handoff_audit.md

Write it in clear professional English and include:

1. scope and non-implementation statement;
2. provenance and evidence hierarchy;
3. Project A source and artifact inventory;
4. dataset/grain summary;
5. checks performed;
6. evidence-backed findings;
7. the six-unmapped-observation investigation;
8. code-output-report reconciliation;
9. handoff candidate table;
10. risks, limitations, and unresolved conflicts;
11. proposed inputs for a future Project B data contract;
12. explicit student decisions required before Stage 3B;
13. status: `Pending student review — no hand-off approved`.

Do not turn it into a report chapter and do not copy Project A prose.

## 9. AI provenance output

Create:

ai/02_project_a_handoff_audit.md

Include:

- date and stage objective;
- the student’s exact authorisation;
- source-identity statement and its limitation;
- division of roles:
  - ChatGPT helped design the staged audit and prompt;
  - the student confirmed the final source and authorised the scope;
  - Codex performed the local read-only inspection and checks;
- this complete operational prompt verbatim;
- exact Project B and Project A paths;
- files inspected;
- commands and exit codes;
- measured evidence and preliminary findings;
- any AI mistakes, failed checks, overclaims, or corrections made during the cycle;
- pre/post checker evidence;
- manifest/boundary evidence;
- limitations and unresolved questions;
- student-review status;
- next action explicitly requiring student approval.

Do not invent a Codex mistake merely to make the log look reflective. Record only genuine errors or corrections. Do not claim student acceptance.

## 10. Checker sequence

Before creating either file, run the Project B checker using:

& "C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe" -B scripts/check_handin.py

Record the exact command, exit code, and output as the pre-edit baseline.

After both files are complete, run the same command again and record the exact post-edit result.

The expected unfinished-output reminders must remain. Do not create placeholder report or result files to remove them. Do not describe “ready to zip and deploy” as substantive readiness.

If the Project A checker is confirmed read-only, run it through the same interpreter from the exact Project A working directory and record its result separately as mechanical evidence.

## 11. Final boundary and content audit

Before reporting completion:

1. Compare the pre/post Project A manifests and prove Project A is unchanged.
2. Compare the pre/post Project B manifests and prove exactly the two authorised files were added.
3. Confirm no existing Project B file changed.
4. Confirm no file was removed.
5. Confirm no `.idea` metadata changed.
6. Confirm no raw data, placeholder result, cache, bytecode, or environment file appeared.
7. Confirm both documents distinguish verified evidence from student confirmation and inference.
8. Confirm the six-unmapped count was measured or honestly marked inconclusive.
9. Confirm no migration, implementation, method approval, or Stage 3B work occurred.

## 12. Final response

Report concisely:

- workspace and source guards;
- Project A evidence inspected;
- measured data-quality conclusions;
- the exact result of the six-unmapped investigation;
- major code-output-report conflicts, if any;
- handoff candidates and blockers, explicitly pending student review;
- exactly which two files were created;
- Project A and Project B manifest results;
- checker commands, exit codes, and exact outputs;
- limitations;
- status: `Stage 3A audit completed; pending student review. Stage 3B not authorised.`

Stop after this response. Do not continue automatically.[@01_project_governance_and_baseline.md](file:///C:/Users/24116/Documents/GitHub/fins-agent/fins2026/z5618000_projectB/ai/01_project_governance_and_baseline.md)
````

The trailing `[@01_project_governance_and_baseline.md](file:///...)` marker is preserved as received. It is a PyCharm file-context attachment marker in the interaction record, not a methodological claim attributed to the student.

## Exact paths and guards

- Project B / opened PyCharm root: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Terminal working directory: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Authorised Project A source: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectA`
- Verified interpreter: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe` (Python 3.13.13)

The Project B root and terminal path matched exactly. Project A existed and contained `PROJECT_BRIEF.md`, `src/`, `scripts/`, `results/`, and `report/report.pdf`. Neither root was a reparse point, and the guarded traversal found no reparse point. The two authorised output paths did not exist before editing.

## Files inspected

### Project B governing evidence

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `README.md`
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `context/verify_ai_output.md`
- `ai/01_project_governance_and_baseline.md`
- `src/data_access.py`
- `scripts/check_handin.py`

### Project A source, instructions, tests, and evidence

- `README.md`, `AGENTS.md`, `SUBMISSION_CHECKLIST.md`, `requirements.txt`, and `report/OUTLINE.md`
- all three `context/` files and `PROJECT_BRIEF.md` by exact-hash comparison with the fully read Project B official copies
- `src/data_access.py`, `src/etl.py`, `src/features.py`, `src/visualization.py`, `src/__init__.py`
- `scripts/run_part_a.py` and `scripts/check_handin.py`
- `tests/test_etl.py`, `tests/test_features.py`, `tests/test_news_alignment.py`, `tests/test_smoke.py`, `tests/test_visualization.py`
- every CSV under `results/data/` and `results/tables/`
- all four PNGs under `results/figures/`
- all 13 pages of `report/report.pdf`
- `ai/01_project_setup.md`, `ai/02_agent_rules_and_environment.md`, `ai/03_station1_data_cleaning.md`, `ai/04_returns_and_calendar_alignment.md`, `ai/05_news_trading_day_alignment.md`, `ai/06_part_a_exhibits.md`, `ai/07_exhibit_issue_audit.md`, and `ai/AI_NOTES.md`

Project A `.git`, `.idea`, caches, virtual environments, credentials, and other siblings were not inspected.

## Pre-audit manifest evidence

The manifest walk excluded `.git`, virtual environments, bytecode and transient caches; Project B `.idea` files were included. No manifest was written inside either project.

| Project | Included file count | SHA-256 digest of canonical manifest | Reparse points followed |
|---|---:|---|---:|
| Project A | 49 | `9D4CC7DC17FD3454DED31949733A5F434665FAD14670C165B57D69006B73E330` | 0 |
| Project B | 37 | `53E62F4A6429241EDB639C5B279E0D89E09E7C49A1B790897506360DB140BC1D` | 0 |

## Pre-edit Project B checker

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

The final sentence is checker boilerplate. The six reminders show that this is not substantive completion or deployment readiness.

## Commands, checks, and exit codes

### Official-file hash comparison

PowerShell `Get-FileHash -Algorithm SHA256` was run on the Project A and Project B copies of `PROJECT_BRIEF.md`, all three official `context/` files, and `src/data_access.py`. Exit code: `0`. Every pair matched; the loader hash was `928887403C34407C99B02984CB0600CBCF2CB9F88D7404D8E81A4B40E778B710`.

### Read-only loader and pipeline validation

A temporary validation script was placed under Windows temporary storage, outside both projects. It called the protected loader and Station 1/2 functions in memory only; it contained no writer call.

Exact successful command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B 'C:\Users\24116\AppData\Local\Temp\fins5545_stage3a_pdf\stage3a_project_a_validation.py'
```

Working directory: exact Project A root  
Exit code: `0`

Material observed output is summarised in the next section. Streamlit emitted its documented `No runtime found, using MemoryCacheStorageManager` warning. No dataset was saved. A second narrow loader command measured all news schema fields: `date`, `ticker`, `sector`, `title`, and `url` each had zero missing/blank values; `publisher` had 140,255 missing values and zero blank strings. Exit code: `0`.

### Focused Project A tests

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_etl.py tests/test_features.py tests/test_news_alignment.py
```

Working directory: exact Project A root  
Exit code: `0`

Exact output:

```text
................................                                         [100%]
32 passed in 2.11s
```

These tests were read first and found not to write Project A files. The full suite was not run because `test_visualization.py` imports the undeclared, non-submission `fintools` dependency and includes figure generation; Stage 3A did not authorise broader-repository inspection or output work.

### Project A hand-in checker

The checker source was read completely and confirmed read-only before execution.

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Working directory: exact Project A root  
Exit code: `0`

Exact output:

```text
16 checks passed.
All checks passed - ready to zip.
```

This is mechanical evidence only. It does not detect the external `fintools.figures` dependency or validate the 69 retained extreme-movement flags.

### Report inspection

The environment had no `pypdf`, `pdfplumber`, PyMuPDF, or Poppler tool, and nothing was installed. Existing environment-owned PDF.js and canvas components were used through temporary support code outside both projects. Text was extracted from 13 pages and every page was rendered for visual inspection. The four submitted PNG exhibits were also opened directly. No PDF or Project A artifact was written.

## Measured evidence and preliminary findings

- **Equity:** 50,300 rows, 50 tickers, 10 sectors, 1,006 dates/rows per ticker, 2020-01-02 to 2023-12-29, zero required missingness and zero duplicate ticker-date keys.
- **Crypto:** 14,620 raw rows, 10 tickers, exactly ten 2024-01-01 rows, 14,610 rows after cutoff, 1,461 complete daily dates, 4,180 weekend rows, zero required missingness and duplicate keys.
- **News:** 149,683 raw rows, 50 tickers, 10 sectors, `datetime64[us, UTC]`, 575 non-midnight timestamps, 140,255 missing publishers, 23 full-row duplicate copies and 2,824 later duplicate-key copies, 146,836 cleaned rows, zero remaining key duplicates, and exact title preservation.
- **Returns:** 50,300 equity rows, 14,610 native crypto rows, and 10,060 aligned crypto rows; missing first returns were 50 and 10 respectively; aligned keys all matched source rows; all panels were unique and stably sorted. A manual ADA-USD 2020-01-06 check reproduced the Sunday-to-Monday return `0.07347140616116543` and rejected the Friday-to-Monday alternative `0.09046221064696236`.
- **Mapping:** 134,279 same-day, 12,551 forward-shifted, 6 unmapped, and 146,830 successfully mapped headlines. The daily panel had 50,300 unique ticker-date rows, 12,338 no-news rows, and reconciliation difference 0. Weekday non-trading shifts numbered 1,610, proving holidays were not treated as ordinary weekdays.
- **Outputs:** six core CSVs exactly matched the in-memory regeneration: inventory, integrity, return statistics, alignment summary, return sample, and headline sample.
- **Six-unmapped records:** measured as six before duplicate removal, after full-row exact deduplication, and after final key deduplication. All are AMD/Tech records dated 2023-12-30 or 2023-12-31, source orders 14659–14664, after the final equity date 2023-12-29.
- **Verified issue:** the complete Part A runner is not self-contained because it imports `fintools.figures`, which is absent from Project A and undeclared in its requirements.
- **Verified issue:** the report says no unresolved price problem remained, while the integrity CSV marks four equity and 65 crypto movements as retained and requiring later review.

No component was approved for hand-off. The full findings and candidate table are in `docs/project_a_handoff_audit.md`.

## Genuine errors, failed checks, and corrections in this cycle

1. Two early manifest-command compositions failed inside Codex's JavaScript orchestration layer: one had an unescaped PowerShell backtick and one interpolated a PowerShell label as a JavaScript variable. Neither reached the shell or changed a file. The manifest command was corrected and then completed successfully.
2. The first in-memory loader attempt reached `src/data_access.py` but both official hosts were blocked by the sandbox (`WinError 10013`). This was correctly treated as an access restriction, not a dataset failure. The same read-only check was rerun with the authorised network permission and succeeded; no host, environment variable, helper, package, or data file was changed.
3. Local PDF packages and Poppler were unavailable. The in-app browser was unavailable, and temporary headless Chrome/Edge attempts failed because their GPU processes were unusable. Existing PDF.js/canvas runtime support was then used successfully without installation. Intermediate parser setup errors were tooling errors, not PDF defects.

No artificial mistake, correction, test, or student decision was invented.

## Post-edit Project B checker

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

This is mechanical structure evidence only. The six reminders are expected at this stage, and the checker's final sentence is not evidence of substantive Project B completion or deployment readiness. No placeholder output was created. The same command will be rerun once more after this log is frozen; that final confirmation will be reported without another project edit.

## Post-audit manifest and boundary evidence

The post-audit comparison used the same exclusions and canonical SHA-256 method as the pre-audit manifest. The snapshot taken after the checker evidence was added produced:

- Project A: 49 files; digest `9D4CC7DC17FD3454DED31949733A5F434665FAD14670C165B57D69006B73E330`; zero reparse points. This exactly matches the pre-audit count and digest.
- Project B, excluding only the two authorised new documents: 37 files; digest `53E62F4A6429241EDB639C5B279E0D89E09E7C49A1B790897506360DB140BC1D`; zero reparse points. This exactly matches the complete pre-audit Project B count and digest.
- Project B including the two documents at that snapshot: 39 files; digest `5CEE4E8B01B15E4F10B461AAB71E0EBC9C418EA98E779217B6A23CE51B5EF183`; zero reparse points.
- The only additions were `ai/02_project_a_handoff_audit.md` and `docs/project_a_handoff_audit.md`. No existing Project B file changed or disappeared. Because `.idea` was included in the 37-file protected comparison, no IDE metadata changed. No raw data, placeholder result, virtual environment, cache directory, or compiled Python file appeared inside either project.

This paragraph necessarily changes the hash of the new AI log itself. The stable comparison for every pre-existing file is therefore conclusive, while the authoritative final full Project B digest will be computed after the last edit and reported in the final response without another project write.

## Limitations and unresolved questions

- The final ZIP itself was not available for an independent identity check.
- No full cleaned data or return panel was submitted; Project B would need a separately authorised recomputation, not a copy.
- The 69 extreme-movement flags require a student decision on targeted validation or explicit limitation treatment.
- The Project A runner's external `fintools.figures` dependency remains unresolved and was not repaired.
- Core logic tests passed, but Project B still needs real-data schema, six-record, leakage, lag, ordering, and deterministic-rerun tests.
- VADER resource availability and all sentiment methods were deliberately deferred.
- No migration or Stage 3B action is authorised.

## Student-review status

**Pending student review — no hand-off approved.** No student acceptance, criticism, correction, or migration decision is inferred.

## Next action — explicit student approval required

The student must review both Stage 3A documents, decide whether corrections are required, and explicitly accept or reject each proposed hand-off component and unresolved issue. Stage 3B must not begin automatically.

## Final student acceptance — Stage 3A closed

The student stated exactly:

> “I accept the Stage 3A audit and its candidate classifications. I approve the seven decisions outlined above and authorise Stage 3B to finalise the Project B data contract. Codex is permitted to record my acceptance at the end of `ai/02_project_a_handoff_audit.md`. Only two files may be created: `docs/data_contract.md` and `ai/03_data_contract_freeze.md`. No authorisation is granted for modifying source code, generating model outputs, or commencing work on portfolios, sentiment analysis, fusion strategies, or Streamlit.”

The student accepted the Stage 3A audit and candidate classifications and approved these seven decisions:

1. Accept the Stage 3A audit and its candidate classifications.
2. Project B will recompute inputs through the protected official `src/data_access.py`; no Project A code, CSV, or panel will be copied.
3. News duplicate identity is `ticker + normalised UTC source timestamp + exact title`; retain `source_row_order` and the auditable UTC source timestamp, and use the UTC calendar date separately for trading-day mapping.
4. The six verified AMD end-of-sample headlines are excluded from trading-day-aligned features, sentiment signals, and trading uses, but may remain in disclosed non-trading corpus-level vocabulary descriptions.
5. Retain all 69 flagged extreme adjusted-close movements without deletion, winsorisation, replacement, or other base-data alteration; conduct a bounded internal-consistency review now and defer portfolio sensitivity analysis to a later authorised model stage.
6. Do not repair, import, or depend on Project A's `fintools.figures`; Project B will create its own figures later.
7. Stage 3B freezes input schemas, keys, ordering, boundary dates, missingness semantics, and validation thresholds only; it approves no portfolio, sentiment method, fusion rule, app, or empirical conclusion.

This acceptance authorises documentation and bounded verification only. It does not approve implementation, model methods, model outputs, or empirical conclusions.

**Final status:** `Stage 3A accepted and closed; Stage 3B authorised for data-contract documentation only.`
