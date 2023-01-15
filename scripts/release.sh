#!/bin/bash

set -euo pipefail

scriptPath=$(dirname $0)
. $scriptPath/_utils.sh

log '[1/3] Install dependencies'
pip install -e '.[devel]'

log "[2/3] Build packages"
hatch build

log "[3/3] Pubilsh to pypi"
hatch publish
