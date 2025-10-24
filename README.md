# CI Self-Healer (Demo)

This repository demonstrates an autonomous CI pipeline for a synthetic application (`simulate_app.py`).

Workflow: .github/workflows/ci_selfheal.yml

How it works:
1. `test` job runs `python simulate_app.py` and uploads `run_output.log`.
2. If the test fails, `self_heal` job runs `scripts/diagnose_and_fix.py`.
3. If diagnostics succeed, the workflow triggers a rerun automatically (limited attempts).
4. If not healed, an issue is created with artifacts for human triage.

To run locally:
- `python simulate_app.py`    # test the simulated app
- `python scripts/diagnose_and_fix.py`    # run diagnoser locally

Adjust `MAX_RETRIES` and retry/wait parameters in scripts/diagnose_and_fix.py as needed.
