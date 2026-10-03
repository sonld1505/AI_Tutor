# SA AI Bootcamp — Workbook Bài tập Thực hành (track SA) v1.0

> **Bổ trợ cho:** Program (Phase 2 — Hands-on) · **track SA (Solution Architect)** theo §14.2.
> **Common Core:** dùng chung tư duy/Delegation/Governance/Capstone với các track khác — file này chỉ **thay bộ bài tập + rubric + đầu ra Customer Zero** cho vai trò **kiến trúc sư giải pháp**.
> **Đặc thù SA:** đào **sâu nhất** về kiến trúc & trade-off, NFR, threat model, **Design-first / 4 lăng kính**.
> **Công cụ xuyên suốt:** lái AI coding agent như orchestrator — nhập môn: Orchestrator Guide.
> **Thuật ngữ:** `docs/GLOSSARY.md`.
> **Cách dùng:** 6 bài chạy **trên CÙNG 1 case study** (hoặc 1 đề PB-01→06); cohort có thể **trộn nghề**.
> **Ngày:** 2026-07-02 · **Phiên bản:** v1.0

---

## Changelog
| Version | Ngày | Nội dung |
|---|---|---|
| v1.0 | 2026-07-02 | Track SA tách từ Workbook Common: giữ Common Core (case §0, telemetry, chống rubber-stamping); 6 bài SA — Kiến trúc & trade-off + ADR · Chọn tech stack có tiêu chí · NFR & kiến trúc đáp ứng · Threat model + Design-first 4 lăng kính · Vertical slice có kiến trúc thật (Customer Zero) · Delegation Map. |

---

## 0. Case study chung — "Dự án LMS" *(giống mọi track)*

> Dùng chung; hoặc thay bằng 1 đề **PB-01→PB-06** (`PM-AI-Bootcamp-ProjectBriefs-v1.0.md`). SA đổi tiền tố file theo mã đề (`ARCH-PB01.md`…).

**Bối cảnh:** Công ty 500 nhân viên quản lý **đăng ký nghỉ phép** bằng email + Excel → chậm, sai sót. Cần **Hệ thống Quản lý Nghỉ phép (LMS)** nội bộ.

**Brief thô từ stakeholder (cố tình mơ hồ, thiếu, mâu thuẫn):**
> *"Anh muốn một app cho nhân viên xin nghỉ phép online, sếp duyệt nhanh trên điện thoại. Phải thấy được số ngày phép còn lại. HR cần báo cáo cuối tháng. Càng sớm càng tốt, tầm 2 tháng. À mà phải tích hợp chấm công nữa. Bảo mật thì... chắc như mấy app nội bộ khác thôi. Ngân sách thì làm sao tối ưu nhất."*

**Ràng buộc giả định:** Team 1 PM + 1 SA (học viên) + 3 dev + 1 QA; mốc ~8 tuần; nội bộ, ~500 user, có tích hợp hệ chấm công; không safety-critical nhưng chứa **dữ liệu nhân sự**.

> 💡 *Brief mơ hồ để SA thấy: AI dựng được kiến trúc nháp rất nhanh, nhưng **quyết định trade-off & chịu trách nhiệm là việc của SA.***

---

## Khung chung mọi bài tập *(giống mọi track)*

Mỗi bài gồm: **Mục tiêu năng lực · Thời lượng · Input · Các bước · Sản phẩm nộp · Telemetry bắt buộc · Rubric (0–4) · Prompt mẫu.**

**Telemetry bắt buộc cho MỌI bài** (thiếu = chưa hoàn thành):
| Trường | Ghi gì |
|---|---|
| Tool dùng | tên tool/model |
| Token (est) | tổng token in/out ước tính |
| Thời gian | phút làm bài (gồm review) |
| Số vòng lặp | bao nhiêu lần chỉnh prompt mới ra kết quả dùng được |
| Rework | có phải làm lại artefact không (có/không + lý do) |
| SA-edit | ≥1 điểm SA sửa sai/chỉnh trade-off của AI (mô tả ngắn) |

