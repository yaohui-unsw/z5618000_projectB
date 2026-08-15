# Stage 8 — MAIA Streamlit implementation

**Date:** 2026-08-14  
**Status:** Pending student visual and interaction review — no deployment authorised.

## Objective and authority

Implement and validate the local **MAIA — Multi-Asset Investment Assistant**
Streamlit product as a read-only interface over frozen Project B artifacts. The
student accepted and closed Stage 7, approved the MAIA identity and a separately
disclosed 0.50% p.a. illustrative management fee, and authorised local app
implementation, testing, documentation, and student-review handoff only.

No model, parameter, lexicon, signal, lag, reliability rule, lambda, transaction
cost, sample, canonical CSV, canonical report PNG, report, Git state, deployment,
publication, or submission was authorised to change.

## Roles and provenance

- **Student:** accepted Stage 7; confirmed the corrected subtitle; approved the
  MAIA identity, target product direction, illustrative management fee, and
  Stage 8 boundary; retains final authority and must visually/interactively
  review the app.
- **ChatGPT:** assisted the student by reviewing the Project Brief, Week 10
  revision material and lecture transcript, the canonical exhibits, and the
  teacher's iShares/BlackRock example. It helped structure the Stage 8 prompt.
- **Codex:** verified the local Project B workspace and interpreter; inspected
  the authorised local requirements and frozen artifacts; implemented the
  downstream app; wrote tests and documentation; ran local validation and the
  checker; and performed the artifact/boundary audit.

The student's exact relevant replies recorded for this stage were:

> `其实没有问题，是not，我核验了`

> `looks good,lets do it`

## Complete operational prompt (verbatim)

