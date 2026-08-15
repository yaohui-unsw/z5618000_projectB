# Codex Operating Contract — FINS5545 Project B

## Purpose, authority, and evidence

This is FINS5545 Project B: a reproducible, out-of-sample workflow linking approved Project A data, portfolios, sector-news sentiment, defensible fusion, validation, Streamlit, and a professional report. Passing `scripts/check_handin.py` is necessary, not sufficient for a high mark; correctness, originality, evidence, interpretation, and reproducibility still matter.

When instructions conflict, use this priority:

1. `PROJECT_BRIEF.md`.
2. Official files under `context/`.
3. `SUBMISSION_CHECKLIST.md`.
4. Starter `README.md` and deployment documentation.
5. Student-created plans and notes.

The student confirms enrolment in FINS5545. The supplied brief's `FINS3645` heading is a known metadata inconsistency: do not edit it; identify this project as FINS5545. This does not override the brief's substantive requirements or priority.

Do not silently resolve ambiguity; record the conflict, consequence, and student decision required. Distinguish official requirements, student decisions, findings, interpretations, assumptions, limitations, and recommendations. Trace every number to source data or reproducible tables, figures, or validation files.

## Scope and protected files

- Work only in this Project B root. Do not inspect or copy Project A without explicit student authorisation in a later stage.
- Never modify `PROJECT_BRIEF.md`, official files under `context/`, `src/data_access.py`, or `scripts/check_handin.py`.
- Preserve the starter architecture and exact required filenames. Do not use machine-specific absolute paths in committed code.
- Do not add raw datasets, secrets, credentials, virtual environments, caches, compiled files, or large generated debris.
- Do not initialise or mutate Git, commit, push, publish, or deploy unless the student explicitly authorises that stage.
- Never create empty or fabricated outputs to satisfy the checker.

## Incremental protocol and student control

For every authorised stage:

1. Verify the workspace root and the exact authorised scope.
2. Read the relevant official and existing project files.
3. State a short plan, assumptions, and decisions still requiring approval.
4. Implement only that stage; do not continue automatically.
5. Run focused validation proportionate to the material risks.
6. Report files changed, commands run, evidence, limitations, and unresolved issues.
7. Update the material AI log and stop for student review.

Large “complete the whole project” executions are prohibited. The student retains control of methodological choices, interpretations, corrections, and approval of each next stage.

## Inherited Project A data rules

Project B must preserve these inherited rules, while verifying them against the actual approved Project A files before reuse:

- Load through the official `src/data_access.py` pathway; do not bypass it.
- Apply the approved cryptocurrency cutoff of `2023-12-31` where required and use adjusted close where specified.
- Calculate returns for each asset on its native trading calendar before applying the approved alignment. Align crypto observations consistently to the relevant equity trading dates.
- Preserve original headline casing, punctuation, text, and relevant metadata. Map news dates forward using the approved trading-date rule.
- Disclose and exclude the six known unmapped observations rather than forcing them into the sample. This count is an inherited claim and must be checked against approved Project A evidence before use.

## Out-of-sample portfolio standards

- Only information available at a decision date may influence weights, model choice, or parameters. Keep estimation-period inputs separate from realised forward returns.
- Document the initial estimation window, first live/out-of-sample date, rolling versus expanding window, rebalance frequency, constraints, risk-free-rate convention, transaction-cost convention, weight timing, and treatment of weight drift between rebalances.
- Record solver status and deterministic fallback behaviour. Validate weight sums, constraints, dates, and asset ordering. If methods produce identical or near-identical weights, diagnose and document whether the cause is the data, constraints, implementation, or a legitimate mathematical result. Never perturb or alter valid outputs merely to make methods appear different.
- Ordinarily annualise equity and combined trading-day series with 252. Use 365 only for a genuinely daily crypto-only series; document any departure.
- Include an equal-weight benchmark. Treat non-convergence and edge cases honestly.
- Never use future information for model selection or parameter tuning, and never optimise merely to inflate Sharpe ratio.

## Sentiment and fusion standards

Begin with a transparent baseline, including plain VADER where applicable.

