# BA AI Bootcamp — Workbook Bài tập Thực hành (track BA) v1.0

> **Bổ trợ cho:** Program (Phase 2 — Hands-on) · **track BA** theo §14.2.
> **Common Core:** dùng chung tư duy/Delegation/Governance/Capstone với các track khác — file này chỉ **thay bộ bài tập + rubric + đầu ra Customer Zero** cho vai trò **Business Analyst**.
> **Mục đích:** biến kỹ năng BA-trong-thời-đại-AI thành **bài tập cụ thể, phát-tay-làm-ngay**.
> **Công cụ xuyên suốt:** lái AI coding agent như orchestrator — nhập môn: Orchestrator Guide.
> **Thuật ngữ:** `docs/GLOSSARY.md`.
> **Cách dùng:** 6 bài chạy **trên CÙNG 1 case study** (hoặc 1 đề PB-01→06) → làm liên tục như một dự án thật; cohort có thể **trộn nghề** (BA/SA/Dev/PM cùng 1 đề, mỗi người nộp lát cắt của mình).
> **Ngày:** 2026-07-02 · **Phiên bản:** v1.0

---

## Changelog
| Version | Ngày | Nội dung |
|---|---|---|
| v1.0 | 2026-07-02 | Track BA tách từ Workbook Common: giữ Common Core (case §0, telemetry, chống rubber-stamping); 6 bài BA — Elicitation/Requirement · User Story + Acceptance Criteria · Process/BPMN · Backlog grooming · Prototype chạy được (Customer Zero mini) · Delegation Map. |

---

## 0. Case study chung — "Dự án LMS" *(giống mọi track)*

> Dùng chung cho cả 6 bài; hoặc thay bằng 1 đề **PB-01→PB-06** (`PM-AI-Bootcamp-ProjectBriefs-v1.0.md`). BA đổi tiền tố file theo mã đề (`REQ-PB01.md`…).

**Bối cảnh:** Công ty 500 nhân viên quản lý **đăng ký nghỉ phép** bằng email + Excel → chậm, sai sót, khó duyệt. Ban lãnh đạo muốn làm **Hệ thống Quản lý Nghỉ phép (LMS)** nội bộ.

**Brief thô từ stakeholder (cố tình mơ hồ, thiếu, mâu thuẫn):**
> *"Anh muốn một app cho nhân viên xin nghỉ phép online, sếp duyệt nhanh trên điện thoại. Phải thấy được số ngày phép còn lại. HR cần báo cáo cuối tháng. Càng sớm càng tốt, tầm 2 tháng. À mà phải tích hợp chấm công nữa. Bảo mật thì... chắc như mấy app nội bộ khác thôi. Ngân sách thì làm sao tối ưu nhất."*

**Ràng buộc giả định:** Team 1 PM + 1 BA (học viên) + 3 dev + 1 QA; mốc ~8 tuần; nội bộ, không safety-critical.

> 💡 *Brief thiếu rõ ràng để học viên thấy AI **không** thay được việc làm rõ intent — đó là việc cốt lõi của BA.*

---

## Khung chung mọi bài tập *(giống mọi track)*

Mỗi bài gồm: **Mục tiêu năng lực · Thời lượng · Input · Các bước · Sản phẩm nộp · Telemetry bắt buộc · Rubric (0–4) · Prompt mẫu.**

**Telemetry bắt buộc cho MỌI bài** (nộp kèm, thiếu = chưa hoàn thành):
| Trường | Ghi gì |
|---|---|
| Tool dùng | tên tool/model |
| Token (est) | tổng token in/out ước tính |
| Thời gian | phút làm bài (gồm review) |
| Số vòng lặp | bao nhiêu lần chỉnh prompt mới ra kết quả dùng được |
| Rework | có phải làm lại artefact không (có/không + lý do) |
| BA-edit | ≥1 điểm BA sửa sai/chỉnh intent của AI (mô tả ngắn) |

