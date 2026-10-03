# Factory Phase 1 — Trạng thái nghiệm thu

> Owner: Claude Scrum Master. Đối chiếu từng mục §51 của `AI_Tutor_Phase1_Agent_Factory_Foundation.md`.
> Cập nhật: 2026-10-03, nhánh `chore/phase1-agent-factory-foundation`.
> Quy ước: **PASS** = có bằng chứng · **PARTIAL** = có một phần, ghi rõ phần thiếu · **OPEN** = chưa làm hoặc chưa kiểm chứng · `UNKNOWN != PASS`.
> **Phase 1 chưa hoàn thành.** Mọi mục trong nhóm CI, CD và Verification đều OPEN.

## Repository & constitution

| Mục §51 | Trạng thái | Bằng chứng / phần thiếu |
|---|---|---|
| Repository structure exists | PARTIAL | Đủ cây thư mục §3 (commit `619c632`). Chỉ có trên nhánh chore, **chưa merge** vào `main`/`develop`. |
| CLAUDE.md exists | PARTIAL | Có Constitution; cùng điều kiện merge như trên. |
| AGENTS.md exists | PARTIAL | Như trên. |

## Vai trò

| Mục | Trạng thái | Bằng chứng |
|---|---|---|
| Claude PM/PO, BA, Scrum Master | PASS | `agents/claude/{pm-po,ba,scrum-master}.md` |
| Codex Backend, Frontend, Android, iOS, Tester, QA, DevOps | PASS | `agents/codex/*.md` (7 file) |

## SAFe

| Mục | Trạng thái | Bằng chứng |
|---|---|---|
| Epic / Feature / Story template | PASS | `safe/templates/`. Story template đã bổ sung `business_context`, `ui_impact`, `data_impact`, khối DoD, khoá DoR khớp `definition-of-ready.yaml` (2026-10-03). |
| PI Objective structure | PASS | `safe/templates/pi-objective.yaml` (`business_value: null` — người quyết). |
| Sprint structure | PASS | `safe/templates/sprint.yaml` |
| DoR | PARTIAL | Template PASS. **Validator fail-open → DEF-001.** Tạm thời SM kiểm tay (R-001 trong `safe/raid.yaml`). |
| DoD | PASS | `safe/templates/definition-of-done.yaml` + khối `definition_of_done` trong Story. Chưa có validator DoD (Phase 2: schema validation). |
| Story state machine | PASS | `agents/claude/scrum-master.md`, có thêm `BLOCKED` + `blocked_from`. |

## Git

| Mục | Trạng thái | Bằng chứng / phần thiếu |
|---|---|---|
| main/develop strategy agreed | OPEN | Chiến lược ghi trong `AGENTS.md` + spec §13. Cần chủ dự án xác nhận. |
| Branch protection configured | OPEN | Chưa kiểm chứng: `gh` chưa đăng nhập trên EC2. |
| Worktree strategy verified | OPEN | `create-worktree.sh` chưa chạy end-to-end lần nào; bị chặn bởi DEF-001, DEF-002. |
| Agents cannot share one mutable worktree | PARTIAL | Script tạo một worktree cho mỗi Story/role; chưa có cơ chế kỹ thuật ngăn hai agent cùng mở một worktree. |

## CI

| Mục | Trạng thái | Bằng chứng / phần thiếu |
|---|---|---|
| Jenkins connected to Git | OPEN | Jenkins LTS chạy, `127.0.0.1:8080/login` HTTP 200. Chưa xác nhận có job multibranch + credential GitHub. |
| Build / lint / unit-test gate operational | PARTIAL | Script tồn tại, `bash -n` PASS, exit≠0 khi chưa có project (đúng fail-closed). Chưa chạy trong Jenkins; chưa có project để chứng minh nhánh PASS. |
| Failing unit test demonstrably blocks pipeline | OPEN | Cần test §52-B. |
| Integration / security gate operational | OPEN | Cố ý `exit 1` — chưa hiện thực. |
| Immutable artifact build operational | OPEN | Cố ý `exit 1`. Lệch chính sách promotion → DEF-003. |

## CD

| Mục | Trạng thái | Ghi chú |
|---|---|---|
| DEV / STG / UAT / Production promotion | OPEN | `deploy.sh` cố ý `exit 1`. Chưa có môi trường. |
| Production human approval operational | OPEN | Có stage `input` trong Jenkinsfile, chưa chạy lần nào. |
| Rollback verified | OPEN | Chưa có cơ chế. |

## Security

| Mục | Trạng thái | Bằng chứng / phần thiếu |
|---|---|---|
| No secrets in Git | PARTIAL | 2026-10-03: grep regex toàn bộ lịch sử (AWS key, private key, GitHub/OpenAI token, Slack token, `password=`) → 0 kết quả; không có file `.pem/.key/.env` từng commit. **Không** phải secret scanner chuyên dụng (gitleaks/trufflehog chưa cài). |
| Jenkins credentials configured | OPEN | — |
| IAM least privilege | OPEN | Chưa kiểm kê IAM role của EC2. |
| Production credentials unavailable to normal agents | OPEN | Chưa có Production; chưa kiểm chứng. |

## Verification (§52)

| Mục | Trạng thái |
|---|---|
| Deliberate unit-test failure blocks DEV / STG / UAT / PROD | OPEN |
| Production cannot deploy without human approval | OPEN |

## Việc chỉ chủ dự án (người) làm được

1. Review và merge `chore/phase1-agent-factory-foundation` vào `main` qua PR; sau đó đồng bộ `develop` từ `main`.
2. Xác nhận chiến lược nhánh `main`/`develop`/`feature/*`/`release/*`.
3. Bật branch protection cho `main`, `develop` trên GitHub (spec §48).
4. Jenkins: tạo admin, credential GitHub, job multibranch (`jenkins/README.md`).
5. Đăng nhập Codex CLI; giao DEF-001 → DEF-003 cho Codex DevOps.
6. Duyệt `docs/capstone/SCOPE-AITUTOR.md` (🔒 Cổng hiểu bước [0]) — điều kiện để PM/PO tạo Epic/Feature.
7. Quyết định môi trường DEV/STG/UAT/PROD, IAM, secret store — việc A+, chưa có kế hoạch.
