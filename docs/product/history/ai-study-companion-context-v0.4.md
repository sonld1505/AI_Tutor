# AI Study Companion — Project Context

> **Đã được thay thế** bởi [Business HLD v1.3](../business-hld-v1.3.md), [Technical HLD v1.3](../technical-hld-v1.3.md) và [context v0.5](../ai-study-companion-context-v0.5.md) ngày 08/10/2026. Giữ lại để tra lịch sử; không dùng làm yêu cầu.

**Phiên bản:** 0.4 • **Ngày:** 07/10/2026 • **Chủ dự án:** Sơn • **Thay thế:** v0.3 (06/10/2026)

## 0. Vai trò và nguồn chuẩn

Bản tóm tắt cho coding agent và người mới vào team. Nguồn chi tiết:

- [Business HLD v1.2](business-hld-v1.2.md): quyết định D01–D25, use case U01–U24, KPI, kinh doanh, cổng và go/no-go (§11 là nguồn chuẩn).
- [Technical HLD v1.2](technical-hld-v1.2.md): kiến trúc, API, state machine, acceptance A01–A42.

Mâu thuẫn giữa context và HLD v1.2 thì **HLD v1.2 thắng**; dừng lại và báo Sơn.

**Thay đổi so với v0.3:**

| # | v0.3 | v0.4 |
| --- | --- | --- |
| 1 | Lớp 6–7 | **Chỉ Toán lớp 6** |
| 2 | Buổi học tự do | **Buổi học theo tờ đề in**: chụp đề đầu buổi, xác nhận câu/ý bằng giọng nói |
| 3 | Gợi ý theo history | Gợi ý **trong phạm vi kiến thức đã học** (có version, do giáo viên hoặc phụ huynh xác nhận) |
| 4 | — | Trẻ chọn câu bất kỳ ("câu 3"); buổi 30–45 phút; lưu tiến độ và học tiếp |
| 5 | Câu khó có thể bỏ qua trong thống kê | Câu chưa hỗ trợ/ngoài phạm vi **vẫn trong tổng số câu** |
| 6 | Scenario SC-01–SC-24 | **Bỏ SC**; dùng trực tiếp acceptance A01–A42 |
| 7 | U01–U17, A01–A31 | U01–U24, A01–A42 (bảng đối chiếu: Business HLD §0.3) |

Giữ nguyên: ảnh vùng giấy lên server; giọng nói "Cô ơi"; không chạm máy; thẻ lệnh; ảnh gần trực tiếp; phiếu bài hệ thống; miễn phí trong pilot; không bán dữ liệu; ảnh xóa sau 7 ngày; 10 tuần; Android và iOS.

Chưa có repo hay code.

## 1. Bài toán và định vị

**Job-to-be-done:** con tự làm đề ôn Toán lớp 6 trên giấy mỗi tối, gọi cô khi cần; bố mẹ biết con làm được bao nhiêu và hổng chỗ nào.

**Bốn trụ khác biệt:** rảnh tay; chấm cách làm, không chỉ đáp án; đúng phần đã học; vòng lặp báo cáo → phiếu luyện.

**Chiến lược:** miễn phí trong pilot, đặt cọc cuối pilot, sau đó freemium. Không bán dữ liệu, không quảng cáo tới trẻ.

## 2. Nguyên tắc

1. AI im lặng khi chưa được gọi.
2. Không bắt trẻ chạm máy trong buổi học, kể cả bước chụp đề.
3. UNKNOWN ≠ WRONG; không rõ thì hỏi lại bằng giọng nói.
4. Gợi ý nhỏ nhất; không tự đưa lời giải đầy đủ.
5. Gợi ý chỉ dùng kiến thức/phương pháp trong phạm vi đã học. Đã học ≠ đã thành thạo.
6. Ngôn ngữ SGK lớp 6.
7. Chỉ nói về bài học.
8. Đáp án đúng không chứng minh cách làm đúng.
9. Câu khó, ngoài phạm vi, chưa hỗ trợ vẫn nằm trong tờ đề.
10. Không ép làm thêm hay đọc đáp án để "hoàn thành".
11. Frame có người không rời máy.
12. Báo cáo chỉ nói điều có bằng chứng.

## 3. Phạm vi MVP

- **Toán lớp 6**, 2–3 dạng bài (ứng viên: tìm số hạng/thừa số chưa biết; thứ tự thực hiện phép tính; phân số cơ bản), một bộ SGK.
- Tờ đề: đề in của giáo viên/phụ huynh, hoặc phiếu hệ thống sinh theo lỗ hổng.
- App học sinh Android và iOS; web phụ huynh/giáo viên (phạm vi đã học, báo cáo, phiếu, ảnh gần trực tiếp, đồng ý, dữ liệu).

