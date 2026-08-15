# Stage 2 — Project Governance and Hand-in Baseline

**Date:** 2026-08-14 (Australia/Sydney)  
**Review status:** Pending student review

## Stage objective

Establish the Project B governance contract, preserve an auditable pre-edit hand-in baseline, and document the real AI-assisted workflow. This stage does not author or implement portfolios, sentiment analysis, fusion strategies, Streamlit, results, figures, or report content.

## Roles and provenance

> The student chose an incremental, stage-gated workflow rather than asking an agent to generate the full project. ChatGPT was used to interpret the project brief and Week 10 lecture transcript and to help convert those requirements into this operational prompt. The student selected the scope, provided the files, ran the workflow in PyCharm, and retains responsibility for reviewing and approving the resulting AGENTS.md.

Division of responsibility:

- **ChatGPT:** assisted with interpreting the supplied assessment requirements and structuring the operational prompt.
- **Codex:** inspected the local Project B starter, edited the authorised files, and ran the local checker.
- **Student:** supplied the materials, selected the staged workflow and scope, executes the workflow in PyCharm, reviews the evidence, decides whether corrections are required, and approves or rejects progression.

No student approval, correction, or acceptance of this stage has yet occurred.

## Complete prompt received

The following is the complete operational prompt received by Codex for this stage:

