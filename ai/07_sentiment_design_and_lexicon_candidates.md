# Stage 6A — Sentiment design and finance-lexicon candidates

**Date:** 2026-08-14  
**Status:** Pending student review

## Objective and authorisation

Freeze a pre-result sentiment/fusion proposal and produce a student-reviewable finance-lexicon candidate set from the 2020 calibration corpus only, without approving a term or generating full sentiment/fusion results.

The student's exact authorisation is preserved both in the complete prompt below and in the Stage 5A closure. In summary, the student accepted the complete Stage 5A evidence, including weak results, three canonical and one sensitivity deterministic retry, and two non-methodological corrections; closed Stage 5A; and authorised only Stage 6A documentation plus a 2020-only candidate review.

## Roles and provenance

- **Student:** approved the stage boundary, accepted Stage 5A, supplied the exact methodology proposal, and retains final authority over every candidate and all later implementation.
- **ChatGPT:** assisted the student with workflow and prompt review. It did not perform this local extraction and cannot approve candidates.
- **Codex:** verified the local workspace/environment, read the authorised Project B materials, checked VADER, performed the in-memory 2020-only candidate analysis, proposed terms/values with warnings, and created the authorised documentation.

No AI system claims that the student approved a candidate. Every `student_decision` remains `PENDING` and every `student_final_value` remains blank.

## Files read

Read completely:

- `AGENTS.md`
- `PROJECT_BRIEF.md`
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `context/verify_ai_output.md`
- `docs/data_contract.md`
- `docs/portfolio_backtest_design.md`
- `ai/06_portfolio_implementation.md`
- `src/sentiment.py`
- `src/fusion.py`
- `src/etl.py`
- `src/features.py`
- `scripts/check_handin.py`

The portfolio CSV outputs were not read, and portfolio performance was not used in term selection or polarity proposals.

## Workspace, interpreter, and pre-edit boundary

The opened project root and terminal working directory both resolved to:

`C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`

The root was not a reparse point. All three new targets were absent. The pre-edit SHA-256 manifest covered Project B files, including `.idea`, while excluding `.git`, environments, caches, and bytecode:

- file count: `58`;
- manifest digest: `AB028388A33A1D910F361A9B49DCD7E7292ECD649D5A787E4C5A41180F9009EC`;
- reparse points found: `0`.

PyCharm's configured environment for `src/etl.py` was independently queried before every Python command:

- executable: `C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe`;
- version: Python 3.13.13;
- environment type: `venv`;
- package manager: `pip`.

The workspace-guard interpreter line in the supplied prompt omitted the separator before `.venv` (`fins-agent.venv`). The later required checker command, the previously verified environment decision, and PyCharm all identify `fins-agent\.venv`. Codex used that verified explicit interpreter and did not create or configure an environment.

## VADER resource evidence

