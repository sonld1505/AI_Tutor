# US-FACTORY-003 independent code review, round 2

| Field | Value |
|---|---|
| Story | US-FACTORY-003 (central fail-closed gate validator, revision-bound evidence, AD-02 runtime) |
| HEAD reviewed | `0790d2fa2d4a6f481fed0f188cfdc48f5f5b7f1c` (rework), branch `feature/US-FACTORY-003-devops` |
| Previous implementation | `42021feb2ddfa1b048990adb5c20213340f13bf4` |
| Base | `a3fb006` (origin/develop) |
| Worktree | `/home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-devops` (clean before and after) |
| Reviewer | fresh independent review agent (Claude, read-only) |
| Date | 2026-10-04 |

> **NOT AC13 evidence.** The formal Code Review gate (AC13) is an approved GitHub PR review by the
> human login `sonld1505`, which is not the implementation identity `sonldfkr2911`, verified through
> the GitHub API. This report is an independent pre-review input to that human review only. Do not
> record it as a Code Review record, a DoD reference or any gate evidence. A read-only GitHub GET
> on 2026-10-04 found no PR for `feature/US-FACTORY-003-devops` yet. The remote branch head is `0790d2f`.

## 2. Verdict: **FAIL**

Most of the rework is solid. I confirmed it by reading the code, by mutation tests and with end-to-end
reproductions. F-01, F-02, F-03, F-05..F-11 and F-23 are closed. Under the verdict rules the review
still fails, for three reasons:

1. **F-04 is only PARTIAL.** The DoR status false-FAIL at IN_PROGRESS is fixed. The Jenkins
   feature-branch check still FAILs whenever *any* historical record of the Story is STALE or not PASS,
   even when the current status does not need that gate. This happens in the normal IN_PROGRESS loop:
   Unit evidence is recorded and then more implementation commits follow. It also happens during the
   documented recovery path, where old Tester/QA records are stale (R2-02, MAJOR, reproduced).
2. **New MAJOR defect introduced by the F-02 fix (R2-01).** `Factory.introduced()` treats a merge
   commit as an evidence rewrite. When evidence reaches the evaluated branch through a real merge
   commit, `records()` raises `INVALID evidence history rewritten`. This covers a GitHub "Merge pull
   request" into develop, and `git merge develop` into a feature branch. After such a merge every
   gate, transition and the Jenkins stage BLOCK permanently, and append-only records cannot repair it.
   I reproduced this with the real engine. It is fail-closed, but it breaks AC06/AC18 on develop and
   the AC12/NFR06 history model in normal Git use.
