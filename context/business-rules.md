# Business Rules

> File điều hướng cho agent. Đây là các luật **bắt buộc**.

| Luật | Nguồn |
|---|---|
| Camera, micro, chặn người, ảnh chỉ gửi khi có trigger, ẩn danh hóa trước khi gửi nhà cung cấp, TTL 7 ngày, hai loại đồng ý, xuất/xóa dữ liệu | `CLAUDE_AI_Tutor.md` §5; `docs/product/business-hld-v1.3.md` §7 |
| Rảnh tay: không bắt trẻ chạm máy trong buổi học, kể cả chụp đề | `docs/product/business-hld-v1.3.md` D03; `docs/product/technical-hld-v1.3.md` §1 |
| Tutor: im lặng khi chưa gọi, UNKNOWN ≠ WRONG, gợi ý nhỏ nhất L1→L3, chỉ trong phạm vi đã học, không khóa trợ giúp | `CLAUDE_AI_Tutor.md` §7; `docs/product/business-hld-v1.3.md` §4, §5.5 |
| Không mở READY khi bộ đề/scope chưa xác nhận; không mặc định scope = toàn lớp 6 | `docs/product/technical-hld-v1.3.md` §8.2, §14 |
| Câu khó/chưa hỗ trợ vẫn trong tổng số câu | `docs/product/business-hld-v1.3.md` §4 nguyên tắc 11 |
| Provider AI cho trẻ em phải được xác minh điều khoản trước khi dùng | `CLAUDE_AI_Tutor.md` §10 |
| Mock/fake adapter phải gắn nhãn; không bịa số liệu | `CLAUDE_AI_Tutor.md` §11, `CLAUDE.md` |
| Thay đổi sản phẩm (phạm vi dữ liệu, chặn trợ giúp, tự bật camera, lời giải đầy đủ, mở scope toàn lớp 6, giá) cần chủ dự án quyết | `docs/product/business-hld-v1.3.md` §13 |
| Security/privacy tối thiểu cho factory | `docs/factory/AI_Tutor_Phase1_Agent_Factory_Foundation.md` §39 |

Câu hỏi nghiệp vụ còn mở: `docs/product/business-hld-v1.3.md` §14 và `safe/raid.yaml`. Agent không được tự trả lời các câu hỏi này.
