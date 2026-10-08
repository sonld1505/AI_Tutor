# AI Study Companion — Project Context

> **Đã được thay thế** bởi [context v0.3](ai-study-companion-context-v0.3.md), [Business HLD v1.1](business-hld-v1.1.md) và [Technical HLD v1.1](technical-hld-v1.1.md) ngày 06/10/2026. Giữ lại để tra lịch sử; không dùng làm yêu cầu. Nội dung bên dưới là v0.2.1.

**Phiên bản:** 0.2.1 • **Ngày:** 05/10/2026 • **Chủ dự án:** Sơn • **Thay thế:** v0.1 (04/10/2026)

**v0.2.1:** chốt khối lớp MVP là **lớp 6–7**. Dạng bài cụ thể và bộ SGK vẫn chờ chốt.

## 0. Thay đổi so với v0.1

| # | Thay đổi | Trạng thái |
| --- | --- | --- |
| 1 | App là **lớp điều phối độc lập với model** (model-agnostic): dùng model AI thương mại, app lọc dữ liệu gửi lên và chọn lọc phản hồi trả về | Đã chốt |
| 2 | **Hệ thống tự chọn model**, người dùng cuối không chọn. Model chỉ được bật khi qua bộ replay đánh giá | Đề xuất, chờ chốt |
| 3 | Phụ huynh theo dõi từ xa, **không can thiệp** vào buổi học | Đã chốt |
| 4 | Parent View hai mức: **ảnh gần trực tiếp** (MVP) và live video (sau MVP) | Đề xuất, chờ chốt |
| 5 | Báo cáo lỗ hổng kiến thức kèm **phiếu bài tập in được**; chụp lại phiếu để chấm | Đã chốt |
| 6 | Không stream video cho AI; **chụp ảnh theo sự kiện** kèm chụp định kỳ thưa làm dự phòng | Đã chốt |
| 7 | Chỉ hỗ trợ **góc chụp từ trên xuống** cùng giá đỡ chuẩn; bỏ góc trực diện | Đề xuất, chờ chốt |
| 8 | MVP cho **học sinh lớp 6–7**; AI **chỉ trao đổi về bài học** | Đã chốt (v0.2.1); dạng bài và SGK chờ chốt |
| 9 | Chặn frame có khuôn mặt/người **ngay trên điện thoại**; chỉ gửi vùng giấy đã cắt | Đã chốt |
| 10 | Ảnh tự xóa sau **7 ngày** hoặc theo cài đặt của phụ huynh; dữ liệu học lưu trong DB của hệ thống, không lưu trên AI | Đã chốt |
| 11 | Hai loại đồng ý riêng: dùng dịch vụ / cho dùng ảnh để cải thiện hệ thống | Đề xuất, chờ chốt |
| 12 | Chiến lược: **miễn phí trong pilot → freemium**; không bán dữ liệu, không quảng cáo tới trẻ | Đã chốt hướng |
| 13 | Pilot tối đa **50 gia đình**, gồm chế độ bóng (shadow mode) và triển khai cuốn chiếu | Đề xuất, chờ chốt |
| 14 | Bộ replay có gán nhãn là **tài sản cốt lõi** và là cổng chất lượng trước pilot | Đề xuất, chờ chốt |

**Đính chính so với phân tích trước:** dạng `ax + b = c` (ví dụ `3x + 5 = 20`) vẫn xuất hiện ở lớp 6–7 dưới dạng bài "tìm x". Vì vậy các fixture vẫn dùng được cho lớp 6–7. Điểm cần đổi là **ngôn ngữ gợi ý**: phải khớp cách SGK của khối lớp đó diễn đạt (ví dụ "tìm số hạng chưa biết" thay vì "trừ cả hai vế"). Giáo viên đồng hành cần xác nhận.

## 1. Mục đích và trạng thái tài liệu

Tài liệu là context đầu vào cho Claude Code/Codex, đồng thời làm nền cho PRD, HLD và acceptance test.

Các ngưỡng độ chính xác, độ trễ, chi phí, giá bán, quy mô pilot và thời gian xây dựng là **mục tiêu/giả thuyết cần kiểm chứng**, chưa phải kết quả đo hay cam kết thương mại. Các ước tính chi phí là ước tính độ lớn, phải thay bằng số đo từ spike.

Chưa có repo hoặc code. Không suy diễn rằng tính năng đã được triển khai. Khi tiếp tục công việc, đọc repo, trạng thái Git và kết quả kiểm thử thực tế trước.

## 2. Bài toán kinh doanh và định vị

**Job-to-be-done:** Khi bố mẹ không thể ngồi cạnh con học, AI hỗ trợ con tự học và cho bố mẹ biết con đang hổng kiến thức ở đâu.

**Tên định vị:** AI Study Companion — AI đồng hành bên cạnh trẻ khi học.

- Với phụ huynh: "Bạn không phải ngồi kèm con mỗi tối. Bạn vẫn biết con học thế nào và cần luyện gì."
- Với học sinh: "Con cứ thử tự làm. Cô sẽ giúp khi con cần."
- Hình thức: smartphone sẵn có + giá đỡ chuẩn + vở, bút, sách giáo khoa, phiếu bài tập in.
- Người dùng: học sinh dùng app học; phụ huynh cho phép, theo dõi và là người trả tiền sau này.

**Vai trò của phụ huynh:** phụ huynh là mắt xích cho phép con dùng app. Phụ huynh theo dõi từ bất kỳ đâu qua ứng dụng song song, **không can thiệp** vào buổi học. Giá trị chính phụ huynh nhận được là **báo cáo lỗ hổng kiến thức** và **phiếu bài tập in** để con tự luyện.

**Giá trị cốt lõi không phải streaming liên tục.** Camera là sensor. AI hiểu đủ quá trình học, giữ im lặng khi trẻ đang tự giải hoặc tự sửa, và chỉ đưa mức hỗ trợ tối thiểu khi có bằng chứng đủ rõ.

### Chiến lược thị trường

