---
id: ADR-0001
title: Validator history semantics, DONE completion snapshot, and the lean DONE gate set
status: ACCEPTED
decided_by_role: CLAUDE_SA
authority: Full technical authority delegated by the human PO, 2026-10-04 (LEAN MODE). The lean DONE semantics were fixed by the PO. This ADR decides only how to realise them technically.
date: 2026-10-04
story: US-FACTORY-003
supersedes: R3-01 rework brief §1-2 (direction kept), R3-02 PO decision brief option B (adopted with D3 below)
evidence_basis: SA prototype under scratchpad/sa-r3/proto/fix (13/13 round-4 tests OK, rerun 2026-10-04, 332 s; the same tests on unmodified 233b1e9 gave 9/13 FAIL) and scratchpad/sa-lean/proto/lean (lean gates, 2/2 OK, 98 s). The prototypes are MOCK/disposable and are not gate evidence.
---

# ADR-0001: Validator history semantics, DONE completion snapshot, lean DONE

## Context

Round-3 review of `233b1e9` returned FAIL with two MAJORs:

- **R3-01. Root cause:** `cli.py:116-125` re-validates every historical record in feature mode. Any PASS record whose
  prerequisites did not precede it (`prior_record_valid(history=True)` is False) is added to `errors` as
  `INVALID <gate>: out-of-order historical record`. Records are append-only (NFR06, `introduced()` makes deletion
  INVALID), so after the documented recovery the old out-of-order records remain forever. The feature stage therefore
  fails forever. That makes Jenkins PASS, and so DONE, unreachable (AC06), which contradicts AC16 and AC22.
- **R3-02. Root cause:** in develop mode, `cli.py:134-137` calls `gate()` at the develop tip, and `engine.py:310-311`
  compares each record's implementation fingerprint with the tip's fingerprint. The fingerprint covers the whole
  repository (AC10), so any other implementation change on develop makes every DONE Story STALE. DONE is terminal (AC04),
  so the evidence can never be refreshed and develop stays red permanently.
- **R3-03.** Feature mode and develop mode use different non-PASS allow-lists (`cli.py:120` vs `engine.py:322`).

The PO also approved a **lean DONE amendment**. One independent Validation, CI (Jenkins incl. Factory Validation and
the full unit suite), the PO's GitHub PR approval (AC13 verification unchanged) and a merge commit replace the separate
Tester, QA and mid-flow Code Review gates. TS24 runs once, after the PR approval. The state machine (AC04) is unchanged.
The lean view maps TODO={DRAFT,REFINED,READY}, DEV={IN_PROGRESS,DEV_COMPLETE} and VERIFY={TESTING,QA}.

Infra blockers: I-005 (backend stages fail closed, so a Factory Story has no meaningful CI PASS) and G-12
(`security-scan.sh` exits 1, so DoD `security_scan_passed` can never be true).

## Decision

**D1. Out-of-order history is non-authorising and does not fail the stage (R3-01).** A historical record that passes
integrity (`record(..., history=True)`) but has no valid preceding prerequisites is printed as
`HISTORY <gate>: out-of-order record <path> kept, non-authorising (AC16)`. It is not an error. Integrity failures
(missing or invalid field, wrong producer or identity, provenance, append-only or merge-introduction violation, ambiguous
latest record, bad artifact, unknown gate, result outside the AC07 vocabulary) still fail. A required gate is still
evaluated through `preconditions()` → `gate()` (non-history). So an out-of-order **latest** record of a required gate
still fails through `engine.py:424` (`out-of-order record`). No fail-open path is introduced.

