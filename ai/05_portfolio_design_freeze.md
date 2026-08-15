# Stage 4B — Pre-result OOS Portfolio Design Freeze

**Date:** 2026-08-14  
**Status:** Pending student review

## Objective and exact authorisation

Document a complete, testable out-of-sample portfolio and backtest proposal before any portfolio result is calculated. This prespecification is intended to reduce look-ahead, data mining, and result-driven changes. It is a workflow governance stage, not implementation and not the teacher's DFF Station 4.

The student stated exactly:

> “I accept the Stage 4A implementation, test evidence, validation results, genuine error-and-correction record, and file-boundary audit. I authorise Workflow Stage 4B only: document and freeze the out-of-sample portfolio and backtest design before any portfolio result is calculated. No implementation, optimisation run, model output, figure, sentiment work, fusion, Streamlit, report writing, deployment, or Git operation is authorised.”

## Complete operational prompt

The following is the complete prompt received for this cycle:

```text
You are working on FINS5545 Project B.

By sending this prompt, the student states:

“I accept the Stage 4A implementation, test evidence, validation results, genuine error-and-correction record, and file-boundary audit. I authorise Workflow Stage 4B only: document and freeze the out-of-sample portfolio and backtest design before any portfolio result is calculated. No implementation, optimisation run, model output, figure, sentiment work, fusion, Streamlit, report writing, deployment, or Git operation is authorised.”

This is Workflow Stage 4B only: Pre-result OOS Portfolio Design Freeze.

Its purpose is to prove that all material portfolio choices were selected before seeing portfolio performance, reducing look-ahead, data-mining, and result-driven parameter changes.

This workflow stage is not the teacher’s DFF Station 4.

## Exact workspace

Project root and terminal working directory must both resolve exactly to:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Do not inspect Project A, sibling folders, or the broader repository.

No data loading or Python modelling command is required for this documentation-only stage.

## Authorised file boundary

Append only:

- `ai/04_data_foundation_implementation.md`

Create only:

- `docs/portfolio_backtest_design.md`
- `ai/05_portfolio_design_freeze.md`

Do not modify or create anything else, including source code, tests, results, figures, report files, requirements, Streamlit files, `.idea`, or Git state.

Verify both new targets are absent before editing. If either exists, stop rather than overwrite it.

## Required reading

Read completely:

- `AGENTS.md`
- `PROJECT_BRIEF.md`, especially Part B Station 3, common mistakes, required exhibits, rubric, and AI-workflow requirements
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `docs/data_contract.md`
- `ai/04_data_foundation_implementation.md`
- current `src/portfolios.py`
- current `src/features.py`
- current `scripts/run_part_b.py`
- `scripts/check_handin.py`

Do not run portfolios or inspect portfolio performance.

## Close Stage 4A

Append a chronological section to `ai/04_data_foundation_implementation.md` titled:

`Final student acceptance — Stage 4A closed`

Record the student’s exact acceptance above and final status:

`Stage 4A accepted and closed; Stage 4B authorised for pre-result portfolio-design documentation only.`

Do not rewrite the earlier record.

## Create `docs/portfolio_backtest_design.md`

Mark it:

`Proposed pre-result OOS portfolio design — pending student review`

Document the following frozen proposal clearly and professionally.

### 1. Investment product

Create twelve investable funds:

Three families:

- `Equity`: the frozen 50-equity universe;
- `Crypto`: the frozen 10-crypto universe;
- `Combined`: the 50 equities followed by the 10 cryptocurrencies in frozen order.

Four methods within every family:

- Equal Weight;
- Minimum Variance;
- Maximum Sharpe;
- Risk Parity.

Use deterministic fund IDs and names. Each family-method pair is one fund and receives its own fact sheet later.

This selection satisfies the high-band breadth requirement without adding shallow extra methods. The main innovation remains the separately approved sentiment/lexicon/fusion path, not an unnecessary fifth optimiser.

### 2. OOS calendars and windows

Freeze:

- Equity funds: native equity trading calendar, annualisation 252.
- Crypto funds: native seven-day crypto calendar, annualisation 365.
- Combined funds: equity trading calendar with crypto returns already calculated on the native crypto calendar before selection, annualisation 252.
- Rolling estimation windows:
  - 252 complete past return observations for Equity and Combined;
  - 365 complete past return observations for Crypto.
- Rebalance on the first observed eligible date of each calendar month.
- The first live date is the first monthly rebalance date with the full required number of strictly prior complete returns.
- On decision/rebalance date `t`, estimation may use only returns dated strictly before `t`.
- Target weights formed at `t` apply to the realised return at `t`.
- Do not use expanding windows, future observations, pairwise-deletion covariance, backfilled data, or a backtest beginning on the first source date.
- Exact first live dates will be measured and recorded during authorised implementation; the rule selecting them is frozen now.

### 3. Portfolio constraints

For every fund:

- long-only: `0 <= weight_i <= 0.20`;
- fully invested: weights sum to one;
- no leverage;
- no short selling;
- no forced minimum allocation to either asset class in Combined funds;
- no post-processing that changes valid weights merely to make methods appear different.

The 20% cap is a product-level concentration guardrail and is feasible for all three universes. If a valid Combined optimiser assigns zero or near-zero crypto weight, retain and interpret that result.

### 4. Estimation and optimisation

Use:

- simple decimal returns from the frozen data foundation;
- sample arithmetic mean and sample covariance from the authorised past-only window;
- risk-free rate `0`;
- annualised mean and covariance using the family’s fixed annualisation factor;
- deterministic asset order;
- covariance symmetrisation and only the smallest deterministic numerical eigenvalue/ridge repair needed for positive-semidefinite solver stability;
- no economically meaningful covariance shrinkage or parameter tuning unless separately approved later.

Methods:

1. Equal Weight:
   `w_i = 1/N` at every rebalance.

2. Minimum Variance:
   minimise `w'Σw` subject to the frozen constraints.

