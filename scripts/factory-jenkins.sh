#!/usr/bin/env bash
set -euo pipefail
exec "$(git rev-parse --show-toplevel)/scripts/factory-runtime.sh" jenkins --branch "${BRANCH_NAME:-$(git branch --show-current)}"
