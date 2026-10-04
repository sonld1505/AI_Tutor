# US-FACTORY-003 independent code review

| Field | Value |
|---|---|
| Story | US-FACTORY-003 (central fail-closed gate validator, revision-bound evidence, AD-02 runtime) |
| Implementation commit | `42021feb2ddfa1b048990adb5c20213340f13bf4` (branch `feature/US-FACTORY-003-devops`) |
| Base | `a3fb006` (origin/develop) |
| Worktree reviewed | `/home/ubuntu/AI_Tutor-worktrees/US-FACTORY-003-devops` (clean, at 42021fe) |
| Reviewer | independent review agent (Claude, read-only) |
| Date | 2026-10-04 |

> **This is NOT AC13 evidence.** Under AC13 the formal Code Review gate is an approved
> GitHub PR review by a human login (`sonld1505`) that differs from the implementation
> identity (`sonldfkr2911`), verified through the GitHub API. This report is only an
> independent input to that human review. It must not be recorded as a Code Review
> record, a DoD reference or any other gate evidence.

## 2. Verdict: **FAIL**

The C1–C3 review semantics, the AD-02 runtime, the fingerprints, stale-contract
isolation and most fail-closed paths are implemented well. I confirmed them by reading
the code and with reproductions. Four findings still meet the FAIL rules:

1. The gate policy is read from the working-tree file, or from any file passed with
   `--workflow`, and not from the Git-tracked definition at the evaluated revision. One
   uncommitted edit to `factory/workflow.yaml` lets the orchestrator pass a transition
   that the committed definition blocks, and the implementation fingerprint does not
   change. This contradicts AC01 and is fail-open (reproduced, F-01).
2. The out-of-order check (AC16) trusts timestamps that the producer writes into the
   record. A Tester record that predates Code Review is accepted if it carries a future
   timestamp, or if the hand-written Code Review record is backdated. Nothing ties the
   Code Review record's timestamp to the GitHub review's `submitted_at`. Reproduced, F-02.
3. AC13 independence accepts an APPROVED review from **any** GitHub login, in **any**
   repository named by the record. It checks neither `author_association` nor write
   permission, and does not pin the repository. On a public repository a throwaway
   account can produce Code Review PASS. Separation of duties is not enforced (F-03).
4. Several test scenarios claim coverage that the tests do not provide. In TS05 and TS08
   the asserted BLOCK comes from the fixture's always-missing DoD evidence, not from the
   condition under test. TS11, TS14, TS26, TS27 and TS10 leave required sub-cases
   untested (F-05 to F-08).

There is also a fail-closed correctness defect against AC18 (F-04). The Jenkins
Factory Validation stage fails every feature-branch build whose Story is
`IN_PROGRESS`, which is the normal state during development. Separately, the
orchestrator deletes every comment in the Story YAML on a transition (F-09), and those
comments hold the PO decisions, including AD-02.

## 3. Findings

