# Glossary

Thuật ngữ dự án: `docs/GLOSSARY.md` (bản tạm).

Thuật ngữ factory (Phase 1):

| Thuật ngữ | Nghĩa |
|---|---|
| DoR / DoD | Definition of Ready / Done — `safe/templates/definition-of-ready.yaml`, `definition-of-done.yaml`. Mọi mục bắt buộc phải `true`. |
| Story states | `DRAFT → REFINED → READY → IN_PROGRESS → DEV_COMPLETE → TESTING → QA → DONE` (xem `agents/claude/scrum-master.md`). |
| `UNKNOWN` | Trạng thái chưa kiểm chứng của một gate. `UNKNOWN != PASS`. |
| Fail closed | Gate không xác minh được → chặn. |
| Worktree | Git worktree riêng cho mỗi Story/role: `feature/<story-id>-<role>` tại `/home/ubuntu/AI_Tutor-worktrees/`. |
| Immutable artifact | Build một lần theo git SHA, promote cùng artifact qua DEV → STG → UAT → PROD. |
