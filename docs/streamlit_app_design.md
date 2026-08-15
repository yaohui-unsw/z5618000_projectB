# MAIA Streamlit App Design

**Status:** Implemented locally; pending student visual and interaction review

## 1. Stage authority

Stage 8 implements and validates the local Streamlit product only. The student
accepted and closed Stage 7, approved the name **MAIA — Multi-Asset Investment
Assistant**, and approved a separately disclosed **0.50% p.a. illustrative
management fee** in Allocation Studio. No model, parameter, lexicon, canonical
CSV, canonical report figure, report, Git state, publication, or deployment is
authorised to change.

The app is intentionally downstream-only. It reads precomputed `results/`
artifacts and performs display transformations and user-allocation arithmetic;
it does not call the protected loader or any portfolio, sentiment, or fusion
engine.

## 2. Target user

MAIA serves a financially curious retail investor who understands basic return
and risk concepts but neither reads Python code nor constructs portfolios
directly. The user compares and allocates across MAIA funds. They do not select
individual securities, open an account, fund a bank connection, place an order,
or receive personalised advice.

Value proposition:

> Compare twelve systematic Equity, Crypto and Combined funds using transparent
> out-of-sample evidence and news-sentiment analytics.

## 3. Customer journey

1. **Explore Funds:** orient to all 12 base funds and compare historical risk,
   return, and growth.
2. **Fund Fact Sheet:** inspect one fund's canonical metrics, historical path,
   latest frozen target holdings, operating rules, turnover, and costs.
3. **Allocation Studio:** choose two to four funds, assign a one-time capital
   allocation, and inspect a historical before/after-fee account illustration.
4. **Sentiment & Innovation:** understand the sector tone, reviewed lexicon,
   complete 24-overlay evidence, and the selectivity/turnover trade-off.
5. **Methodology & Disclosures:** inspect the frozen rules, limitations, solver
   evidence, and separately labelled extreme-return sensitivity.

The default Explore Funds page contains useful evidence before any control is
changed.

## 4. Teacher requirement-to-feature mapping

| Requirement | MAIA feature | Evidence source |
|---|---|---|
| Portfolio-management interface | Fund explorer, fact sheet, allocation journey | Frozen base return/weight/metric CSVs |
| Multiple products/methods | 12 funds: 3 families × 4 methods | `performance_metrics.csv` |
| Growth of $1 | Selectable net paths and fund fact sheet | `fund_returns.csv` |
| Drawdown | Fact-sheet historical drawdown | `fund_returns.csv` |
| Current holdings | Latest target rebalance and complete holdings table | `fund_weights.csv` |
| User allocation | Two-to-four-fund one-time sleeve simulation | Canonical fund `net_return` only |
| Sentiment analytics | Finance-VADER market tone and sector selection | `sector_sentiment_index.csv` |
| Innovation evidence | 23-term lexicon, diagnostics, all 24 fusion comparisons | Lexicon, diagnostics, fusion CSVs |
| Transparent methodology | Plain-English rules and bounded implementation evidence | Solver and sensitivity tables |
| Deployable architecture | Root entrypoint, relative paths, precomputed artifacts | `streamlit_app.py`, `src/app_data.py` |

## 5. Information hierarchy and visual system

The hierarchy is inspired by professional fund-provider sites: product identity,
clear evidence summary, progressively deeper fact-sheet detail, and disclosures
near the relevant decision. It does not copy BlackRock/iShares branding, logos,
wording, or layouts.

- Dark navy establishes headings and primary text.
- Teal marks analytical/evidence-aware content.
- Orange identifies Finance-VADER and selected emphasis; blue identifies Plain
  VADER.
- White/light-grey surfaces, restrained rules, local sans-serif typography, and
  generous spacing preserve contrast and readability.
- Charts state units, sample meaning, and net/fee status. Zero or $1 references
  are used where economically relevant; negative outcomes are retained.
- Conditional rendering avoids loading large artifacts before they are needed.

## 6. Navigation and page specification

### Explore Funds

Shows the full 12-row table regardless of chart filters, all-family/method risk-
return evidence, up-to-four-fund growth comparison, method descriptions, and a
visible historical disclaimer. No fund is labelled best, recommended, or
personally optimal.

### Fund Fact Sheet

Shows exact canonical KPI cards, growth and drawdown derived from `net_return`,
the latest `target_weight` holdings and date, all holdings in a bounded table,
Combined sleeve exposure, and frozen operating terms.

### Allocation Studio

Uses two to four base funds, five-percentage-point controls, a default of the
four Combined funds chosen without performance ranking, an equal-split action,
and an exact 100% gate. Invalid allocations are never silently normalised.

### Sentiment & Innovation

Shows Finance-VADER market tone and selected sector series with a 21-trading-day
display mean; the full 23-term operational lexicon; canonical diagnostic ratios;
and all 24 base/overlay comparisons, including negative results. It states that
term exposure is not contextual accuracy and that no significance test was
prespecified.

