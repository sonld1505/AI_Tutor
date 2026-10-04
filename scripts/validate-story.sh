#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
if [[ -z "${STORY_FILE:-}" ]]; then
  echo 'STORY_FILE is required'
  echo 'DEFINITION OF READY: FAILED'
  exit 1
fi
if ! "$ROOT/scripts/factory-runtime.sh" dor --story-file "$STORY_FILE"; then
  echo 'DEFINITION OF READY: FAILED'
  exit 1
fi
