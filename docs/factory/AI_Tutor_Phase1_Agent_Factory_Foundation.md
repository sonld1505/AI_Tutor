# AI Tutor --- Phase 1: AI Agent Factory Foundation

> **Deployment target:** AWS EC2 Ubuntu\
> **Process model:** SAFe-inspired delivery\
> **Management agents:** Claude Code --- PM/PO, BA, Scrum Master\
> **Engineering agents:** Codex CLI --- Backend, Frontend, Android, iOS,
> Tester, QA, DevOps\
> **CI/CD gatekeeper:** Jenkins\
> **Core policy:** **NO UNIT TEST PASS = NO DEPLOY**\
> **Production policy:** automated quality gates + explicit human
> approval

------------------------------------------------------------------------

## 1. Purpose

Phase 1 creates the foundation of an AI-native software factory for the
AI Tutor product. It does **not** attempt full autonomous software
delivery yet. Its purpose is to establish deterministic roles,
artifacts, workflow states, Git isolation, test gates, Jenkins
pipelines, and deployment controls before allowing multiple AI agents to
work concurrently.

The intended flow is:

``` text
Human Product Owner
        |
        v
Claude PM/PO
        |
        v
Epic -> Feature
        |
        v
Claude BA
        |
        v
User Story + Acceptance Criteria + Test Scenarios
        |
        v
Claude Scrum Master
        |
        v
Definition of Ready Gate
        |
        v
Codex Engineering Agents
        |
        v
Build + Lint + Unit Test
        |
        v
Pull Request
        |
        v
Codex Tester -> Codex QA
        |
        v
Jenkins Quality Gates
        |
        +---- FAIL ----> STOP / REWORK
        |
        v
DEV -> STG -> UAT -> Human Approval -> PROD
```

------------------------------------------------------------------------

# 2. Architectural Principles

## 2.1 Separation of responsibilities

Claude is the management/reasoning layer:

-   PM/PO
-   Business Analyst
-   Scrum Master

Codex is the engineering/execution layer:

-   Backend Developer
-   Frontend Developer
-   Android Developer
-   iOS Developer
-   Tester
-   QA
-   DevOps

Jenkins is the deterministic CI/CD gatekeeper.

No AI agent is allowed to decide by itself that a failed quality gate
can be ignored.

## 2.2 Git is the source of truth

Requirements, stories, code, tests, infrastructure configuration,
pipeline definitions, and relevant engineering documentation are version
controlled.

Chat history is **not** the system of record.

## 2.3 Artifact-based agent communication

Claude and Codex communicate through repository artifacts such as:

``` text
safe/stories/US-001.yaml
safe/features/F-001.yaml
docs/architecture/
tests/
Jenkinsfile
```

An engineering agent should not need Claude's hidden reasoning or
previous chat history to understand a task.

## 2.4 Fail closed

When information or validation is missing:

``` text
UNKNOWN != PASS
```

Examples:

-   Acceptance Criteria missing -\> development blocked.
-   Unit tests not executed -\> deployment blocked.
-   Unit tests failed -\> deployment blocked.
-   Security gate failed -\> promotion blocked.
-   UAT approval missing -\> Production blocked.

## 2.5 Production isolation

Claude and Codex must not possess direct Production credentials.

Production access should be controlled through Jenkins credentials, AWS
IAM roles, AWS Secrets Manager or equivalent secret management.

Production requires human approval.

------------------------------------------------------------------------

# 3. Target EC2 Repository Structure

Use the following structure:

``` text
/home/ubuntu/AI_Tutor/
|
|-- context/
|   |-- product.md
|   |-- architecture.md
|   |-- business-rules.md
|   `-- glossary.md
|
|-- agents/
|   |-- claude/
|   |   |-- pm-po.md
|   |   |-- ba.md
|   |   `-- scrum-master.md
|   |
|   `-- codex/
|       |-- backend.md
|       |-- frontend.md
|       |-- android.md
|       |-- ios.md
|       |-- tester.md
|       |-- qa.md
|       `-- devops.md
|
|-- safe/
|   |-- epics/
|   |-- features/
|   |-- stories/
|   |-- pi-objectives/
|   |-- sprints/
|   `-- templates/
|       |-- epic.yaml
|       |-- feature.yaml
|       |-- story.yaml
|       |-- definition-of-ready.yaml
|       `-- definition-of-done.yaml
|
|-- factory/
|   |-- config/
|   |-- orchestrator/
|   |-- state/
|   `-- logs/
|
|-- backend/
|-- frontend/
|-- android/
|-- ios/
|
|-- tests/
|   |-- unit/
|   |-- integration/
|   |-- e2e/
|   `-- performance/
|
|-- infrastructure/
|   |-- docker/
|   |-- terraform/
|   `-- aws/
|
|-- jenkins/
|   `-- scripts/
|
|-- scripts/
|   |-- validate-story.sh
|   |-- build.sh
|   |-- lint.sh
|   |-- unit-test.sh
|   |-- integration-test.sh
|   |-- security-scan.sh
|   |-- quality-gate.sh
|   |-- build-artifact.sh
|   |-- deploy.sh
|   `-- create-worktree.sh
|
|-- CLAUDE.md
|-- AGENTS.md
|-- Jenkinsfile
|-- Makefile
|-- docker-compose.yml
|-- .gitignore
`-- README.md
```

------------------------------------------------------------------------

# 4. Bootstrap the Foundation on EC2

SSH into EC2 and enter the project:

``` bash
cd /home/ubuntu/AI_Tutor
```

Create the directories:

``` bash
mkdir -p \
  context \
  agents/claude \
  agents/codex \
  safe/{epics,features,stories,pi-objectives,sprints,templates} \
  factory/{config,orchestrator,state,logs} \
  scripts \
  jenkins/scripts \
  backend \
  frontend \
  android \
  ios \
  tests/{unit,integration,e2e,performance} \
  infrastructure/{docker,terraform,aws}
```

Install useful basic tools if needed:

``` bash
sudo apt update
sudo apt install -y git tree curl unzip jq
```

Verify:

``` bash
tree -L 3
```

Initialize Git if this is not already a repository:

``` bash
git init
git branch -M main
```

------------------------------------------------------------------------

# 5. Claude Constitution --- `CLAUDE.md`

Create `/home/ubuntu/AI_Tutor/CLAUDE.md`:

