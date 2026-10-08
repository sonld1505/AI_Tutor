# AI Study Companion — Project Context

> **Đã được thay thế** bởi [Business HLD v1.2](business-hld-v1.2.md), [Technical HLD v1.2](technical-hld-v1.2.md) và [context v0.4](ai-study-companion-context-v0.4.md) ngày 07/10/2026. Giữ lại để tra lịch sử; không dùng làm yêu cầu.

**Phiên bản:** 0.3 • **Ngày:** 06/10/2026 • **Chủ dự án:** Sơn • **Thay thế:** v0.2.1 (05/10/2026)

## 0. Vai trò của tài liệu và thay đổi so với v0.2.1

Tài liệu này là **bản tóm tắt cho coding agent và người mới vào team**. Nguồn chi tiết là bộ HLD v1.1:

- [Business HLD v1.1](business-hld-v1.1.md): giá trị, use case, KPI, mô hình kinh doanh, pilot.
- [Technical HLD v1.1](technical-hld-v1.1.md): kiến trúc, contract, acceptance A01–A31.
- Use case U01–U17: Business HLD v1.1 §5.3. Cổng và go/no-go: Business HLD v1.1 §11 (nguồn chuẩn), trang Kế hoạch Pilot phản chiếu cùng nội dung.

Nếu context và HLD v1.1 mâu thuẫn, **HLD v1.1 thắng**. Dừng lại và báo Sơn, không tự chọn.

| # | v0.2.1 | v0.3 |
| --- | --- | --- |
| 1 | AI quan sát liên tục và tự quyết định khi nào can thiệp | **AI chỉ phản hồi khi học sinh gọi** (Kiểm tra/Trợ giúp); idle ~60 giây chỉ hỏi một lần |
| 2 | Voice là giao diện trợ giúp chính | **Lệnh giọng nói** với từ gọi; thẻ lệnh in làm dự phòng |
| 3 | Nút Start/Pause/End trên app | **Học sinh không chạm máy suốt buổi học** |
| 4 | Chụp ảnh theo sự kiện liên tục | **Chỉ chụp khi có trigger**; app tự chờ vở ổn định, không có tay che |
| 5 | Chế độ bóng 1–2 tuần đầu pilot | **Bỏ chế độ bóng**, vì AI không tự lên tiếng |
| 6 | Nhóm kết quả: tự làm / tự sửa / sau gợi ý | **Đúng lần đầu / đúng sau kiểm tra / đúng sau trợ giúp / chưa xong** (không đoán việc tự sửa trước khi gọi) |
| 7 | Pilot 14 tuần | **10 tuần từ kickoff đến go/no-go** |
| 8 | Kiểm tra Toán do model kết hợp engine | **Bộ kiểm tra Toán tất định** (parser + SymPy) chấm từng dòng; LLM chỉ viết lời |
| 9 | 2 kỹ sư | 3 kỹ sư |
| 10 | Nền tảng app chờ chốt | **Pilot trên Android và iOS**; từ gọi **"Cô ơi"** |

Giữ nguyên từ v0.2.1: lớp 6–7; ảnh vùng giấy đã cắt gửi model thương mại; chặn frame có người trên máy; ảnh xóa sau 7 ngày; phiếu bài in; miễn phí trong pilot; không bán dữ liệu; ảnh gần trực tiếp cho phụ huynh.

Chưa có repo hay code. Không suy diễn tính năng đã được triển khai.

## 1. Bài toán và định vị

**Job-to-be-done:** Khi bố mẹ không ngồi kèm được, con vẫn tự học Toán trên giấy, gọi cô khi cần, và bố mẹ biết con hổng chỗ nào.

- Học sinh: "Con cứ thử tự làm. Khi cần, con gọi cô."
- Phụ huynh: "Biết con hổng chỗ nào, có sẵn bài để con luyện, không cần ngồi kèm."

**Ba trụ khác biệt** so với trợ lý AI miễn phí và app giải bài:

1. **Rảnh tay như có cô ngồi cạnh:** gọi bằng giọng nói, không cầm máy, không chỉnh camera.
2. **Chấm cách làm, không chỉ đáp án:** chỉ đúng dòng sai gốc; không đưa đáp án.
3. **Vòng lặp phụ huynh:** báo cáo lỗ hổng → phiếu bài in → con làm → chụp chấm → hồ sơ cập nhật.

