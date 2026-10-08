# AI Study Companion — Project Context

**Phiên bản:** 0.5 • **Ngày:** 08/10/2026 • **Chủ dự án:** Sơn • **Thay thế:** v0.4 (07/10/2026, `history/ai-study-companion-context-v0.4.md`)

## 0. Vai trò và nguồn chuẩn

Bản tóm tắt cho coding agent và người mới vào team. Nguồn chi tiết:

- [Business HLD v1.3](business-hld-v1.3.md): quyết định D01–D31, use case U01–U25, KPI, kinh doanh, cổng và go/no-go (§11 là nguồn chuẩn).
- [Technical HLD v1.3](technical-hld-v1.3.md): kiến trúc, API, state machine, acceptance A01–A46.

Mâu thuẫn giữa context và HLD v1.3 thì **HLD v1.3 thắng**; dừng lại và báo Sơn.

**Thay đổi so với v0.4:**

| # | v0.4 | v0.5 |
| --- | --- | --- |
| 1 | Toán lớp 6, 2–3 dạng bài, bộ SGK chưa chọn | **Toán lớp 6 HK1, SGK Cánh diều**: chấm số học và đại số; câu hình học giữ "chưa hỗ trợ", chấm hình học sau pilot |
| 2 | Đề nhiều trang | **Tối đa 1 trang đề** |
| 3 | Chọn câu bằng "Câu 3" | **Trẻ làm trong vở, ghi số câu ở lề trái** (`1) 5x + 3 = 28`); hệ thống đọc số câu; "Câu 3" là dự phòng |
| 4 | Nhà cung cấp chưa chọn | **Anthropic** chỉ nhận dạng ảnh, ảnh đã **ẩn danh hóa**; ASR **Viettel AI**; TTS **Azure Neural**, giọng nữ |
| 5 | D25 chờ chốt | **Shadow teacher** xác nhận phạm vi và rà, gán nhãn mọi phản hồi AI |
| 6 | Chưa có lịch | Kickoff **08/10/2026**; S 14/10; G0 11/11; G1 18/11; G2 ≈ 22/11; go/no-go 16/12 |
| 7 | — | Android 15+, iOS 18.7+; Python/FastAPI, React + TypeScript, Flutter + native; không giới hạn giờ dùng |

Giữ nguyên: ảnh vùng giấy lên server; giọng nói "Cô ơi"; không chạm máy; thẻ lệnh; ảnh gần trực tiếp; phiếu bài hệ thống; miễn phí trong pilot; không bán dữ liệu; ảnh xóa sau 7 ngày; 10 tuần.

Chưa có code sản phẩm.

## 1. Bài toán và định vị

**Job-to-be-done:** con tự làm đề ôn Toán lớp 6 trên giấy, gọi cô khi cần; bố mẹ biết con làm được bao nhiêu và hổng chỗ nào.

**Bốn trụ khác biệt:** rảnh tay; chấm cách làm, không chỉ đáp án; đúng phần đã học; vòng lặp báo cáo → phiếu luyện.

**Chiến lược:** miễn phí trong pilot, đặt cọc cuối pilot, sau đó freemium. Không bán dữ liệu, không quảng cáo tới trẻ.

## 2. Nguyên tắc

1. AI im lặng khi chưa được gọi.
2. Không bắt trẻ chạm máy trong buổi học, kể cả bước chụp đề.
3. UNKNOWN ≠ WRONG; không rõ thì hỏi lại bằng giọng nói.
4. Gợi ý nhỏ nhất; không tự đưa lời giải đầy đủ.
5. Gợi ý chỉ dùng kiến thức/phương pháp trong phạm vi đã học. Đã học ≠ đã thành thạo.
6. Ngôn ngữ SGK lớp 6 (Cánh diều).
7. Chỉ nói về bài học.
8. Đáp án đúng không chứng minh cách làm đúng.
9. Câu khó, ngoài phạm vi, chưa hỗ trợ (gồm câu hình học) vẫn nằm trong tờ đề.
10. Không ép làm thêm hay đọc đáp án để "hoàn thành".
11. Frame có người không rời máy; ảnh gửi nhà cung cấp không mang dữ liệu định danh.
12. Báo cáo chỉ nói điều có bằng chứng.

## 3. Phạm vi MVP

- **Toán lớp 6 học kỳ 1, SGK Cánh diều.** Chấm phần số học và đại số; support matrix chi tiết do shadow teacher lập trong tuần 1. Câu hình học: "chưa hỗ trợ".
- Tờ đề **1 trang**: đề in của giáo viên/phụ huynh, hoặc phiếu hệ thống sinh theo lỗ hổng.
- Trẻ làm bài **trong vở**, ghi số câu ở lề trái trước mỗi câu.
- App học sinh Android 15+ và iOS 18.7+; web phụ huynh/giáo viên (báo cáo, phiếu, ảnh gần trực tiếp, đồng ý, dữ liệu) và màn hình của shadow teacher (phạm vi đã học, rà soát).

