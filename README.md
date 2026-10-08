# AI_Tutor

**AI Study Companion** — app trên smartphone đặt trên giá đỡ: học sinh lớp 6 tự làm đề Toán in một trang, làm bài trong vở, gọi "Cô ơi" khi cần kiểm tra hoặc gợi ý, không phải chạm máy; cô chỉ gợi ý trong phạm vi đã học; phụ huynh nhận báo cáo theo tờ đề. MVP: Toán lớp 6 HK1 (SGK Cánh diều), Android 15+ và iOS 18.7+, pilot tối đa 50 gia đình từ 08/10 đến 16/12/2026.

## Trạng thái thực tế (2026-10-08)

Repository **chỉ có tài liệu**: baseline sản phẩm v1.3 (`docs/product/`), thiết kế đề xuất, giả định kinh doanh, bộ tài liệu phương pháp PM AI Bootcamp, nền Factory Phase 1 và backlog sản phẩm ở trạng thái DRAFT.
**Chưa có:** code, deployment, camera integration, benchmark OCR, provider production hợp lệ cho trẻ em, dữ liệu thị trường/doanh thu. Chi tiết: `CLAUDE_AI_Tutor.md` §3.

## Bản đồ repository

| Đường dẫn | Nội dung |
|---|---|
| `CLAUDE_AI_Tutor.md` | **Luật gốc** của dự án: thứ tự ưu tiên nguồn, camera/privacy, tutor policy, ràng buộc provider, nguyên tắc coding agent; phần sản phẩm trỏ về baseline v1.3. |
| `docs/product/` | **Baseline sản phẩm v1.3** (2026-10-08): Business HLD (D01–D30, U01–U25, KPI, cổng pilot), Technical HLD (kiến trúc, API, A01–A46), context v0.5, `pilot-plan.html`. `history/` là bản cũ (v1.1, v1.2, v0.2–v0.4). |
| `CLAUDE.md` / `AGENTS.md` | Điểm vào cho Claude Code / agent khác — trỏ về `CLAUDE_AI_Tutor.md`. |
| `docs/GLOSSARY.md` | Thuật ngữ (bản tạm, dựng từ nội dung repo). |
| `dev-book/` | PM AI Bootcamp: Capstone Playbook (11 bước), Project Briefs (PB-01→06), Workbook Common/BA/SA/Dev. Dùng làm **phương pháp làm việc** cho dự án. |
| `docs/capstone/` | `SCOPE-AITUTOR.md`, `HLD-AITUTOR.md`: **SUPERSEDED** bởi baseline v1.3, giữ để tra lịch sử. |
| `CHANGELOG.md` | Nhật ký thay đổi. |
| `docs/factory/` | Spec Factory Phase 1 (SAFe-inspired, Claude PM/BA/SM + Codex engineering + Jenkins); `PHASE1-STATUS.md` (nghiệm thu §51 — **chưa hoàn thành**), `GAP-REGISTER.md`, `PLAYBOOK-SAFE-MAPPING.md`. |
| `DEVBOOK-AITUTOR.md` | Nhật ký AI sai → người sửa. |
| `context/` | File điều hướng bối cảnh cho agent (product, architecture, business rules, glossary) — trỏ về nguồn gốc. |
| `agents/claude/`, `agents/codex/` | Định nghĩa vai trò: Claude PM/PO, BA, Scrum Master; Codex Backend, Frontend, Android, iOS, Tester, QA, DevOps. |
| `safe/` | Artefact SAFe: `epics/` (EPIC-001→007, DRAFT), `features/` (F-001→024, DRAFT), `stories/` (factory + tuần 1, DRAFT), `roadmap.yaml` (08/10 → 16/12/2026 theo cổng S/G0/G1/G2), `backlog.yaml` (chờ PO duyệt), `pi-objectives/`, `retrospectives/` (trống), `raid.yaml`, `defects/` (DEF-001→003 cho Codex DevOps) và `templates/` (Epic, Feature, Story, PI, Sprint, DoR, DoD, Backlog, Roadmap, RAID, Retrospective, Defect). |
| `factory/` | `config/`, `orchestrator/`, `state/`, `logs/` — chưa có orchestrator (Phase 1 có giám sát). |
| `scripts/`, `Jenkinsfile`, `Makefile`, `jenkins/README.md` | Quality gate **fail-closed**: NO UNIT TEST PASS = NO DEPLOY. Integration, security, artifact và deploy hiện **cố ý trả lỗi** cho tới khi được hiện thực. |
| `backend/`, `frontend/`, `android/`, `ios/`, `tests/`, `infrastructure/`, `jenkins/` | Khung thư mục rỗng; chưa có code. |

## Tài liệu được tham chiếu nhưng chưa có trong repo

Các file dưới đây được nhắc tới nhưng **không tồn tại** trong repository hay trên máy. Không được tự viết lại nội dung của chúng; cần chủ dự án cung cấp.

| Tài liệu | Ai tham chiếu | Ảnh hưởng | Thay thế tạm |
|---|---|---|---|
| `context.md` (Project Context gốc) | `CLAUDE_AI_Tutor.md` | Không đối chiếu được nguồn gốc của mô hình tài chính/roadmap | `CLAUDE_AI_Tutor.md` là bản tổng hợp từ nó |
| `docs/GLOSSARY.md` chính thức | mọi file `dev-book/` | — | `docs/GLOSSARY.md` bản tạm |
| *Orchestrator Guide* | Workbook, Playbook | Thiếu chi tiết vòng 7 nhịp | Tóm tắt trong Playbook: Context→Plan→Delegate→Execute→Gate→Log→Iterate |
| *Program* (§5, §7–§10, §14) | Workbook, Playbook | Thiếu rubric/KPI tổng | Rubric từng bài có trong Workbook |
| *Operating Model* (L0–L5, Leash, governance) | Playbook | Thiếu định nghĩa đầy đủ L0–L5, CASAN | Định nghĩa rút gọn trong Workbook Common EX-06 |
| Artefact RevenueOS (`ARCHITECTURE.md`, `DEV_STATUS.md`, `rtm_check.py`, …) | Playbook | Chỉ là ví dụ tham chiếu | Không cần cho AI Tutor |

## Bắt đầu

Đọc theo thứ tự trong `CLAUDE.md`. Baseline sản phẩm: `docs/product/README.md`. Việc tiếp theo: chủ dự án duyệt Epic/Feature/backlog/roadmap (đều DRAFT) và chốt câu hỏi mở ở RAID I-013 (xác minh điều khoản nhà cung cấp, đồng ý, ngân sách), rồi refine Story tuần 1 cho cổng S (14/10).