Lợi thế nằm ở lớp điều phối, bộ replay có gán nhãn, template theo SGK và niềm tin của phụ huynh, không nằm ở model.

**Chiến lược:** miễn phí trong pilot, mời đặt cọc cuối pilot, sau đó freemium. Không bán hoặc chia sẻ dữ liệu cá nhân, không quảng cáo tới trẻ.

## 2. Nguyên tắc sản phẩm

1. Trẻ tự làm trước; AI im lặng khi chưa được gọi.
2. **Không bắt trẻ chạm máy trong buổi học.**
3. Ngừng viết một phút chỉ là tín hiệu để hỏi một lần, không chứng minh trẻ bí hay lười.
4. UNKNOWN ≠ WRONG. Không đọc rõ thì hỏi lại bằng giọng nói.
5. Gợi ý nhỏ nhất đủ để trẻ làm tiếp; không tự đưa lời giải đầy đủ.
6. Ngôn ngữ gợi ý theo SGK lớp 6–7.
7. AI chỉ nói về bài học.
8. History để cá nhân hóa, không để từ chối giúp.
9. Đáp án đúng không chứng minh cách làm đúng.
10. Nhắc chỉnh vở/camera không tính là gợi ý Toán.
11. Quyền riêng tư bằng kỹ thuật: frame có người không rời máy.
12. Phụ huynh quan sát, không can thiệp; máy con báo khi đang được xem.
13. Báo cáo chỉ nói điều có bằng chứng.

## 3. Phạm vi MVP

- **Toán lớp 6–7**, 2–3 dạng bài (chốt cùng giáo viên ở tuần 1). Ứng viên: tìm x dạng `ax + b = c`, `a(x + b) = c` với số nguyên; tìm x với phân số; tính biểu thức nhiều bước.
- App học sinh Android và iOS; web phụ huynh có liên kết tài khoản, đồng ý, xem/xuất/xóa dữ liệu.
- Kiểm tra/Trợ giúp bằng giọng nói; thẻ lệnh dự phòng.
- Gợi ý L1–L2; L3 khi trẻ chủ động hỏi thêm.
- Báo cáo sau buổi và báo cáo tuần; phiếu bài in; ảnh bàn học gần trực tiếp.

**Ngoài MVP:** môn khác, lớp 8 trở lên, live video, nhận dạng chữ trên máy, tự nhận biết hoàn thành bài, gamification, avatar, chấm điểm tập trung/cảm xúc, hình học.

## 4. Trải nghiệm rảnh tay

**Trước buổi học (được chạm máy):** mở app, cắm sạc, bật Không làm phiền, đặt máy lên giá đỡ đế nặng, góc chụp từ trên xuống.

**Trong buổi học (không chạm máy):**

| Việc | Cách làm |
| --- | --- |
| Bắt đầu | App thấy đủ 4 góc trang, máy đứng yên, không có người → chào và bắt đầu |
| Kiểm tra | "Cô ơi, kiểm tra giúp con" hoặc thẻ KIỂM TRA |
| Trợ giúp | "Cô ơi, con không biết làm" hoặc thẻ GIÚP CON |
| Chọn bài | Nói "câu 3" hoặc khoanh số câu trên giấy |
| Sang bài mới | "Sang bài tiếp", hoặc app tự nhận trang mới |
| Chữ không rõ | Cô hỏi câu đóng ("mười lăm hay mười tám?"), con trả lời |
| Tay che vở | "Con bỏ tay ra khỏi vở nhé", rồi app tự chụp |
| Vở lệch | Lệch nhỏ app tự bù; lệch lớn nhắc **xê dịch vở**, không chỉnh máy |
| Dừng cô đang nói | "Cô ơi, dừng" |
| Nghe lại | "Cô nhắc lại" |
| Tạm dừng / tiếp tục | "Cô ơi, tạm dừng" / "Học tiếp" |
| Chấm phiếu bài | Đặt phiếu vào vùng chụp, nói "Cô chấm giúp con" |
| Kết thúc | "Con học xong rồi" hoặc thẻ XONG; lâu không hoạt động thì hỏi rồi tự kết thúc |

