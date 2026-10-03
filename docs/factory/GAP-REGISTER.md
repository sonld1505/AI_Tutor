# Factory Phase 1 — Gap register

> Owner: Claude Scrum Master. Gap phát hiện khi đối chiếu repo với spec Phase 1 ngày 2026-10-03.
> Gap thuộc `scripts/**`, `Jenkinsfile` thuộc quyền Codex DevOps (`agents/codex/devops.md`) → ghi thành defect, Claude **không tự sửa**.

| ID | Gap | Loại | Xử lý | Trạng thái |
|---|---|---|---|---|
| G-01 | `validate-story.sh` cho PASS khi DoR rỗng, thiếu khoá, hoặc Story không có AC/test scenario | Defect engineering | DEF-001 → Codex DevOps; R-001 kiểm tay tạm thời | OPEN |
| G-02 | Khoá DoR lệch: Story `estimated` vs DoR `estimation_completed` (lỗi từ chính spec) | Template | Story template dùng `estimation_completed` | FIXED 2026-10-03 |
| G-03 | Story template thiếu `business_context`, `ui_impact`, `data_impact` (bắt buộc theo `CLAUDE.md`), thiếu khối DoD | Template | Đã bổ sung; `database_impact` đổi thành `data_impact` | FIXED 2026-10-03 |
| G-04 | `BLOCKED` được `ba.md` dùng nhưng không có trong state machine | Quy trình | Thêm vào `scrum-master.md` + trường `blocked_from` | FIXED 2026-10-03 |
| G-05 | `create-worktree.sh` mặc định dùng `develop`, nhánh này chỉ có `README.md` | Defect engineering + việc của người | DEF-002 → Codex DevOps; đồng bộ `develop` → chủ dự án | OPEN |
| G-06 | Jenkinsfile: PROD tự build lại thay vì promote artifact; STG/UAT không có cổng; không kiểm UAT acceptance; không có smoke | Defect engineering (tiềm ẩn) | DEF-003 → Codex DevOps | OPEN |
| G-07 | Không có nơi lưu backlog ưu tiên, roadmap, RAID, retrospective, defect | Artefact quản lý | Thêm template + `safe/backlog.yaml`, `safe/raid.yaml`, `safe/defects/`, `safe/retrospectives/` | FIXED 2026-10-03 |
| G-08 | Chưa có ánh xạ Playbook ↔ SAFe | Quy trình | `PLAYBOOK-SAFE-MAPPING.md` | FIXED 2026-10-03 |
| G-09 | `DEVBOOK` bắt buộc theo `CLAUDE.md` nhưng chưa có | Quy trình | `DEVBOOK-AITUTOR.md` | FIXED 2026-10-03 |
| G-10 | Không có tracker cho checklist §51 | Quy trình | `PHASE1-STATUS.md` | FIXED 2026-10-03 |
| G-11 | Chưa có validator DoD, chưa có schema YAML | Engineering | Spec xếp vào Phase 2 (§54) | DEFERRED |
| G-12 | Chưa có secret scanner chuyên dụng | Engineering | Thuộc gate security (`security-scan.sh`), Codex DevOps | OPEN |
| G-13 | Mọi mục CI/CD/Verification §51 | Engineering + người | Xem `PHASE1-STATUS.md` | OPEN |
