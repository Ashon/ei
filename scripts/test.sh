#!/bin/bash

set -euo pipefail

scriptPath=$(dirname $0)
. $scriptPath/_utils.sh

log '[1/4] Install dependencies'
pip install -e '.[devel]'

log "[2/4] Lint"
hatch run test:lint

log "[3/4] TypeChecking"
hatch run test:typecheck

log "[4/4] UnitTest"
hatch run test:test
