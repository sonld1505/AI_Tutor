# PM AI Bootcamp — Workbook Bài tập Thực hành (Common) v2.0

> **Bổ trợ cho:** `Program` (Phase 2 — Hands-on).
> **Mục đích:** biến các assignment guideline (T1–T10) thành **bài tập cụ thể, phát-tay-làm-ngay**.
> **Phạm vi:** chỉ các bài **common** — không phụ thuộc chuẩn chuyên ngành; mọi PM đều làm được.
> **Cách dùng:** 5 bài tập chạy **trên CÙNG 1 case study** → học viên làm liên tục như một dự án thật.
> **Công cụ xuyên suốt:** lái **Claude Code như "super orchestrator"** làm trọn từng bước (Context→Plan→Delegate→Execute→Gate→Log) — nhập môn: `Orchestrator Guide`.
> **Ngày:** 2026-08-24 · **Phiên bản:** v2.0

---

## 0. Case study chung — "Dự án LMS"

> Dùng chung cho cả 5 bài. Học viên có thể thay bằng dự án thật của mình; nếu chưa có, dùng case này.

**Bối cảnh:** Công ty 500 nhân viên đang quản lý **đăng ký nghỉ phép** bằng email + Excel → chậm, sai sót, khó duyệt. Ban lãnh đạo muốn làm **Hệ thống Quản lý Nghỉ phép (Leave Management System — LMS)** nội bộ.

**Brief thô từ stakeholder (input gốc — cố tình mơ hồ, thiếu, mâu thuẫn):**
> *"Anh muốn một app cho nhân viên xin nghỉ phép online, sếp duyệt nhanh trên điện thoại. Phải thấy được số ngày phép còn lại. HR cần báo cáo cuối tháng. Càng sớm càng tốt, tầm 2 tháng. À mà phải tích hợp chấm công nữa. Bảo mật thì... chắc như mấy app nội bộ khác thôi. Ngân sách thì làm sao tối ưu nhất."*

**Ràng buộc giả định cho lớp:**
- Team: 1 PM (học viên), 3 dev, 1 QA, 0.5 designer.
- Mốc mong muốn: ~8 tuần. Đây là dự án nội bộ, không safety-critical.

> 💡 *Đây là dữ liệu "đời thực hoá": brief thiếu rõ ràng để học viên thấy AI **không** thay được việc làm rõ intent — đó là việc của PM.*

---

## Khung chung mọi bài tập

Mỗi bài tập gồm: **Mục tiêu năng lực · Thời lượng · Input · Các bước · Sản phẩm nộp · Telemetry bắt buộc · Rubric (0–4) · Prompt mẫu gợi ý.**

**Telemetry bắt buộc cho MỌI bài** (nộp kèm, thiếu = chưa hoàn thành):
| Trường | Ghi gì |
|---|---|
| Tool dùng | tên tool/model |
| Token (est) | tổng token in/out ước tính |
| Thời gian | phút làm bài (gồm review) |
| Số vòng lặp | bao nhiêu lần chỉnh prompt mới ra kết quả dùng được |
| Rework | có phải làm lại artefact không (có/không + lý do) |
| PM-edit | ≥1 điểm PM sửa sai/chỉnh intent của AI (mô tả ngắn) |

> **Đo trung thực (theo RevenueOS):** (1) **Thời gian là giờ làm thật**, KHÔNG suy từ token — token nhiều ≠ làm được nhiều; (2) Token ghi là **ước tính (est)**, cuối buổi đối chiếu lại nếu có số thật (**reconcile**); (3) Ghi cả vòng lặp/việc *phụ* để bức tranh không bị thổi phồng. `PM-edit` mới là cột "đắt" nhất — nó đo **phán đoán của người**, không đo độ "đẹp" của AI.

---

## EX-01 — AI viết & review Requirement *(gắn T1 + T2)*

- **Năng lực:** C1 AI Literacy · C2 Delegation · C6 Outcome.
- **Thời lượng:** 90 phút.

**Input:** Brief thô ở §0.