> **Đo trung thực:** thời gian là **giờ thật**; token **est → reconcile**; `SA-edit` đo **phán đoán kiến trúc của người**, không đo độ "đẹp" của sơ đồ AI vẽ.

---

## SA-EX-01 — Kiến trúc & trade-off + ADR

- **Năng lực:** C1 · C3 Workflow/System Design · C6 Outcome.
- **Thời lượng:** 120 phút.

**Input:** `REQ-LMS.md` (từ BA hoặc tự viết theo brief §0).

**Các bước:**
1. AI đề xuất **2–3 phương án kiến trúc** (vd monolith modular / tách service / serverless) — mỗi phương án: sơ đồ thành phần (Mermaid/C4 mức Context+Container), luồng dữ liệu chính, cách tích hợp chấm công.
2. AI lập **bảng trade-off** theo tiêu chí: chi phí, thời gian ra MVP (mốc 8 tuần), vận hành, mở rộng, rủi ro bảo mật dữ liệu nhân sự.
3. **SA phán xử:** chọn 1 phương án + **viết ADR** (Architecture Decision Record: bối cảnh · lựa chọn · lý do · hệ quả · phương án bị loại). Chỉnh ≥1 chỗ AI đánh giá trade-off **sai/thiên lệch** (vd coi nhẹ chi phí vận hành serverless, hoặc over-engineer microservices cho 500 user).
4. **Hard-stop:** đánh dấu ≥1 quyết định **không đủ dữ liệu để chốt** → ghi giả định cần xác nhận, không để AI tự quyết.

**Sản phẩm nộp:**
- `ARCH-LMS.md`: 2–3 phương án + sơ đồ + bảng trade-off.
- `ADR-001.md`: quyết định kiến trúc đã chọn (đã qua tay SA).
- ≥1 điểm chỉnh trade-off sai của AI + ≥1 hard-stop.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | ≥2 phương án có sơ đồ + trade-off; ADR đủ mục; SA đã chỉnh ≥1 điểm |
| 3 | Trade-off bám tiêu chí thật (mốc/chi phí/bảo mật); bắt được chỗ AI over/under-engineer; hard-stop hợp lý |
| 4 | ADR dùng thẳng cho team + có tiêu chí xem lại quyết định khi ràng buộc đổi |

**Prompt mẫu:**
> *"Bạn là SA. Từ requirement sau, đề xuất 2–3 phương án kiến trúc cho hệ nội bộ ~500 user, mốc 8 tuần, có tích hợp hệ chấm công, chứa dữ liệu nhân sự. Mỗi phương án: sơ đồ C4 (Context+Container, Mermaid), luồng dữ liệu, cách tích hợp. Lập bảng trade-off theo chi phí/thời-gian-MVP/vận-hành/mở-rộng/bảo-mật. Nêu giả định, KHÔNG tự chốt. Requirement: [...]"* → SA chọn + viết ADR.

---

## SA-EX-02 — Chọn tech stack có tiêu chí

- **Năng lực:** C1 · C3 · C5.
- **Thời lượng:** 75 phút.

**Input:** `ADR-001.md` (phương án đã chọn).

**Các bước:**
1. AI đề xuất **stack** (frontend / backend / DB / hạ tầng / tích hợp) kèm **ma trận đánh giá** theo tiêu chí: phù hợp năng lực team, thời gian học, chi phí license/hạ tầng, cộng đồng/hỗ trợ, bảo mật.
2. AI nêu **ràng buộc & rủi ro** mỗi lựa chọn + phương án thay thế.
3. **SA phán xử:** đối chiếu với năng lực thật của team (3 dev: 2 trung cấp + 1 mới), loại lựa chọn "hot nhưng team chưa quen", chốt stack + ghi lý do; đánh dấu ≥1 chỗ AI chọn theo "trend" thay vì phù hợp.

**Sản phẩm nộp:**
- `TECHSTACK-LMS.md`: ma trận đánh giá + stack chốt + lý do + rủi ro tồn đọng.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Stack đủ tầng + ma trận có tiêu chí; SA đã chỉnh |
| 3 | Lựa chọn bám năng lực team + chi phí thật; loại được lựa chọn "theo trend" |
| 4 | Có phân tích nhạy cảm (đổi ràng buộc → đổi lựa chọn) + kế hoạch giảm rủi ro "team chưa quen" |

