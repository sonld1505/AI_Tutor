#!/usr/bin/env bash
# Host Bash coordinates canonical Python phases; Docker stays on the host.
set -euo pipefail
ROOT=$(git rev-parse --show-toplevel)
export FACTORY_INTEGRATION_DIRECTORY
FACTORY_INTEGRATION_DIRECTORY=$(mktemp -d /tmp/factory-integration-output.XXXXXX)
export FACTORY_INTEGRATION_PHASE=prepare
unset FACTORY_CANONICAL_REENTRY
"$ROOT/scripts/factory-runtime.sh" "$@"
mapfile -t stage_input < "$FACTORY_INTEGRATION_DIRECTORY/stage-input"
[[ ${#stage_input[@]} == 2 ]] || { echo 'BLOCK Integration handoff invalid'; exit 1; }
clone=${stage_input[0]}
expected=${stage_input[1]}
[[ $(realpath -e "$clone") == "$FACTORY_INTEGRATION_DIRECTORY/"*/repo ]] || { echo 'BLOCK Integration clone outside disposable directory'; exit 1; }
[[ $(git -C "$clone" rev-parse HEAD) == "$expected" ]] || { echo 'BLOCK Integration clone revision mismatch'; exit 1; }
mkdir -p "$clone/factory/logs"
stage_exit=0
(cd "$clone"; unset FACTORY_INTEGRATION_PHASE FACTORY_INTEGRATION_DIRECTORY
 BRANCH_NAME=feature/US-987654-devops timeout 1800 bash ./scripts/factory-jenkins.sh) > "$clone/factory/logs/integration-stage.log" 2>&1 || stage_exit=$?
printf '%s\n' "$stage_exit" > "$clone/factory/logs/integration-stage.exit"
export FACTORY_INTEGRATION_PHASE=complete
"$ROOT/scripts/factory-runtime.sh" "$@"
