# Factory workflow validation (US-FACTORY-003)

This is Factory tooling, not product functionality. It does not close any defect,
RAID item or Story. The initial implementation was committed as `42021fe`.
This rework follows the independent pre-review FAIL of 2026-10-04; canonical
host validation and orchestrator commit remain separate steps.

`factory/workflow.yaml` **at the evaluated Git revision** is the policy definition.
Working-tree edits are ignored; there is no `--workflow` override. It defines states, transitions,
failure paths, dispatch prerequisites, producers, fingerprint classes, material
keys, external systems, N/A eligibility and Factory commands. Missing/unreadable
or invalid definitions block every entry point. Unknown evidence is never PASS.

Normal flow is DRAFT → REFINED → READY → IN_PROGRESS → DEV_COMPLETE → TESTING →
QA → DONE. Implementation requires DoR and DONE dependencies. DEV_COMPLETE needs
build, lint and Unit Test. Code Review requires Unit Test; Integration requires
Unit Test and independent Code Review; Tester dispatch requires all three; QA
requires Tester as well. Jenkins is a completion gate after QA. DONE additionally
requires every AC PASS in QA, DoD true with evidence per key, no blockers and DONE
dependencies. The workflow contains the supervised failure-return rules.

Run from the repository root, using the single runtime:

```bash
./scripts/factory-runtime.sh build
./scripts/factory-runtime.sh lint
./scripts/factory-runtime.sh unit
./scripts/factory-runtime.sh status --story US-101
./scripts/factory-runtime.sh can-transition --story US-101 --from READY --to IN_PROGRESS
./scripts/factory-runtime.sh can-dispatch --story US-101 --role CODEX_DEVOPS
./scripts/factory-runtime.sh validate-gate --story US-101 --gate 'Code Review'
STORY_FILE=safe/stories/US-101.yaml ./scripts/validate-story.sh
```

The Factory Unit Test command rejects any failure, skipped/not-executed test,
zero collection overall or zero collection for a workflow-listed scenario.
TS24 and TS25 are deliberately excluded. C1–C3 have executable tests against
the approved AC13 and TS12/TS13 contract. MOCK tests never produce real gate evidence.
No backend build/lint/unit scripts are substituted or weakened.

The sanctioned supervised mutation entry point is:

```bash
./scripts/factory-runtime.sh --write US-101 orchestrate --story US-101 --action dispatch --role CODEX_DEVOPS --identity APPROVED_AGENT_LOGIN
./scripts/factory-runtime.sh --write US-101 orchestrate --story US-101 --action transition --from READY --to IN_PROGRESS
```

The Story file, state JSON and evidence directory must exist. Provisioning and
committing those real management records belongs to the Scrum Master/human, not
this implementation. No write occurs on validation BLOCK. On PASS the command
records an event and prints the dispatch invocation; a human starts the agent.
It never launches an agent, commits, merges, pushes or deploys. Uncommitted Story or state
edits are rejected rather than overwritten. Orchestration requires the evaluated
revision to equal HEAD. Transitions edit only the single top-level status value,
re-parse to verify that nothing else changed, and preserve comments and key order.
State records include the implementing
role and approved identity. Commit produced records before subsequent evaluation;
Git objects, not uncommitted claims, are authoritative.

Gate records are JSON/YAML under `factory/evidence/<story>/`. Short Markdown
summaries are allowed; raw logs, JSONL, archives and fixture trees are rejected.
Record fields are `story_id`, `gate`, `result`, `producer_role`, `producer_identity`,
UTC `timestamp`, full `source_commit`, `implementation_fingerprint`,
`acceptance_contract_fingerprint` for contract gates, `checks`, `artifacts` and
`ac_results`/`ts_results` when applicable. Every implementing-role record
must include the exact Story-specific workflow `command`, including Integration
Test and N/A records. Other Stories require explicit command bindings; missing
bindings return NOT_EXECUTED rather than guessing commands. Local artifacts use relative `path`
and `sha256`; they must be tracked regular files, not ignored or outside the repo.
External artifacts use `system`, `job`, `build`, relative `path` and `sha256`.
Initially only Jenkins is allowed. References are supporting metadata, not PASS
proof. DoD `evidence` maps each DoD key to a verified artifact reference.

The writer fills commit/fingerprints/time itself, checks producers and artifacts,
and refuses to write Code Review claims from the implementing role:

```bash
./scripts/factory-runtime.sh --write US-101 write-evidence --story US-101 --record-file producer-result.json
```