```text
You are working on FINS5545 Project B.

This is Workflow Stage 8 only: MAIA Streamlit App Design, Local Implementation, Validation, and Student-Review Handoff.

It corresponds to the teacher’s DFF Station 4 implementation stage. It does not authorise report writing, deployment, Git operations, publication, submission, or changes to any frozen analytical result.

## 1. Student acceptance and authority

By sending this prompt, the student:

1. accepts and closes Stage 7, including its result audit, eight canonical figures, visual corrections, limitations, and AI-workflow record;

2. confirms that the final diagnostics subtitle reads `not contextual accuracy`;

3. preserves all favourable and unfavourable analytical outcomes;

4. approves the product name:

   `MAIA — Multi-Asset Investment Assistant`

5. approves a separately disclosed:

   `0.50% p.a. illustrative management fee`

   for the user-facing Allocation Studio;

6. authorises Stage 8 local Streamlit design, implementation, testing, and documentation only;

7. does not authorise any modification to a frozen model, parameter, portfolio, finance lexicon, signal, lag, reliability rule, lambda, cost assumption, sample, canonical CSV, canonical analytical result, or canonical report figure;

8. does not authorise report drafting, Git initialisation, GitHub push, Streamlit Community Cloud deployment, publication, or submission.

The student’s exact relevant replies were:

* `其实没有问题，是not，我核验了`
* `looks good,lets do it`

ChatGPT assisted the student by reviewing the Project Brief, Week 10 revision material, lecture transcript, current canonical exhibits, and the teacher’s iShares/BlackRock example. The student retains final decision-making authority.

## 2. Exact workspace and interpreter guard

Before reading or editing Project B files, confirm that:

* PyCharm’s opened project root resolves exactly to:

  `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`

* the terminal working directory resolves exactly to the same path;

* `PROJECT_BRIEF.md` and `streamlit_app.py` exist directly inside that root.

Use only:

`C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`

Do not create another environment. Do not install, remove, or upgrade any package.

Do not inspect Project A, another student’s files, sibling project folders, or the broader `fins-agent` repository.

Stop before reading project contents if the workspace guard fails.

## 3. Stage boundary

This stage may build and test the local Streamlit product only.

Do not:

* rerun portfolio optimisation;
* rerun VADER or sentiment scoring;
* rerun fusion;
* regenerate canonical CSVs;
* regenerate or alter the eight canonical report PNGs;
* load or save raw data;
* import `nltk` at app runtime;
* call `src.data_access` from the deployed app;
* import or execute `src.portfolios`, `src.sentiment`, or `src.fusion` from the app;
* change the approved finance lexicon;
* change any portfolio, sentiment, reliability, tilt, cost, or evaluation parameter;
* add a fifth optimisation method;
* tune anything after observing results;
* draft the report;
* initialise or modify Git;
* push a repository;
* deploy the app;
* make anything public.

The app must read the existing precomputed artifacts under `results/` only. Lightweight display transformations, chart construction, fund selection, and user-allocation arithmetic are permitted. They must not be described as new model results.

## 4. Read before editing

Read completely:

* `AGENTS.md`
* `PROJECT_BRIEF.md`
* `README.md`
* `SUBMISSION_CHECKLIST.md`
* `context/project_context.md`
* `context/verify_ai_output.md`
* `docs/STUDENT_DEPLOY.md`
* `docs/data_contract.md`
* `docs/portfolio_backtest_design.md`
* `docs/sentiment_innovation_design.md`
* `docs/finance_lexicon_review.md`
* `docs/results_audit_and_exhibit_design.md`
* `ai/09_sentiment_fusion_implementation.md`
* `ai/10_results_audit_and_exhibit_generation.md`
* current `streamlit_app.py`
* current `.streamlit/config.toml`
* current `requirements.txt`
* current `requirements-dev.txt`
* current `src/reporting.py`
* relevant current tests and `scripts/check_handin.py`

Inspect the schemas and hashes of all thirteen frozen canonical CSVs:

Portfolio:

* `results/data/fund_returns.csv`
* `results/data/fund_weights.csv`
* `results/tables/performance_metrics.csv`
* `results/tables/portfolio_solver_diagnostics.csv`
* `results/tables/extreme_sensitivity_metrics.csv`

Sentiment and fusion:

* `results/data/sector_sentiment_index.csv`
* `results/data/ticker_sentiment_daily.csv`
* `results/data/fusion_returns.csv`
* `results/data/fusion_weights.csv`
* `results/tables/sentiment_diagnostics.csv`
* `results/tables/finance_lexicon.csv`
* `results/tables/fusion_performance_metrics.csv`
* `results/tables/fusion_comparison.csv`

Capture a pre-edit SHA-256 hash for every canonical CSV and every existing canonical PNG. These artifacts are immutable in Stage 8.

Do not open raw data or call the official data loader.

## 5. Authorised file boundary

Modify only:

* `streamlit_app.py`
* `.streamlit/config.toml`
* `README.md`
* append only to `ai/10_results_audit_and_exhibit_generation.md`

Create only:

* `src/app_data.py`
* `src/app_logic.py`
* `src/app_charts.py`
* `tests/test_app_data.py`
* `tests/test_app_logic.py`
* `tests/test_streamlit_app.py`
* `docs/streamlit_app_design.md`
* `ai/11_streamlit_implementation.md`

Do not modify `requirements.txt`: use only the packages already declared and available. Do not add a remote font, remote image, JavaScript dependency, or external web service.

No other project file may change. No new PNG, CSV, raw-data, cache, bytecode, environment, temporary, report, Git, or deployment artifact may be created inside Project B.

If `.idea/workspace.xml` changes independently while PyCharm is open, do not edit or restore it. Report it separately as IDE metadata.

## 6. Close Stage 7

Append chronologically to `ai/10_results_audit_and_exhibit_generation.md`:

* the student’s Stage 7 acceptance;
* the student’s confirmation that the subtitle says `not contextual accuracy`;
* the ChatGPT-assisted visual review;
* acceptance of all eight figures;
* confirmation that weak and negative results remain retained;
* confirmation that no analytical output changed during visual correction;
* Stage 8’s limited authority.

End the appended section with:

`Stage 7 accepted and closed; Stage 8 authorised only for local MAIA Streamlit implementation, validation, and student-review handoff.`

Do not rewrite any prior history.

## 7. Product identity and audience

Use this product identity exactly:

**MAIA**
**Multi-Asset Investment Assistant**

Value proposition:

`Compare twelve systematic Equity, Crypto and Combined funds using transparent out-of-sample evidence and news-sentiment analytics.`

Target user:

A financially curious retail investor who understands basic return and risk concepts but does not read Python code or build portfolios directly.

The product is a portfolio-management interface, not a stock-trading app.

The user allocates money across MAIA’s funds. They do not select or trade individual securities.

Do not implement:

* account registration;
* login;
* bank funding;
* real orders;
* live prices;
* “Buy now” functionality;
* personalised financial advice;
* performance forecasts;
* guaranteed-return language.

Use language such as `Build an allocation`, `Explore a fund`, and `Historical illustration`, not `Invest now`.

## 8. Design system

Create a restrained institutional visual system inspired by the information hierarchy of professional fund-provider websites, without copying BlackRock/iShares branding, logos, wording, or layouts.

Use:

* dark navy for headers and primary text;
* white or very light grey page backgrounds;
* teal for evidence-aware and analytical elements;
* orange for Finance-VADER and selected emphasis;
* blue for Plain VADER;
* accessible contrast;
* consistent percentage, currency, date, and decimal formatting;
* professional sans-serif typography already available locally;
* generous spacing and clear section hierarchy.

Use `.streamlit/config.toml` for a coherent theme and minimal internal CSS only where Streamlit cannot provide the required hierarchy.

Do not create a decorative landing page that delays access to the evidence.

The default page must be useful before the user changes a control.

Use a single root entrypoint and one app with five clear navigation sections. Prefer conditional page rendering so heavy artifacts are loaded only when required.

Navigation:

1. `Explore Funds`
2. `Fund Fact Sheet`
3. `Allocation Studio`
4. `Sentiment & Innovation`
5. `Methodology & Disclosures`

The interface must remain understandable at narrower desktop widths.

## 9. Data-access architecture

### `src/app_data.py`

Implement deterministic, cached, read-only artifact loaders.

Requirements:

* resolve paths relative to the Project B root;
* never depend on the current terminal directory;
* never use an absolute laptop path;
* never call `src.data_access`;
* never read raw data;
* never write a file;
* parse dates explicitly;
* validate required columns before returning a frame;
* give a human-readable error naming the missing or invalid artifact;
* use stable sorting;
* return defensive copies where UI code may filter or reshape data;
* avoid loading every large artifact on the first page;
* cache deterministic reads with `st.cache_data`.

Provide small loader functions by functional area rather than one uncontrolled global load.

The app must fail visibly and helpfully if a required artifact is absent. It must not silently substitute a placeholder or fabricated number.

### `src/app_logic.py`

Keep all calculations pure and independently testable.

Implement:

* growth-of-$1 calculation from canonical `net_return`;
* drawdown from compounded net wealth;
* latest target holdings from the most recent rebalance;
* current holdings date;
* asset-class exposure summaries;
* user-allocation validation;
* cross-family return-calendar reconciliation;
* one-time fund-sleeve allocation growth;
* the separately disclosed management-fee adjustment;
* user-allocation performance metrics;
* display-only rolling sentiment summaries;
* complete fusion comparison summaries without selective omission.

Do not call a model, optimiser, VADER, or fusion engine.

### `src/app_charts.py`

Implement lightweight, display-only charts from precomputed data using the already available Streamlit and Matplotlib stack.

Charts must:

* use consistent MAIA colours;
* label dates, axes, units, samples, and net/gross status clearly;
* include zero or `$1` references where economically relevant;
* avoid clipped text and overlapping legends;
* retain negative fusion outcomes;
* never save or overwrite a canonical report figure;
* return figure objects to the app instead of writing PNG files.

## 10. Page 1 — Explore Funds

This is the default page.

It must immediately communicate:

* 12 frozen base funds;
* three families: Equity, Crypto, Combined;
* four methods: Equal Weight, Minimum Variance, Maximum Sharpe, Risk Parity;
* strictly historical out-of-sample evidence;
* net results after the frozen 5-bps one-way-turnover cost.

Include:

1. a concise MAIA product header and value proposition;
2. a visible historical-performance disclaimer;
3. family and method filters;
4. a complete metrics table across all 12 funds;
5. a risk-return map using annualised net volatility and annualised net return;
6. a user-selectable growth-of-$1 comparison, allowing up to four funds;
7. plain-language method descriptions.

Use these method interpretations:

* **Equal Weight:** a transparent diversified benchmark.
* **Minimum Variance:** seeks the lowest estimated portfolio variance using prior observations.
* **Maximum Sharpe:** seeks the highest estimated return per unit of risk using a zero risk-free rate.
* **Risk Parity:** seeks to balance portfolio risk contributions.

Do not label any fund `best`, `recommended`, or `optimal for you`.

The table must retain all 12 funds even if filters or visual selections are offered.

## 11. Page 2 — Fund Fact Sheet

Allow selection of any one of the 12 base funds.

Show:

* human-readable fund name;
* family and method;
* OOS start and end date;
* annualised net return;
* annualised net volatility;
* net Sharpe ratio;
* net maximum drawdown;
* net growth of $1;
* drawdown time series;
* current holdings from the latest target rebalance;
* the exact current-holdings date;
* top holdings chart and complete bounded holdings table;
* for Combined funds, Equity-versus-Crypto target exposure;
* number of holdings;
* average rebalance turnover;
* total turnover;
* transaction-cost assumption;
* monthly rebalance frequency;
* 252-day or 365-day estimation window as appropriate;
* long-only, fully invested and 20% per-asset cap;
* zero risk-free rate.

The four primary KPI cards must reconcile exactly to `performance_metrics.csv`.

Growth and drawdown may be recomputed only as display transformations from the canonical `net_return` series.

Current holdings must come from the most recent `target_weight`, not pretrade weights, and must sum to one within tolerance.

Include an expandable plain-English section titled `How this fund works`.

Never describe historical results as expected or guaranteed future returns.

## 12. Page 3 — Allocation Studio

This is an investor-journey simulation using frozen fund returns, not a new portfolio model.

Controls:

* initial capital, default `$10,000`;
* choose between two and four base funds;
* default selection: the four Combined funds, without performance-based ranking;
* allocation controls in five-percentage-point increments;
* a visible total-allocation indicator;
* an `Equal split` convenience action;
* require total allocation to equal exactly 100% before displaying results;
* do not silently normalise an invalid allocation.

Use a **one-time initial allocation**:

* each selected fund sleeve starts with the user-selected dollar amount;
* each sleeve compounds using its own precomputed `net_return`;
* sleeves drift with performance;
* do not rebalance the user’s fund-level allocation;
* do not rerun any underlying fund portfolio.

Calendar rule:

* if all selected funds are Crypto, use their shared native Crypto calendar;
* if any Equity or Combined fund is selected, use the shared Equity/Combined display calendar over the common OOS period;
* compound each selected Crypto fund’s native daily net returns between consecutive shared display dates so weekend returns are preserved;
* never drop Crypto weekend performance without compounding it;
* begin at the latest first-live date among selected funds and end at the earliest last date;
* label the resulting common historical period.

Cost and fee rule:

* the canonical fund `net_return` already includes the frozen 5-bps turnover cost;

* do not apply that cost again;

* display a fixed `0.50% p.a. illustrative management fee`;

* apply it separately to the account wealth using elapsed calendar time:

  `after_fee_wealth = before_fee_wealth × (1 - 0.005) ** (elapsed_calendar_days / 365)`

* show both before-management-fee and after-management-fee wealth;

* describe the management fee as a product illustration, not a canonical portfolio-model result.

Show:

* dollar allocation by selected fund;
* historical account value before and after management fee;
* ending account value after fee;
* historical total return after fee;
* annualised return after fee;
* annualised volatility after fee;
* Sharpe ratio after fee;
* maximum drawdown after fee;
* total illustrative management-fee drag in dollars;
* selected-fund allocation table.

Use annualisation 365 only when all selected funds are Crypto; otherwise use 252 for the shared display series.

Prominently state:

`Historical out-of-sample illustration only. This is not a forecast, recommendation, or guarantee.`

## 13. Page 4 — Sentiment & Innovation

This page must make the existing innovation understandable without claiming causal or statistically significant success.

Include:

### Market Sentiment Pulse

Create a display-only cross-sector summary from precomputed `finance_compound`.

* use a 21-trading-day rolling mean for readability;
* clearly label the smoothing as visual only;
* do not use it for trading;
* do not call it a calibrated Fear & Greed Index;
* describe it as `Finance-VADER market tone`;
* show the underlying numeric scale and latest source date.

### Sector sentiment

* allow one or more of the ten sectors to be selected;
* show the precomputed Finance-VADER sector series;
* optionally overlay a clearly labelled 21-day visual mean;
* retain the no-news treatment;
* state that Crypto has no news sentiment input.

### Finance lexicon evidence

Show:

* all 23 student-approved operational entries;
* approved value;
* candidate class;
* student decision;
* rationale;
* custom-term hit share from `sentiment_diagnostics.csv`;
* changed-score share from `sentiment_diagnostics.csv`;
* exact-zero and neutral-band diagnostics;
* sector custom-term exposure.

State clearly:

* term exposure is not contextual accuracy;
* higher Finance zero/neutral rates partly reflect intentional neutralisation of generic finance words with inappropriate vanilla polarity;
* this does not imply lower information coverage;
* Utilities and Energy are exposure concentrations, not proof of greater sentiment accuracy.

Do not hard-code diagnostic values when they can be retrieved from the canonical diagnostics CSV.

### Fusion evidence

Show all 24 overlays and all eight paired comparisons for each of:

* Plain VADER;
* Finance VADER;
* Evidence-aware Finance.

Include:

* annualised-return delta;
* Sharpe delta;
* turnover delta;
* base-versus-overlay comparison;
* strongest and weakest observed Sharpe delta, clearly labelled as descriptive;
* a trade-off view using incremental turnover and Sharpe;
* complete bounded data table.

Retain every negative result.

Prominently disclose:

* Finance VADER improved Sharpe versus base in 5 of 8 funds;
* Plain VADER and Evidence-aware each improved 4 of 8;
* Finance exceeded Plain in Sharpe in 6 of 8 comparisons;
* Evidence-aware reduced turnover in 8 of 8 comparisons;
* Evidence-aware nevertheless had lower return and Sharpe than naive Finance in all 8 paired comparisons;
* no prespecified statistical significance test was conducted.

These claims must be calculated from the canonical comparison file, not manually typed without validation.

## 14. Page 5 — Methodology & Disclosures

Create a concise, plain-English methodology page.

Cover:

* target user and customer journey;
* three fund families and four methods;
* rolling 252/365-day windows;
* monthly rebalancing;
* information dates strictly earlier than decision dates;
* long-only, fully invested, 20% cap;
* zero risk-free rate;
* weight drift between rebalances;
* 5-bps transaction cost;
* native Crypto return calendar;
* one-trading-day sentiment lag;
* 23-term student-reviewed finance lexicon;
* fixed lambda 0.10;
* no Crypto news;
* no-news is not the same as neutral news;
* 69 extreme returns retained;
* short-headline limitation;
* no significance test;
* historical OOS evidence is not a forecast.

Use `portfolio_solver_diagnostics.csv` and `extreme_sensitivity_metrics.csv` in a bounded expandable `Implementation and robustness evidence` section.

Do not overwhelm the default page with technical prose.

## 15. README and design documentation

Update `README.md` so another person can:

* understand what MAIA is;
* identify its target user;
* see the five app sections;
* understand that the app reads precomputed results;
* run it locally using the verified shared environment;
* understand that `nltk` is build-only and absent at runtime;
* understand the distinction between the 5-bps trading cost and the 0.50% illustrative management fee;
* find the future deployment instructions;
* see that deployment remains pending student action.

Create `docs/streamlit_app_design.md` containing:

1. stage authority;
2. target user;
3. customer journey;
4. teacher requirement-to-feature mapping;
5. BlackRock/iShares-inspired information hierarchy without brand copying;
6. navigation and page specification;
7. canonical source-to-widget lineage;
8. allocation formula and calendar rule;
9. fee rule;
10. accessibility and responsive-design rules;
11. disclosures;
12. test plan;
13. explicitly deferred deployment and report work;
14. status `Implemented locally; pending student visual and interaction review`.

## 16. Required tests

### `tests/test_app_data.py`

Test:

* relative path resolution;
* all required artifact paths;
* required schemas;
* missing-artifact failure messages;
* date parsing;
* stable ordering;
* exact 12 base funds;
* exact 24 overlays;
* exact 23 approved lexicon entries;
* read-only behaviour;
* no placeholder fallback.

### `tests/test_app_logic.py`

Use independent synthetic examples for:

* growth of $1;
* drawdown;
* latest holdings;
* holdings sum;
* allocation sum validation;
* one-time sleeve drift;
* no silent allocation normalisation;
* common OOS window;
* Crypto weekend compounding onto the shared display calendar;
* all-Crypto native calendar;
* 5-bps cost not applied twice;
* exact 0.50% annual management-fee formula;
* before-fee versus after-fee wealth;
* user-allocation metrics;
* 21-day sentiment display mean;
* all 24 fusion rows retained;
* positive and negative results retained.

### `tests/test_streamlit_app.py`

Use `streamlit.testing.v1.AppTest` where feasible.

Test:

* app starts without a runtime exception;
* default page is useful without clicks;
* MAIA identity and disclaimer are visible;
* all five navigation destinations exist;
* 12-fund comparison is available;
* a fact sheet can be selected;
* Allocation Studio controls exist and reject invalid totals;
* Sentiment & Innovation exposes the lexicon and complete fusion evidence;
* Methodology & Disclosures is reachable;
* no raw-data, VADER, optimiser, or fusion execution occurs;
* no absolute Windows project path is rendered;
* no `Buy now`, guaranteed return, or recommendation wording appears.

Add a static import/AST guard that blocks app runtime imports of:

* `nltk`
* `src.data_access`
* `src.portfolios`
* `src.sentiment`
* `src.fusion`

Also block writes to `results/` from the app modules.

Do not weaken a valid test merely to make the suite pass. Preserve and document genuine failed tests and corrections.

## 17. Validation sequence

Use the explicit interpreter and disable bytecode and pytest caches.

Run:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -p no:cacheprovider tests/test_app_data.py tests/test_app_logic.py tests/test_streamlit_app.py tests/test_smoke.py
```

