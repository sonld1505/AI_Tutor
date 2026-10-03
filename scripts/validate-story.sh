#!/usr/bin/env bash
set -euo pipefail

STORY_FILE="${STORY_FILE:-}"

if [ -z "$STORY_FILE" ]; then
  echo "STORY_FILE is required."
  echo "Example: STORY_FILE=safe/stories/US-101.yaml ./scripts/validate-story.sh"
  exit 1
fi

if [ ! -f "$STORY_FILE" ]; then
  echo "Story not found: $STORY_FILE"
  exit 1
fi

echo "Validating story: $STORY_FILE"

required_patterns=(
  "^id:"
  "^title:"
  "^status:"
  "^acceptance_criteria:"
  "^test_scenarios:"
  "^definition_of_ready:"
)

for pattern in "${required_patterns[@]}"; do
  if ! grep -q "$pattern" "$STORY_FILE"; then
    echo "Missing required section matching: $pattern"
    exit 1
  fi
done

if grep -A20 "^definition_of_ready:" "$STORY_FILE" | grep -q "false"; then
  echo "DEFINITION OF READY: FAILED"
  exit 1
fi

echo "DEFINITION OF READY: PASSED"
