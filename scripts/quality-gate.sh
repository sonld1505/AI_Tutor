#!/usr/bin/env bash
set -euo pipefail

echo "================================"
echo " AI Tutor — Quality Gate"
echo "================================"

./scripts/build.sh
./scripts/lint.sh
./scripts/unit-test.sh
./scripts/integration-test.sh
./scripts/security-scan.sh

echo
echo "QUALITY GATE: PASSED"
