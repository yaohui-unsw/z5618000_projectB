# Project B out-of-sample portfolio and backtest design

**Status:** **Accepted and frozen by student — 2026-08-14**  
**Date:** 2026-08-14 (Australia/Sydney)  
**Scope:** Prespecified portfolio design only; no implementation, optimisation, output, or empirical result

## 1. Authority, purpose, and investment product

`PROJECT_BRIEF.md`, the official `context/` files, the accepted input contract in `docs/data_contract.md`, and the Project B operating contract control this proposal. Its purpose is to select every material portfolio and backtest choice before performance is observed. Acceptance would freeze the canonical specification; it would not constitute implementation evidence or an empirical conclusion.

The product will offer twelve investable funds: three asset families crossed with four methods. Every family-method pair is a separate fund and will receive its own fact sheet later.

| `fund_id` | Fund name | Family | Frozen assets | Method |
|---|---|---|---|---|
| `equity_equal_weight` | Equity - Equal Weight | Equity | Frozen 50 equities | Equal Weight |
| `equity_minimum_variance` | Equity - Minimum Variance | Equity | Frozen 50 equities | Minimum Variance |
| `equity_maximum_sharpe` | Equity - Maximum Sharpe | Equity | Frozen 50 equities | Maximum Sharpe |
| `equity_risk_parity` | Equity - Risk Parity | Equity | Frozen 50 equities | Risk Parity |
| `crypto_equal_weight` | Crypto - Equal Weight | Crypto | Frozen 10 cryptocurrencies | Equal Weight |
| `crypto_minimum_variance` | Crypto - Minimum Variance | Crypto | Frozen 10 cryptocurrencies | Minimum Variance |
| `crypto_maximum_sharpe` | Crypto - Maximum Sharpe | Crypto | Frozen 10 cryptocurrencies | Maximum Sharpe |
| `crypto_risk_parity` | Crypto - Risk Parity | Crypto | Frozen 10 cryptocurrencies | Risk Parity |
| `combined_equal_weight` | Combined - Equal Weight | Combined | 50 equities followed by 10 cryptocurrencies | Equal Weight |
| `combined_minimum_variance` | Combined - Minimum Variance | Combined | 50 equities followed by 10 cryptocurrencies | Minimum Variance |
| `combined_maximum_sharpe` | Combined - Maximum Sharpe | Combined | 50 equities followed by 10 cryptocurrencies | Maximum Sharpe |
| `combined_risk_parity` | Combined - Risk Parity | Combined | 50 equities followed by 10 cryptocurrencies | Risk Parity |

Fund IDs, family values, method values, names, and asset order are deterministic. The breadth satisfies the high-band portfolio requirement without adding a shallow fifth optimiser. The separately governed sentiment, finance-lexicon, and fusion path remains the planned innovation; this portfolio breadth is not itself claimed as an empirical innovation result.

## 2. Out-of-sample calendars, windows, and timing

| Family | Return calendar | Annualisation | Rolling estimation window |
|---|---|---:|---:|
| Equity | Native observed equity trading dates | 252 | 252 complete strictly prior return observations |
| Crypto | Native seven-day crypto dates | 365 | 365 complete strictly prior return observations |
| Combined | Observed equity trading dates; crypto returns calculated on their native calendar before selection | 252 | 252 complete strictly prior return observations across all 60 assets |

Rules:

1. A complete window contains no missing return for any asset in that fund. Pairwise deletion, filling, backfilling, and expanding windows are prohibited.
2. Determine eligible dates using the required complete past window, then select the first observed eligible date in each calendar month. This is the monthly rebalance schedule.
3. The first live date is the first selected monthly rebalance date with the full window. Exact first live dates are implementation measurements, not claims in this document.
4. On decision date `t`, the estimation sample contains only returns with date `< t`. Target weights formed at `t` apply to the realised asset returns dated `t`.
5. The backtest does not begin on the first source date. Future observations may not affect windows, weights, solver choices, fallbacks, or parameters.
6. Equal Weight begins on the same family live date and follows the same monthly rebalance schedule as the optimised funds, preserving like-for-like OOS comparisons even though its weights do not require estimated moments.

A one-year rolling window is long enough to provide repeated observations while remaining responsive to changing market conditions. Fixed 252/365 factors respect the family calendars. Monthly rebalancing limits needless turnover while meeting the brief's monthly-or-less-frequent rule.