Then launch the local app using the same interpreter:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m streamlit run streamlit_app.py --server.headless true --server.port 8501
```

Confirm:

* the server reaches a healthy state;
* the root page responds;
* at least one real fund-comparison path renders;
* at least one selected fact-sheet path renders;
* at least one valid Allocation Studio path renders;
* the Sentiment & Innovation page renders;
* the methodology page renders;
* rerunning controls does not trigger model computation or file writes.

Terminate the local test server cleanly after the smoke test.

Then run:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Do not claim visual browser inspection unless an actual rendered browser view was opened and inspected. If browser inspection is unavailable, state that clearly and leave visual approval to the student.

## 18. Canonical-artifact integrity

After all app tests:

* recompute SHA-256 for all thirteen canonical CSVs;
* verify every hash is identical to the pre-edit value;
* verify all eight canonical PNG hashes are unchanged;
* verify the app created no result, raw-data, cache, bytecode, temporary, report, deployment, or Git artifact;
* compare the complete pre/post project manifest;
* verify only authorised files changed or were created;
* separately disclose any independently changing `.idea/workspace.xml`.

Any canonical CSV or canonical PNG change is a BLOCK. Stop and report it; do not restore, regenerate, or silently accept it.

## 19. AI workflow record

Create `ai/11_streamlit_implementation.md`.

Record:

* date and stage;
* exact authority and exclusions;
* complete operational prompt;
* roles of student, ChatGPT, and Codex;
* files read;
* pre-edit manifest;
* frozen canonical hashes;
* teacher requirement-to-feature mapping;
* product name and target user;
* design decisions;
* data lineage;
* allocation and fee calculations;
* implementation details;
* tests and exact command outputs;
* local health/smoke evidence;
* genuine errors and corrections;
* absence of model recomputation;
* post-edit canonical hashes;
* boundary audit;
* limitations;
* deployment explicitly deferred;
* student visual-review status.

Do not invent an error or student decision.

Status must remain:

`Pending student visual and interaction review — no deployment authorised.`


## 20. Final response

Report concisely:

1. workspace and interpreter;
2. Stage 7 closure;
3. product name;
4. implemented navigation and features;
5. exact canonical data sources used;
6. allocation and management-fee rules;
7. test results and exit codes;
8. local Streamlit health result;
9. checker result;
10. canonical CSV and PNG integrity;
11. exact files modified and created;
12. boundary result;
13. genuine limitations or unresolved UI issues;
14. whether direct browser visual inspection was actually performed;
15. exact local run command for the student.

End exactly:

`Stage 8 MAIA Streamlit app implemented and validated locally; pending student visual and interaction review. No frozen model, parameter, canonical analytical output, report figure, report, Git state, or deployment was changed or commenced.`
```