> **Đo trung thực:** thời gian là **giờ làm thật** (không suy từ token); token ghi **est** rồi **reconcile**; cột `BA-edit` là "đắt" nhất — đo **phán đoán của người**, không đo độ "đẹp" của AI.

---

## BA-EX-01 — Elicitation & Requirement: AI viết & review *(lõi chung với PM EX-01)*

- **Năng lực:** C1 AI Literacy · C2 Delegation · C6 Outcome.
- **Thời lượng:** 90 phút.

**Input:** Brief thô ở §0.

**Các bước:**
1. **AI sinh draft requirement** từ brief: mục tiêu, scope (in/out), stakeholder & user, NFR, ràng buộc, giả định.
2. **AI tự review**: liệt kê **mâu thuẫn / thiếu / mơ hồ** + sinh **danh sách câu hỏi elicitation** phân theo nhóm stakeholder (nhân viên / sếp duyệt / HR / IT).
3. **BA phán xử:** đánh dấu câu hỏi nào *thật sự* cần hỏi, câu nào AI tự suy luận sai. Chỉnh ≥1 điểm AI hiểu sai intent ("tích hợp chấm công" in/out MVP? "bảo mật như app khác" — cụ thể hoá thế nào?).
4. **Phản xạ hard-stop:** chỉ ≥1 chỗ brief **mâu thuẫn/không đủ để quyết** mà BA **KHÔNG để AI tự đoán** — ghi `[CHỜ LÀM RÕ]` (vd "~2 tháng" **vs** scope có tích hợp chấm công + migration).

**Sản phẩm nộp:**
- `REQ-LMS.md`: requirement có cấu trúc (đã qua tay BA).
- Danh sách ≥6 câu hỏi elicitation, mỗi câu gắn nhãn `[Hỏi stakeholder]` / `[AI tự sai]` + nhóm stakeholder.
- ≥1 điểm **hard-stop** `[CHỜ LÀM RÕ — không để AI đoán]`.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Đủ mục requirement, bám brief, ≥6 câu hỏi hợp lệ, BA đã sửa ≥1 điểm sai intent |
| 3 | Phân loại đúng câu hỏi thật vs AI-tự-sai; câu hỏi gắn đúng nhóm stakeholder; có ≥1 hard-stop hợp lý |
| 4 | Requirement có tiêu chí đo được + template elicitation tái dùng cho dự án khác |

**Prompt mẫu:**
> *"Bạn là BA. Từ brief sau, viết requirement có cấu trúc: Mục tiêu, Scope (in/out), Stakeholder & User, NFR, Ràng buộc, Giả định. Đánh dấu rõ chỗ brief chưa đủ thay vì bịa. Sau đó đóng vai reviewer khó tính: liệt kê mâu thuẫn/thiếu/mơ hồ và đặt câu hỏi elicitation phân theo nhóm stakeholder. Brief: [...]"*

---

## BA-EX-02 — User Story + Acceptance Criteria (Gherkin)

- **Năng lực:** C1 · C3 · C6.
- **Thời lượng:** 75 phút.

**Input:** `REQ-LMS.md` từ BA-EX-01.

**Các bước:**
1. AI phân rã requirement → **user story** dạng *As a… I want… so that…*, gom theo epic.
2. Với mỗi story, AI sinh **Acceptance Criteria** dạng **Gherkin** (Given / When / Then) — đo được, có case biên & case lỗi (vd hết ngày phép, duyệt trùng, huỷ đơn đã duyệt).
3. **BA rà theo INVEST** (Independent/Negotiable/Valuable/Estimable/Small/Testable): loại story "to mù", tách story quá lớn, bổ AC còn thiếu case biên mà AI bỏ.
4. BA đánh dấu ≥1 story mà AI viết AC **sai/thiếu case biên** rồi sửa.

