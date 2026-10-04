# US-FACTORY-003: R3-02 PO decision brief

| Field | Value |
|---|---|
| Finding | R3-02 (MAJOR, pre-existing since `42021fe`, contract-level) |
| Author | Claude orchestrator (CLAUDE_BA / PM support), 2026-10-04 |
| Decision owner | Human PO |
| Status | **PENDING PO DECISION** (RAID I-010). Not sent to Codex |
| Conflict to resolve first | The Factory V2 decision (2026-10-04) says US-FACTORY-003 stays under its existing approved contract and must not be re-contracted. Every option below except G changes AC text. The PO either grants an explicit exception for R3-02 or chooses G |

## a. Current contract and behaviour

- **AC18, non-feature branches:** the Factory Validation stage "fails when any Story with status DONE does not satisfy AC06".
- **AC06:** Unit Test, Code Review, Integration Test and Tester must be valid (**not STALE**), and Jenkins PASS must be for
  the **same implementation fingerprint**.
- **AC10:** the implementation fingerprint covers the **whole repository**. Every path not explicitly non-implementation
  counts (fail closed).
- **AC12(a):** any implementation fingerprint change makes every implementation-bound gate STALE_IMPLEMENTATION.
- **AC04:** any transition out of DONE is BLOCK. **TS21:** "on develop, a DONE Story without valid AC06 evidence -> FAIL".
- **Code:** `cli.py:134-137` calls `gate()` at the develop tip, and `engine.py:310-311` compares each record's fingerprint
  with the tip's fingerprint. The code follows the AC text.

## b. Why DONE evidence becomes stale

DONE evidence is bound to the fingerprint of the feature branch at QA/Jenkins time. Develop's fingerprint moves away from
it in two ways:

1. **Before the merge:** develop already has another Story's implementation change. The merge tree differs from the
   feature tree, so every gate is STALE on the first develop build.
2. **After a clean merge:** any later implementation commit on develop, from any Story, changes the repository-wide
   fingerprint.

AC04 forbids leaving DONE, so the evidence can never be refreshed. The develop Factory Validation stage runs right after
Checkout, so it fails **permanently** and blocks the whole develop pipeline (Build, Unit, …, DEV deploy) for every Story.
The reviewer reproduced 194 STALE_IMPLEMENTATION lines for one Story (`repro_r3.py` → `contract_develop_impl()`).

**When it would happen:** RAID I-009 schedules the US-FACTORY-002 recovery merge immediately after 003 is integrated. That
merge is an implementation change, so develop would break on the first merge after 003.

## c. Expected behaviour on develop after a Story is DONE

DONE is a terminal fact about history: the Story met AC06 at the revision where it was completed. Develop validation should
prove that this fact is true and untampered, not that the old evidence matches today's code. Whether today's develop code
still works is the job of develop's own pipeline stages (Build, Unit, Integration on develop) and of the gates of later
Stories. A later regression is a new defect, not a retroactive un-DONE.

## d/e. Alternatives

| Option | Rule on develop | Advantages | Disadvantages |
|---|---|---|---|
| **A. Keep as is** | AC06 freshness at develop tip | No change | Develop is permanently red after the second implementation merge. **Not viable** |
| **B. Completion snapshot** | Find the unique commit that set the Story status to DONE. Require it to be an ancestor of the evaluated revision. Evaluate AC06 **at that commit**. Check integrity of all Story evidence at the tip | Keeps the full AC06 check, fail-closed and deterministic. Reuses the existing `Factory(revision=…)` engine and the merge-commit-only policy (ancestry is preserved). Later commits never stale DONE Stories | Needs a precise "completion snapshot" rule (status introduction, ambiguity → FAIL). The integrated combination of this Story with other develop changes is checked only by develop's own pipeline stages, not by this Story's gates |
| **C. Merge commit + up-to-date rule** | The feature branch must contain the develop tip before QA/Jenkins (GitHub "require branches up to date"). Evaluate at the merge commit that brought DONE into develop | Strongest: the evidence matches the exact integrated tree at merge time | Every develop movement forces a rerun of Code Review, Integration, Tester, QA and Jenkins, which serialises merges and is expensive. It still needs B's rule for commits after the merge. Needs a GitHub setting (human admin) |
| **D. Integrity only** | Develop checks only evidence integrity and provenance for DONE Stories, with no AC06 re-evaluation | Simplest | Weaker. A status hand-edited to DONE on a branch that skipped feature Jenkins would pass develop. Contradicts the intent of AC18 |
| **E. Story-scoped fingerprint** | Fingerprint only the paths owned by the Story | Later unrelated changes don't stale it | Large change to AC10 (whole-repo, fail-closed). Path ownership is ambiguous and cross-Story effects are missed. **Rejected** |
| **F. Re-certify DONE** | Allow DONE→DONE re-evaluation and reruns | Evidence always current | Breaks AC04 (DONE terminal) and causes endless reruns on every merge. **Rejected** |
| **G. No re-contract now** | Complete 003 under the current AC18. Register R3-02 as a defect owned by a later Story (for example US-FACTORY-007) | Respects the V2 "do not re-contract 003" directive literally | Ships a validator known to break develop on the next implementation merge, which is the planned US-FACTORY-002 recovery (I-009). The fix would have to land before 002 merges anyway, and 002 must merge before 004–007 can progress. In practice this delays the same fix and blocks the roadmap |

