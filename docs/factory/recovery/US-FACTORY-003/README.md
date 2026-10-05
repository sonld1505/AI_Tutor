# US-FACTORY-003 recovery checkpoints (preserved 2026-10-05)

PO decision 2026-10-05: the uncommitted `docs/factory/CURRENT-STATE.md` in the US-FACTORY-003 implementation worktree
is **not** committed to `feature/US-FACTORY-003-devops` (PR #8 head stays `36f95d5`). It is preserved here under the human
management identity. Afterwards only that file is restored to its committed version in the implementation worktree.

## Files (verbatim copies, sha256)

| File | Source | sha256 |
|---|---|---|
| `CURRENT-STATE.checkpoint-2026-10-04T17.md` | Uncommitted working copy in `US-FACTORY-003-devops` (orchestrator reconciliation, ~17:00 UTC) | cfe5a444…1f78c |
| `CURRENT-STATE.prev-session-2026-10-04T16-48.md` | Earlier uncommitted version ("preserved outside Git"), found only in a temporary session scratchpad under `/tmp` | dd61c718…fc9f1 |
| `CURRENT-STATE.worktree-vs-36f95d5.diff` | `git diff` of the working copy against the committed version at `36f95d5` (blob sha256 130c4366…9454) | 96c6caea…d392 |
| `PR8-body-draft-2026-10-04.md` | PR #8 description draft, found only at `/tmp/US-FACTORY-003-pr-body.md` | 36dee092…e3807 |

Also preserved before any change (local only, not pushed): `refs/preserve/2026-10-05/US-FACTORY-003-devops` (a3ad8ea) in the
shared repository and `~/AI_Tutor-backups/2026-10-05/US-FACTORY-003-devops.{patch,files.tgz}`.

## Fact reconciliation (as of 2026-10-05)

| Fact in the checkpoints | Status | Durable record |
|---|---|---|
| Story US-FACTORY-003 IN_PROGRESS; contract = Lean model `8c544b8` + ADR-0001; R3-02 snapshot rule | Still current | Story YAML on feature branch; ADR-0001; RAID I-010 |
| Feature HEAD = origin = PR #8 head = `36f95d5`; author/identity `sonldfkr2911` | Still current | GitHub PR #8; RAID I-015 |
| PR #8 review 5405577037 APPROVED on `36f95d5` at 10:49:59Z (plus COMMENTED 5405575137, 10:49:35Z); historical only | Still current | RAID I-015 (`po_decision_2026_10_04`) |
| No AC08 records at `36f95d5`; all seven gates MISSING; first unfinished gate = build/lint/Unit Test by CODEX_DEVOPS | Still current | RAID I-015; this file |
| Jenkins #3 on `36f95d5`: Factory Validation stage PASS (107 tests OK, gitleaks/trivy/bandit, SECURITY SCAN PASSED, FACTORY CI PASS); overall FAILURE at backend Build (I-005) | Still current; supporting only, not an AC08 Jenkins record | Checkpoints here; local ignored logs `factory/logs/US-FACTORY-003/recovery/jenkins-3.log`, `jenkins-current.json`; Jenkins build #3 log |
| Host runs (build, lint, targeted 2 tests, security scan) | Still current; **not** CODEX_DEVOPS evidence | Ignored logs in `factory/logs/US-FACTORY-003/recovery/` |
| Round-4 review 0 Critical / 0 Major after one fix pass (inspection only) | Still current | `docs/factory/US-FACTORY-003-round4-review.md` (feature branch) |
| TS24 not run; single run reserved | Still current | RAID I-015 |
| Blocker I-016: guard design awaiting PO approval/install | **Superseded**: PO installed P1–P3/U1; N1–N9/N11 PASS; POS blocked by Codex-injected GIT_* vars; r2 approved by PO 2026-10-05 | `management/factory-v2-stabilization` e3f57f8: RAID I-016, FACTORY-RUNTIME-GUARD.md §10 |
| Jenkins bootstrap/admin password exposed and not rotated | **Superseded**: rotated, RAID I-018 CLOSED | `management/factory-v2-stabilization` c9adac2; DEVBOOK #21 |
| D-006 identity drift; management commits must use `sonld1505` | Still current | RAID I-017 (this branch, c5e1dc9) |
| Jenkins Secret Text `factory-github-token` imported, read-only GET 200 | Reported, not re-verified | Checkpoints here |
| No bot GitHub API write credential; `gh` unauthenticated | Reported, not re-verified | Checkpoints here |
| Helper `/tmp/factory-003-jenkins.py` (`status` read-only; `index`/`build` change Jenkins) | Exists in `/tmp` (volatile); not copied because it handles Jenkins auth | Checkpoints here |
| Management branch heads named in the checkpoints (c8c0415, 010f250, 5e446f7) | Outdated: current heads are on origin | `git log` of each branch |

Risk: the ignored logs under `factory/logs/` and the `/tmp` helper exist only on this single host (RAID R-005).
