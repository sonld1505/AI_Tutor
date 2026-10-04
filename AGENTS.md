# AGENTS.md

Hướng dẫn cho mọi coding agent (Codex, Claude Code, …) làm việc trên repository này.

**Nguồn luật sản phẩm:** `CLAUDE_AI_Tutor.md` — đọc toàn bộ trước khi thay đổi bất cứ thứ gì; `CLAUDE.md` chứa thứ tự đọc và bản tóm tắt luật. **Luật quy trình kỹ thuật:** mục Engineering Agent Constitution bên dưới. Lệch về sản phẩm → `CLAUDE_AI_Tutor.md` thắng; mâu thuẫn khác → hard-stop, hỏi chủ dự án.

---

# AI Tutor — Engineering Agent Constitution (Lean Mode, 2026-10-04)

> Luật sản phẩm vẫn nằm ở `CLAUDE_AI_Tutor.md` và thắng nếu lệch về sản phẩm. Mục này bổ sung luật **quy trình kỹ thuật**. Nếu hai nguồn mâu thuẫn → hard-stop, hỏi chủ dự án.
> Role files: `agents/codex/`. Story: `safe/stories/`. Gates: `scripts/`, `Jenkinsfile`. Tạo worktree: `./scripts/create-worktree.sh <story-id> <role>`.

### Engineering Roles

Codex may operate as:

- Backend Developer
- Frontend Developer
- Android Developer
- iOS Developer
- AI/ML Engineer
- DevOps/Cloud Engineer (infrastructure, CI/CD, runtime, Factory tooling; **not** the generic application developer)
- Tester / QA (used for Validation when a Story needs functional or system testing)

Every invocation must have one clearly identified role. Specialists are activated only when the Story needs them.

### Mandatory Reading Before Work

Before implementing a Story, the agent must read:

1. AGENTS.md
2. Its role file under agents/codex/
3. Relevant User Story
4. Acceptance Criteria
5. Relevant architecture/context documentation

### Git Policy

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

### Requirement Policy

Never silently invent missing requirements.

When a material requirement is unclear:

STOP.

Document the question and return it to Claude: product questions go to the PO, technical questions to the SA (`agents/claude/solution-architect.md`), who decides.

### Mandatory Engineering Validation

Before declaring work complete:

1. Build
2. Lint/static checks
3. Unit tests
4. Relevant security checks
5. Review git diff
6. Check Acceptance Criteria
7. Report evidence

### Deployment Policy

NO UNIT TEST PASS = NO DEPLOY.

Agents may not bypass Jenkins.

Agents may not directly deploy Production.

Production secrets must not be available to normal engineering agents.

### Lean Rules (2026-10-04)

- Work inside the boundaries the SA set (owned paths of your role file, interfaces, ADRs). Changing another domain's code or a shared interface needs an SA decision first.
- Run the smallest useful targeted tests during development. The full suite runs in CI once per merge candidate. Every long command has a `timeout` and a log.
- Review cap: one review, one fix, one re-review. Remaining Critical/Major go to the SA, never into an open-ended loop.
- You never validate, review or approve your own work. You never merge into `develop`/`main`.
- Mocks are labelled MOCK in code, test names, logs and reports.
