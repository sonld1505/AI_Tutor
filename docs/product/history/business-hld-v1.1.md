# Business HLD — AI Study Companion

> **Đã được thay thế** bởi [Business HLD v1.2](business-hld-v1.2.md), [Technical HLD v1.2](technical-hld-v1.2.md) và [context v0.4](ai-study-companion-context-v0.4.md) ngày 07/10/2026. Giữ lại để tra lịch sử; không dùng làm yêu cầu.

**Phiên bản:** 1.1  
**Ngày:** 06/10/2026  
**Chủ dự án:** Sơn  
**Tài liệu đồng hành:** [Technical HLD v1.1](technical-hld-v1.1.md)  
**Thay thế:** Business HLD 1.0 (06/10/2026)  
**Trạng thái:** Thiết kế sản phẩm và kinh doanh cho MVP pilot; các giả thuyết chưa được pilot xác nhận.

## 0. Baseline và quy tắc dùng tài liệu

Business HLD và Technical HLD cùng phiên bản **1.1** là một bộ baseline. Business HLD quản lý giá trị sản phẩm, use case, vận hành, KPI và mô hình kinh doanh. Technical HLD quản lý kiến trúc, contract và kiểm chứng. Khi đổi một quyết định chung phải cập nhật cả hai.

Nguồn hợp nhất: HLD 1.0, context v0.2.1, kế hoạch pilot, và các quyết định Sơn đưa ra ngày 06/10/2026. Không có code, benchmark hay báo giá mới trong lần cập nhật này.

### 0.1. Quyết định chung v1.1

Cột "Nguồn": **Sơn** = quyết định của chủ dự án; **Đề xuất** = đề xuất đã được đưa vào baseline, Sơn có thể bác bỏ.

| ID | Quyết định | Nguồn | Trạng thái |
| --- | --- | --- | --- |
| D01 | Paper-first: học sinh tự làm trên giấy; AI không chấm liên tục trong lúc viết | HLD 1.0 | Baseline |
| D02 | Kiểm tra bài và Trợ giúp được kích hoạt **bằng lệnh giọng nói** để học sinh có cảm giác tương tác với AI | Sơn | Baseline |
| D03 | **Rảnh tay hoàn toàn:** từ lúc bắt đầu đến lúc kết thúc buổi học, học sinh không phải chạm vào điện thoại | Sơn | Baseline |
| D04 | **MVP gửi ảnh lên server** khi có lệnh Kiểm tra/Trợ giúp: chỉ vùng giấy đã cắt, frame có người bị chặn trên máy | Sơn | Baseline |
| D05 | Ảnh được xử lý bởi model AI thương mại qua adapter; hệ thống tự chọn model; model mới phải qua bộ replay | Đề xuất | Baseline |
| D06 | Nhận dạng chữ trên điện thoại (PP-OCR, ML Kit, UniMERNet) chuyển thành **hướng R&D dài hạn**, không nằm trong MVP | Đề xuất | Baseline |
| D07 | Khoảng 60 giây không viết: AI hỏi **một lần bằng giọng nói** theo mẫu có sẵn; không gọi AI cloud; có cooldown | HLD 1.0 + Đề xuất | Baseline |
| D08 | **Thẻ lệnh in sẵn** (KIỂM TRA / GIÚP CON / XONG) là phương án dự phòng khi giọng nói không dùng được | Đề xuất | Baseline |
| D09 | Tách trạng thái đáp án và cách làm; không báo điều chưa có bằng chứng | HLD 1.0 | Baseline |
| D10 | History theo kỹ năng; ba lần trợ giúp không tạo khóa cứng hay nhãn lười | HLD 1.0 | Baseline |
| D11 | **Toán lớp 6–7**, 2–3 dạng bài; ngôn ngữ gợi ý theo SGK lớp 6–7 | Sơn | Khối lớp chốt; dạng bài chờ chốt |
| D12 | **Phiếu bài tập in** theo lỗ hổng kiến thức, sinh theo template, đáp án kiểm bằng CAS, chụp lại để chấm | Sơn | Baseline |
| D13 | Phụ huynh xem **ảnh bàn học gần trực tiếp theo yêu cầu**; live video nằm ngoài MVP | Đề xuất | Baseline |
| D14 | **Miễn phí trong pilot**, kiểm chứng ý định trả tiền bằng đặt cọc; sau pilot là freemium | Sơn | Baseline |
| D15 | Không bán/chia sẻ dữ liệu cá nhân; không quảng cáo tới trẻ | Sơn | Baseline |
| D16 | Ảnh bài làm tự xóa sau 7 ngày hoặc theo cài đặt phụ huynh; hai loại đồng ý tách biệt | Sơn + Đề xuất | Baseline |
| D17 | AI chỉ trao đổi về bài học; có bộ lọc đầu ra | Sơn | Baseline |
| D18 | Pilot tối đa 50 gia đình; **10 tuần từ kickoff đến go/no-go** | Sơn | Baseline |
| D19 | Pilot chạy trên **cả Android và iOS** | Sơn | Baseline |
| D20 | Từ gọi là **"Cô ơi"** | Sơn | Baseline |