## 3. Portfolio constraints

Every target portfolio must satisfy:

- `0 <= weight_i <= 0.20` for every asset;
- `sum(weight_i) = 1`;
- long-only, fully invested, no leverage, and no short selling;
- no forced minimum equity or crypto allocation in Combined funds.

The cap is a product-level concentration guardrail. It is feasible because `N × 0.20` equals 10 for Equity, 2 for Crypto, and 12 for Combined, all above the required total weight of one; equal weights are also strictly within the cap for all families. A valid Combined solution with zero or near-zero cryptocurrency weight must be retained and interpreted. Valid outputs may never be perturbed merely to make methods look different.

For validation, target weights must be finite, each bound residual and the absolute sum-to-one residual must be at most `1e-8`, and asset order must exactly match the frozen family order. Breaching those tolerances is a BLOCK.

## 4. Estimation, numerical policy, and optimisation

All methods use simple decimal returns from the frozen data foundation. For each authorised past-only window:

- estimate the arithmetic sample mean and sample covariance (`ddof=1`);
- annualise both using the family's fixed factor `A` (`mu_annual = A × mu_daily`, `Sigma_annual = A × Sigma_daily`);
- use risk-free rate `r_f = 0`;
- preserve deterministic asset order and reject non-finite inputs;
- prohibit pairwise covariance estimation and economically meaningful shrinkage unless later approved as a separately retained robustness specification.

Numerical covariance handling is prespecified. First symmetrise `Sigma` as `(Sigma + Sigma.T) / 2`. Define `scale = max(trace(Sigma) / N, 1e-12)` and `epsilon = 1e-10 × scale`. If the smallest eigenvalue is below `epsilon`, add exactly `(epsilon - lambda_min)I`; otherwise add nothing. Record the smallest eigenvalue and ridge magnitude. This is a deterministic numerical repair only, not tunable economic shrinkage.

The proposed optimiser is SciPy SLSQP with `maxiter=2000`, `ftol=1e-12`, and `disp=False`. Primary initial weights are equal weights. One retry only is authorised after an unsuccessful primary attempt, using the same inputs, objective, constraints, covariance, and solver settings but a deterministic feasible staggered seed. For zero-based asset index `i`, its raw seed is

`v_i = 1 + 0.01 × (2i - (N - 1)) / (N - 1)`,

normalised so weights sum to one. For all three frozen universe sizes it is positive and below the cap. A persistent failure, non-finite objective, unsuccessful solver flag, or material constraint violation is a BLOCK. No silent fallback or substituted weights are allowed.

Every attempt must record solver name, attempt number, status code, success flag, iterations, message, objective, maximum constraint residual, initial-value identifier, and covariance-repair evidence. `solver_status` in the holdings output will be a deterministic sorted-key JSON string containing this diagnostic summary; Equal Weight records `solver="none"` and status `deterministic_equal_weight`.

The methods are frozen as follows.

### Equal Weight

At every rebalance, `w_i = 1/N`. It is the transparent benchmark and uses no optimiser.

### Minimum Variance

Minimise

`w' Sigma w`

subject to the frozen bounds and full-investment constraint.

### Maximum Sharpe

Maximise

`(w' mu - r_f) / sqrt(w' Sigma w)`, where `r_f = 0`,

subject to the frozen constraints. Implementation may minimise its negative but may not replace the objective with an in-sample return-maximisation shortcut. Non-positive or non-finite portfolio variance is a BLOCK.

### Risk Parity

Let portfolio variance be `V = w' Sigma w`, component variance contribution be `RC_i = w_i(Sigma w)_i`, and normalised contribution be `NRC_i = RC_i / V`. Minimise

`sum_i (NRC_i - 1/N)^2`

subject to the frozen constraints. Non-positive or non-finite `V` is a BLOCK.

At a common rebalance date, two methods are flagged as near-identical when their maximum absolute weight difference is at most `1e-6`. This is a diagnostic, not a failure and never permission to alter weights. The diagnostic must assess data, binding constraints, numerical convergence, and legitimate mathematical equivalence.

## 5. Weight timing and drift

At each rebalance date `t`:

1. Use only information dated through `t-1`.
2. Observe pre-trade weights produced by prior holding drift.
3. Trade from those pre-trade weights to the new target.
4. Apply the target weights to date-`t` asset returns.
5. After returns, update each holding using the post-trade, pre-return weight:

   `w_post,i = w_pre-return,i × (1 + r_i) / (1 + r_portfolio)`

