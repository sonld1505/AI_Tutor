#!/usr/bin/env bash
# G-12: full-history secrets, tree security, and hash-locked Python SAST.
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
cd "$ROOT"
source "$ROOT/scripts/security/scanners.env"
source "$ROOT/factory/runtime/contract.env"
fail() { echo "SECURITY SCAN FAILED: $*" >&2; exit 1; }
for image in "${GITLEAKS_IMAGE:-}" "${TRIVY_IMAGE:-}"; do
    [[ "$image" =~ ^[a-zA-Z0-9./_-]+:v?[0-9]+\.[0-9]+\.[0-9]+@sha256:[a-f0-9]{64}$ ]] || fail 'missing or unpinned scanner image'
done
[[ "${FACTORY_IMAGE:-}" =~ ^python:3\.12@sha256:[a-f0-9]{64}$ ]] || fail 'invalid canonical image'
command -v docker >/dev/null || fail 'Docker unavailable'
mkdir -p "$ROOT/factory/logs"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
# A clone makes linked-worktree Git metadata self-contained and scans full ancestry.
[[ $(git rev-parse --is-shallow-repository) == false ]] || fail 'full Git history required'
git clone --no-local --quiet "$ROOT" "$TMP/repo"
for image in "$GITLEAKS_IMAGE" "$TRIVY_IMAGE" "$FACTORY_IMAGE"; do
    docker pull "$image" >/dev/null
    digests=$(docker image inspect --format '{{join .RepoDigests "\n"}}' "$image")
    expected="${image%%:*}@${image##*@}"
    [[ $'\n'"$digests"$'\n' == *$'\n'"$expected"$'\n'* ]] || fail 'image digest mismatch'
done
# JSON secrets are redacted; report directory is the only writable repository mount.
docker run --rm --user "$(id -u):$(id -g)" --read-only --cap-drop ALL --security-opt no-new-privileges \
    --tmpfs /tmp:rw,nosuid,nodev -v "$TMP/repo:/repo:ro" -v "$ROOT/factory/logs:/reports:rw" \
    "$GITLEAKS_IMAGE" git /repo --redact --no-banner --exit-code 1 --report-format json --report-path /reports/security-gitleaks.json
docker run --rm --user "$(id -u):$(id -g)" --read-only --cap-drop ALL --security-opt no-new-privileges \
    --tmpfs /tmp:rw,nosuid,nodev -e TRIVY_CACHE_DIR=/tmp/trivy -v "$ROOT:/repo:ro" -v "$ROOT/factory/logs:/reports:rw" \
    "$TRIVY_IMAGE" fs --scanners vuln,misconfig,secret --severity HIGH,CRITICAL --exit-code 1 --no-progress \
    --format json --output /reports/security-trivy.json /repo
docker run --rm --user "$(id -u):$(id -g)" --read-only --cap-drop ALL --security-opt no-new-privileges \
    --tmpfs /tmp:rw,nosuid,nodev,exec -e PYTHONDONTWRITEBYTECODE=1 -v "$ROOT:/repo:ro" -v "$ROOT/factory/logs:/reports:rw" \
    -w /repo "$FACTORY_IMAGE" bash -euo pipefail -c \
    'python -m venv /tmp/security-venv
/tmp/security-venv/bin/python -m pip install --disable-pip-version-check --no-cache-dir --no-deps --only-binary=:all: --require-hashes -r factory/runtime/security-requirements.txt
/tmp/security-venv/bin/python -m bandit -r factory scripts -ll -ii -f json -o /reports/security-bandit.json'
echo 'SECURITY SCAN PASSED'
