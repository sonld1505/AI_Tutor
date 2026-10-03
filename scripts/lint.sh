#!/usr/bin/env bash
set -euo pipefail

echo "=== LINT / STATIC CHECK ==="

FOUND=0

if [ -f backend/package.json ]; then
  FOUND=1
  (cd backend && npm run lint --if-present)
fi

if [ -f frontend/package.json ]; then
  FOUND=1
  (cd frontend && npm run lint --if-present)
fi

if [ -f android/gradlew ]; then
  FOUND=1
  (cd android && ./gradlew lint)
fi

if [ "$FOUND" -eq 0 ]; then
  echo "No supported project detected."
  echo "Failing closed: lint cannot be proven PASS."
  exit 1
fi

echo "LINT PASSED"
