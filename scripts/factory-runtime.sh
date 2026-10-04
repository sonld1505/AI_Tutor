#!/usr/bin/env bash
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
source "$ROOT/factory/runtime/contract.env"
if [[ "${1:-}" == integration && -z "${FACTORY_INTEGRATION_PHASE:-}" ]]; then
  exec bash "$ROOT/scripts/factory-integration.sh" "$@"
fi
if [[ "${FACTORY_CANONICAL_REENTRY:-}" == "$FACTORY_IMAGE" && -f /.dockerenv && -f /tmp/factory-runtime-ready && -d /tmp/deps/yaml ]]; then
  [[ "$(/usr/local/bin/python -c 'import platform; print(platform.python_version())')" == "$FACTORY_PYTHON" ]] || { echo "BLOCK canonical Python version mismatch"; exit 1; }
  echo "Runtime: $FACTORY_IMAGE Python $FACTORY_PYTHON (canonical container reentry)"
  exec /usr/local/bin/python "$ROOT/factory/cli.py" "$@"
fi
[[ "$FACTORY_IMAGE" =~ ^python:3\.12@sha256:[a-f0-9]{64}$ ]] || { echo 'BLOCK invalid image contract'; exit 1; }
command -v docker >/dev/null || { echo 'BLOCK Docker unavailable'; exit 1; }
docker image inspect "$FACTORY_IMAGE" >/dev/null || docker pull "$FACTORY_IMAGE"
echo "Runtime: $FACTORY_IMAGE Python $FACTORY_PYTHON"
COMMON="$(git rev-parse --path-format=absolute --git-common-dir)"
GITDIR="$(git rev-parse --absolute-git-dir)"
MOUNTS=(--mount "type=bind,src=$ROOT,dst=$ROOT,readonly" --mount "type=bind,src=$COMMON,dst=$COMMON,readonly")
if [[ "$GITDIR" != "$COMMON" ]]; then MOUNTS+=(--mount "type=bind,src=$GITDIR,dst=$GITDIR,readonly"); fi
if [[ "${1:-}" == unit ]]; then
  RUNTIME_TEST_OUTPUT="$(mktemp -d /tmp/factory-runtime-test.XXXXXX)"
  trap 'RUNTIME_EXIT=$?; rm -rf "$RUNTIME_TEST_OUTPUT" || :; exit "$RUNTIME_EXIT"' EXIT
  bash "$ROOT/scripts/factory-runtime-test.sh" "$ROOT" "$RUNTIME_TEST_OUTPUT"
  MOUNTS+=(--mount "type=bind,src=$RUNTIME_TEST_OUTPUT/report.json,dst=$RUNTIME_TEST_OUTPUT/report.json,readonly" -e "FACTORY_RUNTIME_TEST_REPORT=$RUNTIME_TEST_OUTPUT/report.json")
fi
# No directory-wide writable repository mount. Existing exact targets only.
if [[ "${1:-}" == --write ]]; then
  shift
  STORY="${1:?story required}"; shift
  [[ "${1:-}" == orchestrate || "${1:-}" == write-evidence ]] || { echo "BLOCK write access only for sanctioned writers"; exit 1; }
  [[ "$STORY" =~ ^US-([0-9]+|FACTORY-[0-9]+)$ ]] || exit 1
  for target in "safe/stories/$STORY.yaml" "factory/state/$STORY.json" "factory/evidence/$STORY"; do
    [[ -e "$ROOT/$target" && ! -L "$ROOT/$target" ]] || { echo "BLOCK write target must already exist: $target"; exit 1; }
    [[ "$(realpath -e "$ROOT/$target")" == "$ROOT/$target" ]] || { echo "BLOCK symlink write target"; exit 1; }
    MOUNTS+=(--mount "type=bind,src=$ROOT/$target,dst=$ROOT/$target")
  done
fi
if [[ "${1:-}" == integration ]]; then
  FIXTURE_OUTPUT="${FACTORY_INTEGRATION_DIRECTORY:-$(mktemp -d /tmp/factory-integration-output.XXXXXX)}"
  [[ -d "$FIXTURE_OUTPUT" && ! -L "$FIXTURE_OUTPUT" ]] || { echo "BLOCK Integration directory invalid"; exit 1; }
  MOUNTS+=(--mount "type=bind,src=$FIXTURE_OUTPUT,dst=$FIXTURE_OUTPUT" -e "TMPDIR=$FIXTURE_OUTPUT")
fi
ARGS=("$@")
for ((i=0; i<${#ARGS[@]}; i++)); do
  if [[ "${ARGS[i]}" == --record-file || "${ARGS[i]}" == --story-file ]]; then
    INPUT="$(realpath -e "${ARGS[i+1]}")"
    ARGS[i+1]="$INPUT"
    if [[ "$INPUT" != "$ROOT/"* ]]; then
      MOUNTS+=(--mount "type=bind,src=$INPUT,dst=$INPUT,readonly")
    fi
  fi
done
docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges \
  --user "$(id -u):$(id -g)" --tmpfs /tmp:rw,exec,mode=1777 \
  "${MOUNTS[@]}" --workdir "$ROOT" -e PYTHONDONTWRITEBYTECODE=1 \
  -e FACTORY_INTEGRATION_PHASE -e FACTORY_INTEGRATION_DIRECTORY -e FACTORY_IMAGE="$FACTORY_IMAGE" -e FACTORY_GITHUB_TOKEN -e JENKINS_URL -e JENKINS_API_USER -e JENKINS_API_TOKEN -e FACTORY_PYTHON="$FACTORY_PYTHON" "$FACTORY_IMAGE" sh -eu -c '
    test "$(python -c "import platform; print(platform.python_version())")" = "$FACTORY_PYTHON"
    python -m pip install --disable-pip-version-check --no-cache-dir --no-deps --only-binary=:all: --require-hashes --target /tmp/deps -r factory/runtime/requirements.txt
    touch /tmp/factory-runtime-ready
    export FACTORY_CANONICAL_REENTRY="$FACTORY_IMAGE"
    export PYTHONPATH="/tmp/deps:$PWD/factory"
    export PATH="/tmp/deps/bin:$PATH"
    exec python factory/cli.py "$@"
  ' factory "${ARGS[@]}"
