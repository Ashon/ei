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

log '[1/4] Install dependencies'
pip install -e '.[devel]'

log "[2/4] Lint"
hatch run ${py_version_arg} test:lint

log "[3/4] TypeChecking"
hatch run ${py_version_arg} test:typecheck

log "[4/4] UnitTest"
hatch run ${py_version_arg} test:test