**Các bước:**
1. **AI sinh draft requirement** từ brief: mục tiêu, scope (in/out), user story, NFR (hiệu năng/bảo mật/khả dụng), acceptance criteria.
2. **AI tự review** chính draft đó: tìm **mâu thuẫn, chỗ thiếu, chỗ mơ hồ** + sinh **danh sách câu hỏi làm rõ** gửi stakeholder.
3. **PM phán xử:** đánh dấu câu hỏi nào *thật sự* cần hỏi, câu nào AI tự suy luận sai. Chỉnh ≥1 điểm AI hiểu sai intent (gợi ý: "tích hợp chấm công" — in hay out scope MVP? "bảo mật như app khác" — PM phải cụ thể hoá).
4. **Phản xạ hard-stop:** chỉ ≥1 chỗ brief **mâu thuẫn/không đủ để quyết** mà PM **KHÔNG để AI tự đoán** — phải dừng lại, ghi là "chờ stakeholder làm rõ" (vd: "càng sớm càng tốt ~2 tháng" **vs** scope có cả tích hợp chấm công + migration). Đây là kỹ năng cốt lõi: AI dừng & hỏi là *tốt*, không phải lỗi.
5. **Simulation: stakeholder đòi thêm scope.**
Dùng AI đóng vai **chủ dự án / khách hàng** với yêu cầu bổ sung hợp lý nhưng ngoài scope MVP. Ví dụ:
   - PB-01: *"Anh muốn có mã giảm giá / coupon trong MVP luôn, bán đợt khai trương cần có."*
   - Case LMS: *"Anh muốn thêm tính năng request làm thêm giờ nữa."*
   PM phải trả lời **bằng văn bản** (không nói miệng):
   - (a) **Ảnh hưởng** tới scope / timeline / team nếu thêm — trích dẫn từ requirement đã làm.
   - (b) **Phương án thay thế** (vd: đợt khai trương dùng tay sửa giá → giữ scope MVP, coupon vào phase 2).
   - (c) **"Email/chat trả lời stakeholder"** — ≤5 dòng, rõ ràng, giữ quan hệ mà vẫn bảo vệ scope.

> 💡 *Kỹ năng "nói KHÔNG có lý do" là cái PM thiếu nhất. AI simulate stakeholder khó tính = đúng tinh thần chương trình (AI làm, người phán xử).*

**Sản phẩm nộp:**
- `REQ-LMS.md`: requirement có cấu trúc (đã qua tay PM).
- Danh sách ≥5 câu hỏi làm rõ, mỗi câu gắn nhãn `[Hỏi stakeholder]` / `[AI tự sai]`.
- ≥1 điểm **hard-stop** đánh dấu `[CHỜ LÀM RÕ — không để AI đoán]`.
- "Email trả lời stakeholder" (≤5 dòng) + lý do phía sau.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Đủ mục requirement, bám brief, ≥5 câu hỏi hợp lệ, PM đã sửa ≥1 điểm sai intent |
| 3 | Phân loại đúng câu hỏi thật vs AI-tự-sai; scope in/out rõ ràng; có ≥1 hard-stop hợp lý; có trả lời stakeholder với phương án thay thế khả thi |
| 4 | Có acceptance criteria đo được + template tái dùng cho dự án khác; email giữ tone phù hợp mà vẫn bảo vệ scope |

**Prompt mẫu gợi ý:**
> *"Bạn là BA. Từ brief sau, hãy viết requirement có cấu trúc: Mục tiêu, Scope (in/out), User Stories (As a… I want… so that…), NFR, Acceptance Criteria. Đánh dấu rõ những chỗ brief chưa đủ thông tin thay vì tự bịa. Brief: [...]"* → sau đó: *"Giờ đóng vai reviewer khó tính: liệt kê mâu thuẫn / thiếu / mơ hồ trong chính draft trên, và đặt câu hỏi làm rõ cho stakeholder."*

---

## EX-02 — AI sinh WBS *(gắn T3)*

- **Năng lực:** C1 · C3 Workflow Design.
- **Thời lượng:** 60 phút.

**Input:** `REQ-LMS.md` từ EX-01.

**Các bước:**
1. AI breakdown scope → **WBS** ≥2 cấp (Epic → Task), kèm **dependency** giữa các task.
2. AI gắn mỗi task với pha SDLC (Design/Code/Test...).
3. PM rà: phát hiện task AI **bỏ sót** (vd: migration dữ liệu phép cũ từ Excel, phân quyền sếp/HR, thông báo) và task **thừa/không phù hợp scope MVP**.

**Sản phẩm nộp:**
- `WBS-LMS.md` (bảng hoặc cây) đã hiệu chỉnh.
- Ghi chú ≥2 task PM thêm/bớt so với bản AI + lý do.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | WBS phủ scope, có dependency hợp lý, PM đã hiệu chỉnh |
| 3 | Phát hiện được task AI bỏ sót quan trọng; gắn đúng pha SDLC |
| 4 | WBS dùng được để estimation/giao việc ngay; cấu trúc tái dùng |