Từ gọi là **"Cô ơi"** (đã chốt). Vì trẻ hay nói cụm này, phải đo kích hoạt nhầm.

## 5. Kiến trúc tóm tắt

```
Điện thoại: camera → 4 góc trang, bù lệch → chất lượng, che tay → chặn người/khuôn mặt → cắt trang
            micro → từ gọi trên máy → đoạn âm thanh sau từ gọi
            thẻ lệnh → nhận marker trên máy
               │ (chỉ khi có trigger)
               ▼
Server:     ASR + intent → RecognitionEngine (model vision qua adapter) → evidence gate
            → math validator (parser + SymPy) → history + hint policy → tutor LLM + output filter → TTS
            PostgreSQL · object storage (ảnh TTL 7 ngày) · queue · report worker · worksheet generator
               │
               ▼
Web phụ huynh: báo cáo, phiếu PDF, ảnh gần trực tiếp theo yêu cầu
```

- Mọi model qua adapter; hệ thống tự chọn; model mới phải qua bộ replay.
- Nhà cung cấp AI có cam kết không huấn luyện trên dữ liệu và lưu tối thiểu.
- Code tất định quyết định đúng/sai; LLM chỉ viết lời phản hồi trong giới hạn policy.
- Câu mẫu (chào, nhắc bỏ tay, nhắc xê dịch vở, câu hỏi idle) cache trên máy.
- Một backend modular monolith cùng worker; Docker trên EC2, PostgreSQL managed, S3.

Chi tiết contract, API và state machine: Technical HLD v1.1 §4–§8, §15.

## 6. Phản hồi và mức gợi ý

| Tình huống | AI làm gì |
| --- | --- |
| Trẻ đang làm, chưa gọi | Im lặng; không gửi gì lên server |
| Ngừng viết ~60 giây | Hỏi một lần: "Con đang nghĩ hay muốn cô gợi ý một chút?"; có cooldown |
| Gọi kiểm tra, bài đúng | Xác nhận ngắn |
| Gọi kiểm tra, bài sai | Chỉ dòng sai gốc, gợi ý L1; không đọc đáp án |
| Gọi trợ giúp | Gợi ý theo history; L1 → L2 khi có bằng chứng vẫn vướng |
| Hỏi thẳng đáp án | Mời làm một bước; không đưa đáp án cuối |
| Chữ/ảnh không rõ | Hỏi lại bằng giọng nói; không phán sai |
| Câu hỏi ngoài lề | Từ chối nhẹ nhàng, đưa về bài |

- **L0** im lặng · **L1** nhắc nhẹ · **L2** gợi ý khái niệm · **L3** dẫn một bước (chỉ khi trẻ chủ động hỏi thêm).
- Không tăng mức chỉ vì hết giờ. Ba lần trợ giúp là tín hiệu xem lại tiến triển, không khóa giúp đỡ.
- Ví dụ lớp 6–7: "Con xem lại dòng thứ hai nhé. Muốn tìm số hạng chưa biết thì con làm phép tính gì?"

## 7. Báo cáo và phiếu bài

**Nhóm kết quả mỗi bài (loại trừ nhau):**

1. Đúng đầy đủ ở lần kiểm tra đầu, chưa nhận gợi ý.
2. Đúng sau phản hồi kiểm tra, chưa nhận gợi ý bổ sung.
3. Đúng sau trợ giúp.
4. Chưa hoàn thành hoặc chưa xác nhận.

Không ghi "con tự sửa" cho thay đổi trước khi gọi, vì AI không quan sát giai đoạn đó.

**North Star:** tỷ lệ bài thuộc nhóm 1 trên tổng bài đủ điều kiện đánh giá; báo song song tỷ lệ nhóm 4.

- Báo cáo sau buổi đọc trong ~30 giây; báo cáo tuần có xu hướng và lỗ hổng.
- "Cần luyện" chỉ khi lỗi cùng kỹ năng lặp ở ≥ 3 bài qua ≥ 2 buổi.
- Phiếu bài: template theo dạng bài; đáp án kiểm bằng SymPy; giáo viên duyệt template; PDF A4 có dấu bốn góc và mã phiếu.