## Workspace and environment evidence

- Resolved opened workspace root:
  `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Resolved terminal working directory: the same exact path.
- `PROJECT_BRIEF.md` and `streamlit_app.py` existed directly inside that root.
- PyCharm environment inspection before Python commands returned Python
  **3.13.13**, `venv`, executable
  `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`,
  package manager `pip`.
- No package or environment was created, installed, removed, or upgraded.
- Project A, sibling project folders, the broader repository, Git history, and
  another student's work were not inspected.

## Files read

Codex read the required Project B governance, official requirements, deployment
guide, frozen design/evidence records, starter app/configuration, dependency
files, reporting layer, relevant tests, checker, and the schemas/contents needed
from the thirteen canonical CSVs:

- `AGENTS.md`, `PROJECT_BRIEF.md`, `README.md`, `SUBMISSION_CHECKLIST.md`;
- `context/project_context.md`, `context/verify_ai_output.md`;
- `docs/STUDENT_DEPLOY.md`, `docs/data_contract.md`,
  `docs/portfolio_backtest_design.md`, `docs/sentiment_innovation_design.md`,
  `docs/finance_lexicon_review.md`,
  `docs/results_audit_and_exhibit_design.md`;
- `ai/09_sentiment_fusion_implementation.md`,
  `ai/10_results_audit_and_exhibit_generation.md`;
- the pre-stage `streamlit_app.py`, `.streamlit/config.toml`,
  `requirements.txt`, `requirements-dev.txt`, `src/reporting.py`, relevant tests,
  and `scripts/check_handin.py`;
- the thirteen canonical CSVs listed in the prompt, as immutable app evidence.

No raw dataset was opened and no analytical pipeline was run by the app. The
required existing smoke test exercised the unchanged official loader only as an
explicit validation-command component; it neither wrote raw data nor became an
app dependency.

## Pre-edit manifest and frozen hashes

The pre-edit SHA-256 manifest covered all 89 Project B files, included `.idea`,
and excluded `.git`, environments, caches, and bytecode. It was stored outside
Project B at
`C:\Users\24116\AppData\Local\Temp\maia_stage8_pre_manifest.tsv`.

- Manifest file count: **89**
- Manifest digest:
  `12A5C06081E3866FF52D628B9DE488D06A610CFA44CA7585895774F939029F26`

The first PowerShell manifest attempt encountered sandbox/file-API access
restrictions for some protected result paths. A read-only FileStream SHA-256
retry with authorised access succeeded. This was a tooling/access correction;
it changed no project file.

### Thirteen canonical CSV hashes before Stage 8

| Artifact | SHA-256 |
|---|---|
| `results/data/fund_returns.csv` | `7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84` |
| `results/data/fund_weights.csv` | `F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8` |
| `results/tables/performance_metrics.csv` | `5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19` |
| `results/tables/portfolio_solver_diagnostics.csv` | `ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C` |
| `results/tables/extreme_sensitivity_metrics.csv` | `40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151` |
| `results/data/sector_sentiment_index.csv` | `D7670369187E3FF6909A88F6459204284A45D07941DC395CE239D8E304E8E96E` |
| `results/data/ticker_sentiment_daily.csv` | `CC9DDF834EF43B9B07240A40949716BA573A14E6ADDCD1997DFF83C125E26FCD` |
| `results/data/fusion_returns.csv` | `5A868D15E4D649FEDCB7BF9A0D58657F1729D6F35A2A62A2DF148622EA8CEBC5` |
| `results/data/fusion_weights.csv` | `13941551A0D3D9A07290235CCEF7C8AB389D2F78EAF36D81CE661A915F485058` |
| `results/tables/sentiment_diagnostics.csv` | `3C7842ED0F955DCA29E1E728EFD51C46AA12D4B93999DC9C72D47C436AC179B5` |
| `results/tables/finance_lexicon.csv` | `5E6EE31DADC6C754DD465E825FBA5F25B3BD26E5E0AA846B3A578619D444C5DB` |
| `results/tables/fusion_performance_metrics.csv` | `B75FA251E385E3709D3EC1380367D0257285D249AF742965C8FD993FCA770A07` |
| `results/tables/fusion_comparison.csv` | `B51DF470AEAB5932356037DF72FCF0044729C6F9F88C117E6C4B90F4922C3946` |

### Eight canonical PNG hashes before Stage 8

| Figure | SHA-256 |
|---|---|
| `fund_growth_comparison.png` | `68AA156B18AACC824346C8820C1B941623FA0D13BA6627AAFB17848EF1F625BE` |
| `combined_drawdowns.png` | `DAA1415C7406098E61E250122A5B1AC11240B8858C2949A482EC453308D59C81` |
| `combined_weights_over_time.png` | `04A8B663D6C1CB29F6E9D8D7CB2A6DD16C90A1C31D9920543E6A2364CC74F1E6` |
| `fund_risk_return_map.png` | `C7CF65BF38BA38214659F28D0CA84B1BD7528C1D74BCCD2B62BBDCA18BC721E8` |
| `sector_sentiment_timeseries.png` | `7A210A89713955EAB7C459F4C3D8044E5317D49733142A9D1B652669A6012FB7` |
| `fusion_before_after.png` | `7789948051C8FBDA8A0E9659C066086C301D972E956465B7EB49156041A994DF` |
| `sentiment_innovation_diagnostics.png` | `1A1F2DAC8AE4330D01B6DAA19FC9D18461A55919A276AD27B12826755D2F97C8` |
| `fusion_turnover_tradeoff.png` | `9D483E2247EE05DC8E90451F63A77F035D586BDC04137BBE1965737CA30B641B` |

## Teacher requirement-to-feature mapping

| Requirement | Implemented feature | Canonical lineage |
|---|---|---|
| Twelve systematic products | Complete 12-fund explorer and selectable fact sheets | Base performance, returns, and weights |
| Investor-facing interface | Five-section portfolio-management journey | Read-only app modules |
| Growth/drawdown/current holdings | Net paths, drawdown, latest target holdings/date | `fund_returns.csv`, `fund_weights.csv` |
| Allocation tool | Two-to-four-fund one-time sleeve simulation | Canonical base `net_return` only |
| Sentiment and innovation | Market/sector Finance-VADER, lexicon, 24 overlays | Canonical sentiment/fusion tables |
| Transparent methodology | Plain-English rules, solver and sensitivity evidence | Canonical diagnostics/evidence tables |
| Deployable architecture | Root entrypoint, relative paths, cached results | `streamlit_app.py`, `src/app_data.py` |

## Product, design, and data lineage

MAIA targets a financially curious retail investor. It is a fund-allocation
interface, not a stock-selection/trading product. The app uses a restrained
navy/light-grey institutional hierarchy with teal analytics, orange Finance-
VADER emphasis, blue Plain-VADER emphasis, local sans-serif typography, and no
copied brand assets, remote fonts, JavaScript, images, or services.

The five conditional sections are Explore Funds, Fund Fact Sheet, Allocation
Studio, Sentiment & Innovation, and Methodology & Disclosures. The default page
loads only base summary evidence. Large artifacts are loaded only by pages that
need them.

`src/app_data.py` resolves every path from the Project B module location,
validates exact columns/rows/keys/dates, applies stable sorting, caches reads,
and returns defensive copies. It never calls `src.data_access` or writes a file.
`src/app_logic.py` contains pure growth, drawdown, holdings, calendar, allocation,
fee, metric, rolling-display, and complete-fusion calculations. `src/app_charts.py`
returns in-memory Matplotlib figures and never saves a PNG.

## Allocation and fee calculations

- Two to four funds; default is the four Combined funds without performance
  ranking; five-percentage-point controls; exact 100% gate; no normalisation.
- Each sleeve receives its one-time initial dollars and compounds its own
  canonical `net_return`; sleeves drift and are never user-level rebalanced.
- All-Crypto selections use the shared native calendar and annualisation 365.
- Mixed/Equity/Combined selections use the common Equity/Combined display
  calendar and annualisation 252; native Crypto returns between consecutive
  display dates are geometrically compounded, preserving weekends.
- Canonical fund net returns already contain the 5-bps turnover cost; the app
  does not apply it again.
- The separate 0.50% p.a. illustrative management fee is applied exactly as
  `before_fee_wealth × (1 - 0.005) ** (elapsed_calendar_days / 365)` and is
  labelled as a product illustration rather than a model result.

## Files changed

Modified within the authorised boundary:

- `streamlit_app.py`
- `.streamlit/config.toml`
- `README.md`
- `ai/10_results_audit_and_exhibit_generation.md` (chronological append only)

Created within the authorised boundary:

- `src/app_data.py`
- `src/app_logic.py`
- `src/app_charts.py`
- `tests/test_app_data.py`
- `tests/test_app_logic.py`
- `tests/test_streamlit_app.py`
- `docs/streamlit_app_design.md`
- `ai/11_streamlit_implementation.md`

## Test inventory, commands, and outcomes

The tests cover all thirteen loader contracts, defensive copies and named
failures; exact 12/24/23 universes; pure growth/drawdown/holdings; allocation
validation; one-time drift; mixed-calendar Crypto weekend compounding;
all-Crypto calendars; cost non-duplication; exact management-fee arithmetic;
allocation metrics; rolling display means; complete positive/negative fusion
evidence; Streamlit startup/navigation/interactions; and static AST guards
against model/raw-loader imports or app writes.

### Initial focused test attempt

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -p no:cacheprovider tests/test_app_data.py tests/test_app_logic.py tests/test_streamlit_app.py tests/test_smoke.py
```

