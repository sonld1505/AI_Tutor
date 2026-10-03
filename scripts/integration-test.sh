#!/usr/bin/env bash
set -euo pipefail

echo "=== INTEGRATION TEST ==="

if [ -f docker-compose.test.yml ]; then
  docker compose -f docker-compose.test.yml up \
    --build \
    --abort-on-container-exit \
    --exit-code-from integration-tests

  docker compose -f docker-compose.test.yml down -v
else
  echo "No docker-compose.test.yml yet."
  echo "Phase 1 requires this gate to be implemented before environment promotion is enabled."
  exit 1
fi

echo "INTEGRATION TEST PASSED"