**Sản phẩm nộp:**
- `STORIES-LMS.md`: ≥8 user story gom theo epic, mỗi story ≥1 AC Gherkin (đã qua tay BA).
- Ghi chú ≥2 chỗ BA sửa theo INVEST + lý do.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | ≥8 story đúng cú pháp + AC Gherkin, BA đã hiệu chỉnh |
| 3 | AC đo được + phủ case biên/lỗi; story qua kiểm INVEST; bắt được chỗ AI bỏ case biên |
| 4 | AC dùng thẳng cho QA viết test + dev nghiệm thu; template tái dùng |

**Prompt mẫu:**
> *"Từ requirement sau, sinh user story (As a…/I want…/so that…) gom theo epic. Mỗi story kèm Acceptance Criteria dạng Gherkin (Given/When/Then), gồm cả case biên và case lỗi. Nêu giả định. Requirement: [...]"* → BA rà lại theo INVEST, không bê nguyên.

---

## BA-EX-03 — Process mapping (As-is → To-be, BPMN)

- **Năng lực:** C3 Workflow Design · C6.
- **Thời lượng:** 60 phút.

**Input:** `REQ-LMS.md` + `STORIES-LMS.md`.

**Các bước:**
1. AI vẽ **luồng As-is** (email + Excel hiện tại) và **To-be** (có LMS), dạng mô tả bước + **swimlane** theo vai (Nhân viên / Sếp / HR / Hệ thống). Dùng text/Mermaid.
2. AI chỉ ra **điểm nghẽn** ở As-is và **điểm ra quyết định / phân nhánh** ở To-be (duyệt/từ chối, vượt hạn mức phép, uỷ quyền khi sếp vắng).
3. **BA rà:** phát hiện nhánh AI **bỏ sót** (sếp đi vắng ai duyệt? đơn quá khứ? huỷ sau duyệt?) và bước thừa; gắn mỗi bước với story ở EX-02 (truy vết).

**Sản phẩm nộp:**
- `PROCESS-LMS.md`: sơ đồ As-is + To-be (swimlane) + danh sách điểm nghẽn/nhánh quyết định.
- Bảng truy vết bước ↔ story.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Có As-is + To-be swimlane phủ các vai; BA đã hiệu chỉnh |
| 3 | Bắt được nhánh AI bỏ sót (uỷ quyền/huỷ/biên); truy vết bước ↔ story |
| 4 | Sơ đồ dùng thẳng cho dev/QA + nêu cải tiến quy trình đo được (giảm bước/thời gian) |

**Prompt mẫu:**
> *"Vẽ quy trình As-is (email+Excel) và To-be (có LMS) cho nghiệp vụ xin & duyệt nghỉ phép, dạng swimlane theo vai Nhân viên/Sếp/HR/Hệ thống (Mermaid). Chỉ rõ điểm nghẽn As-is và điểm ra quyết định/phân nhánh To-be. Nêu giả định. Ngữ cảnh: [...]"*

---

## BA-EX-04 — Backlog grooming & prioritization

- **Năng lực:** C3 · C5 · C6.
- **Thời lượng:** 60 phút.

**Input:** `STORIES-LMS.md` + ràng buộc mốc 8 tuần.