**D2. A DONE Story is validated at its completion snapshot (R3-02, option B).** The completion snapshot is the unique
commit in the evaluated history whose Story file has `status: DONE` while no parent has DONE. Each of the following
fails closed: no such commit, more than one, a merge or root introduction, DONE removed later in history, a parent status
other than QA (AC04), a snapshot that is not an ancestor, or a shallow repository. AC06 (`QA->DONE` preconditions, read
from the snapshot's own workflow definition) is evaluated by a `Factory` pinned to that snapshot. The integrity of every
record (D1 rules) is checked at the evaluated revision. Both modes apply this to DONE. Feature mode additionally keeps
the tip check of the incoming edge, so implementation committed after DONE on an unmerged feature branch is STALE and
cannot be merged green.

**D3. Remote verification happens once, where the merge is authorised.** GitHub review verification (AC13) and Jenkins
archive verification (AC09) always run on feature branches (pre-merge, fail-closed). On other branches they run for a
DONE Story only when its completion snapshot is *not* reachable from the evaluated revision's first parent, that is,
when the Story arrives in this revision. A Story integrated earlier is re-checked offline (AC06 at the snapshot, record
integrity) by a `Factory(..., github=None, archive=None, verify_review=False)`. Reason: the PO rule that historical
evidence must never permanently block normal flow. Re-querying a reviewer's current association or a rotated Jenkins
archive on every develop build would make develop permanently red for historical reasons.

**D4. R3-03 aligned.** One constant `HISTORY_NONPASS = (FAIL, NOT_EXECUTED, UNKNOWN, PENDING_PO, PARTIAL,
PASS WITH BLOCKERS)` is the accepted vocabulary for well-formed non-authorising history in both modes. Any other result
fails.

**D5. Lean DONE as data plus 3 code touch points.** In `factory/workflow.yaml`, the gates `Tester` and `QA` are replaced
by a single gate named `Validation` (producer `CODEX_QA`, existing role, no new role; implementation- and
contract-bound; prerequisite Unit Test). `Code Review` (the PO's PR approval) moves after Validation and Jenkins
(prerequisites Unit Test, Validation, Jenkins). `Integration Test` keeps `[Unit Test, Code Review]` and therefore
follows the approval. Transitions: `DEV_COMPLETE->TESTING: [Unit Test]`, `TESTING->QA: [Unit Test, Validation]`,
`QA->DONE: [Unit Test, Validation, Jenkins, Code Review, Integration Test, DoD, dependencies, blockers]`. Dispatch:
`CODEX_QA` in TESTING; `Code Review` and `Integration Test` in QA. Failure paths and the state machine are unchanged.
Code: (1) the literal `('Tester', 'QA')` at `engine.py:307` and `:335` becomes `INDEPENDENT_GATES = ('Validation',)`;
(2) a Validation PASS additionally needs `findings: {critical: 0, major: 0}` (integers, bool rejected) next to the
existing per-AC check; (3) the invocation texts in `cli.py:60-64` change, and `integration.py:69` uses `CODEX_QA`
instead of `CODEX_TESTER` for its BLOCK step. `Code Review` keeps its name, producer and all AC13 checks. Only its
position changes. `review()` already requires the reviewed commit to satisfy the Code Review prerequisites, so the PO
must approve a commit that already contains Validation and Jenkins PASS.

**D6. I-005: the Factory Validation stage becomes the Factory CI composite (inside 003, AC18 amendment).**
`scripts/factory-jenkins.sh` (003-owned, not AC20-protected) runs, fail-fast and in order: the validator, then
`factory-runtime.sh build`, `lint` and `unit` (full suite), then `scripts/security-scan.sh`. Logs go to `factory/logs/`,
which the existing post step archives. The Jenkinsfile diff remains only the added stage. Inside that stage, the stage
body is wrapped in `withCredentials` for `FACTORY_GITHUB_TOKEN` (closes F-25). Backend stages stay fail-closed and keep
blocking artifact and deploy. Details are in `infra-decisions.md`.

**D7. G-12: a pinned, containerised OSS scanner set inside 003 (AC20 amendment for security-scan.sh only).** The set is
gitleaks (full Git history), trivy fs (vuln, misconfig, secret; HIGH/CRITICAL) and bandit (Python SAST in the canonical
runtime, hash-locked). All are pinned by exact version plus digest or hash, and all fail on findings and on scanner
error. Details are in `infra-decisions.md`.

**Also in round 4 (already prototyped, small):** R2-05 (`blocked_from` must be a pre-DONE state) and the 3 R3-04
mutant-guard tests. R2-07 and R3-05 stay open (MINOR/INFO).

## Alternatives considered (brief)

| Topic | Alternative | Why rejected |
|---|---|---|
| R3-01 | Keep INVALID for out-of-order history | Documented recovery can never reach DONE (append-only) |
| R3-01 | Allow deletion or supersession markers | Breaks NFR06 / `introduced()` append-only integrity |
| R3-02 | A keep tip freshness / C merge+up-to-date / D integrity only / E story-scoped fingerprint / F re-certify / G defer | Per R3-02 brief: A not viable; C serialises merges and still needs B; D drops AC06; E breaks AC10; F breaks AC04; G breaks develop at the 002 merge |
| D3 | Always re-verify GitHub and archive on develop | Permanent red from historical facts (reviewer association change, archive rotation), API cost grows with DONE count |
| D3 | Never verify on develop | Loses the arrival check for an admin merge that bypassed the feature check |
| D5 | Keep Tester+QA gates, one producer | Two records for one activity; contradicts "ONE independent Validation" |
| D5 | Reuse gate name `QA` for Validation | Fewer test edits, but collides with state `QA` and hides the semantic change |
| D5 | Drop the Code Review gate, rely on branch protection | PO kept AC13 verification |
| D5 | New validator role | AC14 "no new reviewer role"; `CODEX_QA` already owns per-AC verification |
| D6 | Factory detection in build/lint/unit-test.sh | AC20, conflicts with 002's edits to those scripts, and Integration/Artifact/Deploy still fail, so no green build |
| D6 | Separate Jenkins job | Extra infra on top of D-001; no benefit |
| D6 | Mark backend stage failures acceptable | Forbidden (constitution) |
| D7 | Follow-up Story | 003 DoD needs `security_scan_passed`; a separate Story would need the same scanner to be DONE |
| D7 | semgrep / pip-audit / osv-scanner | semgrep downloads rule sets at runtime (non-deterministic, heavier); trivy covers dependency CVEs |

## Consequences

- AC text changes are required (management PR by CLAUDE_BA, exact text in `story-003-amendment.md`): AC03, AC05, AC06,
  AC12, AC13 (position only), AC14, AC16, AC18, AC20, AC24; TS01-TS05, TS07, TS08, TS11-TS13, TS18, TS19, TS21, TS24-TS26.
  AC04, AC10, AC11, AC15, AC21-AC23, AC25 are unchanged. TS IDs are unchanged, so `unit_scenarios` and the Unit Test
  `ts_results` set are unchanged.
- The contract change stales only contract-bound gates (Validation). None exist on the branch, and round 4 changes
  implementation anyway, so all gates rerun.
- About 30 existing tests need mechanical updates (Tester/QA → Validation; Code Review now needs Validation and Jenkins
  first). The list is in `round4-codex-spec.md`.
- The DoD template is unchanged (it is a `contract_ref`). Key mapping: `qa_passed` and `acceptance_criteria_passed` →
  Validation record; `code_review_passed` → Code Review record; `security_scan_passed` → the Jenkins Factory Validation
  record (archived security log).
- Jenkins needs `FACTORY_GITHUB_TOKEN` (read-only) bound to the stage. Without it the stage fails closed.
- GitHub settings (human admin, UNVERIFIED): merge commits only; "dismiss stale approvals" and "require approval of the
  most recent push" OFF. Evidence commits follow the approval. Safety comes from the validator: any implementation
  change after the approved commit makes Code Review STALE (`engine.py:285`).
- Residual risk (accepted, documented): on develop, a Story integrated earlier is not re-verified remotely. The
  guarantees are the feature-branch check (a required status check) and the arrival build.
- CI time grows (the full unit suite runs in Factory Validation). Performance stays an R3-05 follow-up.
- `agents/codex/tester.md` is no longer on the DONE path. It is not deleted.


## Recovery addendum: real integration composite (2026-10-04)

The recovery SA approved host Bash coordination of two canonical Python phases to
realise D6 and AC23/AC24 without exposing the Docker socket inside a container.
Prepare verifies the real approved review, creates the disposable clone and runs
schema, dispatch, BLOCK and DoR checks. The host runs the actual
`scripts/factory-jenkins.sh` composite on that same clone. Complete verifies the
source revision, clone containment, unchanged clone HEAD and actual exit status
before continuing transitions, evidence writing and stale detection. A failed
composite produces non-PASS output. Every Python phase still uses AD-02; no host
Python fallback or additional writable real-repository mount is introduced.

This is a technical implementation decision from the recovery SA, not a change
to the acceptance contract. The implementing DevOps agent recorded this decision.
