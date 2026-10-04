# US-FACTORY-003: R3-01 analysis and rework brief (round 4 candidate)

| Field | Value |
|---|---|
| Finding | R3-01 (MAJOR), round-3 independent pre-review `US-FACTORY-003-code-review-r3-2026-10-04.md` |
| Commit analysed | `233b1e90146d90caef5cb4cc4e28e31b0970d1b6` (`feature/US-FACTORY-003-devops`), read-only |
| Author | Claude orchestrator (CLAUDE_BA analysis, CLAUDE_SM routing), 2026-10-04 |
| Status | **PREPARED, NOT DISPATCHED.** Round 4 needs PO approval. The PO also has to decide R3-02 first (see the R3-02 PO decision brief) so that round 4 is one rework, not two |
| Not | Not a Code Review record, not gate evidence, not AC13 |

## 1. Classification: implementation defect, no contract change required

R3-01 is an **implementation defect**. The current contract already decides the behaviour, if AC18 is read together with
AC16, AC22, AC06, NFR06 and TS11:

| Contract clause | What it says about an out-of-order record |
|---|---|
| AC16 | "Records produced by an out-of-order run are **kept as history** but never satisfy a precondition." The contract classifies them as non-authorising history, not as invalid records |
| AC22 | Documentation must describe recovery after out-of-order execution: return through the AC04 failure path, **keep the old evidence as history**, rerun the gates in order |
| NFR06, AC12 | Records are append-only. Nothing deletes or rewrites them, so an out-of-order record stays in the tree forever |
| AC06 | QA->DONE needs Jenkins PASS **including Factory Validation PASS** |
| TS11 | "the documented recovery path ... reaches QA" |
| AC18 (feature branch) | Fails the build when the recorded status is not supported by valid evidence "or any of its evidence records is **invalid**" |

If "invalid" in AC18 included out-of-order history, the documented recovery (AC22) could never reach DONE (AC06), because
the out-of-order record can't be removed (NFR06). The contract would then contradict itself. The only consistent reading
is the one the AC07/AC08 vocabulary already uses: "invalid" means a record that fails integrity (missing or empty field,
unparseable, wrong Story/gate, wrong producer or identity, bad source commit or fingerprint, provenance rewrite, ambiguous
latest record, bad artifact). A record that passes integrity but ran before its prerequisites is *history that never
authorises* (AC16).

`233b1e9` reports such a record as `INVALID <gate>: out-of-order historical record` in feature mode (`factory/cli.py:122-123`).
That contradicts AC16 and AC22. The round-2 code returned `[]` for the same scenario.

**BA interpretation (explicit, not silent).** This brief applies the reading above and does not change any AC text. It only
chooses between the two readings of an undefined word, so the PO should confirm it when approving round 4. If the PO
prefers the other reading, R3-01 becomes contract-level and must go through the same decision route as R3-02.

### No fail-open from the fix

A *required* gate is still evaluated through `preconditions()` → `gate()` in non-history mode. `gate()` checks the order of
the latest record itself (`engine.py:424`, `require(... precedes ... prior_record_valid ..., "out-of-order record")`). An
out-of-order latest record therefore still BLOCKs every transition, dispatch and Jenkins status check that needs that gate.
The fix only stops *superseded or not-currently-required* out-of-order history from failing the stage.

## 2. Rework instruction for Codex DevOps (round 4, when approved)

Scope: `factory/cli.py` (feature-mode Jenkins history loop), `factory/tests/*`, `docs/factory/WORKFLOW-VALIDATION.md`.
No change to the Story, the workflow definition semantics, AC20 protected paths or any other gate.

1. **Behaviour.** In feature mode, a historical record that passes `record(..., history=True)` but fails
   `prior_record_valid(..., history=True)` is reported as non-authorising history. The stage prints, for example,
   `HISTORY <gate>: out-of-order record kept, non-authorising (AC16)` to stdout. It must **not** be added to `errors` and
   must **not** fail the stage.
2. **Still fails (unchanged).** Integrity failures from `record()`, unknown gate, ambiguous latest record, provenance
   violations, required-gate failures from `preconditions()` (including an out-of-order *latest* record of a required gate
   through `engine.py:424`), external-archive unavailability.
3. **Tests (all MOCK-labelled, disposable fixtures, AC21):**
   - End-to-end documented recovery, Jenkins feature mode at every step. Start with Tester and QA run before Code Review, at
     QA. Then QA->DEV_COMPLETE (`DoD FAIL: missing independent review`), Code Review, Integration, Tester, QA rerun in
     order, then Jenkins record and DoD. Expected: Jenkins feature `[]` and exit 0 at DEV_COMPLETE, TESTING, QA and DONE.
     Validator QA->DONE `[]`. The out-of-order records are still present and unchanged.
   - Negative: the out-of-order record is the **latest** record of a gate required by the current status → Jenkins feature
     FAIL with `out-of-order record` (from `gate()`).
   - Negative: an integrity-invalid superseded record (for example a rewritten record or a wrong producer) → still FAIL.
   - Revise `test_TS11_MOCK_real_git_optional_out_of_order_pass_is_invalid` (`test_git_graph.py:223-227`). At IN_PROGRESS
     an out-of-order Tester record is non-authorising history: the stage passes with the HISTORY notice, and the next
     transition that needs Tester still BLOCKs.
   - Each new test must fail when run against `233b1e9` `cli.py` (prove the test detects the defect).
4. **Docs.** Remove the contradiction between `WORKFLOW-VALIDATION.md:182-183` ("INVALID records still fail, even when
   superseded") and `:233-236` (documented recovery). State that out-of-order history is reported but does not fail the
   feature stage, and that it never authorises.
5. **Gates before handing back.** Canonical host `./scripts/factory-runtime.sh unit` (not only in-container),
   build, lint, `validate-story.sh`, `git diff --check`, AC20 protected-path diff empty.

## 3. Other open findings: candidates for the same round (PO decides)

| ID | Severity | Note |
|---|---|---|
| R3-03 | MINOR | Align the feature-mode non-PASS allow-list (`cli.py:120`) with develop mode (`engine.py:322`), or the reverse. If R3-02 option B is approved, develop evaluates at the completion snapshot and the alignment belongs to the same change |
| R3-04 | MINOR | Add tests that kill the 3 surviving mutants (`engine.py:187`, `:361-367`, `:296-297`) |
| R2-05 | MINOR | Hand-committed BLOCKED / `blocked_from` not validated (`engine.py:477-482`, `cli.py:105`) |
| R2-07 | MINOR | `check-ignore --no-index` reads the working tree (`engine.py:237`) |
| R3-05 | INFO | CI time (88 tests ≈ 919 s) and duplicate develop error lines. Not a blocker |

R3-02 is **excluded** from this brief. It is contract-level and must not be sent to Codex until the PO decides.
