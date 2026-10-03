# CLAUDE.md

> File này tự động nạp cho Claude Code. Luật chi tiết nằm ở `CLAUDE_AI_Tutor.md` — **đọc toàn bộ file đó trước khi làm bất cứ việc gì**.

## Thứ tự đọc bắt buộc

1. `CLAUDE_AI_Tutor.md` — bối cảnh sản phẩm AI Study Companion + luật camera/privacy/provider/tutor + nguyên tắc coding agent.
2. `README.md` — bản đồ repository và trạng thái thực tế.
3. `dev-book/PM-AI-Bootcamp-Capstone-Playbook-v1.0.md` — quy trình 11 bước (scope → spec → … → build → test → RTM).
4. Workbook theo vai trò khi cần: `dev-book/PM-AI-Bootcamp-Workbook-{Common,BA,SA,Dev}-v1.0.md`.
5. `docs/GLOSSARY.md` — thuật ngữ (L0–L5, Leash A/A+, fail-closed, …).

## Luật không được vi phạm (tóm tắt — bản đầy đủ ở `CLAUDE_AI_Tutor.md`)

- Repository hiện **chỉ có tài liệu**. Không mô tả code, EC2, camera, provider, benchmark hay doanh thu là đã có.
- Mock phải được gắn nhãn rõ trong code, log và tài liệu; không dùng mock để tuyên bố năng lực thật.
- Không dùng provider AI cho trẻ em khi điều khoản chưa được xác minh.
- Không đưa secret vào Git, tài liệu, log hoặc client.
- Camera: chỉ bật trong phiên, hướng xuống bàn, không lưu video mặc định, ảnh tạm có TTL.
- Không bịa số liệu; thiếu nguồn → ghi `N/A`.
- Việc A+ (schema, secret, dữ liệu trẻ em, provider, phân quyền) → trình plan, **dừng chờ người duyệt**.
- Mâu thuẫn hoặc thiếu thông tin để quyết → **hard-stop**, hỏi người dùng, không tự đoán.
- Sau mỗi thay đổi: chạy test, ghi cách chạy + phần chưa kiểm chứng, cập nhật `CHANGELOG.md`; ghi AI-sai/người-sửa vào DEVBOOK.