### 0.2. Thay đổi so với v1.0

| Nội dung v1.0 | Nội dung v1.1 |
| --- | --- |
| Nút Check/Help trên màn hình | Lệnh giọng nói; thẻ lệnh dự phòng; nút chỉ cho phụ huynh/khẩn cấp |
| Học sinh chọn vùng bài, xác nhận ký hiệu tại App | Xác nhận bằng giọng nói; khoanh số câu trên giấy; không chạm máy |
| OCR tại client, API chỉ nhận JSON | MVP gửi ảnh đã cắt; OCR trên máy là R&D dài hạn |
| Lớp 6–9, ưu tiên phương trình một ẩn | Lớp 6–7, dạng tìm x và tính biểu thức |
| Ví dụ gợi ý "trừ 5 ở cả hai vế" | Ngôn ngữ SGK lớp 6–7 ("tìm số hạng chưa biết") |
| Không có phiếu bài in | Phiếu bài in là giá trị chính cho phụ huynh |
| Subscription B2C 200–400k từ đầu | Miễn phí trong pilot, đặt cọc, freemium sau pilot |
| Live View qua WebRTC | Ảnh gần trực tiếp theo yêu cầu; live video sau MVP |
| Pilot 30 ngày, gate G0–G5 | 10 tuần, cổng S/G0/G1/G2, bảng go/no-go có ngưỡng |
| Phần scale 100.000–1 triệu active | Chuyển thành phụ lục; MVP thiết kế cho 50 gia đình |

## 1. Tầm nhìn và giá trị

AI Study Companion giúp học sinh lớp 6–7 tự học Toán trên giấy với smartphone sẵn có đặt trên giá đỡ. Học sinh tự làm; khi muốn, các em **gọi cô bằng giọng nói** để kiểm tra hoặc xin gợi ý, không cần chạm vào máy. Phụ huynh biết con đang hổng chỗ nào qua báo cáo và nhận **phiếu bài in** để con luyện đúng chỗ đó.

- Thông điệp học sinh: "Con cứ thử tự làm. Khi cần, con gọi cô."
- Thông điệp phụ huynh: "Biết con hổng chỗ nào, có sẵn bài để con luyện, không cần ngồi kèm."

Không hứa tăng điểm, đọc mọi kiểu chữ hay thay thế giáo viên.

## 2. Khách hàng và người dùng

| Persona | Nhu cầu | Giá trị cần kiểm chứng |
| --- | --- | --- |
| Học sinh lớp 6–7 | Học trên giấy, được giúp khi gọi, không bị cho đáp án | Gọi cô tự nhiên; không phải chỉnh máy; làm tiếp được sau gợi ý |
| Phụ huynh | Không phải kèm, biết lỗ hổng thật, có bài để con luyện | Báo cáo đáng tin; phiếu bài in hữu ích; kiểm soát camera |
| Giáo viên đồng hành (pilot) | Gợi ý đúng chương trình | Gán nhãn, kiểm tra quyết định AI, duyệt template phiếu |
| Đội vận hành | Kiểm soát chất lượng, sự cố, chi phí | Trace được lỗi; không lẫn dữ liệu |

Thị trường đầu: gia đình tại Việt Nam có smartphone tương thích và con học lớp 6–7. Chưa có TAM/SAM/SOM hay số liệu willingness-to-pay.

## 3. Định vị và khác biệt

**Rủi ro định vị:** khi AI chỉ lên tiếng lúc được gọi, sản phẩm gần với "chụp bài để kiểm tra" mà các trợ lý AI miễn phí cũng làm được. Khác biệt phải nằm ở ba điểm dưới đây, và sales copy phải nói rõ ba điểm này.

| Đối thủ | Điểm yếu cần kiểm chứng | Khác biệt của chúng ta |
| --- | --- | --- |
| Trợ lý AI đa năng có camera (ChatGPT, Gemini…) | Phải cầm máy chụp; dễ đưa đáp án; không có báo cáo cho phụ huynh | Rảnh tay; chấm từng dòng, chỉ lỗi gốc; báo cáo và phiếu bài theo SGK |
| App giải bài (Photomath…) | Trẻ lấy đáp án ngay | Không đưa đáp án; gợi ý từng bậc |
| Gia sư, học thêm | Chi phí theo giờ | Hỗ trợ tự học mỗi tối giữa các buổi học |
| Thiết bị AI học tập chuyên dụng | Phải mua phần cứng | Dùng smartphone sẵn có và giá đỡ |

