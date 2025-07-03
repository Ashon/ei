#!/bin/bash

set -euo pipefail

python_version=${1:-""}

scriptPath=$(dirname $0)
. $scriptPath/_utils.sh

if [ $python_version ]; then
  py_version_arg="+py=${python_version}"
else
  py_version_arg=""
fi

log "Run Test ${python_version} ${py_version_arg}"
log "- on python version: $(uv run python --version)"

log '[1/4] Install dependencies'
uv sync

log "[2/4] Lint"
uv run ruff check

log "[3/4] TypeChecking"
uv run mypy .

log "[4/4] UnitTest"
uv run pytest
