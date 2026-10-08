# Technical HLD — AI Study Companion

> **Đã được thay thế** bởi [Business HLD v1.2](business-hld-v1.2.md), [Technical HLD v1.2](technical-hld-v1.2.md) và [context v0.4](ai-study-companion-context-v0.4.md) ngày 07/10/2026. Giữ lại để tra lịch sử; không dùng làm yêu cầu.

**Phiên bản:** 1.1  
**Ngày:** 06/10/2026  
**Chủ dự án:** Sơn  
**Tài liệu đồng hành:** [Business HLD v1.1](business-hld-v1.1.md)  
**Thay thế:** Technical HLD 1.0 (06/10/2026)  
**Trạng thái:** Thiết kế đề xuất cho MVP pilot 50 gia đình; chưa có code, benchmark hay capacity đã xác nhận.

## 0. Baseline và quy tắc dùng tài liệu

Technical HLD và Business HLD cùng phiên bản **1.1** là một bộ baseline. Bảng quyết định D01–D20 nằm ở [Business HLD §0.1](business-hld-v1.1.md) và áp dụng nguyên văn cho tài liệu này. Khi đổi một quyết định chung phải cập nhật cả hai.

Các quyết định ảnh hưởng mạnh nhất tới kiến trúc:

- **D02/D03:** lệnh giọng nói; học sinh không chạm máy trong buổi học.
- **D04/D05/D06:** MVP gửi ảnh vùng giấy đã cắt lên server; model AI thương mại qua adapter; OCR trên máy là R&D.
- **D11/D12:** lớp 6–7; phiếu bài in kiểm đáp án bằng CAS.
- **D13/D16:** ảnh gần trực tiếp cho phụ huynh; ảnh xóa sau 7 ngày.

### 0.1. Thay đổi kiến trúc so với v1.0

| v1.0 | v1.1 |
| --- | --- |
| OCR/formula trên máy, API chỉ nhận JSON | Client gửi ảnh vùng giấy đã cắt; server gọi model vision qua adapter |
| Cấm cloud image fallback | Cloud image là đường chính của MVP; nhận dạng trên máy là R&D |
| Nút Check/Help, chọn vùng, xác nhận trên màn hình | Từ gọi + ASR + intent; tự chụp; xác nhận bằng giọng nói; thẻ lệnh |
| Live View WebRTC/TURN | Ảnh gần trực tiếp theo yêu cầu, dùng lại pipeline chụp; live video sau MVP |
| Xóa ảnh khi End | Ảnh trên server xóa sau 7 ngày (cấu hình theo phụ huynh) |
| Không có worksheet | Worksheet generator: template + CAS + PDF có dấu bốn góc và mã phiếu |
| Sizing 100.000 active ở thân tài liệu | Thiết kế cho pilot; sizing lớn chuyển sang Phụ lục A |

## 1. Quyết định kiến trúc

1. **Rảnh tay là ràng buộc cứng.** Mọi bước trong buổi học có đường không cần chạm: giọng nói, giấy hoặc thẻ lệnh. Không bước nào được thiết kế mà bắt buộc chạm màn hình.
2. **Ba trigger phân tích:** lệnh Kiểm tra, lệnh Trợ giúp, chụp phiếu bài. Idle ~60 giây chỉ phát câu hỏi mẫu tại máy, không gọi server.
3. **Client lọc trước khi gửi:** chất lượng ảnh, che tay, phát hiện người/khuôn mặt (chặn frame), cắt và chỉnh phối cảnh vùng giấy. Frame có người không bao giờ rời máy.
4. **Server nhận ảnh đã cắt**, gọi model vision qua `RecognitionEngine` adapter để lấy transcription có cấu trúc kèm độ tin cậy. Đổi model không đổi phần còn lại.
5. **Chấm Toán tất định:** parser theo allowlist và symbolic engine quyết định đúng/sai; LLM không tự chấm.
6. **LLM chỉ viết lời phản hồi** trong giới hạn của policy; output qua bộ lọc (mức gợi ý, lộ đáp án, ngoài lề, độ dài).
7. **Âm thanh:** từ gọi nhận diện trên máy; chỉ đoạn sau từ gọi được gửi lên ASR. TTS là kênh phản hồi chính.
8. UNKNOWN không thành WRONG; nhận dạng không tự sửa phép tính sai của học sinh.
9. Backend modular monolith cùng worker tách tiến trình. Không microservice trong MVP.

## 2. Phạm vi MVP

**Có:** buổi học rảnh tay (tự bắt đầu, lệnh giọng nói, tự kết thúc); liên kết tài khoản và đồng ý; xem, xuất, xóa dữ liệu; Kiểm tra/Trợ giúp; xác nhận bằng giọng nói; history theo kỹ năng; sửa và kiểm tra lại; báo cáo sau buổi và tuần; phiếu bài in và chụp chấm; ảnh gần trực tiếp cho phụ huynh; thẻ lệnh dự phòng.

