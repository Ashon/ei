#!/bin/bash

set -euo pipefail

scriptPath=$(dirname $0)
. $scriptPath/_utils.sh

log '[1/3] Install dependencies'
uv sync

log "[2/3] Build packages"
uv build

log "[3/3] Pubilsh to pypi"
uv publish