3. Maximum Sharpe:
   maximise `(w'μ - r_f) / sqrt(w'Σw)` with `r_f = 0`, subject to the frozen constraints.

4. Risk Parity:
   minimise squared deviations of normalised variance contributions from `1/N`, subject to the frozen constraints.

Optimisation must use deterministic initial values and a documented solver configuration. Record every solver status, iteration/message, constraint residual, and objective value.

No silent fallback is allowed. One deterministic retry from an authorised feasible starting point may be used and logged. A persistent solver failure, invalid constraint, non-finite objective, or materially infeasible weight vector is a BLOCK, not a reason to substitute invented weights.

Near-identical methods are a diagnostic condition, not permission to perturb weights.

### 5. Weight timing and drift

At each rebalance:

1. Use only information through `t-1`.
2. Observe the pre-trade weights resulting from prior portfolio drift.
3. Trade to the new target weights.
4. Apply the target weights to date-`t` asset returns.
5. After returns, update holdings weights by:

   `w_post,i = w_pre-return,i × (1 + r_i) / (1 + r_portfolio)`

6. Carry the post-return weights forward until the next return or rebalance.

Between rebalances, do not reset weights daily to the target. They must drift with realised asset returns.

The most recent rebalance target weights are the “current holdings” shown in a later fact sheet, with the date clearly stated.

### 6. Turnover and transaction costs

Freeze one-way turnover at a rebalance as:

`turnover_t = 0.5 × Σ_i |target_weight_i - pretrade_weight_i|`

The initial portfolio formation is excluded from turnover and cost statistics and disclosed.

Freeze transaction cost at 5 basis points per unit of turnover:

`cost_t = 0.0005 × turnover_t`

Retain both:

- gross fund return before costs;
- net fund return after costs.

Apply the cost multiplicatively before the rebalance-date investment return:

