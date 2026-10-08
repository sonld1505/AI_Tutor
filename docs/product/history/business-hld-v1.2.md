# Business HLD — AI Study Companion

> **Đã được thay thế** bởi [Business HLD v1.3](../business-hld-v1.3.md), [Technical HLD v1.3](../technical-hld-v1.3.md) và [context v0.5](../ai-study-companion-context-v0.5.md) ngày 08/10/2026. Giữ lại để tra lịch sử; không dùng làm yêu cầu.

**Phiên bản:** 1.2  
**Ngày:** 07/10/2026  
**Chủ dự án:** Sơn  
**Tài liệu đồng hành:** [Technical HLD v1.2](technical-hld-v1.2.md)  
**Thay thế:** Business HLD v1.1 ngày 06/10/2026 (`business-hld-v1.1.md`) và Business HLD "1.1" ngày 07/10/2026 (`business-hld_7_Oct.md`)  
**Trạng thái:** Thiết kế sản phẩm và kinh doanh cho MVP pilot; các giả thuyết chưa được pilot xác nhận.

## 0. Baseline và quy tắc dùng tài liệu

Business HLD và Technical HLD cùng phiên bản **1.2** là một bộ baseline. Business HLD quản lý giá trị, use case, KPI, mô hình kinh doanh và pilot. Technical HLD quản lý kiến trúc, contract và acceptance. Đổi một quyết định chung phải sửa cả hai, rồi mới đồng bộ context, kế hoạch pilot và slide.

**Nguồn hợp nhất:** hai bộ tài liệu cùng mang tên "1.1" nhưng khác nội dung:

- **Bộ 06/10** (`*-v1.1.md`): các quyết định Sơn đưa ra trong trao đổi ngày 06/10 (ảnh lên server, giọng nói, không chạm máy, miễn phí, 10 tuần, Android và iOS, "Cô ơi").
- **Bộ 07/10** (`*_7_Oct.md`): buổi học theo tờ đề, phạm vi kiến thức đã học, chọn câu, lưu tiến độ, lớp 6.

**Quy tắc hợp nhất:** giữ quyết định 06/10 khi hai bộ mâu thuẫn, trừ khối lớp (Sơn chốt **lớp 6** ngày 07/10). Thêm toàn bộ phần mới của bộ 07/10 và điều chỉnh để tương thích với mô hình rảnh tay. Mã được đánh lại; bảng đối chiếu ở §0.3.

Không có code, benchmark hay báo giá mới trong lần hợp nhất này.

### 0.1. Quyết định chung v1.2

| ID | Quyết định | Nguồn | Trạng thái |
| --- | --- | --- | --- |
| D01 | Paper-first: học sinh tự làm trên giấy; AI không chấm liên tục trong lúc viết | Cả hai bộ | Baseline |
| D02 | Kiểm tra bài và Trợ giúp kích hoạt **bằng giọng nói**; thẻ lệnh in sẵn làm dự phòng | 06/10 | Baseline |
| D03 | **Không chạm máy trong buổi học**, kể cả bước chụp đề đầu buổi. Chỉ chạm máy khi setup trước buổi học | 06/10 | Baseline |
| D04 | MVP gửi **ảnh vùng giấy đã cắt** lên server khi có trigger; frame có người bị chặn trên máy | 06/10 | Baseline |
| D05 | Model vision thương mại qua adapter; hệ thống tự chọn model; model mới phải qua bộ replay | 06/10 | Baseline |
| D06 | Nhận dạng chữ trên điện thoại là R&D dài hạn, không thuộc MVP | 06/10 | Baseline |
| D07 | Ngừng viết khoảng 60 giây: hỏi một lần bằng câu mẫu tại máy, không gọi AI cloud | Cả hai bộ | Baseline |
| D08 | Tách trạng thái đáp án và cách làm; không báo điều chưa có bằng chứng | Cả hai bộ | Baseline |
| D09 | History theo kỹ năng; ba lần trợ giúp không khóa giúp đỡ, không gắn nhãn lười | Cả hai bộ | Baseline |
| D10 | **Chỉ Toán lớp 6**; chỉ cam kết dạng bài, bộ chấm và thiết bị đã kiểm chứng | 07/10, Sơn chốt | Baseline |
| D11 | **Buổi học theo tờ đề in.** Đầu buổi chụp đủ các trang đề và xác nhận danh sách câu/ý | 07/10 | Baseline |
| D12 | Hệ thống biết bộ đề sau khi chụp; không bắt nhập đề trước, không bắt QR | 07/10 | Baseline |
| D13 | Kho kiến thức Toán lớp 6 kèm **phạm vi đã học có version**; gợi ý không dùng kiến thức hay phương pháp chưa học | 07/10 | Baseline |
| D14 | Buổi học 30–45 phút, mục tiêu hoàn thành bộ đề; hết giờ thì lưu tiến độ để học tiếp | 07/10 | Baseline |
| D15 | Trẻ chọn câu đang làm, không cần theo thứ tự, bằng giọng nói ("câu 3") hoặc khoanh số câu | 07/10 + 06/10 | Baseline |
| D16 | Tờ đề có hai nguồn: **đề in do giáo viên/phụ huynh chuẩn bị**, hoặc **phiếu bài hệ thống sinh theo lỗ hổng** (template + CAS) | 06/10 + 07/10 | Baseline |
| D17 | Phụ huynh xem **ảnh bàn học gần trực tiếp** theo yêu cầu; live video sau MVP | 06/10 | Baseline |
| D18 | **Miễn phí trong pilot**; kiểm chứng bằng đặt cọc; sau pilot là freemium | 06/10 | Baseline |
| D19 | Không bán/chia sẻ dữ liệu cá nhân; không quảng cáo tới trẻ | 06/10 | Baseline |
| D20 | Ảnh tự xóa sau 7 ngày hoặc theo cài đặt phụ huynh; hai loại đồng ý tách biệt | 06/10 | Baseline |
| D21 | AI chỉ trao đổi về bài học; có bộ lọc đầu ra | 06/10 | Baseline |
| D22 | Pilot tối đa 50 gia đình; **10 tuần từ kickoff đến go/no-go** | 06/10 | Baseline |
| D23 | Pilot trên **cả Android và iOS** | 06/10 | Baseline |
| D24 | Từ gọi là **"Cô ơi"** | 06/10 | Baseline |
| D25 | Người xác nhận phạm vi đã học: **giáo viên nếu có; nếu không, phụ huynh chọn theo mục lục SGK lớp 6** | Đề xuất v1.2 | **Chờ Sơn chốt** |