| ID | Severity | File:line | Summary | AC/TS |
|---|---|---|---|---|
| F-01 | MAJOR | factory/engine.py:55; factory/cli.py:119,133 | Workflow policy read from the working tree or a `--workflow` override, not from Git at the evaluated revision. Uncommitted edits weaken gates and the fingerprint does not change | AC01, AC03, AC07, TS17 |
| F-02 | MAJOR | factory/engine.py:39-44, 285, 315, 320; 207-220 | Out-of-order detection relies on unverified, producer-declared timestamps. Future or backdated timestamps make an out-of-order Tester record satisfy TESTING->QA | AC16, AC12, TS11 |
| F-03 | MAJOR | factory/engine.py:207-220; factory/remotes.py:235-241 | Code Review accepts approval from any GitHub login (no author_association or permission check) on any repository the record names | AC13, decision D, TS13 |
| F-04 | MAJOR | factory/cli.py:91-95 + factory/engine.py:145-146 | Jenkins stage always FAILs a feature branch whose Story is IN_PROGRESS, because the DoR check requires status REFINED or READY | AC18, TS21 |
| F-05 | MAJOR | factory/tests/test_factory.py:58-68, 92-97 | TS05 "everything except Jenkins" and TS08 "stale blocks QA->DONE" pass only because the fixture DoD evidence is always missing. Neither the Jenkins nor the staleness condition is exercised | TS05, TS08, AC06, AC12 |
| F-06 | MAJOR | factory/tests/test_factory.py:116-127 | TS11 regression does not test TESTING->QA BLOCK, does not test that the old out-of-order Tester record fails after Code Review and Integration are added, and the recovery does not reach QA | TS11, AC16 |
| F-07 | MAJOR | factory/tests/test_factory.py:215-226, 337-345 | TS14 and TS26 omit N/A on a non-eligible gate, N/A not permitted by the Story, failed run recorded as N/A, US-FACTORY-003 N/A, Integration before Code Review, and Tester dispatch BLOCK with a wrong-producer Integration record | TS14, TS26, AC15 |
| F-08 | MAJOR | factory/tests/test_factory.py:347-351, 369-373, 107-114 | TS27 ownership assertion is a tautology and `--write` mounts are untested. TS10 never tests a sha256 mismatch on a tracked file, a gitignored path other than factory/logs/, .jsonl or archive files, or a record whose only PASS proof is a raw log | TS27, TS10, AC17, AC23 |
| F-09 | MAJOR | factory/cli.py:74-76 | Orchestrator transition rewrites the Story file with `yaml.safe_dump` and deletes all comments (PO decisions, AD-02 header, "keep this block LAST") | AC03 (record integrity), NFR06 |
| F-10 | MINOR | factory/cli.py:42-78, 118 | `orchestrate --revision X` validates an arbitrary revision but mutates the current working tree. Dispatch can PASS against an old revision while HEAD is stale | AC03, AC16 |
| F-11 | MINOR | factory/engine.py:216-218 | Login comparisons are case-sensitive. GitHub logins are case-insensitive and `implementing_identity` is typed by a human | AC13 |
| F-12 | MINOR (PLAUSIBLE) | factory/remotes.py:225-233 | GitHub's PR commits endpoint returns at most 250 commits. A truncated list is treated as complete, so the commit-author check can miss authors | AC13 |
| F-13 | MINOR | factory/engine.py:211 | A PENDING review (no `submitted_at`) visible to the token owner raises KeyError, so Code Review is INVALID. Fail-closed false BLOCK | AC13 |
| F-14 | MINOR | factory/engine.py:254, 265 | Hard-coded `{'TS24','TS25'}` exclusion and `story != 'US-FACTORY-003'`. `workflow.unit_scenarios` is ignored by the record check | AC01, AC25 |
| F-15 | MINOR | factory/cli.py:98-104; engine.py:247-248 | History records are re-validated against artifacts at the current revision. Editing an old artifact makes immutable history permanently INVALID and the Jenkins stage FAILs | AC12, NFR06 |
| F-16 | MINOR | factory/cli.py:168 | "Rerun order" is the static list of every gate, not the stale gates in order | AC12 |
| F-17 | MINOR | factory/engine.py:232-236, 261 | Tester and QA records are not checked against `producer_identity` ≠ implementing identity. Separation is by self-declared role string only | AC14 |
| F-18 | MINOR | factory/workflow.yaml:34 | Tester can be dispatched only in DEV_COMPLETE. After QA FAIL -> TESTING it can never be re-dispatched | AC04, AC05 |
| F-19 | MINOR | factory/cli.py:71-78 | Orchestrator writes are not atomic: event, then Story, then state. A failure partway leaves partial state | AC03 |
| F-20 | MINOR | factory/integration.py:28-105 | Integration exercises orchestrator dispatches only, no transition. The Integration record reuses Code Review artifacts instead of its own | AC24 |
| F-21 | MINOR | factory/tests/test_factory.py:369-373 | TS27 probe writes `factory/readonly-probe` into the real repository whenever the suite runs outside the canonical runtime | AC21 |
| F-22 | MINOR | factory/engine.py:140-141, 357-359 | An empty DoR or DoD template mapping makes the DoR or DoD check pass vacuously | AC06, AC19 |
| F-23 | MINOR | docs/factory/WORKFLOW-VALIDATION.md:4; CHANGELOG.md (last row) | Stale text: "Changes remain uncommitted pending an approved agent identity", CHANGELOG "Chưa commit", but the code is committed in 42021fe. Docs also omit the GitHub token permission scope | AC22 |
| F-24 | MINOR | factory/tests/test_factory.py:37-56, 228-241, 243-252, 597-613 | Weaker scenario coverage: TS02 does not assert "Code Review MISSING"; TS04 does not test QA dispatch; TS15 omits READY->IN_PROGRESS with an unfinished dependency; TS16 omits the post-suite real-repo git status; TS23 "no python on PATH" exercises only the in-container re-entry; TS22 never runs validate-story.sh itself or the unmodified template (DEF-001 AC09) | TS02, TS04, TS15, TS16, TS22, TS23 |
| F-25 | INFO | Jenkinsfile:28-32; factory/remotes.py:249 | The stage injects no `FACTORY_GITHUB_TOKEN` or Jenkins credential and requires an HTTPS `JENKINS_URL`. In Jenkins, Code Review and archive checks will be NOT_EXECUTED (fail-closed) unless they are configured outside the Jenkinsfile. UNVERIFIED (D-001) | AC18, TS25 |
| F-26 | INFO | factory/engine.py:269-270 | A Jenkins gate PASS is a repository-written record. It is not verified against Jenkins except for the archive hashes of its external artifacts | AC06 |
| F-27 | INFO | scripts/factory-runtime.sh:16,27,40 | `--mount` CSV values are built from unquoted paths. A path containing a comma breaks or alters mount options. Low risk | AC23 |
| F-28 | INFO | factory/tests/test_factory.py:395 | TS18 diffs against `05004fc`, not the actual base `a3fb006`. Equivalent in practice, because 05004fc..a3fb006 changes only CHANGELOG, DEVBOOK, raid.yaml and the Story | TS18 |
| F-29 | INFO | factory/workflow.yaml:3 | `agents/` (role prompts) is classified as non-implementation documentation. Acceptable, but it is a policy choice the PO should confirm | AC10 |