**Prompt mẫu:**
> *"Đề xuất tech stack cho kiến trúc đã chọn (LMS nội bộ). Lập ma trận đánh giá theo: phù hợp team (3 dev, 1 mới), thời gian học, chi phí, cộng đồng, bảo mật. Nêu rủi ro & phương án thay thế mỗi lựa chọn. KHÔNG chọn theo độ 'hot'. Kiến trúc: [...]"* → SA đối chiếu năng lực team.

---

## SA-EX-03 — NFR chi tiết & kiến trúc đáp ứng

- **Năng lực:** C3 · C4 · C6.
- **Thời lượng:** 75 phút.

**Input:** `REQ-LMS.md` + `ARCH-LMS.md`.

**Các bước:**
1. AI cụ thể hoá **NFR đo được**: hiệu năng (thời gian phản hồi, tải đồng thời mùa cao điểm cuối tháng), khả dụng (uptime), bảo mật (phân quyền, mã hoá dữ liệu nhân sự, audit log), khả năng bảo trì, sao lưu/khôi phục.
2. Với mỗi NFR, AI chỉ **thành phần kiến trúc nào chịu trách nhiệm** đáp ứng + cách kiểm chứng.
3. **SA phán xử:** thay các NFR sáo rỗng ("phải nhanh", "phải bảo mật") bằng **con số/tiêu chí đo được**; đối chiếu với brief "bảo mật như app khác" → cụ thể hoá đúng dữ liệu nhân sự; đánh dấu NFR AI bịa số không căn cứ.

**Sản phẩm nộp:**
- `NFR-LMS.md`: bảng NFR (chỉ tiêu đo được · thành phần chịu trách nhiệm · cách kiểm chứng).
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | NFR phủ đủ nhóm + đo được; gắn thành phần kiến trúc |
| 3 | Thay được NFR sáo rỗng bằng số có căn cứ; NFR bảo mật đúng đặc thù dữ liệu nhân sự |
| 4 | NFR gắn cách test/nghiệm thu cụ thể + ngưỡng cảnh báo vận hành |

**Prompt mẫu:**
> *"Cụ thể hoá NFR đo được cho LMS nội bộ ~500 user (cao điểm cuối tháng), chứa dữ liệu nhân sự: hiệu năng, khả dụng, bảo mật, bảo trì, backup. Mỗi NFR: chỉ tiêu đo được, thành phần kiến trúc chịu trách nhiệm, cách kiểm chứng. KHÔNG dùng từ chung chung như 'phải nhanh/bảo mật'. Ngữ cảnh: [...]"*

---

## SA-EX-04 — Threat model (STRIDE) + Design-first / 4 lăng kính

- **Năng lực:** C4 Governance & Risk · C2 Delegation.
- **Thời lượng:** 90 phút.

**Input:** `ARCH-LMS.md` + `NFR-LMS.md`.

**Các bước:**
1. AI dựng **threat model STRIDE** (Spoofing/Tampering/Repudiation/Info-disclosure/DoS/Elevation) cho các điểm nhạy: đăng nhập, duyệt phép, tích hợp chấm công, dữ liệu nhân sự — mỗi mối đe doạ + biện pháp.
2. **Review chéo 4 lăng kính** (Design-first — cách làm RevenueOS): rà thiết kế qua **Req / SIT / UAT / Arch** — kiến trúc có đáp ứng đủ requirement? test tích hợp/nghiệm thu phủ được? có lỗ hổng kiến trúc?
3. **SA phán xử:** loại biện pháp chung chung, gắn mỗi biện pháp AI-liên-quan với **cổng fail-closed** (vd dữ liệu nhân sự **không** vào prompt AI; code AI sinh **phải** review trước merge); đánh dấu ≥1 threat AI bỏ sót.

