#!/bin/bash

set -euo pipefail

scriptPath=$(dirname $0)
. $scriptPath/_utils.sh

log "Run Test"
log "- on python version: $(uv run python --version)"

log '[1/4] Install dependencies'
uv sync

log "[2/4] Lint"
uv run ruff check

log "[3/4] TypeChecking"
uv run mypy .

log "[4/4] UnitTest"
uv run pytest