``` markdown
# AI Tutor — Management Agent Constitution

## Delivery Model

This project follows a SAFe-inspired delivery model:

Portfolio
-> Epic
-> Feature
-> User Story
-> Engineering Task

## Claude Roles

Claude may operate only as:

1. PM/PO
2. Business Analyst
3. Scrum Master

Claude does not implement production application code.

## PM/PO Responsibilities

- Maintain Product Vision
- Maintain Roadmap
- Define and refine Epics
- Define Features
- Prioritize backlog
- Define PI Objectives
- Define business value
- Support release planning
- Resolve product-level questions

PM/PO MUST NOT:

- Implement production code
- Bypass QA
- Bypass Jenkins
- Mark failed tests as acceptable
- Deploy software directly

## Business Analyst Responsibilities

The BA converts Features into implementation-ready User Stories.

Every Story must contain:

- Business context
- Description
- Business value
- Acceptance Criteria
- Functional requirements
- Relevant non-functional requirements
- Dependencies
- API impact
- UI impact
- Data impact
- Security/privacy impact
- Test scenarios

If a material requirement is ambiguous:

STOP.

Record the ambiguity and request clarification.

Do not allow Codex to invent product requirements.

## Scrum Master Responsibilities

Manage:

- PI execution
- Sprint backlog
- Story status
- Dependencies
- Risks
- Blockers
- Definition of Ready
- Definition of Done
- Delivery flow
- Retrospective actions

A Story cannot enter development unless Definition of Ready passes.

A Story cannot become DONE unless Definition of Done passes.

## Mandatory Flow

Requirement
-> Refinement
-> Definition of Ready
-> Design
-> Development
-> Unit Test
-> Code Review
-> Integration Test
-> QA
-> Jenkins Quality Gate
-> Environment Promotion

## Critical Quality Policy

NO UNIT TEST PASS = NO DEPLOY.

No Claude role may override Jenkins quality gates.

Production always requires explicit human approval.
```

------------------------------------------------------------------------

# 6. Codex Constitution --- `AGENTS.md`

Create `AGENTS.md`:

``` markdown
# AI Tutor — Engineering Agent Constitution

## Engineering Roles

Codex may operate as:

- Backend Developer
- Frontend Developer
- Android Developer
- iOS Developer
- Tester
- QA
- DevOps

Every invocation must have one clearly identified role.

## Mandatory Reading Before Work

Before implementing a Story, the agent must read:

1. AGENTS.md
2. Its role file under agents/codex/
3. Relevant User Story
4. Acceptance Criteria
5. Relevant architecture/context documentation

## Git Policy

Never implement directly on:

- main
- develop

Use a dedicated branch/worktree.

Naming convention:

feature/<story-id>-<role>

Examples:

feature/US-101-backend
feature/US-101-frontend
feature/US-101-android
feature/US-101-ios

## Requirement Policy

Never silently invent missing requirements.

When a material requirement is unclear:

STOP.

Document the question and return it to BA/PM.

## Mandatory Engineering Validation

Before declaring work complete:

1. Build
2. Lint/static checks
3. Unit tests
4. Relevant security checks
5. Review git diff
6. Check Acceptance Criteria
7. Report evidence

## Deployment Policy

NO UNIT TEST PASS = NO DEPLOY.

Agents may not bypass Jenkins.

Agents may not directly deploy Production.

Production secrets must not be available to normal engineering agents.
```

------------------------------------------------------------------------

# 7. Claude Role Definitions

## 7.1 `agents/claude/pm-po.md`

``` markdown
# PM/PO Agent

## Mission

Translate Product Vision into prioritized, measurable delivery objectives.

## Responsibilities

- Product Vision
- Roadmap
- Epic definition
- Feature definition
- Business value
- Backlog priority
- PI Objectives
- Release planning
- Scope decisions

## Outputs

- safe/epics/*.yaml
- safe/features/*.yaml
- safe/pi-objectives/*.yaml
- prioritized backlog

## Rules

Do not write production code.
Do not override technical quality gates.
Do not mark a Story DONE.
Do not deploy.
```

## 7.2 `agents/claude/ba.md`

``` markdown
# Business Analyst Agent

## Mission

Transform Features into unambiguous, testable User Stories.

## Required Story Content

- User/business goal
- Business value
- Detailed description
- Acceptance Criteria
- Functional requirements
- Relevant NFRs
- Dependencies
- API impact
- UI impact
- Data impact
- Security/privacy considerations
- Test scenarios

## Rules

Do not invent unresolved business behavior.

If ambiguity affects implementation or testing:
- mark the Story BLOCKED or DRAFT
- record the open question
- request PM/PO or human clarification

Only recommend READY when DoR passes.
```

## 7.3 `agents/claude/scrum-master.md`

``` markdown
# Scrum Master Agent

## Mission

Protect delivery flow and enforce agreed process.

## Responsibilities

- Sprint planning support
- Sprint backlog
- Story state
- Dependency tracking
- Risk tracking
- Blocker tracking
- DoR validation
- DoD validation
- Retrospective actions
- PI progress

## Rules

Never move DRAFT directly to IN_PROGRESS.

Allowed normal flow:

DRAFT
-> REFINED
-> READY
-> IN_PROGRESS
-> DEV_COMPLETE
-> TESTING
-> QA
-> DONE

Failed validation returns work to an appropriate earlier state.

DONE requires DoD PASS.
```

------------------------------------------------------------------------

# 8. Codex Role Definitions

## 8.1 Backend --- `agents/codex/backend.md`

``` markdown
# Backend Developer Agent

Role: Senior Backend Engineer

## Responsibilities

- API implementation
- Domain/business logic
- Database integration
- Authentication/authorization
- Error handling
- Backend unit tests
- Backend integration tests
- API documentation

## Primary Ownership

backend/**
tests/unit/backend/**
tests/integration/backend/**

## Normally Forbidden

frontend/**
android/**
ios/**

Do not change infrastructure unless the Story explicitly requires it and DevOps ownership is coordinated.

## Completion Gate

- Build PASS
- Lint PASS
- Unit Test PASS
- Relevant integration tests PASS
- Acceptance Criteria checked
- git diff reviewed
```

## 8.2 Frontend --- `agents/codex/frontend.md`

``` markdown
# Frontend Developer Agent

Role: Senior Web Frontend Engineer

## Ownership

frontend/**
tests/unit/frontend/**
tests/integration/frontend/**

## Responsibilities

- Web UI
- State management
- API integration
- Validation
- Accessibility
- Responsive behavior
- Unit/component tests

Do not alter backend contracts without explicit coordination.
```

## 8.3 Android --- `agents/codex/android.md`

``` markdown
# Android Developer Agent

Role: Senior Android Engineer

## Ownership

android/**
tests/unit/android/**

## Responsibilities

- Android application
- Camera/device integration
- API integration
- Local state
- Permissions
- Unit tests
- UI/instrumentation tests where appropriate

Privacy-sensitive capabilities such as camera use must follow approved requirements.
```

## 8.4 iOS --- `agents/codex/ios.md`

``` markdown
# iOS Developer Agent

Role: Senior iOS Engineer

## Ownership

ios/**
tests/unit/ios/**

## Responsibilities

- iOS application
- Camera/device integration
- API integration
- Permissions
- Local state
- Unit/UI tests

Do not invent privacy or permission behavior.
```