> You are working on FINS5545 Project B.
>
> This is Stage 2 only: establish project governance, AI-workflow provenance, and the hand-in baseline.
>
> Do not implement portfolios, sentiment analysis, fusion strategies, Streamlit, results, figures, or report content in this stage.
>
> ## 1. Mandatory workspace guard
>
> Before reading or changing any file:
>
> 1. Report the active workspace root.
> 2. Report the terminal working directory.
> 3. Confirm that `PROJECT_BRIEF.md` exists directly inside the workspace root.
> 4. Confirm that the exact intended project is:
>
> `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
>
> You must operate only inside `z5618000_projectB`.
>
> If the active workspace is instead `fins-agent`, `fins2026`, `z5618000_projectA`, or any broader/other directory:
>
> * stop immediately;
> * make no changes;
> * explain that the student must reopen the exact Project B folder as the PyCharm project root.
>
> Do not inspect, copy from, or edit Project A in this stage.
>
> ## 2. Read the authoritative Project B materials
>
> If the workspace guard passes, read the following materials completely before editing:
>
> * `PROJECT_BRIEF.md`
> * `README.md`
> * `SUBMISSION_CHECKLIST.md`
> * all relevant files under `context/`
> * `docs/STUDENT_DEPLOY.md`
> * `report/OUTLINE.md`
> * `scripts/check_handin.py`
> * the current `AGENTS.md`
> * the current `CLAUDE.md`
> * the existing README/template files under `ai/`
>
> You may inspect the Project B starter directory structure to understand the intended architecture.
>
> Do not implement or complete any starter source-code modules.
>
> Apply this source hierarchy when instructions conflict:
>
> 1. `PROJECT_BRIEF.md`
> 2. official files in `context/`
> 3. `SUBMISSION_CHECKLIST.md`
> 4. starter README and deployment documentation
> 5. student-created planning files
>
> Do not silently resolve genuine ambiguity. Record it as an uncertainty for student review.
>
> ## 3. Establish the pre-edit baseline
>
> Before editing any file, run:
>
> `python scripts/check_handin.py`
>
> Record the exact observed output.
>
> Based on the student’s previous manual run, the likely baseline is:
>
> * 16 checks passed;
> * 6 reminders concerning the unfinished report/results;
> * 1 failure because both `AGENTS.md` and `CLAUDE.md` are still provided stubs.
>
> This is only an expectation. Do not copy it as if it were observed. Record the command’s actual output.
>
> The six unfinished-output warnings are expected at this early stage. Do not create empty, fake, or placeholder report/result files merely to remove them.
>
> ## 4. Replace only `AGENTS.md`
>
> Replace the provided `AGENTS.md` stub with a concise, project-specific operating contract for Codex.
>
> Keep it practical and preferably between approximately 4 KB and 8 KB, with an upper target below 10 KB. Avoid generic AI advice and unnecessary prose.
>
> Do not edit `CLAUDE.md` because this project is using Codex.
>
> The new `AGENTS.md` must cover all of the following.
>
> ### A. Project purpose and scope
>
> Explain that this repository implements FINS5545 Project B and must produce a reproducible out-of-sample investment workflow connecting:
>
> * the approved Project A dataset;
> * portfolio construction;
> * sector-news sentiment;
> * a defensible fusion strategy;
> * validation evidence;
> * a Streamlit presentation layer;
> * a concise professional report.
>
> State that passing the hand-in checker is necessary but not sufficient for a high mark.
>
> ### B. Instruction and evidence priority
>
> Define the source hierarchy stated above.
>
> Require the agent to distinguish:
>
> * official assignment requirements;
> * student design decisions;
> * empirical findings;
> * interpretations;
> * assumptions;
> * limitations;
> * recommendations.
>
> Require all numerical claims to be traceable to generated tables, figures, validation files, or clearly identified source data.
>
> ### C. Protected scope and files
>
> Require Codex to:
>
> * remain inside the Project B root;
> * not inspect or copy Project A unless the student explicitly authorises that in a later stage;
> * not modify `PROJECT_BRIEF.md`;
> * not modify official files under `context/`;
> * not modify `src/data_access.py`;
> * not modify `scripts/check_handin.py`;
> * not use machine-specific absolute paths in committed code;
> * not add raw datasets, secrets, credentials, virtual environments, caches, or large generated debris;
> * not initialise, push, publish, deploy, or otherwise mutate Git/GitHub unless explicitly authorised;
> * preserve the official starter structure and exact required filenames.
>
> ### D. Incremental agent protocol
>
> Require stage-gated work:
>
> 1. verify the workspace and authorised scope;
> 2. inspect relevant files;
> 3. state a short plan and assumptions;
> 4. implement only the authorised stage;
> 5. run focused validation;
> 6. report files changed, commands run, evidence, limitations, and unresolved issues;
> 7. stop for student review.
>
> The agent must not automatically continue into later stages.
>
> Large “complete the whole project” executions are prohibited.
>
> The student must retain control over methodological decisions, interpretations, and approval of each stage.
>
> ### E. Project A data rules that Project B must preserve
>
> Record the important inherited data rules, including:
>
> * use the official data-access pathway rather than bypassing it;
> * apply the approved cryptocurrency cutoff of 2023-12-31 where required;
> * use adjusted close prices where specified;
> * calculate asset returns on their native trading calendars before applying the approved alignment;
> * align cryptocurrency observations to the relevant equity trading dates consistently;
> * preserve original news headlines and relevant metadata;
> * map news dates forward according to the approved trading-date rule;
> * disclose and exclude the six known unmapped observations instead of silently forcing them into the sample.
>
> State that inherited rules must later be verified against the actual approved Project A files before reuse.
>
> ### F. Out-of-sample portfolio standards
>
> Require:
>
> * only information available at the decision date may affect weights or model choices;
> * explicit documentation of the initial estimation window;
> * explicit live/out-of-sample start date;
> * rolling or expanding-window choice;
> * rebalance frequency;
> * constraints;
> * risk-free-rate convention;
> * transaction-cost convention;
> * weight timing;
> * treatment of drift between rebalances;
> * solver status and fallback behaviour;
> * validation of weight sums, constraints, dates, and asset ordering;
> * appropriate annualisation, ordinarily 252 for equity/combined trading-day series and 365 only where a truly daily crypto-only series is used;
> * an equal-weight benchmark;
> * honest treatment of non-convergence and edge cases;
> * no future-information model selection or parameter tuning;
> * no optimisation designed merely to inflate Sharpe ratio.
>
> Require clear separation between estimation-period information and realised forward returns.
>
> ### G. Sentiment and fusion standards
>
> Require the workflow to begin with a transparent baseline, including plain VADER where applicable.
>
> Record these rules:
>
> * preserve headline casing and punctuation for sentiment scoring;
> * keep “no news” as missing information rather than automatically treating it as neutral sentiment;
> * do not fabricate cryptocurrency news;
> * apply at least a one-trading-day lag before sentiment can affect portfolio weights;
> * estimate standardisation parameters using past data only;
> * document coverage, missingness, aggregation, mappings, and lag rules;
> * validate that the sentiment feature used on a decision date contains no future headlines;
> * distinguish predictive association from causal claims.
>
> Record the planned innovation path, subject to later student approval and empirical validation:
>
> 1. plain VADER baseline;
> 2. a documented, student-reviewed finance-domain lexicon adjustment;
> 3. a confidence-aware, lagged sentiment-tilt strategy that scales exposure according to signal coverage/reliability;
> 4. comparison against the base portfolio and a simpler naive sentiment overlay;
> 5. turnover and transaction-cost analysis.
>
> Make clear that this is currently a planned research direction, not an already-approved conclusion.
>
> Negative or insignificant results must be reported honestly. The workflow must not search repeatedly until a favourable performance result appears.
>
> ### H. Architecture and required outputs
>
> Require:
>
> * reusable analytical logic under `src/`;
> * orchestration through appropriate scripts, including `run_part_b.py`;
> * deterministic outputs where feasible;
> * Streamlit to load precomputed outputs rather than recomputing expensive models on each refresh;
> * light app dependencies;
> * clear schema checks before the app consumes result files.
>
> Protect the exact expected outputs:
>
> * `results/data/fund_returns.csv`
> * `results/data/fund_weights.csv`
> * `results/data/sector_sentiment_index.csv`
> * `results/tables/performance_metrics.csv`
> * `report/report.pdf`
>
> Do not create placeholder versions of these files.
>
> ### I. Testing and validation evidence
>
> Require focused tests and machine-readable validation for material risks, including:
>
> * trading-calendar alignment;
> * forward date mapping;
> * leakage and lag rules;
> * rolling/expanding estimation windows;
> * annualisation conventions;
> * asset ordering;
> * weight sums and constraints;
> * missing-news handling;
> * no-news versus neutral-news distinction;
> * portfolio-weight drift;
> * turnover and transaction costs;
> * output schemas;
> * deterministic reruns where applicable.
>
> Require figures and tables to be self-contained, clearly labelled, and reproducible.
>
> A successful script run alone is not sufficient evidence of correctness.
>
> ### J. Report, interpretation, and academic integrity
>
> Require the final report to:
>
> * answer the investment problem rather than merely describe code;
> * explain the economic reasoning behind design choices;
> * distinguish facts, results, interpretations, limitations, and recommendations;
> * include three concrete recommendations supported by evidence;
> * acknowledge negative findings and uncertainty;
> * avoid causal language unless causality is genuinely established;
> * verify every citation and source;
> * avoid fabricated references, outputs, tests, or claims;
> * be reviewed and rewritten by the student in their own analytical voice.
>
> AI-generated prose must not be treated as final student analysis.
>
> ### K. AI-workflow transparency
>
> Require material AI-assisted stages to be logged under `ai/`.
>
> Each material log should record, where applicable:
>
> * stage objective;
> * participating AI tool and its role;
> * exact prompt or sufficiently complete prompt record;
> * files supplied or inspected;
> * agent output or decisions;
> * identified risks and errors;
> * commands and checks run;
> * verification evidence;
> * student review status;
> * student corrections, acceptances, or rejections;
> * unresolved limitations;
> * next authorised action.
>
> Do not dump every trivial chat message. Log decisions and evidence that demonstrate a genuine iterative workflow.
>
> Never invent a correction, error, test, approval, or student decision.
>
> If student review has not occurred, label it honestly as pending.
>
> Update `AGENTS.md` later only when a recurring, project-wide lesson genuinely belongs in the operating contract. Stage-specific corrections belong in the relevant AI log.
>
> ### L. Definition of done and stop conditions
>
> Define “done” for an individual stage as:
>
> * authorised scope completed;
> * focused checks run;
> * outputs traceable;
> * changes and evidence reported;
> * uncertainties disclosed;
> * AI log updated;
> * student review still required before the next stage.
>
> Require the agent to stop when:
>
> * the workspace is wrong;
> * official requirements conflict;
> * required data are absent;
> * a proposed action exceeds the authorised stage;
> * a methodological choice requires student judgement;
> * validation fails in a way that could materially change the conclusion.
>
> ## 5. Create the Stage 2 AI-workflow log
>
> Create:
>
> `ai/01_project_governance_and_baseline.md`
>
> This is evidence of the real workflow, not promotional prose.
>
> It must contain:
>
> 1. stage title and date;
> 2. stage objective;
> 3. roles and provenance;
> 4. the complete prompt received in this chat;
> 5. files read;
> 6. exact pre-edit checker command and output;
> 7. concise summary of the new `AGENTS.md`;
> 8. risks or uncertainties identified;
> 9. exact post-edit checker command and output;
> 10. files changed;
> 11. student-review status;
> 12. next action, explicitly marked as requiring student approval.
>
> Include the following provenance statement accurately, without claiming that the prompt was written solely by the student:
>
> > The student chose an incremental, stage-gated workflow rather than asking an agent to generate the full project. ChatGPT was used to interpret the project brief and Week 10 lecture transcript and to help convert those requirements into this operational prompt. The student selected the scope, provided the files, ran the workflow in PyCharm, and retains responsibility for reviewing and approving the resulting AGENTS.md.
>
> Also record the division of responsibility:
>
> * ChatGPT: assisted with interpreting the supplied assessment requirements and structuring the operational prompt;
> * Codex: inspected the local Project B starter, edited the authorised files, and ran the local checker;
> * student: supplied the materials, selected the staged workflow and scope, executes the workflow in PyCharm, reviews the evidence, decides whether corrections are required, and approves or rejects progression.
>
> Do not state that the student has approved this stage yet.
>
> Set the review status to something equivalent to:
>
> `Pending student review`
>
> Do not invent criticisms or corrections merely to make the workflow look iterative. Real corrections will be added after the student reviews this output.
>
> ## 6. Run the post-edit checker
>
> After creating the two authorised files, run again:
>
> `python scripts/check_handin.py`
>
> Record the exact output.
>
> The expected effect is:
>
> * the AGENTS/CLAUDE placeholder failure should be resolved because `AGENTS.md` is now project-specific;
> * the six unfinished report/result reminders should remain.
>
> Again, record the actual output rather than the expected wording.
>
> If a new failure appears, diagnose it but do not expand the editing scope without student approval.
>
> ## 7. Strict change boundary
>
> Exactly two files may be created or modified in this stage:
>
> * `AGENTS.md`
> * `ai/01_project_governance_and_baseline.md`
>
> Do not change any other file.
>
> Specifically, do not:
>
> * implement source code;
> * copy files from Project A;
> * create models;
> * generate results;
> * create figures;
> * write the report;
> * build Streamlit;
> * install dependencies;
> * initialise or modify Git;
> * remove expected warnings using fake placeholder outputs.
>
> ## 8. Final response and mandatory stop
>
> At the end, report:
>
> 1. confirmed workspace root;
> 2. files read;
> 3. exactly which two files changed;
> 4. exact pre-edit checker result;
> 5. exact post-edit checker result;
> 6. key sections added to `AGENTS.md`;
> 7. uncertainties or risks;
> 8. student-review status;
> 9. the next proposed stage, without starting it.
>
> Then stop and wait for student review.
> [@README.md](file:///C:/Users/24116/Documents/GitHub/fins-agent/fins2026/z5618000_projectB/README.md)

## Files read and structure inspected

Read completely before editing:

- `PROJECT_BRIEF.md`
- `README.md`
- `SUBMISSION_CHECKLIST.md`
- `context/DATA_GUIDE.md`
- `context/project_context.md`
- `context/verify_ai_output.md`
- `docs/STUDENT_DEPLOY.md`
- `report/OUTLINE.md`
- `scripts/check_handin.py`
- the original `AGENTS.md` stub
- the original `CLAUDE.md` stub
- `ai/README.md`
- `ai/prompt_log_template.md`

The Project B starter directory tree was inspected to identify its architecture and required filenames. No starter source-code module was opened or completed. No Project A file or directory was inspected. The environment-owned PyCharm Python-tooling instructions were also consulted because they govern interpreter selection; they were not modified or copied into the project.

## Workspace guard evidence

- Active workspace root: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Terminal working directory: `C:\Users\24116\Documents\GitHub\fins-agent\fins2026\z5618000_projectB`
- Resolved root matched the intended path exactly: `True`
- `PROJECT_BRIEF.md` existed directly in that root: `True`

## Pre-edit checker

Exact command:

```text
python scripts/check_handin.py
```

Exit code: `1`

Exact observed output:

```text
16 checks passed.
6 reminder(s):
  [WARN] no report/report.pdf yet - author it in Word and export to PDF
  [WARN] results/ has no figures or tables yet - save your exhibits there
  [WARN] expected output results/data/fund_returns.csv not found - use this exact name so markers can find it
  [WARN] expected output results/data/fund_weights.csv not found - use this exact name so markers can find it
  [WARN] expected output results/data/sector_sentiment_index.csv not found - use this exact name so markers can find it
  [WARN] expected output results/tables/performance_metrics.csv not found - use this exact name so markers can find it