### Finding details

**F-01 (MAJOR): workflow definition not bound to Git.** `Factory.__init__` reads
`(self.root/'factory/workflow.yaml').read_text()` (engine.py:55), and `cli.py:119,133`
accepts `--workflow <any path>`. Evidence, Story and fingerprints come from Git
objects at `--revision`, but the policy that decides which gates a transition needs
comes from the working tree. The implementation fingerprint is computed from the Git
tree, so an uncommitted edit leaves it unchanged. The `--write` runtime still mounts the
whole repository read-only, so the modified working-tree file is the one that gets read.
*Reproduction* (scratchpad `repro.py` R1, fixture repository): with Unit PASS only,
`transition(DEV_COMPLETE->TESTING)` returns errors. After an **uncommitted** edit
setting `DEV_COMPLETE->TESTING: [Unit Test]`, a new `Factory` returns `[]`. The
fingerprint is unchanged and `git status` shows only ` M factory/workflow.yaml`.
Failure scenario: an operator, or an agent with a shell in the worktree, runs
`factory-runtime.sh --write US-X orchestrate ... --to TESTING` without Code Review or
Integration. The orchestrator writes the event and the status. The Jenkins
feature-branch check, which uses a clean checkout, would catch this later, so the
damage is bounded, but AC01 ("read only this definition"), AC03 and AC07 are not met.
TS17 itself shows the dependency: it edits the working-tree workflow without
committing and expects the change to take effect.

**F-02 (MAJOR): out-of-order evidence accepted through timestamps.** `_gate` keeps the
newest record (`max(..., key=timestamp_key)`). The check at line 320 then requires
each prerequisite to have a valid record with `timestamp <= r.timestamp`. Every
timestamp comes from the record itself. It is not compared with "now", with the commit
time of the record file, or, for Code Review, with the GitHub review `submitted_at`.
Code Review records cannot be produced by `write_record` (cli.py:30), so they are
always hand-written with a timestamp someone chose.
*Reproduction* R2a: a Tester record written before any Code Review record, but
timestamped `2099-01-01`. After Code Review and Integration are recorded,
`gate(Tester)` is `PASS`, and both `TESTING->QA` and QA dispatch return `[]`.
R2b: a Tester record at `2026-10-03T12:00Z`, then Code Review and Integration
records backdated to `2026-10-02`. Same result, `PASS`. R2c (control, honest
timestamps): `INVALID`, as intended.
This is the exact US-FACTORY-002 failure mode, which AC16 says must "never satisfy a
precondition". `write_record` mitigates it on the sanctioned path, because it stamps
`now` and checks prerequisites. The validator itself, which per AC08 must not trust a
record on its own, does not.

