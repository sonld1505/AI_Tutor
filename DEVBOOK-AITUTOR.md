# DEVBOOK — AI Tutor

> Nhật ký **AI sai → người sửa** (Playbook bước [8], `CLAUDE.md`). Ghi ngay khi xảy ra, không viết bù.
> Cột "Ai phát hiện" phân biệt rõ **người** với **AI tự phát hiện**. Theo Playbook, 🔒 Cổng hiểu cần điểm *người* bắt được lỗi; dòng do AI tự phát hiện **không** thay thế được điểm đó.

| # | Ngày | AI đã làm gì | Sai ở đâu | Ai phát hiện | Sửa thế nào | Mức L | Cổng nào chặn | Hard-stop? |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-03 | Claude dựng `scripts/validate-story.sh` theo spec §15 (commit `619c632`) và ghi trong CHANGELOG là đã kiểm chứng (FAIL trên template, PASS trên story mẫu). | Chỉ thử ca có chữ `false`; không thử ca DoR rỗng/thiếu khoá → gate fail-open (`UNKNOWN` thành PASS). | AI tự phát hiện khi rà gap (Claude SM, phiên 2026-10-03). | Chủ dự án chọn hướng: ghi DEF-001 cho Codex DevOps thay vì Claude tự vá; SM kiểm DoR tay (R-001). | L3 | Không cổng nào chặn — chính gate bị lỗi. | Không |
| 2 | 2026-10-03 | Claude chép template Story và DoR nguyên văn từ spec §9.3, §10. | Khoá `estimated` ≠ `estimation_completed`; Story thiếu trường BA bắt buộc (`business_context`, `ui_impact`). Không đối chiếu chéo khi chép. | AI tự phát hiện khi rà gap. | Sửa `safe/templates/story.yaml`; kiểm bằng script so khoá (khớp). | L1 | Không | Không |
| 3 | 2026-10-03 | Claude dựng nền Phase 1 nhưng không tạo DEVBOOK dù `CLAUDE.md` bắt buộc. | Bỏ sót luật quy trình. | AI tự phát hiện khi rà gap. | Tạo file này. | L1 | Không | Không |
| 4 | 2026-10-03 | Claude viết vòng lặp test `echo "$(basename $c) exit=$?"`. | `$(...)` chạy trước nên `$?` bị reset → báo sai là template PASS validator. | AI tự phát hiện ngay (chạy lại riêng lẻ, template thực tế exit=1). | Lưu `rc=$?` trước khi in. Không ảnh hưởng file nào. | L3 | Không | Không |
| 5 | 2026-10-03 | Claude cập nhật `safe/raid.yaml` bằng `str.replace` trong Python (thêm US-FACTORY-001 vào `blocks` của I-002). | Chuỗi cần thay không khớp, nên `replace` không làm gì mà cũng không báo lỗi. | AI tự phát hiện khi grep lại kết quả. | Sửa bằng `sed` theo số dòng; các lần sửa sau dùng `assert` để chuỗi không khớp thì báo lỗi ngay. | L1 | Không | Không |
