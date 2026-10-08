# Technical HLD — AI Study Companion

**Phiên bản:** 1.3  
**Ngày:** 08/10/2026  
**Chủ dự án:** Sơn  
**Tài liệu đồng hành:** [Business HLD v1.3](business-hld-v1.3.md)  
**Thay thế:** Technical HLD v1.2 ngày 07/10/2026 (`history/technical-hld-v1.2.md`)  
**Trạng thái:** Thiết kế đề xuất cho MVP pilot 50 gia đình, Toán lớp 6 HK1 (SGK Cánh diều); chưa có code, benchmark hay capacity đã xác nhận.

## 0. Baseline và quy tắc dùng tài liệu

Bảng quyết định **D01–D31**, quy tắc đánh mã và bảng đối chiếu nằm ở [Business HLD v1.3 §0](business-hld-v1.3.md). Use case **U01–U25** ở Business HLD §5.3. Acceptance **A01–A46** ở §15 của tài liệu này; A01–A42 giữ số của v1.2.

Các quyết định ảnh hưởng mạnh nhất tới kiến trúc:

- **D02/D03:** lệnh giọng nói, không chạm máy, kể cả bước chụp đề.
- **D04/D05/D26:** ảnh vùng giấy đã cắt lên server; ẩn danh hóa; Anthropic (Claude) chỉ dùng để nhận dạng ảnh qua adapter.
- **D10–D15:** Toán lớp 6 HK1 Cánh diều; tờ đề 1 trang; phạm vi đã học; lưu và học tiếp; trẻ ghi số câu trong vở.
- **D16/D17/D20:** phiếu bài hệ thống; ảnh gần trực tiếp; ảnh xóa sau 7 ngày.
- **D23/D24/D27/D28:** Android 15+, iOS 18.7+; "Cô ơi"; ASR Viettel AI, TTS Azure; Python/FastAPI, React, Flutter.
- **D25:** shadow teacher rà và gán nhãn phản hồi AI.
- **D30:** chấm hình học sau pilot; validator theo domain có registry.
- **D31:** không LLM sinh lời; template đã duyệt hoặc "cần xem lại"; intent theo bộ luật.

### 0.1. Thay đổi kiến trúc so với v1.2

| Thành phần | v1.2 | v1.3 |
| --- | --- | --- |
| Chụp đề | Nhiều trang, "Hết rồi ạ" | 1 trang; chụp xong là xác nhận |
| Xác định câu | Lệnh "Câu N" hoặc khoanh số | Nhận dạng số câu ở lề trái vở + lệnh "Câu N" dự phòng (§5.3, §8.3) |
| Nhà cung cấp | Chưa chọn | Anthropic (ảnh), Viettel AI (ASR), Azure Neural TTS (TTS) |
| Bảo vệ dữ liệu | Chặn người trên máy | Thêm ẩn danh hóa trên server trước khi gọi Anthropic (§5.7) |
| Math validator | Một bộ chấm | Registry theo domain; MVP: số học/đại số; hình học sau pilot (§8.5) |
| Chất lượng | Giáo viên gán nhãn replay | Thêm hàng rà soát shadow teacher cho mọi phản hồi pilot (§8.11) |
| Tutor | LLM viết lời khi template không phù hợp | Chỉ template đã duyệt; không có template → "cần xem lại" (D31) |

## 1. Quyết định kiến trúc

1. **Rảnh tay là ràng buộc cứng.** Mọi bước trong buổi học, kể cả chụp đề và xác nhận bộ đề, có đường không cần chạm: giọng nói, giấy hoặc thẻ lệnh.
2. **Buổi học bắt đầu bằng bộ đề.** Không mở trạng thái làm bài khi bộ đề và phạm vi đã học chưa được xác nhận.
3. **Trigger gửi ảnh:** chụp trang đề, lệnh Kiểm tra, lệnh Trợ giúp, chụp phiếu bài, phụ huynh đang xem. Idle ~60 giây chỉ phát câu hỏi mẫu tại máy.
4. **Client lọc trước khi gửi:** chất lượng, che tay, chặn người/khuôn mặt, cắt và chỉnh phối cảnh vùng giấy. Frame có người không rời máy.
5. **Server nhận ảnh đã cắt, ẩn danh hóa** (§5.7), rồi gọi Claude (Anthropic) qua `RecognitionEngine` adapter. Anthropic chỉ nhận ảnh trang giấy.
6. **Chấm Toán tất định:** `ValidatorRegistry` chọn bộ chấm theo domain của item. MVP có bộ số học/đại số (parser allowlist + SymPy). Item không có bộ chấm → `UNSUPPORTED`. Thêm hình học sau pilot là thêm một bộ chấm, không đổi pipeline (D30).
7. **Gợi ý giới hạn trong phạm vi đã học:** retrieval lọc theo `learned_scope_version` trước; output gate chặn kiến thức/phương pháp ngoài phạm vi; LLM không tự mở rộng phạm vi.
8. **Lời phản hồi chỉ lấy từ template giáo viên đã duyệt (D31).** MVP không dùng LLM sinh lời; không có template phù hợp → cô báo "cần xem lại", ghi log và đưa vào hàng rà soát của shadow teacher (§8.11) để bổ sung template. Output filter kiểm tra mức gợi ý, lộ đáp án, ngoài lề, ngoài phạm vi.
9. Từ gọi nhận diện trên máy; chỉ đoạn sau từ gọi (hoặc câu trả lời xác nhận) gửi lên ASR Viettel AI. TTS Azure Neural (giọng nữ tiếng Việt) là kênh phản hồi chính.
10. UNKNOWN không thành WRONG; nhận dạng không tự sửa phép tính sai.
11. Backend modular monolith cùng worker (Python + FastAPI). Không microservice trong MVP.
12. **Mọi phản hồi AI trong pilot được lưu đủ để shadow teacher rà lại** (§8.11); rà soát không chặn đường phản hồi tới trẻ.

## 2. Phạm vi MVP

**Có:** buổi học rảnh tay; chụp 1 trang đề và xác nhận câu/ý bằng giọng nói; phạm vi đã học có version; đọc số câu trẻ ghi trong vở, lệnh "Câu N" dự phòng; Kiểm tra/Trợ giúp; xác nhận chữ bằng giọng nói; history theo kỹ năng; lưu tiến độ và học tiếp; báo cáo theo tờ đề; phiếu bài hệ thống; ảnh gần trực tiếp; thẻ lệnh; liên kết tài khoản, đồng ý, xem/xuất/xóa dữ liệu; ẩn danh hóa ảnh; màn hình rà soát của shadow teacher.

**Nội dung:** Toán lớp 6 học kỳ 1, SGK Cánh diều. Chấm phần số học và đại số; câu hình học có trong đề nhưng `UNSUPPORTED`. Kho kiến thức và support matrix theo mục lục Cánh diều do shadow teacher lập.