### 0.2. Nội dung bị thay thế khi hợp nhất

| Nội dung bộ 07/10 | Thay bằng (giữ quyết định 06/10) |
| --- | --- |
| Nút Kiểm tra/Trợ giúp; chọn vùng và xác nhận chữ trên màn hình | Lệnh giọng nói, thẻ lệnh, xác nhận bằng giọng nói (D02, D03) |
| OCR trên máy, API chỉ nhận JSON, cấm ảnh lên cloud | Ảnh vùng giấy đã cắt lên server; OCR trên máy là R&D (D04, D06) |
| Live View qua WebRTC | Ảnh gần trực tiếp (D17) |
| Pilot 30 ngày, giá 200–400k/tháng | Miễn phí, 10 tuần, đặt cọc (D18, D22) |
| Gate G0–G5 | Cổng S, G0, G1, G2 và go/no-go (§11) |
| Ví dụ gợi ý "trừ 5 ở cả hai vế" | Cách nói SGK lớp 6 ("tìm số hạng chưa biết") |

| Nội dung bộ 06/10 | Thay bằng |
| --- | --- |
| Lớp 6–7 | Chỉ lớp 6 (D10) |
| Buổi học tự do, trẻ làm bài bất kỳ trong vở | Buổi học theo tờ đề, có chụp đề và xác nhận đầu buổi (D11) |
| Phiếu bài hệ thống là nguồn bài tập duy nhất ngoài vở | Thêm đề in của giáo viên/phụ huynh (D16) |

### 0.3. Bảng đối chiếu mã

**Quyết định**

| v1.2 | Bộ 06/10 | Bộ 07/10 |
| --- | --- | --- |
| D01 | D01 | D01 |
| D02 | D02 + D08 (thẻ lệnh) | D02 (bị thay) |
| D03 | D03 | — |
| D04 | D04 | D04, D05 (bị thay) |
| D05 | D05 | — |
| D06 | D06 | D06 (đổi vai trò thành R&D) |
| D07 | D07 | D03 |
| D08 | D09 | D09 |
| D09 | D10 | D08 |
| D10 | D11 (lớp 6–7 → lớp 6) | D11 |
| D11 | — | D14 |
| D12 | — | D15 |
| D13 | — | D16 |
| D14 | — | D17 |
| D15 | — | D18 |
| D16 | D12 | — |
| D17 | D13 | D10 (bị thay) |
| D18 | D14 | D13 (bị thay) |
| D19 | D15 | — |
| D20 | D16 | — |
| D21 | D17 | — |
| D22 | D18 | D13 (bị thay) |
| D23 | D19 | D07 (một phần) |
| D24 | D20 | — |
| — | — | D12 (sizing) → Technical HLD Phụ lục A |

**Use case:** U01–U24 ở §5.3 thay toàn bộ U01–U17 (06/10) và U01–U18 (07/10); cột "Nguồn" trong bảng ghi mã cũ.  
**Acceptance:** A01–A42 ở Technical HLD §15 thay A01–A31 (06/10) và A01–A30 (07/10).  
**Scenario SC-xx** trong context v0.3 **không dùng nữa**; context v0.4 tham chiếu trực tiếp mã A.

### 0.4. Cập nhật sau baseline (08/10/2026)

Quyết định Sơn đưa ra sau khi phát hành v1.2. Chưa đánh lại mã D; khi hợp nhất bản sau thì đưa vào bảng §0.1.

| Chủ đề | Quyết định | Ghi chú |
| --- | --- | --- |
| Khung giờ dùng app | Không giới hạn; học bất kỳ lúc nào | Camera vẫn chỉ chạy trong buổi học |
| Kickoff | 08/10/2026 | Cổng S 14/10; G0 11/11; G1 18/11; G2 ≈ 22/11; go/no-go 16/12 |
| Nhà cung cấp AI | Anthropic (Claude) cho tutor LLM và nhận dạng ảnh, qua adapter. Model chọn sau spike US-001, so sánh Opus 5.5, Sonnet 5.5, Haiku 5.5 trên cùng bộ ảnh | Chưa dùng với dữ liệu trẻ thật cho tới khi xác minh điều khoản cho người dưới 18 tuổi. ASR/TTS chưa chọn |
| Dạng bài | **Toàn bộ Toán lớp 6 học kỳ 1, gồm cả hình học**; thay "2–3 dạng bài" của D10 và bỏ "hình học" khỏi danh sách ngoài MVP | Bộ SGK: **Cánh diều**. Rủi ro trượt G0 tăng (RAID R-003) |
| Tờ đề trong MVP | **Tối đa 1 trang đề.** Trẻ làm trong vở; trước mỗi câu ghi số câu ở lề trái, ví dụ `1) 5x + 3 = 28` | Thay "giới hạn số trang/câu" ở §14. Chọn câu dùng **cả hai**: hệ thống đọc số câu ghi trong vở; lệnh "Câu N" (D15) vẫn dùng khi số không rõ. Bỏ "tự nhận biết câu đang làm" khỏi danh sách ngoài MVP |
| Stack | Backend Python + FastAPI; web phụ huynh/giáo viên React + TypeScript; app học sinh Flutter + native (giữ Technical HLD §9) | |
| Ngưỡng cổng S | Model tốt nhất: kết luận lỗi đúng ≥ 75% trên bài làm; đủ câu/ý đề in ≥ 95% trước xác nhận. "Cô ơi": nhận đúng ≥ 80%, kích hoạt nhầm ≤ 3 lần/giờ trên mỗi nền tảng | Con số do Claude đề xuất, Sơn chọn; chưa có căn cứ đo |
| Danh sách máy | **iOS 18.7 trở lên, Android 15 trở lên**; test thật 2–3 máy mỗi nền tảng trong tuần 2–5 | RAM/camera tối thiểu chưa đặt |

## 1. Tầm nhìn và giá trị