Exit code: **1**. Summary: **18 passed, 5 failed, 2 errors**.

This run exposed:

1. one genuine compatibility defect: the installed Streamlit did not support
   `min_selections` on `st.multiselect`;
2. a non-methodological deprecation warning for `use_container_width`;
3. sandbox-denied reads of several protected canonical sentiment/fusion CSVs;
4. sandbox denial of pytest's Windows temporary directory; and
5. restricted network access for the explicitly required existing
   `tests/test_smoke.py` official-loader check.

Codex removed only the unsupported `min_selections` argument; the existing pure
allocation gate still enforces two-to-four selections. It replaced deprecated
Streamlit width arguments. Neither change altered data, allocation arithmetic,
analytics, or results. The same suite was then retried with authorised access
to the frozen CSVs, pytest temp folder, and unchanged official loader URLs.

### Corrected focused test run

Same command; exit code: **0**.

```text
collected 25 items
tests\test_app_data.py ......                                            [ 24%]
tests\test_app_logic.py ..........                                       [ 64%]
tests\test_streamlit_app.py .......                                      [ 92%]
tests\test_smoke.py ..                                                   [100%]
============================= 25 passed in 13.74s =============================
```

No test was weakened. The required negative disclaimer contains the word
“recommendation”; the wording guard therefore correctly blocks affirmative
sales/advice phrases while preserving that mandated disclosure.

## Local server and interaction evidence

Requested command semantics:

```powershell
$env:PYTHONDONTWRITEBYTECODE = '1'
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m streamlit run streamlit_app.py --server.headless true --server.port 8501
```

Two `Start-Process` wrapper attempts did not launch Python: Windows PowerShell
raised a case-insensitive duplicate `Path/PATH` environment-dictionary error,
even with `-UseNewEnvironment`. These were genuine launch-wrapper errors and
created no project artifact. Codex used the Windows process API with the same
executable, arguments, hidden window, working directory, and `-B`; the server
started as PID 8340.

- `/_stcore/health`: HTTP **200**, healthy.
- Root `/`: HTTP **200**, response content length **1,522**.
- `streamlit.testing.v1.AppTest` rendered the useful default fund comparison,
  selected Combined Risk Parity fact sheet, valid default Allocation Studio and
  invalid-total rejection, Sentiment & Innovation page with 23-row lexicon and
  24-row fusion table, and Methodology & Disclosures page.
- Repeated page/control runs passed without app exceptions and the AST guard
  confirmed no model/raw-loader import or app write path.
- The process was terminated cleanly; PID 8340 was no longer running.
- All external launch-attempt temp logs were removed; none existed inside
  Project B.

The in-app browser runtime was consulted for direct rendered inspection, but it
reported no connected browser (`[]`). Therefore **no direct browser visual
inspection is claimed**. Automated Streamlit rendering/interaction passed, but
the status remains pending the student's visual and interaction review.