**Không có:** lớp 7 trở lên; học kỳ 2; chấm hình học (sau pilot); đề nhiều trang; câu có hình/bảng cần đọc (giữ trạng thái chưa hỗ trợ); camera chạy ngầm; live video; nhận dạng trên máy; ASR luôn bật; giao diện giáo viên cho cả lớp.

## 3. Kiến trúc logic

~~~mermaid
flowchart TD
  subgraph Client["App học sinh (trên giá đỡ)"]
    Cam["Camera"]
    Frame["4 góc trang, bù lệch"]
    Guard["Chất lượng, che tay, chặn người/khuôn mặt"]
    Crop["Cắt và chỉnh phối cảnh trang"]
    Wake["Từ gọi 'Cô ơi' trên máy"]
    Card["Nhận thẻ lệnh"]
    Idle["Idle timer"]
    Speak["Phát TTS, barge-in"]
    Cam --> Frame --> Guard --> Crop
    Cam --> Card
  end
  subgraph Server["Backend"]
    API["API: xác thực, session, run, version"]
    ASR["ASR Viettel AI + intent"]
    DeID["Ẩn danh hóa ảnh"]
    Rec["RecognitionEngine (Claude)"]
    Item["Xác định item: số câu trong vở / lệnh"]
    Review["Hàng rà soát shadow teacher"]
    PS["Problem set builder: tách câu/ý, manifest"]
    Scope["Scope gate: kỹ năng, phạm vi đã học"]
    Gate["Evidence gate"]
    Val["ValidatorRegistry: số học/đại số (MVP), hình học (sau pilot)"]
    Pol["History + hint policy"]
    KS["Knowledge store lớp 6 (lọc theo scope)"]
    Tut["Tutor LLM + output filter"]
    TTS["TTS Azure Neural"]
    WS["Worksheet generator"]
    Rep["Report worker"]
    DB["PostgreSQL"]
    Obj["Object storage (ảnh, TTL 7 ngày)"]
    API --> DeID --> Rec
    Rec --> PS --> Scope
    Rec --> Item --> Gate --> Val --> Pol --> Tut --> TTS
    DB --> Review
    KS --> Pol
    KS --> Scope
    Pol <--> DB
    Rec --> Obj
    DB --> Rep
    DB --> WS
  end
  Wake -->|đoạn sau từ gọi| ASR --> API
  Card -->|intent| API
  Crop -->|trang đề / lời giải khi có trigger| API
  TTS -->|audio + text| Speak
  Idle -->|câu hỏi mẫu tại máy| Speak
  Rep --> Parent["Web phụ huynh / giáo viên"]
  WS --> Parent
  Review --> Parent
  Crop -->|ảnh thưa khi phụ huynh xem| Parent
~~~

## 4. Giọng nói và rảnh tay

### 4.1. Vòng đời buổi học không chạm

| Bước | Cơ chế |
| --- | --- |
| Bắt đầu | Màn hình chờ kiểm tra: máy đứng yên ≥ 3 giây, ánh sáng đạt, không có người trong khung → chào. Nếu có đề dở dang thì hỏi học tiếp |
| Chụp đề | Thấy đủ 4 góc trang ổn định ≥ 2 giây và không che tay → tự chụp, âm báo ngắn, nói "Cô chụp xong đề rồi". MVP chỉ nhận 1 trang; nếu trẻ đặt trang thứ hai, cô nói "Mỗi buổi cô chỉ chấm một trang đề" và giữ trang đầu |
| Xác nhận bộ đề | Server trả danh sách câu/ý; cô đọc "Cô thấy 10 câu. Đúng không con?"; mở ASR không cần từ gọi ~8 giây. "Thiếu câu 4" → nhờ đặt lại trang đề cho thẳng và đủ sáng. Token đề không chắc → câu hỏi đóng |
| Báo trước câu chưa hỗ trợ | Cô nói ngắn câu nào chưa chấm được hoặc cần xem lại phạm vi; vẫn giữ trong đề |
| Xác định câu | Trẻ ghi số câu ở lề trái vở trước khi làm (`3)`); khi có trigger, server đọc số câu gần vùng lời giải. Lệnh "Câu 3", "Câu 2 ý b" vẫn dùng được và được ưu tiên khi số trong vở không rõ hay mâu thuẫn |
| Lệnh | Từ gọi → ghi đoạn tối đa ~6 giây hoặc tới khi VAD im lặng → ASR → intent |
| Tự chụp lời giải | Sau Kiểm tra/Trợ giúp: chờ trang ổn định, không tay che (timeout ~5 giây, quá thì nhắc) |
| Xác nhận chữ | Câu hỏi đóng; ASR không cần từ gọi ~8 giây |
| Lệch giấy | Bù phối cảnh trong ngưỡng; ngoài ngưỡng nhắc xê dịch giấy |
| Barge-in | Từ gọi hoặc "dừng" khi đang phát → dừng, hủy câu còn lại |
| Kết thúc | "Con học xong rồi" / thẻ XONG; hết thời lượng dự kiến (30–45 phút, cấu hình) → cô đề nghị lưu; không hoạt động 10 phút → hỏi → tự kết thúc. Luôn lưu tiến độ |

Nút Pause/End hiện trên màn hình cho phụ huynh và trường hợp khẩn cấp, không bắt buộc.

### 4.2. Từ gọi và ASR

- Từ gọi **"Cô ơi"** (D24) nhận diện trên máy. Vì là cụm từ trẻ hay nói, phải đo kích hoạt nhầm (TV, anh chị em, trẻ gọi người nhà); có thể thêm bước xác nhận ý định ngắn.
- Chưa xác nhận có thư viện từ gọi tiếng Việt đạt chất lượng với giọng trẻ trên cả Android và iOS. Spike tuần 1 so sánh: thư viện keyword spotting có custom wake word; model nhỏ tự huấn luyện; phương án VAD + ASR server (chỉ khi hai phương án đầu không đạt).
- ASR: **Viettel AI** qua adapter `SpeechRecognizer`. Phải đo trên giọng trẻ lớp 6 trong spike tuần 1. Không lưu audio mặc định; lưu transcript lệnh trong event.
- Intent: bộ luật cho tập lệnh ở Business HLD §5.2 (gồm "Đúng rồi ạ", "Thiếu câu N", "Câu N ý x"). Không khớp thì hỏi lại; MVP không phân loại intent bằng LLM (D31).

### 4.3. Thẻ lệnh

Ba thẻ in KIỂM TRA, GIÚP CON, XONG, có marker (ArUco/AprilTag) và chữ in to. Nhận trên máy; giữ ổn định ~1 giây mới kích hoạt.

### 4.4. TTS

TTS: **Azure Neural TTS, giọng nữ tiếng Việt**, qua adapter `TtsProvider`; cache câu mẫu trên máy (chào, nhắc đặt trang, nhắc bỏ tay, nhắc xê dịch giấy, câu hỏi idle, báo mất mạng). Đọc biểu thức Toán bằng lời tiếng Việt.