Records are append-only. A new record does not rewrite history. Ordering uses Git
ancestry, never producer timestamps or Git author/committer dates. Each record path
must have one unique introduction commit in the evaluated history and unchanged
contents since introduction. A record's `source_commit` must strictly precede its
introduction. Every prerequisite must have been introduced at or before that source
snapshot, and its own prerequisite chain must be valid. The source tree thus hashes
the exact committed prerequisite records available to the producer. A prerequisite
added later cannot repair an earlier committed out-of-order record with its declared
source snapshot, even with backdated or future
record timestamps. Records committed together cannot authorise one another.
The latest record is the unique introduction descendant of all earlier records for
that gate; incomparable branches or duplicate records in one commit BLOCK rather
than picking an arbitrary winner. Complete history is required; insufficient Git
objects or ambiguous provenance BLOCK. Review IDs and `review_submitted_at` are
immutable references to the GitHub server response; the latter must match server
`submitted_at`. A review record claiming creation before server submission BLOCKs
as inconsistent; a later claimed timestamp alone never proves ordering. The
server-reviewed commit must itself contain valid Unit evidence.
This provides ordering through committed snapshots and the server-reviewed snapshot,
without claiming caller-controlled wall-clock values prove execution order.
The source snapshot is a producer declaration, not an execution attestation. A
producer who commits a record late and falsely declares a later valid snapshot
cannot be detected from Git ancestry alone; this mechanism does not prove the
wall-clock order of unrecorded runs.

The human PO's 2026-10-04 evidence provenance policy requires **merge commits only**
for Factory branch integration: `git merge --no-ff`, GitHub "Merge pull request",
and updates merging develop into a feature branch preserve implementation commits
and evidence introductions. Squash merge and rebase merge are prohibited.
GitHub administrators must disable the squash/rebase merge options in repository
settings and retain merge commits; changing those settings is a human admin action.
Jenkins must fetch complete history, including both merge parents, rather than a
shallow checkout. This implementation changes no GitHub setting or Git configuration.
The validator traces each record through every parent in the evaluated commit graph.
An unchanged record inherited from one or both merge parents keeps its unique
original introduction. Any content rewrite (including a merge resolution), deletion
and re-addition, or multiple independent introductions is INVALID. Missing source
commits, lost source ancestry after squash/cherry-pick/rebase, ambiguous introductions
and shallow history BLOCK with a reason naming the merge-commit-only policy.
Git cannot identify the command used to create an otherwise indistinguishable
graph; enforcement fails closed when record provenance cannot be established.
Historical stale
records remain available but do not authorise a transition. Raw local execution
logs belong under gitignored `factory/logs/<story>/<role>/`, never in evidence.
Historical artifact hashes are checked at their source revision; current records
must still match the evaluated revision. Rerun output lists only unsatisfied gates
in the workflow's prerequisite order.

Implementation fingerprints hash sorted Git tree entries (paths, modes and object
IDs), excluding explicitly classified non-implementation paths: `safe/`, evidence, process state,
listed documentation directories and named documentation files. Unclassified
paths count as implementation. Acceptance-contract fingerprints canonicalise
parsed material Story YAML keys with sorted keys and add Git object IDs for sorted
`contract_refs`. Formatting/comments and all non-material keys are ignored.
Implementation changes stale all bound gates and their dependents. Contract
changes stale Tester and QA and their dependents. Rerun in prerequisite order.

