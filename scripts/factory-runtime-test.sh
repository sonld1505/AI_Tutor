#!/usr/bin/env bash
# Real Docker mount probes on a disposable MOCK repo. No real management reads.
set -euo pipefail
SOURCE_ROOT="${1:?source root required}"
OUTPUT="${2:?disposable output directory required}"
DOCKER_EXECUTABLE="$(command -v docker)"
FIXTURE="$OUTPUT/repo"
mkdir -p "$FIXTURE/scripts" "$FIXTURE/factory/runtime" "$FIXTURE/safe/stories" "$FIXTURE/factory/state" "$FIXTURE/factory/evidence/US-999" "$OUTPUT/bin"
cp "$SOURCE_ROOT/scripts/factory-runtime.sh" "$FIXTURE/scripts/"
cp "$SOURCE_ROOT/factory/runtime/contract.env" "$FIXTURE/factory/runtime/"
printf 'id: US-999\nstatus: READY\n' > "$FIXTURE/safe/stories/US-999.yaml"
printf '{}\n' > "$FIXTURE/factory/state/US-999.json"
printf 'MOCK readable implementation\n' > "$FIXTURE/factory/source.txt"
printf 'MOCK outside writable targets\n' > "$FIXTURE/elsewhere.txt"
git -C "$FIXTURE" init -q
cat > "$OUTPUT/bin/docker" <<'WRAPPER'
#!/usr/bin/env bash
# MOCK workload only; all Docker security flags and mounts are real and unchanged.
set -euo pipefail
if [[ "${1:-}" != run ]]; then exec "$FACTORY_TEST_DOCKER" "$@"; fi
arguments=("$@")
for ((index=0; index<${#arguments[@]}; index++)); do
  if [[ "${arguments[index]}" == "$FACTORY_TEST_IMAGE" ]]; then
    exec "$FACTORY_TEST_DOCKER" "${arguments[@]:0:index+1}" sh "$FACTORY_TEST_PROBE"
  fi
done
echo 'BLOCK runtime probe image missing' >&2
exit 1
WRAPPER
chmod +x "$OUTPUT/bin/docker"
cat > "$FIXTURE/probe.sh" <<'PROBE'
set -eu
test -r safe/stories/US-999.yaml
test -r factory/state/US-999.json
test -r factory/source.txt
test -r scripts/factory-runtime.sh
test -r factory/runtime/contract.env
deny() {
  if (printf 'MOCK forbidden\n' > "$1") 2>/dev/null; then
    echo "BLOCK unexpected write: $1"
    exit 1
  fi
}
deny elsewhere.txt
deny factory/source.txt
deny scripts/factory-runtime.sh
deny factory/runtime/contract.env
deny factory/workflow.yaml
deny .git/config
deny .git/readonly-probe
deny safe/stories/US-998.yaml
deny factory/state/US-998.json
deny factory/evidence/outside.json
if test -e factory/evidence/US-999/write-mode.md; then
  printf 'id: US-999\nstatus: IN_PROGRESS\n' > safe/stories/US-999.yaml
  printf '{"status":"IN_PROGRESS"}\n' > factory/state/US-999.json
  printf 'MOCK host ownership probe\n' > factory/evidence/US-999/created.md
  echo 'MOCK WRITE TARGETS PASS'
else
  deny safe/stories/US-999.yaml
  deny factory/state/US-999.json
  deny factory/evidence/US-999/created.md
  echo 'MOCK READONLY PASS'
fi
PROBE
source "$FIXTURE/factory/runtime/contract.env"
export FACTORY_TEST_DOCKER="$DOCKER_EXECUTABLE" FACTORY_TEST_IMAGE="$FACTORY_IMAGE" FACTORY_TEST_PROBE="$FIXTURE/probe.sh"
export FACTORY_CANONICAL_REENTRY=''
export PATH="$OUTPUT/bin:$PATH"
cd "$FIXTURE"
bash scripts/factory-runtime.sh build > "$OUTPUT/readonly.txt"
grep -Fxq 'MOCK READONLY PASS' "$OUTPUT/readonly.txt"
printf 'MOCK write mode\n' > factory/evidence/US-999/write-mode.md
# The helper itself parses --write and constructs the exact sanctioned mounts.
bash scripts/factory-runtime.sh --write US-999 orchestrate --story US-999 --action transition --from READY --to IN_PROGRESS > "$OUTPUT/write.txt"
grep -Fxq 'MOCK WRITE TARGETS PASS' "$OUTPUT/write.txt"
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"
for target in safe/stories/US-999.yaml factory/state/US-999.json factory/evidence/US-999/created.md; do
  [[ "$(stat -c '%u:%g' "$target")" == "$HOST_UID:$HOST_GID" ]]
done
[[ "$(cat elsewhere.txt)" == 'MOCK outside writable targets' ]]
printf '{"readonly":"PASS","write_targets":"PASS","outside_targets":"PASS","host_uid":%s,"host_gid":%s,"owned_files":3}\n' "$HOST_UID" "$HOST_GID" > "$OUTPUT/report.json"