## 5. Pipeline client

### 5.1. Chụp đề đầu buổi

1. Tạo session ở trạng thái `SETUP`.
2. Với trang đề (MVP: 1 trang): phát hiện 4 góc → ổn định, không tay che → **chặn người** → cắt, chỉnh phối cảnh → gửi `prompt-pages` kèm `page_order = 1`. Server từ chối trang thứ hai trong MVP.
3. Gửi yêu cầu dựng bộ đề ngay sau khi trang được nhận.
4. Nhận danh sách câu/ý và các token không chắc → điều phối xác nhận bằng giọng nói (§4.1).
5. Xác nhận xong → `problem-set/confirm` → `READY`.

QR, mã đề hay template là tối ưu tùy chọn để đối chiếu, không bắt buộc. Câu có hình/bảng thiết yếu mà hệ thống không biểu diễn được giữ placeholder và `support_status = UNSUPPORTED`, không biến thành câu text đầy đủ.

### 5.2. Quan sát nhẹ trong buổi học

Camera → mẫu độ phân giải thấp (giả thuyết 2 khung hình/giây) → 4 góc trang → che tay/chất lượng → thay đổi nét viết → idle timer. Không gửi gì lên server.

### 5.3. Khi có Kiểm tra/Trợ giúp

1. Khóa snapshot với `run_id`, `problem_set_version`, `submission_revision`, và `item_id` nếu trẻ đã nói "Câu N" (nếu không thì `null`).
2. Chờ ổn định, không tay che; **chặn người**.
3. Cắt vùng lời giải trong vở, **gồm cả lề trái có số câu**; gửi ảnh kèm metadata. Server đọc số câu và gắn item (§8.3); không đọc được hoặc không khớp bộ đề → cô hỏi "Con đang làm câu mấy?". Đề lấy từ bộ đề đã xác nhận, **không đọc lại đề mỗi lần Kiểm tra**, chỉ chụp lại khi cần sửa đề.
4. Nhận phản hồi; bỏ phản hồi nếu câu, trang hoặc revision đã đổi.

### 5.4. Chụp phiếu bài hệ thống

Phiếu có dấu bốn góc và mã phiếu. Phát hiện mã phiếu thì bộ đề lấy từ phiếu đã sinh, bỏ qua bước dựng đề từ ảnh (vẫn xác nhận trang). "Cô chấm giúp con" → chấm theo câu trên phiếu.

### 5.5. Ảnh gần trực tiếp cho phụ huynh

Chỉ khi phụ huynh đang xem: gửi ảnh vùng giấy đã cắt, độ phân giải thấp, mỗi vài giây, qua cùng bộ chặn người. Máy con hiện chỉ báo. Không dùng để chấm, không lưu quá thời gian xem.

### 5.6. Lifecycle

- App foreground, màn hình sáng (độ sáng thấp). Không cam kết chạy ngầm.
- Checklist trước buổi học: cắm sạc, bật Không làm phiền/Focus (app không tự bật được trên mọi nền tảng, nhất là iOS).
- Pause/End dừng camera, micro, nhận diện, TTS; hủy request đang chờ; **không xóa tiến độ đã lưu**.
- Hàng đợi offline có giới hạn và TTL; reconnect kiểm tra run/revision trước khi gửi.

### 5.7. Ẩn danh hóa trước khi gửi nhà cung cấp (D26)

Chạy trên server, sau khi lưu ảnh gốc (TTL) và trước mọi lời gọi `RecognitionEngine`:

1. Kiểm tra lại `person_check`; ảnh có người → từ chối.
2. Bỏ toàn bộ metadata ảnh (EXIF, GPS, model máy, thời gian).
3. Che vùng có thể chứa thông tin định danh: dải đầu trang vở và đầu tờ đề (tên, lớp, trường). Kích thước dải đo trong spike tuần 1.
4. Request tới Anthropic chỉ có ảnh đã xử lý và prompt chép lại; **không** có `student_id`, `session_id`, `run_id`, tên hay mã thiết bị. Dùng `provider_request_id` ngẫu nhiên; bảng ánh xạ chỉ nằm trong DB của hệ thống.
5. Log ghi hash ảnh đã gửi, không ghi ảnh.
6. Test tự động kiểm tra payload đi ra (A43).

Che dải đầu trang không bảo đảm loại hết tên viết ở chỗ khác; shadow teacher báo khi thấy dữ liệu định danh trong ảnh rà soát.

## 6. Model portfolio

| Thành phần | MVP | R&D dài hạn |
| --- | --- | --- |
| Nhận dạng đề in, bài làm và số câu trong vở | Claude (Anthropic) qua `RecognitionEngine`; model chọn sau spike giữa Opus 5.5, Sonnet 5.5, Haiku 5.5; structured output JSON câu/ý/dòng, LaTeX, nhãn câu, độ tin cậy | PP-OCRv6, ML Kit, TrOCR, UniMERNet trên máy [S1–S5] |
| Đối chứng STEM | Mathpix chỉ benchmark trên dữ liệu có quyền [S7] | — |
| Từ gọi | Keyword spotting trên máy | Model tự huấn luyện giọng trẻ Việt |
| ASR | Viettel AI qua `SpeechRecognizer` | ASR trên máy |
| TTS | Azure Neural TTS, giọng nữ tiếng Việt, qua `TtsProvider` | — |
| Map kỹ năng của câu | Luật + support matrix do shadow teacher duyệt | Model có kiểm soát |
| Tutor | Template đã duyệt, retrieval theo scope (D31) | LLM viết lời sau pilot, nếu có nhà cung cấp được duyệt |
| Kiểm chứng Toán | `ValidatorRegistry`: bộ số học/đại số (parser allowlist + SymPy) | Bộ hình học sau pilot |
| Chặn người/khuôn mặt, marker | Detection trên máy | — |

### 6.1. Chính sách chọn model

- Mọi model qua adapter; logic nghiệp vụ không gọi API nhà cung cấp trực tiếp.
- Model chỉ được bật khi qua bộ replay và cổng G0.
- Hệ thống tự định tuyến; người dùng không chọn model.
- Chỉ nhà cung cấp có cam kết không huấn luyện trên dữ liệu và lưu tối thiểu. Anthropic chỉ nhận ảnh đã ẩn danh hóa (§5.7).
- Mỗi attempt ghi `engine`, `model_version`, `prompt_version`, `policy_version`, `learned_scope_version`.
- Có model dự phòng đã qua cổng.

### 6.2. Yêu cầu với output nhận dạng

- Giữ nguyên những gì trẻ viết ("2 + 3 = 6" giữ 6).
- Đề: số câu, ý con, thứ tự đọc, text/LaTeX, vùng nguồn, độ tin cậy, cờ hình/bảng.
- Bài làm: số câu ghi ở lề trái và vùng của từng câu; dòng theo thứ tự, LaTeX, token không chắc kèm cách đọc thay thế.
- Prompt nhận dạng chỉ yêu cầu chép lại, không giải bài.