**F-03 (MAJOR): reviewer authority and repository not verified.** `review()` checks
the state, the latest non-comment review, CHANGES_REQUESTED, the forbidden logins and
the reviewed-commit fingerprint. The `repository` and `pull_request` values come from
the record (remotes.py:236-241) and are not pinned to the Story's repository, branch or
PR. The reviewer's `author_association` or permission is never checked. On a public
repository, any GitHub account can submit an "Approve" review, and the API returns
`state: APPROVED`. A second account, in the same repository or in a fork holding the
same commit, gives Code Review PASS. *Reproduction* R4: a review with
`author_association: NONE` is accepted, and the record carries no repository
constraint. This fails decision D and AC13's intent of an *independent* review. The
designated human reviewer, `sonld1505` per D-006, is not enforced anywhere.

**F-04 (MAJOR, fail-closed): Jenkins stage false FAIL at IN_PROGRESS.** `jenkins()`
evaluates the preconditions of every incoming edge of the current status. For
`IN_PROGRESS` that edge is `READY->IN_PROGRESS: [DoR, dependencies]`, and `dor()`
appends `DoR status must be REFINED or READY` (engine.py:145-146). *Reproduction* R5:
`jenkins(feature/US-999-devops)` at IN_PROGRESS returns `['DoR status must be REFINED
or READY']`. AC18 says the build fails only when the status is *not supported*. No
test covers the IN_PROGRESS case.

**F-05 (MAJOR): TS05 and TS08 pass for the wrong reason.** The fixture Story has
`definition_of_done: {implementation_complete: true, evidence: {}}`, so QA->DONE always
returns `DoD implementation_complete missing true/evidence` (R6).
`test_TS05...:62` (`all_gates()`, which *includes* Jenkins, followed by
`assertTrue(transition QA->DONE)`) and `test_TS08...:97` (asserting truthy errors after
an implementation change) both pass with or without the condition under test. The
"everything except Jenkins -> BLOCK" case, the "DoD key false -> BLOCK" case and TS08's
"validator prints the rerun order" are never exercised.

**F-06 (MAJOR): TS11 regression incomplete.** The test checks only that
DEV_COMPLETE->TESTING is blocked and later allowed. It never asserts TESTING->QA BLOCK.
It never records Code Review and Integration *without* rerunning Tester and QA to show
that the old out-of-order records do not satisfy, although the code does block that
case (R2c). The recovery stops at DEV_COMPLETE->TESTING instead of "reaches QA".

**F-07 (MAJOR): TS14 and TS26 sub-cases missing.** TS14 tests only the approved case
and the deletion of the four approval fields. The engine logic for non-eligible gates
is correct (R7, Tester N/A -> BLOCK) but untested, and so are "Story does not permit",
"failed run recorded as N/A" and "real US-FACTORY-003 permits no N/A". TS26 omits
"Integration before Code Review -> BLOCK", "Tester dispatch BLOCK when Integration is
from Tester/QA" and "Integration N/A for a fixture copy of this Story". The hard-coded
`story != 'US-FACTORY-003'` at engine.py:254 is never exercised.

**F-08 (MAJOR): TS27 and TS10 assertions do not test the scenario.**
`test_TS27_MOCK_linked_worktree:351` compares the uid of a file the test process itself
just created in its own temp directory, which is always equal. Nothing runs the helper
with `--write` to prove that only the Story, state and evidence targets are writable,
that a write elsewhere fails, or that host ownership holds. In TS10, every path uses
`sha256 '0'*64` on files that are absent, untracked, absolute or in factory/logs, so
the "tracked file with mismatched sha256" branch (engine.py:192) and the generic
`check-ignore` branch (engine.py:189-190) are never reached. .jsonl, archives and the
"only proof is a raw log" case are not tested.

**F-09 (MAJOR): Story comments destroyed.** `orchestrate` parses the Story blob and
writes `yaml.safe_dump(s, sort_keys=False)` (cli.py:75-76). *Reproduction* R3: two
comment lines before, zero after. The real US-FACTORY-003.yaml keeps the PO decisions
A–F, AD-02, the C1–C3 history and DoR notes in comments. Its first sanctioned
transition would remove all of them, plus the "keep this block LAST" ordering note.
The contract fingerprint is unaffected, because it is computed from parsed YAML.

## 4. AC01–AC25 matrix

