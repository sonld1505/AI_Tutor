# US-FACTORY-003 independent pre-review, round 3

| Field | Value |
|---|---|
| Story | US-FACTORY-003 (central fail-closed gate validator, revision-bound evidence, AD-02 runtime) |
| Commit reviewed | `233b1e90146d90caef5cb4cc4e28e31b0970d1b6`, branch `feature/US-FACTORY-003-devops` |
| Previous rounds | `42021fe` (initial), `0790d2f` (round 2) |
| Base | `a3fb006` (origin/develop) |
| Worktree | `/home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-devops`. HEAD = 233b1e9 and clean (0 porcelain lines) before and after this review |
| Reviewer | Fresh, independent review agent (Claude), read-only |
| Date | 2026-10-04 |
| Read-only statement | No modify, commit, push, stash, checkout, reset or fetch in any real worktree or branch. No PR, no GitHub writes, no Codex, no Jenkins, no Tester or QA. All experiments ran in disposable clones under this scratch directory, with per-command `GIT_*` identity env vars and no repository `git config` writes |

> **NOT AC13.** This report is not the AC13 Code Review gate. AC13 requires an approved GitHub PR review by the human
> login `sonld1505`, verified through the GitHub API. This report is an independent pre-review input only. Do not use
> it as a Code Review record, as a DoD reference or as gate evidence.

## 1. Verdict: **FAIL**

| Severity | Count |
|---|---|
| CRITICAL | 0 |
| MAJOR | 2 (R3-01 new in round 3; R3-02 pre-existing, contract-level) |
| MINOR | 4 (R3-03 new, R3-04 new test gaps, R2-05 still open, R2-07 still open) |
| INFO | 3 (R3-05, R2-08, R2-10 carried) |

Round 3 closes R2-01, R2-02, R2-03, R2-04 and R2-06. I confirmed this by reproductions against the real engine and by
reverting each fix. I found no fail-open authorisation path. The verdict is still FAIL for two reasons:

- **R3-01 (MAJOR, introduced by the R2-02 fix).** The documented recovery after an out-of-order execution
  (WORKFLOW-VALIDATION.md:233-236, AC22, AC16) now leaves the feature-branch Factory Validation stage FAILing
  permanently. The retained out-of-order Tester/QA records are reported as `INVALID ...: out-of-order historical
  record` forever. The Jenkins gate needs Factory Validation PASS, so the Story can never reach DONE honestly.
  Round-2 code gave `[]` for the same scenario.
- **R3-02 (MAJOR, pre-existing, contract-level: needs a PO/BA decision).** Develop-mode validation of DONE Stories
  checks the evidence fingerprint against the current develop tip. Once any later implementation change lands on
  develop, or develop already had other implementation changes at merge time, every gate of every DONE Story becomes
  STALE_IMPLEMENTATION. The develop Factory Validation stage, which runs before Build, then FAILs permanently. A DONE
  Story cannot transition again.

## 2. R2-01..R2-07 closure matrix