## 7. Contract client–server

### 7.1. API

| API | Mục đích |
| --- | --- |
| POST /v1/sessions | Tạo session ở `SETUP` (cần đồng ý loại 1) |
| POST /v1/sessions/{id}/prompt-pages | Gửi ảnh một trang đề đã cắt |
| POST /v1/sessions/{id}/problem-set/build | Dựng bộ đề từ các trang; trả câu/ý và token không chắc |
| PUT /v1/sessions/{id}/problem-set | Sửa bộ đề (từ câu trả lời xác nhận); tạo version mới |
| POST /v1/sessions/{id}/problem-set/confirm | Xác nhận đủ trang/câu và scope; mở `READY` |
| POST /v1/sessions/{id}/voice | Đoạn âm thanh sau từ gọi hoặc câu trả lời xác nhận → transcript + intent |
| POST /v1/sessions/{id}/active-item | Đặt câu/ý đang làm khi trẻ nói "Câu N" (khi dùng số câu trong vở, server tự gắn trong attempt) |
| POST /v1/sessions/{id}/attempts | Kiểm tra/Trợ giúp: multipart metadata JSON + ảnh lời giải |
| POST /v1/attempts/{id}/clarify | Câu trả lời xác nhận chữ |
| GET /v1/attempts/{id} | Trạng thái và kết quả (SSE hoặc polling) |
| POST /v1/attempts/{id}/cancel | Hủy attempt |
| POST /v1/sessions/{id}/end | Kết thúc run; lưu tiến độ; output pending thành lỗi thời |
| POST /v1/sessions/{id}/resume | Khôi phục bộ đề và tiến độ; tạo run mới |
| POST /v1/worksheets/{id}/submissions | Nộp ảnh phiếu bài hệ thống |
| GET /v1/students/{id}/worksheets | Danh sách phiếu, PDF |
| GET / PUT /v1/students/{id}/learned-scope | Xem/cập nhật phạm vi đã học (shadow teacher trong pilot); mỗi lần PUT tạo version |
| GET /v1/students/{id}/reports | Báo cáo theo quyền |
| POST /v1/parent-view/token | Token xem ảnh gần trực tiếp |
| POST /v1/students/{id}/consents | Ghi/rút đồng ý loại 1/loại 2 |
| GET /v1/students/{id}/export | Xuất dữ liệu |
| DELETE /v1/students/{id}/data | Xóa dữ liệu |
| PUT /v1/students/{id}/retention | Chỉnh thời hạn lưu ảnh |
| GET /v1/review/queue | Hàng rà soát của shadow teacher: phản hồi AI chưa gán nhãn, ưu tiên độ tin cậy thấp và sắp hết TTL ảnh |
| GET /v1/review/attempts/{id} | Ảnh (trong TTL), transcription, kết luận validator, gợi ý, versions |
| POST /v1/review/attempts/{id}/labels | Gán nhãn; mỗi lần tạo version nhãn |

Server **từ chối mọi ảnh** khi `person_check != PASSED`, payload quá giới hạn, session/run không hợp lệ, hoặc chưa có đồng ý loại 1.

### 7.2. Metadata attempt (phần JSON)

~~~json
{
  "schema_version": "1.3",
  "event_id": "evt_001",
  "session_id": "ses_001",
  "run_id": "run_002",
  "problem_set_id": "set_001",
  "problem_set_version": 1,
  "learned_scope_version": "scope_stu01_v3",
  "item_id": null,
  "item_selection": "NOTEBOOK_LABEL",
  "submission_revision": 3,
  "intent": "CHECK",
  "trigger": "VOICE",
  "voice_transcript": "cô ơi kiểm tra giúp con",
  "capture": {
    "image_count": 1,
    "surface": "NOTEBOOK",
    "crop": "PAGE_CORNERS",
    "person_check": "PASSED",
    "quality": { "blur": 0.08, "occlusion": 0.0 }
  },
  "client": { "app_version": "0.1.0", "platform": "ios", "device_tier": "B" }
}
~~~

`trigger`: `VOICE`, `CARD` hoặc `SCREEN` (chỉ phụ huynh/khẩn cấp). `surface`: `NOTEBOOK` (mặc định MVP: giải trong vở), `PROMPT_SHEET` hoặc `WORKSHEET`. `item_selection`: `NOTEBOOK_LABEL` (server đọc số câu, `item_id = null`) hoặc `VOICE` (trẻ đã nói "Câu N", `item_id` có giá trị). Server tra đề chuẩn theo `problem_set_version` và `item_id`; không tin nội dung đề do client gửi ngoài luồng PUT problem-set.

### 7.3. Response

`attempt_id`, `revision`, `item_id`, `item_resolution` (`LABEL`, `VOICE`, `ASKED`), `evidence_status`, `answer_status`, `reasoning_status`, `scope_status`, `feedback_type`, `target_line`, `hint_level`, `speech_text`, `display_text`, `clarification`, `item_progress`, `policy_version`, usage nội bộ.

### 7.4. Idempotency và kết quả lỗi thời

- Idempotency key theo user/session/event_id kèm fingerprint.
- Retry cùng logical event không tạo gợi ý mới; nhiều lần gọi khi đang chờ được gộp.
- Cache transcription theo student + item + revision + hash ảnh + version model.
- Client và server kiểm tra run, problem_set_version, item, revision trước khi phát phản hồi.
- Đổi version đề hoặc scope: kết quả phụ thuộc bị đánh dấu cần kiểm tra lại; output pending bị hủy; không xóa lịch sử.

## 8. Backend

### 8.1. Đường xử lý chụp đề

Auth/consent → lưu ảnh trang (TTL) → ẩn danh hóa (§5.7) → `RecognitionEngine` (đề in) → tách câu/ý, thứ tự, cờ hình/bảng → manifest + token không chắc → xác nhận bằng giọng nói → **scope gate** → `READY`.

### 8.2. Scope gate

- Với mỗi item: map kỹ năng/prerequisite; tìm ít nhất một phương pháp giải hợp lệ nằm trong `learned_scope_version`.
- Không chắc → `NEEDS_SCOPE_REVIEW`. Ngoài support matrix → `UNSUPPORTED`. Cả hai vẫn trong bộ đề, không tính đã xác nhận.
- Không suy ra phạm vi từ "lớp 6" hay từ việc trẻ từng làm đúng một bài. Thiếu profile phạm vi thì không mặc định cho phép toàn chương trình.
- Buổi học dùng snapshot scope; đổi scope giữa chừng cần xác nhận lại ở buổi sau.
- Trẻ dùng cách giải đúng ngoài phạm vi: ghi nhận theo policy, không đánh sai chỉ vì khác mẫu; không kiểm chứng được thì `reasoning_status = UNKNOWN`.

### 8.3. Đường xử lý attempt