| AC | Status | Evidence / note |
|---|---|---|
| AC01 | PARTIAL | workflow.yaml:1-48; schema engine.py:63-99; BLOCK on missing or invalid (cli.py:190). Not Git-bound and overridable (F-01); hard-coded TS24/25 and Story id (F-14) |
| AC02 | IMPLEMENTED | can-transition, can-dispatch, validate-gate, status (cli.py:162-175); states engine.py:313,326; reasons engine.py:199-271 |
| AC03 | PARTIAL | cli.py:42-80 validates first, writes only after validation, prints invocation, launches nothing. F-09 comment loss, F-10 `--revision`, F-19 non-atomic, F-01 policy source |
| AC04 | IMPLEMENTED | engine.py:369-384; workflow.yaml:16-29 matches scrum-master.md:27-50 |
| AC05 | IMPLEMENTED | workflow.yaml:8-15, 30-35; engine.py:386-394; producers engine.py:232-236 (F-18 usability) |
| AC06 | IMPLEMENTED | workflow.yaml:23; engine.py:338-367, 261-263, 269-270 (F-26 INFO) |
| AC07 | IMPLEMENTED | require/Block everywhere; non-PASS results engine.py:259; unknown Story engine.py:114-116. Uncaught classes (AttributeError) still exit non-zero |
| AC08 | IMPLEMENTED | engine.py:156-170 (types, modes), 222-266 (fields, fingerprints, checks, ac/ts results) |
| AC09 | IMPLEMENTED locally / NOT-TESTABLE-LOCALLY (Jenkins) | engine.py:172-180; remotes.py:244-265; cli.py:109-110 |
| AC10 | IMPLEMENTED | engine.py:119-128 (Git tree entries, unclassified = implementation) |
| AC11 | IMPLEMENTED | engine.py:130-136; workflow.yaml:4 |
| AC12 | PARTIAL | Stale propagation via prerequisites (engine.py:307-310) and per-record checks (237-244). History kept. Rerun order not computed (F-16); F-15 |
| AC13 | PARTIAL | C1/C2 correct (policy.py:4-6, engine.py:211-215). Reviewer authority and repository not enforced (F-03); F-11, F-12, F-13. Real verification UNVERIFIED (no credential) |
| AC14 | IMPLEMENTED (role-string level) | engine.py:232-236; cli.py:30. F-17. Implementing-role evidence still an open blocker |
| AC15 | IMPLEMENTED (logic) | engine.py:252-258; tests incomplete (F-07) |
| AC16 | PARTIAL | dispatch BLOCK writes nothing (cli.py:43-44); out-of-order check bypassable (F-02) |
| AC17 | IMPLEMENTED | engine.py:107-111, 182-192; tests incomplete (F-08) |
| AC18 | PARTIAL / NOT-TESTABLE-LOCALLY | Jenkinsfile stage after Checkout; cli.py:83-111. F-04 false FAIL; F-25 credentials; D-001 |
| AC19 | IMPLEMENTED | validate-story.sh:1-12 (STORY_FILE, last line); engine.py:138-154 covers DEF-001 AC01-AC08; create-worktree.sh unchanged |
| AC20 | IMPLEMENTED | `git diff --name-only a3fb006 42021fe -- <9 scripts> docker-compose.test.yml` returned nothing. The Jenkinsfile diff only adds the stage |
| AC21 | PARTIAL | Fixtures in temp directories, MOCK labels in fixtures.py and test names. No post-suite real-repo status check (F-24); F-21 |
| AC22 | PARTIAL | WORKFLOW-VALIDATION.md covers the topics. Stale "uncommitted" line; token permission scope missing (F-23) |
| AC23 | IMPLEMENTED | contract.env; requirements.txt (hash-pinned); factory-runtime.sh:10-55. See §6 |
| AC24 | PARTIAL / NOT-TESTABLE-LOCALLY | integration.py; workflow.yaml:40,45. Never executed (D-006); no transition exercised (F-20) |
| AC25 | IMPLEMENTED | cli.py:135-158; workflow.yaml:36-46; TS28 tests real failures |

## 5. TS01–TS28 matrix

