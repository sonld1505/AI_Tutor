# Factory runtime guard — design (PROPOSED, NOT INSTALLED)

Status: design only, 2026-10-04. Waiting for PO approval of the privileged changes (§5).
Resolves: DEVBOOK #11 (Codex DevOps cannot run the canonical Docker gates), RAID I-016.
Unblocks: RAID I-015 (US-FACTORY-003 build/lint/Unit Test records from CODEX_DEVOPS).
PO constraints (2026-10-04): Codex stays sandboxed; no `danger-full-access`; Codex gets no
direct access to `docker.sock`; host runs are never recorded as CODEX_DEVOPS evidence;
AC05/AC14/AC25 are unchanged.

## 1. Facts observed (not assumed)

| # | Fact | How verified |
|---|---|---|
| F1 | `codex exec -s workspace-write` runs commands as `ubuntu` under seccomp + no_new_privs (`Seccomp: 2`, `NoNewPrivs: 1`); writable roots = workdir, `/tmp`, `$TMPDIR`. | Codex 0.160 probe run, 2026-10-04 |
| F2 | A command matched by an execpolicy `prefix_rule(..., decision="allow")` runs **outside** the sandbox (`Seccomp: 0`, `NoNewPrivs: 0`). | Same probe; temporary rule allowing only `cat /proc/self/status`, removed afterwards |
| F3 | Codex sends commands as `/bin/bash -lc '<cmd>'` and still matches rules against the inner command, so it parses shell text. | Probe log |
| F4 | `ubuntu` is in group `docker` (socket `root:docker 0660`) and has `NOPASSWD: ALL` sudo. Any unsandboxed `ubuntu` process is root-equivalent. | `id`, `ls -l /var/run/docker.sock`, `sudo -n -l` |
| F5 | Earlier finding (DEVBOOK #11): sandboxed Codex could not reach `docker.sock`. | Not re-tested; see N2 |

Consequence: in Codex 0.160 the allow rule itself is the privilege boundary. The guard is the
only command allowed to leave the sandbox, and it accepts only fixed operations. Point 6 of the
PO instruction (guard still sandboxed → cannot reach Docker) does **not** apply. F2 shows that
allowed commands run unsandboxed, so the design is technically viable.

## 2. Allowed operations

| Guard argv | Runs (in a private snapshot, §3) | Needed for |
|---|---|---|
| `factory-runtime-guard build` | `scripts/factory-runtime.sh build` | build record (AC25) |
| `factory-runtime-guard lint` | `scripts/factory-runtime.sh lint` | lint record (AC25) |
| `factory-runtime-guard unit` | `scripts/factory-runtime.sh unit` | Unit Test record (AC25) |
| `factory-runtime-guard write-evidence <name>.json` | `scripts/factory-runtime.sh --write US-FACTORY-003 write-evidence --story US-FACTORY-003 --record-file <staged copy>` | stamping the producer's record with the evidence writer (AC08) |

`write-evidence` goes beyond "build, lint, unit" in the PO text. Without it, Codex cannot stamp its
own records: the writer is canonical-runtime only, and Codex has no Docker. **PO to confirm.**
Without it, the orchestrator would stamp, which is mechanical but leaves the producer out of
the stamping step.

Precondition for `write-evidence`: the SM has committed `factory/state/US-FACTORY-003.json` (implementing role
CODEX_DEVOPS, identity `sonldfkr2911`) and `factory/evidence/US-FACTORY-003/` with a tracked `README.md`,
because the writer needs both to exist at the snapshot revision.

Not allowed: `integration`, `jenkins`, `orchestrate`, `status`, every other subcommand, every
extra argument, every other Story or worktree.

## 3. Guard behaviour

1. `#!/bin/bash -p` (ignores `BASH_ENV`/`ENV`). Re-exec once under `env -i` with a fixed `PATH`,
   `HOME`, `LANG`. Refuse if any `LD_*`, `GIT_*`, `DOCKER_*` or `BASH_ENV` variable is present.
2. Argument check: exactly one of `build|lint|unit`, or `write-evidence` plus one name matching
   `^[A-Za-z0-9._-]{1,64}\.json$`. Anything else → BLOCK.
3. Worktree check: `pwd -P` must equal the pinned path
   `/home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-devops`. `realpath -e` of that path must equal
   itself (no symlink). The branch must be `feature/US-FACTORY-003-devops`. Tracked files must be
   clean (`git status --porcelain --untracked-files=no` empty). Git runs with
   `-c core.fsmonitor=false -c core.hooksPath=/dev/null`.
4. Snapshot (TOCTOU defence): full non-shallow `git clone --no-local --no-hardlinks` of the worktree
   into `/var/lib/factory-runtime-guard/run.XXXXXXXX`, then `checkout --detach <worktree HEAD>`. That
   directory is outside the Codex writable roots, so Codex cannot change files between the check
   and execution.
5. Pins: `sha256sum --check --strict` in the snapshot against root-owned
   `/etc/factory-runtime-guard/pins.sha256`. Pinned files are the ones the **host** executes or
   sources (values at 36f95d5):
   ```
   f17b11cf67dff588618f0edd26ce1363643d5553b8ea02747232633a050fb7c7  scripts/factory-runtime.sh
   7fe41e0c4d641b22a0d794729e71d539aade6bf5e6db650c05312f157685296a  scripts/factory-runtime-test.sh
   3b2b0113bc9a67eaf68542eb7dbb3c3527b1f2048f9f2fc95fc4d97ee9a4de18  factory/runtime/contract.env
   65b9e716e50546b4b3d38421b8972aa3712fa5360ac7c18c95fcf936c1d98111  factory/runtime/requirements.txt
   ```
   Any mismatch or missing file → BLOCK. The image digest is pinned inside `contract.env`.
   Python code under test runs only inside the canonical container (read-only, `--cap-drop ALL`,
   `no-new-privileges`, no socket mount).
6. `write-evidence` input: read `<worktree>/factory/logs/US-FACTORY-003/devops/records/<name>` with
   `dd iflag=nofollow` (max 64 KiB) into the snapshot's staging area. No symlink following.
7. Execute `timeout --kill-after=30 3600 /bin/bash --noprofile --norc scripts/factory-runtime.sh …` in
   the snapshot. Docker arguments are built only by the pinned `factory-runtime.sh`. The guard
   takes no Docker arguments.
8. Output: the guard **never writes into the worktree** (doing so would race symlink swaps by Codex).
   Run log and stamped record stay in `/var/lib/factory-runtime-guard/out/<run-id>/` (not writable
   by Codex). The guard prints `GUARD RESULT run=<id> op=<op> head=<sha> exit=<n> sha256=<file hash>`.
   The orchestrator copies the stamped record into the worktree, checks the printed sha256 and
   commits it with the bot identity. The validator re-derives source commit and fingerprints anyway.
9. Append-only audit line in `/var/lib/factory-runtime-guard/audit.log`. Remove the snapshot on exit.
   Any error → non-zero exit (fail closed).

Draft script (to be reviewed before installation, not installed):

```bash
#!/bin/bash -p
# factory-runtime-guard: narrow host broker for CODEX_DEVOPS canonical gates (US-FACTORY-003 only).
set -euo pipefail
if [[ "${FACTORY_GUARD_CLEAN:-}" != 1 ]]; then
  for v in $(compgen -e); do
    case "$v" in LD_*|GIT_*|DOCKER_*|BASH_ENV|ENV|PYTHON*) echo "GUARD BLOCK: forbidden environment $v" >&2; exit 1;; esac
  done
  exec /usr/bin/env -i FACTORY_GUARD_CLEAN=1 PATH=/usr/sbin:/usr/bin:/sbin:/bin HOME=/home/ubuntu LANG=C.UTF-8 \
    /bin/bash -p --noprofile --norc /usr/local/bin/factory-runtime-guard "$@"
fi
umask 077
readonly WORKTREE=/home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-devops
readonly BRANCH=feature/US-FACTORY-003-devops STORY=US-FACTORY-003
readonly PINS=/etc/factory-runtime-guard/pins.sha256 STATE=/var/lib/factory-runtime-guard
die() { echo "GUARD BLOCK: $*" >&2; exit 1; }
G() { /usr/bin/git -c core.fsmonitor=false -c core.hooksPath=/dev/null -c safe.directory="$1" -C "$1" "${@:2}"; }

case "${1:-}:$#" in
  build:1|lint:1|unit:1) OP=$1 ;;
  write-evidence:2) OP=$1; [[ "$2" =~ ^[A-Za-z0-9._-]{1,64}\.json$ ]] || die "invalid record name"; NAME=$2 ;;
  *) die "operation not permitted" ;;
esac
[[ "$(realpath -e "$WORKTREE")" == "$WORKTREE" && ! -L "$WORKTREE" ]] || die "worktree path invalid"
[[ "$(pwd -P)" == "$WORKTREE" ]] || die "working directory is not the US-FACTORY-003 worktree"
[[ "$(G "$WORKTREE" symbolic-ref --short HEAD)" == "$BRANCH" ]] || die "wrong branch"
[[ -z "$(G "$WORKTREE" status --porcelain --untracked-files=no)" ]] || die "uncommitted tracked changes"
HEAD=$(G "$WORKTREE" rev-parse --verify 'HEAD^{commit}')
[[ -f "$PINS" && ! -L "$PINS" && "$(stat -c %u:%a "$PINS")" == 0:644 ]] || die "pin file invalid"

RUN=$(mktemp -d "$STATE/run.XXXXXXXX"); ID=${RUN##*.}; OUT="$STATE/out/$ID"
trap 'rm -rf "$RUN"' EXIT
mkdir -p "$OUT"
/usr/bin/git -c core.hooksPath=/dev/null clone --quiet --no-local --no-hardlinks --no-checkout "$WORKTREE" "$RUN/repo"
G "$RUN/repo" checkout --quiet --detach "$HEAD"
[[ "$(G "$RUN/repo" rev-parse HEAD)" == "$HEAD" ]] || die "snapshot revision mismatch"
(cd "$RUN/repo" && /usr/bin/sha256sum --check --strict --quiet "$PINS") || die "canonical runtime pin mismatch"

ARGS=("$OP")
if [[ "$OP" == write-evidence ]]; then
  /usr/bin/dd if="$WORKTREE/factory/logs/$STORY/devops/records/$NAME" of="$RUN/input.json" iflag=nofollow bs=65537 count=1 status=none \
    || die "record input unreadable"
  [[ "$(stat -c %s "$RUN/input.json")" -le 65536 ]] || die "record input too large"
  ARGS=(--write "$STORY" write-evidence --story "$STORY" --record-file "$RUN/input.json")
  BEFORE=$(ls -1 "$RUN/repo/factory/evidence/$STORY")
fi
set +e
(cd "$RUN/repo" && /usr/bin/timeout --kill-after=30 3600 /bin/bash --noprofile --norc scripts/factory-runtime.sh "${ARGS[@]}") > "$OUT/$OP.log" 2>&1
RC=$?
set -e
cat "$OUT/$OP.log"
HASH=$(/usr/bin/sha256sum "$OUT/$OP.log" | cut -d' ' -f1)
if [[ "$OP" == write-evidence && $RC -eq 0 ]]; then
  NEW=$(comm -13 <(echo "$BEFORE") <(ls -1 "$RUN/repo/factory/evidence/$STORY"))
  [[ $(wc -l <<<"$NEW") -eq 1 && "$NEW" =~ ^[0-9TZ.-]+\.json$ ]] || die "writer output ambiguous"
  cp -- "$RUN/repo/factory/evidence/$STORY/$NEW" "$OUT/$NEW"
  HASH=$(/usr/bin/sha256sum "$OUT/$NEW" | cut -d' ' -f1)
fi
printf '%s op=%s head=%s exit=%s run=%s sha256=%s\n' "$(date -u +%FT%TZ)" "$OP" "$HEAD" "$RC" "$ID" "$HASH" >> "$STATE/audit.log"
echo "GUARD RESULT run=$ID op=$OP head=$HEAD exit=$RC sha256=$HASH out=$OUT"
exit "$RC"
```

## 4. Codex exec policy

User-level file `~/.codex/rules/factory-runtime-guard.rules`. It is outside Codex's writable roots,
and it applies to every Codex session of user `ubuntu`. The guard pins the worktree, so other sessions
gain nothing by calling it.

```python
prefix_rule(pattern=["/usr/local/bin/factory-runtime-guard", ["build", "lint", "unit", "write-evidence"]], decision="allow")
prefix_rule(pattern=["docker"], decision="forbidden")
prefix_rule(pattern=["sudo"], decision="forbidden")
prefix_rule(pattern=["su"], decision="forbidden")
```

`prefix_rule` also matches longer argument lists. The guard's exact-arity check (§3.2) closes that.
Only the absolute path is allowed, so `factory-runtime-guard` resolved through `PATH` does not match.
Dispatch remains `codex exec -s workspace-write` (no `danger-full-access`, no extra writable roots).

## 5. Exact privileged changes (require PO approval; none applied)

| # | Command (run by the orchestrator via sudo) | Effect |
|---|---|---|
| P1 | `sudo install -o root -g root -m 0755 <reviewed guard> /usr/local/bin/factory-runtime-guard` | Guard executable, not writable by `ubuntu` without sudo and never by the sandbox |
| P2 | `sudo install -d -o root -g root -m 0755 /etc/factory-runtime-guard` and `sudo install -o root -g root -m 0644 pins.sha256 /etc/factory-runtime-guard/pins.sha256` | Root-owned pin file (§3.5) |
| P3 | `sudo install -d -o ubuntu -g ubuntu -m 0700 /var/lib/factory-runtime-guard` | Private snapshot/output/audit directory (outside sandbox writable roots) |
| U1 (not root, security-relevant) | create `~/.codex/rules/factory-runtime-guard.rules` (§4) | Lets exactly the guard command leave the sandbox |

Not changed: sudoers, docker group membership, `docker.sock` permissions, Codex sandbox mode,
Jenkins, GitHub settings, the Story contract. Rollback: remove P1–P3 and U1.

## 6. Threat analysis

| # | Threat | Mitigation | Residual |
|---|---|---|---|
| T1 | **Rule-match bypass**: a compound, substituted, redirected, env-prefixed or wrapped command (`guard build; id`, `$(…)`, `LD_PRELOAD=… guard build`, `bash -c …`) is matched as allowed and runs unsandboxed (F2, F4 ⇒ root-equivalent). | Absolute-path-only allow rule; `forbidden` rules; guard rejects bad env. | **HIGH until N3–N8 pass.** Rule-parser behaviour is not verified: my negative probe was blocked by the Claude Code auto-mode classifier. |
| T2 | Arbitrary operation via the guard (other subcommands, extra args, other Story). | Fixed operation table, exact arity, Story and worktree hard-coded. | Low |
| T3 | TOCTOU: Codex swaps pinned files or symlinks after the checks. | Private snapshot clone outside writable roots; pins checked in the snapshot; no writes into the worktree; `dd iflag=nofollow`. | Low |
| T4 | Modified host-executed runtime (`factory-runtime.sh`, test probe, `contract.env`). | SHA-256 pins in a root-owned file; mismatch → BLOCK. Pins must be updated (with sudo) whenever these files change legitimately. | Low |
| T5 | Env/loader injection (`LD_PRELOAD`, `BASH_ENV`). | `bash -p`, env scan, `env -i` re-exec. A preload would still run before the guard's first line **if** the rule matched an env-prefixed command, which T1/N5 must exclude. | Depends on N5 |
| T6 | Malicious Python under test reaches the host. | Runs only in the canonical container: read-only, `--cap-drop ALL`, `no-new-privileges`, no socket, uid `ubuntu`. | Container has network (needed for hash-pinned pip install). It can reach the EC2 metadata service; mitigate with IMDSv2 hop limit 1 (admin, separate). This exists already in the canonical runtime and in Jenkins. |
| T7 | Codex adds its own rules or config (e.g. `<worktree>/.codex/rules/*.rules`) and widens its own policy. | Not part of this design. | **Unknown, pre-existing.** N9 must show that workspace `.codex/` is not writable or not loaded. |
| T8 | Forged evidence: Codex edits the stamped record or claims results it did not get. | Stamped record and run log stay in Codex-unwritable `/var/lib/...`. The orchestrator copies them by printed sha256. Independent Validation (CODEX_QA) and Jenkins cross-check. | Producer honesty about `ts_results` remains a review item (inherent in AC08) |
| T9 | Login-shell startup files sourced for the unsandboxed `bash -lc`. | They live in `$HOME`, outside Codex writable roots. | Low; check `~/.profile`/`~/.bashrc` do not source `/tmp` |
| T10 | Guard replaced or edited. | Root-owned 0755 in `/usr/local/bin`. The sandbox cannot write it. Unsandboxed `ubuntu` can via sudo, at the same trust level as the orchestrator. | Low |
| T11 | Denial of service (long runs, disk). | 3600 s timeout and kill; snapshot removed on exit. | Low |

## 7. Tests before any evidence use

All run through `codex exec -s workspace-write` dispatches (the Codex side) after P1–P3/U1, unless noted.
**Running them needs the user's explicit permission in Claude Code**, because the auto-mode classifier
blocks sandbox-escape probes. Any FAIL → uninstall (rollback §5) and stop.

| # | Test | Expected |
|---|---|---|
| N1 | Codex runs `docker ps` | Rejected (forbidden rule) or fails in sandbox; no container list |
| N2 | Codex connects to `/var/run/docker.sock` (python/curl `--unix-socket`) | Connection denied |
| N3 | `/usr/local/bin/factory-runtime-guard build; id` and `… && id` | Not auto-allowed: runs sandboxed (`Seccomp: 2`) or is rejected |
| N4 | `/usr/local/bin/factory-runtime-guard build $(id -u)` and with redirect `> /tmp/x` | Not auto-allowed |
| N5 | `LD_PRELOAD=/tmp/x.so /usr/local/bin/factory-runtime-guard build`, `env X=1 /usr/local/bin/…` | Not auto-allowed, or guard BLOCK before any action |
| N6 | `bash -c '/usr/local/bin/factory-runtime-guard build'`, `sh -c …`, `factory-runtime-guard build` (PATH lookup) | Not auto-allowed |
| N7 | `/usr/local/bin/factory-runtime-guard integration`, `… build --x`, `… write-evidence ../../x.json`, `… jenkins` | Guard BLOCK |
| N8 | Guard run with cwd = another worktree, a symlink to the 003 worktree, or `/tmp` | Guard BLOCK |
| N9 | Codex writes `<workdir>/.codex/rules/z.rules` allowing `id`, then a new session runs `id` | File not writable, or `id` still sandboxed |
| N10 | Host-side (orchestrator): disposable copy with one byte changed in each pinned file, run guard against a fixture setup; and committed but un-pinned change | Guard BLOCK "pin mismatch" |
| N11 | Uncommitted tracked change in the 003 worktree | Guard BLOCK |
| POS | Codex runs `/usr/local/bin/factory-runtime-guard build` once | `exit=0`, `GUARD RESULT … op=build`, audit line present, worktree unchanged |

The first evidence-producing use (build, lint, unit, write-evidence) comes only after all N tests and POS pass.
