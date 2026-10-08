# Playbook ↔ SAFe — quan hệ giữa hai quy trình

> Quyết định của chủ dự án ngày 2026-10-03:
> **Playbook 11 bước** (`dev-book/PM-AI-Bootcamp-Capstone-Playbook-v1.0.md`) là **nguồn nội dung sản phẩm**.
> **Dòng SAFe** (`CLAUDE.md` → Mandatory Flow) là **đường ống giao hàng**.
> SAFe không tự sinh yêu cầu: Epic/Feature/Story chỉ được lấy từ artefact Playbook **đã được người duyệt**.
> Nếu hai nguồn mâu thuẫn → hard-stop, hỏi chủ dự án.

## Bảng ánh xạ

| Bước Playbook | Artefact Playbook (`docs/capstone/`) | Artefact SAFe sinh ra | Vai trò Claude | Điều kiện |
|---|---|---|---|---|
| [0] Scope | `SCOPE-AITUTOR.md` | Epic (`safe/epics/`), mục trong `safe/backlog.yaml` | PM/PO | SCOPE được duyệt (🔒 Cổng hiểu) |
| [1] SW Spec | `SPEC-AITUTOR.md` | Feature (`safe/features/`), nguyên liệu Story | PM/PO + BA | SPEC được duyệt |
| [2] Module Map | `MODULEMAP-AITUTOR.md` | Thứ tự backlog, cờ `components` của Story | PM/PO | — |
| [3] Architecture | `ARCH-AITUTOR.md` (hiện có `HLD-AITUTOR.md` DRAFT) | DoR `architecture_reviewed`, `api_impact`/`data_impact` | BA | ADR dưới `docs/architecture/` |
| [4] WBS | `WBS-AITUTOR.md` | Story (`safe/stories/`) cho wave gần | BA | — |
| [5] Estimation | `EST-AITUTOR.md` | `story_points`, DoR `estimation_completed` | BA + SM | — |
| [6] Risk + Delegation | `RISK-AITUTOR.md`, `DELEGATION-MAP-AITUTOR.md` | `safe/raid.yaml`; vai trò Codex nào được giao | SM | Việc A+ phải có người duyệt |
| [7] DoR | `DOR-AITUTOR.md` | Story `READY` + `safe/pi-objectives/`, `safe/sprints/` | SM | DoR PASS mọi mục |
| [8] Build | code + `DEVBOOK-AITUTOR.md` | `IN_PROGRESS → DEV_COMPLETE` (Codex) | SM theo dõi | Claude không viết code sản phẩm |
| [9] Test & Gate | SIT/UAT | `TESTING → QA`, Jenkins, `safe/defects/` | SM theo dõi | NO UNIT TEST PASS = NO DEPLOY |
| [10] Trace + Telemetry | `RTM-AITUTOR.md` | Story `DONE` (DoD PASS) | SM | — |

## Hệ quả hiện tại

- **2026-10-08:** chủ dự án chọn bộ tài liệu trong `docs/product/` làm baseline sản phẩm; cùng ngày hợp nhất thành **v1.3**. Business HLD v1.3 giữ vai trò bước [0]–[1] (scope, D01–D31, use case U01–U25, KPI); Technical HLD v1.3 là đầu vào bước [3] (kiến trúc, API, acceptance A01–A46), chưa thay thế ADR. `SCOPE-AITUTOR.md` và `HLD-AITUTOR.md` đã SUPERSEDED; RAID I-001 CLOSED.
- Đã tạo ở trạng thái **DRAFT**: EPIC-001→007, F-001→024 (mỗi U và mỗi A gắn với ít nhất một Feature), `safe/roadmap.yaml` (kickoff 08/10, go/no-go 16/12/2026), Story tuần 1 US-001→003. Chưa có PI-001: chờ PO duyệt. Câu hỏi mở chặn refinement: RAID I-013.
- `DEVBOOK-AITUTOR.md` dùng chung cho cả Playbook (bước [8]) và factory: mọi lần AI sai → người sửa đều ghi vào đó.
- Điểm business value (PI, Epic) do chủ dự án quyết; agent chỉ đề xuất, để `null` khi chưa có quyết định.