- **Pilot:** miễn phí, tối đa 50 gia đình.
- **Sau pilot:** freemium. Phần lõi miễn phí có giới hạn chi phí; gói trả phí cho phụ huynh.
- **Dữ liệu:** dùng để cải thiện chính sách can thiệp, chấm điểm model và cá nhân hóa cho chính học sinh đó. **Không bán hoặc chia sẻ dữ liệu cá nhân cho bên thứ ba, không quảng cáo nhắm tới trẻ.**
- Kiểm chứng ý định trả tiền **ngay trong pilot** bằng đặt cọc, không đợi có nhiều người dùng.

## 3. Đối thủ và lợi thế cạnh tranh

Không cộng toàn bộ feature của đối thủ vào MVP. Bảng dưới kế thừa v0.1, chưa được kiểm chứng lại trên thị trường.

| Nhóm/sản phẩm | Điểm mạnh được nhắc tới | Khoảng trống cần kiểm chứng | Hướng áp dụng |
| --- | --- | --- | --- |
| **Trợ lý AI đa năng có camera và voice** (ChatGPT, Gemini…) | Miễn phí hoặc rẻ, model mạnh, cải thiện liên tục | Có xu hướng nói nhiều; không có báo cáo cho phụ huynh, không có chương trình VN, không có bộ nhớ học tập theo lỗi | Dùng chính các model này làm engine; cạnh tranh ở lớp điều phối |
| Chatbot/ứng dụng giải bài kiểu Photomath | Nhận ảnh, giải nhanh | Trẻ phải chủ động hỏi; dễ lấy đáp án | Quan sát quá trình; ưu tiên gợi ý |
| Vizo | Camera nhìn vở, Socratic tutoring | Trải nghiệm phụ huynh cần đối chiếu thêm | Hiểu từng bước, nhớ lịch sử |
| Dali/thiết bị học tập Trung Quốc | Theo dõi bàn học, quản lý từ xa | Chi phí thiết bị riêng | Parent View và báo cáo trên smartphone |
| 字闪闪 / ZiShanShan | Phản hồi trong lúc viết | Chủ yếu luyện chữ | Phản hồi theo hành động, áp dụng cho Toán |
| Zuoyebang AI伴学岛 | Cần phân tích sâu | Chưa đủ dữ liệu | Backlog nghiên cứu |

Nguồn tham khảo từ v0.1: https://askvizo.com/ • https://www.dalijiaoyu.com/zh/news/5 • https://apps.apple.com/cn/app/id1659411739 • https://zhongce.sina.com.cn/report/view/8319 • https://static.cninfo.com.cn/finalpage/2026-04-22/1225142158.PDF

**Lợi thế dự kiến nằm ở lớp điều phối, không nằm ở model:**

1. Chính sách can thiệp: khi nào im lặng, chờ, hỏi, gợi ý.
2. Bộ lọc dữ liệu đầu vào (ảnh đã cắt, ngữ cảnh bài) và bộ lọc đầu ra (chặn lộ đáp án, chặn nội dung ngoài lề).
3. **Bộ replay có gán nhãn về cách trẻ VN làm Toán** cùng bộ test chấm từng model. Đây là tài sản cốt lõi.
4. Student Memory, báo cáo lỗ hổng kiến thức và phiếu bài tập bám SGK.

Đây vẫn là giả thuyết, chưa phải lợi thế đã được bảo vệ.

## 4. Nguyên tắc sản phẩm

1. **Self-correction first:** cho trẻ thời gian tự phát hiện và sửa lỗi.
2. **Silence is a valid action:** im lặng là quyết định được ghi nhận và kiểm thử.
3. **Minimum effective intervention:** chỉ dùng mức hỗ trợ nhỏ nhất giúp trẻ tiếp tục.
4. **UNKNOWN ≠ WRONG:** chữ không rõ hoặc confidence thấp không phải bằng chứng trẻ sai.
5. **False intervention đắt hơn missed intervention:** ưu tiên precision để giữ niềm tin.
6. **Paper-first:** trẻ học trên giấy; voice là giao diện trợ giúp chính.
7. **Student memory không được nhắc bài trước.**
8. **Tách kỹ thuật khỏi sư phạm:** nhắc chỉnh camera không tính là một lần gợi ý Toán.
9. **Dừng hỗ trợ khi trẻ đã tiếp tục.**
10. **Chỉ nói về bài học:** AI không trò chuyện ngoài lề. Khi trẻ hỏi chuyện khác, từ chối nhẹ nhàng và đưa về bài.
11. **Quyền riêng tư bằng kỹ thuật, không chỉ bằng hướng dẫn:** frame có người bị chặn trên máy; chỉ vùng giấy được gửi đi.
12. **Phụ huynh quan sát, không can thiệp:** Parent View không có kênh nói chuyện với trẻ trong buổi học.
13. **Ngôn ngữ gợi ý khớp SGK của khối lớp.**

Ví dụ gợi ý cần đúng bản chất Toán và đúng cách diễn đạt của SGK lớp 6–7: "Muốn tìm số hạng chưa biết thì con làm thế nào?" Không dùng cách nói của lớp 8 như "trừ 5 ở cả hai vế".

## 5. Phạm vi MVP pilot

### Khối lớp và dạng bài

**Khối lớp: lớp 6–7 (đã chốt).** Lớp 8 trở lên nằm ngoài MVP.

Dạng bài ứng viên (chờ chốt 2–3 dạng cùng giáo viên):

| Dạng bài | Lớp | Ghi chú |
| --- | --- | --- |
| Tìm x dạng `ax + b = c`, `a(x + b) = c` với số nguyên | 6 | Khớp các fixture SC-02 đến SC-15 |
| Tìm x với số hữu tỉ/phân số | 7 | Chữ viết phân số khó nhận diện hơn |
| Tính giá trị biểu thức số nguyên/phân số nhiều bước | 6–7 | Nhiều bước trung gian, hợp với quan sát từng bước |