Auth/schema/size gate → lưu ảnh (TTL) → ẩn danh hóa (§5.7) → `RecognitionEngine` (bài làm + số câu ở lề) → **xác định item** (số câu trong vở khớp bộ đề; nếu có lệnh "Câu N" thì lệnh thắng; không xác định được → hỏi lại) → evidence gate → `ValidatorRegistry` → skill lookup/history → hint policy → retrieval kiến thức lọc theo scope → tutor LLM khi cần → output filter (gồm kiểm tra phạm vi) → TTS → cập nhật ItemProgress → persist/result → đưa vào hàng rà soát (§8.11).

### 8.4. Evidence gate

- Thiếu dòng liên quan → yêu cầu bổ sung (giọng nói).
- Token không chắc ảnh hưởng kết luận → câu hỏi đóng; câu trả lời ghi provenance `STUDENT_CONFIRMED`.
- Không đủ evidence → prompt kỹ thuật, không tính là gợi ý Toán.

### 8.5. Math validator

- `ValidatorRegistry` ánh xạ domain/kỹ năng của item → bộ chấm. Mỗi bộ chấm cài cùng một interface `MathValidator` (đầu vào: đề chuẩn + các dòng đã nhận dạng; đầu ra: `answer_status`, `reasoning_status`, dòng sai gốc, lý do). Item có domain chưa đăng ký → `UNSUPPORTED`.
- MVP đăng ký một bộ: **số học và đại số** HK1. Thêm hình học sau pilot = bộ chấm mới + support matrix + template gợi ý + dữ liệu replay; không sửa pipeline, API hay state machine (D30, A45).
- Parse trong allowlist; không eval text/LaTeX tùy ý.
- Giới hạn độ sâu, độ dài, thời gian; SymPy trong process có timeout.
- So sánh từng bước trên tập nghiệm và điều kiện; xác định **dòng sai gốc**.
- Ngoài phạm vi validator → `reasoning_status = UNKNOWN`.

### 8.6. Tutor, policy và kho kiến thức

- Policy chọn L1/L2/L3 theo bằng chứng, history, episode. L3 chỉ khi trẻ hỏi thêm.
- Kho kiến thức lớp 6: chủ đề, kỹ năng, prerequisite, phương pháp, template gợi ý; có version và trạng thái duyệt. Truy xuất theo metadata trước; vector search chỉ khi cần.
- Không nạp toàn bộ kiến thức lớp 6 vào prompt. Retrieval lọc theo scope, lấy phần liên quan tới item hiện tại, phối hợp history. **Đã học khác đã thành thạo.**
- `TutorProvider` chọn template theo kỹ năng, loại lỗi, mức gợi ý và scope; điền tham số từ transcription và kết quả validator. Bài làm là dữ liệu, không phải lệnh.
- Chỉ template giáo viên duyệt (D31). Không có template phù hợp → câu mẫu "cần xem lại", ghi log `NO_TEMPLATE` (kỹ năng, loại lỗi, mức) và đưa vào hàng rà soát để shadow teacher bổ sung template.
- Output filter: đúng mức gợi ý; không chứa đáp án cuối ở L1/L2; khớp validator; **không dùng kiến thức/phương pháp ngoài scope**; không ngoài lề; độ dài nói ≤ ~2 câu. Không đạt → template đã duyệt hoặc báo cần xem lại; ghi log vi phạm phạm vi.

### 8.7. Tiến độ, hoàn thành và học tiếp

- `ItemProgress`: `NOT_STARTED`, `IN_PROGRESS`, `STUDENT_MARKED_DONE`, `NEEDS_REVISION`, `UNVERIFIED`, `VERIFIED`; cờ `NEEDS_SCOPE_REVIEW`, `UNSUPPORTED`.
- Câu nhiều ý chỉ `VERIFIED` khi các ý bắt buộc đủ evidence và đạt; đáp án đúng mà cách làm chưa xác nhận thì không `VERIFIED`.
- Bộ đề hoàn thành có xác nhận khi mọi item bắt buộc `VERIFIED`. Item chưa hỗ trợ vẫn trong mẫu số.
- Resume: tải bộ đề và tiến độ; xác nhận trang/câu hiện tại; tạo `run_id` mới; không phát phản hồi của run cũ.
- Không đưa lời giải để đạt hoàn thành.

### 8.8. Worksheet generator

Template theo dạng bài lớp 6; tham số để nghiệm phù hợp; đáp án kiểm bằng SymPy; template mới cần giáo viên duyệt; PDF A4 có dấu bốn góc, mã phiếu. Phiếu là một nguồn tờ đề (D16): khi chụp, bộ đề lấy từ phiếu đã sinh.

### 8.9. Báo cáo

- Sau mỗi run và theo tuần. Theo tờ đề: đã xác nhận đúng (3 nhóm), cần sửa, chưa xác nhận, chưa hỗ trợ, cần xem lại phạm vi, còn lại.
- Tách "trẻ báo xong" khỏi "đã xác nhận".
- "Cần luyện" chỉ khi lỗi cùng kỹ năng lặp ở ≥ 3 câu qua ≥ 2 buổi.

### 8.10. Data store

| Store | Dữ liệu | MVP |
| --- | --- | --- |
| Transaction DB | User, student, consent, LearnedScope (version), SessionProblemSet (version), PromptPage (metadata), Item, SessionRun, ItemProgress, attempt, result, hint episode, worksheet, ReviewLabel (version), ProviderRequestMap | PostgreSQL managed |
| Knowledge store | Kiến thức Toán lớp 6, prerequisite, phương pháp, template gợi ý; version, trạng thái duyệt | Bảng có cấu trúc trong PostgreSQL |
| Object storage | Ảnh trang đề và lời giải đã cắt (TTL 7 ngày), PDF phiếu | S3 hoặc tương đương với lifecycle rule |
| Job queue | Dựng bộ đề, attempt, report, worksheet | Queue bền vững |
| Cache | Idempotency, state ngắn hạn | Redis khi cần |
| Replay dataset | Ảnh có đồng ý loại 2, nhãn | Bucket riêng, quyền riêng, xóa được |

Nội dung đề đã xác nhận (text) lưu theo vòng đời tiến độ, độc lập với TTL ảnh.

### 8.11. Rà soát của shadow teacher (D25)

- Mọi attempt trong pilot vào hàng rà soát kèm: ảnh (trong TTL 7 ngày), transcription, item đã gắn và cách gắn, kết luận validator, mức gợi ý, câu cô đã nói, `model_version`, `prompt_version`, `policy_version`, `learned_scope_version`.
- Nhãn: đọc chữ đúng/sai; gắn câu đúng/sai; kết luận lỗi đúng/sai; gợi ý trong/ngoài phạm vi; gợi ý phù hợp/không; có dữ liệu định danh trong ảnh hay không. Nhãn có version, không ghi đè.
- Hàng ưu tiên phản hồi có độ tin cậy thấp và ảnh sắp hết TTL. Phản hồi chưa rà khi ảnh hết hạn vẫn giữ text để rà, ghi rõ thiếu ảnh.
- Nhãn "gợi ý ngoài phạm vi" hoặc "có dữ liệu định danh" tạo sự cố An toàn (Business HLD §11.2).
- Nhãn là nguồn cho KPI chất lượng (Business HLD §8.2). Ảnh chỉ vào bộ replay khi có đồng ý loại 2.
- Rà soát diễn ra sau buổi học; không chặn phản hồi tới trẻ.

