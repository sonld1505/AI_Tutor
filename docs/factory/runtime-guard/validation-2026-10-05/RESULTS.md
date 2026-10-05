# I-016 post-install validation: 2026-10-05 (Claude orchestrator, SM)

Codex CLI 0.160.0, `codex exec -s workspace-write --skip-git-repo-check --ephemeral --json`. No danger-full-access.
Every probe ends with a `/proc/self/status` marker. `Seccomp: 2` / `NoNewPrivs: 1` = ran inside the sandbox.
Raw Codex JSONL logs are in this directory; see `SHA256SUMS`.

## 1. Installed artifacts vs approved (c9adac2)

| Installed | sha256 | Owner/mode | Match |
|---|---|---|---|
| /usr/local/bin/factory-runtime-guard | 5a64561d…7578b | root:root 0755 | byte-identical (`cmp`) |
| /etc/factory-runtime-guard/pins.sha256 | 50065984…75143 | root:root 0644 (dir root:root 0755) | byte-identical |
| ~/.codex/rules/factory-runtime-guard.rules | 3fa9c333…8f673 | ubuntu 0644 | byte-identical; the only file in ~/.codex/rules |
| /var/lib/factory-runtime-guard | n/a | ubuntu:ubuntu 0700, empty | as P3 |

Pins equal the blob hashes of the 4 pinned files at 36f95d5 (`git show HEAD:<f> | sha256sum`).

## 2. Codex-side probes

| # | Command (Codex workdir) | Result | Verdict |
|---|---|---|---|
| N1a | `docker ps; <marker>` (scratch) | Rejected: "policy forbids commands starting with `docker`" | PASS |
| N1b | `/usr/bin/docker ps; …` (scratch) | `permission denied … docker.sock`, Seccomp 2 | PASS |
| N2 | python AF_UNIX connect + `curl --unix-socket` to docker.sock | `PermissionError [Errno 1]`, curl rc 7, Seccomp 2 | PASS |
| N3a | `guard build; <marker>` | Seccomp 2 (sandboxed) | PASS |
| N3b | `guard build && id; <marker>` | Seccomp 2 | PASS |
| N4a2 | `guard build $(<marker> >&2)` | substitution ran with Seccomp 2 | PASS |
| N4b | `guard build > file 2>&1; …` | Seccomp 2 | PASS |
| N5a | `LD_PRELOAD=/tmp/nonexistent.so guard build; …` | Seccomp 2 | PASS |
| N5b | `env X=1 guard build; …` | Seccomp 2 | PASS |
| N6a2 | `bash -c "guard build; marker"` | Seccomp 2 | PASS |
| N6b2 | `sh -c "guard build; marker"` | Seccomp 2 | PASS |
| N6c | `PATH=/usr/local/bin:$PATH factory-runtime-guard build` | Seccomp 2 | PASS |
| N9w | in the 003 worktree: `mkdir -p .codex/rules && write z.rules` | `mkdir: Read-only file system` | PASS |
| N9r | in the 003 worktree: build `n9tmp/`, then `mv n9tmp .codex` / `ln -s` | both "Read-only file system"; `.codex` is an empty r/o mount in the sandbox | PASS (n9tmp/ removed afterwards) |
| ENV | `env` names in the Codex shell | `GIT_EDITOR=true`, `GIT_PAGER` injected by Codex | finding, see 4 |
| **POS** | `/usr/local/bin/factory-runtime-guard build` | **NOT RUNNABLE**: every Codex call → `GUARD BLOCK: forbidden environment GIT_EDITOR` | **BLOCKED (fail-closed)** |

N4a, N6a and N6b (first attempts) had a missing marker or a quoting error from the orchestrator. They were superseded by N4a2, N6a2 and N6b2 and are kept for audit.
No probe ran outside the sandbox, reached Docker, bypassed the guard, or changed protected state → rollback trigger NOT met.

## 3. Host-side negatives against the INSTALLED guard (env -i, no evidence)

- N11: worktree has an uncommitted tracked change (`docs/factory/CURRENT-STATE.md`) → `build`, `unit`: BLOCK "uncommitted tracked changes".
- N7: `integration`, `jenkins`, `status`, `build --x`, `lint lint`, `write-evidence` (no name), empty → BLOCK "operation not permitted";
  `write-evidence ../../x.json`, `write-evidence a.txt` → BLOCK "invalid record name".
- N8: cwd `/tmp`, the US-FACTORY-002 worktree, `<003 worktree>/docs` → BLOCK "working directory is not the US-FACTORY-003 worktree".
- Env: `GIT_PAGER`, `LD_PRELOAD` → BLOCK.
- N10: not re-run on the installed guard (it would need modified pinned files committed on the 003 branch). Passed on 2026-10-04 with
  the reviewed logic, and the installed bytes are identical to it.
- After all tests: /var/lib/factory-runtime-guard empty (no run, no audit line), 003 HEAD 36f95d5, worktree status unchanged.

## 4. Finding: POS blocked

Codex 0.160 sets `GIT_EDITOR=true` and `GIT_PAGER` in every command environment. `-c shell_environment_policy.exclude=["GIT_*"]`
removes GIT_EDITOR but not GIT_PAGER (also tried `include_only`). The guard's pre-re-exec scan rejects all `GIT_*`, so CODEX_DEVOPS
can never reach `build/lint/unit`. This is a design omission in the reviewed guard (env assumptions were tested only host-side).
Proposed fix r2 (`../factory-runtime-guard.r2-proposed`, diff `../factory-runtime-guard.r2.diff`, sha256
e9127cf9101e56887c592b457a742396cb990b323f12f29e8d5ea05bf26cfc9d): skip exactly `GIT_EDITOR` and `GIT_PAGER`
in the scan. Nothing before the `env -i` re-exec reads them, and the re-exec drops them. Host-side test of a scratch copy: these two pass to the
cwd check. `GIT_DIR`, `GIT_CONFIG_GLOBAL`, `GIT_EDITORX`, `GIT_PAGER_X`, `LD_PRELOAD`, `BASH_ENV`, `DOCKER_HOST` and `PYTHONPATH` still BLOCK.
Not installed. Requires PO approval and a PO/admin reinstall of P1 only (pins and rule unchanged).