- Preserve headline casing and punctuation when scoring. Do not fabricate crypto news.
- “No news” is missing information, not automatically neutral sentiment. Preserve the distinction between no headline and a scored-neutral headline.
- Apply at least a one-trading-day lag before sentiment affects weights. On every decision date, validate that the feature contains no future headline.
- Estimate standardisation parameters from past data only. Document coverage, missingness, aggregation, sector/ticker mappings, date mapping, and lag rules.
- Describe predictive association without causal claims unless causality is genuinely established.

The planned innovation path, pending student approval and empirical validation, is: (1) plain VADER; (2) a documented, student-reviewed finance lexicon adjustment; (3) a confidence-aware, lagged tilt scaled by signal coverage or reliability; (4) comparison with the base portfolio and a naive overlay; and (5) turnover and transaction-cost analysis. This is a proposed research direction, not an approved conclusion. Report negative or insignificant results honestly; do not repeatedly adjust models, parameters, samples, or reporting choices until a favourable result appears.

## Architecture and required outputs

- Put reusable analytical logic under `src/` and orchestration in appropriate scripts, including `scripts/run_part_b.py`.
- Make outputs deterministic where feasible. The Streamlit app must load precomputed outputs rather than rerun expensive models on refresh; keep app dependencies light and validate schemas before consumption.
- Before model execution, verify and record the selected Project B PyCharm interpreter, Python version, and required dependency availability. A successful terminal `python` command does not prove that PyCharm has the intended project interpreter configured.
- Preserve these exact deliverables and never create placeholder versions:
  - `results/data/fund_returns.csv`
  - `results/data/fund_weights.csv`
  - `results/data/sector_sentiment_index.csv`
  - `results/tables/performance_metrics.csv`
  - `report/report.pdf`

## Testing and validation evidence

Create focused tests and machine-readable validation for material risks: trading-calendar alignment; forward news-date mapping; leakage and lag rules; rolling/expanding windows; annualisation; asset ordering; weight sums and constraints; missing-news handling; no-news versus neutral-news; portfolio-weight drift; turnover and transaction costs; output schemas; and deterministic reruns where applicable. Validate boundary dates and manually check representative calculations. A successful script run alone is not proof of correctness. Figures and tables must be reproducible, self-contained, clearly labelled with units and sample dates, and interpreted against their underlying data.

## Report, interpretation, integrity, and delivery

The final report must answer the investment problem rather than describe code; explain the economics of design choices; separate facts, results, interpretations, limitations, and recommendations; give three concrete evidence-backed recommendations; acknowledge negative findings and uncertainty; and avoid causal language without causal evidence. Verify every source and number; never fabricate references, outputs, tests, or claims. AI prose is a draft the student must review and rewrite in their own analytical voice.

- Limit written narrative to 10 pages, excluding appendix and references. The canonical required exhibits are those in Section 5 of `PROJECT_BRIEF.md`.
- Final hand-in requires the complete Moodle ZIP, a public GitHub repository, and a working live Streamlit URL. Keep the repository private while building and make it public only at final hand-in. Credentialed browser deployment and final publication remain student-controlled actions and require explicit authorisation.

## AI-workflow transparency

Log each material AI-assisted stage under `ai/`. Where applicable, record the stage objective; participating AI tool and role; exact or sufficiently complete prompt; files supplied or inspected; agent output and decisions; risks and errors; commands and checks; verification evidence; student review status; student corrections, acceptances, or rejections; unresolved limitations; and next authorised action.

Curate decisions and evidence rather than dumping every trivial chat message. Never invent an error, correction, test, approval, or student decision. If review has not occurred, state `Pending student review`. Update this contract later only when a recurring project-wide lesson belongs here; put stage-specific corrections in that stage’s AI log.

## Definition of done and stop conditions

A stage is done only when its authorised scope is complete, focused checks have run, outputs are traceable, changes and evidence are reported, uncertainties are disclosed, and the AI log is updated. Student review is still required before the next stage.

Stop without expanding scope when the workspace is wrong; official requirements conflict; required data are absent; an action exceeds the authorised stage; a methodological choice needs student judgement; or validation fails in a way that could materially change a conclusion.
