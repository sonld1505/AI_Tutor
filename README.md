# AI_Tutor

**AI Study Companion** — AI gia sư quan sát học sinh tự học trên giấy qua camera cố định tại bàn, hỗ trợ đúng lúc và xây dựng mô hình học tập dài hạn. MVP v0.1: Toán lớp 6.

## Trạng thái thực tế (2026-10-03)

Repository **chỉ có tài liệu**: bối cảnh sản phẩm, thiết kế đề xuất, giả định tài chính và bộ tài liệu phương pháp PM AI Bootcamp.
**Chưa có:** code, deployment, camera integration, benchmark OCR, provider production hợp lệ cho trẻ em, dữ liệu thị trường/doanh thu. Chi tiết: `CLAUDE_AI_Tutor.md` §3.

## Bản đồ repository

| Đường dẫn | Nội dung |
|---|---|
| `CLAUDE_AI_Tutor.md` | **Luật gốc** của dự án: tầm nhìn, scope MVP, camera/privacy, kiến trúc đề xuất, tutor policy, ràng buộc provider, nguyên tắc coding agent. |
| `CLAUDE.md` / `AGENTS.md` | Điểm vào cho Claude Code / agent khác — trỏ về `CLAUDE_AI_Tutor.md`. |
| `docs/GLOSSARY.md` | Thuật ngữ (bản tạm, dựng từ nội dung repo). |
| `dev-book/` | PM AI Bootcamp: Capstone Playbook (11 bước), Project Briefs (PB-01→06), Workbook Common/BA/SA/Dev. Dùng làm **phương pháp làm việc** cho dự án. |
| `docs/capstone/` | Artefact Capstone theo Playbook: `SCOPE-AITUTOR.md`, `HLD-AITUTOR.md` (đều DRAFT). |
| `CHANGELOG.md` | Nhật ký thay đổi. |

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

Đọc theo thứ tự trong `CLAUDE.md`. Đang ở Playbook bước [0]: `docs/capstone/SCOPE-AITUTOR.md` (DRAFT, chờ chủ dự án duyệt và qua 🔒 Cổng hiểu).
