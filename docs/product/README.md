# AI Study Companion — Bộ tài liệu

Cập nhật: 08/10/2026 · Chủ dự án: Sơn · MVP: **Toán lớp 6 học kỳ 1, SGK Cánh diều** · Kickoff 08/10/2026

## Tài liệu hiện hành

| Tài liệu | Vai trò | Nguồn chuẩn cho |
| --- | --- | --- |
| [business-hld-v1.3.md](business-hld-v1.3.md) | Business HLD | Quyết định D01–D31, quy tắc đánh mã, use case U01–U25, KPI, kinh doanh, cổng S/G0/G1/G2 và go/no-go |
| [technical-hld-v1.3.md](technical-hld-v1.3.md) | Technical HLD | Kiến trúc, API, state machine, acceptance A01–A46 |
| [ai-study-companion-context-v0.5.md](ai-study-companion-context-v0.5.md) | Context cho coding agent | Bản tóm tắt; tham chiếu trực tiếp mã A |
| Kế hoạch Pilot (bản offline [`pilot-plan.html`](pilot-plan.html); [artifact](https://claude.ai/artifact/GUipf5SazWRNDdRaL6tT9x) chưa đồng bộ v1.3) | Checklist theo tuần | Phản chiếu Business HLD v1.3 §11 |
| Bộ slide use case ([artifact](https://claude.ai/artifact/NoZ82234fxTq97JCXnDkpH)) | Trình bày cho team | **Chưa đồng bộ v1.3** (còn theo v1.2) |

**Thứ tự ưu tiên khi mâu thuẫn:** Business HLD và Technical HLD v1.3 → context v0.5 → kế hoạch pilot và slide. Gặp mâu thuẫn thì dừng lại và báo Sơn.

**Quy tắc cập nhật:** đổi một quyết định chung thì sửa cả hai HLD trước, rồi mới đồng bộ context, kế hoạch pilot (cả bản offline) và slide.

**Quy tắc đánh mã:** D, U, A giữ số qua các phiên bản; mã mới nhận số tiếp theo; nội dung mã thay đổi ghi ở Business HLD §0.3.

## Tài liệu lịch sử (không dùng làm yêu cầu)

Nằm trong `history/`. Các file `Downloads/…` chỉ được nhắc tên, không có trong repository.

| File | Ghi chú |
| --- | --- |
| `history/business-hld-v1.2.md`, `history/technical-hld-v1.2.md` | Bộ 07/10; đã hợp nhất vào v1.3 |
| `history/ai-study-companion-context-v0.4.md` | Đã được v0.5 thay thế |
| `history/business-hld-v1.1.md`, `history/technical-hld-v1.1.md` | Bộ 06/10; đã hợp nhất vào v1.2 |
| `Downloads/business-hld_7_Oct.md`, `Downloads/technical-hld_7_Oct.md` | Bộ 07/10 (cũng ghi "1.1"); đã hợp nhất vào v1.2. **Không có trong repo.** |
| `history/ai-study-companion-context-v0.3.md` | Đã được v0.4 thay thế |
| `history/ai-study-companion-context-v0.2.md` | Nội dung v0.2.1 |
| `Downloads/business-hld.md`, `Downloads/technical-hld.md` | v1.0. **Không có trong repo.** |

## Còn mở

Xem Business HLD v1.3 §14: xác minh điều khoản Anthropic, Viettel AI, Azure; cấu hình máy tối thiểu; khối lượng rà soát của shadow teacher; nội dung đồng ý; đặt cọc; ngân sách.
