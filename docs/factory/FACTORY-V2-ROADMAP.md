# AI Agent Factory V2: PO master architecture decision (roadmap record)

| Field | Value |
|---|---|
| Decision | "PO MASTER ARCHITECTURE DECISION: AI AGENT FACTORY V2, AUTONOMOUS SOFTWARE DELIVERY FACTORY" |
| Decided by | Human PO, 2026-10-04 (given to the Claude orchestrator in session) |
| Recorded by | Claude orchestrator (PM/PO support, SM), 2026-10-04 |
| Status | **Approved target roadmap. Not implemented.** No Story, role file, constitution or code is changed by this record |
| Machine-readable form | `safe/roadmap.yaml` |

## 1. Scope of this record

This decision defines the target architecture after US-FACTORY-003. It does **not** modify, restart or re-contract
US-FACTORY-003, which stays governed by its existing approved contract. The current constitution (`CLAUDE.md`: Claude may act
only as PM/PO, BA, Scrum Master; Codex roles in `agents/codex/`) **stays in force** until a V2 Story changes it through
the normal workflow.

## 2. Roadmap (sequential)

| Order | Story | Title |
|---|---|---|
| 1 | US-FACTORY-003 | Central fail-closed workflow validator and supervised orchestrator. Complete under its existing contract |
| 2 | US-FACTORY-004 | Solution Architect Technical Authority |
| 3 | US-FACTORY-005 | Domain Engineering Agents |
| 4 | US-FACTORY-006 | Dynamic Multi-Agent Delivery Orchestration |
| 5 | US-FACTORY-007 | Quality, Governance and Release Pipeline |

Implement in order 003 → 004 → 005 → 006 → 007. A later Factory Story must not be implemented before its required
predecessor reaches the state required by the Factory workflow. Planning and contract preparation may happen earlier when
it is safe, meaning it does not modify the active Story's governed implementation.

When US-FACTORY-003 reaches its safe completion checkpoint, the orchestrator proposes US-FACTORY-004.

## 3. Target organisation

```text
PO / Human
    |
    v
Claude Orchestrator
    |
    +-- BA Agent
    |
    +-- Solution Architect Agent
    |      |
    |      +-- Backend Engineer
    |      +-- Frontend Engineer
    |      +-- Android Engineer
    |      +-- iOS Engineer
    |      +-- AI/ML Engineer
    |      +-- DevOps/Cloud Engineer
    |
    +-- Independent Code Reviewer
    +-- Tester
    +-- QA
    +-- CI/Jenkins
```

## 4. Authority model

| Role | Authority |
|---|---|
| PO | Product and governance authority |
| Claude | Workflow and orchestration authority |
| BA | Requirement analysis authority within approved product intent. Cannot silently change product scope or AC semantics |
| SA | Technical authority |
| Engineering agents | Implementation authority within their assigned domains and the approved technical architecture |
| Independent Reviewer | Independent verification authority |
| Tester | Functional and system verification authority |
| QA | Quality and release-readiness authority |
| CI/Jenkins | Automated reproducibility and enforcement authority |

## 5. Autonomy principle

Human involvement happens only when a decision crosses an explicit human authority boundary. Ordinary technical, workflow
and implementation decisions are **not** escalated to the PO.

| Question type | Route |
|---|---|
| Technical | Engineering → SA |
| Workflow | Agent → Claude |
| Product / governance | Claude / SA / BA → PO |

## 6. Fail-closed principle

No agent may: fabricate evidence; weaken ACs, tests, security controls or mandatory gates; silently expand its authority;
impersonate another role; approve its own independent verification; bypass a required human approval; mark a gate PASS
without the required evidence. Unknown authority or unverifiable evidence fails closed.

## 7. Durable state

All autonomous workflow state must be recoverable after SSH disconnect, Claude session loss, agent process loss, tmux
detach, and EC2 reboot where repository state survives. **Chat context is not authoritative state.**

Durable state must be enough to reconstruct: active Story; workflow phase; assigned agents; worktrees; branches; base/head
commits; dependency graph; completed gates; evidence; failures; rework; blockers; pending human decisions; next executable
nodes.

## 8. Notes for later Story refinement (orchestrator observations, not decisions)

These are inputs for refining US-FACTORY-004..007. The PO decides them in each Story.

1. **Constitution change.** Adding SA (and possibly the Independent Reviewer) as Claude roles changes `CLAUDE.md`
   ("Claude may operate only as PM/PO, BA, Scrum Master"). That is a permissions change (A+): plan, then human approval.
2. **"Independent Code Reviewer" vs AC13.** In US-FACTORY-003, Code Review PASS is an approved GitHub PR review by a human
   login, verified through the API. AI review is pre-review input only. V2 has to state whether the Independent Code
   Reviewer agent replaces, precedes or adds to that human gate.
3. **Mandatory Flow.** The V2 organisation has to keep Unit Test and Integration Test as explicit gates (NO UNIT TEST PASS =
   NO DEPLOY), and add an "SA Tech Gate" without reordering the existing gates.
4. **Engineering roles.** AI/ML Engineer is new. DevOps becomes "DevOps/Cloud". A Database role appeared in an earlier PO
   sketch but not in this decision. Confirm it during US-FACTORY-005 refinement.
5. **Orchestration defect carried into US-FACTORY-006:** DEF-004 (orchestrator and agent state not observable outside the
   session, no durable completion result).

## 9. Lean amendment (human PO, 2026-10-04): supersedes sections 2–8 where they conflict

- **Minimum Viable Factory (MVF), then freeze.** 003 is completed in Lean mode (one final fix + one independent
  verification + CI + PO PR approval). 004 and 005 are docs only (SA role, Lean constitution, one-page role files).
  006 is a supervised run wrapper plus a status command. 007 is the PR decision template, branch protection and a
  required Jenkins check. Everything else (Delivery DAG, SA Gate machinery, E1–E10 enforcement, readiness engine,
  post-merge verifier) is **deferred until a product Story needs it**.
- **Authority:** PO = product, priority, acceptance, budget/legal/privacy, accounts/admin, credentials, production, final
  merge. Claude = orchestration. SA = all normal technical decisions. Engineering = implementation. Validation =
  independent verification.
- **Flow:** requirement → triage → SA if useful → engineering → targeted tests → independent review (one fix, one
  re-review, then SA) → CI → PO PR approval → merge.
- After the MVF works, the next work is AI Tutor product development (needs SCOPE approval, I-001).