**Prompt mẫu:**
> *"Từ requirement sau, sinh WBS 2 cấp (Epic → Task) cho team 3 dev + 1 QA, dự án nội bộ ~8 tuần. Với mỗi task ghi: pha SDLC, dependency (task phải xong trước). Nêu rõ giả định. Requirement: [...]"*

---

## EX-03 — AI Estimation *(gắn T4)*

- **Năng lực:** C1 · C5 Telemetry & Economics.
- **Thời lượng:** 60 phút.

**Input:** `WBS-LMS.md` từ EX-02.

**Các bước:**
1. AI ước lượng effort mỗi task theo **3-point** (lạc quan / khả dĩ / bi quan) → quy ra **MD** (người-ngày).
2. AI nêu **giả định** đằng sau từng ước lượng + tổng hợp + buffer rủi ro.
3. PM hiệu chỉnh theo thực tế năng lực team (vd dev mới, công nghệ chưa quen) và **đối chiếu với mốc 8 tuần** → kết luận: khả thi / phải cắt scope.
4. **Đối chiếu & trade-off (bắt buộc — kỹ năng PM quan trọng nhất).**
So tổng effort (kịch bản "khả dĩ" + buffer) với mốc thời gian × capacity team.
   - **Nếu vượt** (rất có thể — đề cài sẵn thế): PM **phải quay lại sửa** `REQ-PB0X.md` và `WBS-PB0X.md` — cắt scope, ghi rõ cắt cái gì và vì sao. Nộp thêm `TRADEOFF-PB0X.md` gồm: (a) bảng so sánh "scope đầy đủ vs scope cắt"; (b) **diff** cụ thể giữa REQ v1 → v2 và WBS v1 → v2 (cái gì bỏ, cái gì dời phase 2); (c) 1 đoạn giải trình cho stakeholder vì sao cắt và ảnh hưởng business goal nào.
   - **Nếu vừa đủ hoặc dư**: PM giải thích vì sao vừa (giả định nào khiến số nhỏ?), và chuẩn bị phương án dự phòng nếu giả định sai.

> 💡 *Đây là iteration loop thật: estimate bung → cắt scope → sửa WBS → sửa requirement. PM thực tế làm việc này mọi dự án — bài tập bắt luyện phản xạ trade-off scope–time–resource.*

**Sản phẩm nộp:**
- Bảng estimation (task · 3-point · MD · giả định).
- Kết luận khả thi vs mốc + đề xuất nếu vượt (cắt scope nào).
- `TRADEOFF-PB0X.md` (nếu vượt mốc): scope cắt + diff REQ/WBS v1→v2 + giải trình stakeholder.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Có 3-point + giả định rõ; PM điều chỉnh theo thực tế |
| 3 | So sánh tổng effort với mốc, ra quyết định khả thi/cắt scope; **có diff REQ+WBS v1→v2 khi cắt** |
| 4 | Có phân tích nhạy cảm (đổi giả định → đổi kết quả) + cắt scope mà vẫn giữ business goal cốt lõi; đề xuất phase 2 rõ |

**Prompt mẫu:**
> *"Ước lượng effort cho WBS sau theo 3-point (optimistic/likely/pessimistic) đơn vị người-ngày. Với mỗi task ghi giả định. Tổng hợp + đề xuất buffer. Giả định team: 3 dev (2 trung cấp, 1 mới), 1 QA. WBS: [...]"*

---

## EX-04 — AI sinh Risk List *(gắn T5 — bắt buộc tốt nghiệp Phase 2)*

- **Năng lực:** C3 · C4 Governance & Risk.
- **Thời lượng:** 60 phút.

**Input:** `REQ-LMS.md` + `WBS-LMS.md` + `Estimation`.

**Các bước:**
1. AI sinh **risk register** ≥10 rủi ro: mô tả · **Likelihood (1–5)** · **Impact (1–5)** · điểm = L×I · **mitigation** · owner.
2. Yêu cầu AI phủ nhiều nhóm: kỹ thuật (tích hợp chấm công), tiến độ (mốc 8 tuần sát), dữ liệu (migration Excel), **rủi ro liên quan AI** (hallucination khi AI sinh code/tài liệu, lộ dữ liệu nhân sự vào prompt).
3. PM xếp ưu tiên top-5, kiểm tra mitigation **khả thi** không (loại các mitigation chung chung/sáo rỗng).
4. **Gắn mức kiểm soát cho rủi ro-AI:** với mỗi rủi ro khi *dùng AI* (vd lộ dữ liệu nhân sự, AI sinh code sai), ghi rõ **mức ủy quyền AI được phép** (L0–L5) + **cổng fail-closed** nào chặn (vd: "AI sinh code → phải qua review người trước khi merge; dữ liệu nhân sự → AI không được đưa vào prompt"). Tức mitigation = *cơ chế kiểm được*, không phải lời hứa.

