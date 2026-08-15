# MAIA AI workflow pack

This folder records the staged AI-assisted workflow used for FINS5545 Project B.
The project was deliberately divided into design, implementation, validation
and review stages so that methods could be frozen before results were observed.
Historical records remain chronological; later acceptance sections close the
earlier `Pending student review` status shown at the start of a stage log.

## Roles and accountability

- **Student:** made the final methodological decisions and approvals, reviewed
  the evidence, and retained authority to accept, reject or request corrections.
- **ChatGPT:** collaborated with the student in inspecting methodology, results,
  figures and application behaviour, and helped structure prompts and review
  questions.
- **Codex:** performed the authorised local implementation, tests, validation,
  output generation and technical corrections within each frozen stage boundary.

The student reflection is recorded in [AI_NOTES.md](AI_NOTES.md). The project-wide
operating instructions actually used by Codex are in `../AGENTS.md`.

## Stage index

| Record | Objective and student control | Key risk, correction or evidence | Final status |
|---|---|---|---|
| [01 — Governance and baseline](01_project_governance_and_baseline.md) | Establish the Project B operating contract and incremental approval model. | Protected files, workspace boundary and checker baseline recorded before analytical work. | Accepted and closed before Stage 3A. |
| [02 — Project A hand-off audit](02_project_a_handoff_audit.md) | Assess the student-authorised Project A foundation without silently copying it. | Source-identity limitation, six unmapped endpoint headlines and 69 retained extremes disclosed. | Accepted and closed before Stage 3B. |
| [03 — Data-contract freeze](03_data_contract_freeze.md) | Freeze source, calendar, mapping, missingness and extreme-observation rules before implementation. | No-news versus neutral-news and forward trading-date mapping made explicit. | Accepted and closed before Stage 4A. |
| [04 — Data-foundation implementation](04_data_foundation_implementation.md) | Implement and test the accepted Project B input contract. | Schema, identity, calendar, boundary-date and retained-extreme tests recorded. | Accepted and closed before Stage 4B. |
| [05 — Portfolio-design freeze](05_portfolio_design_freeze.md) | Prespecify the OOS portfolio methodology before calculating results. | Rolling windows, monthly timing, constraints, weight drift, fallback policy and 5-bps cost frozen. | Accepted and closed before Stage 5A. |
| [06 — Portfolio implementation](06_portfolio_implementation.md) | Implement the frozen twelve-fund OOS design and sensitivity evidence. | Five-second wrapper timeout and overly strict output-order validator were corrected without changing the method or results. | Accepted and closed before Stage 6A. |
| [07 — Sentiment design and candidates](07_sentiment_design_and_lexicon_candidates.md) | Prespecify sentiment/fusion rules and create a 2020-only candidate lexicon for student review. | Candidate ambiguity and ticker-attribution risks were surfaced before full-sample scoring. | Accepted and closed before Stage 6B. |
| [08 — Student lexicon review and freeze](08_student_lexicon_review_and_freeze.md) | Record the student's decisions on every candidate and freeze the tradable design. | Twenty-three terms approved or edited; four ETF-flow terms rejected because of attribution and repeated-reporting risks. | Accepted and closed before Stage 6C. |
| [09 — Sentiment and fusion implementation](09_sentiment_fusion_implementation.md) | Implement the frozen lexicon, lagged signals and all eligible overlays. | All 24 favourable and unfavourable comparisons retained; no result-driven tuning permitted. | Accepted and closed before Stage 7. |
| [10 — Results audit and exhibits](10_results_audit_and_exhibit_generation.md) | Independently reconcile frozen outputs and create eight canonical report figures. | Arithmetic, lag, schemas, hashes and complete comparison coverage checked; presentation-only corrections documented. | Accepted and closed before Stage 8. |
| [11 — Streamlit implementation](11_streamlit_implementation.md) | Build and validate MAIA as a read-only app over precomputed results. | Five-page journey, allocation rules, complete sentiment evidence and visual-correction cycles reviewed. | Accepted and closed by the student's final Stage 8 statement. |

## Current hand-off boundary

The analytical models, canonical outputs, report figures and local Streamlit
implementation have been accepted through Stage 8. The Word/PDF report, final
Git repository, public Streamlit deployment, Moodle package and submission are
not claimed as complete in this workflow pack. Those actions require their own
evidence and final student review.

After student review, the unused starter prompt template and unused Claude
instruction placeholder were removed. The submitted workflow evidence consists
of the project-specific Codex instructions, the staged records indexed above,
and the student's reflection.