AI Study Companion giúp học sinh **lớp 6** tự làm bài Toán trên giấy với smartphone đặt trên giá đỡ. Mỗi buổi học là một **tờ đề**: đề ôn tuần của giáo viên, đề phụ huynh in, hoặc phiếu luyện hệ thống sinh theo lỗ hổng. Trẻ đặt đề dưới camera, chọn câu, tự làm, và **gọi cô bằng giọng nói** khi muốn kiểm tra hoặc cần gợi ý. Cô chỉ gợi ý bằng kiến thức trẻ đã học. Phụ huynh biết con làm được bao nhiêu phần của đề, hổng chỗ nào, và có sẵn phiếu để con luyện.

- Học sinh: "Con cứ thử tự làm. Khi cần, con gọi cô."
- Phụ huynh: "Con làm hết đề ôn mà không cần bố mẹ ngồi kèm. Bố mẹ biết con hổng chỗ nào."

Không hứa tăng điểm, đọc mọi kiểu chữ, chấm mọi dạng bài lớp 6, hay thay thế giáo viên.

## 2. Khách hàng và người dùng

| Persona | Nhu cầu | Giá trị cần kiểm chứng |
| --- | --- | --- |
| Học sinh lớp 6 | Làm đề trên giấy, được giúp khi gọi, không bị cho đáp án | Gọi cô tự nhiên; không chỉnh máy; làm tiếp được sau gợi ý |
| Phụ huynh | Không phải kèm; biết tiến độ thật; có bài cho con luyện | Báo cáo đáng tin; phiếu bài hữu ích; kiểm soát camera |
| Giáo viên của lớp (tùy chọn) | Học sinh làm đề ôn ở nhà có hỗ trợ đúng phương pháp đã dạy | Gợi ý không dạy trước, không dạy khác cách |
| Người phụ trách nội dung Toán (đội dự án) | Kho kiến thức và gợi ý đúng chương trình | Duyệt template, phạm vi, phương pháp |
| Đội vận hành | Kiểm soát chất lượng, sự cố, chi phí | Trace được lỗi; không lẫn dữ liệu |

**Vai trò giáo viên trong mô hình B2C (D25, chờ chốt):** sản phẩm bán cho phụ huynh. Giáo viên của lớp **không bắt buộc** phải dùng hệ thống. Đề xuất:

- Nếu có giáo viên tham gia (qua giới thiệu hoặc thử B2B2C), giáo viên chuẩn bị đề và xác nhận phạm vi đã dạy.
- Nếu không, phụ huynh chọn bộ SGK và tick các bài đã học trong mục lục lớp 6 trên web; đề là đề giáo viên giao về nhà hoặc phiếu hệ thống.
- Trong pilot, giáo viên đồng hành của dự án hỗ trợ phụ huynh thiết lập phạm vi.

Thị trường đầu: gia đình tại Việt Nam có smartphone tương thích và con học lớp 6. Chưa có TAM/SAM/SOM hay số liệu willingness-to-pay.

## 3. Định vị và khác biệt

| Đối thủ | Điểm yếu cần kiểm chứng | Khác biệt của chúng ta |
| --- | --- | --- |
| Trợ lý AI đa năng có camera | Phải cầm máy chụp; dễ đưa đáp án; không biết con đã học đến đâu; không có báo cáo | Rảnh tay; chấm từng dòng; gợi ý trong phạm vi đã học; báo cáo theo tờ đề |
| App giải bài | Trẻ lấy đáp án ngay | Không đưa đáp án; gợi ý từng bậc |
| Gia sư, học thêm | Chi phí theo giờ | Hỗ trợ làm đề ôn mỗi tối |
| App luyện bài trên màn hình | Không dùng được đề giấy giáo viên giao | Dùng chính tờ đề giáo viên giao |
| Thiết bị AI chuyên dụng | Phải mua phần cứng | Smartphone sẵn có và giá đỡ |

**Bốn trụ khác biệt:**

1. **Rảnh tay như có cô ngồi cạnh.**
2. **Chấm cách làm, không chỉ đáp án.**
3. **Đúng phần đã học:** gợi ý không dạy trước, không dạy khác phương pháp.
4. **Vòng lặp phụ huynh:** báo cáo theo tờ đề → lỗ hổng → phiếu luyện → con làm → hồ sơ cập nhật.

Moat tiềm năng: kho kiến thức và template gợi ý Toán lớp 6 đã kiểm chứng; bộ replay bài làm thật; dữ liệu lỗi kỹ năng có đồng ý; niềm tin của phụ huynh.

## 4. Nguyên tắc sản phẩm

1. Trẻ tự làm trước; AI im lặng khi chưa được gọi.
2. Không bắt trẻ chạm máy trong buổi học, kể cả bước chụp đề.
3. Ngừng viết một phút chỉ là tín hiệu để hỏi một lần.
4. Không đọc rõ thì hỏi lại bằng giọng nói; không chấm sai vì camera hoặc nhận dạng.
5. Gợi ý nhỏ nhất đủ để trẻ làm tiếp; không tự đưa lời giải đầy đủ.
6. **Gợi ý chỉ dùng kiến thức và phương pháp trong phạm vi đã học.** Đã học không có nghĩa là đã thành thạo.
7. Ngôn ngữ gợi ý theo SGK lớp 6.
8. AI chỉ nói về bài học.
9. History để cá nhân hóa, không để từ chối giúp.
10. Đáp án đúng không chứng minh cách làm đúng.
11. Câu khó, ngoài phạm vi hay chưa hỗ trợ **vẫn nằm trong tờ đề**; không bị bỏ đi để số liệu đẹp.
12. Không ép trẻ làm thêm hay đọc đáp án để "hoàn thành" đề.
13. Camera chỉ chạy trong buổi học; máy con báo khi phụ huynh đang xem.
14. Báo cáo chỉ nói điều có bằng chứng.

## 5. Hành trình và use case

### 5.1. Hành trình chính

**Trước buổi học (được chạm máy):** phụ huynh setup lần đầu (liên kết tài khoản, đồng ý, phạm vi đã học). Mỗi tối trẻ mở app, cắm sạc, đặt máy lên giá.

**Trong buổi học (không chạm máy):**