**Sản phẩm nộp:**
- `RISK-LMS.md`: bảng ≥10 rủi ro đã xếp hạng + top-5 ưu tiên.
- Cột "mức ủy quyền + cổng chặn" cho các rủi ro-AI.
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | ≥10 rủi ro có L×I + mitigation khả thi |
| 3 | Phủ đủ nhóm gồm **rủi ro AI**; loại được mitigation sáo rỗng; rủi ro-AI có mức ủy quyền + cổng chặn |
| 4 | Mitigation gắn owner + trigger theo dõi; dùng làm risk review thật |

**Prompt mẫu:**
> *"Sinh risk register cho dự án LMS (nội bộ, 8 tuần, có tích hợp chấm công + migration dữ liệu từ Excel, team dùng AI để sinh code/tài liệu). ≥10 rủi ro, mỗi cái: mô tả, Likelihood 1–5, Impact 1–5, điểm L×I, mitigation cụ thể, owner. Bắt buộc có nhóm rủi ro khi DÙNG AI trong delivery."*

---

## EX-05 — AI Weekly Report + Mini Dashboard *(gắn T7 + T10 — T10 bắt buộc tốt nghiệp)*

- **Năng lực:** C5 Telemetry & Economics · C6 Outcome.
- **Thời lượng:** 90 phút.

**Input (dữ liệu giả lập 1 tuần chạy dự án — phát kèm):**
> Tuần 3/8. Kế hoạch tuần: xong module chính #1 + module chính #2 (tuỳ đề — vd PB-01: "Danh mục sản phẩm" + "Giỏ hàng"; case LMS: "Xin phép" + "Duyệt"). Thực tế: module #1 done. Module #2 trễ 1 ngày do vướng logic nghiệp vụ phức tạp hơn dự kiến. 3 bug mở (2 UI, 1 logic). AI hỗ trợ sinh code CRUD (tiết kiệm ~1.5 MD). Token tuần ~120k. 1 rủi ro mới: tích hợp bên thứ 3 chưa có tài liệu API tốt.
> ⚠️ **Dữ liệu CHỈ gồm các thông tin trên.** Không có: doanh thu, conversion rate, số đơn, tốc độ tải trang, hay bất kỳ con số nào khác. Nếu report/dashboard xuất hiện số ngoài danh sách này → đó là AI bịa.

**Các bước:**
1. AI sinh **Weekly Report**: tiến độ (kế hoạch vs thực tế), điểm nghẽn, rủi ro, **next week**, có nêu **đóng góp của AI**.
2. AI đề xuất **mini dashboard** ≥5 KPI lấy từ Telemetry Framework (§10 chương trình): vd AI Adoption, Review Time, Rework Rate, Token Cost, Schedule Variance — mỗi KPI ghi **công thức + nguồn dữ liệu**.
3. PM kiểm chứng số liệu đúng nguồn (AI không được bịa số) + viết 1 câu **quyết định** rút ra từ dashboard.
4. **Bắt AI bịa số — luyện phản xạ chống hallucination (bắt buộc).**
Sau khi AI sinh weekly report + dashboard, PM rà từng con số: **có số nào KHÔNG có trong dữ liệu input?**
   - AI rất hay bịa: "conversion rate 3.2%", "doanh thu tuần đạt 15M", "tốc độ tải trang 1.8s" — những con số **không ai cho**.
   - Đánh dấu từng số bịa: *"Số X ở đoạn Y — không có trong input, AI tự sinh."*
   - Nộp **≥1 phát hiện hallucination thật** + cách sửa (thay bằng "chưa có dữ liệu" hoặc "N/A" — không bịa số khác thay thế).

> 💡 *Kỹ năng sống còn: khi PM dùng AI viết báo cáo cho lãnh đạo, 1 con số bịa → quyết định sai. Phản xạ đúng: "số này lấy từ đâu?" — không có nguồn thì xoá, không thay bằng số khác.*