**Sản phẩm nộp:**
- `THREATMODEL-LMS.md`: bảng STRIDE + biện pháp + cổng chặn.
- `DESIGN-REVIEW-4L.md`: kết quả rà 4 lăng kính (mỗi lăng kính ≥1 phát hiện/xác nhận).
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | STRIDE phủ điểm nhạy chính + biện pháp; có rà 4 lăng kính |
| 3 | Biện pháp gắn cổng fail-closed cụ thể; bắt được threat AI bỏ sót; 4 lăng kính ra phát hiện thật |
| 4 | Threat model dùng cho security review thật + gắn owner/kiểm chứng từng biện pháp |

**Prompt mẫu:**
> *"Dựng threat model STRIDE cho LMS (đăng nhập, duyệt phép, tích hợp chấm công, dữ liệu nhân sự). Mỗi điểm: các mối đe doạ theo STRIDE + biện pháp. Sau đó rà thiết kế qua 4 lăng kính Requirement/SIT/UAT/Architecture, chỉ ra chỗ chưa phủ. Kiến trúc & NFR: [...]"* → SA gắn cổng fail-closed, không nhận biện pháp sáo rỗng.

---

## SA-EX-05 — Vertical slice có kiến trúc thật *(Customer Zero mini của SA)*

- **Năng lực:** C1 · C3 · C6 — *tự tay dựng để hiểu, chống rubber-stamping.*
- **Thời lượng:** 150 phút.

> **Đầu ra Customer Zero của SA (§14.2):** không dừng ở sơ đồ — SA phải dựng **lát cắt dọc có kiến trúc thật chạy được** để chứng minh kiến trúc mình chọn khả thi.

**Input:** `ADR-001.md` + `TECHSTACK-LMS.md`.

**Các bước:**
1. Dùng AI dựng **skeleton chạy được** theo kiến trúc đã chọn cho 1 luồng dọc (vd: API xin phép → lưu DB → sếp duyệt), đúng ranh giới thành phần trong ADR (không để AI trộn tầng bừa).
2. SA **tự chạy** + kiểm: ranh giới thành phần có đúng ADR? điểm tích hợp có cô lập được? NFR bảo mật (phân quyền) có chỗ móc vào?
3. Ghi **Dev Book mini** ≥3 điểm AI dựng **lệch kiến trúc/sai ranh giới** và cách SA nắn lại; cập nhật sơ đồ C4 khớp thực tế chạy.

**Sản phẩm nộp:**
- Skeleton chạy được (repo/link) + hướng dẫn chạy + sơ đồ C4 cập nhật khớp code.
- `SLICE-NOTES.md`: ≥3 mục Dev Book (AI-lệch-kiến-trúc / SA-nắn) + đối chiếu ranh giới thành phần với ADR.
- Telemetry (kèm SA-edit).

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Lát cắt dọc chạy được; ranh giới thành phần cơ bản theo ADR |
| 3 | Bắt & nắn được ≥3 chỗ AI lệch kiến trúc; sơ đồ C4 khớp code chạy; điểm tích hợp cô lập |
| 4 | Slice làm nền mở rộng thật + chứng minh NFR then chốt (vd phân quyền) bằng chạy thử |

**Prompt mẫu:**
> *"Dựng skeleton chạy được cho luồng 'xin phép → lưu DB → sếp duyệt' theo kiến trúc trong ADR sau, giữ đúng ranh giới thành phần (không trộn tầng). Ưu tiên chạy được + đúng cấu trúc hơn đầy đủ tính năng. ADR & stack: [...]"* → SA tự chạy, đối chiếu ranh giới, ghi chỗ lệch.

---

## SA-EX-06 — Delegation Map + Autonomy Leash *(Common Core, góc SA)*

- **Năng lực:** C2 AI Delegation · C4 Governance.
- **Thời lượng:** 75 phút.

**Input:** danh sách **quyết định/việc kiến trúc** (chọn phương án, chốt stack, viết ADR, dựng skeleton, threat model, chuẩn hoá pattern…).

