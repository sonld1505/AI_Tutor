#!/usr/bin/env bash
set -euo pipefail

echo "=== BUILD ==="

FOUND=0

if [ -f backend/pom.xml ]; then
  FOUND=1
  (cd backend && mvn -B -DskipTests package)
fi

if [ -f backend/package.json ]; then
  FOUND=1
  (cd backend && npm ci && npm run build --if-present)
fi

if [ -f frontend/package.json ]; then
  FOUND=1
  (cd frontend && npm ci && npm run build)
fi

if [ -f android/gradlew ]; then
  FOUND=1
  (cd android && chmod +x gradlew && ./gradlew assembleDebug)
fi

if [ "$FOUND" -eq 0 ]; then
  echo "No supported project detected."
  echo "Failing closed: build cannot be proven PASS."
  exit 1
fi

echo "BUILD PASSED"