**Ba trụ khác biệt:**

1. **Rảnh tay, như có cô ngồi cạnh:** gọi bằng giọng nói, không cầm máy, không chỉnh camera.
2. **Chấm cách làm, không chỉ đáp án:** bộ kiểm tra Toán tất định chỉ ra đúng dòng sai gốc.
3. **Vòng lặp phụ huynh:** báo cáo lỗ hổng → phiếu bài in → con làm → chụp chấm → hồ sơ cập nhật.

Moat tiềm năng: bộ replay có gán nhãn bài làm thật của trẻ Việt; template gợi ý và phiếu bài đã kiểm chứng theo SGK; dữ liệu lỗi kỹ năng có đồng ý; niềm tin của phụ huynh. Model AI thương mại không phải lợi thế, vì đối thủ cũng thuê được.

## 4. Nguyên tắc sản phẩm

1. Trẻ tự làm trước; AI im lặng khi chưa được gọi.
2. **Không bắt trẻ chạm máy trong buổi học.** Mọi tương tác qua giọng nói, giấy hoặc thẻ lệnh.
3. Khoảng một phút không viết chỉ là tín hiệu để hỏi một lần, không chứng minh trẻ bí hay lười.
4. Không đọc rõ thì hỏi lại bằng giọng nói; không chấm sai vì camera hoặc nhận dạng.
5. Gợi ý nhỏ nhất đủ để trẻ làm tiếp; không tự đưa lời giải đầy đủ.
6. Gợi ý dùng đúng cách diễn đạt của SGK lớp 6–7.
7. AI chỉ nói về bài học.
8. History chỉ dùng để cá nhân hóa, không dùng để từ chối giúp.
9. Đáp án đúng không chứng minh cả cách làm đúng.
10. Camera chỉ chạy trong buổi học, có chỉ báo; máy của con báo khi phụ huynh đang xem.
11. Báo cáo chỉ mô tả điều có bằng chứng; không chấm điểm tập trung hay gán động cơ.
12. Kết quả bài cũ không xuất hiện ở bài hoặc buổi học mới.

## 5. Hành trình và use case

### 5.1. Hành trình chính

**Trước buổi học (được chạm máy):** phụ huynh setup lần đầu; mỗi tối trẻ mở app, cắm sạc, đặt máy lên giá.

**Trong buổi học (không chạm máy):**

App thấy đủ trang vở → chào một câu → trẻ tự làm → trẻ nói "Cô ơi, kiểm tra" hoặc "Cô ơi, giúp con" → app tự chụp khi vở ổn định → cô phản hồi bằng giọng nói → trẻ sửa hoặc làm tiếp → kiểm tra lại → trẻ nói "Con học xong rồi" → phụ huynh nhận báo cáo.

App phải báo trạng thái bằng âm thanh ngắn và câu nói: đã nghe lệnh, đang xem bài, cần bỏ tay khỏi vở, mất mạng. Không dùng một hiệu ứng "AI đang nghĩ" để che lỗi camera hoặc mạng.

### 5.2. Lệnh giọng nói (bộ đầu, chờ test với trẻ)

| Ý định | Ví dụ câu nói | Thẻ lệnh dự phòng |
| --- | --- | --- |
| Kiểm tra bài | "Cô ơi, kiểm tra giúp con" | KIỂM TRA |
| Xin trợ giúp | "Cô ơi, con không biết làm", "Cô gợi ý cho con" | GIÚP CON |
| Chọn bài | "Câu 3", hoặc khoanh số câu trên giấy | — |
| Sang bài tiếp | "Sang bài tiếp" | — |
| Chấm phiếu bài in | "Cô chấm giúp con" | — |
| Nghe lại | "Cô nhắc lại" | — |
| Dừng AI đang nói | "Cô ơi, dừng" | — |
| Tạm dừng / tiếp tục | "Cô ơi, tạm dừng" / "Học tiếp" | — |
| Kết thúc | "Con học xong rồi" | XONG |

Từ gọi là **"Cô ơi"** (D20). Vì trẻ hay nói cụm này với người khác, phải đo kích hoạt nhầm trong spike tuần 1 và trong pilot.

### 5.3. Use case