## 9. Stack và deployment cho pilot

- **App học sinh:** Flutter cùng native modules (Kotlin cho Android, Swift cho iOS) cho camera, từ gọi, marker, person detection. Pilot trên Android 15+ và iOS 18.7+ (D23).
- **Phát hành pilot:** Google Play internal/closed testing và TestFlight. Bản TestFlight cho tester bên ngoài cần qua bước duyệt beta của Apple; tính vào tuần 5.
- **Lưu ý iOS:** không tự bật Focus/Không làm phiền; app phải ở foreground; thông báo xin quyền camera và micro rõ mục đích; test pin/nhiệt riêng.
- **Web phụ huynh/giáo viên (React + TypeScript):** báo cáo, phiếu PDF, ảnh gần trực tiếp, **phạm vi đã học** (tick theo mục lục SGK Cánh diều lớp 6), **màn hình rà soát của shadow teacher**, quản lý dữ liệu và đồng ý.
- **Backend:** Python + FastAPI, API + worker Docker trên EC2; PostgreSQL managed; S3; queue managed. Một môi trường pilot, một môi trường dev. Secrets (khóa Anthropic, Viettel AI, Azure) chỉ ở server.
- **Nhà cung cấp AI:** Anthropic (nhận dạng ảnh), Viettel AI (ASR), Azure Neural TTS (TTS). Mọi lời gọi qua adapter; điều khoản dữ liệu phải xác minh trước khi dùng dữ liệu trẻ thật.

## 10. Capacity và chi phí cho pilot

Giả định: 50 học sinh × 1 run/ngày × 20 ngày = 1.000 run/tháng; run 30–45 phút.

| Thành phần | Giả định | Ước tính/tháng |
| --- | --- | --- |
| Chụp đề | 1 trang/run (run học tiếp chỉ xác nhận lại, không đọc lại đề) | ~1.000 ảnh trang đề |
| Kiểm tra/Trợ giúp | 18 trigger/giờ (fixture) → ~9–14 trigger/run | ~9.000–14.000 trigger, ~10.000–28.000 ảnh |
| Dung lượng ảnh | ~200–400 KB/ảnh | ~3–12 GB, lưu tối đa 7 ngày |
| Đoạn âm thanh | Lệnh + câu trả lời xác nhận | ~15.000–30.000 đoạn |

Chụp đề và scope mapping có chi phí riêng, đo tách khỏi Kiểm tra/Trợ giúp. Benchmark giờ học đồng loạt phải gồm cả **đợt chụp đề đầu buổi**. Chi phí model chưa có báo giá; công thức ở Business HLD §9.2. Sizing lớn ở Phụ lục A.

## 11. NFR, an toàn dữ liệu và quan sát

| Hạng mục | Gate |
| --- | --- |
| Rảnh tay | 0 bước bắt buộc chạm máy từ lúc bắt đầu đến kết thúc, gồm chụp đề |
| Chụp đề | p95 bắt đầu chụp → bộ đề sẵn sàng ≤ 60 giây cho đề 1 trang (đề xuất) |
| Độ trễ | p95 kết thúc lệnh → âm báo ≤ 1 giây; → câu phản hồi ≤ 5 giây |
| Giọng nói | Lệnh hiểu đúng lần đầu ≥ 90%; kích hoạt nhầm < 1 lần/giờ |
| Phạm vi | 0 gợi ý ngoài phạm vi được phát trên tập test |
| Evidence | Mẫu không đủ bằng chứng không bị kết luận sai |
| Thiết bị | Buổi 45–60 phút có cắm sạc trên Android và iOS: nhiệt, RAM, crash, độ trễ |
| Isolation | Không truy cập chéo học sinh; không phát phản hồi sang run/item/revision khác |
| Privacy | 0 frame có người tới server; 0 trường định danh trong request tới nhà cung cấp; ảnh tự xóa đúng TTL; không log ảnh hoặc audio |
| Rà soát | 100% phản hồi AI trong pilot vào hàng rà soát |

- TLS; mã hóa DB và object storage; phân quyền trên từng object (phụ huynh, giáo viên được cấp quyền).
- Log `event_id`, `run_id`, versions, độ tin cậy, latency từng stage, tokens/cost, outcome, vi phạm phạm vi.
- Provider timeout: câu mẫu báo chờ; không đoán kết quả.

## 12. Bộ replay và kiểm chứng

- **Tuần 1:** 100–200 bài làm thật của trẻ lớp 6 trong vở, có số câu ở lề trái (chụp từ giá đỡ, đã ẩn danh hóa); **20–30 tờ đề in lớp 6 HK1 Cánh diều một trang** (có ý con, có câu hình học); 20–30 trẻ nói bộ lệnh.
- **Tuần 2–5:** mở rộng lên 200–300 bài; shadow teacher gán nhãn transcription, số câu, dòng sai gốc, gợi ý phù hợp, kỹ năng và phạm vi của từng câu đề.
- **Tuần 6–10:** nhãn rà soát pilot (§8.11) bổ sung vào bộ replay khi có đồng ý loại 2.
- **Harness:** chạy ảnh đề, ảnh bài làm và âm thanh qua hệ thống; chấm theo acceptance; báo cáo theo `model_version`/`policy_version`/`learned_scope_version`.

Metrics: đủ câu/ý của đề; đúng nội dung đề; đọc đúng số câu trong vở; exact-match transcription theo dòng; lỗi dấu âm/phân số; false acceptance; tỷ lệ hỏi lại; tuân thủ phạm vi; sai chấm do nhận dạng tách khỏi sai chấm do validator/tutor; lệnh hiểu đúng; kích hoạt nhầm/giờ.

## 13. Lộ trình kỹ thuật 10 tuần