| ID | Status | Evidence (file:line at 233b1e9) | Covering tests | Fails if fix reverted? |
|---|---|---|---|---|
| R2-01 merges poison evidence | **CLOSED** | engine.py:157-192 `introduced()` traces `rev-list --parents` and per-commit `ls-tree` blobs. An unchanged blob inherited from any parent is not an introduction (186). A rewrite (184), a deletion (185), an evil-merge introduction (187) or multiple introductions (189) are INVALID. Shallow history BLOCKs (164) | test_git_graph.py:70 (merge develop into feature), :88 (`--no-ff` PR merge into develop), :101 (merge-resolution rewrite), :138/:155/:164 (squash/cherry-pick, rebase, shallow), :229, :240 | **YES.** With 0790d2f `engine.py` restored (`rev_engine`), test_git_graph gives 10 failures and 2 errors out of 13. The merge tests :70 and :88 ERROR with `INVALID evidence history rewritten` |
| R2-02 stale/non-PASS history fails Jenkins | **CLOSED** (but see R3-01, which the fix introduced) | cli.py:116-137: feature mode validates each record with `history=True` and allows well-formed non-PASS results (120). It checks the historical PASS order at the source snapshot (122-123) and checks latest-record ambiguity (131). It calls `gate()` only in develop mode (134-137). engine.py:355-372 checks prerequisite freshness at the source snapshot | test_git_graph.py:174 (IN_PROGRESS stale plus FAIL/UNKNOWN/NOT_EXECUTED/PARTIAL/PASS WITH BLOCKERS), :190 (recovery with stale downstream), :205, :214 (stale contract), :223 | **YES.** With 0790d2f `cli.py` restored (`rev_cli`), 6 of 13 git-graph tests fail (:174, :190, :214, :223, :205, :70) |
| R2-03 allow-list subcase not isolated | **CLOSED** | test_rework.py:167-190: an unlisted COLLABORATOR whose identity matches must give exactly `^review unapproved reviewer$`. A mutant copy in the disposable fixture shows that deleting engine.py:275 lets the review pass | test_rework.py:167 | **YES.** If line 275 is removed, both `count(check) == 1` and the regex assertion fail |
| R2-04 source_commit is a producer declaration | **CLOSED** (documentation; the limit is inherent) | WORKFLOW-VALIDATION.md:87-90, 101-104 | n/a | n/a (documentation) |
| R2-05 hand-committed BLOCKED / `blocked_from` | **OPEN** (MINOR; CHANGELOG states it was skipped) | engine.py:477-482 unchanged. cli.py:105 accepts BLOCKED without checks | none | n/a |
| R2-06 orchestrator carries uncommitted state | **CLOSED** | cli.py:49 compares the state file bytes with the Git blob before any write | test_rework.py:227 `test_TS16_MOCK_uncommitted_state_refused_without_writes` | **YES.** It fails under `rev_cli` |
| R2-07 `check-ignore --no-index` reads working tree | **OPEN** (MINOR; CHANGELOG states it was skipped) | engine.py:237 unchanged | none | n/a |

### Reproductions (real engine and CLI, disposable MOCK Git fixtures, `repro_r3.py`, canonical image)

| Scenario | 233b1e9 | 0790d2f code (same script) |
|---|---|---|
| R2-01 case 1: all gates, DEV_COMPLETE, `git merge --no-ff develop` (develop changed docs only). The merge commit has 2 parents | every gate PASS; DEV_COMPLETE->TESTING `[]`; feature jenkins `[]` | `Block: INVALID evidence history rewritten` |
| R2-01 case 2: DONE feature merged into develop with `--no-ff` "Merge pull request", then develop back-merged into feature | develop jenkins `[]`; feature jenkins after back-merge `[]` | develop and feature both `Block: INVALID evidence history rewritten` |
| R2-02: IN_PROGRESS, more implementation after Unit evidence, later build FAIL | `[]`, `[]` | 5 STALE errors; `build: INVALID FAIL result not PASS` |
| R2-02 recovery: all gates, QA FAIL to IN_PROGRESS, fix commit, build/lint/Unit, DEV_COMPLETE, rerun to DONE | DEV_COMPLETE `[]`; DONE `[]` | 16 STALE errors at DEV_COMPLETE |
| **Documented out-of-order recovery** (R3-01) | at QA and at DONE: `['INVALID Tester: out-of-order historical record', 'INVALID QA: out-of-order historical record']`; validator QA->DONE `[]`; develop-mode `[]` | feature jenkins at QA `[]` |
| **Develop after a DONE merge where develop has another implementation change** (R3-02) | 194 STALE_IMPLEMENTATION errors. A clean merge gives `[]`, and a single later implementation commit on develop again gives 194 errors | raised `history rewritten` first, so this was masked |
| **Superseded `PASS WITH BLOCKERS` Tester record, DONE** (R3-03) | feature jenkins `[]`; develop after merge `['PASS WITH BLOCKERS result not PASS']` | n/a |

## 3. New findings