1. App thấy bàn học sẵn sàng → chào → "Con đặt trang đề đầu tiên dưới camera nhé."
2. Trẻ đặt từng trang đề; app tự chụp khi trang ổn định; trẻ lật trang và nói "Hết rồi ạ" khi xong.
3. Cô đọc lại: "Cô thấy 5 câu, 8 ý. Đúng không con?" Trẻ trả lời "Đúng rồi ạ" hoặc "Thiếu câu 4". Chữ đề không rõ thì cô hỏi lại.
4. Hệ thống kiểm tra phạm vi; câu ngoài phạm vi hoặc chưa hỗ trợ được báo trước: "Câu 5 có hình vẽ, cô chưa chấm được, con cứ làm nhé."
5. Trẻ nói "Câu 3" rồi tự làm, trên đề hoặc vở.
6. "Cô ơi, kiểm tra giúp con" / "Cô ơi, con không biết làm" → app tự chụp lời giải → cô phản hồi bằng giọng nói.
7. Trẻ sửa, gọi kiểm tra lại, chuyển câu khác.
8. Hết 30–45 phút, hoặc trẻ nói "Con học xong rồi": lưu tiến độ; cô nói còn bao nhiêu câu để buổi sau.
9. Phụ huynh nhận báo cáo.

**Buổi sau:** cô hỏi "Mình làm tiếp đề hôm qua nhé?"; trẻ đặt lại đề; hệ thống khôi phục tiến độ.

### 5.2. Lệnh giọng nói

| Ý định | Ví dụ câu nói | Thẻ lệnh |
| --- | --- | --- |
| Xong phần chụp đề | "Hết rồi ạ" | XONG |
| Xác nhận bộ đề | "Đúng rồi ạ" / "Thiếu câu 4" | — |
| Chọn câu | "Câu 3", "Câu 2 ý b", hoặc khoanh số câu trên giấy | — |
| Kiểm tra bài | "Cô ơi, kiểm tra giúp con" | KIỂM TRA |
| Xin trợ giúp | "Cô ơi, con không biết làm" | GIÚP CON |
| Sang câu khác | "Sang câu tiếp" | — |
| Nghe lại | "Cô nhắc lại" | — |
| Dừng cô đang nói | "Cô ơi, dừng" | — |
| Tạm dừng / tiếp tục | "Cô ơi, tạm dừng" / "Học tiếp" | — |
| Chấm phiếu bài hệ thống | "Cô chấm giúp con" | — |
| Kết thúc | "Con học xong rồi" | XONG |

Từ gọi là **"Cô ơi"** (D24). Vì trẻ hay nói cụm này với người khác, phải đo kích hoạt nhầm trong spike và pilot.

### 5.3. Use case

**Học sinh**

| ID | Use case | Hành vi và kết quả | Nguồn |
| --- | --- | --- | --- |
| U01 | Đặt máy, tự bắt đầu | App thấy bàn học sẵn sàng thì chào và bắt đầu; không bấm gì | 06/10 U01 |
| U02 | Chụp đề đầu buổi | Đặt từng trang; app tự chụp; cô đọc lại số câu/ý để con xác nhận bằng giọng nói; chụp lại phần thiếu | 07/10 U13, U01 |
| U03 | Chọn câu đang làm | "Câu 3" hoặc khoanh số câu; làm không theo thứ tự; phản hồi gắn đúng câu/ý | 07/10 U14 |
| U04 | Tự làm, tự sửa trước khi gọi | AI im lặng; chưa ghi kết quả xác nhận | 06/10 U02 |
| U05 | Gọi cô kiểm tra | Đọc lời giải của câu đang chọn; đúng thì xác nhận; sai thì chỉ dòng sai gốc | 06/10 U03 |
| U06 | Gọi cô trợ giúp | Gợi ý theo history và trong phạm vi đã học | 06/10 U05 |
| U07 | Nhận gợi ý rồi làm tiếp | Dừng giải thích; không giải nốt | 06/10 U06 |
| U08 | Sửa rồi kiểm tra lại | Dùng đúng phiên bản bài mới | 06/10 U08 |
| U09 | Hết giờ hoặc kết thúc sớm | Lưu tiến độ; nói còn lại bao nhiêu; không ép làm tiếp | 07/10 U17 |
| U10 | Học tiếp bộ đề | Khôi phục bộ đề và tiến độ; xác nhận trang/câu hiện tại; không phát phản hồi cũ | 07/10 U18 |
| U11 | Giơ thẻ lệnh | Dùng khi phòng ồn hoặc con ngại nói | 06/10 U15 |

**Hệ thống tự xử lý**

| ID | Use case | Hành vi và kết quả | Nguồn |
| --- | --- | --- | --- |
| U12 | Ngừng viết khoảng 1 phút | Hỏi một lần tại máy; không gọi AI | 06/10 U04 |
| U13 | Chữ/ảnh không rõ | Hỏi lại bằng giọng nói, nhờ bỏ tay ra hoặc viết rõ; không yêu cầu chạm máy | 06/10 U07 |
| U14 | Xin giúp nhiều lần | Xem lại tiến triển và kiến thức nền; không khóa | 06/10 U09 |
| U15 | Đổi trang hoặc mất mạng | Báo trạng thái bằng giọng nói; không phát phản hồi sang câu khác | 06/10 U10 |
| U16 | Vở/đề bị lệch | Tự bù lệch nhỏ; lệch lớn nhắc xê dịch giấy, không chỉnh máy | 06/10 U11 |
| U17 | Câu cần kiến thức chưa học | Báo "cần xem lại phạm vi"; không gợi ý vượt phạm vi; không chấm sai | 07/10 U15 |
| U18 | Câu chưa hỗ trợ (hình vẽ, bảng…) | Giữ "chưa xác nhận"; vẫn tính trong tổng số câu của đề | 07/10 U16 |

**Phụ huynh và giáo viên**

| ID | Use case | Hành vi và kết quả | Nguồn |
| --- | --- | --- | --- |
| U19 | Liên kết tài khoản và đồng ý | Chưa có đồng ý loại 1 thì app không bật camera/micro | 06/10 U16 |
| U20 | Xác nhận phạm vi đã học | Giáo viên hoặc phụ huynh chọn bộ SGK, tick bài đã học; mỗi lần đổi tạo version | 07/10 D16 |
| U21 | Xem con học từ xa | Ảnh gần trực tiếp; máy con báo đang được xem | 06/10 U12 |
| U22 | Đọc báo cáo | Theo tờ đề: phần đã xác nhận, cần sửa, chưa xác nhận, còn lại | 06/10 U13, 07/10 U12 |
| U23 | In phiếu bài theo lỗ hổng | Phiếu hệ thống trở thành tờ đề cho buổi sau | 06/10 U14 |
| U24 | Xem, xuất, xóa dữ liệu | Chỉnh thời hạn lưu ảnh; rút đồng ý loại 2 | 06/10 U17 |