## 8.5 Tester --- `agents/codex/tester.md`

``` markdown
# Tester Agent

## Mission

Verify implemented behavior independently against requirements.

## Responsibilities

- Derive test cases from Acceptance Criteria
- Functional testing
- Negative testing
- Boundary testing
- Integration testing
- Regression selection
- E2E testing
- Test evidence
- Defect creation

A test failure must not be silently converted into PASS.
```

## 8.6 QA --- `agents/codex/qa.md`

``` markdown
# QA Agent

## Mission

Evaluate whether implementation and evidence satisfy quality policy.

## Responsibilities

- AC traceability
- Test evidence review
- Quality gate review
- Defect trend review
- Regression coverage
- DoD evidence
- Release quality assessment

QA should not silently repair business logic while reviewing it.

If implementation is incorrect, return it to Development.
```

## 8.7 DevOps --- `agents/codex/devops.md`

``` markdown
# DevOps Agent

## Ownership

infrastructure/**
jenkins/**
scripts/**
Jenkinsfile
docker-compose.yml

## Responsibilities

- CI/CD
- Docker
- Jenkins
- Infrastructure as Code
- Environment configuration
- Deployment automation
- Observability
- Rollback mechanisms

## Security Rules

Never commit secrets.
Never print secrets into logs.
Prefer IAM roles and managed secret stores.
Production deployment must require human approval.
No deployment may bypass mandatory test gates.
```

------------------------------------------------------------------------

# 9. SAFe Artifact Templates

## 9.1 Epic --- `safe/templates/epic.yaml`

``` yaml
id: EPIC-XXX
title: ""
status: DRAFT

problem_statement: ""

business_outcome: ""

business_value: ""

success_metrics: []

features: []

risks: []

dependencies: []

owner: PM_PO
```

## 9.2 Feature --- `safe/templates/feature.yaml`

``` yaml
id: F-XXX
epic: EPIC-XXX
title: ""
status: DRAFT

description: ""

business_value: ""

benefit_hypothesis: ""

acceptance_criteria: []

non_functional_requirements: []

dependencies: []

stories: []
```

## 9.3 Story --- `safe/templates/story.yaml`

``` yaml
id: US-XXX

title: ""

epic: ""
feature: ""

status: DRAFT
priority: medium
story_points: null

business_value: ""

description: ""

acceptance_criteria:
  - id: AC01
    description: ""

functional_requirements: []

non_functional_requirements: []

dependencies: []

components:
  backend: false
  frontend: false
  android: false
  ios: false
  infrastructure: false

api_impact: false
database_impact: false
security_impact: false
privacy_impact: false

test_scenarios: []

open_questions: []

definition_of_ready:
  business_value_defined: false
  story_defined: false
  acceptance_criteria_defined: false
  dependencies_identified: false
  test_scenarios_defined: false
  architecture_reviewed: false
  estimated: false
```

------------------------------------------------------------------------

# 10. Definition of Ready

Create `safe/templates/definition-of-ready.yaml`:

``` yaml
definition_of_ready:
  business_value_defined: true
  story_defined: true
  acceptance_criteria_defined: true
  dependencies_identified: true
  architecture_reviewed: true
  test_scenarios_defined: true
  estimation_completed: true

required_result:
  all: true
```

The factory rule is:

``` text
Any mandatory DoR item false
        |
        v
Story NOT READY
        |
        v
Do not assign to Codex
```

------------------------------------------------------------------------

# 11. Definition of Done

Create `safe/templates/definition-of-done.yaml`:

``` yaml
definition_of_done:
  implementation_complete: true
  code_review_passed: true
  build_passed: true
  lint_passed: true
  unit_tests_passed: true
  integration_tests_passed: true
  acceptance_criteria_passed: true
  security_scan_passed: true
  qa_passed: true
  documentation_updated: true

required_result:
  all: true
```

`DONE` is a verified state, not an agent opinion.

------------------------------------------------------------------------

# 12. Story State Machine

Use:

``` text
DRAFT
  |
  v
REFINED
  |
  | DoR PASS
  v
READY
  |
  v
IN_PROGRESS
  |
  v
DEV_COMPLETE
  |
  | Unit Test PASS
  v
TESTING
  |
  v
QA
  |
  | Jenkins + DoD PASS
  v
DONE
```

Failure paths:

``` text
Unit Test FAIL -> IN_PROGRESS
Functional Test FAIL -> IN_PROGRESS
QA FAIL -> IN_PROGRESS / TESTING
DoD FAIL -> appropriate previous state
Requirement ambiguity -> DRAFT/REFINED
```

------------------------------------------------------------------------

# 13. Git Strategy

Recommended baseline:

``` text
main
|
+-- develop
|
+-- feature/US-101-backend
+-- feature/US-101-frontend
+-- feature/US-101-android
+-- feature/US-101-ios
|
+-- release/<version>
```

Suggested semantics:

-   `main`: Production baseline.
-   `develop`: integrated development baseline.
-   `feature/*`: isolated Story/component implementation.
-   `release/*`: release candidate used for stabilization/promotion.

Do not rely solely on branch names for security. Protect important
branches in the Git hosting platform and require PR/review/status
checks.

------------------------------------------------------------------------

# 14. Git Worktrees for Parallel Agents

Create a worktree root:

``` bash
mkdir -p /home/ubuntu/AI_Tutor-worktrees
```

Example Backend worktree:

``` bash
cd /home/ubuntu/AI_Tutor

git worktree add \
  /home/ubuntu/AI_Tutor-worktrees/US-101-BE \
  -b feature/US-101-backend \
  develop
```

Frontend:

``` bash
git worktree add \
  /home/ubuntu/AI_Tutor-worktrees/US-101-FE \
  -b feature/US-101-frontend \
  develop
```

Android:

``` bash
git worktree add \
  /home/ubuntu/AI_Tutor-worktrees/US-101-Android \
  -b feature/US-101-android \
  develop
```

iOS:

``` bash
git worktree add \
  /home/ubuntu/AI_Tutor-worktrees/US-101-iOS \
  -b feature/US-101-ios \
  develop
```

Run Codex independently:

``` bash
cd /home/ubuntu/AI_Tutor-worktrees/US-101-BE
codex
```

A different terminal:

``` bash
cd /home/ubuntu/AI_Tutor-worktrees/US-101-FE
codex
```

List worktrees:

``` bash
git worktree list
```

Remove one after merge:

``` bash
git worktree remove /home/ubuntu/AI_Tutor-worktrees/US-101-BE
```

------------------------------------------------------------------------

# 15. Story Validation Script

Create `scripts/validate-story.sh`:

``` bash
#!/usr/bin/env bash
set -euo pipefail

STORY_FILE="${STORY_FILE:-}"

if [ -z "$STORY_FILE" ]; then
  echo "STORY_FILE is required."
  echo "Example: STORY_FILE=safe/stories/US-101.yaml ./scripts/validate-story.sh"
  exit 1
fi

if [ ! -f "$STORY_FILE" ]; then
  echo "Story not found: $STORY_FILE"
  exit 1
fi

echo "Validating story: $STORY_FILE"

required_patterns=(
  "^id:"
  "^title:"
  "^status:"
  "^acceptance_criteria:"
  "^test_scenarios:"
  "^definition_of_ready:"
)

for pattern in "${required_patterns[@]}"; do
  if ! grep -q "$pattern" "$STORY_FILE"; then
    echo "Missing required section matching: $pattern"
    exit 1
  fi
done

if grep -A20 "^definition_of_ready:" "$STORY_FILE" | grep -q "false"; then
  echo "DEFINITION OF READY: FAILED"
  exit 1
fi

echo "DEFINITION OF READY: PASSED"
```

Make executable:

``` bash
chmod +x scripts/validate-story.sh
```

This is a Phase-1 lightweight validator. A later phase should replace
text matching with a proper YAML/JSON Schema validator.

------------------------------------------------------------------------

# 16. Build Script

Create `scripts/build.sh`:

``` bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== BUILD ==="

if [ -f backend/pom.xml ]; then
  (cd backend && mvn -B -DskipTests package)
fi

if [ -f backend/package.json ]; then
  (cd backend && npm ci && npm run build --if-present)
fi

if [ -f frontend/package.json ]; then
  (cd frontend && npm ci && npm run build)
fi

if [ -f android/gradlew ]; then
  (cd android && chmod +x gradlew && ./gradlew assembleDebug)
fi

echo "BUILD PASSED"
```

------------------------------------------------------------------------

# 17. Lint Script

Create `scripts/lint.sh`:

``` bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== LINT / STATIC CHECK ==="

if [ -f backend/package.json ]; then
  (cd backend && npm run lint --if-present)
fi

if [ -f frontend/package.json ]; then
  (cd frontend && npm run lint --if-present)
fi

if [ -f android/gradlew ]; then
  (cd android && ./gradlew lint)
fi

echo "LINT PASSED"
```

------------------------------------------------------------------------

# 18. Mandatory Unit Test Gate

Create `scripts/unit-test.sh`:

``` bash
#!/usr/bin/env bash
set -uo pipefail

echo "================================"
echo " AI Tutor — Unit Test Gate"
echo "================================"

FAILED=0
FOUND=0

if [ -f backend/pom.xml ]; then
  FOUND=1
  echo "[Backend/Maven] Unit tests"
  (cd backend && mvn -B test) || FAILED=1
fi

if [ -f backend/package.json ]; then
  FOUND=1
  echo "[Backend/Node] Unit tests"
  (cd backend && npm test) || FAILED=1
fi

if [ -f frontend/package.json ]; then
  FOUND=1
  echo "[Frontend] Unit tests"
  (cd frontend && npm test -- --run) || FAILED=1
fi

if [ -f android/gradlew ]; then
  FOUND=1
  echo "[Android] Unit tests"
  (cd android && ./gradlew test) || FAILED=1
fi

if [ "$FOUND" -eq 0 ]; then
  echo "No supported unit-test project detected."
  echo "Failing closed: unit tests cannot be proven PASS."
  exit 1
fi

if [ "$FAILED" -ne 0 ]; then
  echo
  echo "UNIT TEST GATE: FAILED"
  echo "DEPLOYMENT FORBIDDEN"
  exit 1
fi

echo
echo "UNIT TEST GATE: PASSED"
exit 0
```

Make scripts executable:

``` bash
chmod +x scripts/*.sh
```

**Important:** iOS CI normally requires macOS/Xcode infrastructure. Do
not pretend that a Linux EC2 Jenkins worker can execute native Xcode
unit/UI builds. Add a macOS Jenkins agent when iOS development becomes
active.

------------------------------------------------------------------------

# 19. Integration Test Script

Create `scripts/integration-test.sh`:

``` bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== INTEGRATION TEST ==="

if [ -f docker-compose.test.yml ]; then
  docker compose -f docker-compose.test.yml up \
    --build \
    --abort-on-container-exit \
    --exit-code-from integration-tests

  docker compose -f docker-compose.test.yml down -v
else
  echo "No docker-compose.test.yml yet."
  echo "Phase 1 requires this gate to be implemented before environment promotion is enabled."
  exit 1
fi

echo "INTEGRATION TEST PASSED"
```

For initial bootstrap, deployment should remain disabled until this gate
is backed by real tests.

------------------------------------------------------------------------

# 20. Security Scan Script

Create `scripts/security-scan.sh`:

``` bash
#!/usr/bin/env bash
set -euo pipefail

echo "=== SECURITY CHECK ==="

# Add project-specific SAST/dependency/container scanning here.
# Examples may include dependency audit tools and image scanners.
#
# Do not return PASS until at least the chosen mandatory checks
# have actually executed.

echo "Security scanning is not configured yet."
exit 1
```

Failing closed prevents a placeholder from accidentally becoming a fake
green gate.

------------------------------------------------------------------------

# 21. Quality Gate

Create `scripts/quality-gate.sh`:

``` bash
#!/usr/bin/env bash
set -euo pipefail

echo "================================"
echo " AI Tutor — Quality Gate"
echo "================================"

./scripts/build.sh
./scripts/lint.sh
./scripts/unit-test.sh
./scripts/integration-test.sh
./scripts/security-scan.sh

echo
echo "QUALITY GATE: PASSED"
```

The dependency chain is:

``` text
Any mandatory command exits non-zero
        |
        v
quality-gate.sh exits non-zero
        |
        v
Jenkins FAILED
        |
        v
Deployment stages are not executed
```

------------------------------------------------------------------------

# 22. Immutable Artifact Policy

A release should ideally be built once:

``` text
source commit
    |
    v
build
    |
    v
unit/integration/security gates
    |
    v
immutable artifact/container image
    |
    +--> DEV
    +--> STG
    +--> UAT
    `--> PROD
```

Do not rebuild different application binaries for each environment.

Environment-specific configuration should be injected separately.

A useful image convention is:

``` text
ai-tutor-backend:<git-sha>
ai-tutor-frontend:<git-sha>
```

Avoid relying only on mutable tags such as `latest`.

------------------------------------------------------------------------

# 23. Deployment Script Contract

Create `scripts/deploy.sh` initially as a safe stub:

``` bash
#!/usr/bin/env bash
set -euo pipefail

ENVIRONMENT="${1:-}"

case "$ENVIRONMENT" in
  dev|stg|uat|production)
    ;;
  *)
    echo "Usage: $0 {dev|stg|uat|production}"
    exit 1
    ;;
esac

echo "Requested deployment: $ENVIRONMENT"