## Hand-in checker

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exit code: **0**.

```text
22 checks passed.
1 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
All checks passed - ready to zip and deploy.
```

This is mechanical evidence only. It does not mean the report, deployment,
publication, submission package, or substantive project hand-in is complete.

## Absence of analytical recomputation

The Streamlit app imports only `src.app_data`, `src.app_logic`, and
`src.app_charts`. Static AST tests block runtime imports of `nltk`,
`src.data_access`, `src.portfolios`, `src.sentiment`, and `src.fusion`, and block
file-write calls in the app modules. No portfolio optimisation, VADER scoring,
fusion, canonical-output regeneration, or canonical-figure build command ran.

## Post-edit artifact and boundary evidence

The complete post-edit manifest was generated read-only after validation and
stored outside Project B at
`C:\Users\24116\AppData\Local\Temp\maia_stage8_post_manifest.tsv`.

- Pre-edit entries: **89**
- Post-edit entries: **97**
- Added: **8**, exactly the authorised new files listed above
- Changed: **4**, exactly `streamlit_app.py`, `.streamlit/config.toml`,
  `README.md`, and the chronological append to
  `ai/10_results_audit_and_exhibit_generation.md`
- Removed: **0**
- Unexpected paths: **0**
- Canonical CSV changes: **0 of 13**
- Canonical report PNG changes: **0 of 8**
- `.idea` changes: **0**; `.idea/workspace.xml` remained unchanged
- Cache/bytecode files: **0**

Every post-edit canonical hash exactly matched the pre-edit table above. No raw
data, result, PNG, report, environment, temporary project script, deployment,
publication, submission, or Git artifact appeared. The full manifest digest
before this audit file's final self-referential evidence update was
`C9297079674D600D9685F02751AFF37D8E60B70E3B4DEF1DA85761A0943C8C2E`.
The final digest after updating this one authorised audit file is reported in
the Codex handoff because a file cannot contain its own final hash without
changing it again.

## Limitations and deferred matters

- Direct browser visual inspection was unavailable because no browser instance
  was connected. The student must perform final visual and interaction review.
- Allocation Studio is a historical one-time sleeve illustration; it is not a
  new optimiser, live product, forecast, advice, or order system.
- The 0.50% p.a. fee is illustrative and separate from canonical analytical
  results.
- Streamlit Community Cloud deployment, Git operations/publication, report
  writing, submission packaging, and hand-in remain unauthorised and deferred.

`Pending student visual and interaction review — no deployment authorised.`

## Visual Correction Cycle 1 — external review and Codex verification

**Date:** 2026-08-14  
**Review status:** Pending student final review; no student acceptance claimed.

### Authority and provenance

The student supplied an independent ChatGPT review of the completed MAIA app
and authorised a presentation-only correction cycle. The external review
identified four issues: overlapping Equity/Combined risk-map labels;
selection-order-dependent growth-chart colours; overlapping long fusion x-axis
labels; and two raw sector names that needed reader-facing display aliases.

ChatGPT supplied the external review findings. Codex then independently
inspected the authorised chart code, implemented the display-only corrections,
added regression tests, rendered the affected chart types from frozen
precomputed artifacts, and directly inspected the rendered previews. The
student has not yet accepted these corrections.

The authorised authored boundary remained exactly:

- `src/app_charts.py`;
- `tests/test_streamlit_app.py`; and
- this chronological append to `ai/11_streamlit_implementation.md`.

No change to `streamlit_app.py`, app data/logic, source analytics, parameters,
canonical CSVs, canonical report PNGs, results, requirements, report, Git state,
or deployment was authorised or made.

### Pre-correction boundary evidence

A read-only manifest of Project B was stored outside the project at
`C:\Users\24116\AppData\Local\Temp\maia_stage8vc1_pre_manifest.tsv`.

- File count: **97**
- Manifest digest:
  `93ED5C221C839FCCFA1AEEF2B6131DFBD9BD7B6CA732EA7A2B106F7B6A791BAD`
- All thirteen canonical CSV and eight canonical report-PNG hashes matched the
  accepted Stage 8 hashes before editing.

### Exact corrections made

1. **Risk-return labels:** all 12 funds now use concise deterministic IDs
   (`Eq/Cr/Comb` and `EW/MV/MS/RP`), fixed per-fund offsets, subtle leader
   lines, white label backing, and plot margins. The subtitle explains every
   abbreviation across three unclipped lines. No point or scale changed.
2. **Growth colours:** `growth_chart` now derives each fund's frozen method
   from its deterministic `fund_id` and uses `METHOD_COLOURS`; selection order
   cannot change the colour. A single-fund chart uses the same method colour.
3. **Fusion labels:** the eight bases display as `Eq/EW`, `Eq/MV`, `Eq/MS`,
   `Eq/RP`, `Comb/EW`, `Comb/MV`, `Comb/MS`, and `Comb/RP`. The subtitle defines
   the abbreviations. All 24 overlay values, including negative values, remain.
4. **Sector names:** only chart display labels changed: `Comm` becomes
   `Comm/Telecom`, and `RealEstate` becomes `Real Estate`. Canonical source
   values remain unchanged.
5. **Title spacing:** chart titles use a lower top position, subtitles have
   dedicated vertical separation, and layout margin expands deterministically
   for multiline subtitles.

### Regression tests and genuine correction sequence

The focused tests added independent assertions for:

- stable method colours under reordered selection and a single-fund fact sheet;
- all 12 concise risk labels, canvas containment, and pairwise non-overlap;
- the exact eight fusion abbreviations, explanatory subtitle, and 48 bars
  representing 24 overlays across two panels; and
- the two display-only sector aliases without input-frame mutation.