**Ngoài MVP:** lớp 7 trở lên, học kỳ 2, môn khác, chấm hình học (sau pilot), đề nhiều trang, câu có hình/bảng cần đọc, live video, nhận dạng trên máy, giao diện giáo viên cho cả lớp, gamification.

## 4. Buổi học rảnh tay

**Trước buổi học (được chạm):** mở app, cắm sạc, bật Không làm phiền, đặt máy lên giá. Dùng được bất kỳ lúc nào.

| Bước | Cách làm |
| --- | --- |
| Bắt đầu | App thấy bàn sẵn sàng → chào; có đề dở thì hỏi học tiếp |
| Chụp đề | Đặt trang đề; app tự chụp khi ổn định; trang thứ hai không được nhận |
| Xác nhận đề | "Cô thấy 10 câu. Đúng không con?" → "Đúng rồi ạ" / "Thiếu câu 4" |
| Báo trước | Câu chưa hỗ trợ (hình học) hoặc cần xem lại phạm vi được nói trước, vẫn giữ trong đề |
| Làm bài | Mở vở, ghi `3)` ở lề trái rồi làm; có thể nói "Câu 3" |
| Kiểm tra | "Cô ơi, kiểm tra giúp con" / thẻ KIỂM TRA |
| Trợ giúp | "Cô ơi, con không biết làm" / thẻ GIÚP CON |
| Số câu không rõ | Cô hỏi "Con đang làm câu mấy?" |
| Chữ không rõ | Cô hỏi câu đóng; con trả lời |
| Tay che, giấy lệch | Nhắc bỏ tay / xê dịch giấy; không chỉnh máy |
| Dừng cô / nghe lại | "Cô ơi, dừng" / "Cô nhắc lại" |
| Chấm phiếu hệ thống | "Cô chấm giúp con" |
| Kết thúc | "Con học xong rồi" / thẻ XONG; hết 30–45 phút cô đề nghị lưu; luôn lưu tiến độ |

## 5. Kiến trúc tóm tắt

```
Điện thoại: camera → 4 góc trang, bù lệch → chất lượng, che tay → chặn người → cắt trang (gồm lề số câu)
            micro → "Cô ơi" trên máy → đoạn lệnh / câu trả lời xác nhận
            thẻ lệnh → marker trên máy
               │ (chỉ khi có trigger: trang đề, Kiểm tra, Trợ giúp, phiếu, phụ huynh xem)
               ▼
Server (Python/FastAPI):
            ASR Viettel AI + intent
            ẩn danh hóa ảnh → RecognitionEngine (Claude, Anthropic)
            ├─ chụp đề: ProblemSetBuilder → xác nhận → ScopeGate → READY
            └─ attempt: ItemResolver (số câu trong vở / lệnh) → evidence gate
                        → ValidatorRegistry (số học/đại số; hình học sau pilot)
                        → history + policy → KnowledgeRetriever (lọc theo learned scope)
                        → template gợi ý → output filter → TTS Azure Neural
                        → hàng rà soát shadow teacher
            PostgreSQL (bộ đề, item, run, tiến độ, scope, knowledge store, nhãn rà soát) · S3 ảnh TTL 7 ngày
               ▼
Web (React + TypeScript): phụ huynh (báo cáo, phiếu PDF, ảnh gần trực tiếp, dữ liệu) · shadow teacher (phạm vi, rà soát)
```

Chi tiết: Technical HLD v1.3 §4–§8, state machine §15.

## 6. Phản hồi

| Tình huống | AI làm gì |
| --- | --- |
| Đang làm, chưa gọi | Im lặng; không gửi gì lên server |
| Ngừng viết ~60 giây | Hỏi một lần tại máy |
| Kiểm tra, đúng | Xác nhận ngắn |
| Kiểm tra, sai | Chỉ dòng sai gốc; L1; không đọc đáp án |
| Trợ giúp | Gợi ý theo history, trong phạm vi đã học; L1 → L2; L3 khi trẻ hỏi thêm |
| Cần kiến thức chưa học | Không gợi ý vượt phạm vi; "cần xem lại phạm vi" |
| Câu hình học | "Cô chưa chấm được câu này"; vẫn tính trong đề |
| Hỏi thẳng đáp án | Mời làm một bước |
| Chữ/ảnh/số câu không rõ | Hỏi lại; không phán sai |
| Ngoài lề | Đưa về bài |

Ví dụ lớp 6: "Con xem lại dòng thứ hai nhé. Muốn tìm số hạng chưa biết thì con làm phép tính gì?"

Lời gợi ý chỉ lấy từ template đã duyệt; không có template phù hợp thì cô báo "cần xem lại" và shadow teacher bổ sung template (D31). MVP không dùng LLM sinh lời; Anthropic chỉ dùng cho ảnh.

## 7. Tiến độ, báo cáo và rà soát