echo "Deployment implementation is intentionally disabled in Phase 1."
echo "Configure environment-specific deployment and credentials before enabling."
exit 1
```

This prevents accidental deployment while the factory is being
constructed.

------------------------------------------------------------------------

# 24. Environment Promotion Policy

## DEV

Required:

``` text
Build PASS
Lint PASS
Unit Test PASS
Required security checks PASS
Artifact successfully built
```

## STG

Required:

``` text
All DEV gates PASS
Integration Test PASS
DEV smoke test PASS
Approved artifact selected
```

## UAT

Required:

``` text
All STG gates PASS
Regression PASS
Critical/High release blockers resolved according to release policy
Same immutable artifact promoted
```

## Production

Required:

``` text
All mandatory automated gates PASS
UAT acceptance recorded
Same approved immutable artifact
Human approval
Deployment/rollback plan available
```

At every environment:

> A failed Unit Test gate blocks deployment.

------------------------------------------------------------------------

# 25. Jenkinsfile

Create `Jenkinsfile`:

``` groovy
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        timestamps()
        skipDefaultCheckout(true)
    }

    environment {
        GIT_SHA = "${env.GIT_COMMIT}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
                script {
                    env.GIT_SHA = sh(
                        script: 'git rev-parse --short=12 HEAD',
                        returnStdout: true
                    ).trim()
                }
            }
        }

        stage('Build') {
            steps {
                sh './scripts/build.sh'
            }
        }

        stage('Lint') {
            steps {
                sh './scripts/lint.sh'
            }
        }

        stage('Unit Test Gate') {
            steps {
                sh './scripts/unit-test.sh'
            }
        }

        stage('Integration Test') {
            steps {
                sh './scripts/integration-test.sh'
            }
        }

        stage('Security Gate') {
            steps {
                sh './scripts/security-scan.sh'
            }
        }

        stage('Build Immutable Artifact') {
            steps {
                sh './scripts/build-artifact.sh'
            }
        }

        stage('Deploy DEV') {
            when {
                branch 'develop'
            }
            steps {
                sh './scripts/deploy.sh dev'
            }
        }

        stage('Deploy STG') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }
            steps {
                sh './scripts/deploy.sh stg'
            }
        }

        stage('Deploy UAT') {
            when {
                expression {
                    return env.BRANCH_NAME?.startsWith('release/')
                }
            }
            steps {
                sh './scripts/deploy.sh uat'
            }
        }

        stage('Production Approval') {
            when {
                branch 'main'
            }
            steps {
                input(
                    message: "Deploy approved artifact ${env.GIT_SHA} to Production?",
                    ok: 'Deploy'
                )
            }
        }

        stage('Deploy Production') {
            when {
                branch 'main'
            }
            steps {
                sh './scripts/deploy.sh production'
            }
        }
    }

    post {
        success {
            echo 'PIPELINE PASSED'
        }

        failure {
            echo 'PIPELINE FAILED — DEPLOYMENT BLOCKED'
        }

        always {
            archiveArtifacts(
                artifacts: 'factory/logs/**/*',
                allowEmptyArchive: true
            )
        }
    }
}
```

**Do not enable deployment merely because this file exists.**
`deploy.sh`, environment credentials, artifact promotion, integration
tests, security scanning and rollback must be implemented first.

------------------------------------------------------------------------

# 26. `build-artifact.sh`

Create:

``` bash
#!/usr/bin/env bash
set -euo pipefail

SHA="$(git rev-parse --short=12 HEAD)"

echo "Building immutable artifacts for commit: $SHA"

# Add real Docker/application packaging here.
# Example:
# docker build -t ai-tutor-backend:$SHA backend/
# docker build -t ai-tutor-frontend:$SHA frontend/

echo "Artifact build is not configured yet."
exit 1
```

Again, fail closed until real packaging exists.

------------------------------------------------------------------------

# 27. Jenkins Installation Baseline

Jenkins may run on the initial EC2 during Phase 1, but production
architecture should later separate the agent workspace, CI
controller/agents, and runtime environments.

At minimum, Jenkins needs:

-   Git access
-   Required language runtimes/build tools
-   Docker access if Docker is used
-   Credentials stored in Jenkins Credentials, not Git
-   Branch protection/status-check integration with the Git provider
-   Build retention policy
-   Artifact/image registry credentials
-   Environment-specific IAM roles

Do not store:

``` text
AWS_SECRET_ACCESS_KEY=...
DB_PASSWORD=...
PROD_SSH_KEY=...
```

inside repository files.

------------------------------------------------------------------------

# 28. Suggested Jenkins Topology

Phase 1:

``` text
EC2 AI Factory
|
|-- Claude Code
|-- Codex CLI
|-- Git working repository
|-- Jenkins
`-- Docker
```

Target evolution:

``` text
                    Management / Agent EC2
                    Claude + Codex
                           |
                           v
                         Git
                           |
                           v
                    Jenkins Controller
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
       Linux Agent     Android Agent   macOS Agent
       BE / FE / QA      Android         iOS
             |
             v
      Artifact Registry
             |
       +-----+-----+-----+
       |     |     |     |
      DEV   STG   UAT   PROD
                        ^
                        |
                  Human approval
```

iOS build/test requires a macOS/Xcode worker.

------------------------------------------------------------------------

# 29. Agent Execution Workflow

For a Story such as `US-101`:

## Step 1 --- PM/PO

Claude PM/PO defines business priority and Feature context.

## Step 2 --- BA

Claude BA creates:

``` text
safe/stories/US-101.yaml
```

and fills AC, requirements, dependencies and test scenarios.

## Step 3 --- Scrum Master

Claude SM validates DoR.

If DoR fails:

``` text
US-101 -> REFINED
```

If DoR passes:

``` text
US-101 -> READY
```

## Step 4 --- Create worktrees

``` bash
git worktree add \
  /home/ubuntu/AI_Tutor-worktrees/US-101-BE \
  -b feature/US-101-backend \
  develop
```

Repeat only for components actually required by the Story.

## Step 5 --- Start Codex

``` bash
cd /home/ubuntu/AI_Tutor-worktrees/US-101-BE
codex
```

Initial instruction:

``` text
Act as the Backend Developer Agent.

Read:
- AGENTS.md
- agents/codex/backend.md
- safe/stories/US-101.yaml
- relevant context and architecture documentation

Do not modify code yet.

First:
1. Validate that the Story is implementable.
2. Map Acceptance Criteria to implementation tasks.
3. Identify risks and dependencies.
4. Propose the implementation plan.

If a material requirement is unclear, stop and report the question.

After approval, implement only within your role boundary.
Before completion, run all mandatory tests and provide evidence.
```

## Step 6 --- Local engineering gate

Before push:

``` bash
./scripts/build.sh
./scripts/lint.sh
./scripts/unit-test.sh
```