**Dạng bài:** 2–3 dạng trong Toán lớp 6–7 (ứng viên: tìm x dạng `ax + b = c`, `a(x + b) = c` với số nguyên; tìm x với phân số; tính biểu thức nhiều bước). Chốt cùng giáo viên ở tuần 1.

**Không có:** hình học; lớp 8 trở lên; camera chạy ngầm; live video; nhận dạng trên máy; tự nhận biết hoàn thành bài; ASR luôn bật; suy luận "lười".

## 3. Kiến trúc logic

~~~mermaid
flowchart TD
  subgraph Client["App học sinh (trên giá đỡ)"]
    Cam["Camera"]
    Frame["Khung hình: 4 góc trang, bù lệch"]
    Guard["Chất lượng, che tay, chặn người/khuôn mặt"]
    Crop["Cắt và chỉnh phối cảnh vùng giấy"]
    Wake["Từ gọi trên máy"]
    Card["Nhận thẻ lệnh"]
    Idle["Idle timer"]
    Speak["Phát TTS, barge-in"]
    Cam --> Frame --> Guard --> Crop
    Cam --> Card
  end
  subgraph Server["Backend"]
    API["API: xác thực, session, revision"]
    ASR["ASR + intent"]
    Rec["RecognitionEngine adapter"]
    Gate["Evidence gate"]
    Val["Math validator"]
    Pol["History + hint policy"]
    Tut["Tutor LLM adapter + output filter"]
    TTS["TTS"]
    WS["Worksheet generator"]
    Rep["Report worker"]
    DB["PostgreSQL"]
    Obj["Object storage (ảnh, TTL 7 ngày)"]
    API --> Rec --> Gate --> Val --> Pol --> Tut --> TTS
    Pol <--> DB
    Rec --> Obj
    DB --> Rep
    DB --> WS
  end
  Wake -->|đoạn âm thanh sau từ gọi| ASR --> API
  Card -->|intent| API
  Crop -->|ảnh đã cắt khi có trigger| API
  TTS -->|audio + text| Speak
  Idle -->|câu hỏi mẫu tại máy| Speak
  Rep --> Parent["Web phụ huynh"]
  WS --> Parent
  Crop -->|ảnh thưa khi phụ huynh xem| Parent
~~~

Sơ đồ thể hiện ranh giới logic. ASR và TTS có thể là dịch vụ ngoài qua adapter.

## 4. Hệ thống giọng nói và rảnh tay

### 4.1. Vòng đời buổi học không chạm

| Bước | Cơ chế |
| --- | --- |
| Bắt đầu | Trên màn hình chờ, app kiểm tra liên tục: thấy đủ 4 góc trang, ánh sáng đạt, không có người trong khung, máy đứng yên ≥ 3 giây → phát lời chào → `WORKING` |
| Lệnh | Từ gọi trên máy → ghi đoạn tối đa ~6 giây hoặc tới khi VAD báo im lặng → ASR → intent |
| Xác nhận đã nghe | Âm báo ngắn tại máy ngay khi nhận từ gọi; câu "Cô xem nhé" khi intent đã rõ |
| Tự chụp | Sau intent Kiểm tra/Trợ giúp: chờ trang ổn định và không có tay che (timeout ~5 giây, quá thì nhắc "Con bỏ tay ra khỏi vở nhé") |
| Xác nhận ký hiệu | Server trả câu hỏi đóng ("mười lăm hay mười tám?"); app phát TTS và mở ASR không cần từ gọi trong ~8 giây |
| Lệch vở | Bù phối cảnh trong ngưỡng; ra khỏi ngưỡng thì nhắc xê dịch vở |
| Barge-in | Từ gọi hoặc "dừng" trong lúc TTS phát → dừng phát, hủy câu còn lại |
| Kết thúc | Lệnh "Con học xong rồi" hoặc thẻ XONG; không hoạt động 10 phút (cấu hình) → hỏi → không trả lời → kết thúc |

Nút Pause/End vẫn hiện trên màn hình cho phụ huynh và trường hợp khẩn cấp, không bắt buộc dùng.

### 4.2. Từ gọi và ASR