| ID | Use case | Hành vi và kết quả |
| --- | --- | --- |
| U01 | Bắt đầu buổi học | Đặt máy lên giá; app tự kiểm tra khung hình; đạt thì chào và bắt đầu, không cần bấm |
| U02 | Tự làm hoặc tự sửa trước khi gọi | AI im lặng; chưa ghi kết quả xác nhận |
| U03 | Gọi kiểm tra bài | Đọc đề và toàn lời giải; đúng thì xác nhận; sai thì chỉ dòng sai gốc |
| U04 | Một phút không viết | Cô hỏi một lần bằng giọng nói: "Con đang nghĩ hay muốn cô gợi ý?" Không gọi AI cloud |
| U05 | Gọi trợ giúp | Không cần đợi timer; gợi ý đúng bài hiện tại theo history |
| U06 | Nhận gợi ý rồi làm tiếp | Dừng giải thích; không giải nốt |
| U07 | Chữ hoặc ảnh không rõ | Cô hỏi lại bằng giọng nói ("15 hay 18?"), nhờ bỏ tay ra hoặc viết rõ lại. **Không yêu cầu chạm màn hình** |
| U08 | Sửa rồi kiểm tra lại | Dùng đúng phiên bản bài mới; dùng lại đề đã xác nhận |
| U09 | Ba lần xin giúp | Xem lại tiến triển và kiến thức nền; không khóa giúp đỡ |
| U10 | Đổi bài/trang hoặc mất mạng | Báo trạng thái bằng giọng nói; không phát phản hồi muộn sang bài khác |
| U11 | Vở bị lệch | App tự bù lệch nhỏ; lệch lớn thì nhắc **xê dịch vở**, không chỉnh máy |
| U12 | Phụ huynh xem từ xa | Ảnh bàn học gần trực tiếp theo yêu cầu; máy con hiện chỉ báo; đóng khi buổi học kết thúc |
| U13 | Báo cáo phụ huynh | Báo cáo sau buổi và báo cáo tuần; nhóm kết quả loại trừ nhau |
| U14 | Phiếu bài in | Phụ huynh tải PDF và in; con làm; đặt phiếu vào vùng chụp và nói "Cô chấm giúp con" |
| U15 | Giọng nói không dùng được | Trẻ giơ thẻ lệnh trước camera |
| U16 | Liên kết tài khoản và đồng ý | Phụ huynh tạo tài khoản, liên kết hồ sơ con, ký đồng ý loại 1 (bắt buộc) và chọn loại 2 (tùy chọn). Chưa có đồng ý loại 1 thì app không bật camera/micro |
| U17 | Quản lý dữ liệu của con | Phụ huynh xem, xuất, xóa dữ liệu; chỉnh thời hạn lưu ảnh; rút đồng ý loại 2 bất cứ lúc nào |

### 5.4. Ví dụ sư phạm (lớp 6–7)

Bài: tìm x biết 3x + 5 = 20. Trẻ viết 3x = 25 rồi x = 25/3, sau đó nói "Cô ơi, kiểm tra".

Phản hồi nhắm vào dòng 2: "Con xem lại dòng thứ hai nhé. Muốn tìm số hạng chưa biết thì con làm phép tính gì?" Không coi phép chia ở dòng 3 là lỗi gốc mới, không đọc đáp án x = 5.

Nếu chưa chắc trẻ viết 15 hay 18, cô hỏi: "Dòng hai con viết mười lăm hay mười tám?" và chờ trẻ trả lời. Nếu đáp án đúng nhưng thiếu dòng giữa, báo cáo ghi "đáp án đúng, cách làm chưa xác nhận".

Giáo viên đồng hành phải duyệt cách diễn đạt theo bộ SGK của nhóm pilot.

### 5.5. Chính sách gợi ý

| Bằng chứng | Hướng hỗ trợ |
| --- | --- |
| Đã tự làm đúng dạng tương đương | Nhắc nguyên lý, mời thử bước đầu |
| Chưa gặp hoặc thiếu kiến thức nền | Giải thích khái niệm; có thể bắt đầu ở mức cao hơn |
| Lặp lỗi cùng kỹ năng | Nhắm vào kiến thức gốc |
| Nhiều gợi ý chưa tiến triển | Đổi cách giải thích, dùng ví dụ đơn giản hơn |
| Xin đáp án liên tục | Mời làm một bước; vẫn giữ đường giúp |

L1 nhắc nhẹ, L2 khái niệm, L3 một bước trung gian. Không tăng mức chỉ vì hết giờ. Nhắc chỉnh vở/camera không tính là gợi ý Toán. Gợi ý ghi theo episode, không theo số lần gọi.

## 6. Phạm vi MVP và đóng gói

| Nhóm | MVP pilot | Sau khi có bằng chứng |
| --- | --- | --- |
| Lõi | Kiểm tra/Trợ giúp bằng giọng nói, 2–3 dạng bài lớp 6–7, history, báo cáo | Thêm dạng bài đã kiểm chứng |
| Rảnh tay | Từ gọi, lệnh giọng nói, tự chụp, tự bù lệch, thẻ lệnh | Nhận biết hoàn thành bài tự động |
| Phụ huynh | Liên kết tài khoản, báo cáo, phiếu bài in, ảnh gần trực tiếp | Live video |
| Thiết bị | Android và iOS, danh sách máy hỗ trợ, giá đỡ chuẩn | Mở rộng dòng máy |
| Nhận dạng | Model AI thương mại trên server | Nhận dạng trên máy (R&D) |
| Bút cảm ứng | Không | Digital Ink |