6. Carry post-return weights into the next date. On non-rebalance dates, apply the carried weights to that date's returns and update them with the same formula.

Here `w_pre-return` equals the new target immediately after a rebalance trade and equals the carried drifted weights otherwise. A non-finite denominator or total portfolio return `<= -1` is a BLOCK. Between rebalances, weights must drift; daily resetting to targets is prohibited.

The current holdings shown later in a fact sheet are the target weights from that fund's most recent rebalance, labelled with their effective date. They are not silently replaced with post-return drifted weights.

## 6. Turnover and transaction costs

For rebalance dates after initial formation, one-way turnover is

`turnover_t = 0.5 × sum_i |target_weight_i - pretrade_weight_i|`.

The initial live portfolio has `pretrade_weight = 0` and `trade_weight = target_weight` for auditability, but its formation turnover and cost are defined as zero, excluded from turnover/cost statistics, and disclosed. On all other rows, signed `trade_weight = target_weight - pretrade_weight`. Fund-level turnover is repeated across that rebalance's asset rows; it is zero on non-rebalance fund-return rows.

Transaction cost is fixed before results at 5 basis points per unit of turnover:

`cost_t = 0.0005 × turnover_t`.

Retain gross and net returns. Apply cost multiplicatively before the rebalance-date investment return:

`net_return_t = (1 - cost_t) × (1 + gross_return_t) - 1`.

On non-rebalance dates and initial formation, cost is zero and gross equals net. Net returns are primary for fact sheets and comparisons; gross returns are a transparent zero-cost comparator. The 5-bps assumption may not be tuned after performance is seen. Any further scenario requires dated student approval and must retain this canonical result.

## 7. Performance definitions

For each fund's live OOS dates, using family annualisation factor `A` and observation count `n`:

- wealth/growth index: `W_t = product_(s<=t)(1 + r_s)`, beginning from 1;
- cumulative return: `product_t(1 + r_t) - 1`;
- annualised geometric return: `(product_t(1 + r_t))^(A/n) - 1`;
- annualised volatility: `std(r_t, ddof=1) × sqrt(A)`;
- Sharpe ratio: `mean(r_t) / std(r_t, ddof=1) × sqrt(A)`, with `r_f = 0`;
- drawdown: `W_t / running_max(W_t) - 1`; maximum drawdown is its minimum;
- rebalance count: number of live dates with `is_rebalance = true`, including initial formation;
- average and total turnover: respectively the mean and sum across cost-bearing rebalances, excluding initial formation;
- transaction-cost drag: gross cumulative return minus net cumulative return over identical live dates;
- current holdings: latest target-weight vector and its effective date.

Primary metrics use net returns. Gross comparison fields are clearly prefixed. Zero standard deviation, non-positive compounded wealth, insufficient observations, or any non-finite metric must be handled explicitly and never converted into a favourable number. Backtested outcomes must never be presented as guaranteed investor returns.

## 8. Frozen portfolio output schemas

These files are not created in Stage 4B.

### `results/data/fund_returns.csv`

Long format, unique key `date + fund_id`, one row per live OOS fund-date, ordered by date then the twelve-fund order in Section 1:

1. `date`
2. `fund_id`
3. `family`
4. `method`
5. `gross_return`
6. `turnover`
7. `transaction_cost`
8. `net_return`
9. `is_rebalance`

### `results/data/fund_weights.csv`

Unique key `date + fund_id + ticker`, one row per fund-rebalance-asset, ordered by date, fund order, then frozen asset order:

1. `date`
2. `fund_id`
3. `family`
4. `method`
5. `ticker`
6. `pretrade_weight`
7. `target_weight`
8. `trade_weight`
9. `turnover`
10. `solver_success`
11. `solver_status`

`solver_status` carries the deterministic diagnostic JSON defined in Section 4. At initial formation, the explicit turnover exception in Section 6 applies.

### `results/tables/performance_metrics.csv`

Unique key `fund_id`, ordered by the twelve-fund order in Section 1:

1. `fund_id`
2. `family`
3. `method`
4. `start_date`
5. `end_date`
6. `observations`
7. `annualisation`
8. `transaction_cost_bps`
9. `net_cumulative_return`
10. `net_annualised_return`
11. `net_annualised_volatility`
12. `net_sharpe_ratio`
13. `net_max_drawdown`
14. `gross_cumulative_return`
15. `gross_annualised_return`
16. `gross_sharpe_ratio`
17. `average_rebalance_turnover`
18. `total_turnover`
19. `rebalance_count`

Transaction-cost drag is derivable from the frozen gross and net cumulative fields; no extra required column is introduced. Current holdings are obtained from each fund's latest rows in `fund_weights.csv`. Every categorical value must match Section 1 exactly, all returns/weights/costs are decimal rather than percentage values, and no placeholder or fabricated row is allowed.

## 9. Required implementation and anti-leakage tests

A later authorised implementation must include at least:

1. exactly twelve family-method funds with the correct frozen memberships;
2. correct 252/365 calendars, windows, and annualisation;
3. exact rolling-window membership and a first live date only after the full initial window;
4. every decision date using only return dates `< t`;
5. perturbing any future return leaving all earlier target weights unchanged;
6. monthly first-observed-eligible rebalance selection;
7. finite non-negative weights, the 20% cap, sum of one, and exact asset order;
8. deterministic reruns, starts, solver configuration, numerical repair, and outputs;
9. independent manual objective and constraint checks for Minimum Variance, Maximum Sharpe, and Risk Parity;
10. complete solver-attempt/retry diagnostics and BLOCK behaviour;
11. near-identical-method diagnostics without output perturbation;
12. manual daily weight-drift examples across rebalance and non-rebalance dates;
13. turnover from drifted pre-trade weights rather than prior targets;
14. independent gross/net multiplicative cost arithmetic and the 5-bps convention;
15. initial formation excluded from turnover and cost statistics;
16. performance metrics checked against small, independently calculated synthetic examples;
17. output columns, dtypes, keys, row counts, categories, order, and absence of placeholders.

Where practical, tests must use independent formulas or small hand-calculated cases rather than merely calling production helpers twice.

## 10. Prespecified interpretation and robustness rules

- Poor, negative, or statistically unremarkable OOS performance remains reportable.
- Maximum Sharpe is expected to be estimation-sensitive; weak results must not be hidden.
- Near-zero Combined cryptocurrency weights may be economically valid.
- High cryptocurrency volatility may produce small Risk-Parity crypto weights.
- Windows, cap, risk-free rate, rebalance frequency, cost, optimiser, sample, and reported fund set may not be changed to improve observed results.
- Any later change requires a dated, student-approved robustness rationale and must retain the original frozen specification and canonical outputs.
- All 69 verified extreme observations remain unchanged in canonical estimation and realised returns. A later, separately labelled sensitivity may clip returns to `[-0.25, 0.25]` in both estimation and realised-return inputs, but it cannot replace canonical results and requires explicit implementation authorisation.
- Negative robustness or later innovation findings must be reported honestly.

## 11. Feasibility, risks, and deferred matters

### Feasibility review

- The accepted input contract supplies 1,006 equity/combined dates and 1,461 native crypto dates. After legitimate first-return missingness, each family has more observations than its one-year rolling window; exact first live dates remain unmeasured here.
- Equal weights satisfy all bounds. Aggregate cap capacity proves a fully invested solution exists in every family.
- Annualising moments before optimisation, normalising Risk-Parity contributions, explicit covariance repair, fixed SLSQP settings, two prespecified feasible starts, and strict residual checks address the official solver-scaling warning without result-driven tuning.
- The three long output schemas have deterministic keys and orders, retain gross/net and holdings evidence, and can support the required later fact sheets and performance exhibits. They intentionally contain no sentiment or fusion fields.

### Risks addressed

The design directly controls look-ahead, incomplete and pairwise windows, calendar/annualisation mismatch, silent solver fallback, covariance scaling, daily target resets, turnover measured from stale targets, hidden costs, artificial method differentiation, extreme-value deletion, and post-result specification searching.

### Deferred matters

The following remain unauthorised and unresolved until a later approved stage:

- all portfolio code, solver execution, and output creation;
- exact first live dates, weights, turnover, metrics, performance, and conclusions;
- implementation of the extreme-observation sensitivity;
- figures, fund fact sheets, and required exhibits;
- sentiment scoring, finance lexicon, fusion, and their tests;
- Streamlit, report writing, deployment, publication, and Git operations.

**Accepted and frozen by student — 2026-08-14.**