### 5.4. Ví dụ sư phạm (lớp 6)

Câu 3: tìm x biết 3x + 5 = 20. Trẻ viết 3x = 25 rồi x = 25/3, sau đó nói "Cô ơi, kiểm tra".

Cô nhắm vào dòng 2: "Con xem lại dòng thứ hai nhé. Muốn tìm số hạng chưa biết thì con làm phép tính gì?" Không coi phép chia ở dòng 3 là lỗi gốc mới, không đọc x = 5.

Nếu chưa chắc trẻ viết 15 hay 18, cô hỏi: "Dòng hai con viết mười lăm hay mười tám?" Nếu đáp án đúng nhưng thiếu dòng giữa, câu đó ghi "đáp án đúng, cách làm chưa xác nhận".

Nếu một câu khác cần kiến thức chưa có trong phạm vi đã học, cô không giảng bài mới: "Câu này cô chưa gợi ý được, con hỏi thầy cô hoặc bố mẹ nhé." Câu đó vẫn nằm trong đề, trạng thái "cần xem lại phạm vi".

### 5.5. Chính sách gợi ý

| Bằng chứng | Hướng hỗ trợ |
| --- | --- |
| Đã tự làm đúng dạng tương đương | Nhắc nguyên lý, mời thử bước đầu |
| Kiến thức nền đã học nhưng chưa vững | Giải thích khái niệm trong phạm vi đã học |
| Lặp lỗi cùng kỹ năng | Nhắm vào kiến thức gốc |
| Nhiều gợi ý chưa tiến triển | Đổi cách giải thích, ví dụ đơn giản hơn |
| Xin đáp án liên tục | Mời làm một bước; vẫn giữ đường giúp |
| Cần kiến thức chưa học | Không gợi ý vượt phạm vi; báo cần xem lại |

L1 nhắc nhẹ, L2 khái niệm, L3 một bước trung gian (chỉ khi trẻ chủ động hỏi thêm). Không tăng mức chỉ vì hết giờ. Nhắc chỉnh giấy/camera không tính là gợi ý Toán. Gợi ý ghi theo episode.

## 6. Phạm vi MVP

| Nhóm | MVP pilot | Sau khi có bằng chứng |
| --- | --- | --- |
| Nội dung | Toán lớp 6; 2–3 dạng bài đã kiểm chứng; kho kiến thức lớp 6 theo một bộ SGK | Thêm dạng bài, thêm bộ SGK, lớp 7 |
| Buổi học | Chụp đề đầu buổi, xác nhận câu/ý, chọn câu, Kiểm tra/Trợ giúp, lưu và học tiếp | Tự nhận biết câu đang làm |
| Rảnh tay | Từ gọi "Cô ơi", lệnh giọng nói, tự chụp, tự bù lệch, thẻ lệnh | — |
| Phạm vi đã học | Phụ huynh hoặc giáo viên tick theo mục lục SGK trên web | Giao diện giáo viên cho cả lớp |
| Phụ huynh | Liên kết, đồng ý, báo cáo theo tờ đề, phiếu bài in, ảnh gần trực tiếp, quản lý dữ liệu | Live video |
| Thiết bị | Android và iOS, danh sách máy hỗ trợ, giá đỡ chuẩn | Mở rộng dòng máy |
| Nhận dạng | Model AI thương mại trên server | Nhận dạng trên máy (R&D) |

**Dạng bài lớp 6 ứng viên** (chốt cùng giáo viên ở tuần 1): tìm số hạng/thừa số chưa biết (dạng `ax + b = c`, `a(x + b) = c` với số tự nhiên, số nguyên); thứ tự thực hiện phép tính; phép tính phân số cơ bản.

**Ngoài MVP:** lớp 7 trở lên, môn khác, hình học, bài có bảng/hình cần đọc, LMS, giao bài cho cả lớp, avatar/3D, gamification, chấm điểm tập trung/cảm xúc, camera chạy ngầm, giải toàn bài tự động.

**Phụ kiện pilot:** giá đỡ đế nặng, bộ thẻ lệnh, hướng dẫn setup in.

## 7. Dữ liệu, quyền và niềm tin

- Ảnh chỉ gửi khi: chụp đề đầu buổi, có lệnh Kiểm tra/Trợ giúp, chụp phiếu bài, hoặc phụ huynh đang xem.
- Frame có người bị chặn trên máy và không rời máy. Chỉ gửi vùng giấy đã cắt.
- Ảnh tự xóa sau 7 ngày hoặc theo cài đặt phụ huynh. **Nội dung đề đã xác nhận (text), tiến độ và kết quả** lưu trong DB của hệ thống để học tiếp và báo cáo.
- Nhà cung cấp AI có cam kết không huấn luyện trên dữ liệu và lưu tối thiểu; có hồ sơ chuyển dữ liệu ra nước ngoài.
- Micro chỉ nhận diện "Cô ơi" trên máy; âm thanh chỉ gửi lên server sau từ gọi, hoặc trong khoảng trả lời câu hỏi xác nhận của cô.
- Hai loại đồng ý: (1) dùng dịch vụ, bắt buộc; (2) cho dùng ảnh để cải thiện hệ thống, tùy chọn, rút lại được.
- Phạm vi đã học là dữ liệu học tập của trẻ, chỉ phụ huynh, giáo viên được cấp quyền và hệ thống truy cập.
- Phụ huynh xem, xuất, xóa dữ liệu của con (U24).
- Không bán/chia sẻ dữ liệu cá nhân; không quảng cáo tới trẻ.

Đây là yêu cầu thiết kế, không phải ý kiến pháp lý. Cần tư vấn pháp lý trước pilot.

## 8. KPI

### 8.1. Kết quả theo câu/ý

Mỗi câu/ý có trạng thái: chưa làm · đang làm · trẻ báo xong · cần sửa · chưa xác nhận · đã xác nhận đúng. Thêm cờ: cần xem lại phạm vi, chưa hỗ trợ. "Trẻ báo xong" khác "đã xác nhận đúng".