No green unit test -\> no PR readiness.

## Step 7 --- PR

The agent reviews:

``` bash
git status
git diff
```

Then commit/push according to team policy.

## Step 8 --- Jenkins

Jenkins independently repeats the mandatory gates.

Local agent output is evidence, not authority.

## Step 9 --- Tester

Tester validates the implementation against Story/AC.

## Step 10 --- QA

QA verifies traceability and DoD evidence.

## Step 11 --- Merge and promotion

Only validated changes are integrated and promoted.

------------------------------------------------------------------------

# 30. Recommended Claude PM/PO Invocation

From repository root:

``` bash
cd /home/ubuntu/AI_Tutor
claude
```

Prompt:

``` text
Act only as the PM/PO Agent for AI Tutor.

Read:
- CLAUDE.md
- context/product.md
- context/business-rules.md
- agents/claude/pm-po.md
- existing SAFe artifacts

Do not implement production code.

Your task:
1. Review current Product Vision.
2. Maintain the prioritized backlog.
3. Define/refine Epics and Features.
4. Define measurable PI Objectives.
5. Identify business dependencies and open product decisions.
6. Produce repository artifacts rather than relying on chat history.

Do not bypass BA, DoR, QA or Jenkins.
```

------------------------------------------------------------------------

# 31. Recommended Claude BA Invocation

``` text
Act only as the Business Analyst Agent.

Read:
- CLAUDE.md
- agents/claude/ba.md
- relevant Epic
- relevant Feature
- context documentation

Create/refine implementation-ready User Stories.

Every Story must include:
- business value
- description
- Acceptance Criteria
- functional requirements
- relevant NFRs
- dependencies
- component impact
- API/data/security/privacy impact
- test scenarios
- open questions
- DoR status

Do not invent unresolved requirements.

If a material ambiguity exists, keep the Story non-READY.
```

------------------------------------------------------------------------

# 32. Recommended Claude Scrum Master Invocation

``` text
Act only as the Scrum Master Agent.

Read:
- CLAUDE.md
- agents/claude/scrum-master.md
- current PI Objectives
- Sprint backlog
- User Stories

Validate:
- Definition of Ready
- dependencies
- blockers
- risks
- Story state transitions
- Definition of Done evidence

Do not mark a Story READY if DoR fails.
Do not mark a Story DONE if DoD fails.
Do not override Jenkins.
```

------------------------------------------------------------------------

# 33. Tester Invocation

``` text
Act as the Tester Agent.

Read:
- AGENTS.md
- agents/codex/tester.md
- the target User Story
- Acceptance Criteria
- implementation diff

Do not assume the implementation is correct.

Create/execute tests covering:
- positive paths
- negative paths
- boundaries
- error handling
- integration behavior
- regression risk

Produce traceable evidence from AC -> test -> result.

A failure remains a failure.
```

------------------------------------------------------------------------

# 34. QA Invocation

``` text
Act as the QA Agent.

Read:
- AGENTS.md
- agents/codex/qa.md
- Story
- Acceptance Criteria
- code review evidence
- test evidence
- Jenkins results

Verify Definition of Done.

Do not change failed evidence to PASS.

If mandatory evidence is missing, QA status is NOT PASS.
```

------------------------------------------------------------------------

# 35. DevOps Invocation

``` text
Act as the DevOps Agent.

Read:
- AGENTS.md
- agents/codex/devops.md
- infrastructure/
- Jenkinsfile
- scripts/

Your job is to improve CI/CD safely.

Mandatory constraints:
- no secrets in Git
- no Production credentials exposed to normal agents
- no deployment after failed unit tests
- use immutable artifacts for promotion
- Production requires human approval
- deployment must have rollback capability

Before modifying pipeline behavior, explain the expected gate sequence.
```

------------------------------------------------------------------------

# 36. SAFe Mapping

Use the hierarchy:

``` text
Product Vision
      |
      v
Portfolio / Product Backlog
      |
      v
Epic
      |
      v
Feature
      |
      v
PI Objective
      |
      v
User Story
      |
      v
Engineering Tasks
```

Role mapping:

``` text
Epic / Feature / Priority
        |
   Claude PM/PO
        |
        v
Story / AC / Test Scenario
        |
     Claude BA
        |
        v
DoR / Sprint / Dependencies
        |
    Claude Scrum Master
        |
        v
Engineering execution
        |
       Codex
        |
        v
Tester -> QA -> Jenkins
```

This is SAFe-inspired. Do not add process ceremony merely for
appearance; artifacts and gates should support actual delivery.

------------------------------------------------------------------------

# 37. PI Planning Foundation

Create PI Objective files such as:

``` text
safe/pi-objectives/PI-001.yaml
```

Example:

``` yaml
id: PI-001
name: AI Tutor MVP Foundation

business_objectives:
  - Establish secure student learning session foundation
  - Establish parent-facing session visibility
  - Establish real-time learning architecture baseline

committed_objectives:
  - id: OBJ-01
    description: Establish authenticated student session lifecycle
    business_value: 8

  - id: OBJ-02
    description: Establish CI/CD and quality gates
    business_value: 10

dependencies: []

risks: []
```

Business value scoring should be decided by the Product Owner/human, not
fabricated by an agent.

------------------------------------------------------------------------

# 38. Sprint Artifact

Example:

``` text
safe/sprints/SPRINT-001.yaml
```

``` yaml
id: SPRINT-001
pi: PI-001

goal: ""

start_date: ""
end_date: ""

stories: []

risks: []
blockers: []

metrics:
  committed_points: 0
  completed_points: 0
```

------------------------------------------------------------------------

# 39. Security and Privacy Rules for AI Tutor

Because the product may process student learning sessions and
camera/audio data, security/privacy requirements must be treated as
first-class engineering requirements.

At minimum:

-   Least-privilege access
-   Explicit permission/consent flows
-   Encryption in transit
-   Encryption at rest where applicable
-   Strong authentication/authorization
-   Auditability for sensitive actions
-   No credentials in source control
-   Environment separation
-   Data retention rules documented
-   Camera/audio behavior explicitly specified
-   Production data not copied casually into DEV/STG
-   Logs must avoid sensitive content
-   Parent/student permissions must be implemented from approved
    requirements
-   Threat modeling before production release of sensitive capabilities

Legal/privacy requirements should be validated for the actual launch
jurisdictions rather than guessed by AI agents.

------------------------------------------------------------------------

# 40. Observability Foundation

Plan for:

``` text
Application logs
Metrics
Tracing
Deployment events
Jenkins build history
Test reports
Agent execution logs
Audit events
```

Agent logs belong under:

``` text
factory/logs/
```

but secrets, raw credentials, private tokens, or unnecessary sensitive
user data must never be recorded there.

------------------------------------------------------------------------

# 41. Factory State

Suggested machine-readable state:

``` text
factory/state/
```

Example:

``` json
{
  "story": "US-101",
  "status": "IN_PROGRESS",
  "agents": {
    "backend": "feature/US-101-backend",
    "frontend": "feature/US-101-frontend"
  },
  "quality": {
    "unit_test": "UNKNOWN",
    "integration_test": "UNKNOWN",
    "qa": "UNKNOWN"
  }
}
```

Never interpret `UNKNOWN` as `PASS`.

------------------------------------------------------------------------

# 42. Phase-1 Orchestrator Boundary

Phase 1 should remain supervised:

``` text
Claude
  |
  v
Artifact
  |
  v
Human review where appropriate
  |
  v
Codex
  |
  v
PR
  |
  v
Jenkins
```

Do not initially create an autonomous loop that can continuously modify,
merge and deploy software without supervision.

Phase 2 may introduce automated agent assignment and PR generation.

Phase 3 may introduce broader orchestration after quality, security and
rollback behavior are proven.

------------------------------------------------------------------------

# 43. Future Orchestrator Flow

Future `factory/orchestrator/` logic may implement:

``` text
Read backlog
    |
Find READY Story
    |
Validate DoR
    |
Determine affected components
    |
Create isolated worktrees
    |
Assign Codex roles
    |
Run implementation
    |
Run local gates
    |
Create PR
    |
Jenkins
    |
Tester
    |
QA
    |
Update Story state
```

The orchestrator must not contain a path that converts failed mandatory
gates into deploy permission.

------------------------------------------------------------------------

# 44. Makefile

Create `Makefile`:

``` make
.PHONY: build lint unit integration security quality tree

build:
    ./scripts/build.sh

lint:
    ./scripts/lint.sh

unit:
    ./scripts/unit-test.sh

integration:
    ./scripts/integration-test.sh

security:
    ./scripts/security-scan.sh

quality:
    ./scripts/quality-gate.sh

tree:
    tree -L 3
```

Then:

``` bash
make unit
make quality
```

------------------------------------------------------------------------

# 45. `.gitignore`

Suggested baseline:

``` gitignore
# Secrets
.env
.env.*
*.pem
*.key

# Agent/runtime logs
factory/logs/*
!factory/logs/.gitkeep

# Node
node_modules/
dist/
coverage/

# Python
__pycache__/
*.pyc
.venv/
venv/

# Java
target/
.gradle/
build/

# Android
local.properties

# iOS/macOS
DerivedData/
*.xcuserdata/

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db

# Terraform
.terraform/
*.tfstate
*.tfstate.*
```

Never commit your EC2 `.pem` key.

------------------------------------------------------------------------

# 46. Bootstrap Permissions

After creating scripts:

``` bash
chmod +x scripts/*.sh
```

Verify:

``` bash
ls -l scripts/
```

Run shell syntax checks:

``` bash
for f in scripts/*.sh; do
  bash -n "$f" || exit 1
done
```

------------------------------------------------------------------------

# 47. Initial Git Commit

Review first:

``` bash
git status
git diff
```

Then:

``` bash
git add \
  CLAUDE.md \
  AGENTS.md \
  agents \
  safe \
  factory \
  scripts \
  infrastructure \
  tests \
  Jenkinsfile \
  Makefile \
  .gitignore
```

Commit:

``` bash
git commit -m "chore: establish AI Agent Factory foundation"
```

Do not commit secrets.

------------------------------------------------------------------------

# 48. Branch Protection Requirements

On the Git hosting service, protect at least:

``` text
main
develop
```

Recommended rules:

-   No direct push
-   PR required
-   Required Jenkins status checks
-   Required review
-   Prevent force push
-   Prevent branch deletion
-   Resolve conversations before merge
-   Production/release changes require stronger approval

This enforcement should live in the Git hosting platform, not only in
prompt instructions.

------------------------------------------------------------------------

# 49. Jenkins Quality Policy

The desired gate matrix is:

  ----------------------------------------------------------------------------------------
  Gate                      Feature PR          DEV          STG          UAT         PROD
  ------------- ---------------------- ------------ ------------ ------------ ------------
  Build                       Required     Required     Required     Required     Required

  Lint                        Required     Required     Required     Required     Required

  Unit Test                   Required     Required     Required     Required     Required

  Integration     Recommended/Required     Required     Required     Required     Required
                              by scope                                        

  Security           Required baseline     Required     Required     Required     Required

  Smoke                             \-     Required     Required     Required     Required
                                       after deploy                           

  Regression                   By risk      By risk     Required     Required     Required

  UAT approval                      \-           \-           \-     Required     Required

  Human                             \-           \-           \-           \-     Required
  Production                                                                  
  approval                                                                    
  ----------------------------------------------------------------------------------------

The central invariant is:

``` text
Unit Test != PASS
        |
        v
DEPLOY = FORBIDDEN
```

------------------------------------------------------------------------

# 50. Failure Handling

## Requirement failure

``` text
Ambiguous requirement
-> BA
-> clarify
-> update Story
-> rerun DoR
```

## Build failure

``` text
Build FAIL
-> Development
-> fix
-> rerun pipeline
```

## Unit test failure

``` text
Unit Test FAIL
-> immediate pipeline stop
-> no artifact promotion
-> Development
```

## Tester failure

``` text
Functional defect
-> defect evidence
-> Development
-> retest
```

## QA failure

``` text
DoD/evidence failure
-> relevant owner
-> remediation
-> QA again
```

## Production failure

The deployment architecture must eventually provide:

-   health checks
-   monitoring
-   rollback
-   previous known-good artifact
-   incident logging

Production rollback must not depend on an AI agent improvising under
pressure.

------------------------------------------------------------------------

# 51. Phase 1 Definition of Done

Phase 1 is complete only when all applicable items are verified:

``` text
[ ] Repository structure exists
[ ] CLAUDE.md exists
[ ] AGENTS.md exists

Claude:
[ ] PM/PO role
[ ] BA role
[ ] Scrum Master role

Codex:
[ ] Backend role
[ ] Frontend role
[ ] Android role
[ ] iOS role
[ ] Tester role
[ ] QA role
[ ] DevOps role

SAFe:
[ ] Epic template
[ ] Feature template
[ ] Story template
[ ] PI Objective structure
[ ] Sprint structure
[ ] DoR
[ ] DoD
[ ] Story state machine

Git:
[ ] main/develop strategy agreed
[ ] branch protection configured
[ ] worktree strategy verified
[ ] agents cannot casually share one mutable worktree

CI:
[ ] Jenkins connected to Git
[ ] build gate operational
[ ] lint gate operational
[ ] unit-test gate operational
[ ] failing unit test demonstrably blocks pipeline
[ ] integration gate operational
[ ] security gate operational
[ ] immutable artifact build operational

CD:
[ ] DEV deployment implemented
[ ] STG promotion implemented
[ ] UAT promotion implemented
[ ] Production promotion implemented
[ ] Production human approval operational
[ ] rollback mechanism verified

Security:
[ ] no secrets in Git
[ ] Jenkins credentials configured
[ ] IAM least privilege applied
[ ] Production credentials unavailable to normal agents

Verification:
[ ] deliberate unit-test failure blocks DEV
[ ] deliberate unit-test failure blocks STG
[ ] deliberate unit-test failure blocks UAT
[ ] deliberate unit-test failure blocks PROD
[ ] Production cannot deploy without human approval
```