- Trạng thái item: chưa làm · đang làm · trẻ báo xong · cần sửa · chưa xác nhận · đã xác nhận; cờ cần xem lại phạm vi, chưa hỗ trợ.
- Đã xác nhận chia ba nhóm: đúng lần đầu / đúng sau kiểm tra / đúng sau trợ giúp. Nhóm 4: chưa xong hoặc chưa xác nhận.
- **North Star:** tỷ lệ câu/ý đúng ở lần kiểm tra đầu trên tổng câu/ý của các đề đã làm.
- Báo cáo theo tờ đề; tách "trẻ báo xong" khỏi "đã xác nhận"; "cần luyện" khi lỗi lặp ≥ 3 câu qua ≥ 2 buổi.
- Shadow teacher rà mọi phản hồi AI trong pilot qua lịch sử học tập; nhãn là nguồn KPI chất lượng; nhãn "ngoài phạm vi" hoặc "có dữ liệu định danh" là sự cố An toàn.

## 8. Dữ liệu

- Ảnh chỉ gửi khi có trigger; frame có người bị chặn; chỉ vùng giấy đã cắt; ảnh xóa sau 7 ngày. Text đề, tiến độ, kết quả lưu trong DB để học tiếp.
- Trước khi gửi Anthropic: bỏ metadata ảnh, che dải đầu trang, không gửi mã người dùng/học sinh/phiên.
- Âm thanh chỉ gửi (tới Viettel AI) sau "Cô ơi" hoặc khi trả lời câu hỏi xác nhận.
- Hai loại đồng ý; phụ huynh xem/xuất/xóa dữ liệu; nhà cung cấp AI không huấn luyện trên dữ liệu. Điều khoản Anthropic, Viettel AI, Azure phải xác minh trước khi dùng dữ liệu trẻ thật.

## 9. Acceptance ưu tiên cho vertical slice

A01, A02, A05, A06, A11, A14, A18, A19, A20, A22, A23, A24, A31, A36, A40, A42, A43, A44, A46. Danh sách đầy đủ: Technical HLD v1.3 §15.1.

## 10. Pilot 10 tuần

| Tuần | Việc chính | Cổng |
| --- | --- | --- |
| 1 (08–14/10) | Spike Claude Opus 5.5/Sonnet 5.5/Haiku 5.5 trên bài làm (ẩn danh) và 20–30 đề in một trang; "Cô ơi", ASR Viettel AI, TTS Azure trên Android và iPhone; mục lục kỹ năng HK1 Cánh diều; pháp lý; shadow teacher | S 14/10 |
| 2–5 (15/10–11/11) | Vertical slice đầy đủ trên hai nền tảng; harness replay; màn hình rà soát; phát hành nội bộ | G0 11/11 |
| 6 (12–18/11) | Alpha 5 gia đình (cả Android và iOS) | G1 18/11 |
| 7–10 (19/11–16/12) | Pilot 15 → 50 gia đình; phiếu bài; phỏng vấn; đặt cọc | G2 ≈ 22/11; go/no-go 16/12 |

Ngưỡng: Business HLD v1.3 §11. Nguồn lực: 3 kỹ sư, 1 shadow teacher Toán lớp 6, Sơn.

## 11. Quyết định

**Đã chốt:** xem bảng D01–D31 ở Business HLD v1.3 §0.1.

**Còn mở:** xác minh điều khoản Anthropic, Viettel AI, Azure; cấu hình máy tối thiểu ngoài phiên bản hệ điều hành; khối lượng rà soát của shadow teacher; nội dung đồng ý; mức đặt cọc; ngân sách.

## 12. Hướng dẫn cho AI coding agent

- Đọc context này, rồi cả hai HLD v1.3; đọc repo và test trước khi làm.
- Thứ tự: spike vision (đề + bài làm + số câu) và "Cô ơi" → harness replay → luồng chụp đề + xác nhận + scope gate → attempt (ẩn danh hóa, ItemResolver, ValidatorRegistry, policy, retrieval theo scope, output filter, TTS) → tiến độ/học tiếp → báo cáo, web, phiếu bài, rà soát.
- Không mở READY khi bộ đề hoặc scope chưa xác nhận; không mặc định scope = toàn lớp 6.
- Mọi luồng trong buổi học có đường không chạm, có test tự động.
- Server từ chối ảnh khi `person_check != PASSED` hoặc chưa có đồng ý; request tới Anthropic không mang dữ liệu định danh (A43).
- Code tất định chấm đúng/sai; bộ chấm đăng ký qua registry theo domain; output filter chặn lộ đáp án, ngoài lề, ngoài phạm vi.
- Mọi model qua adapter; ghi `model_version`, `prompt_version`, `policy_version`, `learned_scope_version`.
- Không triển khai: camera chạy ngầm, ASR luôn bật, chặn cứng sau ba lần trợ giúp, chấm điểm tập trung, lời giải tự động, gợi ý ngoài phạm vi.
- Bàn giao: code đã đổi, test đã chạy, benchmark đã đo, blocker, bước tiếp theo.

**Nguyên tắc xuyên suốt:** Con tự làm đề, gọi cô khi cần, cô chỉ dạy những gì con đã học, và con không phải chạm vào máy.