Câu/ý đã xác nhận đúng chia thành ba nhóm loại trừ nhau:

1. Đúng ở lần kiểm tra đầu, chưa nhận gợi ý.
2. Đúng sau phản hồi kiểm tra, chưa nhận gợi ý bổ sung.
3. Đúng sau trợ giúp.

Còn lại là nhóm 4: chưa hoàn thành hoặc chưa xác nhận (gồm câu chưa hỗ trợ và câu cần xem lại phạm vi).

**North Star:** tỷ lệ câu/ý nhóm 1 trên tổng câu/ý của các đề đã làm. Báo song song tỷ lệ nhóm 4.

### 8.2. Chất lượng và trải nghiệm

| KPI | Định nghĩa | Mục tiêu pilot |
| --- | --- | --- |
| Error precision | Kết luận lỗi đúng / tổng kết luận lỗi | > 90% |
| Error recall | Lỗi phát hiện / lỗi ground truth trên evidence đủ | ≥ 90% |
| Hint → Recovery | Episode dẫn tới tiến triển đúng / episode đánh giá được | > 70% |
| Kết luận sai khi thiếu bằng chứng | Kết luận Toán sai trên mẫu evidence không đủ | < 1% |
| Gợi ý lộ đáp án | Gợi ý L1/L2 chứa đáp án cuối | < 5% |
| **Tuân thủ phạm vi** | Gợi ý dùng kiến thức/phương pháp ngoài phạm vi đã học | 0 trên tập test; theo dõi thực tế |
| **Đủ câu/ý của đề** | Câu/ý trong bộ đề đã xác nhận / câu/ý trên đề thật | 100% sau xác nhận; đo riêng lỗi bỏ câu trước xác nhận |
| **Đúng nội dung đề** | Text/công thức thiết yếu của đề đúng sau xác nhận | ≥ 98% |
| **Thời gian chụp đề** | Bắt đầu chụp → bộ đề sẵn sàng (đề 2 trang) | p95 ≤ 60 giây (đề xuất) |
| **Gánh nặng xác nhận** | Số lần chụp lại/sửa ở bước chụp đề; số buổi cần người lớn giúp | Đo baseline trong alpha |
| Buổi phải chạm máy | Buổi có ít nhất một lần trẻ phải chạm máy, kể cả bước chụp đề | ≤ 10% |
| Buổi phải chỉnh lại máy | — | < 10% |
| Lệnh hiểu đúng lần đầu | — | ≥ 90% |
| Kích hoạt nhầm | — | < 1 lần/giờ |
| Âm báo đã nghe lệnh | Kết thúc lệnh → âm báo | p95 ≤ 1 giây |
| Bắt đầu câu phản hồi | Kết thúc lệnh → câu phản hồi | p95 ≤ 5 giây |

Precision, recall và tuân thủ phạm vi phải có nhãn của giáo viên Toán.

### 8.3. KPI tờ đề, phụ huynh và kinh doanh

- **Hoàn thành có xác nhận:** câu/ý đã xác nhận đúng / tổng câu/ý bắt buộc của đề (câu chưa hỗ trợ vẫn trong mẫu số).
- **Hoàn thành cả đề:** số đề có mọi câu/ý đã xác nhận / tổng đề. Không gọi chỉ số này là "tiến bộ học tập".
- **Học tiếp thành công:** trẻ quay lại và làm phần còn lại của đề.
- Activation, số buổi/tuần, retention theo tuần, tỷ lệ mở báo cáo, tỷ lệ phiếu bài được làm, tỷ lệ đặt cọc, chi phí/học sinh/tháng, thời gian hỗ trợ.

## 9. Mô hình kinh doanh

### 9.1. Chiến lược

- **Pilot:** miễn phí, tối đa 50 gia đình. Cuối pilot mời đặt cọc thật cho gói sau pilot, có cam kết hoàn tiền nếu không ra mắt.
- **Sau pilot:** freemium.

| Miễn phí (giả thuyết) | Trả phí (giả thuyết) |
| --- | --- |
| Giới hạn số buổi hoặc số đề mỗi tuần | Không giới hạn |
| Kiểm tra bài, gợi ý L1–L2 | Toàn bộ mức gợi ý |
| Báo cáo sau buổi | Báo cáo tuần/tháng, lỗ hổng chi tiết |
| — | Phiếu bài in theo lỗ hổng |
| Ảnh gần trực tiếp giới hạn | Không giới hạn; live video sau này |

Giới hạn gói miễn phí không được chặn trợ giúp giữa một câu đang làm. Giá 200.000–400.000 đồng/tháng vẫn là giả thuyết.

Hướng thu tiền khác cần kiểm chứng: trường hoặc trung tâm dùng để giao đề về nhà (B2B2C), nơi giáo viên xác nhận phạm vi cho cả lớp.

### 9.2. Unit economics

`V = chụp đề và kiểm tra phạm vi + vision + tutor + ASR + TTS + lưu ảnh 7 ngày + parent view + infra biến đổi + thanh toán + hỗ trợ biến đổi`

- **Chi phí mỗi lượt học (run)** = chụp đề/xác nhận/phạm vi (hoặc khôi phục khi học tiếp) + Kiểm tra/Trợ giúp + báo cáo/voice/parent view/hỗ trợ.
- **Chi phí mỗi tờ đề** = tổng các lượt học của đề đó.
- Vision: số trang đề + số lần Kiểm tra/Trợ giúp/chụp phiếu × số ảnh × đơn giá.
- ASR: đoạn sau từ gọi và câu trả lời xác nhận. TTS: số giây cô nói.

`Contribution = P_net − V`; P_net phải trừ phí nền tảng 15–30% nếu thu qua App Store/Google Play. `Break-even = ceil(chi phí cố định tháng / Contribution)`, chỉ có nghĩa khi Contribution > 0.

**Pilot:** chi phí AI ước tính vài triệu đến khoảng 15 triệu VND/tháng cho 50 gia đình (chưa có báo giá). Pilot dùng model chất lượng tốt nhất.

### 9.3. Kịch bản

