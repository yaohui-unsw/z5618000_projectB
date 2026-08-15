# Stage 5A — Frozen OOS Portfolio Implementation

**Date:** 2026-08-14 (Australia/Sydney)  
**Status:** Pending student review

## Objective and exact student authorisation

Implement, test, and execute the student-accepted Stage 4B out-of-sample design without changing any frozen modelling choice; generate the four canonical portfolio artifacts, canonical solver diagnostics, and the separately labelled ±25% extreme-return sensitivity comparison.

The student stated exactly:

> “I accept the Stage 4B pre-result OOS portfolio design, including the twelve funds, calendars, rolling windows, monthly timing, constraints, solver policy, weight drift, turnover, 5-bps transaction-cost convention, performance definitions, output schemas, anti-leakage tests, and prespecified interpretation rules. I authorise Workflow Stage 5A only: implement, test, and run the frozen portfolio design; create the canonical required portfolio outputs and separately labelled ±25% extreme-return sensitivity evidence. No sentiment scoring, finance lexicon, fusion, figures, fact-sheet design, Streamlit, report writing, deployment, publication, or Git operation is authorised.”

## Roles and provenance

- **Student:** accepted the pre-result specification, authorised this bounded implementation, and retains authority over review, interpretation, correction, and any later stage.
- **ChatGPT:** earlier assistance with the staged workflow and requirement interpretation is documented in the preceding governance records. No claim is made that ChatGPT executed the local code or independently approved the results.
- **Codex:** verified the local Project B boundary, read the controlling materials, implemented only the authorised portfolio layer, ran the local commands through the verified interpreter, generated and validated the five authorised CSVs, recorded genuine errors and corrections, and stopped before any sentiment or application work.

## Complete operational prompt