Quy tắc: **một chương, 2–3 dạng bài**, đối chiếu với bộ SGK (Kết nối tri thức / Chân trời sáng tạo / Cánh diều) mà các gia đình pilot dùng. Gia đình pilot chỉ tuyển học sinh lớp 6–7.

### Tính năng

| Nhóm | Trong MVP | Ngoài MVP |
| --- | --- | --- |
| Buổi học | Start, Pause, Resume, End; kiểm tra góc chụp kiểu chụp CCCD | Lịch tự khởi động |
| Quan sát và Intervention Engine | Chụp theo sự kiện, nhận bước viết, xóa/sửa, chuyển bài; state machine §8 | — |
| Voice Tutor | Nhận yêu cầu trợ giúp; L1–L2 chủ động; L3 chỉ khi trẻ chủ động hỏi | Hội thoại tự do |
| Parent View | Ảnh gần trực tiếp, làm mới vài giây; trạng thái buổi học | Live video (gói trả phí sau MVP) |
| Báo cáo | Báo cáo sau buổi qua thông báo; báo cáo tuần | Dashboard phân tích phức tạp |
| Phiếu bài tập | 1 phiếu/tuần theo điểm yếu, PDF in được; chụp lại để chấm | Kho bài lớn, nhiều môn |
| Student Memory | Lớp, chủ đề, lỗi thường gặp, lịch sử tự sửa và trợ giúp | Hồ sơ năng lực dài hạn |
| Ứng dụng phụ huynh | **Web app** kèm thông báo (ví dụ Zalo) | App native riêng |
| Chọn model | Hệ thống tự định tuyến | Người dùng tự chọn |

**Luôn ngoài MVP:** môn khác ngoài Toán; avatar/3D; gamification; LMS; marketplace giáo viên; thiết bị riêng; nhận diện khuôn mặt, cảm xúc, ánh mắt hoặc tư thế; chỉ số "focus %".

## 6. Thiết lập thiết bị và chụp ảnh

### Thiết bị

- **Giá đỡ chuẩn** tặng mỗi gia đình pilot, cố định góc chụp **từ trên xuống**.
- Góc trực diện **không hỗ trợ trong MVP**, vì chữ bị méo phối cảnh, tay che chữ và dễ lọt khuôn mặt.
- Một nền tảng cho app học sinh trong pilot (chờ chốt theo tỷ lệ thiết bị của nhóm pilot), có danh sách máy tối thiểu và 3–5 máy dự phòng cho mượn.
- Tùy chọn: vở hoặc giấy in sẵn **dấu bốn góc** để cắt vùng giấy chính xác. Phiếu bài tập in cũng có các dấu này.
- Phụ huynh setup lần đầu; hằng ngày trẻ tự đặt máy. App kiểm tra góc chụp mỗi lần Start và chỉ cho bắt đầu khi ảnh đạt.

### Chính sách chụp ảnh

AI không cần video. Pipeline chạy trên điện thoại:

1. **So sánh ảnh liên tiếp** (rẻ, offline) để phát hiện thay đổi trong vùng giấy.
2. Chờ **ảnh ổn định**, tức tay không còn che, rồi mới chụp frame để gửi.
3. **Chặn frame có khuôn mặt hoặc người** bằng phát hiện trên máy (không phải nhận diện danh tính). Frame bị chặn không rời khỏi máy và được ghi log.
4. **Cắt vùng giấy** rồi mới gửi lên server.
5. **Chụp định kỳ thưa** làm dự phòng khi bộ phát hiện thay đổi bỏ sót. Chu kỳ là tham số cấu hình (giả thuyết ban đầu 15–30 giây), cần đo.
6. **Burst ngắn có giới hạn** khi cần xác nhận lỗi hoặc tự sửa.
7. Bỏ kết quả cũ nếu trẻ đã đổi bài, sửa bước hoặc kết thúc buổi.

Ước tính để định hướng: chụp đều 3 giây một lần trong buổi 45 phút là khoảng 900 ảnh; chụp theo sự kiện kỳ vọng còn khoảng 100–200 ảnh. Cần đo thực tế.

### Camera và quyền kiểm soát

- Chỉ hoạt động trong buổi học đã bật. Không mở camera ngoài buổi học để phục vụ phụ huynh xem.
- Trạng thái camera/micro rõ ràng; nút tạm dừng và kết thúc luôn hiện.
- **Máy của con hiện chỉ báo khi phụ huynh đang xem.**
- Phụ huynh chỉ xem được buổi học đang hoạt động của con đã liên kết.

## 7. Kiến trúc

### Lớp điều phối độc lập với model

```
App học sinh ──(frame đã cắt + sự kiện)──▶ Backend điều phối ──▶ Model adapter ──▶ Model AI thương mại
                                              │                                   (vision / reasoning / ASR / TTS)
                                              ├─ Session state + Intervention Engine
                                              ├─ Bộ lọc đầu vào (ngữ cảnh, ngân sách)
                                              ├─ Bộ lọc đầu ra (chặn lộ đáp án, ngoài lề, độ dài)
                                              ├─ Event store + Student Memory (DB riêng)
                                              └─ Report + Worksheet generator (template + CAS)
Web phụ huynh ◀──(ảnh gần trực tiếp, trạng thái, báo cáo)── Backend
```

- **Model adapter:** mỗi nhà cung cấp có một adapter cùng interface (input: frame + ngữ cảnh; output: cách đọc + độ tin cậy). Đổi model không đổi Intervention Engine.
- **Định tuyến:** hệ thống chọn model theo nhiệm vụ. Model rẻ làm mặc định; model mạnh khi độ tin cậy thấp hoặc khi sinh gợi ý.
- **Cổng đánh giá:** model mới chỉ được bật khi chạy qua bộ replay SC-01 đến SC-18 và đạt ngưỡng ở §11. Kết quả lưu kèm `model_version` và `policy_version`.
- **Intervention Engine là code của hệ thống**, không giao quyết định im lặng/gợi ý hoàn toàn cho model. Model cung cấp bằng chứng; engine quyết định.
- **Dữ liệu gửi nhà cung cấp:** chỉ dùng API có cam kết không huấn luyện trên dữ liệu và lưu tối thiểu. Ghi rõ nhà cung cấp nào nhận dữ liệu gì.
- MVP dùng **một backend với module rõ ràng**, không tách microservice.