| Kịch bản | Giá ròng | Mức sử dụng | Dữ liệu cần |
| --- | --- | --- | --- |
| Thận trọng | Đặt cọc thấp | Đề nhiều trang, nhiều lần chụp lại | Chi phí p95 mỗi đề, người dùng nặng |
| Cơ sở | Giá pilot chấp nhận | Trung vị đo được | Cohort thực |
| Lạc quan | Retention và đặt cọc tốt | Template/cache hiệu quả | Bằng chứng từ pilot |

## 10. Go-to-market

- Tuyển gia đình có con học lớp 6 qua nhóm phụ huynh, giáo viên giới thiệu và người quen; ít nhất một phần là người không quen.
- Ưu tiên gia đình có con được giao đề ôn giấy về nhà; nếu không, dùng phiếu hệ thống.
- Onboarding qua gọi video 15 phút: đặt máy, cắm sạc, bật Không làm phiền, tick phạm vi đã học, thử chụp đề và lệnh giọng nói.
- Chưa có CAC. Mỗi thử nghiệm kênh có giới hạn ngân sách và theo dõi cohort.

## 11. Pilot và lộ trình 10 tuần

10 tuần **từ kickoff đến buổi quyết định go/no-go**, trên cả Android và iOS (D22, D23).

**Nguồn chuẩn:** các cổng và bảng go/no-go ở mục này là bản gốc. Trang Kế hoạch Pilot phản chiếu cùng nội dung; khi đổi ngưỡng phải sửa cả hai.

| Tuần | Việc chính | Cổng |
| --- | --- | --- |
| 1 | Spike: model đọc chữ viết tay trẻ (100–200 mẫu) và **đề in lớp 6 (20–30 tờ thật)**; từ gọi "Cô ơi" trên Android và iPhone; chọn bộ SGK, lập mục lục kỹ năng lớp 6; pháp lý; giáo viên; chốt dạng bài | **S** cuối tuần 1 |
| 2–5 | Vertical slice trên cả hai nền tảng: chụp đề, xác nhận, phạm vi, chọn câu, Kiểm tra/Trợ giúp, lưu và học tiếp, báo cáo, phiếu bài, web phụ huynh; phát hành nội bộ | **G0** cuối tuần 5 |
| 6 | Alpha 5 gia đình, có cả Android và iOS | **G1** cuối tuần 6 |
| 7–10 | Pilot 15 → 50 gia đình; phiếu bài; phỏng vấn hằng tuần; mời đặt cọc cuối tuần 10 | **G2** giữa tuần 7 |
| Cuối tuần 10 | Quyết định go/no-go | §11.2 |

**Đánh đổi:** gia đình vào pilot dùng khoảng 3–4 tuần, chưa đủ kết luận về retention dài hạn. Bước chụp đề và phạm vi đã học làm tăng khối lượng tuần 2–5; nếu G0 trễ, thu hẹp còn một dạng bài trước khi bỏ tính năng.

**Nguồn lực tối thiểu:** 3 kỹ sư (mobile và voice cho Android và iOS; backend và AI; fullstack cho web phụ huynh, phạm vi đã học, báo cáo, phiếu bài), 1 giáo viên Toán lớp 6 bán thời gian (gán nhãn, duyệt template, lập mục lục kỹ năng), Sơn làm product và vận hành. Cân nhắc thêm một kỹ sư mobile bán thời gian cho iOS.

### 11.1. Các cổng

**S — Spike đạt (cuối tuần 1)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Model vision đọc đúng từng dòng bài làm của trẻ | Đủ để đạt G0 sau tuning |
| Model đọc đúng đề in lớp 6 (câu/ý, công thức) | Đủ để đạt G0 sau tuning |
| Từ gọi "Cô ơi" nhận đúng giọng trẻ trên Android và iPhone | Có phương án khả thi |
| 2–3 dạng bài, bộ SGK, mục lục kỹ năng lớp 6 | Đã chốt |

**G0 — Replay và máy thật, trước khi phát cho gia đình (cuối tuần 5)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Error precision | ≥ 85% |
| Kết luận Toán từ ảnh xấu | ≈ 0 |
| Gợi ý L1/L2 lộ đáp án | < 5% |
| Gợi ý ngoài phạm vi đã học (tập test) | 0 |
| Đủ câu/ý của đề sau xác nhận (tập đề test) | 100% |
| Frame có người tới server | 0 |
| Đề/đáp án phiếu bài hệ thống sai | 0 |
| Lệnh giọng nói hiểu đúng (giọng trẻ, phòng thường) | ≥ 85% |
| Buổi test 45 phút, gồm chụp đề, không cần chạm máy | Đạt |
| Chạy ổn trên Android và iOS trong danh sách máy hỗ trợ | Đạt |

**G1 — Alpha 5 → mở 15 gia đình (cuối tuần 6)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Buổi học không crash hoặc mất dữ liệu | ≥ 95% |
| Gia đình setup lần đầu (gồm phạm vi đã học) trong 10 phút | ≥ 4/5 |
| Báo cáo khớp kiểm tra tay của giáo viên | 100% |
| Học tiếp đề dở dang khôi phục đúng tiến độ | 100% số lần thử |
| Sự cố dữ liệu hoặc quyền riêng tư | 0 |
| Gia đình alpha dùng mỗi nền tảng | ≥ 2 |

**G2 — 15 → mở 50 gia đình (giữa tuần 7)**

| Chỉ số | Ngưỡng |
| --- | --- |
| Lỗi blocker còn mở | 0 |
| Kích hoạt nhầm đo thực tế | < 1 lần/giờ |
| Đội hỗ trợ phản hồi trong ngày | ≥ 90% yêu cầu |

### 11.2. Go/no-go cuối tuần 10

Đánh giá trên các gia đình đã dùng ít nhất 3 tuần. Báo riêng Android và iOS.