- **Từ gọi chạy trên máy** (keyword spotting). Từ gọi là **"Cô ơi"** (D20). Vì đây là cụm từ trẻ hay nói, phải đo kích hoạt nhầm với TV, anh chị em, trẻ gọi người nhà; có thể thêm bước xác nhận ý định ngắn.
- Chưa xác nhận có thư viện từ gọi tiếng Việt đạt chất lượng với giọng trẻ trên cả Android và iOS. **Spike tuần 1** so sánh: thư viện keyword spotting có custom wake word, model nhỏ tự huấn luyện, và phương án dùng VAD + ASR trên server cho cụm "Cô ơi" (tốn chi phí và kém riêng tư hơn, chỉ dùng nếu hai phương án đầu không đạt).
- **ASR trên server** qua adapter, chỉ nhận đoạn sau từ gọi. Không lưu audio mặc định; lưu transcript lệnh trong event.
- **Intent:** bộ luật và từ khóa cho tập lệnh nhỏ ở Business HLD §5.2, sau đó mới dùng LLM phân loại khi không khớp. Câu ngoài lề được trả lời bằng câu mẫu đưa về bài.
- Mic indicator luôn hiện khi buổi học đang chạy.

### 4.3. Thẻ lệnh

- Ba thẻ in: KIỂM TRA, GIÚP CON, XONG. Mỗi thẻ có marker hình học (ví dụ ArUco/AprilTag) cùng chữ in to.
- Nhận diện marker trên máy, không cần model AI. Thẻ phải được giữ ổn định ~1 giây để tránh nhận nhầm.

### 4.4. TTS

- TTS server qua adapter; cache câu mẫu (lời chào, nhắc bỏ tay, nhắc xê dịch vở, câu hỏi idle) **trên máy** để phát ngay, không phụ thuộc mạng.
- Giọng nữ, tốc độ phù hợp lớp 6–7; đọc biểu thức Toán theo cách đọc tiếng Việt ("ba x cộng năm bằng hai mươi").

## 5. Pipeline chụp ảnh trên client

### 5.1. Quan sát nhẹ trong buổi học

Camera → mẫu độ phân giải thấp (giả thuyết 2 khung hình/giây) → phát hiện 4 góc trang → che tay/chất lượng → thay đổi nét viết → idle timer.

Không gửi gì lên server ở bước này. Tay chuyển động không tính là viết thêm; camera bị che hoặc Pause làm timer dừng.

### 5.2. Khi có trigger

1. Khóa snapshot với `problem_id`, `page_id`, `submission_revision`.
2. Chờ trang ổn định, không tay che (timeout và nhắc bằng giọng nói).
3. **Phát hiện người/khuôn mặt trên máy. Có thì bỏ frame**, ghi event chặn, nhắc chỉnh.
4. Cắt vùng trang, chỉnh phối cảnh, nén (JPEG, cạnh dài giả thuyết 1600 px; đo chất lượng đọc trên bộ replay).
5. Gửi ảnh cùng metadata. Ảnh gốc không cắt không rời máy.
6. Nhận phản hồi; nếu trang đã đổi trước khi phản hồi tới thì bỏ phản hồi.

### 5.3. Chụp phiếu bài

Phát hiện dấu bốn góc và mã phiếu trên máy → chụp → gửi kèm `worksheet_id`. Lệnh: "Cô chấm giúp con" hoặc tự động khi phát hiện mã phiếu ổn định ≥ 2 giây (cấu hình).

### 5.4. Ảnh gần trực tiếp cho phụ huynh

Chỉ khi phụ huynh đang mở trang xem: app gửi ảnh vùng giấy đã cắt, độ phân giải thấp, mỗi vài giây (cấu hình), qua cùng bộ chặn người. Màn hình con hiện chỉ báo "Bố/mẹ đang xem". Ảnh này không dùng để chấm và không lưu quá thời gian xem.

### 5.5. Lifecycle

- App foreground, màn hình luôn sáng (độ sáng thấp) suốt buổi học. Không cam kết chạy ngầm.
- Checklist trước buổi học: cắm sạc, bật Không làm phiền. App không tự bật Không làm phiền trên mọi nền tảng.
- Pause/End dừng camera, micro, nhận diện, TTS; hủy request đang chờ.
- Hàng đợi offline có giới hạn và TTL; reconnect kiểm tra revision trước khi gửi.

## 6. Model portfolio

| Thành phần | MVP | R&D dài hạn |
| --- | --- | --- |
| Nhận dạng bài làm | Model vision đa phương thức thương mại qua `RecognitionEngine`; output JSON có cấu trúc dòng, LaTeX, độ tin cậy | PP-OCRv6, ML Kit, TrOCR, UniMERNet trên máy [S1–S5] |
| Đối chứng STEM | Mathpix chỉ để benchmark trên dữ liệu có quyền [S7] | — |
| Từ gọi | Keyword spotting trên máy (chọn sau spike) | Model tự huấn luyện giọng trẻ Việt |
| ASR | Dịch vụ server qua adapter | ASR trên máy |
| Tutor | LLM text qua adapter | — |
| Kiểm chứng Toán | Parser allowlist + SymPy, tất định | — |
| Chặn người/khuôn mặt | Face/person detection trên máy (phát hiện, không nhận diện danh tính) | — |
| Thẻ lệnh, dấu bốn góc | Marker detection trên máy | — |