## 8. Dữ liệu và quyền riêng tư

- Ảnh chỉ gửi khi có trigger, khi chụp phiếu, hoặc khi phụ huynh đang xem.
- Frame có người bị chặn trên máy; chỉ gửi vùng giấy đã cắt.
- Ảnh tự xóa sau 7 ngày hoặc theo cài đặt phụ huynh. Dữ liệu học có cấu trúc lưu trong DB riêng.
- Âm thanh chỉ gửi sau từ gọi; không lưu bản ghi âm mặc định.
- Hai loại đồng ý: dùng dịch vụ (bắt buộc); cho dùng ảnh để cải thiện hệ thống (tùy chọn, rút lại được).
- Phụ huynh xem, xuất, xóa dữ liệu của con. Cần tư vấn pháp lý trước pilot.

## 9. Scenarios

Mỗi scenario ánh xạ tới acceptance trong Technical HLD §15.1. Use case gốc: U01–U17 trong Business HLD §5.3.

| ID | Tình huống | Hành vi mong đợi | Acceptance |
| --- | --- | --- | --- |
| SC-01 | Đặt máy lên giá | Tự bắt đầu khi đủ 4 góc trang; chào một câu; không bấm gì | A01, A21 |
| SC-02 | Trẻ làm đúng, không gọi | Im lặng; 0 gọi server | A02 |
| SC-03 | Trẻ tự sửa trước khi gọi | Im lặng; không ghi sự kiện tự sửa | A02 |
| SC-04 | Gọi kiểm tra: `3x + 5 = 20 → 3x = 25 → x = 25/3` | Chỉ dòng 2 là lỗi gốc; L1; không đọc x = 5 | A03 |
| SC-05 | Ngừng viết ~60 giây | Hỏi một lần tại máy; 0 gọi cloud | A04 |
| SC-06 | "Cô ơi, con không biết làm" | Gợi ý theo history; không cần đợi timer | A05 |
| SC-07 | L1 chưa giúp được | Lên L2 khi có bằng chứng; L3 chỉ khi trẻ hỏi thêm | A05, A14 |
| SC-08 | Trẻ làm tiếp đúng sau gợi ý | Dừng giải thích; không giải nốt | A06 |
| SC-09 | Tay che vở hoặc ảnh mờ khi chụp | Nhắc bỏ tay; chờ rồi tự chụp; không phán sai | A10, A21 |
| SC-10 | Sang bài mới | Không nhắc lỗi bài trước; bỏ phản hồi lỗi thời | A12 |
| SC-11 | Phụ huynh xem từ xa | Ảnh gần trực tiếp; máy con hiện chỉ báo; End ngắt xem | A15 |
| SC-12 | "Con học xong rồi" | Dừng camera/micro; báo cáo. Fixture: 12 bài = 8 nhóm 1 + 2 nhóm 2 + 2 nhóm 3 | A01, A16 |
| SC-13 | Lịch sử lỗi tìm số hạng; buổi mới `5x + 7 = 32` | Không nhắc trước; gợi ý phù hợp khi được gọi | A05 |
| SC-14 | Chữ 15 hay 18 không rõ | Hỏi câu đóng bằng giọng nói; chờ trả lời | A08 |
| SC-15 | "Đáp án là bao nhiêu?" | Không đưa đáp án; mời làm một bước | A03 |
| SC-16 | Chấm phiếu bài in | Nhận mã phiếu và số câu; chấm; cập nhật hồ sơ | A27 |
| SC-17 | Có người trong khung hình | Frame không rời máy; nhắc chỉnh | A26 |
| SC-18 | Thêm model mới | Phải qua bộ replay và G0 | A19 |
| SC-19 | TV hoặc anh chị em nói gần máy | Kích hoạt nhầm < 1 lần/giờ | A22 |
| SC-20 | Trẻ giơ thẻ lệnh | Giữ 1 giây → đúng intent | A28 |
| SC-21 | Vở lệch | Trong ngưỡng tự bù; ngoài ngưỡng nhắc xê dịch vở | A25 |
| SC-22 | "Cô ơi, dừng" khi cô đang nói | TTS dừng ≤ 500 ms | A24 |
| SC-23 | Phụ huynh chưa ký đồng ý loại 1 | Không tạo buổi học, không bật camera/micro | A30 |
| SC-24 | Phụ huynh xuất rồi xóa dữ liệu của con | Bản xuất đầy đủ; sau khi xóa không còn ảnh, attempt, báo cáo | A31 |

