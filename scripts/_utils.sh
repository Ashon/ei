#!/bin/bash

set -euo pipefail

BIGREEN='\033[1;92m'
NC='\033[0m'

function log {
  echo -e "${BIGREEN}${1}${NC}"
}