**Các bước:**
1. AI gom story thành **backlog** có **ưu tiên** theo **MoSCoW** (Must/Should/Could/Won't) và/hoặc **value × effort**.
2. AI đề xuất **phạm vi MVP** (Sprint 1–2) đủ chạy được với mốc 8 tuần + nêu giả định value.
3. **BA phán xử:** kiểm value có bịa không, đối chiếu ưu tiên với mục tiêu kinh doanh (HR báo cáo cuối tháng = Must hay Should?), cắt/nâng ≥2 mục có lý do; đánh dấu điểm AI đánh giá value sai.

**Sản phẩm nộp:**
- `BACKLOG-LMS.md`: backlog xếp ưu tiên (MoSCoW/value-effort) + phạm vi MVP đề xuất.
- Ghi chú ≥2 chỉnh ưu tiên của BA + lý do gắn mục tiêu kinh doanh.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Backlog có ưu tiên rõ tiêu chí; BA đã hiệu chỉnh |
| 3 | Ưu tiên bám mục tiêu kinh doanh; MVP khả thi với mốc; loại được value "bịa" |
| 4 | Backlog dùng lập kế hoạch sprint ngay + có tiêu chí re-prioritize khi thay đổi |

**Prompt mẫu:**
> *"Từ danh sách story sau, lập backlog xếp ưu tiên theo MoSCoW và value×effort. Đề xuất phạm vi MVP chạy được trong 8 tuần cho team 3 dev + 1 QA. Nêu rõ giả định về value. Story: [...]"* → BA đối chiếu lại với mục tiêu kinh doanh.

---

## BA-EX-05 — Prototype/clickable chạy được *(Customer Zero mini của BA)*

- **Năng lực:** C1 · C2 · C6 — *tự tay dựng để hiểu, chống rubber-stamping.*
- **Thời lượng:** 120 phút.

> **Đầu ra Customer Zero của BA (§14.2):** không dừng ở tài liệu — BA phải có **prototype clickable / luồng nghiệp vụ chạy được** để tự nghiệm thu chính requirement mình viết.

**Input:** `STORIES-LMS.md` + `PROCESS-LMS.md`.

**Các bước:**
1. Dùng AI dựng **prototype clickable** cho ≥1 luồng chính (xin phép → sếp duyệt → xem số ngày còn lại). Công cụ gợi ý: sinh **HTML/JS tĩnh** hoặc dùng builder (v0 / Figma Make / tương tự) — miễn **bấm qua được các bước**.
2. BA **tự chạy** prototype đối chiếu với AC ở EX-02: mỗi AC → **đạt / chưa đạt**; bắt chỗ luồng thực tế lệch requirement.
3. Ghi **Dev Book mini**: ≥3 điểm AI làm sai/hiểu sai khi dựng prototype và cách BA sửa (đây là bằng chứng "làm thật, không ký bừa").

**Sản phẩm nộp:**
- Prototype chạy được (link/kèm file) + hướng dẫn bấm thử 1 phút.
- `WALKTHROUGH-LMS.md`: bảng AC ↔ đạt/chưa + ≥3 mục Dev Book (AI-sai / BA-sửa).
- Telemetry (kèm số lần BA-edit).

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Prototype bấm qua được ≥1 luồng chính; có đối chiếu AC |
| 3 | Bắt được ≥3 chỗ prototype lệch requirement + Dev Book ghi rõ AI-sai/BA-sửa |
| 4 | Prototype đủ cho stakeholder review thật + rút ra thay đổi requirement từ việc chạy thử |

**Prompt mẫu:**
> *"Dựng prototype HTML/JS clickable cho luồng: nhân viên xin nghỉ phép → sếp duyệt → xem số ngày phép còn lại, đúng theo các Acceptance Criteria sau. Ưu tiên bấm-qua-được hơn đẹp. AC: [...]"* → BA tự chạy, đối chiếu, ghi chỗ lệch.

---

## BA-EX-06 — Delegation Map + Autonomy Leash *(Common Core, góc BA)*

- **Năng lực:** C2 AI Delegation · C4 Governance.
- **Thời lượng:** 75 phút.

**Input:** danh sách **công việc BA** (elicitation, viết story, vẽ process, groom backlog, dựng prototype, nghiệm thu AC…).

**Các bước:**
1. Lấy **≥12 việc BA**. Với mỗi việc điền: **nhóm 5-loại** (AI-do / Human-do / AI-review / Human-review / AI-không-nên) · **mức L0–L5** · **ai gỡ chốt duyệt**.
2. **Áp Leash A vs A+** *(nhắc: A ≈ L3, A+ ≈ L4 — 2 nấc của thang L0–L5, không phải khung khác)*: việc chạm **dữ liệu nhân sự / cam kết scope với stakeholder / chốt AC nghiệm thu** → **A+ chờ duyệt (BUILT-flagged)**; việc nháp tài liệu → **A**.
3. **BA giải trình:** 1 dòng lý do cho mỗi việc ≥ L3; chỉ ≥1 việc **cố giữ ở L1/L2** dù AI "làm được" (vd chốt intent với stakeholder — không giao AI).

**Sản phẩm nộp:**
- `DELEGATION-MAP-BA.md`: bảng ≥12 việc × (nhóm · L0–L5 · ai duyệt · A/A+ · lý do).
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | ≥12 việc đủ nhóm + mức + ai duyệt; lý do hợp lý |
| 3 | Phân biệt đúng A vs A+; việc chạm dữ liệu/cam kết đều A+ chờ duyệt; có việc cố giữ thấp |
| 4 | Map vận hành thật được; gắn cổng fail-closed cho từng nhóm hazard; tái dùng |

**Prompt mẫu:**
> *"Với danh sách công việc BA sau, đề xuất mỗi việc: (a) giao AI/giữ người/AI-review/human-review/AI-không-nên; (b) mức L0–L5; (c) ai duyệt. Đánh dấu việc chạm dữ liệu nhân sự hoặc chốt cam kết với stakeholder (cần kiểm soát chặt). KHÔNG nâng mức cho việc rủi ro cao. Việc: [...]"* → BA phán xử lại.

---

## Bảng ánh xạ bài tập ↔ năng lực (track BA)

| Bài | Trọng tâm BA | Tuần gợi ý | Năng lực chính | Bắt buộc tốt nghiệp |
|---|---|---|---|---|
| BA-EX-01 | Elicitation & Requirement | W1 | C1, C2, C6 | ✅ (lõi) |
| BA-EX-02 | User Story + AC (Gherkin) | W2 | C1, C3, C6 | ✅ |
| BA-EX-03 | Process/BPMN | W2 | C3, C6 | — |
| BA-EX-04 | Backlog grooming | W3 | C3, C5, C6 | — |
| BA-EX-05 | Prototype chạy được (Customer Zero mini) | W4 | C1, C2, C6 | ✅ |
| BA-EX-06 | Delegation Map | W3 | C2, C4 | — *(khuyến nghị mạnh)* |

> **Trọng số dịch về (theo §14.2):** Requirement & Acceptance Criteria **nặng hơn**; WBS/estimation nhẹ. Đầu ra Customer Zero = prototype/luồng nghiệp vụ chạy được.

---

## Hướng dẫn giảng viên (facilitator notes) *(giống mọi track)*

- **Chấm cái gì:** không chấm "AI trả lời hay" — chấm **phán xử của BA** (chỗ sửa sai AI, AC bổ sung, nhánh quy trình phát hiện). Cột `BA-edit` là bằng chứng quan trọng nhất.
- **Tiêu chí trượt — "rubber-stamping":** nộp output AI mà **không có dấu vết review của người** → tối đa 1 điểm dù nội dung "đẹp". EX-05 chống điều này bằng **prototype chạy thật + Dev Book**.
- **Bẫy cố ý:** brief mơ hồ (EX-01), case biên hay bị bỏ trong AC (EX-02), nhánh uỷ quyền/huỷ trong process (EX-03), value bịa khi ưu tiên (EX-04), prototype lệch requirement (EX-05).
- **Cohort trộn nghề:** cho BA/SA/Dev/PM cùng 1 đề PB → BA giao `REQ`/`STORIES` cho SA & Dev dùng tiếp → mô phỏng bàn giao thật.

---

*Track BA thuộc bộ Workbook nhiều-nghề dùng chung Common Core. Xem thêm track SA (`…-Workbook-SA-…`), Dev (`…-Workbook-Dev-…`), PM (`…-Workbook-Common-…`).*