3. R2-02 contradicts AC18 ("fails ... when the recorded status is not supported by valid evidence or
   any of its evidence records is invalid"). Under AC02 and AC12, STALE is not INVALID, and stale
   records are kept as history.

There is no CRITICAL finding and no fail-open gate path in the evaluated code. The AD-02 runtime, C1–C3,
fingerprints, stale-contract isolation, the F-03 reviewer authority and F-09 YAML preservation are correct.

## 3. Closure matrix

| ID | Status | Evidence (file:line) | Regression test(s) | Does the test really exercise it? |
|---|---|---|---|---|
| F-01 | **CLOSED** | engine.py:48 reads the policy with `self.blob('factory/workflow.yaml')` at the evaluated revision. cli.py:131-147 has no `--workflow` option | test_rework.py:28 `test_TS17_MOCK_uncommitted_policy_cannot_weaken_gates`; :47; test_factory.py:617 | YES. Mutation M2 (read the working-tree file) makes the test fail. End to end in a scratch clone: an uncommitted edit `IN_PROGRESS->DEV_COMPLETE: []` plus the real helper `--write ... orchestrate` gives BLOCK, exit 1 (§8). Residual: R2-07 (working-tree `.gitignore`), R2-08 (committed policy is self-hosted, by design) |
| F-02 | **CLOSED** (residual R2-04, and the new defect R2-01 comes from this fix) | engine.py:154-167 (unique introduction, immutable), 169-174, 316-338 (`precedes` = Git ancestry of the introduction commit and source_commit), 340-344 (latest = unique descendant), 382-386. Timestamps are no longer used for ordering. For Code Review they are only cross-checked against the server `submitted_at` (engine.py:253-256) | test_rework.py:55 backdated and future cases; :87 rewritten record; test_factory.py:371 recovery | YES. Mutation M5 (`precedes` → True) fails both TS11 tests. The backdated (2026-10-02) and future (2099) records stay INVALID, and later honest records PASS. Residual: `source_commit` is still declared by the producer (R2-04, reproduced) |
| F-03 | **CLOSED** (test-precision gap R2-03) | engine.py:232-253: repository pinned to policy (234), base repository (236), head branch `feature/<story>-<role>` (238), commit count (239), approved reviewers `[sonld1505]` from workflow.yaml:6-8 (250), author_association OWNER/MEMBER/COLLABORATOR (251), record identity = reviewer (252), server `submitted_at` (253), reviewed snapshot holds Unit evidence (258-259) | test_rework.py:97 (positive, then arbitrary login / NONE / CONTRIBUTOR / wrong base / wrong branch / truncated / submission / wrong repository / predates); :127; test_factory.py:245 | Mostly. Mutation M9 (drop the association check) fails the test. Mutation M1 (drop the `approved_reviewers` check) **survives** all three TS13 tests: the "arbitrary login" subcase is caught by the identity-mismatch check, not the allow-list (R2-03). The code is correct. D-006 semantics are enforced: reviewer = sonld1505 only, never the implementing identity, PR author or commit authors |
| F-04 | **PARTIAL** | cli.py:107-111 skips the READY-only DoR status rule at IN_PROGRESS | test_rework.py:166 `test_TS21_MOCK_in_progress_status_and_next_transition` | YES for the reported cause (mutation M3 fails the test). **Not handled per contract** once any record is stale or FAIL: cli.py:122-125 (R2-02, reproduced) |
| F-05 | **CLOSED** | fixtures.py:36 now gives valid DoD evidence, so DoD no longer masks the result | test_factory.py:61 (exact `['Jenkins: MISSING missing evidence']`, DoD false, DoD without evidence, per-AC, blocked_by, RAID), :524 (depends_on exact); test_factory.py:114 TS08 (QA->DONE `[]` first, then every error STALE_IMPLEMENTATION, CLI rerun order); test_rework.py:280 | YES. Exact-equality assertions fail if the condition under test is removed. TS08 starts from a `[]` baseline |
| F-06 | **CLOSED** | engine.py:382-386 | test_factory.py:171 | YES. Asserts TESTING->QA BLOCK, old Tester/QA INVALID after Code Review + Integration, recovery through `DoD FAIL:` to QA, history bytes unchanged |
| F-07 | **CLOSED** | engine.py:295-301 | test_rework.py:201 (not permitted by Story; permitted → N/A-APPROVED; ineligible Tester; FAIL/MISSING_TOOL/MISSING_CONFIGURATION), :218 (US-FACTORY-003 copy, also with `na_permitted` set, isolates the 003 rule); test_factory.py:415 (Integration before Code Review, Tester/QA-produced Integration → Tester dispatch BLOCK, implementer after Code Review → PASS) | YES (traced each assertion to an isolated branch) |
| F-08 | **CLOSED** | scripts/factory-runtime-test.sh (real Docker helper on a disposable repository, readonly and `--write`, host stat ownership); engine.py:205-215 | test_factory.py:459 (TS27 report), :341 (TS10: tracked sha mismatch, gitignored non-logs, .log/.jsonl/.zip/.tar.gz, raw-log-only record) | YES. Ownership is now `stat` on host files written by the container, not a tautology. My unit run executed the probe (TS27 2/2) |
| F-09 | **CLOSED** | cli.py:72-81, 87: single top-level `status:` value replaced in the Git blob text, re-parsed and compared | test_rework.py:179 | YES. Mutation M4 (`safe_dump`) fails it. **Real Story repro** (scratch clone, canonical helper `--write ... transition READY->IN_PROGRESS`): the `diff` shows only line 104 `status: READY` → `IN_PROGRESS`. The comment on that line, the A–F decisions, AD-02, the C1–C3 history and "Keep this block LAST" all survive |
| F-10 | **CLOSED** | cli.py:43, 83 | test_rework.py:190 | YES |
| F-11 | **CLOSED** | policy.py:6; engine.py:248-250, 278 (casefold) | test_rework.py:127 | YES. Mutation M6 (case-sensitive comparison) fails 4 subtests |
| F-23 | **CLOSED** | WORKFLOW-VALIDATION.md:4-6 (committed as 42021fe), token scope section (Pull requests: Read + Metadata: Read); CHANGELOG last rows mark "Chưa commit" as history | n/a | n/a |
| F-12 | CLOSED | remotes.py:107; engine.py:239 | test_rework.py:237, :101 "truncated" | YES |
| F-13 | CLOSED | engine.py:241 filters PENDING | test_rework.py:133 | YES |
| F-15 | CLOSED | engine.py:289 checks history artifacts at their source revision | test_rework.py:248 | YES. R2-01 creates a new "permanently INVALID history" case |
| F-16 | CLOSED | engine.py:346-356; cli.py:184 | test_rework.py:280; test_factory.py:126-132 | YES |
| F-17 | CLOSED | engine.py:277-278 | test_rework.py:259 | YES (mutation M8 fails) |
| F-20 | CLOSED in code | integration.py:85-91 (transition), 109-110 (own summary) | none (TS24 is real-only) | Not executed (D-006 / no PR) |
| F-21 | CLOSED | the TS27 probe uses a disposable fixture only | test_factory.py:459 | YES |
| F-22 | CLOSED | engine.py:138, 424 | test_rework.py:266 | YES |
| F-24 | PARTIAL (as claimed) | TS02 asserts "Code Review: MISSING" (test_factory.py:43); TS04 asserts QA dispatch (:59) | — | Still missing: TS15 READY->IN_PROGRESS with an unfinished dependency; TS16 post-suite real-repository status; TS22 never runs `validate-story.sh` or the unmodified template; TS23 PATH test covers only the in-container re-entry |
| F-14, F-18, F-19, F-25..F-29 | Not claimed, still open | engine.py:297, 308 (hard-coded `US-FACTORY-003`, `TS24/TS25`); workflow.yaml:37 (Tester only in DEV_COMPLETE); cli.py:84-89 (non-atomic writes); Jenkinsfile injects no token; factory-runtime.sh mounts built from unquoted CSV paths | — | Carried forward as MINOR/INFO (R2-10) |

## 4. New findings

| ID | Severity | File:line | Summary | AC/TS |
|---|---|---|---|---|
| R2-01 | **MAJOR** (new, introduced by the rework) | factory/engine.py:160-165 (with 176-193, 377) | A merge commit counts as an evidence rewrite. Every record reaching the branch through a real merge is INVALID, `records()` raises, and the Story BLOCKs permanently, including develop after a PR merge | AC06, AC12, AC18, NFR06; no TS covers merges |
| R2-02 | **MAJOR** (pre-existing; makes F-04 PARTIAL) | factory/cli.py:122-125 | Jenkins feature-branch check fails on any stale or non-PASS historical gate, even when the status does not need it (IN_PROGRESS after more commits; DEV_COMPLETE during recovery) | AC18, AC12; TS21 covers only fresh records |
| R2-03 | MINOR | factory/tests/test_rework.py:101-120 | The TS13 "arbitrary login" subcase does not isolate the `approved_reviewers` check. Mutation M1 survives every TS13 test | TS13 (F-03 negative test) |
| R2-04 | MINOR (inherent residual) | factory/engine.py:326, 336-338; docs WORKFLOW-VALIDATION.md:86-88 | `source_commit` is declared by the producer. An out-of-order run committed later with a post-review `source_commit` PASSes. The docs overclaim | AC16 (residual) |
| R2-05 | MINOR (pre-existing) | factory/engine.py:442-444; factory/cli.py:104 | A hand-committed `BLOCKED` with an arbitrary `blocked_from` passes Jenkins, and the orchestrator then moves the Story to that state with no gate check | AC04, AC18 |
| R2-06 | MINOR | factory/cli.py:49-52, 66-67, 89 | The orchestrator rejects an uncommitted Story file but carries uncommitted edits of `factory/state/<story>.json` (e.g. `implementing_identity`) into its write | AC03 |
| R2-07 | MINOR | factory/engine.py:212 | `git check-ignore --no-index` reads the working-tree `.gitignore`/exclude, so the AC17 "gitignored" decision still depends on uncommitted files | AC17, AC01 spirit |
| R2-08 | INFO | factory/workflow.yaml (whole); engine.py:48 | The policy is self-hosted at the evaluated revision. A *committed* workflow edit, including `approved_reviewers`, changes gate semantics for that revision. Only human PR review guards it. This follows AC01 by design; the PO should be aware | AC01, AC13 |
| R2-09 | INFO | engine.py:160-174, 266-267 | Squash or rebase merges, or shallow clones (Jenkins option), make all evidence INVALID (fail-closed). The merge policy must be documented | AC18 |
| R2-10 | INFO | various | Carry-overs and small items: F-14, F-18, F-19, F-25, F-27, F-29; the integration `FIXTURE_OUTPUT` mktemp dir is never removed (factory-runtime.sh:37-39); per the AC13 literal, any public login's CHANGES_REQUESTED blocks Code Review; the in-container re-entry trusts `/.dockerenv` plus `/tmp` markers (a containerised host could satisfy them only with a deliberately set env var) | — |

### Details

**R2-01 (MAJOR): merges poison evidence.** `introduced()` requires
`git log --full-history --format=%H <rev> -- <path>` to list exactly the
`--diff-filter=A` commits (engine.py:164-165). With `--full-history`, a merge commit that is
not TREESAME to one of its parents for that path appears in the plain log but not in the
`--diff-filter=A` log. Every record introduced on one side of a true merge is then treated as
"history rewritten". `records()` calls `introduced()` for every record and the exception is not
caught there, so `gate()` (engine.py:377 sits outside the `try`), `jenkins()` (cli.py:115) and every
precondition BLOCK. Scratch reproduction (`review-r2/repro2.py`, real engine, canonical image):

- Case 1: build/lint/Unit PASS at DEV_COMPLETE, then `git merge --no-ff develop` (develop added
  `docs/other.md`; the implementation fingerprint is unchanged). Result: `Unit gate raised Block:
  INVALID evidence history rewritten`; `DEV_COMPLETE->TESTING` gives `['Unit Test: INVALID evidence
  history rewritten', ...]`; `jenkins` raises Block, so the stage exits 1.
- Case 2: Story DONE on the feature branch (develop-mode Jenkins gives `[]`), then merged into
  develop with a "Merge pull request" commit. Develop `jenkins` raises `INVALID evidence history
  rewritten`.

Failure scenario: US-FACTORY-003 reaches DONE on its feature branch and the PR is merged with a merge
commit, as this repository does (e.g. a3fb006). From then on, every develop build fails the Factory
Validation stage, which runs before Build. A routine "update branch from develop" on any feature
branch makes all of that Story's evidence permanently INVALID. Append-only records cannot repair it;
only a history rewrite can. No test exercises a merge, because the fixtures build linear histories
with `hash-object`.

**R2-02 (MAJOR): Jenkins false FAIL from stale history (F-04 incomplete).** cli.py:122-125 evaluates
`factory.gate()` for every gate that has *any* record and appends its reasons unless PASS/N/A. The
Story status check (cli.py:102-114) is already done above, so these lines turn every STALE or latest-FAIL
gate into a build failure. Reproduction (`repro1.py`): IN_PROGRESS with fresh build/lint/Unit gives `[]`.
After one more implementation commit it gives 5 `STALE_IMPLEMENTATION` errors. After recording a later
build FAIL it gives `build: INVALID FAIL result not PASS`. In recovery (all gates, fix commit, fresh
build/lint/Unit, DEV_COMPLETE) it gives 16 STALE errors for Code Review, Integration, Tester, QA and
Jenkins, which cannot be rerun before TESTING. AC18 fails a feature branch only for an unsupported status
or an *invalid* record. AC02 separates STALE from INVALID, and AC12 keeps stale records as history. The
F-04 regression test (test_rework.py:166) and TS07 (test_factory.py:734, test_rework.py:248) use only
freshly re-run gates, so they do not catch this. The code is unchanged since 42021fe.

**R2-03 (MINOR).** For the "arbitrary login" subcase the record keeps `producer_identity='MOCK_reviewer'`,
so `review identity mismatch` (engine.py:252) blocks even when line 250 is deleted. An attacker who
writes the record would set `producer_identity` to their own login. Add a subcase where the record
identity matches an unlisted COLLABORATOR login. The NONE/CONTRIBUTOR subcases are isolated (mutation M9
fails them), so the public throwaway-account attack is truly covered.

**R2-04 (MINOR, inherent).** `repro3.py`: a Tester record whose `source_commit` is its real pre-review
snapshot gives INVALID. The identical record claiming the post-review HEAD (same fingerprints) gives
`('PASS', [])`. Records committed out of order are detected deterministically. A record committed late
with a false `source_commit` cannot be detected without producer attestation. The docs sentence "A
prerequisite added later cannot repair an earlier out-of-order run" should say that the guarantee covers
*committed* records and declared snapshots.

**R2-05 (MINOR).** `repro4.py`: build/lint/Unit only, Story hand-committed as `BLOCKED`,
`blocked_from: QA`. `jenkins` gives `[]`. After clearing `blocked_by`, `transition BLOCKED->QA` gives `[]`.
The net is Jenkins at QA (TESTING->QA preconditions) and the full QA->DONE gate, so nothing reaches
DONE. The orchestrator and the stage both accept an unsupported `blocked_from`.

**R2-06 (MINOR).** Read from code: `state = json.loads(state_path.read_text())` (working tree) is updated
and written back (cli.py:89). Only the Story file is compared with its Git blob (cli.py:67). Gate evaluation
reads state from Git (engine.py:225-228), so the effect is limited to persisting uncommitted claims through
the sanctioned writer.

## 5. AC01–AC25

| AC | Status | Evidence |
|---|---|---|
| AC01 | IMPLEMENTED | workflow.yaml; Git-bound load engine.py:48; schema engine.py:56-96; every CLI command BLOCKs on invalid, missing or unreadable (TS17 tests). Hard-coded 003/TS24/25 remain (F-14) |
| AC02 | IMPLEMENTED | cli.py:178-191; states engine.py:379-393; named reasons |
| AC03 | IMPLEMENTED | cli.py:42-91: validate first, revision = HEAD, Story must be committed, YAML preserved, no agent launch, no commit/push. R2-06 minor; non-atomic writes (F-19) |
| AC04 | IMPLEMENTED | workflow.yaml:19-32 matches scrum-master.md:24-48; engine.py:436-451 (R2-05 minor) |
| AC05 | IMPLEMENTED | workflow.yaml:10-38; engine.py:262-314, 453-461 |
| AC06 | IMPLEMENTED (on feature branch) / broken after merge (R2-01) | workflow.yaml:26; engine.py:404-434, 304-306 |
| AC07 | IMPLEMENTED | require/Block throughout; non-PASS engine.py:302 |
| AC08 | IMPLEMENTED | engine.py:176-193, 262-314 |
| AC09 | IMPLEMENTED locally / NOT-TESTABLE-LOCALLY (real Jenkins) | engine.py:195-203; remotes.py:111-132 |
| AC10 | IMPLEMENTED | engine.py:116-125 |
| AC11 | IMPLEMENTED | engine.py:127-133 |
| AC12 | PARTIAL | Stale computation is correct (TS07/08/12/19). Stale history makes Jenkins fail (R2-02). Merges invalidate history (R2-01) |
| AC13 | IMPLEMENTED (logic, MOCK-verified) / NOT-TESTABLE-LOCALLY (real review) | engine.py:230-260; remotes.py:74-108. No PR exists yet |
| AC14 | IMPLEMENTED (code) | engine.py:272-278. Implementing-role execution evidence is still open (see §9) |
| AC15 | IMPLEMENTED | engine.py:295-301 |
| AC16 | IMPLEMENTED (committed ordering); residual R2-04 | engine.py:316-344, 382-386; cli.py:42-45 |
| AC17 | IMPLEMENTED | engine.py:104-108, 205-215 (R2-07 minor) |
| AC18 | PARTIAL / NOT-TESTABLE-LOCALLY | Stage after Checkout (Jenkinsfile diff); cli.py:94-128. R2-02 false FAIL; R2-01 develop FAIL after merge; F-25 token not injected; D-001 |
| AC19 | IMPLEMENTED | validate-story.sh:1-12; engine.py:135-152. `validate-story.sh` on Story 003 exits 0, last line PASSED |
| AC20 | IMPLEMENTED | `git diff --name-only a3fb006 0790d2f -- <9 scripts> docker-compose.test.yml` is empty; the Jenkinsfile diff is the single stage |
| AC21 | PARTIAL | Fixtures are disposable and MOCK-labelled. No post-suite real-repository status assertion (F-24) |
| AC22 | IMPLEMENTED | WORKFLOW-VALIDATION.md (token scope, recovery, merge-free ordering). R2-04 overclaim; merge policy undocumented (R2-01/R2-09) |
| AC23 | IMPLEMENTED | contract.env; requirements.txt hash pins; factory-runtime.sh (read-only mounts, exact write targets, version check, no host fallback); TS27 probe |
| AC24 | IMPLEMENTED in code / NOT-TESTABLE-LOCALLY | integration.py; not executed (no PR/review, D-006 credential) |
| AC25 | IMPLEMENTED | workflow.yaml:39-49; cli.py:151-174; TS28 |

## 6. TS01–TS28

| TS | Real test? | Note |
|---|---|---|
| TS01 | YES | QA->DONE `[]` with valid DoD evidence; intermediate transitions not each asserted |
| TS02 | YES | Asserts "Code Review: MISSING" for both dispatches and the transition |
| TS03 | YES (weak) | BLOCK asserted, reason not checked |
| TS04 | YES | Tester INVALID and QA dispatch BLOCK |
| TS05 | YES | Exact assertions for every sub-case (F-05 closed) |
| TS06 | YES | Fields, results, parse, unknown Story, gate command, UTC forms. Unknown gate not directly tested |
| TS07 | YES | STALE for all gates, history unchanged |
| TS08 | YES | `[]` baseline, then all STALE, plus the printed rerun order |
| TS09 | YES (partial) | Same-fingerprint case |
| TS10 | YES | F-08 sub-cases present |
| TS11 | YES | Recovery plus backdated/future plus rewritten record (mutation-killed) |
| TS12 | YES | Including C3 and state metadata |
| TS13 | YES | All contract sub-cases. The allow-list subcase is not isolated (R2-03) |
| TS14 | YES | F-07 sub-cases |
| TS15 | PARTIAL | No READY->IN_PROGRESS with an unfinished dependency (F-24) |
| TS16 | PARTIAL | BLOCK byte-identical, PASS record, YAML preservation, old revision refused. No post-suite real-repository check |
| TS17 | YES | Committed invalid/missing/unreadable workflow across all 12 commands; uncommitted edit ignored |
| TS18 | YES | Base 05004fc (equivalent for these files) |
| TS19 | YES | |
| TS20 | YES | |
| TS21 | PARTIAL | Fresh-record cases only; the stale-history case (R2-02) fails against the contract |
| TS22 | PARTIAL | `dor()` in-process; the shell script and the unmodified template are not exercised in the suite |
| TS23 | YES (partial PATH case) | Contract, single definition, Docker unavailable, invalid image, docker failure, hash mismatch, exit propagation for 12 commands × 4 codes plus cleanup failure |
| TS24 | EXCLUDED (honest) | Not in `unit_scenarios`; `ts_results.TS24` is written only by a completed real integration run; never faked |
| TS25 | EXCLUDED (honest) | D-001; never faked |
| TS26 | YES | |
| TS27 | YES | Linked-worktree fingerprints plus a real Docker probe of readonly/`--write`/ownership (ran in my unit run) |
| TS28 | YES | |

## 7. Focus sections

**AD-02.** The image is digest-pinned (contract.env:2), and a regex check runs before use
(factory-runtime.sh:10). The Python version is checked in the container (line 55). Dependencies are
installed with `--require-hashes --no-deps --only-binary=:all:`. Mounts: repository, common Git dir and
per-worktree Git dir are read-only (lines 16-18). `--write` mounts only the existing, non-symlink Story,
state and evidence targets (25-34). The container runs with `--read-only`, `--cap-drop ALL`,
`no-new-privileges` and the host uid:gid. There is no host-Python path. Exit status: non-unit commands end
with `docker run`, which is the script's last command. `unit` uses an EXIT trap that preserves `$?` even
when cleanup fails (TS23 test, 48 combinations, plus `rm` exit 88). Host tools used: bash, git, docker,
coreutils (mktemp, realpath, id, cp, chmod, stat, rm), grep. No `rg`, no python. The probe wrapper replaces
only the workload after the image argument and keeps all flags and mounts. My canonical `unit` run (exit 0)
included both real probe invocations.

**C1–C3.** policy.py:4-6 (latest non-COMMENTED per casefolded login), engine.py:241-245. APPROVED then
COMMENTED gives PASS. CHANGES_REQUESTED, including when followed by COMMENTED and from another reviewer,
gives BLOCK. DISMISSED gives BLOCK, and a re-approval clears it. TS12/C3: `safe/` is non-implementation,
while material keys and `contract_refs` blobs feed the contract fingerprint. Correct.

**Fail-closed.** No fail-open path found. Unreadable, invalid or missing inputs give BLOCK. GitHub or
Jenkins errors give NOT_EXECUTED. Ambiguous provenance gives INVALID. Exceptions inside `records()` propagate
as Block or a non-zero exit. The two MAJOR findings are *false* BLOCK/FAIL (R2-01, R2-02).

**Fingerprints and stale contract.** Unchanged and correct. The implementation fingerprint is computed over
`git ls-tree -r`, with unclassified paths counted as implementation. The contract fingerprint is canonical JSON
of the material keys plus `contract_refs` object ids. Only Tester and QA are `contract: true`. History records
are checked at their source revision (F-15).

**Security and SoD.** The reviewer must be on the policy allow-list (sonld1505), have write-level association,
and differ from the PR author, every commit author/committer and the implementing identity (casefolded). The
repository, base and head branch are pinned. The writer refuses Code Review records. Tester and QA must differ
from the implementing identity. Tokens are used only in headers, and errors are re-raised `from None`. Story ids
are regex-validated in the shell scripts, and arguments are passed positionally to `sh -c`. Residuals: R2-03..R2-08.

## 8. Commands run

| Command | Exit |
|---|---|
| `git -C <wt> status --porcelain` (start and end) | 0, empty |
| `git log`, `git diff --stat a3fb006 0790d2f`, `git diff 42021fe 0790d2f`, `git ls-tree`, `git show 42021fe:factory/cli.py` | 0 |
| `git diff --name-only a3fb006 0790d2f -- <9 AC20 scripts> docker-compose.test.yml` (empty) | 0 |
| `./scripts/factory-runtime.sh unit` (worktree root) | **0**. Ran 72 tests, OK. Every unit_scenario collected>0, failed=0, not-executed=0 (TS13=12, TS06=5, TS23=5) |
| `./scripts/factory-runtime.sh build` / `lint` | 0 / 0 ("All checks passed!") |
| `STORY_FILE=safe/stories/US-FACTORY-003.yaml ./scripts/validate-story.sh` | 0, last line `DEFINITION OF READY: PASSED` |
| `curl` GET api.github.com pulls?head=…feature/US-FACTORY-003-devops → `[]`; branches/… → `0790d2f` | 0 |
| `git clone` worktree → scratch `clone`, `f09`, mutants `m_M1..m_M9` | 0 |
| Merge semantics probe (`mergetest`, plain git) | 0 |
| `run.sh python repro1.py` (F-01, F-04, R2-02) | 0 |
| `run.sh python repro2.py` (R2-01) | 0 |
| `run.sh python repro3.py` (R2-04), `repro4.py` (R2-05) | 0 |
| Scratch clone `f09`: `./scripts/factory-runtime.sh --write US-FACTORY-003 orchestrate ... READY->IN_PROGRESS` (real Story; F-09) | 0, PASS; diff = status value only |
| Scratch clone `f09`: uncommitted workflow weakening + `--write ... IN_PROGRESS->DEV_COMPLETE` | 1, BLOCK (F-01) |
| Scratch clone `f09`: `jenkins --branch feature/US-FACTORY-003-devops` at IN_PROGRESS, no records | 0 |
| Mutation runs (`python -m unittest <tests>` in canonical image): M1 OK (survives); M2, M3, M4, M5, M6, M8, M9 FAILED (killed) | as stated |

`run.sh` is a scratch-only analysis wrapper. It runs the same digest-pinned image with the hash-pinned
requirements, mounts only the scratchpad, and is not canonical gate evidence. Scratch-clone commits use
per-command `GIT_*` environment variables only, with no `git config` writes.

## 9. Not verified

- Real GitHub review semantics (TS24/AC13/AC24): no PR exists and no credential is used. The behaviour
  of `author_association` and PENDING visibility follows GitHub documentation and is UNVERIFIED live.
- TS25 / real Jenkins (D-001). Credential injection for the stage is UNVERIFIED (F-25). The I-005
  decision is still needed.
- AC14 implementing-role evidence: the Codex sandbox lacks Docker. My host runs, like the orchestrator's,
  are local verification only and not gate evidence.
- Tester and QA have not run. This review replaces neither.
- AD-02 item 5 (no copy of the 002 runtime): no file named `python-runtime.sh` or `python-gate.py` is in
  the diff. I did not diff against the 002 worktree.
- Non-x86_64 hosts (wheel hash pins).
- R2-06 is from code reading only, with no reproduction.