**Ngoài MVP:** lớp 7 trở lên, môn khác, hình học, câu có hình/bảng (giữ "chưa hỗ trợ"), live video, nhận dạng trên máy, giao diện giáo viên cho cả lớp, gamification.

## 4. Buổi học rảnh tay

**Trước buổi học (được chạm):** mở app, cắm sạc, bật Không làm phiền, đặt máy lên giá.

| Bước | Cách làm |
| --- | --- |
| Bắt đầu | App thấy bàn sẵn sàng → chào; có đề dở thì hỏi học tiếp |
| Chụp đề | Đặt từng trang; app tự chụp khi ổn định; "Hết rồi ạ" hoặc thẻ XONG |
| Xác nhận đề | "Cô thấy 5 câu, 8 ý. Đúng không con?" → "Đúng rồi ạ" / "Thiếu câu 4" |
| Báo trước | Câu chưa hỗ trợ hoặc cần xem lại phạm vi được nói trước, vẫn giữ trong đề |
| Chọn câu | "Câu 3", "Câu 2 ý b", hoặc khoanh số câu |
| Kiểm tra | "Cô ơi, kiểm tra giúp con" / thẻ KIỂM TRA |
| Trợ giúp | "Cô ơi, con không biết làm" / thẻ GIÚP CON |
| Chữ không rõ | Cô hỏi câu đóng; con trả lời |
| Tay che, giấy lệch | Nhắc bỏ tay / xê dịch giấy; không chỉnh máy |
| Dừng cô / nghe lại | "Cô ơi, dừng" / "Cô nhắc lại" |
| Chấm phiếu hệ thống | "Cô chấm giúp con" |
| Kết thúc | "Con học xong rồi" / thẻ XONG; hết 30–45 phút cô đề nghị lưu; luôn lưu tiến độ |

## 5. Kiến trúc tóm tắt

```
Điện thoại: camera → 4 góc trang, bù lệch → chất lượng, che tay → chặn người → cắt trang
            micro → "Cô ơi" trên máy → đoạn lệnh / câu trả lời xác nhận
            thẻ lệnh → marker trên máy
               │ (chỉ khi có trigger: trang đề, Kiểm tra, Trợ giúp, phiếu, phụ huynh xem)
               ▼
Server:     ASR + intent → RecognitionEngine (vision qua adapter)
            ├─ chụp đề: ProblemSetBuilder → xác nhận → ScopeGate → READY
            └─ attempt: evidence gate → MathValidator (SymPy) → history + policy
                        → KnowledgeRetriever (lọc theo learned scope) → tutor LLM
                        → output filter (mức gợi ý, lộ đáp án, ngoài phạm vi) → TTS
            PostgreSQL (bộ đề, item, run, tiến độ, scope, knowledge store) · S3 ảnh TTL 7 ngày
               ▼
Web phụ huynh/giáo viên: phạm vi đã học, báo cáo theo tờ đề, phiếu PDF, ảnh gần trực tiếp
```

Chi tiết: Technical HLD v1.2 §4–§8, state machine §15.

## 6. Phản hồi

| Tình huống | AI làm gì |
| --- | --- |
| Đang làm, chưa gọi | Im lặng; không gửi gì lên server |
| Ngừng viết ~60 giây | Hỏi một lần tại máy |
| Kiểm tra, đúng | Xác nhận ngắn |
| Kiểm tra, sai | Chỉ dòng sai gốc; L1; không đọc đáp án |
| Trợ giúp | Gợi ý theo history, trong phạm vi đã học; L1 → L2; L3 khi trẻ hỏi thêm |
| Cần kiến thức chưa học | Không gợi ý vượt phạm vi; "cần xem lại phạm vi" |
| Hỏi thẳng đáp án | Mời làm một bước |
| Chữ/ảnh không rõ | Hỏi lại; không phán sai |
| Ngoài lề | Đưa về bài |

Ví dụ lớp 6: "Con xem lại dòng thứ hai nhé. Muốn tìm số hạng chưa biết thì con làm phép tính gì?"

## 7. Tiến độ và báo cáo