### Thành phần

1. **App học sinh:** camera, pipeline trên máy (§6), lifecycle, voice input/output.
2. **Perception (qua model adapter):** đọc đề và bước làm; phát hiện xóa, viết lại, đổi trang; trả nội dung kèm độ tin cậy.
3. **Session state:** bài hiện tại, bước đã xác nhận, pending error, hint level, tiến trình.
4. **Intervention Engine:** kết hợp bằng chứng, thời gian chờ, yêu cầu của trẻ, confidence và cooldown.
5. **Tutor/voice:** sinh gợi ý đúng ngữ cảnh và khối lớp; ASR/TTS; ngắt lời và hủy phát ngôn lỗi thời; bộ lọc đầu ra.
6. **Web phụ huynh:** trạng thái, ảnh gần trực tiếp, báo cáo, phiếu bài tập, quản lý dữ liệu và đồng ý.
7. **Event store + Student Memory:** sự kiện có cấu trúc và tổng hợp lịch sử.
8. **Worksheet generator:** sinh đề theo template, kiểm đáp án bằng công cụ tính toán (CAS), xuất PDF có dấu bốn góc.

### Parent View hai mức

| Mức | Cách làm | Khi nào |
| --- | --- | --- |
| Gần trực tiếp (MVP) | Dùng lại frame đã cắt; làm mới vài giây | Mặc định |
| Live video (sau MVP) | WebRTC theo yêu cầu, tự tắt sau vài phút; cần signaling và có thể cần TURN | Gói trả phí; đo bitrate, tỷ lệ relay, pin/nhiệt trước khi bật |

### Ngân sách và giới hạn

- Ngân sách request/frame/token theo buổi và theo ngày. Vượt ngân sách hoặc mất mạng thì báo đúng trạng thái, vẫn giữ quyền gọi trợ giúp của trẻ nếu khả dụng.
- Sau pilot, đặt **trần chi phí cho mỗi người dùng miễn phí** (giả thuyết ≤ 20–30k VND/tháng), đo bằng dữ liệu thật.

## 8. State và quyết định can thiệp

| State | Bằng chứng chính | Hành động |
| --- | --- | --- |
| OBSERVING | Buổi học sẵn sàng, chưa đủ dữ liệu | Quan sát |
| PROGRESSING | Bước hợp lệ, trẻ tiếp tục | Im lặng |
| POSSIBLE_ERROR | Có bước sai đáng tin cậy, chưa kéo dài | Chờ, quan sát tự sửa |
| SELF_CORRECTED | Trẻ sửa lỗi trước hỗ trợ sư phạm | Ghi sự kiện, im lặng |
| NEEDS_HELP | Lỗi kéo dài có bằng chứng hoặc yêu cầu trực tiếp | Gợi ý tối thiểu |
| POSSIBLY_STUCK | Bài chưa xong, không tiến triển, có ngữ cảnh | Hỏi trẻ có muốn gợi ý |
| UNKNOWN | Ảnh/chữ/ngữ cảnh không đủ tin cậy | Không phán sai; lấy thêm bằng chứng |
| RECOVERED | Trẻ tiếp tục đúng sau gợi ý | Hủy gợi ý chờ, về im lặng |

### Mức hỗ trợ

- **L0 — Silence:** không trợ giúp sư phạm.
- **L1 — Nudge:** "Con thử kiểm tra lại bước vừa rồi nhé."
- **L2 — Concept hint:** gợi ý khái niệm theo ngôn ngữ SGK của khối lớp.
- **L3 — Guided step:** hướng dẫn một bước rồi để trẻ tự làm bước tiếp. **Trong MVP, L3 chỉ dùng khi trẻ chủ động hỏi**, không do engine tự nâng.

Không tự động đưa full solution. Không tăng mức chỉ vì timer hết hạn.

Wait window, confidence threshold, stuck threshold và cooldown là **tham số cấu hình**, hiệu chỉnh qua chế độ bóng và pilot. Các mốc 8/30/45 giây trong scenario là fixture.

### Chế độ bóng (shadow mode)

Engine chạy đầy đủ, ghi lại quyết định kèm lý do, nhưng **không phát gợi ý sư phạm**. Lời chào và nhắc chỉnh camera vẫn được phép. Bật/tắt theo từng học sinh. Dùng ở 1–2 tuần đầu pilot để giáo viên gán nhãn và hiệu chỉnh tham số.

## 9. Báo cáo và phiếu bài tập

### Báo cáo sau buổi (đọc trong khoảng 30 giây)

- Thời lượng buổi học và thời lượng pause riêng.
- Số bài đã thử, hoàn thành, chưa xác nhận.
- Independent / self-corrected / after-hint.
- Một nhận xét có bằng chứng, ví dụ: "Hai lần nhầm khi tìm số hạng chưa biết; một lần con tự sửa."

### Báo cáo tuần

- Xu hướng IPSR theo tuần.
- **Lỗ hổng kiến thức:** chỉ báo "cần luyện" khi lỗi cùng loại lặp lại **ở ít nhất 3 bài qua ít nhất 2 buổi** (ngưỡng cấu hình). Dưới ngưỡng đó ghi là "cần theo dõi".
- Không khẳng định năng lực chắc chắn từ một buổi.
- Kèm **1 phiếu bài tập** nhắm vào lỗ hổng.

### Phiếu bài tập in

- Sinh **theo template** của dạng bài, tham số chọn sao cho nghiệm phù hợp khối lớp.
- **Đáp án kiểm bằng công cụ tính toán (CAS)**, không chỉ dựa vào LLM.
- Bám dạng bài và cách diễn đạt của SGK đang dùng.
- PDF khổ A4, có dấu bốn góc và mã phiếu để nhận diện khi chụp lại.
- Trẻ làm xong thì chụp lại trong app để chấm và cập nhật Student Memory.