First requested test run:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -p no:cacheprovider tests/test_app_data.py tests/test_app_logic.py tests/test_streamlit_app.py
```

Exit code: **1** — **26 passed, 1 failed**. The new geometry assertion found
remaining overlaps among `Eq/EW`, `Eq/MV`, and `Eq/RP`, and between `Eq/MS` and
`Comb/MV`. This was a genuine presentation defect; the assertion was retained.

An initial read-only diagnostic command exited **1** because Matplotlib selected
the unavailable Tk backend outside pytest. Codex reran it with the non-GUI Agg
backend; exit code **0**. The diagnostic identified the exact overlapping label
pairs and bounding boxes. Codex adjusted only the fixed annotation offsets.

The next complete focused run exited **0**:

```text
27 passed in 9.85s
```

Direct rendered inspection then found that the risk-map abbreviation line was
clipped at the right edge and that `Comb/MV` sat unnecessarily below the zero
line. Codex wrapped the subtitle into three lines and moved that one fixed
callout without moving any data point or changing an axis scale. The final
complete focused run exited **0**:

```text
27 passed in 9.75s
```

### Direct visual verification actually performed

Codex rendered five temporary previews outside Project B using only the frozen
precomputed artifacts and the display-only chart functions:

- all-12-fund risk-return map;
- reordered four-fund growth chart;
- single Maximum-Sharpe fund growth chart;
- complete 24-overlay fusion delta chart; and
- ten-sector reviewed-term exposure chart.

Codex directly inspected every preview. The final review verified:

- all 12 risk labels are identifiable, within the canvas, connected to their
  unchanged points, and not materially overlapping;
- title/subtitle blocks are separated and unclipped;
- Equal Weight is grey, Minimum Variance blue, Maximum Sharpe orange, and Risk
  Parity green regardless of selection order; the single Maximum-Sharpe path is
  orange;
- the fusion chart retains positive and negative values for all 24 overlays and
  shows the exact eight abbreviated bases with a readable key; and
- `Comm/Telecom` and `Real Estate` render while raw source categories remain
  unchanged.

The five temporary preview files and their exact Windows Temp directory were
deleted after inspection. No preview was written to Project B.

### Hand-in checker

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exit code: **0**.

```text
22 checks passed.
1 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
All checks passed - ready to zip and deploy.
```

This remains mechanical evidence only and does not authorise or establish
report, deployment, publication, Git, or submission completion.

### Final frozen-artifact and boundary evidence

The first final-manifest attempt used PowerShell `Get-FileHash`. Windows denied
that command access to 16 locked canonical sentiment/fusion CSV and report-PNG
artifacts, so their missing hashes appeared as false changes. A shared-read
`FileStream` retry inside the sandbox was also denied. Codex did not accept
either attempt as integrity evidence. The identical read-only shared-read audit
was then run with authorised filesystem access and exited **0**. This corrected
only the audit access mechanism; it changed no student decision, chart, test,
model, parameter, project document, canonical artifact, or result.

The successful comparison used:

- pre-manifest path:
  `C:\Users\24116\AppData\Local\Temp\maia_stage8vc1_pre_manifest.tsv`;
- post-manifest path:
  `C:\Users\24116\AppData\Local\Temp\maia_stage8vc1_post_manifest.tsv`;
- pre-manifest digest:
  `93ED5C221C839FCCFA1AEEF2B6131DFBD9BD7B6CA732EA7A2B106F7B6A791BAD`;
- post-manifest digest before this final self-referential log update:
  `A1197AFA80C811A1D7F2D17B4268395168AE365DFE1D73AAE945990E3071CE71`.

The successful boundary result was:

- pre-edit entries: **97**;
- post-edit entries: **97**;
- added: **0**;
- removed: **0**;
- changed: **3**, exactly `src/app_charts.py`,
  `tests/test_streamlit_app.py`, and this authorised chronological append to
  `ai/11_streamlit_implementation.md`;
- unexpected changes: **0**;
- canonical CSV changes: **0 of 13**;
- canonical report-PNG changes: **0 of 8**;
- `.idea` changes: **0**;
- cache or bytecode artifacts: **0**.

A final log-location check found that this correction section had initially
been anchored to a matching status sentence inside the preserved verbatim Stage
8 prompt. Before handoff, Codex restored that prompt and moved the correction
record unchanged to the true chronological file end. This was a documentation-
placement correction only; it changed no student decision, method, test,
application behaviour, canonical artifact, or result. The final manifest digest
after this audit file's last update is reported in the Codex handoff because a
file cannot contain its own final hash without changing it again.

`Stage 8 Visual Correction Cycle 1 completed; pending student final review. No analytical output, model, parameter, report figure, report, deployment, or Git state changed.`

## Stage 8 Visual Correction Cycle 2

**Date:** 2026-08-14  
**Review status:** Pending student final visual review; no student acceptance
claimed.

### Student review evidence and scope

The student visually reviewed the corrected running MAIA app and supplied
independent screenshot evidence. The student did not grant final Stage 8
acceptance because the teal kicker, “MAIA · MULTI-ASSET INVESTMENT ASSISTANT”,
was still clipped beneath Streamlit's fixed toolbar. The screenshot showed that
the main “Explore Funds” heading itself was visible. The defect was therefore
identified as shared page-level header spacing rather than analytical content,
chart content, data, or a model result.

The student authorised changes only to `streamlit_app.py`,
`tests/test_streamlit_app.py`, and this chronological append. No new project
file, analytical rerun, chart change, canonical-artifact change, report,
deployment, publication, submission, or Git operation was authorised.

### Complete operational prompt received

~~~text
Stage 8 Visual Correction Cycle 2 only.

The student has completed the final visual review and does not yet accept Stage 8.

The student-provided screenshot confirms that the main “Explore Funds” heading is visible, but the teal MAIA kicker immediately above it is clipped underneath the fixed Streamlit toolbar. Only the lower part of:

“MAIA · MULTI-ASSET INVESTMENT ASSISTANT”

is visible.

This is a page-layout/CSS defect, not a chart defect. Do not modify any chart, model, result, metric, data, parameter, or canonical artifact.

Exact workspace:
C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Authorised modifications only:
- streamlit_app.py
- tests/test_streamlit_app.py
- ai/11_streamlit_implementation.md

No new file may be created.

Required correction:

1. Correct the shared page-header safe area in streamlit_app.py.
2. The current `.block-container` top padding is insufficient under Streamlit’s fixed toolbar.
3. Use a restrained responsive top padding or equivalent safe layout so that:
   - the complete teal MAIA kicker is visible;
   - the page title is fully visible;
   - neither element sits underneath the toolbar;
   - no excessive blank space is introduced;
   - all five pages use the same correct alignment;
   - normal desktop and narrower layouts remain readable.
4. Do not hide or remove the MAIA kicker merely to make the test pass.
5. Do not hide the Streamlit toolbar or use fragile negative positioning.
6. Preserve the existing MAIA colours, typography hierarchy, sidebar, navigation, disclosures, and page content.

Validation:

- Run all five pages through Streamlit AppTest and confirm zero exceptions.
- Add a focused regression assertion that the shared page-header safe-area CSS remains present and that the MAIA kicker and all five page titles remain rendered.
- If browser inspection is available, inspect the top of all five pages at desktop and narrower width.
- If browser inspection is unavailable, state this honestly and leave final pixel-level acceptance to the student.
- Run:

& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -p no:cacheprovider tests/test_streamlit_app.py

- Then run:

& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py

- Confirm all 13 canonical CSVs and all eight canonical report PNGs remain byte-identical.
- Confirm only the three authorised files changed.
- Do not start the report, deployment, Git, publication, or another stage.

AI-workflow record:

Append a chronological section titled:

“Stage 8 Visual Correction Cycle 2”

to ai/11_streamlit_implementation.md.

Record:
- the student visually reviewed the corrected running App;
- the student supplied screenshot evidence;
- the student rejected final Stage 8 acceptance because the teal MAIA kicker remained clipped;
- the main Explore Funds heading itself was visible;
- the defect was traced to page-level header spacing rather than analytical or chart content;
- the complete prompt received;
- the exact CSS correction;
- tests, checker output, artifact hashes, and file-boundary evidence;
- any genuine failed attempt;
- final review status.

Do not claim student acceptance.

Final status must remain:

Stage 8 Visual Correction Cycle 2 completed; pending student final visual review. No analytical output, model, parameter, canonical report figure, report, deployment, publication, submission, or Git state changed.
~~~

### Exact correction

The single app change replaced the fixed `2.0rem` content-top padding with this
shared fixed-toolbar safe area:

~~~css
.block-container {
    padding-top: clamp(4.25rem, 8vh, 5rem);
    padding-bottom: 3rem;
    max-width: 1280px;
}
@media (max-width: 768px) {
    .block-container { padding-top: 4.75rem; }
}
~~~

The clamp rule supplies restrained height-responsive desktop clearance. The
narrow-layout media rule preserves toolbar clearance without negative
positioning. The same `.block-container` and `_header` structure serves all
five pages. The MAIA kicker, title, colours, typography, sidebar, navigation,
disclosures, and page content remain present. No toolbar-hiding selector was
added.

The focused regression test verifies the exact responsive safe-area rules,
requires the kicker to remain in source, rejects an app toolbar selector, and
runs all five navigation states with zero AppTest exceptions. It also verifies
that every page renders exactly one full MAIA kicker and its corresponding
title.

### Environment and validation sequence

PyCharm reported the verified shared environment:

- executable:
  `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`;
- Python **3.13.13**;
- Streamlit **1.58.0**.

First requested test attempt:

~~~powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -p no:cacheprovider tests/test_streamlit_app.py
~~~

Exit code: **1**. Result: **1 passed, 11 failed**. Matplotlib selected its Tk
GUI backend, but the local Python installation could not locate a usable
`init.tcl`; chart creation therefore failed before the app assertions ran.
Codex made the authorised test module self-contained by selecting Matplotlib's
non-GUI `Agg` backend before importing `pyplot`. This changed no chart,
application behaviour, canonical artifact, analytical method, or result.

Second unchanged test command under the default sandbox exited **1** with
**11 passed, 1 failed**. The Sentiment page had no readable canonical tables in
that sandbox context, although the app caught the artifact-access condition and
raised no Streamlit runtime exception. No assertion was weakened. The exact
command was rerun with authorised read access to the immutable artifacts and
exited **0**:

~~~text
collected 12 items
tests\test_streamlit_app.py ............                                 [100%]
============================= 12 passed in 14.61s =============================
~~~

This successful run rendered all five navigation pages with zero AppTest
exceptions and passed the new shared-header regression.

### Browser inspection status

The unchanged local app reached HTTP **200** at
`http://127.0.0.1:8501/_stcore/health`. The available browser runtime reported
no connected browser (`[]`). Consequently, Codex does **not** claim direct
desktop or narrow-width pixel inspection. The temporary Streamlit process was
stopped cleanly and port 8501 was no longer listening. Final pixel-level
acceptance remains with the student.