| Nhóm | Chỉ số | Go | Xem lại | No-go |
| --- | --- | --- | --- | --- |
| Chất lượng AI | Phản hồi sai / tổng phản hồi | < 10% | 10–20% | > 20% |
| Rảnh tay | Buổi phải chạm hoặc chỉnh máy | < 10% | 10–25% | > 25% |
| Chụp đề | Buổi chụp đề xong mà không cần người lớn giúp | ≥ 80% | 60–80% | < 60% |
| Giọng nói | Gia đình phàn nàn về nhận lệnh | < 15% | 15–30% | > 30% |
| Sử dụng | Gia đình còn dùng ≥ 3 buổi/tuần ở tuần thứ 3 của họ | ≥ 50% | 30–50% | < 30% |
| Giá trị | Đồng ý "báo cáo giúp tôi biết con hổng chỗ nào" | ≥ 70% | 50–70% | < 50% |
| Giá trị | Phiếu bài được làm | ≥ 40% | 20–40% | < 20% |
| Kinh doanh | Đặt cọc thật | ≥ 20% | 10–20% | < 10% |
| Chi phí | Chi phí AI p95/học sinh/tháng | Đo được, có lộ trình giảm | Đo được | Không đo được |
| An toàn | Frame có người tới server; sự cố dữ liệu; gợi ý ngoài phạm vi bị phát | 0 | — | ≥ 1: dừng ngay |

**Quy tắc quyết định:**

1. **Go:** An toàn đạt, không có No-go, và ít nhất 7/9 chỉ số còn lại đạt Go. Mở rộng, bắt đầu freemium.
2. **Lặp lại:** không có No-go nhưng dưới 7 chỉ số đạt Go. Chạy thêm 4 tuần với cùng nhóm.
3. **Chuyển hướng:** No-go ở Giá trị hoặc Kinh doanh. Xem lại định vị hoặc thử B2B2C với giáo viên.
4. **Quay về replay:** No-go ở Chất lượng AI, Rảnh tay, Chụp đề hoặc Giọng nói. Không mở rộng.
5. **Dừng ngay:** bất kỳ vi phạm An toàn nào.

## 12. Rủi ro

| Rủi ro | Tác động | Xử lý |
| --- | --- | --- |
| Model đọc sai chữ viết tay hoặc đề in | Chấm sai, bỏ câu | Hỏi lại bằng giọng nói; xác nhận bộ đề; bộ replay |
| Chụp đề nhiều trang rườm rà | Trẻ nản ngay đầu buổi | Tự chụp khi trang ổn định; chỉ hỏi phần không chắc; đo gánh nặng xác nhận |
| Phụ huynh không biết con đã học đến đâu | Phạm vi sai, gợi ý dạy trước | Mục lục SGK dễ tick; giáo viên đồng hành hỗ trợ; mặc định không mở toàn lớp 6 |
| Đề giáo viên có dạng bài chưa hỗ trợ | Nhiều câu "chưa xác nhận" | Báo trước đầu buổi; ưu tiên phiếu hệ thống; mở rộng dạng bài theo dữ liệu |
| Không nhận giọng trẻ hoặc phòng ồn | Trẻ phải chạm máy | Spike tuần 1; thẻ lệnh |
| "Cô ơi" là cụm từ trẻ hay nói | Kích hoạt nhầm | Đo trong spike; xác nhận ý định ngắn |
| Làm cả Android và iOS trong 10 tuần | Trượt cổng | Flutter cho phần chung; cân nhắc thêm kỹ sư iOS; thu hẹp dạng bài trước |
| Giới hạn iOS | Không tự bật Không làm phiền; app phải ở foreground | Hướng dẫn bật Focus; giữ màn hình sáng |
| Máy nóng, hết pin | Gián đoạn | Cắm sạc trong checklist; đo 45–60 phút |
| Khác biệt yếu so với trợ lý AI miễn phí | Không ai trả tiền | Bốn trụ khác biệt §3; đo đặt cọc |
| Rủi ro pháp lý dữ liệu trẻ | Dừng dự án | Tư vấn pháp lý tuần 1; hai loại đồng ý |

## 13. Traceability

| Yêu cầu kinh doanh | Cơ chế kỹ thuật | Acceptance (Technical HLD §15) |
| --- | --- | --- |
| Chụp đủ đề, xác nhận câu/ý | Problem set manifest, xác nhận bằng giọng nói | A02–A04 |
| Rảnh tay suốt buổi | Từ gọi, lệnh giọng nói, tự chụp, tự bù lệch, thẻ lệnh | A01, A31–A35, A38 |
| Không chen ngang | Chỉ phản hồi khi được gọi; idle hỏi một lần | A05, A07 |
| Không chấm sai vì ảnh | Quality gate, UNKNOWN, hỏi lại | A11–A14 |
| Gợi ý trong phạm vi đã học | Learned scope, retrieval có lọc, output gate | A19–A21, A42 |
| Làm câu bất kỳ | Active item, revision | A18 |
| Lưu và học tiếp | SessionRun, ItemProgress, version | A23, A24 |
| Không bỏ câu khó | Unsupported/unverified trong mẫu số | A22 |
| Gợi ý cá nhân hóa, không chặn | History, episode | A08, A17 |
| Không gợi ý trùng hoặc lỗi thời | Idempotency, revision | A09, A10, A15, A16 |
| Quyền riêng tư | Chặn người, chỉ gửi vùng giấy, xóa 7 ngày | A27, A36, A39 |
| Đồng ý và quản lý dữ liệu | Consent gate, API xuất/xóa | A40, A41 |
| Báo cáo đáng tin | Event/outcome theo item | A26 |
| Phiếu bài đúng | Template + CAS | A37 |
| Phụ huynh xem từ xa | Token theo parent–student–session | A25 |

Đổi phạm vi dữ liệu, chặn cứng trợ giúp, tự bật camera, đưa lời giải đầy đủ, mở phạm vi gợi ý ra toàn lớp 6, hay đổi giá là thay đổi sản phẩm, cần Sơn quyết định và cập nhật cả hai HLD.

## 14. Còn mở

- **D25:** ai xác nhận phạm vi đã học trong mô hình B2C.
- 2–3 dạng bài lớp 6 và bộ SGK; giáo viên đồng hành.
- Danh sách máy Android và iOS hỗ trợ.
- Nhà cung cấp model vision/LLM/ASR/TTS và điều khoản lưu dữ liệu.
- Giới hạn số trang/câu mỗi tờ đề trong MVP.
- Nội dung hai loại đồng ý; thời hạn lưu ảnh cho bộ replay.
- Mức đặt cọc, giá gói sau pilot, kênh thanh toán.
- Ngân sách pilot.

**Khi bàn giao:** đọc cả hai HLD v1.2, kiểm tra repo, lập backlog theo tuần và cổng, báo trạng thái thật. Không khôi phục nội dung đã bị thay ở §0.2.