## 10. Dữ liệu, quyền riêng tư và pháp lý

Dữ liệu của trẻ vị thành niên, gồm hình ảnh trong nhà, giọng nói và lịch sử học, được bảo vệ chặt theo Nghị định 13/2023/NĐ-CP và Luật Bảo vệ dữ liệu cá nhân. **Phải có tư vấn pháp lý trước pilot.**

| Hạng mục | Chính sách |
| --- | --- |
| Ảnh bài làm | Chỉ vùng giấy đã cắt. Tự xóa sau **7 ngày** hoặc theo cài đặt của phụ huynh |
| Frame có người | Chặn trên máy, không gửi đi; chỉ ghi log sự kiện chặn |
| Video | Không lưu |
| Audio | Không lưu bản ghi mặc định; chỉ lưu transcript cần thiết cho event |
| Dữ liệu học có cấu trúc | Lưu trong DB của hệ thống, không lưu trên nhà cung cấp AI |
| Nhà cung cấp AI | API có cam kết không huấn luyện, lưu tối thiểu; có hồ sơ chuyển dữ liệu ra nước ngoài |
| Quyền phụ huynh | Xem ảnh bài làm, xem/xuất/xóa toàn bộ dữ liệu của con bằng một thao tác |
| Phân quyền | Mỗi tài khoản phụ huynh chỉ truy cập học sinh đã liên kết |
| Thương mại hóa | Không bán/chia sẻ dữ liệu cá nhân; không quảng cáo nhắm tới trẻ |

### Hai loại đồng ý tách biệt

1. **Dùng dịch vụ:** bắt buộc để dùng app. Có phần giải thích dễ hiểu cho trẻ.
2. **Cho dùng ảnh bài làm để cải thiện hệ thống:** tùy chọn, có thể rút lại. Ảnh đã cắt, không có người, lưu theo thời hạn ghi rõ. Đây là nguồn cho bộ replay.

## 11. Acceptance test và phép đo

- Tách **assertion từng testcase** khỏi **metric trên cả tập**. Testcase "phải im lặng" yêu cầu 0 phát ngôn sư phạm; mục tiêu 95% là tỷ lệ trên tập mẫu.
- Ground truth do giáo viên Toán gán nhãn; tập mẫu đa dạng chữ viết, ánh sáng, điện thoại, tốc độ viết, độ khó.
- Đánh giá precision/recall theo nhóm; confidence của model chưa hiệu chỉnh không tương đương xác suất đúng.
- Độ trễ báo **p95**, ghi rõ thiết bị, mạng và model.
- Log các mốc: event phát sinh, backend nhận, đủ bằng chứng theo ground truth, engine quyết định, bắt đầu phát âm thanh, trẻ tiến triển lại.

### Bộ replay

- **Nguồn ban đầu:** 200–300 bài làm thật (chuỗi ảnh theo thời gian) của đúng khối lớp, có cả sai, tự sửa, bỏ dở, ảnh xấu.
- **Gán nhãn:** bước đúng/sai, thời điểm tự sửa, thời điểm nên/không nên can thiệp, mức gợi ý phù hợp.
- **Harness:** đưa chuỗi ảnh vào hệ thống, chấm tự động theo scenario, xuất báo cáo theo model và policy version.

### Cổng chất lượng trước khi phát cho gia đình pilot

| Chỉ số trên bộ replay | Ngưỡng |
| --- | --- |
| Can thiệp sai khi trẻ đang làm đúng | < 5% |
| Error Detection Precision | ≥ 85% |
| Kết luận Toán từ ảnh xấu (SC-09/14) | ≈ 0 |
| Gợi ý L1/L2 lộ đáp án | < 5% |
| Frame có người bị gửi lên server (SC-17) | 0 trên tập test |

Không đạt thì chưa phát cho gia đình; sửa chính sách hoặc prompt rồi chạy lại.

## 12. Main product scenarios

Các ngưỡng là đề xuất ban đầu, review sau spike. Fixture dùng cho lớp 6–7 dạng tìm x; ngôn ngữ gợi ý theo §4.

### SC-01 — Bắt đầu buổi học
**Hành động:** trẻ bấm Start và bắt đầu viết.
**Behavior:** kiểm tra góc chụp kiểu CCCD; ảnh chưa đạt thì hướng dẫn chỉnh, không cho bắt đầu. Đạt thì chào một lần ngắn rồi im lặng; không yêu cầu scan từng câu hay nhập đề.
**Technical:** tạo session ID; kiểm tra chất lượng, phát hiện vùng giấy, chặn frame có người; chuyển OBSERVING. Mục tiêu p95 camera ready < 2 giây; phát hiện bắt đầu viết < 3 giây; page-visible detection ≥ 95%; problem recognition ≥ 90% trong phạm vi dạng bài hỗ trợ. Sau lời chào, 0 phát ngôn sư phạm không cần thiết.

### SC-02 — Trẻ làm đúng, AI im lặng
**Fixture:** `3x + 5 = 20 → 3x = 15 → x = 5`.
**Behavior:** không "Đúng rồi" hoặc "Giỏi lắm" sau từng bước.
**Technical:** PROGRESSING → L0. Testcase: 0 tutoring speech. Trên tập: correct-step recognition ≥ 95%, false intervention < 5%, Silent Success Rate > 95%.

### SC-03 — Viết sai rồi tự sửa
**Fixture:** viết `3x = 25`, sau 8 giây xóa và viết `3x = 15`, trước khi có gợi ý.
**Behavior:** im lặng xuyên suốt.
**Technical:** POSSIBLE_ERROR → chờ → erase/rewrite → SELF_CORRECTED → L0; hủy intervention đang chờ; đúng một self-correction event. Pipeline trên máy phải bắt được thao tác xóa/viết lại giữa hai lần chụp định kỳ. Mục tiêu nhận lỗi ≥ 95%, nhận tự sửa ≥ 90%, premature intervention < 10%.

