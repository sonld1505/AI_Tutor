#!/usr/bin/env bash
set -euo pipefail

SHA="$(git rev-parse --short=12 HEAD)"

echo "Building immutable artifacts for commit: $SHA"

# Add real Docker/application packaging here.
# Example:
# docker build -t ai-tutor-backend:$SHA backend/
# docker build -t ai-tutor-frontend:$SHA frontend/

echo "Artifact build is not configured yet."
exit 1