## 10. KPI chính

| KPI | Mục tiêu pilot |
| --- | --- |
| Error precision | > 90% |
| Error recall | ≥ 90% |
| Hint → Recovery | > 70% |
| Kết luận sai khi thiếu bằng chứng | < 1% |
| Buổi phải chạm máy | ≤ 10% |
| Buổi phải chỉnh lại máy | < 10% |
| Lệnh hiểu đúng lần đầu | ≥ 90% |
| Kích hoạt nhầm | < 1 lần/giờ |
| Âm báo đã nghe lệnh | p95 ≤ 1 giây |
| Bắt đầu câu phản hồi | p95 ≤ 5 giây |
| Gợi ý L1/L2 lộ đáp án | < 5% |

## 11. Pilot 10 tuần

10 tuần tính từ kickoff đến buổi go/no-go, trên cả Android và iOS.

| Tuần | Việc chính | Cổng |
| --- | --- | --- |
| 1 | Spike model vision (100–200 mẫu) và từ gọi "Cô ơi"/ASR giọng trẻ trên Android và iPhone; pháp lý; giáo viên; chốt dạng bài | S |
| 2–5 | Vertical slice đầy đủ trên cả hai nền tảng; harness replay; phát hành nội bộ | G0 |
| 6 | Alpha 5 gia đình (cả Android và iOS) | G1 |
| 7–10 | Pilot 15 → 50 gia đình; phiếu bài; phỏng vấn; đặt cọc | G2; go/no-go cuối tuần 10 |

Ngưỡng các cổng và bảng go/no-go: Business HLD v1.1 §11 là nguồn chuẩn; trang Kế hoạch Pilot phản chiếu cùng nội dung.

**Nguồn lực:** 3 kỹ sư (mobile và voice; backend và AI; fullstack), 1 giáo viên Toán bán thời gian, Sơn làm product và vận hành.

## 12. Quyết định

**Đã chốt:** lớp 6–7; Kiểm tra/Trợ giúp bằng giọng nói; không chạm máy trong buổi học; ảnh vùng giấy gửi server; phiếu bài in; miễn phí trong pilot; không bán dữ liệu; ảnh xóa sau 7 ngày; pilot tối đa 50 gia đình trong 10 tuần, trên Android và iOS; từ gọi "Cô ơi".

**Chờ chốt:** 2–3 dạng bài và bộ SGK; danh sách máy Android và iOS hỗ trợ; nhà cung cấp model vision/LLM/ASR/TTS; nội dung đồng ý; mức đặt cọc và giá sau pilot; kênh thông báo phụ huynh; ngân sách pilot.

## 13. Hướng dẫn cho AI coding agent

- Đọc context này, sau đó đọc **cả hai HLD v1.1**; đọc repo và test trước khi làm.
- Thứ tự ưu tiên: spike model vision và từ gọi → harness replay → vertical slice (nói → chụp → nhận dạng → validator → gợi ý → TTS) → báo cáo, web phụ huynh, phiếu bài.
- Mọi luồng trong buổi học phải có đường không chạm; có test tự động cho điều này.
- Frame có người không rời máy; server từ chối ảnh khi `person_check != PASSED`.
- Code tất định chấm đúng/sai; LLM chỉ viết lời; output filter chặn lộ đáp án và nội dung ngoài lề.
- Mọi model đi qua adapter; ghi `model_version`, `prompt_version`, `policy_version`.
- Không triển khai: camera chạy ngầm, ASR luôn bật gửi server, chặn cứng sau ba lần trợ giúp, chấm điểm tập trung, lời giải đầy đủ tự động.
- Khi bàn giao: code đã đổi, test đã chạy, benchmark đã đo, blocker, bước tiếp theo. Không ghi "done" chỉ vì mock chạy.

**Nguyên tắc xuyên suốt:** Con tự làm, gọi cô khi cần, không phải chạm vào máy.