| Tuần | Bàn giao | Gate |
| --- | --- | --- |
| 1 (08–14/10) | Spike Claude Opus 5.5/Sonnet 5.5/Haiku 5.5 trên bài làm và đề in; ẩn danh hóa; spike "Cô ơi", ASR Viettel AI, TTS Azure trên Android và iPhone; mục lục kỹ năng HK1 Cánh diều; adapter skeleton; repo, CI | **S** 14/10 |
| 2 | Client Flutter + native: khung hình, tự bắt đầu, chặn người, cắt trang, từ gọi. Backend: session, run, prompt-pages, storage TTL, consent, ẩn danh hóa | "Đặt đề → chụp → dựng bộ đề" chạy trên cả hai nền tảng |
| 3 | Xác nhận bộ đề bằng giọng nói; learned scope + scope gate; knowledge store tối thiểu; đọc số câu trong vở; attempt; ValidatorRegistry + bộ số học/đại số; evidence gate | Vertical slice một chủ đề HK1 |
| 4 | Policy, template gợi ý, output filter (gồm phạm vi), TTS, xác nhận chữ; ItemProgress, end/resume; báo cáo; web phụ huynh (phạm vi, báo cáo, ảnh gần trực tiếp, dữ liệu); màn hình rà soát shadow teacher; worksheet cơ bản; thẻ lệnh | Đủ tính năng MVP |
| 5 | Harness replay; test máy thật 45–60 phút cả hai nền tảng; phát hành TestFlight và Google Play testing | **G0** 11/11 |
| 6 | Alpha 5 gia đình (cả Android và iOS); đo khối lượng rà soát; sửa lỗi | **G1** 18/11 |
| 7–10 | Pilot 15 → 50; theo dõi chi phí, độ trễ, kích hoạt nhầm, chụp đề theo nền tảng; sửa nóng; mở thêm chủ đề HK1 khi đạt | **G2** ≈ 22/11; go/no-go 16/12 |

## 14. Checklist cho coding agent

- Đọc cả hai HLD v1.3 và context v0.5; kiểm tra repo/tests trước; không nhận tính năng đã hoàn thành.
- Interface: `RecognitionEngine`, `Deidentifier`, `ItemResolver`, `ProblemSetBuilder`, `ScopeGate`, `KnowledgeRetriever`, `SpeechRecognizer`, `IntentClassifier`, `TutorProvider`, `TtsProvider`, `MathValidator` + `ValidatorRegistry`, `WorksheetGenerator`, `ReviewQueue`; policy có version.
- Dùng fake adapter cho vertical slice; không trình bày output fake như kết quả thật.
- Server từ chối ảnh khi `person_check != PASSED`, payload quá giới hạn, session/run không hợp lệ, chưa có đồng ý loại 1.
- Không mở `READY` khi bộ đề hoặc scope chưa xác nhận. Không mặc định scope = toàn lớp 6.
- Mọi luồng trong buổi học, kể cả chụp đề, có đường không chạm; có test tự động cho điều này.
- Test: đặt trang đề thứ hai, ý con, đề chụp thiếu câu, câu hình học, số câu trong vở không rõ hoặc không có trong đề, lệnh "Câu N" khác số trong vở, request tới nhà cung cấp có dữ liệu định danh, câu ngoài phạm vi, chọn câu không theo thứ tự, hết giờ, học tiếp, đổi version đề, dấu âm mất, phân số sai, thiếu dòng, che tay, có người trong khung, kích hoạt nhầm, barge-in, mất mạng, provider timeout.
- Không triển khai: camera chạy ngầm, ASR luôn bật gửi server, chặn cứng sau ba lần trợ giúp, chấm điểm tập trung, lời giải đầy đủ tự động, gợi ý ngoài phạm vi.
- Báo code đã đổi, test đã chạy, benchmark đã đo, giới hạn và bước tiếp theo.

## 15. State machine và acceptance

| State | Điều kiện / chuyển tiếp |
| --- | --- |
| WAITING_FOR_DESK | App mở; máy đứng yên, không có người → SETUP (có đề dở → hỏi học tiếp → RESUMING) |
| SETUP / CAPTURING_PROMPT | Chụp trang đề (MVP: 1 trang) → CONFIRMING_PROBLEM_SET |
| CONFIRMING_PROBLEM_SET | Cô đọc số câu/ý; xác nhận bằng giọng nói; sửa → version mới; scope gate → READY |
| RESUMING | Tải bộ đề và tiến độ; xác nhận trang/câu → READY (run mới) |
| READY | Trẻ bắt đầu làm (ghi số câu trong vở hoặc nói "Câu N") → WORKING |
| WORKING | Quan sát nhẹ; lệnh/thẻ → CAPTURING; idle → IDLE_OFFER; "câu N" → đổi item; số câu trong vở được đọc khi có trigger |
| IDLE_OFFER | Hỏi một lần; "nghĩ tiếp" → WORKING (cooldown); "giúp con" → CAPTURING |
| CAPTURING | Chờ ổn định, không tay che, kiểm tra người → UPLOADING |
| UPLOADING / CHECKING / HELPING | Server ẩn danh hóa, nhận dạng, xác định item; run, version, item, revision, deadline được kiểm tra |
| NEEDS_CLARIFICATION | Câu hỏi đóng bằng giọng nói (chữ không rõ, hoặc "Con đang làm câu mấy?") |
| SPEAKING | Phát TTS; barge-in → WORKING |
| NEEDS_REVISION | Phản hồi lỗi; trẻ sửa → WORKING |
| VERIFIED | Item đúng đầy đủ; trẻ chuyển câu khác → WORKING |
| PAUSED | Dừng camera, micro, timer, TTS |
| SAVED_FOR_CONTINUATION | Hết giờ/End: lưu tiến độ; output pending lỗi thời; resume tạo run mới |

### 15.1. Acceptance matrix