### 6.1. Chính sách chọn model

- Mỗi model đi qua adapter cùng interface; logic nghiệp vụ không gọi API nhà cung cấp trực tiếp.
- Model chỉ được bật khi chạy qua bộ replay và đạt cổng G0 (Business HLD §11.1).
- Hệ thống tự định tuyến; người dùng không chọn model.
- Chỉ dùng nhà cung cấp có cam kết không huấn luyện trên dữ liệu và lưu tối thiểu.
- Mỗi attempt ghi `engine`, `model_version`, `prompt_version`, `policy_version`.
- Có model dự phòng đã qua cổng để chuyển khi nhà cung cấp lỗi hoặc đổi giá.

### 6.2. Yêu cầu với output nhận dạng

- Giữ nguyên những gì trẻ viết; không sửa "2 + 3 = 6" thành 5.
- Trả cấu trúc dòng theo thứ tự đọc, LaTeX cho biểu thức, token không chắc chắn kèm các cách đọc thay thế.
- Phân biệt vùng text/công thức/không hỗ trợ.
- Prompt nhận dạng không được yêu cầu model giải bài; chỉ chép lại.

## 7. Contract client–server

### 7.1. API

| API | Mục đích |
| --- | --- |
| POST /v1/sessions | Tạo buổi học đã xác thực |
| POST /v1/sessions/{id}/voice | Gửi đoạn âm thanh sau từ gọi → transcript + intent |
| POST /v1/sessions/{id}/attempts | Nộp Kiểm tra/Trợ giúp: multipart gồm metadata JSON + ảnh đã cắt |
| POST /v1/attempts/{id}/clarify | Gửi câu trả lời xác nhận (từ ASR) |
| GET /v1/attempts/{id} | Trạng thái và kết quả (SSE hoặc polling) |
| POST /v1/attempts/{id}/cancel | Hủy attempt |
| POST /v1/worksheets/{id}/submissions | Nộp ảnh phiếu bài |
| POST /v1/sessions/{id}/end | Kết thúc; kết quả pending thành lỗi thời |
| GET /v1/students/{id}/reports | Báo cáo theo quyền |
| GET /v1/students/{id}/worksheets | Danh sách phiếu bài, PDF |
| POST /v1/parent-view/token | Token xem ảnh gần trực tiếp theo parent–student–session |
| POST /v1/students/{id}/consents | Ghi hoặc rút đồng ý loại 1/loại 2 (U16, U17) |
| GET /v1/students/{id}/export | Xuất toàn bộ dữ liệu của học sinh (U17) |
| DELETE /v1/students/{id}/data | Xóa dữ liệu của học sinh (U17) |
| PUT /v1/students/{id}/retention | Chỉnh thời hạn lưu ảnh (U17) |

POST attempts trả `202` kèm `attempt_id`.

### 7.2. Metadata attempt (phần JSON)

~~~json
{
  "schema_version": "1.1",
  "event_id": "evt_001",
  "session_id": "ses_001",
  "problem_id": "prob_001",
  "page_id": "page_1",
  "submission_revision": 3,
  "intent": "CHECK",
  "trigger": "VOICE",
  "voice_transcript": "cô ơi kiểm tra giúp con",
  "problem_hint": { "spoken_number": "câu 3", "circled_number_detected": true },
  "capture": {
    "image_count": 1,
    "crop": "PAGE_CORNERS",
    "person_check": "PASSED",
    "quality": { "blur": 0.08, "occlusion": 0.0 }
  },
  "client": { "app_version": "0.1.0", "device_tier": "B" }
}
~~~

`trigger` nhận `VOICE`, `CARD` hoặc `SCREEN` (chỉ phụ huynh/khẩn cấp). Server **từ chối ảnh** nếu `person_check` khác `PASSED`, và giới hạn kích thước/số ảnh.

### 7.3. Response

`attempt_id`, `revision`, `evidence_status`, `answer_status`, `reasoning_status`, `feedback_type`, `target_line`, `hint_level`, `speech_text`, `display_text`, `clarification` (câu hỏi đóng và các lựa chọn, nếu có), `policy_version`, usage nội bộ.

`speech_text` dùng cho TTS: đọc Toán bằng lời, không đọc LaTeX. `display_text` hiện chữ to trên màn hình.

### 7.4. Idempotency và kết quả lỗi thời