### SC-04 — Sai và tiếp tục theo hướng sai
**Fixture:** `3x + 5 = 20 → 3x = 25 → x = 25/3`; không tự sửa. Phân biệt lỗi gốc ở bước trước với phép chia hợp lệ trên giá trị sai.
**Behavior:** sau đủ bằng chứng, gợi ý kiểm tra bước tìm `3x`; không đọc đáp án.
**Technical:** persistent error → NEEDS_HELP → L1, không lặp hint. Mục tiêu persistent-error detection ≥ 90%; wrong intervention < 10%; lộ đáp án < 5%. p95 từ đủ bằng chứng tới quyết định < 3 giây; từ quyết định tới âm thanh < 1,5 giây; báo riêng tổng thời gian.

### SC-05 — Ngừng viết nhưng chưa sai
**Fixture:** `2(x + 3) = 14`; không viết trong 45 giây.
**Behavior:** không kết luận trẻ không biết hay mất tập trung. Nếu đủ ngữ cảnh, hỏi một lần: "Con đang suy nghĩ hay muốn cô gợi ý một chút?" Trẻ muốn tự nghĩ thì tiếp tục im lặng.
**Technical:** timer đơn độc không trigger tutoring. Mục tiêu stuck detection precision > 85%; theo dõi recall và số lần hỏi lặp.

### SC-06 — Trẻ chủ động yêu cầu giúp
**Hành động:** "Con không biết làm câu này."
**Behavior:** không áp wait window; gợi ý bước nhỏ phù hợp. Trẻ trả lời đúng hướng thì xác nhận ngắn và để trẻ tự viết.
**Technical:** VAD → ASR → REQUEST_HELP → ngữ cảnh bài → hint → bộ lọc đầu ra → TTS → OBSERVING. Mục tiêu p95 từ kết thúc câu nói tới âm thanh trả lời < 2 giây. Chưa xác định được câu nào thì hỏi lại; không đoán đề.

### SC-07 — Hỗ trợ tăng dần
**Hành động:** L1 chưa giúp trẻ tiến triển.
**Behavior:** chuyển L2 khi có bằng chứng. **Trong MVP, L3 chỉ khi trẻ chủ động hỏi thêm.** Dừng khi trẻ làm được.
**Technical:** log hint level, nguyên nhân tăng mức, phản hồi, kết quả. Không phát lại hint cũ; không full solution tự động. Đo tỷ lệ recovery theo từng mức.

### SC-08 — Trẻ làm tiếp sau hint
**Fixture:** sau hint, trẻ viết `3x = 20 - 5 → 3x = 15 → x = 5`.
**Behavior:** dừng hỗ trợ, không giảng tiếp.
**Technical:** NEEDS_HELP → RECOVERED → L0; hủy hint đang chờ và lời nói lỗi thời. Mục tiêu Intervention Exit Accuracy > 90%; 0 hint bổ sung sau recovery đã xác nhận.

### SC-09 — Camera bị che, mờ hoặc thiếu sáng
**Behavior:** không phán trẻ sai; chỉ nhắc chỉnh camera khi vấn đề kéo dài.
**Technical:** UNKNOWN; chặn kết luận Toán trên vùng thiếu bằng chứng. Mục tiêu bad-view detection > 95%; tutoring dựa trên ảnh không đủ < 2%; hallucinated-error < 1%.

### SC-10 — Chuyển sang bài tiếp theo
**Behavior:** không hỏi xác nhận mỗi lần chuyển; không nhắc lỗi bài trước vào bài mới.
**Technical:** problem ID mới; reset pending error/hint; giữ liên kết lịch sử. Mục tiêu transition detection > 90%. Đổi trang không đủ để kết luận bài cũ đã xong; thiếu bằng chứng thì đánh dấu "chưa xác nhận".

### SC-11 — Phụ huynh xem từ xa
**Tiền điều kiện:** tài khoản phụ huynh đã liên kết; buổi học đang hoạt động.
**Behavior:** phụ huynh thấy **ảnh gần trực tiếp** của bàn học và trạng thái buổi học; máy của con hiện chỉ báo đang được xem; buổi học AI không bị ảnh hưởng. Buổi học dừng thì không xem tiếp được. Không có kênh nói với trẻ.
**Technical:** dùng lại frame đã cắt, không mở luồng camera riêng; xác thực theo student/session. Test chứng minh tài khoản khác không xem được. Đo độ trễ làm mới ảnh.

### SC-12 — Kết thúc và báo cáo
**Hành động:** trẻ bấm End.
**Behavior:** camera, micro và trợ giúp dừng; phụ huynh nhận báo cáo sau buổi.
**Technical:** đóng session, hủy pending jobs, tổng hợp từ event log. Fixture: 12 bài hoàn thành = 8 independent + 2 self-corrected + 2 after-hint; full-assistance = 0. Không đếm một bài vào nhiều nhóm; bài chưa hoàn thành tách riêng. Tổng khớp 100%.

### SC-13 — Nhớ lỗi từ buổi trước
**Fixture:** lịch sử lỗi tìm số hạng chưa biết; buổi mới gặp `5x + 7 = 32`.
**Behavior:** không nhắc trước. Làm đúng → im lặng; sai rồi tự sửa → im lặng; sai kéo dài → hint phù hợp.
**Technical:** tải đúng profile, không lẫn tài khoản; history không bypass confidence/wait policy. Log phiên bản profile.

### SC-14 — Chữ viết không chắc chắn
**Fixture:** perception trả `3x = 15` (55%), `3x = 18` (31%), unknown (14%).
**Behavior:** không khẳng định sai; lấy frame có ý nghĩa tiếp theo; vẫn không rõ thì nhắc viết rõ hơn hoặc chỉnh camera.
**Technical:** UNKNOWN → không tutoring trên cách đọc chưa xác nhận. Testcase: 0 kết luận sai.