| ID | Tình huống | Assertion | Mã cũ |
| --- | --- | --- | --- |
| A01 | Đặt máy; tạm dừng/kết thúc bằng giọng nói | Không cần chạm; indicator đúng; End dừng capture/mic/TTS và giữ tiến độ | 06/10 A01; 07/10 A01 |
| A02 | Đề 1 trang, 10 câu, có ý con | Manifest và thứ tự đúng; đủ item; chưa READY khi chưa xác nhận; trang thứ hai bị từ chối có thông báo | 07/10 A21; sửa v1.3 |
| A03 | Đề thiếu dấu âm hoặc ý nhỏ khi nhận dạng | Hỏi xác nhận; không bỏ item; không tự sửa đề | 07/10 A22 |
| A04 | Đề không QR, chưa có trên hệ thống | Vẫn dựng bộ đề; không bắt nhập trước | 07/10 A23 |
| A05 | Trẻ làm đúng hoặc tự sửa trước khi gọi | 0 gọi server phân tích; không bịa sự kiện tự sửa | 06/10 A02 |
| A06 | Kiểm tra: 3x + 5 = 20 → 3x = 25 → x = 25/3 | Chỉ dòng 2 là lỗi gốc; không đọc đáp án; ngôn ngữ SGK lớp 6 | 06/10 A03 |
| A07 | Idle 60 giây | Một câu hỏi mẫu tại máy; 0 gọi cloud; cooldown | 06/10 A04 |
| A08 | Trợ giúp có/không có history | Đúng student/skill; thiếu history vẫn giúp | 06/10 A05 |
| A09 | Gọi ba lần khi đang chờ | Một logical request | 06/10 A06 |
| A10 | Trợ giúp mới trên bài không đổi | Intent mới được xử lý; dùng lại transcription | 06/10 A07 |
| A11 | Chữ 15/18 không rõ | Câu hỏi xác nhận bằng giọng nói; không phán sai trước khi rõ | 06/10 A08 |
| A12 | Trẻ viết "2 + 3 = 6" | Transcription giữ 6 | 06/10 A09 |
| A13 | Mất dấu âm/phân số hoặc thiếu dòng | Evidence gate ghi uncertainty; không xác nhận đầy đủ | 06/10 A10 |
| A14 | Đáp án đúng, thiếu dòng giữa | answer và reasoning khác trạng thái; item không VERIFIED | 06/10 A11 |
| A15 | Đổi trang/câu/revision/End khi đang chờ | Bỏ output cũ | 06/10 A12 |
| A16 | Mất mạng/reconnect | Retry giới hạn; không phát hàng loạt; báo bằng giọng nói | 06/10 A13 |
| A17 | Ba lần trợ giúp cùng kỹ năng | Xem lại tiến triển; không chặn | 06/10 A14 |
| A18 | Làm câu 4 trước câu 1 (ghi `4)` trong vở, hoặc nói "Câu 4") | Phản hồi đúng item; không đoán theo thứ tự | 07/10 A26; sửa v1.3 |
| A19 | Câu cần kiến thức chưa học | NEEDS_SCOPE_REVIEW; gợi ý không vượt phạm vi; không chấm sai | 07/10 A24 |
| A20 | Retrieval/LLM dùng phương pháp chưa học | Output gate chặn; dùng template; log vi phạm; không phát gợi ý đó | 07/10 A30 |
| A21 | Trẻ yếu ở chủ đề đã học | History điều chỉnh gợi ý; không chặn vì "đã được dạy" | 07/10 A25 |
| A22 | Câu hình học hoặc có hình vẽ chưa hỗ trợ | UNSUPPORTED; vẫn trong tổng; báo cáo không ghi "xong hết" | 07/10 A29; sửa v1.3 |
| A23 | Hết 45 phút còn 2 câu | Lưu tiến độ; nói phần còn lại; không đưa lời giải để hoàn thành | 07/10 A27 |
| A24 | Học tiếp / đổi version đề | Run ID mới; output cũ bị loại; item phụ thuộc cần kiểm tra lại | 07/10 A28 |
| A25 | Phụ huynh xem từ xa | Đúng quyền; máy con hiện chỉ báo; End ngắt xem | 06/10 A15 |
| A26 | Báo cáo | Khớp event; không đếm trùng; tách trẻ báo xong / đã xác nhận / cần sửa / chưa xác nhận | 06/10 A16 |
| A27 | Payload bất thường hoặc chữ trong bài giống lệnh | Từ chối ảnh khi thiếu person_check; parser allowlist/timeout; bài làm không điều khiển prompt | 06/10 A17 |
| A28 | Provider timeout/quota | Không giả vờ đã chấm; câu mẫu báo chờ; chuyển model dự phòng | 06/10 A18 |
| A29 | Model mới | Phải qua replay và G0 trước khi bật | 06/10 A19 |
| A30 | Câu hỏi ngoài lề | Từ chối nhẹ nhàng, đưa về bài | 06/10 A20 |
| A31 | Cả buổi 45 phút gồm chụp đề | 0 bước bắt buộc chạm máy từ WAITING_FOR_DESK đến SAVED_FOR_CONTINUATION | 06/10 A21 |
| A32 | "Cô ơi" trong phòng có TV/anh chị em | Kích hoạt nhầm < 1 lần/giờ trên tập test | 06/10 A22 |
| A33 | Lệnh của trẻ lớp 6 | Hiểu đúng lần đầu ≥ 90% trên tập test | 06/10 A23 |
| A34 | Barge-in "Cô ơi, dừng" | TTS dừng ≤ 500 ms | 06/10 A24 |
| A35 | Giấy lệch trong/ngoài ngưỡng | Trong: tự bù. Ngoài: nhắc xê dịch giấy, không nhắc chỉnh máy | 06/10 A25 |
| A36 | Có người trong khung | Frame không rời máy; server không nhận; ghi event chặn | 06/10 A26 |
| A37 | Phiếu bài hệ thống | 0 đề/đáp án sai trên tập sinh thử; chụp lại nhận đúng mã phiếu và số câu | 06/10 A27 |
| A38 | Thẻ lệnh | Giữ 1 giây → đúng intent; lướt qua không kích hoạt | 06/10 A28 |
| A39 | Ảnh tự xóa | Ảnh quá 7 ngày (hoặc cài đặt) không còn; text đề và tiến độ vẫn còn | 06/10 A29 |
| A40 | Chưa có đồng ý loại 1 | Không tạo session, không bật camera/micro; tắt loại 2 thì ảnh không vào replay | 06/10 A30 |
| A41 | Xuất và xóa dữ liệu | Bản xuất đủ; sau xóa không còn ảnh, đề, tiến độ, attempt, báo cáo | 06/10 A31 |
| A42 | Phạm vi đã học | Thiếu profile → không mặc định toàn lớp 6; đổi scope tạo version; buổi đang chạy dùng snapshot | Mới v1.2 |
| A43 | Ảnh gửi nhà cung cấp | Payload tới Anthropic không có EXIF, mã người dùng/học sinh/phiên/thiết bị; dải đầu trang bị che; log chỉ có hash | Mới v1.3 |
| A44 | Số câu trong vở | `3)` rõ → gắn câu 3; số không rõ hoặc không có trong đề → hỏi "Con đang làm câu mấy?", không đoán; lệnh "Câu N" thắng số trong vở | Mới v1.3 |
| A45 | Mở rộng bộ chấm | Item domain chưa đăng ký → UNSUPPORTED; đăng ký bộ chấm thử nghiệm mới không đổi API, state machine hay kết quả của item số học/đại số | Mới v1.3 |
| A46 | Rà soát shadow teacher | Mọi attempt vào hàng rà soát với đủ trường §8.11; nhãn có version; nhãn "ngoài phạm vi" hoặc "có định danh" tạo sự cố | Mới v1.3 |

A02, A03, A06, A11, A13, A19, A20, A32, A33, A44 cần ground truth thật (ảnh đề, ảnh bài làm, âm thanh, nhãn giáo viên).

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

Với 18 trigger/giờ, 1–2 ảnh ~200–400 KB mỗi trigger, chưa tính đợt chụp đề đầu buổi:

| Active cùng lúc | Trigger/giây | Ảnh vào (ước tính) |
| ---: | ---: | ---: |
| 1.000 | 5 | ~1–4 MB/s |
| 10.000 | 50 | ~10–40 MB/s |
| 100.000 | 500 | ~100–400 MB/s |

Đợt chụp đề đầu buổi cộng thêm `λ_setup × số trang × kích thước ảnh`, và cần test burst riêng cho giờ học đồng loạt. Từ 10.000 active trở lên, đánh giá lại nhận dạng trên máy để chỉ gửi JSON như bộ 07/10 đề xuất; quyết định dựa trên số đo pilot và benchmark máy thật.