Code Review requires real read-only GitHub API verification at evaluation time.
The workflow pins repository `sonld1505/AI_Tutor` and the approved independent human
reviewer `sonld1505` (RAID D-006). The PR base repository must match and its head must
be `feature/<story>-<implementing-role>`. The chosen PR number identifies a PR only
within those constraints; the record cannot choose another repository or branch.
The reviewer needs OWNER, MEMBER or COLLABORATOR association and must differ from
the PR author, every commit author/committer, and the implementing identity. All
GitHub login comparisons, including latest-review grouping, ignore case.
The adapter paginates PR commits/reviews, checks the returned commit count against
the PR's server count (including GitHub's 250-commit cap), verifies independent logins, rejects
unresolved authors/committers, and compares the reviewed local commit fingerprint.
Unsubmitted PENDING reviews do not withdraw submitted decisions. Revisions predating
the authority policy cannot pass Code Review; no default reviewer authority exists.
`FACTORY_GITHUB_TOKEN` is supplied outside Git; values are never printed. Without
credentials/connectivity, review is NOT_EXECUTED. No live GitHub call was run by
this implementation dispatch. No new reviewer role exists; records use GITHUB.
Use a read-only fine-grained token restricted to this repository, with Pull requests:
Read and the automatically required Metadata: Read. It needs no write permission
and performs only GET requests. Configure it in the local environment or Jenkins
credential store; Jenkins administrators must inject it into the stage environment.
No credential value belongs in a record, document, command output or URL.
Permission reference: [GitHub list-reviews documentation](https://docs.github.com/en/rest/pulls/reviews#list-reviews-for-a-pull-request).
Commit completeness reference: [GitHub list-commits documentation](https://docs.github.com/en/rest/pulls/pulls#list-commits-on-a-pull-request).

`factory/policy.py` applies the approved C1–C3 contract. A reviewer's latest
non-comment review controls approval and change requests; later comments withdraw
neither. Comment-only and dismissed reviews supply no approval. Any reviewer's
latest non-comment CHANGES_REQUESTED blocks review. Material Story keys and
contract_refs changes produce STALE_CONTRACT for Tester/QA and downstream gates;
non-material classified changes stale nothing. Unclassified paths remain
implementation changes and fail closed.

N/A requires an eligible workflow gate, explicit Story permission, PO identity/date,
reason, verified durable decision reference and execution_status NOT_APPLICABLE.
Failed execution/missing tools/configuration are not N/A. US-FACTORY-003 allows none.

`Factory Validation` is the only Jenkinsfile addition, immediately after Checkout.
`factory-jenkins.sh` calls the same CLI. Feature branches validate the named Story's
status and evidence; other branches validate DONE Stories.
IN_PROGRESS checks readiness content and dependencies without applying the READY-only
admission status rule; the next DEV_COMPLETE transition still needs build/lint/Unit.
On feature branches, historical records are checked for integrity at their source
revision, separately from the gates required to support the current status.
STALE_IMPLEMENTATION/STALE_CONTRACT, superseded records and well-formed non-PASS
history for unrequired gates do not fail a supported status. INVALID records still
fail, even when superseded or unrelated to that status. Stale evidence never
authorises a required gate or transition. Develop-mode DONE validation is unchanged.
External references are
read from the Jenkins archive at `JENKINS_URL` (HTTPS, no credential-bearing URL).
Missing/inaccessible/mismatched archives block completion. This mechanism has not
been verified against a real Jenkins job. Optional authenticated archive reads use
JENKINS_API_USER and JENKINS_API_TOKEN from credential storage, never URL text.

The additive Integration command is registered as `factory_integration`:

```bash
./scripts/factory-runtime.sh integration --story US-FACTORY-003 --revision HEAD
```

It refuses to begin before Unit Test and real independent Code Review PASS. In a
disposable local clone it exercises schema load, supervised dispatch PASS/BLOCK and
a READY → IN_PROGRESS transition,
the evidence writer, shell DoR delegation, local Jenkins entry, both fingerprints
and stale detection after fixture Git object commits. Its GitHub check verifies
the actual Story's review through the real API. No MOCK adapters are used. The
output is retained in a host-owned disposable `/tmp/factory-integration-output.*`
directory and is explicitly NON-AUTHORITATIVE. A human must promote it through the
writer and commit durable evidence before evaluation. The command has not been
executed here. Failed attempts produce FAIL/NOT_EXECUTED structured per-step output;
promotion into Git-tracked evidence is a separate supervised writer operation.
Each attempt has its own short `integration-summary.md` with the component results;
it does not reuse Code Review artifacts. Promote and commit that summary first,
then use the writer to bind the result record to the current source revision. Neither
the disposable output nor its draft references authorise a gate before promotion.

The AD-02 runtime contract is `factory/runtime/contract.env`. Image and version
were selected from this clean worktree, pulled and checked independently. All
third-party Python dependencies are exact-version, SHA-256-pinned wheels, installed
with `--require-hashes --no-deps --only-binary=:all:`. These hashes currently target
Linux x86_64; unsupported platforms fail closed. Python's bundled standard library
and pip are part of the digest-pinned image. Host Python is never a fallback.
Repository and linked-worktree common Git metadata are read-only. Only explicitly
requested Story/state/evidence targets gain write mounts; `/tmp` is ephemeral
runtime/fixture storage. UID/GID match the invoking user. Nested shell delegation
reuses the marked, already-verified canonical container. US-FACTORY-002 must adopt
this contract during recovery; its uncommitted runtime was not read or copied.
The host-side canonical `unit` command first runs `scripts/factory-runtime-test.sh`:
two real Docker invocations of the helper on a disposable MOCK repository, including
`--write`. The workload is a labelled probe, while Docker's actual mounts and security
flags are preserved. It checks read access, denied writes outside the exact targets,
allowed Story/state/evidence writes, and host UID/GID ownership. A read-only report
is supplied to TS27; missing or failed probes fail the unit command. No probe writes
to the real repository. Direct in-container unit entry without this host probe report
fails TS27 instead of skipping it.

After out-of-order execution: return via an explicit failure path, for example
QA → DEV_COMPLETE with `DoD FAIL: missing independent review`; retain previous
records; rerun Unit Test, independent Code Review, Integration, Tester and QA in
workflow order. Jenkins/DoD then decide DONE. Nothing converts missing, stale,
failed, pending or not-executed evidence into deploy permission.
