# Factory current state

Updated: 2026-10-04 (post-approval hard-stop; see HARD-STOP section). Previous: 10:45 UTC. Resumed by user instruction. Step 1 (read Jenkins #3)
and step 3 (update PR description/status) are DONE. **Now STOPPED at step 4: waiting for
one human action to create the bot-authored PR** (bot has no GitHub API write access).
Nothing else is in flight; no background jobs.

## Active work

- Story: **US-FACTORY-003**; role: DevOps; Story YAML remains **IN_PROGRESS**.
- Worktree: `/home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-devops`.
- Branch: `feature/US-FACTORY-003-devops`.
- HEAD / pushed candidate: `36f95d5a25bacf584ed7a27835749c7bc13125cc`.
- Candidate commit: `fix(factory): complete US-FACTORY-003 lean round 4 recovery`.
- Git was clean immediately before this status update. This file is now a local
  uncommitted update; it has not been pushed. No other implementation edits are pending.
- Bot Git author and SSH identity verified: `sonldfkr2911`; human PO/reviewer:
  `sonld1505`. Do not author implementation or its PR as the human PO.
- **US-FACTORY-002 was not modified/reset/cleaned/stashed/rebased.** Its separate
  unfinished worktree remains out of scope.

## Completed

Recovery verified Git/worktrees, uncommitted implementation, Story amendment,
ADR-0001, RAID/DEVBOOK/CHANGELOG, prior logs and Jenkins. Original feature HEAD was
8c544b8; remote previously held 233b1e9. Management migration commits 9648c0f and
5e446f7 exist; actual branch spelling is `management/factory-v2-stabilization`,
in worktree `US-FACTORY-004-MGMT`. Do not merge/recreate the old gate workflow.

Round-4 implementation is committed and pushed. It includes Lean Validation;
non-authorising out-of-order history with integrity enforcement; DONE completion
snapshots and arrival-only remote verification; pre-DONE BLOCKED guards; the
credential-bound fail-fast Factory CI composite; pinned gitleaks/trivy/bandit;
and regressions/docs. Backend gates retain fail-closed behaviour.

Independent review found two Major issues: historical offline DONE still required
an archive adapter, and integration claimed full stage coverage while running only
the validator. **One fix pass and one re-review are complete: 0 Critical / 0 Major
remaining.** Do not dispatch another review round. Review is code inspection,
not an AC08 Validation PASS record or a Story DONE claim.

Recovery SA approved two canonical integration phases coordinated by host Bash.
Prepare checks the real review and exercises the disposable components. Host Bash
runs the actual `factory-jenkins.sh` composite on the same clone. Complete verifies
source revision, clone containment, unchanged HEAD and actual stage exit before
continuing. No Docker socket in containers or host Python fallback. Decision is
recorded in ADR-0001's recovery addendum.

## Verified execution evidence

- Canonical build: exit 0. Final canonical lint: exit 0, all checks passed.
- Final affected targeted run: **exit 0; 2 tests; 96.828 seconds; OK**:
  Lean DONE flow with external historical artifacts and no remote adapters;
  canonical runtime exit propagation across all subcommands.
- Three other focused regressions passed in the preceding four-test run:
  integration coordinator lifecycle, CI composite order/fail-fast, pinned scanner
  failure behaviour. That run's Lean test had an assertion error; only the affected
  BLOCK-exception assertions were corrected and the final run passed. Do not call
  the earlier four-test run PASS overall.
- Real local security scan: **PASS**, all gitleaks/trivy/bandit steps executed.
  The earlier noexec failure was fixed using venv Python `-m pip` / `-m bandit`.
  Committed Bandit annotations explain HTTPS validation and rejected MOCK paths.
- Earlier broad targeted attempt timed out (exit 124); it is not PASS evidence.
- **No expensive full suite was run locally.** Reuse these valid results unless
  their inputs change; full suite ran once in Jenkins #3: 107 tests OK.

## Jenkins result (TS25 real evidence) — build #3 FINISHED

- URL: `http://localhost:8080/job/AI_Tutor/job/feature%252FUS-FACTORY-003-devops/3/`;
  checked out exactly **36f95d5a25bacf584ed7a27835749c7bc13125cc**; ran 10:18–10:38 UTC.
- **Factory Validation stage: PASS.** Validator PASS; canonical build PASS; lint PASS;
  full Factory unit suite **Ran 107 tests in 1139.541s, OK**. Per-TS: TS01–TS23, TS26–TS28
  all `failed=0 not-executed=0` (counts sum to 107). TS24 (real integration, after PO
  approval) and TS25 (this Jenkins build) are by contract not in the automated suite.
  Security: gitleaks "no leaks found", trivy and bandit executed (bandit only B108 nosec
  warnings on test_factory.py:672), `SECURITY SCAN PASSED`, `FACTORY CI PASS`.
- **Overall build result: FAILURE.** Backend `Build` stage failed closed ("No supported
  project detected", I-005); later stages skipped; `PIPELINE FAILED — DEPLOYMENT BLOCKED`.
  Per ADR-0001 D6 this equals Factory CI PASS, **not** deployment permission.
- No new issue found; no SA escalation needed. Log copy:
  `factory/logs/US-FACTORY-003/recovery/jenkins-3.log` + `jenkins-current.json`.
- No AC08 gate records or DoD flags were written in this session.

## Credentials and PR

Jenkins Secret Text `factory-github-token` was imported under existing human
approval, verified by source-value match and a read-only repository GET (HTTP 200).
Both temporary token copies were securely removed; one-time import script removed.
Use it only for the approved read-only Factory GitHub operations. Never print it.
A prior broad journal read exposed a Jenkins bootstrap password in tool output;
no rotation was performed. Keep future credential checks narrowly scoped and never
dump service journals or credential files.

Bot SSH push succeeded. `gh` is not authenticated; no bot API write credential is
configured. Last public PR lookup returned an empty list; no PR was created by
this session. SSH access cannot create a PR through the API. Prepared description:
`/tmp/US-FACTORY-003-pr-body.md` (updated 10:45 UTC with actual CI evidence).

## HARD-STOP 2026-10-04 (after PO approval of PR #8) — waiting for PO decision

Verified through the real GitHub REST API (public, unauthenticated, read-only):
- PR #8 open, not draft, not merged, `feature/US-FACTORY-003-devops` -> `develop`, author `sonldfkr2911`.
- Review 5405577037: `sonld1505` **APPROVED**, commit_id `36f95d5a25bacf584ed7a27835749c7bc13125cc`,
  2026-10-04T10:49:59Z (an earlier COMMENTED review 5405575137 on the same commit, 10:49:35Z, from the same reviewer).
  No CHANGES_REQUESTED. All 5 PR commits are authored and committed by `sonldfkr2911`.
- PR head = `refs/pull/8/head` = origin branch = local HEAD = 36f95d5. Candidate unchanged.

**TS24 NOT run.** 36f95d5 has no `factory/evidence/US-FACTORY-003/` (no AC08 build, lint, Unit
Test, Validation or Jenkins record), and the Story is IN_PROGRESS, not QA. workflow.yaml:
Code Review needs Unit Test, Validation and Jenkins; Integration Test needs Unit Test and Code
Review, in QA. `factory/integration.py:149` would BLOCK immediately, so the single run would be
spent for nothing. RAID I-015, DEVBOOK #18 and CHANGELOG are recorded (uncommitted) in worktree
US-FACTORY-004-MGMT (`management/factory-v2-stabilization`).

DoD: NOT met (Validation, Unit/build/lint records, Jenkins record, valid Code Review, Integration Test
are missing; Story not in QA). Next: the PO picks a recovery path (RAID I-015). Do not merge or deploy.

## Recovery status (PO option (a), later decisions 2026-10-04)

- Management records committed and pushed by the bot on `management/factory-v2-stabilization`:
  1d0f261 (I-015, DEVBOOK #18), 12f48cb (pause), 010f250 (runtime-guard design, I-016, DEVBOOK #19).
- No gate record has been created. PR #8 head is still 36f95d5; the approval on it is historical only.
  Story is IN_PROGRESS.
- Blocked on I-016: CODEX_DEVOPS cannot run the canonical Docker gates from its sandbox. PO chose a narrow
  root-owned guard. Design and exact privileged changes: `docs/factory/FACTORY-RUNTIME-GUARD.md` (management
  branch). **Next: PO approves P1-P3/U1 and gives explicit permission for the sandbox negative tests N1-N11,
  then POS, then build/lint/unit via the guard.**

## Durable pointers

- Contract: `safe/stories/US-FACTORY-003.yaml`; ADR:
  `docs/architecture/adr/ADR-0001-validator-history-and-lean-done.md`.
- Independent report: `docs/factory/US-FACTORY-003-round4-review.md`.
- Usage: `docs/factory/WORKFLOW-VALIDATION.md`.
- Local ignored logs: `factory/logs/US-FACTORY-003/recovery/`:
  `targeted-final.log`, `targeted-fix.log`, `targeted-a.log`, `security.log`,
  `build.log`, `lint-final.log`, and earlier Jenkins API snapshot `jenkins-3.log` /
  `jenkins-current.json` (final snapshot of finished build #3). Live build log is under
  `/var/lib/jenkins/jobs/AI_Tutor/branches/feature-US-F.1shirk.Y-003-devops/builds/3/log`.
- Existing narrow host API helper: `/tmp/factory-003-jenkins.py status` via sudo;
  reads existing Jenkins authentication without printing it. Its `index` / `build`
  modes mutate Jenkins; do not invoke them merely to read build status.
- No AC08 gate records or DoD flags were fabricated; no DONE claim, no PR, no merge,
  no deployment. The current blocker to PR automation is missing bot API write access.