| TS | Real test? | Note |
|---|---|---|
| TS01 | YES (partial) | Gates PASS and QA->DONE `[]`. Intermediate transitions and dispatches not each asserted |
| TS02 | YES (weak) | BLOCK asserted; "naming Code Review MISSING" not asserted |
| TS03 | YES (weak) | BLOCK asserted, reason not checked |
| TS04 | PARTIAL | Only Tester gate INVALID; QA dispatch not tested |
| TS05 | PARTIAL / TAUTOLOGICAL | Jenkins-missing case masked by DoD (F-05); RAID, blocked_by, depends_on and per-AC are real |
| TS06 | YES | Fields, results, parse, unknown Story, command. Unknown gate not directly tested |
| TS07 | YES | STALE for all gates; history unchanged (rerun test) |
| TS08 | TAUTOLOGICAL | F-05 |
| TS09 | YES (partial) | Same fingerprint at another commit stays valid; different fingerprint covered by TS07 |
| TS10 | PARTIAL | F-08 |
| TS11 | PARTIAL | F-06 |
| TS12 | YES | Includes C3 (safe/unrelated.md, contract_refs, material key, unclassified path) |
| TS13 | YES | All listed cases incl. APPROVED->COMMENTED PASS, CR->COMMENTED BLOCK, DISMISSED, unresolved, missing commit, NOT_EXECUTED. Reviewer authority not in contract list (see F-03) |
| TS14 | PARTIAL | F-07 |
| TS15 | YES (partial) | Dependency case missing (F-24) |
| TS16 | PARTIAL | Byte-identical BLOCK and PASS record are tested; post-suite real-repo status is not |
| TS17 | YES | All CLI commands BLOCK on an invalid workflow; missing file -> OSError |
| TS18 | YES | Script byte-equality and exact Jenkinsfile stage diff (base 05004fc, F-28) |
| TS19 | YES (partial) | All material keys and refs; non-material subset only (no key-order, formatting or DoD case) |
| TS20 | YES | Missing fields, local path, unknown system, credential, MOCK archive match and mismatch |
| TS21 | YES | IN_PROGRESS case absent (F-04) |
| TS22 | PARTIAL | dor() cases 1-3 tested in-process; the validate-story.sh interface and unmodified template are not tested by the unit suite |
| TS23 | PARTIAL | Contract and versions, single-contract search, Docker unavailable, invalid image, MOCK docker failure, pip hash mismatch. The PATH test exercises only the container re-entry |
| TS24 | EXCLUDED (honest) | Not in workflow `unit_scenarios` (workflow.yaml:46); docs line 34; CHANGELOG lists it as not executed. Never faked as PASS |
| TS25 | EXCLUDED (honest) | Same; D-001 |
| TS26 | PARTIAL | F-07 |
| TS27 | PARTIAL / TAUTOLOGICAL ownership | F-08. The linked-worktree fingerprint and read-only probe are real |
| TS28 | YES | Real build, lint and unit failures and pass via cli.py |

## 6. Focus sections

**AD-02 runtime.** The image is `python:3.12@sha256:4f80f792…` (contract.env:2). Local
`docker image inspect` gives amd64 with `PYTHON_VERSION=3.12.15`, matching
`FACTORY_PYTHON`. The version is checked again inside the container
(factory-runtime.sh:48). Dependencies are installed with
`--require-hashes --no-deps --only-binary=:all:` (line 49). There is no host-Python
path, and a missing Docker or a failed pull is BLOCK through `set -e`. The repository,
the common Git dir and the per-worktree Git dir are mounted read-only (lines 14-17).
`--write` adds exact existing, non-symlink targets for the Story, state and evidence
(19-29). The container runs with `--read-only --cap-drop ALL no-new-privileges` as the
host uid and gid. The in-container re-entry (lines 5-9) depends on `/.dockerenv` and a
marker in `/tmp`, which is acceptable. Gaps: no test covers `--write` (F-08), and F-27
(INFO).

**C1–C3.** policy.py:4-6 builds the latest non-COMMENTED review per login from the
chronologically sorted list (engine.py:211). APPROVED followed by COMMENTED stays
APPROVED (test line 187). CHANGES_REQUESTED followed by COMMENTED still blocks, for the
reviewer and for another reviewer (line 198). DISMISSED blocks, and a later re-approval
clears it (line 704). The TS12 safe/ exemption applies only outside material keys and
contract_refs: safe/ is non-implementation, and contract_refs blob ids enter the
contract fingerprint (engine.py:135). Tested at lines 129-167. **Correct.**

