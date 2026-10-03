#!/usr/bin/env bash
set -uo pipefail

echo "================================"
echo " AI Tutor — Unit Test Gate"
echo "================================"

FAILED=0
FOUND=0

if [ -f backend/pom.xml ]; then
  FOUND=1
  echo "[Backend/Maven] Unit tests"
  (cd backend && mvn -B test) || FAILED=1
fi

if [ -f backend/package.json ]; then
  FOUND=1
  echo "[Backend/Node] Unit tests"
  (cd backend && npm test) || FAILED=1
fi

if [ -f frontend/package.json ]; then
  FOUND=1
  echo "[Frontend] Unit tests"
  (cd frontend && npm test -- --run) || FAILED=1
fi

if [ -f android/gradlew ]; then
  FOUND=1
  echo "[Android] Unit tests"
  (cd android && ./gradlew test) || FAILED=1
fi

if [ "$FOUND" -eq 0 ]; then
  echo "No supported unit-test project detected."
  echo "Failing closed: unit tests cannot be proven PASS."
  exit 1
fi

if [ "$FAILED" -ne 0 ]; then
  echo
  echo "UNIT TEST GATE: FAILED"
  echo "DEPLOYMENT FORBIDDEN"
  exit 1
fi

echo
echo "UNIT TEST GATE: PASSED"
exit 0