`````text
You are working on FINS5545 Project B.

By sending this prompt, the student states:

“I accept the Stage 4B pre-result OOS portfolio design, including the twelve funds, calendars, rolling windows, monthly timing, constraints, solver policy, weight drift, turnover, 5-bps transaction-cost convention, performance definitions, output schemas, anti-leakage tests, and prespecified interpretation rules. I authorise Workflow Stage 5A only: implement, test, and run the frozen portfolio design; create the canonical required portfolio outputs and separately labelled ±25% extreme-return sensitivity evidence. No sentiment scoring, finance lexicon, fusion, figures, fact-sheet design, Streamlit, report writing, deployment, publication, or Git operation is authorised.”

This is Workflow Stage 5A only: Frozen OOS Portfolio Implementation.

Do not change any frozen modelling choice because performance is poor, weights are surprising, or optimisation methods appear similar.

## 1. Workspace and interpreter guard

The opened PyCharm project root and terminal working directory must both resolve exactly to:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Use only this existing interpreter:

C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe

Do not inspect Project A, sibling folders, or the broader repository.

Do not create an environment or install dependencies.

If the workspace guard fails, stop without reading or editing project files.

## 2. Authorised file boundary

Existing files authorised for modification:

- `docs/data_contract.md`
- `docs/portfolio_backtest_design.md`
- `ai/05_portfolio_design_freeze.md`
- `src/portfolios.py`
- `scripts/run_part_b.py`

The only authorised change to `docs/data_contract.md` is correcting its header status to:

`Accepted and frozen by student — 2026-08-14`

Do not change any substantive data-contract rule.

In `docs/portfolio_backtest_design.md`, change only its review status to accepted. Do not rewrite the frozen methodology.

Append the Stage 4B acceptance to `ai/05_portfolio_design_freeze.md` without rewriting its earlier history.

New files authorised:

- `src/portfolio_validation.py`
- `scripts/validate_portfolios.py`
- `tests/test_portfolios.py`
- `tests/test_portfolio_outputs.py`
- `ai/06_portfolio_implementation.md`
- `results/data/fund_returns.csv`
- `results/data/fund_weights.csv`
- `results/tables/performance_metrics.csv`
- `results/tables/portfolio_solver_diagnostics.csv`
- `results/tables/extreme_sensitivity_metrics.csv`

Verify every new target is absent before implementation. If an unexpected target already exists, stop rather than overwrite it.

Do not modify or create anything else, including:

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `context/*`
- `src/data_access.py`
- `src/etl.py`
- `src/features.py`
- `src/validation.py`
- `src/sentiment.py`
- `src/fusion.py`
- existing tests
- requirements files
- Streamlit files
- report files
- figures
- `.idea/*`
- Git state

Do not create caches, bytecode, raw-data files, environments, placeholder outputs, or unlisted artifacts.

## 3. Required reading

Read completely:

- `AGENTS.md`
- the Part B Station 3, common-mistakes, required-exhibits, and rubric sections of `PROJECT_BRIEF.md`
- `context/DATA_GUIDE.md`
- `docs/data_contract.md`
- `docs/portfolio_backtest_design.md`
- `ai/05_portfolio_design_freeze.md`
- `src/etl.py`
- `src/features.py`
- `src/validation.py`
- current `src/portfolios.py`
- current `scripts/run_part_b.py`
- all existing tests
- `scripts/check_handin.py`

The accepted data contract and portfolio design control the implementation.

If those two documents conflict materially, stop and report the conflict rather than resolving it silently.

## 4. Pre-edit evidence

Before editing:

1. Capture a read-only SHA-256 manifest of all Project B files, including `.idea`, while excluding `.git`, environments, caches and bytecode.
2. Store any working manifest outside the project.
3. Confirm all authorised new paths are absent.
4. Run the existing test suite as a baseline using the explicit interpreter and `-B`.
5. Record commands, outputs and exit codes.

## 5. Close Stage 4B

Append a section to `ai/05_portfolio_design_freeze.md` titled:

`Final student acceptance — Stage 4B closed`

Record the student’s exact acceptance and end with:

`Stage 4B accepted and closed; Stage 5A authorised for frozen OOS portfolio implementation only.`

Do not rewrite earlier sections.

## 6. Exact fund universe

Implement exactly twelve funds with these IDs:

- `equity_equal_weight`
- `equity_minimum_variance`
- `equity_maximum_sharpe`
- `equity_risk_parity`
- `crypto_equal_weight`
- `crypto_minimum_variance`
- `crypto_maximum_sharpe`
- `crypto_risk_parity`
- `combined_equal_weight`
- `combined_minimum_variance`
- `combined_maximum_sharpe`
- `combined_risk_parity`

Families:

- Equity: frozen 50-equity universe;
- Crypto: frozen 10-crypto universe;
- Combined: frozen 50 equities followed by 10 cryptocurrencies.

Preserve deterministic asset order throughout.

## 7. OOS design to implement

Follow `docs/portfolio_backtest_design.md` exactly.

Critical invariants:

- Equity and Combined use the equity calendar and annualisation factor 252.
- Crypto uses its native seven-day calendar and annualisation factor 365.
- Combined crypto returns must already have been calculated on the native crypto calendar before equity-date selection.
- Rolling window:
  - 252 complete strictly prior observations for Equity and Combined;
  - 365 complete strictly prior observations for Crypto.
- Rebalance on the first observed eligible date of each calendar month.
- On decision date `t`, every estimation observation must have a date strictly earlier than `t`.
- Target weights formed at `t` apply to the realised asset return at `t`.
- Do not use expanding windows, pairwise covariance, filled returns, future information, or a backtest beginning on the first source date.
- Measure the exact first live date for each family during execution. Do not hard-code an assumed date.

Constraints:

- long-only;
- fully invested;
- no leverage;
- no short selling;
- `0 <= weight_i <= 0.20`;
- no forced equity/crypto minimum in Combined funds;
- no alteration of valid weights merely to make methods different.

Estimation:

- simple decimal returns;
- sample arithmetic mean;
- sample covariance;
- risk-free rate zero;
- correct family annualisation;
- covariance symmetrisation;
- only the smallest deterministic numerical covariance repair permitted by the frozen design.

Methods:

1. Equal Weight.
2. Minimum Variance.
3. Maximum Sharpe.
4. Risk Parity.

Use the exact deterministic SLSQP settings and starting points frozen in the design.

One frozen deterministic retry is permitted. Record it.

A persistent solver failure, non-finite objective, constraint failure, or invalid weight vector is a BLOCK. Do not silently substitute Equal Weight, previous weights, or invented weights.

## 8. Weight drift, turnover and costs

At each rebalance:

1. Use information through `t-1`.
2. Calculate the drifted pretrade weights.
3. Trade to target weights.
4. Apply target weights to date-`t` asset returns.
5. Update post-return holdings by:

`w_post,i = w_pre-return,i × (1 + r_i) / (1 + r_portfolio)`

Between rebalances, carry drifted holdings forward. Do not reset weights to target every day.

Turnover at later rebalances:

`turnover_t = 0.5 × Σ_i |target_weight_i - pretrade_weight_i|`

The initial portfolio formation is the documented exception:

- `pretrade_weight = 0`;
- `trade_weight = target_weight`;
- recorded turnover = 0;
- recorded transaction cost = 0.

For subsequent rebalances:

`transaction_cost_t = 0.0005 × turnover_t`

Gross return:

`gross_return_t = Σ_i w_pre-return,i × r_i,t`

Net return:

`net_return_t = (1 - transaction_cost_t) × (1 + gross_return_t) - 1`

The proportional transaction cost does not change relative post-return asset weights.

Primary performance metrics use net returns. Retain gross results as the transparent zero-cost comparator.

## 9. Performance metrics

Calculate for every fund over its complete live OOS period:

- net and gross cumulative return;
- annualised geometric return;
- annualised volatility with `ddof=1`;
- zero-risk-free-rate Sharpe ratio;
- maximum drawdown from compounded wealth;
- observation count;
- start and end dates;
- annualisation factor;
- rebalance count;
- average rebalance turnover;
- total turnover;
- transaction-cost drag;
- latest target holdings.

Use the exact formulas and column schemas frozen in `docs/portfolio_backtest_design.md`.

Do not describe backtested returns as guaranteed investor returns.

## 10. Solver diagnostics

Create `results/tables/portfolio_solver_diagnostics.csv` with one row per fund-rebalance and at least:

- `date`
- `fund_id`
- `family`
- `method`
- `solver_success`
- `attempts`
- `status_code`
- `message`
- `iterations`
- `objective_value`
- `sum_residual`
- `lower_bound_violation`
- `upper_bound_violation`
- `covariance_repair`

Equal Weight must use deterministic non-solver values.

A successful retry is allowed but must remain disclosed.

Define two target-weight vectors as near-identical when their maximum absolute difference is no greater than `1e-6`.

Near-identical methods produce a WARN and explanation, not a failure and not permission to perturb the weights.

## 11. Canonical output validation

Build all outputs in memory and validate them fully before writing final CSVs.

Validate at least:

- exactly twelve fund IDs;
- exact required columns and stable ordering;
- unique keys;
- correct family calendars;
- correct first live dates;
- no output before the full initial estimation window;
- every estimation date strictly earlier than its decision date;
- finite asset and fund returns;
- no fund return less than or equal to `-1`;
- finite weights and metrics;
- weight sums equal one within numerical tolerance;
- no negative weights;
- no weight above `0.20` within tolerance;
- correct rebalance schedule;
- correct daily weight drift;
- initial turnover and cost equal zero;
- later turnover appears only at rebalances;
- turnover uses drifted pretrade weights;
- exact gross/net cost reconciliation;
- parseable solver diagnostics;
- performance metrics independently reconcile to the return output;
- required output files contain substantive results rather than placeholders.

Only after every canonical BLOCK check passes may final CSVs be written.

## 12. Extreme-return sensitivity

Canonical required outputs must retain all 69 accepted extreme observations unchanged.

Create a separate robustness run that clips native asset returns to:

`[-0.25, +0.25]`

Apply clipping before both:

- estimation-window use;
- realised-return use.

For Combined funds, clip native returns before selecting crypto returns onto the equity calendar.

Keep every other parameter identical to the canonical design.

Do not overwrite or mix sensitivity results with canonical required outputs.

Before running the sensitivity, reproduce:

- 4 extreme equity observations;
- 65 extreme crypto observations.

Create `results/tables/extreme_sensitivity_metrics.csv` with:

- `fund_id`
- `family`
- `method`
- `canonical_net_annualised_return`
- `sensitivity_net_annualised_return`
- `delta_net_annualised_return`
- `canonical_net_sharpe_ratio`
- `sensitivity_net_sharpe_ratio`
- `delta_net_sharpe_ratio`
- `canonical_net_max_drawdown`
- `sensitivity_net_max_drawdown`
- `delta_net_max_drawdown`

Describe this only as a robustness scenario. It is not corrected data and cannot replace canonical results.

If the sensitivity cannot run under the frozen design, stop and report rather than weakening the specification.

## 13. Reusable validation layer

Create `src/portfolio_validation.py` with machine-readable PASS/WARN/BLOCK results.

Create `scripts/validate_portfolios.py` that:

- reads the precomputed portfolio outputs;
- validates schemas, keys, constraints, metrics and solver diagnostics;
- prints concise PASS/WARN/BLOCK counts;
- exits nonzero on BLOCK;
- optionally supports JSON;
- does not rerun optimisation.

## 14. Required tests

Create independent synthetic and real-data tests.

Test at least:

- twelve exact funds and deterministic IDs;
- 252/365 estimation-window membership;
- exact first-live-date rule;
- first eligible monthly rebalance dates;
- future-data perturbation leaving earlier target weights unchanged;
- correct family annualisation;
- deterministic asset ordering;
- long-only, 20% cap and full-investment constraints;
- deterministic solver results;
- independent controlled cases for Minimum Variance and Risk Parity;
- Maximum-Sharpe objective and feasibility on a controlled case;
- retry and persistent-failure BLOCK behaviour;
- manual daily weight-drift calculation;
- turnover from drifted pretrade weights rather than previous targets;
- initial-formation exception;
- exact 5-bps multiplicative cost arithmetic;
- independently calculated annualised return, volatility, Sharpe and drawdown;
- canonical output schemas and keys;
- real outputs reconciling to source asset returns;
- canonical retention of extremes;
- separate clipped sensitivity;
- deterministic representative reruns.

Tests must not merely repeat production helper functions.

Do not weaken tests to make unexpected output pass. Fix implementation bugs only within the frozen methodology.

## 15. Orchestration

Update `scripts/run_part_b.py` to support:

- `--stage portfolios`
- `--with-extreme-sensitivity`

The portfolio stage must:

1. run the accepted data-contract validation;
2. build the frozen return matrices;
3. run all canonical backtests;
4. validate all canonical outputs in memory;
5. optionally run the separate extreme-return sensitivity;
6. write only the authorised final outputs after successful validation.

Do not add sentiment, fusion, figure, app or report placeholders.

## 16. Required commands

Use the explicit interpreter and `-B`. Disable pytest cache.

First run source and existing tests:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_smoke.py tests/test_data_contract.py tests/test_data_foundation.py tests/test_portfolios.py
````

Run the data validator:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_data_contract.py
```

Generate canonical portfolios and the sensitivity:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/run_part_b.py --stage portfolios --with-extreme-sensitivity
```

Run the complete suite:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider
```

Run portfolio validation:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_portfolios.py
```

Run the hand-in checker:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

A sandbox or network failure is not automatically a data or model discrepancy. Retry only through the unchanged official loader pathway.

If the frozen design proves numerically infeasible or a solver persistently fails, stop and request student review.

Do not change the cap, window, cost, objective, rebalance rule, annualisation, sample or reported funds.

## 17. AI workflow log

Create `ai/06_portfolio_implementation.md` containing:

* date, objective and exact student authorisation;
* complete operational prompt;
* files read and changed;
* student, ChatGPT and Codex roles;
* implementation decisions;
* all commands and exit codes;
* test inventory and results;
* exact first live dates and OOS observation counts;
* all twelve performance rows, not a favourable subset;
* solver attempts, retries, failures and near-identical warnings;
* weight and constraint ranges;
* output row counts and SHA-256 hashes;
* all twelve sensitivity comparisons;
* genuine implementation errors and corrections;
* limitations;
* manifest evidence;
* status `Pending student review`.

Do not invent a correction, result or favourable interpretation.

## 18. Final boundary audit

Compare the complete post-edit manifest with the pre-edit manifest.

Confirm exactly the authorised files changed or appeared.

Report separately any:

* `.idea` change;
* cache or bytecode;
* raw data;
* environment artifact;
* placeholder;
* unexpected file;
* removed file.

## 19. Final response

Report:

* workspace guard;
* Stage 4B closure and metadata correction;
* implementation and test results;
* first live dates;
* output row counts;
* solver failures and retry counts;
* constraint ranges;
* a complete compact table of all twelve funds;
* complete extreme-sensitivity result;
* exact files modified and created;
* validator and checker results;
* limitations;
* final status:

`Stage 5A frozen OOS portfolios implemented and generated; pending student review. No sentiment or application work authorised.`

Stop after Stage 5A. Do not begin sentiment, finance-lexicon work, fusion, figures, Streamlit, report writing, deployment, publication, or Git operations.

```
```
`````

## Workspace, interpreter, and boundary guard

- Opened project root: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Terminal working directory: the same exact path
- Verified interpreter before each Python toolchain command: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`
- Interpreter version: Python 3.13.13; environment type: existing `venv`; package manager: pip
- Project root reparse points before work: `0`
- Every authorised new target was absent before implementation.
- Project A, sibling folders, the broader repository, Git state, environments, and dependencies were not inspected or modified.

The pre-edit manifest included `.idea`, excluded `.git`, environments, caches, bytecode, and compiled files, and recorded:

- file count: `48`;
- canonical SHA-256 digest: `5B672029C6B2418A20C1FE0CDE8D18E3301828A56DEAA37CB160288BED1A3954`;
- reparse-point count: `0`.

## Files read

- `AGENTS.md`
- the Part B Station 3, common-mistakes, required-exhibits, rubric, and AI-workflow sections of `PROJECT_BRIEF.md`
- `context/DATA_GUIDE.md`
- `docs/data_contract.md`
- `docs/portfolio_backtest_design.md`
- `ai/05_portfolio_design_freeze.md`
- `src/etl.py`
- `src/features.py`
- `src/validation.py`
- the pre-edit `src/portfolios.py`
- the pre-edit `scripts/run_part_b.py`
- `tests/test_smoke.py`
- `tests/test_data_contract.py`
- `tests/test_data_foundation.py`
- `scripts/check_handin.py`

No material conflict was found between the accepted input contract and portfolio design.

## Files changed

Existing files deliberately modified:

- `docs/data_contract.md`: corrected only the header status to `Accepted and frozen by student — 2026-08-14`; substantive contract unchanged.
- `docs/portfolio_backtest_design.md`: changed only the review-status statements to accepted; frozen methodology unchanged.
- `ai/05_portfolio_design_freeze.md`: appended the exact Stage 4B acceptance and closure chronologically.
- `src/portfolios.py`: replaced the starter stub with the frozen in-memory OOS engine.
- `scripts/run_part_b.py`: implemented only `--stage portfolios` and `--with-extreme-sensitivity` orchestration.

New files deliberately created:

- `src/portfolio_validation.py`
- `scripts/validate_portfolios.py`
- `tests/test_portfolios.py`
- `tests/test_portfolio_outputs.py`
- `ai/06_portfolio_implementation.md`
- `results/data/fund_returns.csv`
- `results/data/fund_weights.csv`
- `results/tables/performance_metrics.csv`
- `results/tables/portfolio_solver_diagnostics.csv`
- `results/tables/extreme_sensitivity_metrics.csv`

No other authored file was deliberately changed or created.

## Implementation decisions within the frozen design

- Family matrices preserve the contract order and complete-row rule. Native crypto returns are calculated by the accepted data foundation before equity-date selection; sensitivity clipping is applied to native matrices before Combined selection.
- The first monthly eligible date is found from the first row with the full number of strictly earlier complete observations; it is measured, not hard-coded.
- Annualised sample means and `ddof=1` covariances are estimated on fixed past-only windows. Covariance is symmetrised and subjected only to the accepted scale-relative eigenvalue repair.
- SLSQP uses `maxiter=2000`, `ftol=1e-12`, `disp=False`, equality/bound constraints, equal-weight primary seed, and the single accepted staggered retry. Analytic gradients were used for numerical efficiency without changing any objective.
- No optimiser output is clipped, renormalised, substituted, or perturbed. Invalid or persistently failed results raise a BLOCK.
- Daily holdings drift, inception exception, one-way turnover, 5-bps multiplicative cost, and gross/net returns are applied in the accepted order.
- Solver status is deterministic sorted-key JSON in every holdings row. The diagnostics table preserves final status, attempt count, iterations, objective, residuals, eigenvalue/ridge evidence, retry flag, and near-identical diagnostics.
- The in-memory validator independently reconstructs live calendars, first dates, target/pretrade holdings, drift, turnover, cost, gross/net returns, metrics, schemas, keys, order, constraints, and extreme retention before any CSV write.
- The file validator checks precomputed artifacts only and never reruns optimisation.
- Transaction-cost drag is available exactly as gross cumulative return minus net cumulative return. Latest target holdings for every fund are in `fund_weights.csv`, effective `2023-12-01`; neither requires an extra unapproved schema column.

## Commands, outputs, and exit codes

All Python commands used the explicit interpreter and `-B`; pytest cache was disabled. PyCharm environment verification preceded each Python toolchain invocation.

### Pre-edit baseline

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider
```

Exit code: `0`

```text
................                                                         [100%]
16 passed in 28.52s
EXIT_CODE=0
```

### Prescribed source and existing tests

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider tests/test_smoke.py tests/test_data_contract.py tests/test_data_foundation.py tests/test_portfolios.py
```

First implementation run: exit `0`, `26 passed in 29.19s`. After the validator correction described below: exit `0`, `26 passed in 28.28s`.

### Accepted input-contract validator

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_data_contract.py
```

Exit code: `0`

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

The loader emitted nine identical non-blocking Streamlit warnings that no runtime was present and the memory cache manager was used. No app was run or modified.

### Portfolio generation history and genuine correction cycle

Exact command each time:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/run_part_b.py --stage portfolios --with-extreme-sensitivity
```

1. The command wrapper was mistakenly given a five-second timeout. It terminated with exit `124` after about five seconds. No output target existed afterward. This was a Codex tooling error, not a data or model failure.
2. The unchanged command then reached `PASS=82/WARN=6/BLOCK=0` and the exact `4/65` extreme gate, but the new portfolio validator returned exit `1` with `RuntimeError: portfolio validation blocked all output writes: twelve_funds, twelve_funds`. No output target existed afterward.
3. Diagnosis found that the validator incorrectly required chronological return and weight rows to *first encounter* fund IDs in specification order. Since Crypto begins on 2021-01-01 and Equity/Combined begin on 2021-01-04, correct date-first output encounters Crypto first. The validator was corrected to require exact twelve-fund membership while retaining explicit metric-order, within-date fund-order, and asset-order checks. No modelling rule changed.
4. Successful generation returned exit `0`. A later deterministic rerun returned the same exit, row counts, metrics, and all five SHA-256 hashes. The final evidence-producing run returned:

```text
Data contract gate: PASS=82 WARN=6 BLOCK=0
Extreme-return gate: equity=4 crypto=65
Canonical portfolio validation: PASS=16 WARN=0 BLOCK=0
First live dates: {'Equity': '2021-01-04', 'Crypto': '2021-01-01', 'Combined': '2021-01-04'}
Output rows: returns=10404 weights=17280 metrics=12 diagnostics=432 sensitivity=12
Canonical solver retries=3; near-identical diagnostic rows=0
Sensitivity solver retries=1; near-identical diagnostic rows=0
Canonical solver attempt: date=2022-06-01 fund_id=combined_maximum_sharpe attempt=1 seed=equal_weight success=False valid=False status=8 iterations=22 message=Positive directional derivative for linesearch
Canonical solver attempt: date=2022-06-01 fund_id=combined_maximum_sharpe attempt=2 seed=staggered success=True valid=True status=0 iterations=22 message=Optimization terminated successfully
Canonical solver attempt: date=2022-07-01 fund_id=combined_maximum_sharpe attempt=1 seed=equal_weight success=False valid=False status=8 iterations=18 message=Positive directional derivative for linesearch
Canonical solver attempt: date=2022-07-01 fund_id=combined_maximum_sharpe attempt=2 seed=staggered success=True valid=True status=0 iterations=19 message=Optimization terminated successfully
Canonical solver attempt: date=2023-02-01 fund_id=combined_maximum_sharpe attempt=1 seed=equal_weight success=False valid=False status=8 iterations=18 message=Positive directional derivative for linesearch
Canonical solver attempt: date=2023-02-01 fund_id=combined_maximum_sharpe attempt=2 seed=staggered success=True valid=True status=0 iterations=14 message=Optimization terminated successfully
Sensitivity solver attempt: date=2022-07-01 fund_id=combined_maximum_sharpe attempt=1 seed=equal_weight success=False valid=False status=8 iterations=18 message=Positive directional derivative for linesearch
Sensitivity solver attempt: date=2022-07-01 fund_id=combined_maximum_sharpe attempt=2 seed=staggered success=True valid=True status=0 iterations=19 message=Optimization terminated successfully
PORTFOLIO STAGE STATUS: PASS
EXIT_CODE=0
```

The final run again emitted only the same nine non-blocking Streamlit no-runtime cache warnings. It had no persistent solver failure.

### Final complete test suite

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -m pytest -q -p no:cacheprovider
```

Final exit code: `0`

```text
..............................                                           [100%]
30 passed in 37.31s
EXIT_CODE=0
```

Earlier complete-suite checkpoints also passed `30/30` (37.03s and 37.44s) before the final orchestration-only diagnostic printing change.

### Final precomputed-output validator

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/validate_portfolios.py
```

Exit code: `0`

```text
Portfolio output validation: PASS=14 WARN=0 BLOCK=0
PORTFOLIO OUTPUT STATUS: PASS
EXIT_CODE=0
```

### Final hand-in checker

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exit code: `0`

```text
21 checks passed.
2 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
  [WARN] expected output results/data/sector_sentiment_index.csv not found - use this exact name so markers can find it
All checks passed - ready to zip and deploy.
EXIT_CODE=0
```

This is mechanical hand-in evidence only. The final sentence is not substantive project completion, deployment readiness, or authorisation for the two deferred deliverables.

## Test inventory and result

The final suite contains 30 passing tests: the 16 accepted smoke/data-foundation tests, 10 synthetic portfolio tests, and 4 real-output tests.

Synthetic tests independently cover:

- exact twelve IDs and 252/365 family configuration;
- complete strictly prior rolling windows, monthly eligibility, and first-live rule;
- diagonal-covariance Minimum-Variance and Risk-Parity controlled solutions;
- Maximum-Sharpe objective improvement and constraints;
- one permitted retry and persistent-failure BLOCK behaviour;
- manual daily drift;
- inception turnover/cost exception and drifted pretrade turnover;
- exact multiplicative 5-bps cost arithmetic;
- independent annualised return, volatility, Sharpe, and drawdown formulas;
- deterministic rerun equality and future-data perturbation leaving earlier targets unchanged.

Real-output tests independently cover:

- exact schemas, IDs, keys, row counts, ordering, and substantive values;
- all source dates and asset returns, live calendars, first dates, drifted pretrade weights, turnover, costs, and gross/net returns;
- family annualisation and constraints;
- canonical retention of 4 equity and 65 crypto extremes;
- all twelve separate sensitivity rows and exact delta arithmetic.

Tests do not create a sentiment score, figure, fact sheet, app, report, or unlisted output.

## OOS dates, observations, constraints, and solver evidence

| Family | First live date | End date | OOS observations per fund | Annualisation | Rebalances per fund |
|---|---|---|---:|---:|---:|
| Equity | 2021-01-04 | 2023-12-29 | 753 | 252 | 36 |
| Crypto | 2021-01-01 | 2023-12-31 | 1,095 | 365 | 36 |
| Combined | 2021-01-04 | 2023-12-29 | 753 | 252 | 36 |

Canonical diagnostics:

- rows: `432` (one per fund-rebalance);
- persistent failures: `0`;
- successful retries: `3`, all disclosed above and in the diagnostics/holdings JSON;
- near-identical diagnostic rows at `max(abs(delta weight)) <= 1e-6`: `0`;
- target-weight minimum: `0`;
- target-weight maximum: `0.2`;
- maximum independently grouped target sum residual: `6.38911146211285e-12`;
- maximum solver-recorded sum residual: `6.3895555513227e-12`;
- maximum lower-bound violation: `0`;
- maximum upper-bound violation: `0`;
- maximum covariance repair: `0` (no observed rebalance required the permitted ridge).

The sensitivity run had one successful retry, no persistent failure, and no near-identical warning. No valid output was altered to make methods appear different.

## All twelve canonical performance rows

These are complete mechanical backtest outputs, not favourable selections or guaranteed investor returns.

```csv
fund_id,family,method,start_date,end_date,observations,annualisation,transaction_cost_bps,net_cumulative_return,net_annualised_return,net_annualised_volatility,net_sharpe_ratio,net_max_drawdown,gross_cumulative_return,gross_annualised_return,gross_sharpe_ratio,average_rebalance_turnover,total_turnover,rebalance_count
equity_equal_weight,Equity,Equal Weight,2021-01-04,2023-12-29,753,252,5.0,0.4265366357098934,0.12624411374600264,0.16117558875630614,0.818319386731492,-0.2025658958348162,0.4272168148150324,0.1264237978181746,0.8192923665597748,0.027239281912380238,0.9533748669333083,36
equity_minimum_variance,Equity,Minimum Variance,2021-01-04,2023-12-29,753,252,5.0,0.1688804271944293,0.05361035177005613,0.1269034172830984,0.47496985425255855,-0.15287760834141817,0.17181881773798335,0.054496001892458734,0.48154524544417043,0.14346203365555896,5.021171177944564,36
equity_maximum_sharpe,Equity,Maximum Sharpe,2021-01-04,2023-12-29,753,252,5.0,0.1843833465021132,0.058266455013252116,0.17303307794185174,0.4139570796020574,-0.22621298737119766,0.190537746030907,0.06010360561440842,0.42391606416093347,0.29613552870184545,10.364743504564592,36
equity_risk_parity,Equity,Risk Parity,2021-01-04,2023-12-29,753,252,5.0,0.325541537413059,0.09890543523526096,0.14527909255249408,0.721895587561868,-0.18500469253793916,0.3262797215120601,0.09911020073711674,0.723160738729669,0.03181329060054001,1.1134651710189003,36
crypto_equal_weight,Crypto,Equal Weight,2021-01-01,2023-12-31,1095,365,5.0,1.77089803995964,0.4045596303068091,0.8188998503669441,0.8283762301618302,-0.8158019170666557,1.7737845161866876,0.4050471763369512,0.8288002835884539,0.05949408815909133,2.0822930855681965,36
crypto_minimum_variance,Crypto,Minimum Variance,2021-01-01,2023-12-31,1095,365,5.0,3.711114959635341,0.6763880923488717,0.7868187244200969,1.0517653233230835,-0.741993059969313,3.721719617709919,0.6776449922786332,1.0527170255003853,0.12847727644203583,4.496704675471254,36
crypto_maximum_sharpe,Crypto,Maximum Sharpe,2021-01-01,2023-12-31,1095,365,5.0,1.4432318531324246,0.3468572258260978,0.7827787007337121,0.7733096348810549,-0.771636648198086,1.4512884288603156,0.3483360255662251,0.7747127398272722,0.1881077497118544,6.5837712399149035,36
crypto_risk_parity,Crypto,Risk Parity,2021-01-01,2023-12-31,1095,365,5.0,2.000843277560129,0.44238469283630466,0.7989361743096439,0.8619498124584476,-0.7988540372959418,2.004219352287716,0.4429254045664892,0.8624190077583102,0.06425046857900893,2.2487664002653127,36
combined_equal_weight,Combined,Equal Weight,2021-01-04,2023-12-29,753,252,5.0,0.522661009703083,0.15109255049553982,0.2159991573116123,0.7597710030593728,-0.27887754909777174,0.523689200315351,0.15135261955180868,0.7608055516376532,0.03857279968817221,1.3500479890860275,36
combined_minimum_variance,Combined,Minimum Variance,2021-01-04,2023-12-29,753,252,5.0,0.16871726679791843,0.053561130770688914,0.12714886711760515,0.4739335678530553,-0.15440908788177665,0.17168698696203388,0.05445629891319359,0.48056857028626176,0.14500988240644055,5.0753458842254195,36
combined_maximum_sharpe,Combined,Maximum Sharpe,2021-01-04,2023-12-29,753,252,5.0,0.5785357854393349,0.16505947638917662,0.2333862933551624,0.7710019291654054,-0.22727623117321627,0.5869342221546403,0.16713024034334878,0.7785265403158709,0.30318979441144767,10.611642804400669,36
combined_risk_parity,Combined,Risk Parity,2021-01-04,2023-12-29,753,252,5.0,0.47698748262294455,0.1394200943917019,0.16201355498282338,0.8867935099990014,-0.19483899920910874,0.4779662399431168,0.13967272846916323,0.8881388134811272,0.03785398522477016,1.3248894828669555,36
```

Transaction-cost drag, derived from the two frozen cumulative-return columns, ranges from `0.0006801791` to `0.0106046581` across the twelve funds. It is not added as an unapproved CSV column.

## Complete ±25% extreme-return sensitivity result

This is a separate mechanical robustness scenario. It does not correct data and does not replace the canonical results.

```csv
fund_id,family,method,canonical_net_annualised_return,sensitivity_net_annualised_return,delta_net_annualised_return,canonical_net_sharpe_ratio,sensitivity_net_sharpe_ratio,delta_net_sharpe_ratio,canonical_net_max_drawdown,sensitivity_net_max_drawdown,delta_net_max_drawdown
equity_equal_weight,Equity,Equal Weight,0.12624411374600264,0.12624411374600264,0.0,0.818319386731492,0.818319386731492,0.0,-0.2025658958348162,-0.2025658958348162,0.0
equity_minimum_variance,Equity,Minimum Variance,0.05361035177005613,0.05361034830989486,-3.4601612686202543e-09,0.47496985425255855,0.4749698276966986,-2.6555859955479377e-08,-0.15287760834141817,-0.1528776083414184,-2.220446049250313e-16
equity_maximum_sharpe,Equity,Maximum Sharpe,0.058266455013252116,0.05826645393011454,-1.0831375796271914e-09,0.4139570796020574,0.41395707390504316,-5.697014249239629e-09,-0.22621298737119766,-0.22621298737119744,2.220446049250313e-16
equity_risk_parity,Equity,Risk Parity,0.09890543523526096,0.09910317873650554,0.00019774350124457385,0.721895587561868,0.7230654058711481,0.0011698183092800907,-0.18500469253793916,-0.18500469253793872,4.440892098500626e-16
crypto_equal_weight,Crypto,Equal Weight,0.4045596303068091,0.25123494214758657,-0.1533246881592225,0.8283762301618302,0.6822281112948088,-0.1461481188670214,-0.8158019170666557,-0.8064342079997491,0.009367709066906649
crypto_minimum_variance,Crypto,Minimum Variance,0.6763880923488717,0.4833749946303427,-0.19301309771852893,1.0517653233230835,0.9047434497267842,-0.14702187359629926,-0.741993059969313,-0.7395153227361033,0.0024777372332096537
crypto_maximum_sharpe,Crypto,Maximum Sharpe,0.3468572258260978,0.252918803381154,-0.09393842244494377,0.7733096348810549,0.6792177402109455,-0.09409189467010937,-0.771636648198086,-0.7678084952958881,0.0038281529021978455
crypto_risk_parity,Crypto,Risk Parity,0.44238469283630466,0.2775303076661446,-0.16485438517016004,0.8619498124584476,0.7072991977138846,-0.154650614744563,-0.7988540372959418,-0.7929277973666701,0.0059262399292717705
combined_equal_weight,Combined,Equal Weight,0.15109255049553982,0.13043830081591046,-0.020654249679629366,0.7597710030593728,0.6892297036442983,-0.07054129941507459,-0.27887754909777174,-0.2810496202379196,-0.0021720711401478354
combined_minimum_variance,Combined,Minimum Variance,0.053561130770688914,0.05595515224092629,0.002394021470237373,0.4739335678530553,0.49152820054957524,0.017594632696519952,-0.15440908788177665,-0.15440981271831755,-7.248365408996094e-07
combined_maximum_sharpe,Combined,Maximum Sharpe,0.16505947638917662,0.14493348694935304,-0.020125989439823577,0.7710019291654054,0.7143954469282232,-0.05660648223718223,-0.22727623117321627,-0.2268270573612361,0.0004491738119801747
combined_risk_parity,Combined,Risk Parity,0.1394200943917019,0.12908993566423654,-0.010330158727465344,0.8867935099990014,0.8356780070539441,-0.05111550294505729,-0.19483899920910874,-0.1962889149145699,-0.0014499157054611578
```

No result is interpreted here; student review is required.

## Output counts, sizes, and hashes

The deterministic rerun reproduced all five hashes exactly.

| Output | Rows | Bytes | SHA-256 |
|---|---:|---:|---|
| `results/data/fund_returns.csv` | 10,404 | 1,184,691 | `7C0DB5C36F7E6CF6F054580980FA5527C812C67F9C57F47039B3B518718B6C84` |
| `results/data/fund_weights.csv` | 17,280 | 12,718,806 | `F31A7B91A3B3CE7BE770C41597F2551913B93F6D3DDE4DCE27EC2B68E5DD53C8` |
| `results/tables/performance_metrics.csv` | 12 | 3,631 | `5719558A3D1D059137513BE0A4748BB3E1877D3956BDCFF92B095AB3B2BE2D19` |
| `results/tables/portfolio_solver_diagnostics.csv` | 432 | 75,094 | `ED837EC8E7BDF0E0356267ABA372D793B33621A102B40C1B3841981CB6F1B27C` |
| `results/tables/extreme_sensitivity_metrics.csv` | 12 | 2,963 | `40E91E876813EF6F493C9C165C0D594D6DA6901FEC8B46ECA4D05F55E5BCE151` |

## Genuine errors and corrections

1. A test helper was initially typed with invalid keyword-expression syntax (`else=9`) while creating `tests/test_portfolios.py`. It was noticed during local inspection and corrected to `else 9` before the first test invocation. No test was weakened.
2. Codex mistakenly invoked the first portfolio command with a five-second wrapper timeout. Exit `124` was recorded, and absence of all result targets was rechecked before retrying unchanged.
3. The first completed optimisation correctly blocked all writes because of the overly strict fund-first-encounter validator described above. The validation logic—not the frozen methodology, outputs, or data—was corrected. The prescribed source suite then passed, the portfolio run passed its in-memory gate, and the complete suite reconciled the written outputs.

There was no invented correction, hidden solver fallback, constraint relaxation, parameter change, sample change, or result-driven specification change.

## Manifest and artifact boundary evidence

Immediately before creating this self-referential AI log, the matching manifest contained 57 files, had canonical digest `33FD625EF31851EF7A161CB8EFB7D514206DDFAF5653FFC0FCE645DD9CBC00E9`, and differed from the 48-file pre-edit manifest exactly as follows:

- modified: `ai/05_portfolio_design_freeze.md`, `docs/data_contract.md`, `docs/portfolio_backtest_design.md`, `scripts/run_part_b.py`, `src/portfolios.py`;
- added: the five authorised CSVs, `scripts/validate_portfolios.py`, `src/portfolio_validation.py`, `tests/test_portfolios.py`, and `tests/test_portfolio_outputs.py`;
- removed: none;
- `.idea` changes: none.

This file is the tenth authorised addition. Its own final hash and the final 58-file manifest digest cannot be embedded without changing that hash; the complete post-write comparison is performed after this edit and reported to the student without another project mutation.

A separate final search found:

- cache or bytecode entries: `0`;
- unlisted result files: `0`;
- raw-data files created: `0`;
- environment artifacts created: `0`;
- placeholders created: `0`.

## Limitations and deferred matters

- These are historical OOS backtests under the frozen specification, not guaranteed investor returns and not yet student-approved interpretations.
- The separately clipped scenario is robustness evidence only. It does not externally or economically validate the 69 source movements and cannot replace canonical results.
- `fund_weights.csv` is comparatively large because the accepted schema requires the complete sorted-key solver diagnostic JSON to be repeated across each fund-rebalance's asset rows. No alternative compressed schema was substituted in this stage.
- The source loader emits benign Streamlit cache warnings when called outside an app runtime; these did not change data or results.
- The two remaining checker reminders are expected. `report/report.pdf` and `results/data/sector_sentiment_index.csv` were not created because report and sentiment work are unauthorised.
- Figures, fact sheets, empirical interpretation, sentiment, finance lexicon, fusion, Streamlit, report writing, deployment, publication, and Git operations remain unauthorised.

## Student-review status and next action

**Pending student review.** The student must review the implementation, tests, complete twelve-fund evidence, solver retries, sensitivity comparison, and file boundary. Any acceptance, correction, interpretation, or later-stage action requires a new explicit student instruction. Nothing continues automatically.

## Final student acceptance — Stage 5A closed

On 2026-08-14, the student stated exactly:

> I have reviewed the complete Stage 5A evidence rather than only the best-performing funds. I accept the twelve-fund OOS implementation, first-live dates, tests, output reconciliation, constraint checks, deterministic results, and separate extreme-return sensitivity analysis.
>
> I specifically acknowledge the three canonical and one sensitivity SLSQP retries. They followed the single prespecified deterministic retry rule, succeeded without relaxing constraints or substituting weights, and remain transparently disclosed.
>
> I accept the corrections to the five-second command timeout and the overly strict output-order validator because neither correction changed the frozen portfolio methodology, data, parameters, or results.
>
> I will retain and report weak or inconvenient evidence, including the underperformance of some optimised equity funds, the very large crypto drawdowns, and the material sensitivity of crypto performance to extreme observations. I do not authorise changing windows, constraints, methods, costs, samples, or reported funds to improve performance.
>
> I therefore accept and close Stage 5A. I authorise Workflow Stage 6A only: freeze the pre-result sentiment and fusion methodology and generate a student-reviewable finance-lexicon candidate table using only the 2020 calibration news corpus. No proposed lexicon term is approved in advance, and no full sentiment or fusion result is authorised.

This acceptance closes the complete Stage 5A record, including the disclosed retries, corrections, weak results, and sensitivity evidence. It authorises documentation and 2020-only lexicon-candidate review in Stage 6A; it does not approve any lexicon entry, sentiment or fusion implementation, result, figure, application, report, deployment, publication, or Git action.

**Stage 5A accepted and closed; Stage 6A authorised for pre-result sentiment-design and finance-lexicon candidate review only.**