**Fail-closed.** These all give BLOCK or NOT_EXECUTED: a missing or invalid workflow,
unknown evidence types, a GitHub or Jenkins error (broad `except` -> `Block`), a missing
credential, YAML errors, non-PASS results, an unknown Story or gate, and an evaluation
exception (`_gate` returns INVALID). Exception classes that are not caught
(AttributeError, RecursionError) give a traceback and exit 1, which is still non-zero,
and validate-story.sh still prints `FAILED`. I found no default-True or
empty-means-PASS path in gate evaluation, apart from F-22 (an empty template). The
fail-open paths are F-01, F-02 and F-03.

**Fingerprints.** The implementation fingerprint is a sha256 over sorted
`[path, "mode type oid"]` entries from `git ls-tree -r`, leaving out the classified
prefixes and files. Unclassified paths count as implementation (TS12 `unknown.bin`).
The contract fingerprint hashes the canonical JSON of the material keys plus
`contract_refs` -> `rev-parse` oid. Stale implementation affects every
implementation-bound gate, and their dependents through prerequisites. Records are
append-only: the writer uses `open('x')`, and nothing deletes. The newest record wins.
/tmp, `..`, untracked, ignored, factory/logs and sha-mismatched artifacts are rejected
in code (engine.py:107-111, 186-192), though only partly tested (F-08).

**Stale contract.** Only `Tester` and `QA` have `contract: true` (workflow.yaml:13-14),
so a contract change stales only those two and their dependents. Changes to
non-material keys and safe/ files leave both fingerprints unchanged (TS12, TS19).
**Correct.**

**Security and separation of duties.** The reviewer is checked against the PR author,
every commit author and committer login, and the implementing identity. An unresolved
login is BLOCK. The writer refuses Code Review. Producer roles are checked per gate.
The orchestrator only prints invocations: there is no subprocess for agents, and no
commit, push or merge on the real repository. Fixture and integration commits are
plumbing objects in disposable repositories. Tokens go only into headers and are never
printed (exceptions are re-raised `from None`). Gaps: F-03, F-11, F-12, F-17, and role
identity is self-declared in general. Shell scripts quote their variables and validate
Story ids by regex. Symlinked write targets are refused.

## 7. Commands run (all read-only with respect to the repository)

| Command | Exit |
|---|---|
| `git -C <wt> log/status/diff --stat a3fb006 42021fe`, `git diff 05004fc a3fb006 --stat`, `git ls-tree` | 0 |
| `git diff --name-only a3fb006 42021fe -- <9 AC20 scripts> docker-compose.test.yml` (empty output) | 0 |
| `git ls-remote --heads origin feature/US-FACTORY-003-devops` (read-only network; outside the stated curl-only allowance, disclosed) -> `42021fe…` | 0 |
| `docker image inspect python:3.12@sha256:4f80f792…` | 0 |
| Reproductions: `TMPDIR=<scratchpad>/tmp PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<wt>/factory:<wt>/factory/tests python3 repro.py` (host Python 3.14 + PyYAML 6.0.3, **analysis only, not canonical-runtime evidence**) | 0 |
| `./scripts/factory-runtime.sh build` (from worktree root) | 0 |
| `./scripts/factory-runtime.sh lint` | 0 |
| `./scripts/factory-runtime.sh unit` | 0. Same total as the CHANGELOG (55 tests, OK); every unit_scenario collected>0 and passed. Passing does not cure the coverage gaps in F-05 to F-08 |
| `git status --porcelain` after the runs | 0, empty: worktree still clean |

## 8. Not verified

- Real GitHub API behaviour: the token's view of PENDING reviews, the 250-commit cap,
  and `author_association` for non-collaborator approvals. Based on GitHub's documented
  behaviour; no live call was made (no credential, and none was wanted).
- TS24 (real integration) and TS25 (real Jenkins, D-001); Jenkins credential wiring
  (F-25).
- AC14 implementing-role evidence: the Codex sandbox lacks Docker, so the host runs,
  including mine, are local verification only.
- AD-02 item 5 (no copy of the uncommitted 002 runtime). I did not diff against the 002
  worktree. No file named `python-runtime.sh` or `python-gate.py` exists in this diff.
- Behaviour on non-x86_64 hosts (wheel hash pins).
- Tester and QA have not run. This review does not replace them.
