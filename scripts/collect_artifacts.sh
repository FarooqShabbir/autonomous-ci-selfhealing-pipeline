#!/usr/bin/env bash
set -eo pipefail
# collect additional artifacts for triage
echo "Collecting env and pip list..."
uname -a > sys_info.txt || true
python -c "import sys, json; print(sys.version)" > python_version.txt || true
pip freeze > pip_freeze.txt || true
tar -czf extra_artifacts.tar.gz sys_info.txt python_version.txt pip_freeze.txt || true
