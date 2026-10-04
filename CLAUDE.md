# CLAUDE.md

> File này tự động nạp cho Claude Code. Luật chi tiết nằm ở `CLAUDE_AI_Tutor.md` — **đọc toàn bộ file đó trước khi làm bất cứ việc gì**.

## Thứ tự đọc bắt buộc

1. `CLAUDE_AI_Tutor.md` — bối cảnh sản phẩm AI Study Companion + luật camera/privacy/provider/tutor + nguyên tắc coding agent.
2. `README.md` — bản đồ repository và trạng thái thực tế.
3. `dev-book/PM-AI-Bootcamp-Capstone-Playbook-v1.0.md` — quy trình 11 bước (scope → spec → … → build → test → RTM).
4. Workbook theo vai trò khi cần: `dev-book/PM-AI-Bootcamp-Workbook-{Common,BA,SA,Dev}-v1.0.md`.
5. `docs/GLOSSARY.md` — thuật ngữ (L0–L5, Leash A/A+, fail-closed, …).
6. Factory (Lean mode từ 2026-10-04): mục **Factory Constitution — Lean Mode** bên dưới + `agents/claude/solution-architect.md` + `safe/templates/`. Lịch sử Phase 1: `docs/factory/AI_Tutor_Phase1_Agent_Factory_Foundation.md`.

## Luật không được vi phạm (tóm tắt — bản đầy đủ ở `CLAUDE_AI_Tutor.md`)

- Repository hiện **chỉ có tài liệu**. Không mô tả code, EC2, camera, provider, benchmark hay doanh thu là đã có.
- Mock phải được gắn nhãn rõ trong code, log và tài liệu; không dùng mock để tuyên bố năng lực thật.
- Không dùng provider AI cho trẻ em khi điều khoản chưa được xác minh.
- Không đưa secret vào Git, tài liệu, log hoặc client.
- Camera: chỉ bật trong phiên, hướng xuống bàn, không lưu video mặc định, ảnh tạm có TTL.
- Không bịa số liệu; thiếu nguồn → ghi `N/A`.
- Việc thuộc quyền PO (secret/credential, dữ liệu trẻ em/privacy/pháp lý, provider cho trẻ em, tài khoản/quyền quản trị bên ngoài, chi phí/budget, production, merge cuối) → **dừng, dùng HUMAN ACTION REQUIRED**. Quyết định kỹ thuật (kể cả schema không chứa dữ liệu cá nhân trẻ em/gia đình) thuộc SA, không hỏi PO.
- Mâu thuẫn hoặc thiếu thông tin **sản phẩm** → hỏi PO; mâu thuẫn/thiếu thông tin **kỹ thuật** → SA quyết.
- Sau mỗi thay đổi: chạy test phù hợp, ghi kết quả; `CHANGELOG.md` một dòng mỗi mốc; DEVBOOK chỉ ghi quyết định, mốc, blocker, cách làm AI thất bại đáng học, can thiệp của người, kết quả merge/release.

---

# AI Tutor — Factory Constitution — Lean Mode (PO decision 2026-10-04)

> Factory tồn tại để xây AI Tutor, không ngược lại. Chọn cơ chế đơn giản nhất mà an toàn. Luật sản phẩm (camera/privacy/provider/tutor) vẫn ở `CLAUDE_AI_Tutor.md` và thắng nếu lệch.

### Authority

| Role | Owns |
|---|---|
| **Human PO** | Product scope and priority, business acceptance, budget/legal/privacy, external accounts/admin, credentials/secrets, production release, final merge approval |
| **Claude Orchestrator** | Triage, sequencing, dispatch, recovery, status tracking, escalation. Also does the lightweight PM/BA/SM work directly (no separate agents) |
| **Solution Architect (SA)** | All normal technical decisions (`agents/claude/solution-architect.md`). Never asks the PO technical questions |
| **Engineering agents** | Implementation inside SA boundaries. Specialists (Backend, Frontend, Android, iOS, AI/ML, DevOps/Cloud) are activated only when a Story needs them |
| **Validation** | Independent review/verification. Never validates its own work |

### Lean Delivery Flow

```
PO requirement → Claude triage → SA (only when useful) → Engineering → targeted tests
→ Independent Review → CI (full suite once per merge candidate) → PO PR approval → merge (merge commit)
```

- **SA when useful:** invoke SA when it lowers expected delivery cost or technical risk (architecture, hard defects, repeated review failures, security design, performance, boundaries, dependencies, infra/CI, data model, API contracts, AI/ML integration). Skip SA for simple Stories.
- **Review cap:** implementation → review → fix → **one** re-review. If Critical/Major remain → SA root-cause analysis. SA picks one of: targeted fix plus targeted verification; redesign/refactor; return to the engineer; accept a Minor/Info debt item with rationale; or BLOCK only if it can't be solved safely within technical authority. No Round-N loops.
- **Tests:** smallest useful targeted set during development. "< 5 min" is a target, not a gate. The full suite runs normally once per merge candidate, in CI. Reuse valid results when inputs are unchanged. No mutation testing by default. Every long-running command has a timeout, observable status and a log when useful.
- **Story states (operational view):** TODO = DRAFT/REFINED/READY · DEV = IN_PROGRESS/DEV_COMPLETE · VERIFY = TESTING/QA · BLOCKED (with a reason) · DONE (merged). The detailed state machine in `agents/claude/scrum-master.md` stays enforced by the validator until it is simplified after US-FACTORY-003 merges.
- **Records (Git):** Story YAML (AC, status, commit, review result, CI link), review reports, ADRs only for material decisions (architecture, public interfaces, security, deployment, data model, cross-team, costly-to-reverse technology), RAID for risks/assumptions/issues/dependencies (no separate gap register). Chat is not a source of truth.

### Human Fast-Path

When a step needs GitHub/AWS/Jenkins admin, accounts, credentials/SSH/PAT/2FA, billing or external service configuration, don't build automation around it. Ask the PO for **one** action at a time:

```
HUMAN ACTION REQUIRED
Reason: / Where: / Action: / Expected result: / How Claude will verify:
```

After the PO answers DONE, verify and continue automatically. Don't wait on the PO for work that can proceed independently.

### Fail-Closed Scope

Fail-closed is mandatory for security, credentials, destructive actions, production deployment, final merge authorisation, and corrupted or unverifiable **required** evidence. Normal development fails fast. Historical evidence never blocks normal flow permanently.

### Critical Quality Policy

NO UNIT TEST PASS = NO DEPLOY. No agent overrides CI. Production and merge into `develop`/`main` always require explicit human approval.

### Factory Freeze

Once the Minimum Viable Factory works (US-FACTORY-003 merged; 004–007 in their MVF form; CI and the PO merge gate working), Factory feature work stops. Further Factory changes happen only when a product Story needs them.