- Trạng thái item: chưa làm · đang làm · trẻ báo xong · cần sửa · chưa xác nhận · đã xác nhận; cờ cần xem lại phạm vi, chưa hỗ trợ.
- Đã xác nhận chia ba nhóm: đúng lần đầu / đúng sau kiểm tra / đúng sau trợ giúp. Nhóm 4: chưa xong hoặc chưa xác nhận.
- **North Star:** tỷ lệ câu/ý đúng ở lần kiểm tra đầu trên tổng câu/ý của các đề đã làm.
- Báo cáo theo tờ đề; tách "trẻ báo xong" khỏi "đã xác nhận"; "cần luyện" khi lỗi lặp ≥ 3 câu qua ≥ 2 buổi.

## 8. Dữ liệu

- Ảnh chỉ gửi khi có trigger; frame có người bị chặn; chỉ vùng giấy đã cắt; ảnh xóa sau 7 ngày. Text đề, tiến độ, kết quả lưu trong DB để học tiếp.
- Âm thanh chỉ gửi sau "Cô ơi" hoặc khi trả lời câu hỏi xác nhận.
- Hai loại đồng ý; phụ huynh xem/xuất/xóa dữ liệu; nhà cung cấp AI không huấn luyện trên dữ liệu.

## 9. Acceptance ưu tiên cho vertical slice

A01, A02, A05, A06, A11, A14, A18, A19, A20, A22, A23, A24, A31, A36, A40, A42. Danh sách đầy đủ: Technical HLD v1.2 §15.1.

## 10. Pilot 10 tuần

| Tuần | Việc chính | Cổng |
| --- | --- | --- |
| 1 | Spike vision (bài làm + 20–30 đề in lớp 6), "Cô ơi" trên Android và iPhone, mục lục kỹ năng lớp 6, pháp lý, giáo viên | S |
| 2–5 | Vertical slice đầy đủ trên hai nền tảng; harness replay; phát hành nội bộ | G0 |
| 6 | Alpha 5 gia đình (cả Android và iOS) | G1 |
| 7–10 | Pilot 15 → 50 gia đình; phiếu bài; phỏng vấn; đặt cọc | G2; go/no-go cuối tuần 10 |

Ngưỡng: Business HLD v1.2 §11. Nguồn lực: 3 kỹ sư, 1 giáo viên Toán lớp 6 bán thời gian, Sơn.

## 11. Quyết định

**Đã chốt:** Toán lớp 6; buổi học theo tờ đề, chụp đề đầu buổi; phạm vi đã học có version; chọn câu bất kỳ; 30–45 phút và học tiếp; giọng nói "Cô ơi"; không chạm máy; ảnh vùng giấy lên server; phiếu bài hệ thống; ảnh gần trực tiếp; miễn phí trong pilot; không bán dữ liệu; ảnh xóa sau 7 ngày; 10 tuần; Android và iOS.

**Chờ chốt:** D25 ai xác nhận phạm vi đã học (đề xuất: giáo viên nếu có, nếu không phụ huynh tick mục lục SGK); 2–3 dạng bài và bộ SGK; giới hạn số trang/câu mỗi đề; danh sách máy hỗ trợ; nhà cung cấp model; nội dung đồng ý; mức đặt cọc; ngân sách.

## 12. Hướng dẫn cho AI coding agent

- Đọc context này, rồi cả hai HLD v1.2; đọc repo và test trước khi làm.
- Thứ tự: spike vision (đề + bài làm) và "Cô ơi" → harness replay → luồng chụp đề + xác nhận + scope gate → attempt (validator, policy, retrieval theo scope, output filter, TTS) → tiến độ/học tiếp → báo cáo, web, phiếu bài.
- Không mở READY khi bộ đề hoặc scope chưa xác nhận; không mặc định scope = toàn lớp 6.
- Mọi luồng trong buổi học có đường không chạm, có test tự động.
- Server từ chối ảnh khi `person_check != PASSED` hoặc chưa có đồng ý.
- Code tất định chấm đúng/sai; LLM chỉ viết lời; output filter chặn lộ đáp án, ngoài lề, ngoài phạm vi.
- Mọi model qua adapter; ghi `model_version`, `prompt_version`, `policy_version`, `learned_scope_version`.
- Không triển khai: camera chạy ngầm, ASR luôn bật, chặn cứng sau ba lần trợ giúp, chấm điểm tập trung, lời giải tự động, gợi ý ngoài phạm vi.
- Bàn giao: code đã đổi, test đã chạy, benchmark đã đo, blocker, bước tiếp theo.

**Nguyên tắc xuyên suốt:** Con tự làm đề, gọi cô khi cần, cô chỉ dạy những gì con đã học, và con không phải chạm vào máy.