Chưa đưa vào MVP: môn khác, lớp 8 trở lên, avatar/3D, gamification, chấm điểm tập trung/cảm xúc, marketplace giáo viên, LMS, camera chạy ngầm, hình học, tự giải toàn bài.

**Phụ kiện tặng kèm pilot:** giá đỡ đế nặng, bộ thẻ lệnh, hướng dẫn setup in.

## 7. Dữ liệu, quyền và niềm tin

- Ảnh chỉ được gửi khi có lệnh Kiểm tra/Trợ giúp, khi chụp phiếu, hoặc khi phụ huynh đang xem.
- Frame có người bị chặn trên máy và không bao giờ rời máy. Chỉ gửi vùng giấy đã cắt.
- Ảnh bài làm tự xóa sau 7 ngày hoặc theo cài đặt phụ huynh. Dữ liệu học có cấu trúc lưu trong DB của hệ thống.
- Nhà cung cấp AI phải có cam kết không huấn luyện trên dữ liệu và lưu tối thiểu. Gửi dữ liệu ra nước ngoài cần hồ sơ theo quy định.
- **Micro:** chỉ nhận diện từ gọi ngay trên máy; âm thanh chỉ gửi lên server sau khi nghe thấy từ gọi. Không lưu bản ghi âm mặc định.
- **Hai loại đồng ý:** (1) dùng dịch vụ, bắt buộc; (2) cho dùng ảnh bài làm để cải thiện hệ thống, tùy chọn, rút lại được.
- Phụ huynh xem, xuất và xóa dữ liệu của con (U16, U17).
- Không bán hoặc chia sẻ dữ liệu cá nhân; không quảng cáo tới trẻ.
- Khung giờ học chỉ là lịch nhắc, không tự bật camera.

Đây là yêu cầu thiết kế, không phải ý kiến pháp lý. Cần tư vấn pháp lý trước pilot.

## 8. KPI

### 8.1. Kết quả học theo bài

Bốn nhóm loại trừ nhau:

1. Đúng đầy đủ ở lần kiểm tra đầu, chưa nhận gợi ý.
2. Đúng sau phản hồi kiểm tra, chưa nhận gợi ý bổ sung.
3. Đúng sau trợ giúp.
4. Chưa hoàn thành hoặc chưa xác nhận.

**North Star:** tỷ lệ bài đúng đầy đủ ở lần kiểm tra đầu, không nhận gợi ý, trên tổng bài đủ điều kiện đánh giá. Báo song song tỷ lệ chưa xác nhận, độ khó và coverage.

### 8.2. Chất lượng và trải nghiệm

| KPI | Định nghĩa | Mục tiêu pilot |
| --- | --- | --- |
| Error precision | Kết luận lỗi đúng / tổng kết luận lỗi | > 90% |
| Error recall | Lỗi phát hiện / lỗi ground truth trên evidence đủ | ≥ 90% |
| Hint → Recovery | Episode dẫn tới tiến triển đúng / episode đánh giá được | > 70% |
| Kết luận sai khi thiếu bằng chứng | Kết luận Toán sai trên mẫu evidence không đủ | < 1% |
| **Chạm máy trong buổi học** | Buổi có ít nhất một lần trẻ phải chạm máy | ≤ 10% số buổi |
| **Chỉnh lại máy** | Buổi phải chỉnh lại vị trí điện thoại | < 10% |
| **Lệnh giọng nói hiểu đúng lần đầu** | Lệnh hiểu đúng / tổng lệnh | ≥ 90% |
| **Kích hoạt nhầm** | AI phản hồi khi trẻ không gọi | < 1 lần/giờ |
| Độ trễ xác nhận đã nghe lệnh | Kết thúc câu lệnh → âm báo/câu "Cô xem nhé" | p95 ≤ 1 giây |
| Độ trễ phản hồi | Kết thúc câu lệnh → bắt đầu câu phản hồi | p95 ≤ 5 giây |
| Gợi ý lộ đáp án | Gợi ý L1/L2 chứa đáp án cuối | < 5% |

Precision và recall phải có nhãn của giáo viên Toán.

### 8.3. KPI phụ huynh và kinh doanh

Activation (setup thành công và buổi học đầu), số buổi/tuần, retention theo tuần, tỷ lệ mở báo cáo, tỷ lệ phiếu bài được làm và chụp lại, tỷ lệ đặt cọc, chi phí/học sinh/tháng, thời gian hỗ trợ.

## 9. Mô hình kinh doanh

### 9.1. Chiến lược

- **Pilot:** miễn phí, tối đa 50 gia đình. Cuối pilot mời **đặt cọc thật** cho gói sau pilot, có cam kết hoàn tiền nếu không ra mắt.
- **Sau pilot:** freemium.

