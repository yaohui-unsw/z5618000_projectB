# MAIA — Multi-Asset Investment Assistant

MAIA is the local Streamlit product for FINS5545 Project B. It helps a
financially curious retail investor compare twelve systematic Equity, Crypto,
and Combined funds using transparent historical out-of-sample evidence and
precomputed news-sentiment analytics. It is a portfolio-management interface,
not a trading account, performance forecast, or personalised advice service.

## App experience

The single entrypoint, `streamlit_app.py`, provides five sections:

1. **Explore Funds** — all 12 base funds, their historical metrics, risk-return
   view, and selectable net growth-of-$1 paths.
2. **Fund Fact Sheet** — one fund's exact canonical metrics, drawdown, latest
   target holdings, turnover, constraints, and operating terms.
3. **Allocation Studio** — a one-time allocation across two to four funds with
   fund sleeves allowed to drift historically.
4. **Sentiment & Innovation** — Finance-VADER sector evidence, the 23-term
   student-reviewed lexicon, and all 24 frozen fusion comparisons.
5. **Methodology & Disclosures** — a concise explanation of the frozen design,
   robustness evidence, and limitations.

The default page is useful immediately; no account, login, bank funding, order
execution, live price, or raw-data access is implemented.

## Read-only data architecture

The deployed app reads validated, precomputed CSV artifacts under `results/`
only. It does not call `src/data_access.py`, rerun portfolio optimisation, import
VADER, rescore news, or execute fusion. The analytical build pipeline remains
separate from the app.

`nltk` is a build/reproduction-only dependency in `requirements-dev.txt`; it is
not imported by the Streamlit runtime. Runtime packages are already declared in
`requirements.txt`.

## Run locally

From this Project B root in PowerShell, use the verified shared environment:

```powershell
& '..\..\.venv\Scripts\python.exe' -B -m streamlit run streamlit_app.py
```

For the focused app tests:

```powershell
& '..\..\.venv\Scripts\python.exe' -B -m pytest -p no:cacheprovider tests/test_app_data.py tests/test_app_logic.py tests/test_streamlit_app.py tests/test_smoke.py
```

If a required precomputed artifact is missing or has the wrong schema, MAIA
shows a named error instead of substituting a placeholder.

## Costs shown in MAIA

- Canonical fund `net_return` already includes the frozen **5-bps transaction
  cost per unit of one-way turnover**. The app never applies that cost again.
- Allocation Studio separately displays a **0.50% p.a. illustrative management
  fee**, applied to account wealth by elapsed calendar time. This is a
  user-facing product illustration, not a canonical portfolio-model result.

All performance remains historical out-of-sample evidence. It is not a
forecast, recommendation, or guarantee.

## Project structure

- `streamlit_app.py` — root Streamlit entrypoint
- `.streamlit/config.toml` — local visual theme
- `src/app_data.py` — cached, read-only canonical-artifact loaders
- `src/app_logic.py` — pure display and allocation calculations
- `src/app_charts.py` — in-memory application charts
- `results/` — frozen analytical CSVs and canonical report figures
- `scripts/` — analytical reproduction and validation commands
- `context/` — official supplied context; do not edit
- `report/` — report workspace
- `ai/` — staged AI-workflow evidence

## Future deployment and hand-in

Deployment remains a student-controlled future action. No repository was made
public and no Streamlit Community Cloud deployment was started in Stage 8.
When authorised, follow [docs/STUDENT_DEPLOY.md](docs/STUDENT_DEPLOY.md) and the
official Project Brief. Final hand-in still requires the Moodle ZIP, public
GitHub repository, and working live Streamlit URL.