`net_return_t = (1 - cost_t) × (1 + gross_return_t) - 1`

The user-facing fact sheet and primary performance comparison will use net returns. Gross results remain available as a transparent zero-cost comparison.

Do not tune the 5-bps assumption after observing performance. Further cost scenarios require explicit later approval.

### 7. Performance definitions

For each fund, calculate over its live OOS period:

- cumulative growth and cumulative return;
- annualised geometric return:
  `(Π(1+r_t))^(A/n) - 1`;
- annualised volatility:
  `std(r_t, ddof=1) × sqrt(A)`;
- Sharpe ratio with zero risk-free rate:
  `mean(r_t) / std(r_t, ddof=1) × sqrt(A)`;
- maximum drawdown from the compounded wealth index;
- rebalance count;
- average and total turnover;
- transaction-cost drag;
- current holdings from the latest target weights.

Use net returns for the primary metrics and retain clearly prefixed gross comparison metrics. Never describe backtested performance as guaranteed investor returns.

### 8. Portfolio output schemas

Freeze the model-dependent portfolio schemas now.

`results/data/fund_returns.csv`, long format:

- `date`
- `fund_id`
- `family`
- `method`
- `gross_return`
- `turnover`
- `transaction_cost`
- `net_return`
- `is_rebalance`

One row per live OOS fund-date.

`results/data/fund_weights.csv`, rebalance holdings:

- `date`
- `fund_id`
- `family`
- `method`
- `ticker`
- `pretrade_weight`
- `target_weight`
- `trade_weight`
- `turnover`
- `solver_success`
- `solver_status`

One row per fund-rebalance-asset. Equal Weight uses a deterministic non-solver status.

`results/tables/performance_metrics.csv`:

- `fund_id`
- `family`
- `method`
- `start_date`
- `end_date`
- `observations`
- `annualisation`
- `transaction_cost_bps`
- `net_cumulative_return`
- `net_annualised_return`
- `net_annualised_volatility`
- `net_sharpe_ratio`
- `net_max_drawdown`
- `gross_cumulative_return`
- `gross_annualised_return`
- `gross_sharpe_ratio`
- `average_rebalance_turnover`
- `total_turnover`
- `rebalance_count`

Do not create these files in Stage 4B.

### 9. Validation and anti-leakage tests required later

Specify implementation tests for:

- exactly twelve family-method funds;
- correct 252/365 calendars and annualisation;
- exact rolling-window membership;
- first live date after the full initial window;
- every decision date using only dates `< t`;
- future-data perturbation leaving all earlier weights unchanged;
- monthly rebalance-date selection;
- non-negative weights, 20% cap and sums of one;
- deterministic asset order and reruns;
- manual Minimum-Variance, Maximum-Sharpe and Risk-Parity objective/constraint checks;
- solver status and retry logging;
- near-identical-method diagnostics;
- correct daily weight drift;
- turnover calculated from pretrade drifted weights rather than prior target weights;
- correct gross/net cost arithmetic;
- initial formation excluded from turnover;
- performance metrics checked against manual synthetic examples;
- output schema, key uniqueness, row counts and no placeholder values.

Tests must not merely repeat production helper functions when an independent formula or small synthetic example can be used.

### 10. Prespecified interpretation and robustness rules

Freeze before results:

- Poor or negative OOS performance remains reportable.
- Maximum Sharpe is expected to be estimation-sensitive; do not hide weak results.
- Near-zero Combined crypto weights may be economically valid.
- Large crypto volatility can make Risk-Parity crypto weights small.
- Do not change windows, cap, risk-free rate, rebalance frequency, cost, optimiser, sample, or reported funds merely to improve results.
- Any later change requires a dated, student-approved robustness rationale and must retain the original frozen specification.
- The 69 extreme observations remain in canonical results. A separately labelled later sensitivity run may clip them to ±25% in both estimation and realised-return inputs, but cannot replace canonical results and requires explicit implementation authorisation.
- Negative robustness or innovation findings must be reported honestly.