| Miễn phí | Trả phí (giả thuyết) |
| --- | --- |
| Giới hạn số buổi hoặc phút mỗi ngày | Không giới hạn |
| Kiểm tra bài, gợi ý L1–L2 | Toàn bộ mức gợi ý |
| Báo cáo sau buổi | Báo cáo tuần/tháng, xu hướng, lỗ hổng chi tiết |
| — | Phiếu bài in theo điểm yếu |
| Ảnh gần trực tiếp giới hạn | Ảnh gần trực tiếp không giới hạn; live video sau này |

Giới hạn của gói miễn phí không được chặn trợ giúp giữa một bài đang làm. Mức giá 200.000–400.000 đồng/tháng vẫn là giả thuyết, chưa có bằng chứng thị trường.

Hướng thu tiền khác cần kiểm chứng: trường hoặc trung tâm dùng để giao bài về nhà (B2B2C); kết nối gia sư khi phụ huynh chủ động đồng ý.

### 9.2. Unit economics

Chi phí biến đổi mỗi học sinh/tháng:

`V = vision + reasoning/tutor + ASR + TTS + lưu ảnh 7 ngày + parent view + infra biến đổi + thanh toán + hỗ trợ biến đổi`

- Vision: số lần Kiểm tra/Trợ giúp/chụp phiếu × số ảnh × đơn giá model.
- Reasoning: số lượt gợi ý/báo cáo/phiếu × token × đơn giá.
- ASR: chỉ các đoạn sau từ gọi. TTS: số giây cô nói.
- Parent view: số phút phụ huynh xem × tần suất làm mới ảnh.

`Contribution = P_net − V`. Nếu thu qua App Store/Google Play, P_net phải trừ phí nền tảng 15–30%; cân nhắc thanh toán trực tiếp qua web.

`Break-even = ceil(chi phí cố định tháng / Contribution)`, chỉ có nghĩa khi Contribution > 0.

**Pilot:** 50 gia đình là quy mô nhỏ, nên chi phí AI ước tính chỉ vài triệu đến khoảng 15 triệu VND/tháng (chưa có báo giá). Pilot dùng model chất lượng tốt nhất; tối ưu chi phí để sau khi có số đo.

### 9.3. Kịch bản

| Kịch bản | Giá ròng | Mức sử dụng | Dữ liệu cần |
| --- | --- | --- | --- |
| Thận trọng | Đặt cọc thấp | Nhiều lần gọi, nhiều ảnh chụp lại | Chi phí p95, người dùng nặng |
| Cơ sở | Giá pilot chấp nhận | Trung vị đo được | Cohort thực |
| Lạc quan | Retention và đặt cọc tốt | Template/cache hiệu quả | Bằng chứng từ pilot |

## 10. Go-to-market

- Tuyển gia đình pilot qua nhóm phụ huynh, giáo viên giới thiệu và người quen; **ít nhất một phần là người không quen** để tránh phản hồi "nể".
- Onboarding qua gọi video 15 phút: đặt máy, cắm sạc, bật Không làm phiền, thử lệnh giọng nói và thẻ lệnh.
- Chưa có CAC hay hiệu quả kênh. Mỗi thử nghiệm kênh cần giới hạn ngân sách và theo dõi cohort.
- Không so sánh với đối thủ trong sales copy khi chưa audit lại từ nguồn hiện tại.

## 11. Pilot và lộ trình 10 tuần

**Lộ trình:** 10 tuần **từ kickoff đến buổi quyết định go/no-go**, gồm cả xây dựng và chạy pilot, trên cả Android và iOS (D18, D19).

**Nguồn chuẩn:** các cổng và bảng go/no-go trong mục này là bản gốc. Trang Kế hoạch Pilot phản chiếu cùng nội dung; khi đổi ngưỡng phải sửa cả hai.

| Tuần | Việc chính | Cổng |
| --- | --- | --- |
| 1 | Spike: model đọc chữ viết tay trẻ trên 100–200 mẫu; từ gọi "Cô ơi" và ASR giọng trẻ trên Android và iPhone; thiết bị; pháp lý; tuyển giáo viên; chốt dạng bài | **S** cuối tuần 1 |
| 2–5 | Vertical slice trên cả hai nền tảng: app rảnh tay, backend, bộ kiểm tra Toán, chính sách gợi ý, tutor, báo cáo, phiếu bài cơ bản, web phụ huynh; phát hành nội bộ | **G0** cuối tuần 5: đạt ngưỡng trên bộ replay và máy thật |
| 6 | Alpha 5 gia đình, có cả Android và iOS | **G1** cuối tuần 6 |
| 7–10 | Pilot 15 → 50 gia đình; phát phiếu bài; phỏng vấn hằng tuần; mời đặt cọc cuối tuần 10 | **G2** giữa tuần 7: mở 50 gia đình |
| Cuối tuần 10 | Quyết định go/no-go | Bảng §11.2 |