**Sản phẩm nộp:**
- `WEEKLY-W3.md` (report ≤1 trang).
- `DASHBOARD-LMS.md`: ≥5 KPI có công thức + nguồn.
- 1 quyết định PM dựa trên số liệu.
- ≥1 phát hiện hallucination (số AI bịa + cách sửa).
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | Report đúng số liệu nguồn; dashboard ≥5 KPI có công thức + nguồn |
| 3 | Số liệu không bịa; có quyết định rút ra từ dashboard; bắt được ≥1 số AI bịa + sửa đúng cách ("N/A" thay vì bịa) |
| 4 | Dashboard vận hành lại được tuần sau; KPI gắn target + cảnh báo; PM gắn quy tắc dashboard: KPI chưa có nguồn dữ liệu → hiển thị N/A |

**Prompt mẫu:**
> *"Từ dữ liệu tuần sau, viết weekly report ≤1 trang: tiến độ (plan vs actual), nghẽn, rủi ro, kế hoạch tuần tới, đóng góp của AI. KHÔNG bịa số ngoài dữ liệu cho. Sau đó đề xuất 5 KPI dashboard, mỗi KPI ghi công thức + nguồn dữ liệu. Dữ liệu: [...]"*

---

## EX-06 — Delegation Map + Autonomy Leash *(gắn Lab M5 — module quan trọng nhất)*

- **Năng lực:** C2 AI Delegation · C4 Governance.
- **Thời lượng:** 75 phút.

**Input:** `WBS-LMS.md` (EX-02) + `RISK-LMS.md` (EX-04).

**Các bước:**
1. Lấy **≥15 task** từ WBS. Với mỗi task, điền 3 cột quyết định:
   - **Nhóm 5-loại:** AI-do / Human-do / AI-review / Human-review / AI-không-nên.
   - **Mức ủy quyền L0–L5:** Observe / Draft / Recommend / Execute-bounded / Operate-workflow / Restricted.
   - **Ai gỡ chốt (duyệt):** AI tự đóng / PM spot-check / PM đích thân duyệt.
2. **Áp "dây cương" A vs A+** *(nhắc: Leash chỉ là 2 nấc vận hành của thang L0–L5 — **A ≈ L3, A+ ≈ L4** — không phải khung khác)*: đánh dấu task nào chạy ở **A** (vùng an toàn, AI tới bản nháp, không tự release) và task nào phải **A+** (chạm dữ liệu nhân sự / phân quyền / tích hợp chấm công → bắt buộc người duyệt trước khi dùng). Mọi task **A+ → BUILT-flagged chờ duyệt**.
3. **PM giải trình:** 1 dòng lý do cho mỗi task ở mức ≥ L3, và chỉ ra ≥1 task **cố tình giữ ở L1/L2** dù AI "làm được" (vì rủi ro/khó kiểm).

**Sản phẩm nộp:**
- `DELEGATION-MAP-LMS.md`: bảng ≥15 task × (nhóm 5-loại · mức L0–L5 · ai duyệt · leash A/A+ · lý do).
- Telemetry.

**Rubric (0–4):**
| Điểm | Mô tả |
|---|---|
| 2 (Đạt) | ≥15 task có đủ nhóm + mức L0–L5 + ai duyệt; lý do hợp lý |
| 3 | Phân biệt đúng A vs A+; task chạm dữ liệu/quyền đều **A+ chờ duyệt**; có task cố ý giữ thấp dù AI làm được |
| 4 | Map dùng vận hành thật được; gắn cổng fail-closed cho từng nhóm hazard; tái dùng cho dự án khác |

**Prompt mẫu:**
> *"Với danh sách task sau của dự án LMS, đề xuất cho mỗi task: (a) nên giao AI / giữ người / AI-review / human-review / AI-không-nên; (b) mức ủy quyền L0–L5; (c) ai nên duyệt. Đánh dấu task nào chạm dữ liệu nhân sự hoặc phân quyền (cần kiểm soát chặt). KHÔNG tự ý nâng mức ủy quyền cho task rủi ro cao. Task: [...]"* → PM tự phán xử lại, không bê nguyên gợi ý AI.

---

## Bảng ánh xạ bài tập ↔ assignment ↔ năng lực