### SC-15 — Xin đáp án trực tiếp
**Hành động:** "Đáp án câu này là bao nhiêu?"
**Behavior:** hướng trẻ thử bước đầu hoặc nói chỗ vướng; progressive hint; không phán xét.
**Technical:** ANSWER_REQUEST; giữ chính sách L1/L2/L3; không phát đáp án cuối. Kiểm thử paraphrase và hỏi lại nhiều lần.

### SC-16 — Phiếu bài tập in và chụp chấm *(mới)*
**Tiền điều kiện:** báo cáo tuần đã xác định một lỗ hổng đủ bằng chứng.
**Behavior:** phụ huynh tải phiếu PDF và in. Trẻ làm trên giấy rồi chụp lại trong app; phụ huynh nhận kết quả chấm.
**Technical:** sinh đề từ template; mọi đáp án qua CAS; nhận mã phiếu và dấu bốn góc khi chụp lại; cập nhật Student Memory. Testcase: 0 đề hoặc đáp án sai trên tập phiếu sinh thử.

### SC-17 — Frame có khuôn mặt hoặc người *(mới)*
**Hành động:** trẻ cúi sát hoặc có người đi qua vùng chụp.
**Behavior:** buổi học tiếp tục; nếu lặp lại, nhắc chỉnh máy.
**Technical:** phát hiện trên máy; frame bị chặn **không rời khỏi máy**; ghi event chặn; Parent View không hiển thị frame đó. Testcase: 0 frame có người tới server trên tập test.

### SC-18 — Đổi hoặc thêm model *(mới)*
**Hành động:** đội phát triển thêm model mới vào định tuyến.
**Technical:** model chạy qua bộ replay và cổng chất lượng §11 trước khi được bật; so sánh với model hiện tại theo từng scenario; có thể rollback về model trước. Không model nào được bật cho người dùng mà thiếu báo cáo đánh giá.

## 13. KPI và cách tính

| KPI | Định nghĩa đo | Mục tiêu đề xuất |
| --- | --- | --- |
| Error Detection Precision | Lỗi xác nhận đúng / tổng lần kết luận có lỗi | > 90% |
| Silent Success Rate | Cửa sổ tiến triển đúng mà AI im lặng / tổng cửa sổ tiến triển đúng | > 95% |
| Self-Correction Preservation | Cơ hội tự sửa được giữ im lặng tới lúc sửa / tổng cơ hội có nhãn | > 90% |
| Correct Intervention Rate | Can thiệp đúng thời điểm, đúng lỗi, đúng mức / tổng can thiệp | > 85% |
| Intervention → Recovery | Episode trợ giúp dẫn tới tiến triển hợp lệ / tổng episode đánh giá được | > 70% |

Một episode có thể chứa nhiều hint. Đo self-correction preservation bằng replay có nhãn.

**North Star — IPSR:** `(bài đúng độc lập + bài đúng sau tự sửa, không nhận hint) / tổng bài đã thử đủ điều kiện`. Báo riêng tỷ lệ chưa hoàn thành. Phân nhóm loại trừ nhau: Independent / Self-corrected / After-hint / Full-assistance (ngoại lệ) / Unfinished hoặc unverified.

**AI Intervention Rate:** interventions/hour và episodes/problem; tách technical prompt, greeting và tutoring. Không tối ưu số lần AI nói như chỉ số engagement.

**KPI phía phụ huynh (mới):** tỷ lệ mở báo cáo; tỷ lệ phiếu bài tập được in và chụp lại; tỷ lệ đồng ý "báo cáo giúp tôi biết con hổng chỗ nào".

## 14. Chi phí và giả thuyết kinh doanh

`Variable cost/student/month = AI vision + reasoning + ASR + TTS + parent view + storage + variable infra + payment/support`

- Vision: số frame gửi thực tế × đơn giá model. Pipeline trên máy quyết định phần lớn chi phí này.
- Reasoning: số lượt xác nhận/gợi ý/báo cáo/phiếu × token × đơn giá.
- ASR/TTS: chỉ phút audio thực xử lý.
- Parent view gần trực tiếp: chủ yếu băng thông ảnh đã có; live video tính riêng.

`Contribution margin = doanh thu thuần − variable cost`. Doanh thu thuần phải trừ **phí nền tảng 15–30% nếu thu qua App Store/Google Play**; cân nhắc thanh toán trực tiếp qua web.

`Break-even paying students = monthly fixed costs / contribution margin`, chỉ có nghĩa khi margin > 0.

**Ước tính độ lớn (chưa kiểm chứng):** khoảng 60–220k VND/học sinh dùng đều mỗi tháng nếu chụp không tối ưu; mục tiêu sau tối ưu là ≤ 20–30k cho người dùng miễn phí. Với 50 gia đình pilot, chi phí API ước tính 5–15 triệu VND/tháng, nên **pilot dùng model chất lượng tốt nhất**, chưa tối ưu giá.

### Mô hình freemium (giả thuyết)

| Miễn phí | Trả phí |
| --- | --- |
| Giới hạn số buổi hoặc phút mỗi ngày | Không giới hạn |
| Gợi ý L1–L2, trẻ chủ động hỏi thì L3 | Toàn bộ mức hỗ trợ |
| Báo cáo sau buổi | Báo cáo tuần/tháng, xu hướng, lỗ hổng chi tiết |
| — | Phiếu bài tập in theo điểm yếu |
| Ảnh gần trực tiếp | Live video |

Hướng thu tiền khác cần kiểm chứng: B2B2C với trường/trung tâm; kết nối gia sư khi phụ huynh chủ động đồng ý.

## 15. Pilot (tóm tắt)

Kế hoạch chi tiết, checklist và bảng go/no-go nằm trong tài liệu **Kế hoạch Pilot**.

- Tối đa 50 gia đình có con học lớp 6–7; một phần người không quen biết.
- Triển khai cuốn chiếu 5 → 15 → 50.
- 1–2 tuần đầu chế độ bóng; bật gợi ý khi đạt ngưỡng.
- Giáo viên Toán bán thời gian xem lại can thiệp và báo cáo mỗi ngày.
- Cuối pilot mời đặt cọc cho gói sau pilot.