### Hand-in checker

Command:

~~~powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
~~~

Exit code: **0**.

~~~text
22 checks passed.
1 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
All checks passed - ready to zip and deploy.
~~~

This is mechanical evidence only and does not establish report, deployment,
publication, submission, or substantive hand-in completion.

### Frozen canonical artifact hashes

All values below matched the in-memory pre-correction manifest after the CSS
change and validation:

| Frozen artifact | SHA-256 |
|---|---|
| `results/data/fund_returns.csv` | `7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84` |
| `results/data/fund_weights.csv` | `F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8` |
| `results/tables/performance_metrics.csv` | `5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19` |
| `results/tables/portfolio_solver_diagnostics.csv` | `ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C` |
| `results/tables/extreme_sensitivity_metrics.csv` | `40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151` |
| `results/data/sector_sentiment_index.csv` | `D7670369187E3FF6909A88F6459204284A45D07941DC395CE239D8E304E8E96E` |
| `results/data/ticker_sentiment_daily.csv` | `CC9DDF834EF43B9B07240A40949716BA573A14E6ADDCD1997DFF83C125E26FCD` |
| `results/data/fusion_returns.csv` | `5A868D15E4D649FEDCB7BF9A0D58657F1729D6F35A2A62A2DF148622EA8CEBC5` |
| `results/data/fusion_weights.csv` | `13941551A0D3D9A07290235CCEF7C8AB389D2F78EAF36D81CE661A915F485058` |
| `results/tables/sentiment_diagnostics.csv` | `3C7842ED0F955DCA29E1E728EFD51C46AA12D4B93999DC9C72D47C436AC179B5` |
| `results/tables/finance_lexicon.csv` | `5E6EE31DADC6C754DD465E825FBA5F25B3BD26E5E0AA846B3A578619D444C5DB` |
| `results/tables/fusion_performance_metrics.csv` | `B75FA251E385E3709D3EC1380367D0257285D249AF742965C8FD993FCA770A07` |
| `results/tables/fusion_comparison.csv` | `B51DF470AEAB5932356037DF72FCF0044729C6F9F88C117E6C4B90F4922C3946` |
| `results/figures/fund_growth_comparison.png` | `68AA156B18AACC824346C8820C1B941623FA0D13BA6627AAFB17848EF1F625BE` |
| `results/figures/combined_drawdowns.png` | `DAA1415C7406098E61E250122A5B1AC11240B8858C2949A482EC453308D59C81` |
| `results/figures/combined_weights_over_time.png` | `04A8B663D6C1CB29F6E9D8D7CB2A6DD16C90A1C31D9920543E6A2364CC74F1E6` |
| `results/figures/fund_risk_return_map.png` | `C7CF65BF38BA38214659F28D0CA84B1BD7528C1D74BCCD2B62BBDCA18BC721E8` |
| `results/figures/sector_sentiment_timeseries.png` | `7A210A89713955EAB7C459F4C3D8044E5317D49733142A9D1B652669A6012FB7` |
| `results/figures/fusion_before_after.png` | `7789948051C8FBDA8A0E9659C066086C301D972E956465B7EB49156041A994DF` |
| `results/figures/sentiment_innovation_diagnostics.png` | `1A1F2DAC8AE4330D01B6DAA19FC9D18461A55919A276AD27B12826755D2F97C8` |
| `results/figures/fusion_turnover_tradeoff.png` | `9D483E2247EE05DC8E90451F63A77F035D586BDC04137BBE1965737CA30B641B` |

### Boundary evidence

The pre-correction in-memory manifest contained **97** files with digest
`835794ECB2EC437E9599B8EDA9DCE29EEEA7B311F725F8C0C939C36DFDFD76EE`.
The comparison immediately before this chronological log append also contained
**97** files with digest
`7B963F303A3D44D2890E33A32CC43989952688521FBB2334561035934F086CC7`.
At that point exactly `streamlit_app.py` and `tests/test_streamlit_app.py` had
changed; no path was added or removed, no canonical artifact or `.idea` file
changed, and no unexpected path appeared.

The first compressed final-boundary command exited **1** before hashing because
PowerShell resolved its one-letter helper name as the history alias and tried
to parse a file path as a history identifier. The corrected read-only command
used an unambiguous helper name and exited **0**. Neither attempt wrote a
project file or changed the app, test, artifact, or methodology.

The corrected final comparison contained **97** files with digest
`240E84AE24AB25D4DD2AFE974FF76CEC65BF2E82E75447FA6D9A5A35E56DD85B`
before this final self-referential log update. It verified:

- changed: exactly `streamlit_app.py`, `tests/test_streamlit_app.py`, and
  `ai/11_streamlit_implementation.md`;
- added: **0**;
- removed: **0**;
- unexpected paths: **0**;
- canonical changes: **0 of 13 CSVs** and **0 of 8 report PNGs**;
- `.idea` changes: **0**.

The final manifest digest after this last audit-log update is reported in the
Codex handoff because recording a file's own hash would change that hash again.

`Stage 8 Visual Correction Cycle 2 completed; pending student final visual review. No analytical output, model, parameter, canonical report figure, report, deployment, publication, submission, or Git state changed.`

## Final student visual and interaction acceptance

**Date:** 2026-08-14

The student stated exactly:

> I have personally inspected MAIA’s five pages, representative funds, the
> Allocation Studio, Sentiment & Innovation, and Methodology & Disclosures. The
> current display, interactions and results align with my understanding, and I
> accept the current Stage 8 version.

The student made the final decision and approval. The inspection was conducted
collaboratively by the student and ChatGPT, while Codex performed the authorised
local implementation, tests and technical corrections recorded above.

This acceptance closes the local Stage 8 Streamlit implementation and its two
visual-correction cycles. It confirms student review of the current display,
interactions and results.

It does not claim that the report, GitHub repository, public deployment, Moodle
package or final submission has been completed.