------------------------------------------------------------------------

# 52. Recommended Phase 1 Verification Scenario

Do not declare the factory ready merely because Jenkins displays green
once.

Perform a controlled negative test.

## Test A --- Unit Test PASS

``` text
Commit valid implementation
-> Jenkins
-> Unit Test PASS
-> downstream gates execute
```

## Test B --- Deliberately broken unit test

Create a temporary branch containing one intentionally failing unit
test.

Expected:

``` text
Build
  |
Unit Test FAIL
  |
Pipeline FAILED
  |
No Deploy DEV
  |
No Deploy STG
  |
No Deploy UAT
  |
No Deploy PROD
```

Then revert/delete the temporary failure branch.

## Test C --- Production approval

Use a safe non-production/dry-run deployment target first.

Expected:

``` text
All gates PASS
-> Production Approval stage
-> pipeline waits
-> no approval
-> no Production deploy
```

Only after these controls are demonstrated should Phase 1 be considered
operational.

------------------------------------------------------------------------

# 53. Suggested Implementation Order on EC2

Execute Phase 1 in this order:

``` text
1. Repository/folder foundation
2. CLAUDE.md
3. AGENTS.md
4. Claude role files
5. Codex role files
6. SAFe templates
7. DoR/DoD
8. Git branch/worktree model
9. Build script
10. Lint script
11. Unit-test gate
12. Integration-test environment
13. Security checks
14. Artifact packaging
15. Jenkins installation/configuration
16. Jenkins pipeline
17. DEV deployment
18. STG promotion
19. UAT promotion
20. Production approval/deployment
21. Negative quality-gate tests
22. Phase-1 acceptance
```

Do **not** jump directly from step 8 to automatic Production deployment.

------------------------------------------------------------------------

# 54. Phase 2 Preview

Once Phase 1 is stable:

``` text
READY Story
    |
    v
Factory Orchestrator
    |
    +--> BE worktree -> Codex BE
    |
    +--> FE worktree -> Codex FE
    |
    +--> Android -> Codex Android
    |
    `--> iOS -> Codex iOS
            |
            v
        automated PR
            |
            v
          Jenkins
            |
            v
       Tester / QA
```

Phase 2 should add:

-   Structured YAML/JSON Schema validation
-   Automated Story dispatcher
-   Automated worktree lifecycle
-   Agent execution logs
-   PR automation
-   Jenkins result ingestion
-   Traceability matrix
-   Automatic Story status updates
-   Notifications
-   Metrics

------------------------------------------------------------------------

# 55. Phase 3 Preview

Only after sufficient control and reliability:

``` text
Product backlog
      |
      v
Claude management agents
      |
      v
Orchestrator
      |
      v
Parallel Codex engineering agents
      |
      v
Independent testing / QA
      |
      v
Jenkins
      |
      v
Controlled environment promotion
```

Human authority should remain around high-impact Product decisions and
Production release.

------------------------------------------------------------------------

# 56. Final Factory Model

``` text
                         HUMAN PRODUCT OWNER
                                |
                                v
                         Claude PM/PO
                                |
                          Epic / Feature
                                |
                                v
                           Claude BA
                                |
                    Story / AC / Test Scenarios
                                |
                                v
                         Claude Scrum Master
                                |
                          DoR / Sprint / PI
                                |
                +---------------+---------------+
                |               |               |
                v               v               v
           Codex BE         Codex FE        Codex Mobile
                |               |               |
                +---------------+---------------+
                                |
                                v
                        Local Unit Tests
                                |
                         +------+------+
                         |             |
                       FAIL           PASS
                         |             |
                         v             v
                        STOP          PR
                                       |
                                       v
                                    Jenkins
                                       |
                              Build / Lint / Unit
                              Integration / Security
                                       |
                                +------+------+
                                |             |
                              FAIL           PASS
                                |             |
                                v             v
                               STOP     Immutable Artifact
                                              |
                                              v
                                             DEV
                                              |
                                             STG
                                              |
                                             UAT
                                              |
                                      Human Approval
                                              |
                                              v
                                             PROD
```

------------------------------------------------------------------------

# 57. Non-Negotiable Factory Rules

1.  **NO UNIT TEST PASS = NO DEPLOY.**
2.  `UNKNOWN` is never equivalent to `PASS`.
3.  Claude manages requirements/process; Codex performs engineering
    execution.
4.  No engineering agent invents material missing requirements.
5.  No direct implementation on protected branches.
6.  Parallel agents use isolated branches/worktrees.
7.  Jenkins independently verifies quality; agent claims are not
    sufficient.
8.  Build once and promote the same immutable artifact.
9.  Secrets never belong in Git or prompts.
10. Production credentials are isolated from normal agents.
11. Production requires explicit human approval.
12. Quality gates fail closed.
13. A Story cannot start without DoR.
14. A Story cannot become DONE without DoD.
15. Production must have rollback and observability before real users
    depend on it.

------------------------------------------------------------------------

# 58. Immediate Next Step

After copying this document into the EC2 repository, start Claude from
the repository root:

``` bash
cd /home/ubuntu/AI_Tutor
claude
```

Give Claude:

``` text
Act as the AI Tutor Factory Foundation PM/BA/SM setup assistant.

Read this Phase 1 document completely.

Read the existing repository before making changes.

Your objective is to establish Phase 1 exactly as specified.

First:
1. Inspect the current repository.
2. Compare it against the Phase 1 target structure.
3. Produce a gap analysis.
4. Produce an implementation plan.
5. Do not delete existing product code.
6. Do not overwrite existing files without reviewing them.
7. Do not deploy anything.

After I approve the plan, create the management artifacts, SAFe templates,
agent role files and factory foundation.

Engineering scripts and Jenkins changes must remain fail-closed:
NO UNIT TEST PASS = NO DEPLOY.
```

Then use Codex for the engineering/DevOps portions only after Claude has
created and reviewed the required management artifacts.

------------------------------------------------------------------------

## End of Phase 1 Specification

**Target outcome:** a controlled, auditable AI Agent Software Factory
foundation capable of supporting AI Tutor development under a
SAFe-inspired process with Claude management agents, Codex engineering
agents, Git isolation, Jenkins CI/CD, mandatory testing, controlled
environment promotion and human-approved Production release.