- Idempotency key theo user/session/event_id kèm fingerprint; cùng key khác payload trả conflict.
- Retry cùng logical event không tạo gợi ý mới. Nhiều lần gọi khi đang chờ được gộp.
- Cache transcription theo student + problem + revision + hash ảnh + version model; không cache gợi ý chỉ theo hash.
- Client và server đều kiểm tra session/revision trước khi phát phản hồi.

## 8. Backend

### 8.1. Đường xử lý attempt

Auth/schema/size gate → lưu ảnh (object storage, TTL) → `RecognitionEngine` → evidence gate → math validator → skill lookup/history → hint policy → tutor LLM khi cần → output filter → TTS → persist/result.

Những phần xử lý được bằng code tất định thì không dùng LLM: idempotency, quyền, history, parse, số học, lifecycle, TTL, rate limit, intent cho lệnh khớp luật.

### 8.2. Evidence gate

- Thiếu đề hoặc thiếu dòng liên quan → yêu cầu bổ sung (nhắc bằng giọng nói).
- Token không chắc chắn ảnh hưởng kết luận → câu hỏi đóng cho trẻ trả lời bằng giọng nói. Câu trả lời ghi provenance `STUDENT_CONFIRMED`.
- Không đủ evidence → prompt kỹ thuật, không tính là gợi ý Toán.

### 8.3. Math validator

- Parse biểu thức trong allowlist; không eval text/LaTeX tùy ý.
- Giới hạn độ sâu, độ dài, thời gian chạy; SymPy trong process có timeout.
- So sánh từng bước trên tập nghiệm và điều kiện xác định; xác định **dòng sai gốc** (lỗi ở dòng 2, phép chia ở dòng 3 hợp lệ trên giá trị sai).
- Cách giải ngoài phạm vi → `reasoning_status = UNKNOWN`.

### 8.4. Tutor và policy

- Policy chọn L1/L2/L3 theo bằng chứng, history và episode. L3 chỉ khi trẻ chủ động hỏi thêm.
- LLM nhận transcription nguyên trạng, kết quả validator, history, mức gợi ý cho phép, **bảng thuật ngữ SGK lớp 6–7**. Bài làm là dữ liệu, không phải lệnh.
- Ưu tiên template đã được giáo viên duyệt cho dạng bài hẹp; LLM chỉ khi template không phù hợp.
- Output filter: đúng mức gợi ý, không chứa đáp án cuối ở L1/L2, khớp kết quả validator, không ngoài lề, độ dài nói ≤ ~2 câu.

### 8.5. Worksheet generator

- Template theo dạng bài; tham số chọn để nghiệm phù hợp lớp 6–7.
- Đáp án kiểm bằng SymPy; template mới cần giáo viên duyệt.
- PDF A4 có dấu bốn góc, mã phiếu, số câu rõ ràng.
- Bài nộp từ phiếu đi qua cùng đường attempt, kèm `worksheet_id` và số câu.

### 8.6. Báo cáo

- Báo cáo sau buổi tạo khi End; báo cáo tuần chạy theo lịch.
- Chỉ báo "cần luyện" khi lỗi cùng kỹ năng lặp ở ≥ 3 bài qua ≥ 2 buổi (cấu hình).
- Kênh thông báo tới phụ huynh (ví dụ Zalo) chờ chốt.

### 8.7. Data store

| Store | Dữ liệu | MVP |
| --- | --- | --- |
| Transaction DB | User, student, session, attempt, result, episode, consent, worksheet | PostgreSQL managed |
| Object storage | Ảnh đã cắt (TTL 7 ngày), PDF phiếu | S3 hoặc tương đương với lifecycle rule |
| Job queue | Attempt, report, worksheet | Queue bền vững |
| Cache | Idempotency, state ngắn hạn | Redis khi cần |
| Replay dataset | Ảnh có đồng ý loại 2, nhãn | Bucket riêng, quyền riêng, xóa được |

## 9. Stack và deployment cho pilot

- **App học sinh:** Flutter cùng native modules (Kotlin cho Android, Swift cho iOS) cho camera, từ gọi, marker và person detection. **Pilot chạy trên cả Android và iOS** (D19).
- **Phát hành pilot:** Google Play internal/closed testing và TestFlight. Bản TestFlight cho tester bên ngoài cần qua bước duyệt beta của Apple; tính thời gian này vào tuần 5.
- **Lưu ý iOS:** app không tự bật Focus/Không làm phiền; app phải ở foreground; thông báo xin quyền camera và micro phải rõ mục đích; test pin/nhiệt riêng trên iPhone.
- **Web phụ huynh:** web app responsive; báo cáo, phiếu PDF, ảnh gần trực tiếp, quản lý dữ liệu và đồng ý.
- **Backend:** API + worker trong Docker trên EC2; PostgreSQL managed; S3; queue managed. Một môi trường pilot, một môi trường dev.
- Secrets và provider keys chỉ ở server.

