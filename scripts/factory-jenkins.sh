#!/usr/bin/env bash
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
BRANCH=${BRANCH_NAME:-$(git branch --show-current)}
mkdir -p "$ROOT/factory/logs"
"$ROOT/scripts/factory-runtime.sh" jenkins --branch "$BRANCH" 2>&1 | tee "$ROOT/factory/logs/factory-jenkins.log"
for step in build lint unit; do
    "$ROOT/scripts/factory-runtime.sh" "$step" 2>&1 | tee "$ROOT/factory/logs/factory-$step.log"
done
"$ROOT/scripts/security-scan.sh" 2>&1 | tee "$ROOT/factory/logs/factory-security.log"
echo 'FACTORY CI PASS'
