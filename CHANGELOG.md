# Changelog

| Ngày | Thay đổi | Ghi chú kiểm chứng |
|---|---|---|
| 2026-10-03 | Thêm `CLAUDE.md` (tự nạp cho Claude Code) và `AGENTS.md`, cả hai trỏ về `CLAUDE_AI_Tutor.md`. | Chỉ là tài liệu; không có code/test. |
| 2026-10-03 | Thêm `docs/GLOSSARY.md` bản tạm, dựng **chỉ** từ nội dung repo, có cột nguồn; thuật ngữ thiếu định nghĩa (CASAN, PEP–PDP–RLS) được đánh dấu, không tự bịa. | Cần thay bằng GLOSSARY chính thức khi có. |
| 2026-10-03 | Viết `README.md`: trạng thái thực tế, bản đồ repo, danh sách tài liệu được tham chiếu nhưng chưa có. | Đã tìm trên toàn máy: không thấy `context.md`, GLOSSARY gốc, Orchestrator Guide, Program, Operating Model. |
| 2026-10-03 | `CLAUDE_AI_Tutor.md`: thêm ghi chú `context.md` chưa có trong repo. | Không đổi nội dung luật. |
| 2026-10-03 | Playbook bước [0]: thêm `docs/capstone/SCOPE-AITUTOR.md` (DRAFT): problem statement, 6 giả định, 6 quyết định nền (3 ràng buộc kiến trúc), 10 câu hỏi làm rõ, 4 hard-stop. | Chưa duyệt; 🔒 Cổng hiểu do chủ dự án thực hiện. |
| 2026-10-03 | Thêm `docs/capstone/HLD-AITUTOR.md` (DRAFT) theo yêu cầu chủ dự án làm HLD trước SPEC: nguyên tắc, C4 context/container, 4 luồng, edge vision, OCR adapter + quy tắc nhiều candidate, verify toán, state machine tutor, data model + độ nhạy, STRIDE, ngân sách latency, công thức chi phí, 8 spike kỹ thuật, quyết định mở. | Chưa duyệt. Sơ đồ Mermaid chưa render được (máy thiếu thư viện cho headless Chrome); cú pháp chỉ rà bằng mắt. |