| Bài | Assignment gốc | Tuần | Năng lực chính | Bắt buộc tốt nghiệp |
|---|---|---|---|---|
| EX-01 | T1 + T2 | W1 | C1, C2, C6 | — |
| EX-02 | T3 | W2 | C1, C3 | — |
| EX-03 | T4 | W2 | C1, C5 | — |
| EX-04 | T5 | W2 | C3, C4 | ✅ (T5) |
| EX-05 | T7 + T10 | W4 | C5, C6 | ✅ (T10) |
| EX-06 | Lab M5 | W3 | C2, C4 | — *(khuyến nghị mạnh)* |

> 6 bài này phủ **6/10 assignment + Lab M5** và đủ "xương sống" SDLC. Các task còn lại (T6 Test Strategy, T8 Meeting Summary, T9 Retrospective) làm trực tiếp trên dự án thật ở Phase 3, hoặc soạn thêm bài common theo cùng template này.

---

## Hướng dẫn giảng viên (facilitator notes)

- **Chấm cái gì:** không chấm "AI trả lời hay" — chấm **phán xử của PM** (chỗ PM sửa sai AI, quyết định rút ra). Cột `PM-edit` trong telemetry là bằng chứng quan trọng nhất.
- **Bẫy cố ý trong case:** brief mơ hồ (EX-01), task dễ sót như migration/phân quyền (EX-02), mốc 8 tuần sát (EX-03), rủi ro-AI hay bị quên (EX-04), cám dỗ để AI bịa số (EX-05). Hỏi học viên có "bắt" được không.
- **Tiêu chí trượt — cảnh giác "rubber-stamping":** nộp output AI mà **không có dấu vết review của người** (ký bừa diff AI) → tối đa 1 điểm, dù nội dung "đẹp". Đây là **rủi ro mới nguy hơn cả thiếu người** — cả khoá phải chấm để diệt thói quen này từ gốc.
- **Showcase:** mỗi tuần 2–3 học viên trình bài + telemetry; lớp phản biện "chỗ nào PM nên không tin AI".
- **Biến tấu cho dự án thật:** học viên thay case LMS bằng dự án của mình, giữ nguyên các bước + rubric.
- **Bộ đề giao sẵn:** thay vì 300 PM làm chung case LMS, dùng **6 đề bài cụ thể (requirement chi tiết + tech stack rõ)** ở `Project Briefs` — chia nhóm theo đề (PB-01→PB-06), PM đổi tiền tố file theo mã đề (`REQ-PB01.md`…). Nhóm mới → PB-03 (dễ nhất); nhóm core → PB-06 (sát chủ đề AI).

---

*Workbook này là **track PM** trong bộ Workbook nhiều-nghề dùng chung Common Core (Program §14). Track khác: BA (`…-Workbook-BA-…`), SA (`…-Workbook-SA-…`), Dev (`…-Workbook-Dev-…`). PM thuộc lĩnh vực có chuẩn chuyên ngành sẽ có bài tập chuyên sâu riêng theo nhóm (ngoài phạm vi training common).*

> **Thuật ngữ:** tra cứu tại `docs/GLOSSARY.md` — bảng thuật ngữ thống nhất có cột mapping sang ngành.

---

## Phụ lục — Changelog
| Version | Ngày | Nội dung |
|---|---|---|
| v1.0 | 2026-06-29 | 5 bài tập common chi tiết (EX-01→EX-05) trên 1 case study chung + hướng dẫn giảng viên. |
| v1.1 | 2026-06-30 | Nạp cách làm RevenueOS: thêm **EX-06 Delegation Map (L0–L5 + Leash A/A+)** cho M5; telemetry thêm nguyên tắc *giờ thật không proxy token + est→reconcile*; EX-01 thêm phản xạ **hard-stop khi mâu thuẫn**; EX-04 gắn **mức ủy quyền + cổng fail-closed** vào mitigation; facilitator gọi tên rủi ro **rubber-stamping**. |
| v1.1.1 | 2026-06-30 | EX-06 bước 2: chú thích rõ **Leash A/A+ = 2 nấc của thang L0–L5 (A≈L3, A+≈L4)**, không phải khung khác — đồng bộ với Program v1.2.2. |
| v2.0 | 2026-08-24 | **Cải tiến bài tập:** EX-01 thêm bước 5 (simulation stakeholder đòi thêm scope); EX-03 thêm bước 4 (đối chiếu & trade-off bắt buộc quay lại sửa scope); EX-05 sửa dữ liệu input (cố tình thiếu để luyện hallucination) + thêm bước 4 (bắt AI bịa số). Dời changelog xuống cuối. Glossary trỏ về `docs/GLOSSARY.md`. |