Command (exit `0`):

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B -c "import nltk; from nltk.sentiment import SentimentIntensityAnalyzer; SentimentIntensityAnalyzer(); p=nltk.data.find('sentiment/vader_lexicon.zip'); print('VADER_STATUS=AVAILABLE'); print('VADER_RESOURCE=' + str(p)); print('NLTK_PATHS=' + '|'.join(nltk.data.path))"
```

Observed output:

```text
VADER_STATUS=AVAILABLE
VADER_RESOURCE=C:\Users\24116\Documents\GitHub\fins-agent\.venv\nltk_data\sentiment\vader_lexicon.zip
NLTK_PATHS=C:\Users\24116/nltk_data|C:\Users\24116\Documents\GitHub\fins-agent\.venv\nltk_data|C:\Users\24116\Documents\GitHub\fins-agent\.venv\share\nltk_data|C:\Users\24116\Documents\GitHub\fins-agent\.venv\lib\nltk_data|C:\Users\24116\AppData\Roaming\nltk_data|C:\nltk_data|D:\nltk_data|E:\nltk_data
```

`VADER_STATUS=AVAILABLE`; no download occurred. A Project B scan found `PROJECT_NLTK_ENTRIES=0`, confirming that no NLTK resource was written inside the project.

## Calibration corpus and deterministic candidate procedure

Data was loaded only through protected `src/data_access.py`, then cleaned with accepted `clean_news_headlines`. All operations remained in memory. The inclusive filter was `source_date_utc` from `2020-01-01` through `2020-12-31`.

Measured evidence:

```text
RAW_NEWS_ROWS=149683
CLEAN_NEWS_ROWS=146836
CALIBRATION_ROWS=36955
CALIBRATION_START=2020-01-01
CALIBRATION_END=2020-12-31
CALIBRATION_TICKERS=50
CALIBRATION_SECTORS=10
CALIBRATION_SOURCE_ORDER_MIN=0
CALIBRATION_SOURCE_ORDER_MAX=144503
QUALIFIED_TOKEN_COUNT=1755
```

Procedure:

1. Match title text with `(?<![A-Za-z0-9])[A-Za-z]+(?:['-][A-Za-z]+)*(?![A-Za-z0-9])`.
2. Lowercase only the match key; preserve the exact title.
3. Count token occurrences, distinct matching headline rows, tickers, and raw sectors.
4. Require at least 25 occurrences, 20 headlines, and 5 tickers.
5. Exclude entities, publishers, people, URLs, numeric/date tokens, stopwords, neutral topic words, and unstable generic meanings.
6. Permit `addition` only when absent from vanilla VADER, or `reviewed_override` when finance usage clearly changes sign/meaning or the vanilla magnitude is materially understated.
7. Propose conservative 0.5-increment values in `[-3,+3]` without returns or outcomes.
8. Sort candidates by occurrence count descending, then term ascending.
9. Sort matching examples by UTC timestamp and source row; retain the earliest and lower-median `(n-1)//2` rows. A fixed five-position review supplied ambiguity checks.

## Proposed candidates

All 27 are pending:

| Term | Class | Occurrences | Headlines | Tickers | Vanilla | Proposed | Conflict/risk summary |
|---|---|---:|---:|---:|---:|---:|---|
| shares | reviewed_override | 1,922 | 1,893 | 48 | 1.2 | 0.0 | Neutral equity noun. |
| energy | reviewed_override | 1,617 | 1,558 | 46 | 1.1 | 0.0 | Neutral sector/theme noun. |
| alert | reviewed_override | 399 | 399 | 50 | 1.2 | 0.0 | Mostly publication/flow/options label. |
| rally | addition | 315 | 314 | 42 | NA | 1.0 | Questions and broad-market attribution can conflict. |
| active | reviewed_override | 307 | 307 | 29 | 1.7 | 0.0 | Trading-volume descriptor. |
| beat | addition | 295 | 295 | 45 | NA | 1.5 | Mixed clauses can offset a beat. |
| inflow | addition | 243 | 243 | 42 | NA | 1.0 | ETF flow may not be issuer-specific. |
| rebound | addition | 235 | 232 | 44 | NA | 1.0 | May be prospective or concern another asset. |
| downgrades | addition | 212 | 212 | 35 | NA | -1.5 | Mixed digest headlines exist. |
| asset | reviewed_override | 207 | 206 | 35 | 1.5 | 0.0 | Neutral noun/name component. |
| outflows | addition | 207 | 207 | 44 | NA | -1.0 | ETF flow attribution risk. |
| outflow | addition | 205 | 205 | 45 | NA | -1.0 | ETF flow attribution risk. |
| inflows | addition | 197 | 197 | 44 | NA | 1.0 | ETF flow attribution risk. |
| beats | addition | 146 | 145 | 42 | NA | 1.5 | Mandatory examples contain offsetting negatives. |
| outperform | addition | 134 | 134 | 37 | NA | 1.5 | Maintained rating can coexist with target cut. |
| miss | reviewed_override | 128 | 128 | 45 | -0.6 | -1.5 | “Miss out” is a conflicting ordinary use. |
| overweight | reviewed_override | 111 | 111 | 29 | -1.5 | 1.0 | Finance sign reverses vanilla; downgrade-from context conflicts. |
| bullish | addition | 101 | 101 | 41 | NA | 1.5 | Questions/negation/mixed forecasts can conflict. |
| slump | addition | 58 | 58 | 24 | NA | -1.5 | Can be framed as a buying opportunity. |
| misses | reviewed_override | 46 | 46 | 32 | -0.9 | -1.5 | Mixed “but” clauses can offset it. |
| plunge | addition | 45 | 45 | 21 | NA | -1.5 | Object/ticker attribution and mixed clauses. |
| downgraded | addition | 41 | 41 | 20 | NA | -1.5 | Analyst-action attribution risk. |
| tumble | addition | 32 | 32 | 16 | NA | -1.5 | Often broad-market rather than issuer-specific. |
| underweight | addition | 31 | 31 | 10 | NA | -1.0 | Rating context; ordinary meaning differs. |
| plunges | addition | 30 | 29 | 13 | NA | -1.5 | Broad index/commodity attribution risk. |
| underperform | addition | 28 | 28 | 16 | NA | -1.5 | Comparison may concern another issuer. |
| layoffs | addition | 27 | 27 | 11 | NA | -1.5 | Cost-saving interpretation can conflict. |

Complete sector lists, exact examples, rationales, and misuse risks are in `docs/finance_lexicon_review.md`.

## Recorded rejected candidates

The recorded rejected set is: `buy`, `earnings`, `dividend`, `target`, `lower`, `growth`, `raises`, `sell`, `profit`, `hold`, `cuts`, `upgrades`, `surge`, `guidance`, `upgrade`, `lawsuit`, `plunged`, `bankruptcy`, `bearish`, `fraud`, and `downgrade`.

Reasons include unstable direction, neutral topic meaning, an adequate vanilla value, entity/issuer-attribution risk, mixed analyst/product meanings, or failure of a fixed threshold. The 25-occurrence threshold was not lowered for `bankruptcy`, `bearish`, `fraud`, or `downgrade`. Rejections and exact measured counts are preserved in the review document and must not be silently reversed.

## Commands, outputs, and genuine errors

All Python invocations used the verified interpreter with `-B`. The official loader emitted seven benign Streamlit cache warnings per standalone process; no cache or bytecode was written in Project B.

1. VADER instantiation/resource lookup: exit `0`; resource already available; no download.
2. Initial in-memory 2020 profile: exit `0`; produced the corpus evidence above.
3. Targeted token-statistics command, first attempt: exit `1`. The unchanged official loader could not reach its two official bundle URLs inside the restricted sandbox; the terminal showed `WinError 10013`. This was a network/sandbox access failure, not a data discrepancy.
4. Exact same targeted command outside the network restriction, still through unchanged `src/data_access.py`: exit `0`.
5. Deterministic five-position context audit: exit `0`.
6. Final 27-candidate earliest/lower-median reconciliation: exit `0`.

No URL, loader, package, threshold, date range, or candidate value was changed to obtain a successful run. No temporary script or data extract was created in Project B. This sandbox retry and the prompt's missing interpreter-path separator are the genuine tool/input corrections in this cycle; no other error is invented.

## Method-design record

`docs/sentiment_innovation_design.md` freezes, pending review:

- plain VADER, student-approved finance VADER, and evidence-aware finance;
- separate-headline scoring and no-news missingness;
- exact-zero versus neutral-band diagnostics;
- equal-weight ticker-day and news-bearing-ticker sector aggregation;
- `covered_headline_share`, directional agreement, volume evidence, and bounded reliability;
- past-only 252-date/60-observation standardisation with current date excluded;
- ticker `evidence_aware_signal = finance_z × reliability` and separate raw compound;
- one-observed-trading-day lag with no carry-forward;
- 24 monthly Equity/Combined overlays, fixed `lambda=0.10`, no Crypto-only fusion;
- capped-simplex projection, Combined crypto/equity-sleeve preservation, and failure as `BLOCK`;
- unchanged Stage 5A drift, turnover, costs, and performance definitions;
- complete comparisons, future output schemas, and anti-leakage tests.

The required sector file's supplied exact column list omits the separately required sector custom-term hit-share diagnostic. The proposal keeps the required sector schema exact and places that diagnostic in `sentiment_diagnostics.csv`; this is explicitly pending student confirmation.

## Hand-in checker

Command (exit `0`):

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Exact output:

```text
21 checks passed.
2 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
  [WARN] expected output results/data/sector_sentiment_index.csv not found - use this exact name so markers can find it
All checks passed - ready to zip and deploy.
```

Checker success is mechanical evidence only and is not sentiment/fusion completion.

## Post-edit manifest and boundary evidence

The first post-documentation comparison, immediately before inserting this evidence into the log, found:

- pre-edit files: `58`; post-edit files: `61`;
- pre-edit manifest digest: `AB028388A33A1D910F361A9B49DCD7E7292ECD649D5A787E4C5A41180F9009EC`;
- provisional post-edit digest: `7DB4E4D76FF95840F82D6392723AD22607D8F88477D2CC5A9DCB0B699B573247`;
- modified: `ai/06_portfolio_implementation.md` only;
- added: `ai/07_sentiment_design_and_lexicon_candidates.md`, `docs/finance_lexicon_review.md`, and `docs/sentiment_innovation_design.md` only;
- removed: none;
- `.idea` changes: none;
- `results/` changes or additions: none;
- project code changes: none;
- cache/bytecode artifacts: none;
- reparse points: none.

The AI log is self-referential: its own final hash and the final aggregate manifest digest cannot be embedded without changing them. The final post-write digest and exact comparison are therefore reported in the Codex handoff after the last project mutation.

## Limitations and unresolved student decisions

- Every candidate value is an AI proposal based on text usage, not empirical effectiveness.
- Two displayed examples and the fixed context sample cannot prove universal meaning; VADER remains bag-of-lexicon-rules rather than contextual language understanding.
- The corpus can contain syndicated/repeated headlines and imperfect ticker attribution.
- The student must decide all 27 terms and confirm the proposed sector custom-hit-share schema resolution.
- VADER resource availability is resolved, but no full-corpus sentiment, sector, fusion, or investment result was generated.
- Implementation, tests, output generation, figures, app, report, deployment, publication, and Git operations require a later explicit authorisation.

## Complete operational prompt

~~~~text
You are working on FINS5545 Project B.

By sending this prompt, the student states:

“I have reviewed the complete Stage 5A evidence rather than only the best-performing funds. I accept the twelve-fund OOS implementation, first-live dates, tests, output reconciliation, constraint checks, deterministic results, and separate extreme-return sensitivity analysis.

I specifically acknowledge the three canonical and one sensitivity SLSQP retries. They followed the single prespecified deterministic retry rule, succeeded without relaxing constraints or substituting weights, and remain transparently disclosed.

I accept the corrections to the five-second command timeout and the overly strict output-order validator because neither correction changed the frozen portfolio methodology, data, parameters, or results.

I will retain and report weak or inconvenient evidence, including the underperformance of some optimised equity funds, the very large crypto drawdowns, and the material sensitivity of crypto performance to extreme observations. I do not authorise changing windows, constraints, methods, costs, samples, or reported funds to improve performance.

I therefore accept and close Stage 5A. I authorise Workflow Stage 6A only: freeze the pre-result sentiment and fusion methodology and generate a student-reviewable finance-lexicon candidate table using only the 2020 calibration news corpus. No proposed lexicon term is approved in advance, and no full sentiment or fusion result is authorised.”

This is Workflow Stage 6A only: Pre-result Sentiment Innovation Design and Finance-Lexicon Candidate Review.

This stage must preserve genuine student control. Codex may propose finance terms and polarity values, but it must not approve them on the student’s behalf.

## 1. Workspace guard

The opened PyCharm root and terminal working directory must both resolve exactly to:

C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB

Use only:

C:\Users\24116\Documents\GitHub\fins-agent.venv\Scripts\python.exe

Do not inspect Project A, sibling folders, the broader repository, or another student’s work.

Stop before reading or editing Project B files if either workspace guard fails.

## 2. Authorised file boundary

Append only:

* `ai/06_portfolio_implementation.md`

Create only:

* `docs/sentiment_innovation_design.md`
* `docs/finance_lexicon_review.md`
* `ai/07_sentiment_design_and_lexicon_candidates.md`

Verify all three new targets are absent before editing.

Do not modify or create anything else, including:

* `AGENTS.md`
* official context or brief files
* `src/*`
* `scripts/*`
* `tests/*`
* `results/*`
* `report/*`
* requirements files
* Streamlit files
* `.idea/*`
* Git state

No portfolio output may be changed or regenerated.

Temporary candidate-analysis code may exist only outside Project B and must be deleted afterward. It may not save raw news, a cleaned-news extract, headline-level sentiment output, candidate token dumps, caches or bytecode inside Project B.

## 3. Required reading

Read completely:

* `AGENTS.md`
* `PROJECT_BRIEF.md`, paying particular attention to sentiment, fusion, innovation, AI-workflow, application and rubric requirements
* `context/DATA_GUIDE.md`
* `context/project_context.md`
* `context/verify_ai_output.md`
* `docs/data_contract.md`
* `docs/portfolio_backtest_design.md`
* `ai/06_portfolio_implementation.md`
* current `src/sentiment.py`
* current `src/fusion.py`
* relevant news functions in `src/etl.py` and `src/features.py`
* `scripts/check_handin.py`

The Stage 5A log must be read for governance and closure evidence. Do not read the portfolio CSV outputs or use portfolio performance when selecting lexicon candidates or proposing polarity values.

The lexicon proposal must remain independent of investment outcomes.

## 4. Close Stage 5A

Append a chronological section to `ai/06_portfolio_implementation.md` titled:

`Final student acceptance — Stage 5A closed`

Record the exact student acceptance above and end with:

`Stage 5A accepted and closed; Stage 6A authorised for pre-result sentiment-design and finance-lexicon candidate review only.`

Do not rewrite, delete or reorder any earlier history.

## 5. VADER resource check

Using the explicit interpreter and `-B`, verify that:

```python
from nltk.sentiment import SentimentIntensityAnalyzer
SentimentIntensityAnalyzer()
```

works.

If and only if the `vader_lexicon` resource is missing, the student authorises downloading exactly that one NLTK resource to the existing default user-level NLTK data location outside Project B.

Do not install, uninstall or upgrade a Python package. Do not download any other NLTK resource.

Record:

* whether the resource was already available;
* whether a download occurred;
* the resolved resource path;
* confirmation that no NLTK resource was written inside Project B.

Do not score the full news corpus in Stage 6A.

## 6. Calibration corpus and candidate generation

Use only cleaned news with inclusive UTC source dates from:

`2020-01-01` through `2020-12-31`

This is the lexicon calibration corpus.

Do not use:

* 2021–2023 news;
* asset returns;
* fund performance;
* portfolio weights;
* fusion outcomes;
* future-period candidate frequencies

when selecting candidates or assigning proposed polarity values.

Load data only through the protected Project B data pathway and use the accepted news-cleaning function. Keep candidate-analysis operations in memory.

For candidate discovery:

* use title text only;
* preserve the exact cleaned title casing, punctuation and text for audit examples;
* use deterministic lowercase token matching for candidate counts;
* consider only token-shaped unigrams compatible with a VADER lexicon update;
* require at least 25 occurrences;
* require appearance in at least 20 distinct headlines;
* require appearance across at least 5 tickers;
* exclude tickers, company names, publisher names, URLs, numbers, dates, names of people, generic stopwords and clearly ambiguous non-finance terms;
* do not use future-period frequency or any association with returns;
* propose no more than 30 terms;
* do not silently lower any threshold if fewer than 30 terms qualify.

Two candidate classes are permitted:

1. `addition`: absent from the vanilla VADER lexicon;
2. `reviewed_override`: already present, but the proposed finance meaning is clearly different in sign or materially understated.

Overrides require stronger written evidence than additions.

Proposed values must:

* lie in `[-3.0, +3.0]`;
* use increments of `0.5`;
* be conservative;
* reflect headline-level financial meaning;
* not reflect whether the term was followed by positive or negative asset returns.

Do not approve any candidate.

## 7. Create `docs/finance_lexicon_review.md`

Mark the document:

`AI-proposed finance lexicon candidates — pending student decision`

For every candidate include:

* `term`
* `candidate_class`
* `2020_occurrences`
* `distinct_headlines`
* `distinct_tickers`
* `sector_coverage`, defined as the number of distinct raw sectors
* the corresponding deterministic raw-sector list
* `vanilla_vader_value`, using `NA` when absent
* `proposed_finance_value`
* `direction`
* concise finance-context rationale
* two deterministically selected 2020 audit examples
* ambiguity or misuse risk
* whether any reviewed occurrence conflicts with the proposed polarity
* `student_decision`, initially `PENDING`
* `student_final_value`, initially blank

Select the two audit examples as:

1. the earliest qualifying occurrence; and
2. the median qualifying occurrence

after sorting by UTC source date and preserved source-row identifier.

This selection rule prevents supportive examples from being cherry-picked. Preserve the source-row identifiers and exact cleaned titles.

Sort the candidate table deterministically by:

1. descending `2020_occurrences`; then
2. ascending `term`.

Also include a rejected-candidate table containing relevant high-frequency terms considered and excluded, together with the exclusion reason. This must demonstrate judgement rather than automatic inclusion.

State explicitly:

* AI proposed the candidates and proposed scores;
* frequency does not establish sentiment polarity;
* two examples do not prove a universally stable meaning;
* the student must accept, reject or edit every entry;
* no candidate is operational until student approval;
* no investment result was used;
* rejected candidates must not be silently restored during implementation.

## 8. Freeze sentiment methodology

Create `docs/sentiment_innovation_design.md` and mark it:

`Proposed pre-result sentiment and fusion design — pending student review`

Freeze the following proposal.

### Models

1. `plain_vader`: unchanged NLTK VADER.

2. `finance_vader`: plain VADER plus only student-approved finance-lexicon entries and student-approved final values.

3. `evidence_aware_finance`: use finance-VADER, then apply evidence reliability after past-only standardisation for the tradable signal. Retain `finance_score × reliability` as a raw diagnostic measure only; do not use it as a separately tuned trading signal.

Preserve headline casing, punctuation and exact text.

Do not:

* strip stopwords before VADER scoring;
* stem or lemmatise;
* concatenate unrelated headlines;
* overwrite the source title;
* convert no-news observations into neutral scores.

Score every headline separately.

Report both:

* the exact-zero compound-score rate;
* the standard VADER neutral-band rate where `abs(compound) < 0.05`.

These are different diagnostics and must not be conflated.

### Ticker-day aggregation

For a ticker-day with news:

* `plain_score` = equal-weight mean of the separate headline plain-VADER compound scores;
* `finance_score` = equal-weight mean of the separate headline finance-VADER compound scores;
* preserve `headline_count`.

For a ticker-day without news:

* sentiment remains missing;
* it is not converted to zero;
* it is not carried forward.

A genuine compound score of zero on a news-bearing day remains scored-neutral news and must remain distinct from no news.

### Evidence reliability

For each news-bearing ticker-day define:

* `n` = headline count;

* `covered_headline_share` = the fraction of headlines containing at least one token with a non-zero valence in the active finance-VADER lexicon;

* token matching for this diagnostic must be deterministic and documented;

* `m` = number of non-neutral headlines under the finance model, using `abs(compound) >= 0.05`;

* if `m > 0`:

  `directional_agreement = abs(sum(sign(compound_j))) / m`

  where the sum includes only the `m` non-neutral finance-model headlines;

* otherwise:

  `directional_agreement = 0`;

* `volume_evidence = n / (n + 1)`;

* `reliability = covered_headline_share × directional_agreement × volume_evidence`.

Reliability must be finite and remain in `[0,1]`.

For diagnostics, separately report:

`custom_finance_term_hit_share`

defined as the fraction of headlines containing at least one student-approved custom finance-lexicon term.

Do not substitute `custom_finance_term_hit_share` for `covered_headline_share` in the frozen reliability formula.

The raw diagnostic evidence-aware ticker compound is:

`evidence_aware_compound = finance_score × reliability`

Document the following limitations:

* directional agreement is not truth;
* article count is not information quality;
* repeated or syndicated reporting may inflate apparent evidence;
* lexicon coverage does not prove contextual accuracy;
* reliability scaling may suppress valid low-volume information.

### Sector index

Build the future sector index by equal-weighting news-bearing ticker-day observations within each sector.

Do not treat no-news tickers as zero and do not include them in that day’s score denominator.

Record:

* headline count;
* number of tickers with news;
* ticker coverage;
* plain compound;
* finance compound;
* mean reliability;
* raw evidence-aware compound;
* custom finance-term hit share.

Define sector ticker coverage as:

`number of sector tickers with news / total number of eligible tickers in that sector`

Use the accepted raw-sector and display-sector mapping.

### Past-only standardisation

For ticker `i` on aligned equity trading date `d`, calculate `plain_z` from `plain_score` and `finance_z` from `finance_score`.

For each calculation:

* estimate the mean and sample standard deviation from non-missing observations in the previous 252 observed equity trading dates only;
* exclude date `d`;
* require at least 60 prior non-missing observations;
* require a finite sample standard deviation greater than `1e-8`;
* calculate the z-score against those past-only parameters;
* clip only the resulting signal z-score to `[-3,+3]`;
* leave the z-score missing when the history or standard-deviation requirement fails;
* do not clip source headline scores or canonical asset returns.

Define the ticker-level tradable evidence-aware signal on aligned date `d` as:

`evidence_aware_signal = finance_z × reliability`

Do not separately standardise `finance_score × reliability` for portfolio formation. This prevents creation of an unintended second evidence-aware trading model.

For sector diagnostics only, apply the same past-only rule separately within each sector to:

* `plain_compound`, producing sector `plain_z`;
* `finance_compound`, producing sector `finance_z`;
* `evidence_aware_compound`, producing sector `evidence_aware_z`.

Sector z-scores are diagnostic outputs and must not be substituted for ticker-level portfolio signals.

### Trading lag

A ticker score aligned to date `d` becomes tradable only on the next observed equity trading date.

At decision date `t`, no signal may use a headline aligned on `t` or later.

The lagged evidence-aware signal must use both:

* the finance z-score calculated for the prior observed trading date; and
* reliability from that same prior observed trading date.

If the previous observed trading day has no usable score, apply no sentiment tilt:

* preserve the missing state;
* use multiplier one operationally;
* do not carry older sentiment forward.

The future implementation must test ordinary trading days, weekends and exchange holidays.

### Fusion variants

Apply all three variants to every Equity and Combined base fund across all four portfolio methods:

* `plain_vader_naive`
* `finance_vader_naive`
* `evidence_aware_finance`

This gives:

`8 equity-bearing base funds × 3 variants = 24 overlay strategies`

Do not fuse sentiment into Crypto-only funds.

Use the same monthly rebalance dates as the accepted base funds. Do not introduce daily sentiment trading.

Signals:

* Plain variant: lagged ticker-level `plain_z`.
* Finance variant: lagged ticker-level `finance_z`.
* Evidence-aware variant: lagged ticker-level `finance_z × reliability`.

Freeze the tilt strength before observing results:

`lambda = 0.10`

For asset `i`, calculate the raw tilted value:

`u_i = base_target_weight_i × exp(lambda × signal_i)`

A missing signal uses multiplier one.

Do not tune lambda, clipping, coverage, minimum history, reliability or lag rules after observing performance.

### Equity-fund projection

For an Equity fund:

1. calculate all raw tilted equity values `u_i`;
2. normalise them to a total of one;
3. apply the same deterministic Euclidean capped-simplex projection used by the accepted portfolio implementation.

The projection must solve:

`minimise sum_i (w_i - u_i)^2`

subject to:

* `0 <= w_i <= 0.20`
* `sum_i w_i = 1`

### Combined-fund projection

For a Combined fund:

* keep every crypto target weight numerically unchanged;
* preserve the original total crypto weight;
* preserve the original total equity-sleeve weight;
* apply multipliers only to equity assets.

Let the frozen base equity-sleeve total be `E`.

Then:

1. calculate the raw tilted equity values;
2. normalise the equity values to sum to `E`;
3. apply the same deterministic Euclidean capped-simplex projection subject to:

   * `0 <= w_i <= 0.20`
   * `sum_i w_i = E`

Every crypto target weight must remain numerically unchanged.

If either projection is infeasible or fails validation:

* return `BLOCK`;
* do not relax the cap;
* do not alter crypto weights;
* do not silently substitute equal weights or base weights;
* do not create portfolio results from the failed rebalance.

Use the same:

* weight-drift mechanics;
* inception convention;
* turnover calculation;
* 5-bps transaction cost;
* net-return calculation;
* performance definitions

as Stage 5A.

### Comparisons

For all 24 overlays, compare against the corresponding frozen base fund using:

* net annualised return;
* annualised volatility;
* Sharpe ratio;
* maximum drawdown;
* cumulative return;
* average turnover;
* total turnover;
* transaction-cost drag.

Also compare:

* exact-zero rate;
* neutral-band rate;
* active finance-lexicon coverage;
* custom finance-term hit share;
* plain-to-finance score changes;
* sector and ticker coverage;
* reliability distribution;
* frequency of multiplier one due to missing signals;
* frequency and magnitude of active tilts.

Negative, weak or insignificant results remain reportable.

Do not select only favourable funds, portfolio methods, dates, sectors or sentiment variants.

## 9. Freeze future output schemas

Document, but do not create, the following future outputs.

For every output, specify:

* purpose;
* row grain;
* primary key;
* exact column order;
* dtypes;
* missing-value meaning;
* sort order;
* validation requirements.

### Required `results/data/sector_sentiment_index.csv`

Required columns:

* `date`
* `sector`
* `sector_display`
* `headline_count`
* `ticker_count_with_news`
* `ticker_coverage`
* `plain_compound`
* `finance_compound`
* `mean_reliability`
* `evidence_aware_compound`
* `plain_z`
* `finance_z`
* `evidence_aware_z`

### Additional future outputs

* `results/data/ticker_sentiment_daily.csv`
* `results/data/fusion_returns.csv`
* `results/data/fusion_weights.csv`
* `results/tables/sentiment_diagnostics.csv`
* `results/tables/finance_lexicon.csv`
* `results/tables/fusion_performance_metrics.csv`
* `results/tables/fusion_comparison.csv`

The ticker-level schema must distinguish:

* raw `evidence_aware_compound = finance_score × reliability`; and
* tradable `evidence_aware_signal = finance_z × reliability`.

Do not create any of these outputs in Stage 6A.

## 10. Required future tests

Specify future tests for:

* exact title preservation;
* vanilla VADER reproducibility;
* approved-lexicon isolation;
* rejected and pending terms not entering the operational lexicon;
* no 2021–2023 information influencing lexicon candidates;
* candidate frequency and threshold reconciliation;
* deterministic candidate ordering and example selection;
* exact-zero versus neutral-band classification;
* no-news versus scored-neutral observations;
* ticker-day equal-weight aggregation;
* sector equal-weight aggregation;
* coverage calculations;
* reliability boundaries;
* independent manual reliability examples;
* previous-252-date standardisation using prior data only;
* exclusion of the current date;
* 60-observation minimum;
* zero or near-zero standard deviation;
* ticker versus sector z-score separation;
* `evidence_aware_signal = finance_z × reliability`;
* one-trading-day lag across ordinary days, weekends and holidays;
* no use of same-day or future headlines;
* future-headline perturbations leaving earlier signals and weights unchanged;
* all 24 overlays;
* Crypto-only fund exclusion;
* Combined-fund crypto-weight preservation;
* Combined-fund equity-sleeve preservation;
* capped-simplex feasibility;
* deterministic projection;
* projection failure producing `BLOCK`;
* lambda fixed at `0.10`;
* monthly-only trading;
* turnover reconciliation;
* transaction-cost reconciliation;
* complete base-versus-overlay reporting;
* exact output schemas;
* deterministic reruns.

Tests must use independent synthetic calculations where possible.

## 11. AI workflow log

Create `ai/07_sentiment_design_and_lexicon_candidates.md` containing:

* objective and exact authorisation;
* complete operational prompt;
* files read;
* student, ChatGPT and Codex roles;
* NLTK-resource result;
* calibration-corpus boundaries and counts;
* deterministic candidate-generation procedure;
* all proposed candidates;
* all recorded rejected candidates;
* AI reasoning and ambiguity warnings;
* confirmation that no return or portfolio result influenced candidate selection or polarity;
* commands and exit codes;
* genuine errors and corrections;
* pre/post manifest evidence;
* status `Pending student review`.

Role attribution must remain accurate:

* the student approved the stage boundary and retains final decision authority;
* ChatGPT assisted the student with workflow and prompt review;
* Codex performed the authorised local inspection, candidate analysis and documentation;
* no AI system may claim that the student approved a candidate.

Do not invent:

* student approval;
* student correction;
* candidate acceptance;
* an AI error that did not occur;
* empirical effectiveness;
* sentiment or fusion results.

## 12. Validation

Run the hand-in checker only after the three documents and Stage 5A closure entry are complete:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -B scripts/check_handin.py
```

Candidate extraction and the VADER-resource check may use the explicit interpreter with temporary code outside Project B.

Do not:

* score the full 2020–2023 corpus;
* generate full ticker sentiment;
* generate sector indices;
* run fusion;
* regenerate portfolios;
* create placeholder outputs.

Capture pre/post manifests and prove:

* only `ai/06_portfolio_implementation.md` changed;
* only the three authorised documents were added;
* no project code changed;
* no results changed or appeared;
* no `.idea` file changed;
* no cache or bytecode appeared;
* no other project file changed;
* no project file was removed.

If the VADER resource was downloaded outside Project B, disclose it separately from the Project B manifest.

Checker success is mechanical evidence only and must not be described as substantive sentiment or fusion completion.

## 13. Final response

Report:

* workspace guard result;
* Stage 5A closure;
* VADER-resource status and resolved path;
* whether any external resource download occurred;
* exact 2020 calibration-corpus boundaries and size;
* candidate count;
* complete compact candidate table;
* rejected-candidate examples;
* confirmation that all candidate decisions remain `PENDING`;
* exact files changed and created;
* checker command, exit code and output;
* manifest result;
* unresolved student decisions;
* confirmation that no sentiment or fusion result was generated;
* final status:

`Stage 6A sentiment innovation design and AI-proposed finance-lexicon candidates documented; pending student review. No lexicon entry or sentiment/fusion result approved.`

Stop. Do not implement sentiment or fusion.

After completion, provide the student with:

* the complete Codex final summary;
* `docs/sentiment_innovation_design.md`;
* `docs/finance_lexicon_review.md`;
* `ai/07_sentiment_design_and_lexicon_candidates.md`.

The next workflow stage will require the student to review every AI-proposed finance term individually and accept, reject or edit it with a reason. That student judgement is required AI-workflow evidence and must not be completed automatically by Codex.
[@06_portfolio_implementation.md](file:///C:/Users/24116/Documents/GitHub/fins-agent/fins2026/z5618000_projectB/ai/06_portfolio_implementation.md)
~~~~

## Review status and next authorised action

**Pending student review.** The student must review every candidate, score, rationale, conflict warning, design rule, and the sector custom-hit-share schema resolution. The next action requires explicit student approval and individual term decisions. No sentiment or fusion implementation may begin automatically.

## Final student review — Stage 6A accepted and Stage 6B authorised

### Confirmation and provenance

After Stage 6A, ChatGPT reviewed all three Stage 6A documents with the student, explained every candidate, deterministic example, ambiguity warning, proposed value, and design choice, and recommended 17 unchanged acceptances, six value edits, and four rejections. The student reviewed that assistance and replied exactly:

> “I have reviewed the methodological design for Stage 6A, the 27 candidate terms, supporting examples and risk statements. I accept the above 17 ACCEPT decisions and the final revised values for the 6 EDIT entries. I reject the four ETF fund-flow terms: inflow, inflows, outflow and outflows. I acknowledge that the ETF fund-flow template carries risks of duplicate reporting and single-stock attribution bias, and these terms should be excluded from the final lexicon. I agree to store sector-level custom-term hit-share metrics within sentiment_diagnostics.csv, and approve the remaining preliminary sentiment outputs and fusion methodology design. Stage 6B is authorised solely to document these student decisions and freeze the final lexicon. No authorisation is yet granted to implement sentiment models, fusion strategies or generate outputs.”

By sending the Stage 6B prompt, the student confirmed the following complete decision statement exactly:

> I have reviewed the Stage 6A methodology, all 27 AI-proposed candidates, the audit examples, and the stated ambiguity risks. I accept the 17 unchanged decisions listed below, approve the six edited final values, and reject `inflow`, `inflows`, `outflow`, and `outflows`.
>
> I agree that repeated ETF-flow template headlines present material ticker-attribution and repeated-reporting risks. ETF-level inflows and outflows therefore should not automatically alter the sentiment score of every tagged constituent.
>
> I accept the proposed sentiment and fusion methodology, including the separation of raw evidence-aware diagnostics from the tradable evidence-aware signal. I also accept preserving the exact required `sector_sentiment_index.csv` schema while storing the sector-level custom-term hit-share diagnostic in `sentiment_diagnostics.csv`.
>
> These are my final pre-implementation lexicon decisions. Stage 6B is authorised only to record these decisions, freeze the approved lexicon and accepted design, and preserve the AI-workflow evidence. No sentiment implementation, full-corpus scoring, sector-index generation, fusion, portfolio regeneration, output generation, figure creation, app work, or report work is authorised.

Codex generated the original 27 proposals and local extraction evidence. ChatGPT supplied the subsequent review assistance and recommendation. The student reviewed that material and explicitly confirmed the final decisions; final authority therefore belongs to the student. This chronology does not claim that the student independently performed Codex's extraction or ChatGPT's technical review.

### Decision reconciliation

The 17 `ACCEPT` decisions retain the AI-proposed values:

- `shares` 0.0; `energy` 0.0; `alert` 0.0; `rally` +1.0; `active` 0.0; `beat` +1.5;
- `asset` 0.0; `beats` +1.5; `overweight` +1.0; `bullish` +1.5; `slump` -1.5;
- `misses` -1.5; `plunge` -1.5; `downgraded` -1.5; `tumble` -1.5; `underweight` -1.0; and `plunges` -1.5.

The six `EDIT` decisions are:

- `rebound`: +1.0 to +0.5;
- `downgrades`: -1.5 to -1.0;
- `outperform`: +1.5 to +1.0;
- `miss`: -1.5 to -1.0;
- `underperform`: -1.5 to -1.0;
- `layoffs`: -1.5 to -1.0.

The four `REJECT` decisions are `inflow`, `inflows`, `outflow`, and `outflows`; their final values remain blank. Thus `17 + 6 + 4 = 27`, with 23 numeric operational entries and four non-operational entries.

The final 23-entry operational list is:

`shares`, `energy`, `alert`, `rally`, `active`, `beat`, `rebound`, `downgrades`, `asset`, `beats`, `outperform`, `miss`, `overweight`, `bullish`, `slump`, `misses`, `plunge`, `downgraded`, `tumble`, `underweight`, `plunges`, `underperform`, and `layoffs`.

The student accepted keeping the exact required `sector_sentiment_index.csv` schema unchanged and placing sector-level `custom_finance_term_hit_share` in `sentiment_diagnostics.csv`. No implementation, full-corpus scoring, sector index, fusion, portfolio regeneration, result, figure, app, report, deployment, publication, or Git operation was authorised.

**Stage 6A accepted and closed; Stage 6B authorised only to record the student’s final lexicon decisions and freeze the accepted pre-result methodology.**