| ID | Severity | File:line | Failure scenario | Repro path |
|---|---|---|---|---|
| R3-01 | **MAJOR** (new in round 3) | factory/cli.py:122-123 with engine.py:355-372; docs WORKFLOW-VALIDATION.md:182-183 contradict :233-236; test_git_graph.py:223-227 encodes the behaviour | Tester/QA ran before Code Review (this Story's origin, US-FACTORY-002). The team follows the documented recovery: DoD FAIL to DEV_COMPLETE, keep the records, rerun Code Review, Integration, Tester and QA in order. The validator accepts every transition, including QA->DONE. The feature Factory Validation stage FAILs on every build because the retained records are out-of-order. Records are append-only and deletion is INVALID, so no recovery exists. The Jenkins record needs `Factory Validation: PASS` (engine.py:343-344), so DONE is unreachable without falsifying Jenkins evidence. This contradicts AC16 ("kept as history but never satisfy a precondition") and AC22/WORKFLOW-VALIDATION.md:233-236 ("retain previous records ... Jenkins/DoD then decide DONE"). If the PO reads AC18 "any of its evidence records is invalid" as covering out-of-order history, then the documented recovery cannot work. Either way the contract needs a decision | `repro_r3.py` → `documented_out_of_order_recovery()`; output in `repro_r3.out`; baseline `repro_r2code.out` |
| R3-02 | **MAJOR** (pre-existing since 42021fe; **contract-level, PO/BA decision needed**) | factory/cli.py:114-115, 134-137; engine.py:310-311 (current-tip freshness); AC06 + AC18 ("other branches ... any Story with status DONE does not satisfy AC06") + AC12 | (a) Develop received another Story's implementation change before the DONE feature PR is merged: the merge-tree fingerprint differs, so every gate is STALE_IMPLEMENTATION. (b) After a clean merge, any later implementation commit on develop, for example a US-FACTORY-002 merge, makes every DONE Story STALE. The develop Factory Validation stage runs before Build, so it FAILs permanently and blocks the develop pipeline. `transition()` refuses source DONE (engine.py:476), so there is no workflow path to refresh the evidence. The code follows the AC text, but the AC text makes develop unbuildable after the second implementation merge. Possible decisions: validate a DONE Story at the merge commit that brought DONE into develop, at its feature-parent snapshot, or only its integrity (not freshness) on develop | `repro_r3.py` → `contract_develop_impl()` |
| R3-03 | MINOR (new in round 3) | factory/cli.py:120 (feature mode allows `PARTIAL`, `PASS WITH BLOCKERS`) vs develop mode `allow_nonpass=True` → engine.py:322 (FAIL/NOT_EXECUTED/UNKNOWN/PENDING_PO only) | A Story with a superseded hand-committed `PARTIAL` or `PASS WITH BLOCKERS` record passes feature Jenkins at DONE. After the merge, develop FAILs permanently with `PASS WITH BLOCKERS result not PASS`. The sanctioned writer (cli.py:31) refuses those result values, so the trigger is a hand-committed record. That is why this is MINOR | `repro_r3.py` → `develop_partial_history()` |
| R3-04 | MINOR (test gaps in new round-3 code) | engine.py:187 (evil-merge introduction), engine.py:361-367 (historical prerequisite freshness filter), engine.py:296-297 (ancestry check in `record()`) | The suite does not detect that these documented behaviours were removed. A regression would go unnoticed. The code itself is correct when read | Bounded mutants, each run against test_git_graph, test_rework and 3 test_factory tests (36 tests): `m_merge_intro` OK (survived), `m_hist_filter` OK (survived), `m_record_intro` OK (survived), `m_shallow` killed (1 failure), `m_prior_cli` killed (1 failure) |
| R3-05 | INFO | engine.py:165-176 (`ls-tree` per commit for each new revision `Factory`, including review snapshots and per-record artifact factories); cli.py:113-137 (duplicate error lines) | The suite ran 88 tests in 919 s alone and 2311 s under parallel load. 33 git-graph and rework tests took 633 s. Develop output repeats each STALE reason (194 lines for one Story). This is a usability and CI-time concern, not a correctness one, at the current repository size (20 commits) | unit runs below |
| R2-08 | INFO (carried) | workflow.yaml; engine.py:51 | Self-hosted committed policy, by design (AC01) | — |
| R2-10 | INFO (carried) | various | F-14, F-18, F-19, F-25 (Jenkins token not injected, which also affects develop Code Review), F-27, F-29; the FIXTURE_OUTPUT mktemp directory is never removed | — |

R2-09 (squash/rebase/shallow fail-closed) is now documented as a PO merge-commit-only policy
(WORKFLOW-VALIDATION.md:106-121) and enforced (engine.py:164, 187, 189, 292-297). It is CLOSED as documented.
GitHub repository settings remain a human admin action and are UNVERIFIED.

**Fail-open check (round-3 changes).** In feature mode `gate()` no longer runs for unrequired gates. Every
*required* gate is still evaluated through `preconditions()` → `gate()` (non-history, with GitHub verification
of Code Review). History mode skips review verification and freshness, but its result only adds errors and never
authorises anything. `prior_record_valid` caches are keyed by `history`, so history acceptance does not leak into
gate evaluation. The `allow_nonpass` tuple applies only in Jenkins history mode, and `gate()` passes `False`.
`introduced()` is stricter than round 2 on every non-merge path. I found no path that turns a failed, missing,
stale or not-executed gate into PASS.

## 4. Earlier CLOSED findings: regression check

| ID | Still closed? | Evidence |
|---|---|---|
| F-01 | YES | engine.py:51 reads the policy from the Git blob; test_rework TS17 tests pass |
| F-02 | YES (strengthened) | engine.py:157-192, 374-382; TS11 tests pass |
| F-03 | YES | engine.py:255-285; TS13 tests pass, including the new R2-03 test |
| F-04 | YES (now closed through R2-02) | cli.py:110-112, 116-137 |
| F-05..F-08 | YES | Fixtures unchanged in substance; TS05/TS08/TS11/TS14/TS10/TS26 pass. TS27 needs the host probe (see §5) |
| F-09, F-10 | YES | cli.py:43, 73-84; TS16 tests pass |
| F-11 | YES | engine.py:273-277 casefold |
| F-23 | YES | CHANGELOG new rows (lines 32-33) correctly say "Chưa chạy ... canonical" and make no gate claim |
| AC20 | **HOLDS** | `git diff --name-only a3fb006 233b1e9 -- scripts/{deploy,build,lint,unit-test,integration-test,security-scan,quality-gate,build-artifact,create-worktree}.sh docker-compose.test.yml` is empty (exit 0). No `docker-compose.test.yml` exists. The Jenkinsfile diff adds only the `Factory Validation` stage after Checkout |

## 5. Commands and results

All test commands used the image `python:3.12@sha256:4f80f792...ab42` (Python 3.12.15), run as uid 1000:1000 with a tmpfs
`/tmp` and only this scratch directory bind-mounted. Dependencies were installed with
`pip install --no-deps --only-binary=:all: --require-hashes --target /tmp/deps -r $CODE/factory/runtime/requirements.txt`,
and `PYTHONPATH=/tmp/deps:$CODE/factory:$CODE/factory/tests` (wrapper `run.sh`; scratch-only, not gate evidence).

| Command | Exit / result |
|---|---|
| `git -C <worktree> rev-parse HEAD`; `status --porcelain` (start and end) | 0; `233b1e9...`; empty both times |
| `git clone <worktree> clone && git checkout 233b1e9` (plus clones `r2`=0790d2f, `rev_engine`, `rev_cli`, 5 mutants) | 0 |
| `python -m unittest discover -s $CODE/factory/tests` (full suite, in container) | **1**. Ran 88: 86 OK, failures=1, errors=1, skipped=0. Both are environmental: `test_TS27_MOCK_actual_helper_mounts_and_ownership` (KeyError `FACTORY_RUNTIME_TEST_REPORT`; the host probe report exists only via `factory-runtime.sh unit`) and `test_TS23_MOCK_python_names_removed_from_PATH` (`BLOCK Docker unavailable` inside the container). The same result came from an earlier identical run (88 tests, 919 s; its outer `timeout` wrapper exited 124 but the container completed) |
| `python -m unittest -v test_git_graph test_rework` | **0**. Ran 33, OK, 0 skipped (633 s) |
| `rev_engine` (0790d2f engine.py): `python -m unittest -v test_git_graph` | **1**. Ran 13, failures=10, errors=2 |
| `rev_cli` (0790d2f cli.py): `python -m unittest -v test_git_graph test_rework...test_TS16_MOCK_uncommitted_state_refused_without_writes` | **1**. Ran 14, failures=7 |
| `python repro_r3.py` (233b1e9) | 0 (output `repro_r3.out`) |
| `python repro_r3.py` against 0790d2f engine/cli/fixtures | 0 (output `repro_r2code.out`) |
| Mutants (5, each `timeout 1200` on the docker client, test_git_graph + test_rework + 3 test_factory tests, 36 tests) | m_merge_intro 0 (survived); m_hist_filter 0 (survived); m_record_intro 0 (survived); m_shallow 1 (killed); m_prior_cli 1 (killed). The client timeouts fired under parallel load, but every container ran to completion, so no mutant is NOT RUN |
| `./scripts/factory-runtime.sh build` (scratch clone, host helper) | **0**, `PASS` |
| `./scripts/factory-runtime.sh lint` | **0**, `All checks passed!` |
| `STORY_FILE=safe/stories/US-FACTORY-003.yaml ./scripts/validate-story.sh` | **0**, `DEFINITION OF READY: PASSED` |
| `BRANCH_NAME=feature/US-FACTORY-003-devops ./scripts/factory-jenkins.sh` | **0**, `PASS` (Story READY, no evidence) |
| `BRANCH_NAME=develop ./scripts/factory-jenkins.sh` | **0**, `PASS` (no DONE Story) |
| `git diff --check a3fb006 233b1e9` | 0 |
| AC20 protected-path diff | 0, empty |
| `./scripts/factory-runtime.sh unit` (canonical host unit gate) | **NOT RUN**. The helper creates `mktemp -d /tmp/factory-runtime-test.XXXXXX` on the host, outside the permitted scratch directory |

## 6. AC coverage notes

- AC06/AC18 (develop): correct after a merge with docs-only changes. Permanently broken by later implementation changes (R3-02, contract-level).
- AC12: stale history no longer fails the feature build (R2-02 closed). STALE stays non-authorising.
- AC16/AC22: out-of-order records are kept, but the feature build can never pass again (R3-01). This contradicts the documented recovery.
- AC18 (feature): supported-status checks and invalid-record checks are separated correctly, apart from R3-01 and R3-03.
- AC03: R2-06 closed. Uncommitted state and Story edits are refused before any write.
- AC13: logic is MOCK-verified only. The real review is NOT-TESTABLE-LOCALLY (no PR).
- AC20: holds. AC19: `validate-story.sh` passes on Story 003.
- AC22: documentation now states the merge-commit-only policy and the R2-04 limit. Lines 182-183 and 233-236 contradict each other (R3-01).

## 7. Not verified

- Canonical host `./scripts/factory-runtime.sh unit`, including the TS27 Docker mount probe and the TS23 PATH test: not run, because of the write-scope rule (§5). Those 2 tests fail only for environmental reasons inside a plain container.
- Real GitHub review semantics (TS24/AC13/AC24), real Jenkins (TS25/D-001), Jenkins credential injection (F-25), GitHub squash/rebase settings.
- Tester and QA have not run. This review replaces neither, nor the AC13 human review.
- Non-x86_64 hosts. Performance on a large real history.
- Mutation testing was bounded to 5 mutants on round-3 code. Other code was not mutated in this round.
