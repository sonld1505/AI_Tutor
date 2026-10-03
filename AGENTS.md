# AGENTS.md

Hướng dẫn cho mọi coding agent (Codex, Claude Code, …) làm việc trên repository này.

**Nguồn luật sản phẩm:** `CLAUDE_AI_Tutor.md` — đọc toàn bộ trước khi thay đổi bất cứ thứ gì; `CLAUDE.md` chứa thứ tự đọc và bản tóm tắt luật. **Luật quy trình kỹ thuật:** mục Engineering Agent Constitution bên dưới. Lệch về sản phẩm → `CLAUDE_AI_Tutor.md` thắng; mâu thuẫn khác → hard-stop, hỏi chủ dự án.

---

# AI Tutor — Engineering Agent Constitution (Factory Phase 1)

> Luật sản phẩm vẫn nằm ở `CLAUDE_AI_Tutor.md` và thắng nếu lệch về sản phẩm. Mục này bổ sung luật **quy trình kỹ thuật**. Nếu hai nguồn mâu thuẫn → hard-stop, hỏi chủ dự án.
> Role files: `agents/codex/`. Story: `safe/stories/`. Gates: `scripts/`, `Jenkinsfile`. Tạo worktree: `./scripts/create-worktree.sh <story-id> <role>`.

### Engineering Roles

Codex may operate as:

- Backend Developer
- Frontend Developer
- Android Developer
- iOS Developer
- Tester
- QA
- DevOps

Every invocation must have one clearly identified role.

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

Document the question and return it to BA/PM.

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