**Các bước:**
1. Lấy **≥12 việc SA**. Mỗi việc điền: **nhóm 5-loại** · **mức L0–L5** · **ai gỡ chốt duyệt**.
2. **Áp Leash A vs A+** *(A ≈ L3, A+ ≈ L4)*: **quyết định kiến trúc/trade-off/chốt stack** → SA **đích thân** (giữ thấp, dù AI "làm được"); **sinh skeleton/boilerplate/sơ đồ nháp** → A; việc chạm bảo mật/dữ liệu nhân sự → **A+ chờ duyệt (BUILT-flagged)**.
3. **SA giải trình:** 1 dòng lý do mỗi việc ≥ L3; chỉ ≥1 quyết định kiến trúc **cố ý không giao AI** + vì sao (phán đoán hiếm, hệ quả dài hạn).

**Sản phẩm nộp:**
- `DELEGATION-MAP-SA.md`: bảng ≥12 việc × (nhóm · L0–L5 · ai duyệt · A/A+ · lý do).
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | ≥12 việc đủ nhóm + mức + ai duyệt; lý do hợp lý |
| 3 | Quyết định kiến trúc cốt lõi giữ ở người; việc chạm bảo mật đều A+ chờ duyệt |
| 4 | Map vận hành thật + tách rõ "phán đoán kiến trúc (người)" vs "sinh tạo đóng-hộp-được (AI)" |

**Prompt mẫu:**
> *"Với danh sách việc kiến trúc sau, đề xuất mỗi việc: (a) giao AI/giữ người/AI-review/human-review/AI-không-nên; (b) mức L0–L5; (c) ai duyệt. Đánh dấu quyết định trade-off cốt lõi và việc chạm bảo mật/dữ liệu nhân sự. KHÔNG nâng mức cho quyết định kiến trúc hệ quả dài hạn. Việc: [...]"* → SA phán xử lại.

---

## Bảng ánh xạ bài tập ↔ năng lực (track SA)

| Bài | Trọng tâm SA | Tuần gợi ý | Năng lực chính | Bắt buộc tốt nghiệp |
|---|---|---|---|---|
| SA-EX-01 | Kiến trúc & trade-off + ADR | W1 | C1, C3, C6 | ✅ (lõi) |
| SA-EX-02 | Chọn tech stack | W2 | C1, C3, C5 | — |
| SA-EX-03 | NFR & kiến trúc đáp ứng | W2 | C3, C4, C6 | ✅ |
| SA-EX-04 | Threat model + Design-first 4 lăng kính | W3 | C4, C2 | ✅ |
| SA-EX-05 | Vertical slice có kiến trúc thật (Customer Zero) | W4 | C1, C3, C6 | ✅ |
| SA-EX-06 | Delegation Map | W3 | C2, C4 | — *(khuyến nghị mạnh)* |

> **Trọng số dịch về (theo §14.2):** thiết kế/NFR **nặng**; báo cáo tiến độ nhẹ. Đầu ra Customer Zero = vertical slice có kiến trúc thật + ADR + sơ đồ.

---

## Hướng dẫn giảng viên (facilitator notes) *(giống mọi track)*

- **Chấm cái gì:** chấm **phán đoán kiến trúc của SA** (chỗ sửa trade-off AI thiên lệch, threat bổ sung, ranh giới nắn lại) — không chấm "sơ đồ AI vẽ đẹp". Cột `SA-edit` là bằng chứng quan trọng nhất.
- **Tiêu chí trượt — "rubber-stamping":** nhận kiến trúc/ADR AI sinh mà **không giải trình được trade-off** → tối đa 1 điểm. EX-05 chống điều này bằng **slice chạy thật + Dev Book**.
- **Bẫy cố ý:** AI over-engineer microservices cho 500 user (EX-01), chọn stack theo trend (EX-02), NFR sáo rỗng/bịa số (EX-03), threat bỏ sót info-disclosure dữ liệu nhân sự (EX-04), skeleton trộn tầng sai ADR (EX-05).
- **Cohort trộn nghề:** SA nhận `REQ`/`STORIES` từ BA, giao `ARCH`/`ADR`/`TECHSTACK` cho Dev dựng tiếp → mô phỏng bàn giao thật.

---

*Track SA thuộc bộ Workbook nhiều-nghề dùng chung Common Core. Xem thêm track BA (`…-Workbook-BA-…`), Dev (`…-Workbook-Dev-…`), PM (`…-Workbook-Common-…`).*