## f. Recommendation: option B

B keeps every AC06 check, stays fail-closed, needs no new GitHub setting and reuses engine capabilities that exist already.
C's extra guarantee can be added later as a release-policy choice in US-FACTORY-007 without changing B.

Because B changes AC12/AC18/TS21 text, it needs an **explicit PO exception** to the V2 "do not re-contract US-FACTORY-003"
directive. If the PO does not grant it, choose G and accept the consequence described above.

## g. Exact contract changes for option B

**AC18, replace** "on other branches it fails when any Story with status DONE does not satisfy AC06." **with:**

> "On other branches, for each Story with status DONE it (1) determines the Story's completion snapshot: the unique commit
> in the evaluated history whose Story file has status DONE while every parent's Story file does not (none, more than one,
> or an unreadable Story file is FAIL); (2) requires the completion snapshot to be an ancestor of the evaluated revision
> (lost ancestry is FAIL with the merge-commit-only policy reason); (3) evaluates AC06 at the completion snapshot, with that
> snapshot's fingerprints, exactly as QA->DONE would be evaluated there; (4) checks the integrity and provenance of every
> evidence record of the Story at the evaluated revision (AC07, AC08, append-only). Implementation or contract changes
> after the completion snapshot never make a DONE Story STALE on these branches. Develop's own Build, Unit and Integration
> stages verify the integrated code."

**AC12, add (d):**

> "(d) Staleness applies to Stories before DONE. A DONE Story is evaluated at its completion snapshot (AC18); later
> implementation or contract fingerprint changes do not stale it."

**TS21, replace the develop clause with:**

> "on develop: a DONE Story merged by merge commit, followed by a later implementation commit of another Story → PASS;
> another Story's implementation change on develop before this Story's merge → PASS; a DONE status introduced at a commit
> where AC06 does not hold → FAIL; DONE introduced more than once or ambiguously → FAIL; completion snapshot not an
> ancestor (squash/rebase) → FAIL naming the merge-commit-only policy; an evidence record rewritten after completion → FAIL."

**AC06, AC04, AC10:** unchanged.

**WORKFLOW-VALIDATION.md (implementation-owned docs, done by Codex in the same rework):** replace "Develop-mode DONE
validation is unchanged." with a description of the completion-snapshot rule.

**Unit Test gate:** the Unit Test record lists per-TS results (`engine.py`, `ts_results`). Changing TS21 does not add a
scenario ID, so the set of expected IDs is unchanged.

## h. Migration and recovery impact on existing evidence

- **No DONE Story exists** on `origin/develop` or `feature/US-FACTORY-003-devops` (001 BLOCKED, 002 IN_PROGRESS, 003 READY
  in the tracked Story files, checked 2026-10-04). No develop evidence needs migration.
- **US-FACTORY-003 has no committed evidence records** at `233b1e9` (`git ls-tree HEAD factory/evidence` is empty).
- Changing AC12/AC18/TS21 changes the acceptance-contract fingerprint (AC11 material keys). That stales only Tester and QA,
  and none exist yet. Round 4 changes implementation anyway, so every implementation-bound gate reruns regardless.
- **Delivery path:** the contract change is a management change (`safe/stories/US-FACTORY-003.yaml`) through a management
  PR to develop. The feature branch then takes it with `git merge --no-ff develop`, following the merge-commit-only policy.
  The validator reads the Story at the feature revision, so round 4 must start after that merge.
- **CHANGELOG/DEVBOOK** record the decision. **Story status is unchanged** (contract edits are not state changes). A DoR
  re-check by CLAUDE_BA is needed because acceptance criteria change.