### Methodology & Disclosures

Summarises the frozen windows, calendars, constraints, timing, costs, lag,
lexicon, lambda, no-news semantics, extreme-observation policy, and limitations.
Solver and sensitivity evidence is placed in a bounded expander.

## 7. Canonical source-to-widget lineage

| Artifact | App use | Permitted transformation |
|---|---|---|
| `fund_returns.csv` | Growth, drawdown, Allocation Studio | Compounding canonical `net_return`; calendar reconciliation |
| `fund_weights.csv` | Latest holdings/exposure | Latest-date filtering and summation |
| `performance_metrics.csv` | 12-fund table and fact-sheet KPIs | Formatting only |
| `portfolio_solver_diagnostics.csv` | Implementation evidence | Bounded display filtering |
| `extreme_sensitivity_metrics.csv` | Robustness evidence | Bounded display only |
| `sector_sentiment_index.csv` | Market/sector tone | Cross-sector mean and 21-day visual rolling mean |
| `sentiment_diagnostics.csv` | Coverage and diagnostic KPIs | Exact-key retrieval and sector display |
| `finance_lexicon.csv` | 23 approved terms | Sorting/column selection only |
| `fusion_performance_metrics.csv` | Overlay levels | Complete one-to-one merge for display |
| `fusion_comparison.csv` | 24 deltas and claims | Complete counts, extrema, charts, table |

The remaining canonical sentiment/fusion daily and weight artifacts are covered
by the loader contract but are not loaded by the default app pages because no
widget requires their row-level detail.

## 8. Allocation formula and calendar rule

For selected fund `j` with initial allocation `a_j` and canonical net returns
`r_j,t`, its one-time sleeve is:

`sleeve_j,t = initial_capital × a_j × cumulative_product(1 + r_j,t)`.

Sleeves drift with performance; the user allocation is not rebalanced. The
canonical fund net return already includes the 5-bps turnover cost, so that cost
is not applied again.

- All-Crypto selections use the common native seven-day Crypto calendar and
  annualisation 365.
- Any Equity/Combined selection uses the common Equity/Combined display calendar
  and annualisation 252.
- A selected Crypto fund's native daily returns between two consecutive shared
  display dates are geometrically compounded, preserving weekend performance.
- The common period begins at the latest selected first-live date and ends at
  the earliest selected last date.

## 9. Management-fee rule

The separately approved illustration uses:

`after_fee_wealth = before_fee_wealth × (1 − 0.005) ** (elapsed_calendar_days / 365)`.

Both wealth paths and dollar fee drag are shown. The 0.50% p.a. management fee is
a product illustration, not a frozen portfolio-model output and not an estimate
of a live product charge.

## 10. Accessibility and responsive design

- Theme colours meet readable light-background contrast; meaning is not conveyed
  by colour alone where labels or line styles can reinforce it.
- Tables remain scrollable and bounded; charts use explicit labels and units.
- The layout uses Streamlit columns sparingly and stacks naturally at narrower
  desktop widths.
- No remote font, image, JavaScript, or web service is used.
- Error messages name the missing/invalid artifact and never fabricate a value.

## 11. Disclosures

- Historical out-of-sample illustration only; no forecast, recommendation, or
  guarantee.
- No live prices, orders, account, or personalised advice.
- No-news is missing information, not scored-neutral news; Crypto has no news
  input.
- Reliability measures coverage/agreement, not truth or news quality.
- Reviewed-term exposure is not contextual accuracy; Utilities/Energy exposure
  concentrations are limitations.
- The 69 extremes remain canonical; the ±25% run is separate sensitivity
  evidence.
- No prespecified statistical significance test was conducted.

The required negative disclaimer contains the word “recommendation”; automated
wording guards therefore prohibit affirmative advice phrases rather than
removing this mandatory disclosure.

## 12. Test plan

- Artifact tests cover relative paths, all schemas, date parsing, row/key/order
  contracts, exact fund/overlay/lexicon universes, defensive copies, and named
  missing-file errors.
- Pure-logic tests independently verify growth, drawdown, holdings, exact
  allocation validation, one-time drift, mixed-calendar weekend compounding,
  all-Crypto calendars, the management-fee formula, metrics, rolling display
  summaries, and complete fusion evidence.
- Streamlit tests cover startup, default usefulness, all navigation sections,
  controls, invalid-total rejection, lexicon/fusion visibility, disclosures, and
  static guards against runtime model imports or result writes.
- A local headless server and rendered browser paths are checked separately; no
  model command is part of app validation.
- Pre/post hashes protect all 13 canonical CSVs and eight canonical report PNGs.

## 13. Deferred work

Report writing, Git initialisation/commit/push, GitHub publication, Streamlit
Community Cloud deployment, Moodle packaging, and submission remain explicitly
deferred to later student-authorised stages.

**Implemented locally; pending student visual and interaction review.**