## 10. Capacity và chi phí cho pilot

Giả định: 50 học sinh × 1 giờ/ngày × 20 ngày = 1.000 giờ học/tháng; 18 trigger/giờ (12 kiểm tra + 4 kiểm tra lại + 2 trợ giúp, fixture từ v1.0); 1–2 ảnh/trigger, ~200–400 KB/ảnh.

| Chỉ số | Ước tính/tháng |
| --- | --- |
| Trigger | ~18.000 |
| Ảnh gửi lên | ~18.000–36.000 |
| Dung lượng ảnh | ~4–15 GB (lưu tối đa 7 ngày) |
| Đoạn âm thanh lệnh | ~20.000–30.000 đoạn, mỗi đoạn vài giây |

Chi phí model chưa có báo giá. Công thức ở Business HLD §9.2. Tải này rất nhỏ với một EC2 và DB managed cỡ nhỏ; nút thắt có thể là quota và độ trễ của nhà cung cấp model, không phải hạ tầng.

Sizing 1.000 → 100.000 active ở Phụ lục A.

## 11. NFR, an toàn dữ liệu và quan sát

| Hạng mục | Gate |
| --- | --- |
| Rảnh tay | 0 bước bắt buộc chạm máy trong buổi học; đo số lần chạm thực tế |
| Độ trễ | p95 kết thúc lệnh → âm báo đã nghe ≤ 1 giây; → bắt đầu câu phản hồi ≤ 5 giây |
| Giọng nói | Lệnh hiểu đúng lần đầu ≥ 90%; kích hoạt nhầm < 1 lần/giờ |
| Evidence | Mẫu không đủ bằng chứng không bị kết luận sai |
| Thiết bị | Buổi học 45–60 phút có cắm sạc trên cả Android và iOS: đo nhiệt, RAM, crash, độ trễ |
| Isolation | Không truy cập chéo học sinh; không phát phản hồi sang revision/session khác |
| Privacy | 0 frame có người tới server; ảnh tự xóa đúng TTL; không log ảnh hoặc audio |

- TLS; mã hóa DB và object storage; phân quyền trên từng object.
- Log `event_id`, versions, độ tin cậy, latency từng stage, tokens/cost, outcome. Raw transcript chỉ trong debug có quyền và TTL.
- Provider timeout: phát câu mẫu "Cô chưa xem được, con đợi chút nhé" hoặc báo lỗi; không đoán kết quả.

## 12. Bộ replay và kiểm chứng

- **Tuần 1:** 100–200 bài làm thật của trẻ lớp 6–7 (ảnh chụp từ giá đỡ, có cả sai, tẩy xóa, ánh sáng kém) để spike chọn model vision.
- **Tuần 2–5:** mở rộng lên 200–300 bài; giáo viên gán nhãn transcription, dòng sai gốc, gợi ý phù hợp.
- **Âm thanh:** 20–30 trẻ nói bộ lệnh trong phòng thường, có TV/tiếng ồn, để đo từ gọi và ASR.
- **Harness:** chạy ảnh và âm thanh qua hệ thống, chấm tự động theo acceptance, báo cáo theo `model_version`/`policy_version`.

Metrics: exact-match transcription theo dòng; lỗi dấu âm/phân số; false acceptance; tỷ lệ hỏi lại; sai chấm do nhận dạng tách khỏi sai chấm do validator/tutor; tỷ lệ lệnh hiểu đúng; kích hoạt nhầm/giờ.

Nhận dạng trên máy (R&D) tái dùng bộ replay có đồng ý; không thuộc lộ trình 10 tuần.

## 13. Lộ trình kỹ thuật 10 tuần

10 tuần từ kickoff đến go/no-go, trên cả Android và iOS (Business HLD §11).

| Tuần | Bàn giao | Gate |
| --- | --- | --- |
| 1 | Spike model vision trên 100–200 mẫu; spike từ gọi "Cô ơi"/ASR giọng trẻ trên Android và iPhone; adapter skeleton; repo, CI | **S**: chọn model vision và phương án từ gọi |
| 2 | Client Flutter + native Android/iOS: khung hình, tự bắt đầu, chặn người, cắt trang, từ gọi. Backend: session, attempt, storage TTL | "Nói → chụp → nhận dạng" chạy trên cả hai nền tảng |
| 3 | Validator, evidence gate, policy, tutor, output filter, TTS, xác nhận bằng giọng nói | Vertical slice đầy đủ một dạng bài |
| 4 | Report, web phụ huynh, ảnh gần trực tiếp, worksheet cơ bản, thẻ lệnh, đồng ý, xuất/xóa dữ liệu | Đủ tính năng MVP |
| 5 | Harness replay; test máy thật 45–60 phút trên cả hai nền tảng; phát hành TestFlight và Google Play testing | **G0** |
| 6 | Alpha 5 gia đình (cả Android và iOS); sửa lỗi | **G1** |
| 7–10 | Pilot 15 → 50; theo dõi chi phí, độ trễ, kích hoạt nhầm theo nền tảng; sửa nóng; dạng bài thứ 2–3 nếu đạt | **G2** giữa tuần 7; go/no-go cuối tuần 10 |

