#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-}"

case "$ENVIRONMENT" in
  dev|stg|uat|production)
    ;;
  *)
    echo "Usage: $0 {dev|stg|uat|production}"
    exit 1
    ;;
esac

echo "Requested deployment: $ENVIRONMENT"

echo "Deployment implementation is intentionally disabled in Phase 1."
echo "Configure environment-specific deployment and credentials before enabling."
exit 1