**Đánh đổi của lộ trình 10 tuần:** gia đình vào pilot dùng khoảng 3–4 tuần, vẫn chưa đủ để kết luận về retention dài hạn. Hai tuần thêm so với phương án 8 tuần chủ yếu dành cho iOS và test máy thật. Không làm chế độ bóng: AI chỉ nói khi được gọi nên rủi ro can thiệp sai thấp hơn bản v0.2. Phiếu bài ở mức cơ bản (1 dạng template mỗi tuần).

**Nguồn lực tối thiểu:** 3 kỹ sư (mobile và voice cho cả Android và iOS; backend và AI; fullstack cho web phụ huynh, phiếu bài, vận hành), 1 giáo viên Toán bán thời gian, Sơn làm product và vận hành pilot.

### 11.1. Các cổng

**S — Spike đạt (cuối tuần 1)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Model vision đọc đúng từng dòng bài làm của trẻ (100–200 mẫu) | Đủ để đạt G0 sau tuning |
| Từ gọi nhận đúng giọng trẻ trong phòng thường | Có phương án khả thi |
| 2–3 dạng bài và bộ SGK | Đã chốt |

**G0 — Replay và máy thật, trước khi phát cho gia đình (cuối tuần 5)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Error precision | ≥ 85% |
| Kết luận Toán từ ảnh xấu | ≈ 0 |
| Gợi ý L1/L2 lộ đáp án | < 5% |
| Frame có người tới server | 0 |
| Đề/đáp án phiếu bài sai | 0 |
| Lệnh giọng nói hiểu đúng (giọng trẻ, phòng thường) | ≥ 85% |
| Buổi test 45 phút không cần chạm máy | Đạt |
| Chạy ổn trên Android và iOS trong danh sách máy hỗ trợ | Đạt |

**G1 — Alpha 5 → mở 15 gia đình (cuối tuần 6)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Buổi học không crash hoặc mất dữ liệu | ≥ 95% |
| Gia đình setup đạt trong 5 phút ở lần đầu | ≥ 4/5 |
| Báo cáo sau buổi khớp kiểm tra tay của giáo viên | 100% |
| Sự cố dữ liệu hoặc quyền riêng tư | 0 |
| Gia đình alpha dùng mỗi nền tảng | ≥ 2 |

**G2 — 15 → mở 50 gia đình (giữa tuần 7)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Lỗi blocker còn mở | 0 |
| Kích hoạt nhầm đo thực tế | < 1 lần/giờ |
| Đội hỗ trợ phản hồi trong ngày | ≥ 90% yêu cầu |

### 11.2. Go/no-go cuối tuần 10

Đánh giá trên các gia đình đã dùng ít nhất 3 tuần. Báo riêng kết quả Android và iOS.

| Nhóm | Chỉ số | Go | Xem lại | No-go |
| --- | --- | --- | --- | --- |
| Chất lượng AI | Phản hồi sai / tổng phản hồi | < 10% | 10–20% | > 20% |
| Rảnh tay | Buổi phải chạm hoặc chỉnh máy | < 10% | 10–25% | > 25% |
| Giọng nói | Gia đình phàn nàn về nhận lệnh | < 15% | 15–30% | > 30% |
| Sử dụng | Gia đình còn dùng ≥ 3 buổi/tuần ở tuần thứ 3 của họ | ≥ 50% | 30–50% | < 30% |
| Giá trị | Đồng ý "báo cáo giúp tôi biết con hổng chỗ nào" | ≥ 70% | 50–70% | < 50% |
| Giá trị | Phiếu bài được làm và chụp lại | ≥ 40% | 20–40% | < 20% |
| Kinh doanh | Đặt cọc thật | ≥ 20% | 10–20% | < 10% |
| Chi phí | Chi phí AI p95/học sinh/tháng | Đo được, có lộ trình giảm | Đo được | Không đo được |
| An toàn | Frame có người tới server; sự cố dữ liệu | 0 | — | ≥ 1: dừng ngay |

**Quy tắc quyết định:**

1. **Go:** An toàn đạt, không có No-go, và ít nhất 6/8 chỉ số còn lại đạt Go. Mở rộng, bắt đầu freemium.
2. **Lặp lại:** không có No-go nhưng dưới 6 chỉ số đạt Go. Chạy thêm 4 tuần với cùng nhóm, tập trung vào chỉ số yếu nhất.
3. **Chuyển hướng:** No-go ở Giá trị hoặc Kinh doanh. Xem lại định vị hoặc thử B2B2C.
4. **Quay về replay:** No-go ở Chất lượng AI, Rảnh tay hoặc Giọng nói. Không mở rộng; sửa trên bộ replay.
5. **Dừng ngay:** bất kỳ vi phạm An toàn nào, ở bất kỳ thời điểm nào.