1 problem(s) to fix:
  [FAIL] edit AGENTS.md or CLAUDE.md (your tool's file) with your own instructions - both are still the provided stub
```

The six reminders were retained as legitimate early-stage gaps. No placeholder report or result artifact was created.

## Summary of the new `AGENTS.md`

The replacement is a project-specific Codex operating contract covering:

- project purpose, source priority, evidence traceability, protected files, and a strict stage-gated protocol;
- inherited Project A data rules that must be verified before reuse;
- look-ahead-safe portfolio, annualisation, solver, benchmark, drift, turnover, and transaction-cost standards;
- transparent VADER baseline and a proposed—not approved—finance-lexicon/confidence-aware fusion research path;
- architecture, exact output names, precomputed-app design, testing, and machine-readable validation expectations;
- report integrity, student-authored interpretation, curated AI-workflow provenance, definition of done, and stop conditions.

The resulting `AGENTS.md` is 9,332 bytes, below the requested 10 KB upper target.

## Risks and uncertainties identified

1. `PROJECT_BRIEF.md` is headed “FINS3645,” while the operational prompt identifies this as FINS5545 Project B. The contract follows the explicit Stage 2 instruction but this course-code inconsistency remains pending student clarification.
2. The “six known unmapped observations” requirement appears in the operational prompt but is not documented in the supplied Project B brief or `context/` files. It is recorded as inherited information that must be verified against the student’s actual approved Project A evidence before reuse.
3. The approved Project A artifacts and the Week 10 lecture transcript were not present in, and were not inspected from, the authorised Project B starter. Any later reuse or lecture-derived methodology requires supplied evidence and explicit student authorisation.
4. PyCharm reported no interpreter configured for `scripts/check_handin.py` and proposed creating a requirements-based environment. Stage 2 forbids installing dependencies or changing files beyond the two authorised documents, so no interpreter or environment was created. The exact requested terminal command nevertheless ran successfully via the available `python` command; environment configuration remains a reproducibility issue for a later authorised setup stage.
5. The checker is mechanical. Its success cannot validate methodology, leakage controls, results, interpretation, report quality, or deployment.
6. `CLAUDE.md` remains the official stub by design because the student selected Codex and authorised replacement of `AGENTS.md` only.
7. The planned sentiment innovation path is a research proposal pending student judgement and later empirical testing, not a result or approved conclusion.

## Post-edit checker

Exact command run after both authorised files existed:

```text
python scripts/check_handin.py
```

Exit code: `0`

Exact observed output:

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

The stub failure was resolved by the project-specific `AGENTS.md`. All six unfinished-output reminders remain, as expected and appropriate for this governance-only stage.

## Files changed

Exactly these two authorised files:

- `AGENTS.md` — replaced the provided stub with the Project B Codex operating contract.
- `ai/01_project_governance_and_baseline.md` — created this Stage 2 evidence log.

No other project file was intentionally created or modified.

## Student review status

**Pending student review.**

No student criticism, correction, acceptance, rejection, or approval has been inferred or invented. The student must compare this contract and log with their intended workflow and request any needed corrections.

## Next action — requires student approval

**Do not begin automatically.** After reviewing and accepting or correcting Stage 2, the student may authorise a proposed Stage 3: supply and verify the approved Project A hand-off evidence, resolve the recorded course-code and six-unmapped-observations uncertainties, and freeze the Part B data contract and methodological decisions before implementation.

## Student review — Correction cycle 1

**Review date:** 2026-08-14 (Australia/Sydney)  
**Status:** Correction cycle 1 completed; awaiting student final acceptance

### Review provenance

ChatGPT performed an external, rubric-based audit of the Stage 2 files with the student. The findings below arose from that ChatGPT-assisted review; they are not presented as issues the student independently discovered. The student supplied these factual confirmations:

- The enrolled course is **FINS5545**. The `FINS3645` heading in the supplied `PROJECT_BRIEF.md` is therefore a metadata inconsistency in the starter. The official brief remains protected and was not edited; its substantive assignment requirements retain their stated priority.
- The Project B PyCharm project currently has **no configured interpreter**. The terminal `python` command nevertheless ran the checker successfully through the available terminal environment.

The student authorised this correction cycle only and has not given final acceptance of the corrected Stage 2 files.

Interaction-record annotation: the trailing `[@README.md](file:///C:/Users/24116/Documents/GitHub/fins-agent/fins2026/z5618000_projectB/README.md)` marker in the original captured prompt is a PyCharm file-context attachment marker, not student-authored methodological content. The original prompt record above is preserved unchanged.

### What the review accepted

- The workspace was correctly isolated to the exact Project B root.
- The ChatGPT, Codex, and student roles were described honestly.
- The exact pre-edit and post-edit checker evidence was preserved.
- No student approval, criticism, or correction was fabricated.
- The work was appropriately stage-gated and did not enter Project B implementation.

### Issues identified

- The identical-weight wording could encourage artificial differentiation even when similar outputs are mathematically legitimate.
- The report limit, canonical-exhibit reference, and final hand-in/deployment requirements were missing from the operating contract.
- The interpreter state needed clearer treatment because terminal command success does not establish a configured Project B PyCharm interpreter.
- The course-code inconsistency required resolution using the student's factual confirmation.

### Requested corrections and reasons

1. Resolve course metadata in favour of the student-confirmed FINS5545 identity while preserving the brief unchanged and retaining its substantive authority.
2. Replace the identical-weight instruction with a diagnostic rule so valid outputs are investigated and documented, never cosmetically altered.
3. Add the report page limit, canonical Section 5 exhibits, and complete final-delivery requirements so the operating contract covers the hand-in baseline.
4. Require interpreter, Python-version, and dependency verification before model execution so later work does not confuse terminal availability with PyCharm configuration.
5. Append this evidence rather than rewriting the original record, preserving the real chronology of review and correction.

### Concise follow-up prompt record

The student authorised “Stage 2 Student Review — Correction Cycle 1” in the same chat, restricted work to the existing `AGENTS.md` and this log, prohibited Stage 3 and all implementation, supplied the FINS5545 and interpreter confirmations, specified four focused contract amendments, required an appended review trail, required the exact `python scripts/check_handin.py` result, and required a final two-file boundary check followed by a stop for final acceptance.

### Exact changes made by Codex

- Added the student-confirmed FINS5545 metadata clarification near the source hierarchy without editing or weakening `PROJECT_BRIEF.md`.
- Replaced “credible—not silently identical—weights” with a rule to diagnose identical or near-identical weights and never perturb valid outputs for appearance.
- Added the 10-page narrative limit, Section 5 canonical-exhibit rule, complete Moodle ZIP/public GitHub/live Streamlit hand-in requirements, private-while-building rule, and student control of credentialed deployment and publication.
- Added a pre-model requirement to record the selected PyCharm interpreter, Python version, and dependency availability, explicitly distinguishing terminal `python` success from PyCharm configuration.
- Tightened nearby wording without removing material safeguards. Final `AGENTS.md` size: **10,050 bytes**, below 10 KiB.
- Appended this correction-cycle evidence; the original Stage 2 record was not rewritten.

### Validation

Exact command authorised after the two-file correction:

```text
python scripts/check_handin.py
```

Immediately before the command, PyCharm's read-only environment check reported no interpreter configured for `scripts/check_handin.py`. No interpreter was configured or installed. The command ran through the available terminal environment.

Exit code: `0`

Exact observed output:

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

The six expected unfinished-output reminders remain. No placeholder output was created to remove them.

### Remaining uncertainties

- Project B still has no configured PyCharm interpreter. Selecting and verifying one is unresolved and was expressly outside this correction cycle.
- The inherited count of six unmapped news observations still requires verification against the approved Project A evidence in a later, explicitly authorised stage.
- The supplied brief's heading remains unchanged as required; the project identity itself is resolved as FINS5545 through the student's confirmation.
- Stage 3 remains unauthorised.

### Review status

**Correction cycle 1 completed; awaiting student final acceptance.**

No final student approval is claimed.

## Student review — Correction cycle 2

**Review date:** 2026-08-14 (Australia/Sydney)  
**Status:** Correction cycle 2 completed; awaiting student final acceptance

### Review provenance

This correction arose from a ChatGPT-assisted final audit conducted with the student. ChatGPT identified the compressed innovation sentence as semantically ambiguous. The environment chronology and the recheck of the supplied Project Brief PDF, Project Overview, Week 10 slides, Week 10 transcript, starter README, requirements files, and deployment guide are student-provided ChatGPT review evidence; Codex did not independently inspect those external attachments in this cycle. The student challenged the initial environment recommendation, supplied the factual evidence, selected the corrected environment approach, and retained decision-making control. Codex read only the two authorised Project B governance records, made the authorised edits, and ran the local read-only validations recorded below.

### Innovation wording correction

Correction Cycle 1 had compressed the final safeguard to: “This is research direction, not an approved conclusion. Report negative or insignificant results honestly; do not search until a favourable result appears.” The grammar was incomplete, and “do not search until” could be read as discouraging research before favourable evidence exists. Methodologically, the intended safeguard is against data snooping, repeated specification searching, and cosmetic changes made to manufacture a favourable outcome—not against legitimate research or honest evaluation.

Codex replaced the complete paragraph with exactly:

> The planned innovation path, pending student approval and empirical validation, is: (1) plain VADER; (2) a documented, student-reviewed finance lexicon adjustment; (3) a confidence-aware, lagged tilt scaled by signal coverage or reliability; (4) comparison with the base portfolio and a naive overlay; and (5) turnover and transaction-cost analysis. This is a proposed research direction, not an approved conclusion. Report negative or insignificant results honestly; do not repeatedly adjust models, parameters, samples, or reporting choices until a favourable result appears.

No innovation method was approved or implemented in this correction cycle. The path remains a proposal pending student approval and empirical validation.

### Environment-recommendation correction and student decision

After the student reopened the exact Project B folder, the initial terminal `python` resolved to the system interpreter:

```text
C:\Users\24116\AppData\Local\Programs\Python\Python313\python.exe
```

ChatGPT had previously recommended a Project B-specific virtual environment too categorically. The student questioned whether the course required an independent environment. ChatGPT then rechecked the supplied course and starter materials listed above. According to that student-provided review evidence, those materials contain no explicit requirement for a separate Part B virtual environment: they require the correct project folder, required dependencies, reproducibility, and an independent Project B GitHub repository. Repository independence is not an environment mandate.

The student therefore chose to reuse the existing environment at:

```text
C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe
```

The student manually activated it in the Project B terminal and supplied this evidence:

```text
Executable: C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe
```

```text
All Part B imports OK
```

```text
No broken requirements found.
```

The student reported Python 3.13.13 and successful imports of `pandas`, `numpy`, `scipy`, `pyarrow`, `requests`, `matplotlib`, `streamlit`, and `nltk`. No new virtual environment was created and no dependency was installed during the student's resolution. The workflow was corrected to reuse this existing verified environment; this is the student's project decision, not a claimed course mandate.

### Codex independent environment verification

Codex used the explicit executable so validation did not depend on terminal activation. PyCharm's read-only environment probe also identified this executable as the selected Python 3.13.13 `venv` with `pip`.

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -c "import sys; print('Executable:', sys.executable); print('Version:', sys.version)"
```

Exit code: `0`

Exact output:

```text
Executable: C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe
Version: 3.13.13 (tags/v3.13.13:01104ce, Apr  7 2026, 19:25:48) [MSC v.1944 64 bit (AMD64)]
```

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -c "import pandas, numpy, scipy, pyarrow, requests, matplotlib, streamlit, nltk; print('All Part B imports OK')"
```

Exit code: `0`

Exact output:

```text
All Part B imports OK
```

Command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' -m pip check
```

Exit code: `0`

Exact output:

```text
No broken requirements found.
```

The environment is resolved for Project B local development through the existing shared virtual environment. Codex created no environment, installed no dependency, and modified nothing in that environment. Terminal auto-activation in a newly opened terminal was not independently tested; the explicit interpreter is verified and manual activation works, so a new terminal may need manual activation. VADER lexicon-resource availability was deliberately not tested or downloaded.

### Files deliberately changed by Codex

- `AGENTS.md` — replaced only the complete ambiguous planned-innovation paragraph with the exact corrected wording above. Final size: **10,133 bytes**, below 10 KiB.
- `ai/01_project_governance_and_baseline.md` — appended this Correction Cycle 2 evidence chronologically.

No other authored Project B file was deliberately modified or created.

### Hand-in checker evidence

Exact command authorised through the verified environment:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' scripts/check_handin.py
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
```

The six expected unfinished-output reminders remain. No placeholder report or result file was created to remove them.

### Remaining uncertainties

- The approved Project A hand-off must still be verified and reused under controlled, explicitly authorised scope.
- The inherited six unmapped news observations must be verified against approved Project A evidence.
- VADER lexicon-resource availability is deferred to the authorised sentiment stage.
- Stage 3 remains unauthorised.

### Final review status

**Correction cycle 2 completed; awaiting student final acceptance.**

No final student approval is claimed.

## Final student acceptance — Stage 2 closed

**Acceptance date:** 2026-08-14 (Australia/Sydney)

The student explicitly stated:

> “I have read and accept the Stage 2 governance contract, environment decision, and audit record. I confirm reuse of the existing fins-agent/.venv and do not require a separate Project B environment. I understand that the innovation path still requires later item-by-item approval and empirical validation. Stage 3 is not authorised.”

This accepts the Stage 2 governance contract, environment decision, and audit record. It does not approve any innovation method, empirical conclusion, or Stage 3 implementation. Verification and controlled reuse of the approved Project A hand-off, the six unmapped observations, and VADER resource availability remain matters for later authorised stages.

### Closure checker

Exact command:

```powershell
& 'C:\Users\24116\Documents\GitHub\fins-agent\.venv\Scripts\python.exe' scripts/check_handin.py
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
```

This is a mechanical hand-in check only; it does not establish substantive project completion.

**Final status:** Stage 2 accepted and closed; Stage 3 not authorised.