### 11. Deferred matters

Explicitly defer:

- all portfolio code and solver execution;
- exact first live dates and empirical performance;
- extreme-observation sensitivity implementation;
- figures and fact sheets;
- sentiment, finance lexicon and fusion;
- app, report and deployment;
- any empirical conclusion.

End with:

`Pending student review — no portfolio implementation or result authorised.`

## Create `ai/05_portfolio_design_freeze.md`

Record:

- date and objective;
- exact student authorisation;
- complete operational prompt;
- files read;
- roles of student, ChatGPT and Codex;
- rationale for every frozen choice;
- feasibility review of the calendars, windows, 20% cap and output schemas;
- risks addressed, especially leakage, solver scaling, weight drift, turnover and data mining;
- genuine concerns or corrections, if any;
- checker and manifest evidence;
- student-review status;
- next implementation action requiring explicit approval.

Do not invent an error, result, approval or correction.

## Validation

Run only:

& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py

Do not load data or run portfolio code.

Capture pre/post manifests and confirm:

- only `ai/04_data_foundation_implementation.md` changed;
- only the two authorised documents were created;
- nothing else changed or appeared;
- `.idea` remained unchanged.

## Final response

Report:

- workspace guard;
- Stage 4A closure;
- proposed frozen design;
- exactly one modified and two created files;
- checker result;
- boundary result;
- unresolved matters;
- status:

`Stage 4B pre-result OOS portfolio design documented; pending student review. No portfolio result generated.`