| Nhóm | Chỉ số | Ngưỡng go |
| --- | --- | --- |
| Chất lượng AI | Can thiệp sai / tổng can thiệp | < 10% |
| | Gia đình phàn nàn AI làm phiền | < 15% |
| Sử dụng | Gia đình còn dùng ≥ 3 buổi/tuần ở tuần 4 | ≥ 50% |
| | Phụ huynh mở báo cáo | ≥ 70% |
| Giá trị | Đồng ý "báo cáo giúp tôi biết con hổng chỗ nào" | ≥ 70% |
| | Phiếu bài tập được làm | ≥ 40% |
| Kinh doanh | Đặt cọc hoặc cam kết trả phí | ≥ 20–30% |
| Chi phí | Chi phí AI p95/học sinh/tháng | Đo được, có phương án giảm khi mở rộng |
| An toàn | Frame có người tới server; sự cố dữ liệu | 0 |

## 16. Lộ trình (~14 tuần)

| Tuần | Việc chính |
| --- | --- |
| 1–3 | Chốt 2–3 dạng bài và bộ SGK; thu và gán nhãn dữ liệu; dựng bộ replay; chấm 2–3 model; thủ tục pháp lý |
| 4–7 | Vertical slice: app học sinh (pipeline trên máy, voice), Intervention Engine, model adapter, báo cáo, web phụ huynh, worksheet generator |
| 8 | Alpha nội bộ 5 gia đình |
| 9–10 | Chế độ bóng; mở rộng 15 → 50 gia đình |
| 11–13 | Bật gợi ý; phát phiếu bài tập; phỏng vấn hằng tuần |
| 14 | Tổng kết, mời đặt cọc, quyết định go/no-go |

**Nguồn lực tối thiểu:** 2 kỹ sư (mobile; backend/AI), 1 giáo viên Toán bán thời gian, Sơn làm product kiêm vận hành pilot.

Không mở rộng môn, thêm dashboard hay tách microservice trước khi vòng lặp quan sát → im lặng/chờ → gợi ý → hồi phục đạt chất lượng.

## 17. Quyết định

### Đã chốt
- Lớp điều phối độc lập với model, dùng model AI thương mại.
- Phụ huynh theo dõi từ xa, không can thiệp.
- Báo cáo lỗ hổng kiến thức kèm phiếu bài tập in.
- Chụp ảnh theo sự kiện, không stream video cho AI.
- Học sinh lớp 6–7; AI chỉ nói về bài học.
- Chỉ chụp bàn học; chặn hình ảnh cá nhân; ảnh tự xóa sau 7 ngày; dữ liệu học trong DB riêng.
- Miễn phí trong pilot; không bán dữ liệu.

### Chờ chốt
- 2–3 dạng bài trong phạm vi lớp 6–7; bộ SGK.
- Chỉ góc từ trên xuống (khuyến nghị) hay hỗ trợ cả góc trực diện.
- Hệ thống tự chọn model (khuyến nghị) hay cho người dùng chọn.
- Parent View: ảnh gần trực tiếp trong MVP (khuyến nghị), live video sau.
- Nền tảng app học sinh trong pilot; danh sách máy tối thiểu.
- Model vision, ASR, TTS, reasoning ban đầu; nhà cung cấp có cam kết không lưu dữ liệu.
- Chu kỳ chụp dự phòng, ngân sách frame/request.
- Wait window, cooldown, recovery window.
- Kênh thông báo cho phụ huynh (Zalo hoặc khác).
- Nội dung hai loại đồng ý; thời hạn lưu ảnh cho bộ replay.
- UX khi mất mạng, app vào background, máy nóng, pin yếu, camera lệch.
- Giá gói trả phí, kênh thanh toán, hạn mức miễn phí sau pilot.

## 18. Hướng dẫn cho AI coding agent

Đọc tài liệu như yêu cầu sản phẩm dự kiến; đọc trạng thái repo và test trước khi tiếp tục. Không tự nhận các mục tiêu ở đây là tính năng đã hoàn thành.

- Giữ MVP nhỏ. Thứ tự ưu tiên: **bộ replay và harness → Intervention Engine → model adapter → pipeline trên máy → báo cáo và phiếu → web phụ huynh.**
- Intervention Engine là code của hệ thống; model chỉ cung cấp bằng chứng kèm độ tin cậy.
- Mọi model đi qua adapter cùng interface; không gọi API nhà cung cấp trực tiếp từ logic nghiệp vụ.
- L0 là quyết định explicit, có reason và log.
- UNKNOWN không chuyển thành WRONG chỉ vì thiếu dữ liệu.
- Frame có người không được rời khỏi máy; chỉ gửi vùng giấy đã cắt.
- Hủy kết quả/hint lỗi thời; session end dừng capture và output.
- Không tự đưa full solution; bộ lọc đầu ra chặn lộ đáp án và nội dung ngoài lề.
- Đáp án phiếu bài tập phải qua CAS.
- Có trace đối chiếu SC-01 đến SC-18, đo latency và cost theo `model_version`, `policy_version`.
- Event tối thiểu: `event_id`, `session_id`, `student_id`, `problem_id`, `timestamp`, `event_type`, `state_before`, `state_after`, `evidence_ref`, `confidence`, `decision_reason`, `hint_level`, `model_version`, `policy_version`, `shadow_mode`, `latency`, `cost_usage`.
- Báo rõ phần cần Sơn thao tác: đăng nhập, quyền thiết bị, tài khoản nhà cung cấp, cấu hình.
- Khi bàn giao: code đã đổi, test đã chạy, blocker thực tế, next step. Không ghi "done" chỉ vì mock/demo chạy.

**Nguyên tắc xuyên suốt:** Quan sát đủ để hiểu; can thiệp ít để giữ việc học độc lập của trẻ.
