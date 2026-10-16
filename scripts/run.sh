#!/usr/bin/env bash
set -euo pipefail
project_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$project_dir"
source ./aws-env.sh
exec .venv/bin/python -m streamlit run app.py --server.address 127.0.0.1 "$@"