## 12. Rủi ro

| Rủi ro | Tác động | Xử lý |
| --- | --- | --- |
| Model đọc sai chữ viết tay của trẻ | Chấm sai, mất niềm tin | Hỏi lại bằng giọng nói; UNKNOWN; bộ replay; chọn model qua cổng |
| Không nhận được giọng trẻ hoặc phòng ồn | Trẻ phải chạm máy, bực bội | Spike tuần 1; thẻ lệnh dự phòng; tối ưu từ gọi |
| Kích hoạt nhầm (TV, anh chị em) | Làm phiền, tốn chi phí | Ngưỡng từ gọi; xác nhận ý định ngắn; đo kích hoạt nhầm |
| Vở lệch, trẻ chạm máy | Mất thời gian chỉnh | Giá đỡ đế nặng; tự bù lệch; nhắc xê dịch vở |
| Máy nóng, hết pin | Buổi học gián đoạn | Cắm sạc trong checklist; đo pin/nhiệt 45–60 phút |
| Thông báo/cuộc gọi che màn hình | Gián đoạn | Hướng dẫn bật Không làm phiền |
| Gợi ý sai cách diễn đạt SGK | Trẻ học lẫn lộn | Giáo viên duyệt template; bộ test ngôn ngữ |
| Khác biệt yếu so với trợ lý AI miễn phí | Không ai trả tiền | Ba trụ khác biệt §3; đo đặt cọc |
| Lộ trình 10 tuần, làm cả Android và iOS | Trượt cổng; lỗi riêng từng nền tảng | Flutter cho phần chung; cân nhắc thêm kỹ sư mobile bán thời gian cho native iOS; cổng chặt; thu hẹp còn 1 dạng bài nếu cần |
| "Cô ơi" là cụm từ trẻ hay nói | Kích hoạt nhầm khi trẻ gọi người nhà hoặc xem video | Đo trong spike; xác nhận ý định ngắn; ngưỡng riêng theo nền tảng |
| Giới hạn của iOS | Không tự bật Không làm phiền; app phải ở foreground | Hướng dẫn phụ huynh bật Focus; giữ màn hình sáng; test riêng trên iPhone |
| Rủi ro pháp lý dữ liệu trẻ | Dừng dự án | Tư vấn pháp lý tuần 1; hai loại đồng ý; nhà cung cấp không lưu dữ liệu |

## 13. Traceability

| Yêu cầu kinh doanh | Cơ chế kỹ thuật | Acceptance (Technical HLD §15) |
| --- | --- | --- |
| Rảnh tay suốt buổi học | Từ gọi, lệnh giọng nói, tự chụp, tự bù lệch, thẻ lệnh | A21–A25, A28 |
| Không chen ngang | Chỉ phản hồi khi có lệnh; hỏi một lần khi idle | A02, A04 |
| Không chấm sai vì ảnh | Quality gate, UNKNOWN, hỏi lại bằng giọng nói | A08–A11 |
| Gợi ý cá nhân hóa | History theo kỹ năng, episode | A05, A14 |
| Không gợi ý trùng hoặc lỗi thời | Idempotency, revision | A06, A07, A12, A13 |
| Bảo vệ quyền riêng tư | Chặn frame có người, chỉ gửi vùng giấy, xóa 7 ngày | A17, A26, A29 |
| Đồng ý và quản lý dữ liệu (U16, U17) | Consent gate; API xuất/xóa dữ liệu | A30, A31 |
| Báo cáo đáng tin | Mô hình event/outcome | A16 |
| Phiếu bài đúng | Template + CAS | A27 |
| Phụ huynh xem từ xa đúng quyền | Token theo parent–student–session | A15 |

Đổi phạm vi dữ liệu, chặn cứng trợ giúp, tự bật camera, đưa lời giải đầy đủ hoặc đổi giá là thay đổi sản phẩm, cần Sơn quyết định và cập nhật cả hai HLD.

## 14. Còn mở

- 2–3 dạng bài và bộ SGK; giáo viên đồng hành.
- Bộ câu lệnh, sau khi test với trẻ.
- Danh sách máy Android và iOS hỗ trợ trong pilot.
- Nhà cung cấp model vision/LLM/ASR/TTS và điều khoản lưu dữ liệu.
- Nội dung hai loại đồng ý; thời hạn lưu ảnh cho bộ replay.
- Mức đặt cọc, giá gói sau pilot, kênh thanh toán.
- Ngân sách pilot.

**Khi bàn giao cho team hoặc coding agent:** đọc cả hai HLD v1.1, kiểm tra repo hiện tại, lập backlog theo tuần và cổng, báo trạng thái thật. Không khôi phục các yêu cầu cũ đã bị thay thế ở §0.2.