## 14. Checklist cho coding agent

- Đọc cả hai HLD v1.1, kiểm tra repo/tests trước; không nhận tính năng đã hoàn thành.
- Tạo interface `RecognitionEngine`, `SpeechRecognizer`, `IntentClassifier`, `TutorProvider`, `TtsProvider`, `MathValidator`, `WorksheetGenerator`; policy có version.
- Dùng fake adapter để kiểm tra vertical slice; không trình bày output fake như kết quả thật.
- Server từ chối ảnh khi `person_check != PASSED`, payload quá giới hạn, hoặc session không hợp lệ.
- Không tạo session, không bật camera/micro khi chưa có đồng ý loại 1. Ảnh chỉ vào bộ replay khi có đồng ý loại 2.
- Mọi luồng trong buổi học phải có đường không chạm; test tự động kiểm tra không có bước UI bắt buộc.
- Test: dấu âm mất, phân số sai, thiếu dòng, đổi trang khi đang chờ, che tay, có người vào khung, kích hoạt nhầm, barge-in, mất mạng, provider timeout, End khi đang chờ.
- Không triển khai: camera chạy ngầm, ASR luôn bật gửi server, chặn cứng sau ba lần trợ giúp, chấm điểm tập trung, lời giải đầy đủ tự động.
- Báo code đã đổi, test đã chạy, benchmark đã đo, giới hạn và bước tiếp theo.

## 15. State machine và acceptance

| State | Điều kiện / chuyển tiếp |
| --- | --- |
| WAITING_FOR_DESK | App mở; chờ đủ 4 góc trang, máy đứng yên, không có người → READY |
| READY | Chào → WORKING |
| WORKING | Quan sát nhẹ; lệnh/thẻ Kiểm tra hoặc Trợ giúp → CAPTURING; idle → IDLE_OFFER |
| IDLE_OFFER | Hỏi một lần bằng giọng nói; "con nghĩ tiếp" → WORKING (cooldown); "giúp con" → CAPTURING |
| CAPTURING | Chờ ổn định, không tay che, kiểm tra người → UPLOADING; quá timeout → nhắc, ở lại CAPTURING |
| UPLOADING / CHECKING / HELPING | Server xử lý; revision và deadline được kiểm tra |
| NEEDS_CLARIFICATION | Câu hỏi đóng bằng giọng nói; trả lời → CHECKING/HELPING; không trả lời → nhắc viết rõ lại → WORKING |
| SPEAKING | Phát TTS; barge-in → WORKING |
| NEEDS_REVISION | Phản hồi lỗi có evidence; trẻ sửa → WORKING |
| VERIFIED | Đúng đầy đủ trong phạm vi kiểm tra; bài mới → WORKING |
| PAUSED / ENDED | Dừng camera, micro, timer, TTS; End làm output pending lỗi thời |

### 15.1. Acceptance matrix