Stop. Do not implement or run portfolios.
```

## Files read

- `AGENTS.md`
- `PROJECT_BRIEF.md` in full, including Part B Station 3, common mistakes, required exhibits, the rubric, and AI-workflow requirements
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `docs/data_contract.md`
- `ai/04_data_foundation_implementation.md`
- `src/portfolios.py`
- `src/features.py`
- `scripts/run_part_b.py`
- `scripts/check_handin.py`

Project A, sibling folders, the broader repository, data sources, portfolio performance, and unlisted files were not inspected.

## Roles and provenance

- **Student:** accepted Stage 4A, selected and authorised the complete Stage 4B proposal, prohibited result generation, and retains authority to accept, reject, or revise the design and authorise any implementation.
- **ChatGPT:** its earlier assistance with the staged workflow and requirement interpretation is recorded in prior logs; it did not run a local portfolio, see performance, or approve this proposal on the student's behalf.
- **Codex:** verified the local boundary, read the governing materials, reconciled the prescribed choices into a testable specification, appended the acceptance record, ran only the checker, and recorded the evidence. Codex did not load data, implement a portfolio, invoke a solver, or observe a portfolio result.

## Frozen choices and rationale

| Choice | Prespecified proposal | Rationale before results |
|---|---|---|
| Product breadth | 3 families × 4 methods = 12 funds | Satisfies the official high-band breadth without an unnecessary fifth optimiser; keeps planned innovation focused on the separately governed sentiment/lexicon/fusion work. |
| Asset membership | Frozen 50 Equity, 10 Crypto, and 60 Combined in equity-then-crypto order | Preserves the accepted data contract and prevents encounter-order or selection bias. |
| Calendars | Equity 252, Crypto 365, Combined 252 | Matches native trading opportunities; Combined selects already-calculated native crypto returns onto the equity calendar. |
| Windows | Rolling 252 complete prior rows for Equity/Combined; 365 for Crypto | Uses about one calendar/trading year, prohibits expanding or pairwise samples, and fixes responsiveness before outcomes. |
| Rebalancing | First observed eligible date per calendar month | Complies with the monthly-or-less-frequent brief, limits turnover, and provides a deterministic schedule. |
| Information timing | Estimation dates strictly `< t`; target applies to return at `t` | Provides an explicit, testable no-look-ahead boundary. |
| Constraints | Long-only, fully invested, 20% cap, no asset-class floor | Provides a concentration guardrail while allowing economically valid zero/near-zero crypto allocations. |
| Moments and risk-free rate | Arithmetic sample mean, sample covariance, zero risk-free rate | Transparent baseline permitted by the brief; avoids an additional external data source or tunable estimator. |
| Numerical policy | Symmetrisation and a scale-relative minimum ridge only when needed | Addresses floating-point/PSD stability without introducing economically meaningful shrinkage. |
| Optimiser | Deterministic SLSQP configuration, equal-weight primary seed, one frozen staggered retry seed | Addresses official solver-scaling risk while prohibiting silent fallbacks or post-result tuning. |
| Benchmark and objectives | Equal Weight, Minimum Variance, Maximum Sharpe, Risk Parity | Provides a transparent benchmark and three distinct standard economic objectives. |
| Drift | Targets drift with realised returns between monthly rebalances | Represents investable holdings and prevents accidental daily rebalancing. |
| Turnover | One-way half-L1 distance from drifted pre-trade weights | Measures actual rebalancing trades rather than stale target-to-target changes. |
| Costs | 5 bps per unit turnover; multiplicative; initial formation excluded | Adds a transparent prespecified implementation friction without tuning to performance. |
| Primary performance | Net returns and geometric/volatility/Sharpe/drawdown definitions; gross retained | Aligns the fact sheet with investor experience while preserving a zero-cost comparator. |
| Extremes | All 69 retained canonically; optional ±25% sensitivity only if later approved | Preserves the frozen base data and prevents outcome-driven deletion; separates robustness from canonical results. |
| Outputs | Three exact long schemas with fixed keys and ordering | Supports reproducibility, fact sheets, required exhibits, and later app consumption without creating placeholders now. |

## Feasibility review

- **Calendars and windows:** the accepted contract records 1,006 equity/combined dates and 1,461 native crypto dates. Even after legitimate initial missing returns, each contains more observations than its 252/365 window. This proves room for a live OOS segment without measuring or claiming an exact first date.
- **20% cap:** feasibility follows from total capacity: 50 × 0.20 = 10, 10 × 0.20 = 2, and 60 × 0.20 = 12, each exceeding one. Equal weights are feasible for all three families.
- **Solver scaling:** annualised moments, normalised Risk-Parity contributions, a fixed scale-relative covariance floor, explicit SLSQP tolerances, deterministic feasible starts, and residual validation address the brief's warning about objectives on tiny daily covariances.
- **Output schemas:** `date + fund_id`, `date + fund_id + ticker`, and `fund_id` provide deterministic unique keys for returns, holdings, and metrics. Fixed categories/order support exact tests and later joins.
- **Required exhibits:** the proposed returns, weights, and metrics schemas can later support growth, drawdown, holdings/weights-over-time, Sharpe/return-risk comparisons, and individual fact sheets. No exhibit or result is claimed here.

## Risks addressed

The proposal directly controls:

- look-ahead through strict `< t` windows and future-perturbation tests;
- sample drift and hidden missingness through complete fixed-length windows;
- calendar and annualisation mismatch through family-specific rules;
- solver stalling, scaling, non-convergence, and hidden fallback through fixed diagnostics and BLOCK conditions;
- output manipulation through fixed fund membership, order, methods, constraints, and near-identical diagnostics;
- unrealistic daily target resets through explicit holding drift;
- understated turnover through comparison with drifted pre-trade weights;
- hidden implementation costs through gross/net retention and a frozen 5-bps convention;
- data mining through dated approval requirements and retention of the original specification;
- outlier deletion through canonical retention of all 69 extremes.

## Genuine concerns and reconciliations

1. The required holdings schema has one `solver_status` field, while the proposal also requires iterations, messages, objectives, residuals, and retry evidence. The design reconciles these without adding an unapproved required column: `solver_status` is frozen as a deterministic sorted-key JSON diagnostic string and is repeated across that fund-rebalance's asset rows.
2. Excluding initial formation from turnover statistics creates an intentional exception to the half-L1 formula. The design makes inception auditable with zero pre-trade weights and target-sized trades while explicitly recording turnover and cost as zero on that first live date. Later tests must check this exception rather than conceal it.
3. Maximum Sharpe and Risk Parity are nonlinear and can depend on numerical starting values. The design therefore fixes both starts and permits one retry only; it does not assert successful convergence before implementation.
4. A pre-existing metadata inconsistency remains in `docs/data_contract.md`: its header says “Proposed frozen input contract — pending student review,” while Section 12 says “Accepted and frozen by student — 2026-08-14,” and the student's acceptance is also recorded in the AI logs. This cycle does not authorise modifying that file. The inconsistency does not change the accepted substantive contract but should be corrected only in a later explicitly authorised documentation cycle.

No fabricated error, result, correction, or approval was added. No official requirement conflicted with the student's prescribed portfolio choices.

## Validation command and checker evidence

Before the sole Python invocation, PyCharm reported Python 3.13.13 at the authorised existing environment:

`C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`

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

This is mechanical structure evidence only. The six reminders are expected because model outputs and the report remain unauthorised and absent. The checker's final sentence is not substantive completion evidence.

No data-loading, test, portfolio, optimisation, solver, performance, or other Python command was run.

## Manifest and boundary evidence

The pre-edit manifest included `.idea`, excluded `.git`, environments, caches, bytecode, and compiled files, and recorded:

- file count: `46`;
- canonical SHA-256 digest: `F32DDA333CF68EB152E40F7FF576421B88F2FBA56F63ED7CFF5A6E6E53885F48`;
- reparse points: `0`.

Immediately before creating this log, the matching 47-file snapshot had digest `EDD4D413CC3FD1F1CA33A44CF6C7882F7D4377D2FD46A25D055BDFA68DA6DA3C`. Direct comparison showed only `ai/04_data_foundation_implementation.md` modified and only `docs/portfolio_backtest_design.md` added; nothing was removed or unexpectedly changed.

This provenance log is the second authorised new document. Its own final hash cannot be embedded without changing that hash. The authoritative post-edit manifest and full pre/post path comparison will be calculated after this final edit and reported without another project mutation.

## Deferred matters and student-review status

All implementation, exact first live dates, optimiser results, portfolio outputs, robustness execution, figures, sentiment, fusion, app, report, deployment, publication, and Git work remain deferred.

**Pending student review.** The student must review and explicitly accept, reject, or revise `docs/portfolio_backtest_design.md`. A later portfolio-implementation stage—including edits to `src/portfolios.py`, tests, solver execution, and output generation—requires a new, explicit scope authorisation. Nothing continues automatically.

## Final student acceptance — Stage 4B closed

On 2026-08-14, the student stated exactly:

> “I accept the Stage 4B pre-result OOS portfolio design, including the twelve funds, calendars, rolling windows, monthly timing, constraints, solver policy, weight drift, turnover, 5-bps transaction-cost convention, performance definitions, output schemas, anti-leakage tests, and prespecified interpretation rules. I authorise Workflow Stage 5A only: implement, test, and run the frozen portfolio design; create the canonical required portfolio outputs and separately labelled ±25% extreme-return sensitivity evidence. No sentiment scoring, finance lexicon, fusion, figures, fact-sheet design, Streamlit, report writing, deployment, publication, or Git operation is authorised.”

This accepts the prespecified design before portfolio performance was generated. It authorises only the frozen Stage 5A implementation, tests, canonical portfolio outputs, and separately labelled extreme-return sensitivity evidence. It does not authorise any sentiment, lexicon, fusion, figure, fact-sheet, application, report, deployment, publication, or Git work.

**Stage 4B accepted and closed; Stage 5A authorised for frozen OOS portfolio implementation only.**