| ID | Tình huống | Assertion |
| --- | --- | --- |
| A01 | Bắt đầu/tạm dừng/kết thúc bằng giọng nói | Không cần chạm; indicator đúng; End dừng capture/mic/TTS |
| A02 | Trẻ làm đúng hoặc tự sửa trước khi gọi | 0 lần gọi server phân tích; 0 lời nói về bài |
| A03 | Kiểm tra: 3x + 5 = 20 → 3x = 25 → x = 25/3 | Chỉ dòng 2 là lỗi gốc; không đọc đáp án; dùng ngôn ngữ SGK lớp 6–7 |
| A04 | Idle 60 giây | Một câu hỏi mẫu tại máy; 0 gọi cloud; có cooldown |
| A05 | Trợ giúp có/không có history | Đúng student/skill; thiếu history vẫn giúp được |
| A06 | Gọi ba lần khi đang chờ | Một logical request, không ba gợi ý |
| A07 | Trợ giúp mới trên bài không đổi | Intent mới được xử lý; dùng lại transcription |
| A08 | Chữ 15/18 không rõ | Câu hỏi xác nhận bằng giọng nói; không phán sai trước khi rõ |
| A09 | Trẻ viết "2 + 3 = 6" | Transcription giữ 6 |
| A10 | Mất dấu âm/phân số hoặc thiếu dòng | Evidence gate ghi uncertainty; không xác nhận đầy đủ |
| A11 | Đáp án đúng, thiếu dòng giữa | answer và reasoning khác trạng thái |
| A12 | Đổi trang/revision/End khi đang chờ | Bỏ output cũ |
| A13 | Mất mạng/reconnect | Retry giới hạn cùng key; không phát hàng loạt bài cũ; báo trạng thái bằng giọng nói |
| A14 | Ba lần trợ giúp cùng kỹ năng | Xem lại tiến triển; không chặn |
| A15 | Phụ huynh xem từ xa | Đúng parent–student–session; máy con hiện chỉ báo; End ngắt xem |
| A16 | Báo cáo | Tổng outcome khớp event; retry không đếm hai lần |
| A17 | Payload bất thường hoặc text độc hại trong bài | Từ chối khi thiếu person_check; parser allowlist/timeout; bài làm không điều khiển prompt |
| A18 | Provider timeout/quota | Không giả vờ đã chấm; câu mẫu báo chờ; chuyển model dự phòng nếu có |
| A19 | Model mới | Phải qua bộ replay và cổng G0 trước khi bật |
| A20 | Câu hỏi ngoài lề | Từ chối nhẹ nhàng, đưa về bài |
| **A21** | Cả buổi học 45 phút | 0 bước bắt buộc chạm máy từ READY đến ENDED |
| **A22** | Từ gọi trong phòng có TV/anh chị em | Kích hoạt nhầm < 1 lần/giờ trên tập test |
| **A23** | Lệnh của trẻ lớp 6–7 | Hiểu đúng lần đầu ≥ 90% trên tập test |
| **A24** | Barge-in "Cô ơi, dừng" | TTS dừng ≤ 500 ms |
| **A25** | Vở lệch trong ngưỡng / ngoài ngưỡng | Trong ngưỡng: tự bù, không nhắc. Ngoài ngưỡng: nhắc xê dịch vở, không nhắc chỉnh máy |
| **A26** | Có người hoặc khuôn mặt trong khung | Frame không rời máy; server không nhận; ghi event chặn |
| **A27** | Phiếu bài | 0 đề/đáp án sai trên tập sinh thử; chụp lại nhận đúng mã phiếu và số câu |
| **A28** | Thẻ lệnh | Giữ thẻ 1 giây → đúng intent; lướt qua nhanh không kích hoạt |
| **A29** | Ảnh tự xóa | Ảnh quá 7 ngày (hoặc cài đặt phụ huynh) không còn trong storage |
| **A30** | Đồng ý (U16) | Chưa có đồng ý loại 1: không tạo session, không bật camera/micro. Tắt đồng ý loại 2: ảnh mới không vào bộ replay, ảnh cũ trong replay bị xóa |
| **A31** | Xuất và xóa dữ liệu (U17) | Bản xuất đủ attempt, báo cáo, phiếu bài; sau khi xóa, không còn ảnh, attempt, báo cáo của học sinh trong DB và storage (trừ log kỹ thuật đã ẩn danh) |

A03, A08, A10, A22, A23 cần ground truth thật (ảnh, âm thanh, nhãn giáo viên), không chỉ mock.

## 16. Nguồn tham khảo

- [S1] PaddleOCR, PP-OCRv6: https://github.com/PaddlePaddle/PaddleOCR
- [S2] ML Kit Text Recognition: https://developers.google.com/ml-kit/vision/text-recognition/v2/languages
- [S3] ML Kit Digital Ink: https://developers.google.com/ml-kit/vision/digital-ink-recognition
- [S4] Microsoft TrOCR: https://github.com/microsoft/unilm/tree/master/trocr
- [S5] UniMERNet: https://github.com/opendatalab/UniMERNet
- [S6] ONNX Runtime Mobile: https://onnxruntime.ai/docs/tutorials/mobile/
- [S7] Mathpix OCR API: https://mathpix.com/ocr

S1–S6 thuộc hướng R&D nhận dạng trên máy. License của từng model/checkpoint phải được rà soát trước khi phân phối.

## Phụ lục A. Sizing khi mở rộng (không thuộc MVP)

Với 18 trigger/giờ và 1–2 ảnh ~200–400 KB mỗi trigger:

| Active cùng lúc | Trigger/giây | Ảnh vào (ước tính) |
| ---: | ---: | ---: |
| 1.000 | 5 | ~1–4 MB/s |
| 10.000 | 50 | ~10–40 MB/s |
| 100.000 | 500 | ~100–400 MB/s |

Ở quy mô 10.000 active trở lên, chi phí và băng thông ảnh trở nên đáng kể. Đây là lúc đánh giá lại nhận dạng trên máy (R&D §6) để chỉ gửi JSON như thiết kế v1.0. Quyết định chuyển phải dựa trên số đo pilot và benchmark trên máy thật, không dựa trên fixture.
