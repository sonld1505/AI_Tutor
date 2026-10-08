# CLAUDE_AI_Tutor.md

> Cập nhật: 08/10/2026 (bản trước: 03/10/2026)  
> Chủ dự án: Sơn (Lê Đình Sơn)  
> **Baseline sản phẩm:** bộ v1.3 trong `docs/product/`: [Business HLD v1.3](docs/product/business-hld-v1.3.md), [Technical HLD v1.3](docs/product/technical-hld-v1.3.md), [context v0.5](docs/product/ai-study-companion-context-v0.5.md). Quyết định của chủ dự án ngày 08/10/2026: **baseline sản phẩm thắng về sản phẩm** (v1.2, hợp nhất thành v1.3 cùng ngày); file này giữ luật privacy, secret, provider, mock và nguyên tắc coding agent.

## 1. Mục đích tài liệu

Tài liệu này hướng dẫn Claude/Codex và đội phát triển khi phân tích, thiết kế hoặc triển khai **AI Study Companion**: một app trên smartphone đặt trên giá đỡ, giúp học sinh **lớp 6** tự làm đề Toán học kỳ 1 (SGK Cánh diều) in trên giấy, gọi "Cô ơi" khi cần kiểm tra hoặc gợi ý, mà không phải chạm máy trong buổi học.

Thứ tự ưu tiên khi mâu thuẫn:

1. Luật ở file này về **privacy, secret, provider cho trẻ em, mock, không bịa số liệu** (§5, §10, §11) và Constitution trong `CLAUDE.md`/`AGENTS.md`. Đây là ràng buộc tối thiểu; HLD v1.3 chỉ được chặt hơn.
2. Business HLD và Technical HLD v1.3 cho mọi nội dung sản phẩm: phạm vi, use case, kiến trúc, API, KPI, cổng pilot.
3. Context v0.5, kế hoạch pilot, slide.

Mâu thuẫn giữa các nguồn trên, hoặc giữa v1.3 và luật ở mục 1 → **hard-stop, hỏi Sơn**.

Toàn bộ nội dung là **thiết kế đề xuất và giả thuyết kinh doanh**. Chưa được coi là bằng chứng rằng sản phẩm, hạ tầng, nhận dạng, benchmark, doanh thu hoặc product-market fit đã tồn tại.

## 2. Tầm nhìn sản phẩm

Nguồn chuẩn: Business HLD v1.3 §1, §3, §4.

> Con tự làm đề, gọi cô khi cần, cô chỉ dạy những gì con đã học, và con không phải chạm vào máy.

Bốn trụ khác biệt: rảnh tay; chấm cách làm, không chỉ đáp án; gợi ý đúng phần đã học; vòng lặp báo cáo → phiếu luyện.

Ví dụ hành vi mong muốn (Business HLD §5.4, acceptance A06): câu `3x + 5 = 20`, trẻ viết `3x = 25` rồi `x = 25/3` và gọi kiểm tra. Cô chỉ dòng 2 là lỗi gốc: "Con xem lại dòng thứ hai nhé. Muốn tìm số hạng chưa biết thì con làm phép tính gì?" Không đọc đáp án, không coi dòng 3 là lỗi gốc mới.

## 3. Trạng thái thực tế

### Đã có

- Bộ tài liệu sản phẩm v1.3 (Business HLD, Technical HLD, context v0.5, kế hoạch pilot offline).
- Nền Factory Phase 1 (vai trò agent, template SAFe, script quality gate fail-closed). Xem `docs/factory/PHASE1-STATUS.md`.

### Chưa có hoặc chưa xác nhận

- Code sản phẩm (app Android/iOS, backend, web phụ huynh) và môi trường pilot.
- Spike vision, spike từ gọi "Cô ơi", benchmark và accuracy thực tế.
- Nhà cung cấp đã **chọn** (Anthropic cho ảnh, Viettel AI cho ASR, Azure cho TTS) nhưng **chưa xác minh điều khoản** cho dữ liệu trẻ em; chưa có hợp đồng hay khóa API.
- Mục lục kỹ năng và support matrix HK1 Cánh diều; shadow teacher chưa ký hợp tác.
- Tư vấn pháp lý, nội dung hai loại đồng ý.
- Khảo sát thị trường, willingness-to-pay, đặt cọc, retention, doanh thu.

Agent không được mô tả phần "chưa có" như thành quả đã triển khai.

## 4. Phạm vi MVP

Nguồn chuẩn: Business HLD v1.3 §6, Technical HLD v1.3 §2. Tóm tắt:

- **Toán lớp 6 học kỳ 1, SGK Cánh diều** (D10): chấm số học và đại số; câu hình học nằm trong đề nhưng "chưa hỗ trợ"; chấm hình học sau pilot, kiến trúc sẵn chỗ (D30).
- **Buổi học theo tờ đề in tối đa 1 trang**: chụp đề đầu buổi, xác nhận câu/ý bằng giọng nói (D11, D12). Tờ đề do giáo viên/phụ huynh chuẩn bị hoặc phiếu hệ thống sinh theo lỗ hổng (D16).
- Trẻ làm trong vở, **ghi số câu ở lề trái** trước khi làm (ví dụ `1) 5x + 3 = 28`); hệ thống đọc số câu; lệnh "Câu N" là dự phòng (D15).
- Gợi ý chỉ trong **phạm vi đã học có version** (D13), do **shadow teacher** xác nhận; shadow teacher rà và gán nhãn mọi phản hồi AI trong pilot (D25). Buổi 30–45 phút, lưu tiến độ và học tiếp (D14).
- App học sinh **Android 15+ và iOS 18.7+** (D23); web phụ huynh/giáo viên; dùng bất kỳ giờ nào (D29).
- Pilot tối đa 50 gia đình, kickoff 08/10/2026, go/no-go 16/12/2026 (D22); miễn phí trong pilot (D18).

Ngoài MVP: lớp 7 trở lên, học kỳ 2, môn khác, chấm hình học, đề nhiều trang, câu có hình/bảng mà hệ thống chưa biểu diễn được (giữ "chưa hỗ trợ"), live video, nhận dạng trên máy, laptop/webcam, giao diện giáo viên cho cả lớp, gamification, chấm điểm tập trung/cảm xúc, camera chạy ngầm, giải toàn bài tự động.

## 5. Quy tắc camera, micro và quyền riêng tư

Nguồn chi tiết: Business HLD v1.3 §7, Technical HLD v1.3 §5, §7.1, §11. Đây là luật bắt buộc:

- Camera và micro chỉ chạy khi app ở foreground trong buổi học; không chạy ngầm. Pause/End dừng camera, micro, nhận diện, TTS.
- Camera đặt trên giá, hướng xuống mặt bàn, đề và vở; không chủ đích quay mặt hoặc căn phòng.
- **Frame có người/khuôn mặt bị chặn trên máy và không rời máy.** Server từ chối mọi ảnh khi `person_check != PASSED`, payload quá giới hạn, session/run không hợp lệ hoặc chưa có đồng ý loại 1.
- Chỉ gửi **ảnh vùng giấy đã cắt**, và chỉ khi có trigger: chụp trang đề, lệnh Kiểm tra/Trợ giúp, chụp phiếu bài, phụ huynh đang xem (D04). Trong lúc trẻ làm bài không gửi gì lên server.
- **Ẩn danh hóa trước khi gửi nhà cung cấp AI (D26):** ảnh gửi Anthropic đã bỏ metadata, che dải đầu trang (tên, lớp, trường); request không mang mã người dùng, học sinh, phiên hay thiết bị (A43).
- Từ gọi "Cô ơi" nhận diện trên máy; âm thanh chỉ gửi (tới ASR) sau từ gọi hoặc trong khoảng trả lời câu hỏi xác nhận. Không có ASR luôn bật. Không lưu audio mặc định.
- Phụ huynh xem **ảnh gần trực tiếp** theo quyền của đúng gia đình; máy con hiện chỉ báo khi đang được xem; End ngắt xem. Không có live video trong MVP (D17).
- Không ghi video. **Ảnh tự xóa sau 7 ngày** hoặc theo cài đặt phụ huynh; text đề đã xác nhận, tiến độ và kết quả lưu trong DB (D20).
- Hai loại đồng ý tách biệt: (1) dùng dịch vụ, bắt buộc; (2) dùng ảnh để cải thiện hệ thống, tùy chọn, rút lại được. Chưa có loại 1 thì không tạo session, không bật camera/micro (A40).
- Phụ huynh xem, xuất, xóa dữ liệu của con (U24, A41). Không bán/chia sẻ dữ liệu cá nhân; không quảng cáo tới trẻ (D19).
- Không log ảnh hoặc audio. API key chỉ ở server; client dùng token ngắn hạn.
- Không đưa secret vào Git, tài liệu, log hoặc mã client.

Đây là yêu cầu thiết kế, không phải ý kiến pháp lý. Cần tư vấn pháp lý trước pilot với trẻ thật.

## 6. Kiến trúc

Nguồn chuẩn: Technical HLD v1.3 §1 (12 quyết định kiến trúc), §3 (sơ đồ logic), §7 (API), §8 (backend), §9 (stack). Tóm tắt các ràng buộc:

- **Rảnh tay là ràng buộc cứng**: mọi bước trong buổi học, kể cả chụp đề, có đường không chạm (giọng nói, giấy, thẻ lệnh).
- Không mở `READY` khi bộ đề hoặc phạm vi đã học chưa được xác nhận. Không mặc định scope = toàn lớp 6.
- Client lọc trước khi gửi (chất lượng, che tay, chặn người, cắt trang); server ẩn danh hóa rồi gọi Claude qua `RecognitionEngine` adapter.
- **Chấm Toán tất định**: `ValidatorRegistry` theo domain; MVP có bộ số học/đại số (parser allowlist + SymPy); hình học thêm sau pilot mà không đổi pipeline.
- Lời gợi ý chỉ từ template đã duyệt; không có template phù hợp → "cần xem lại" (D31). MVP không dùng LLM sinh lời; intent theo bộ luật. Output filter chặn lộ đáp án, ngoài lề, ngoài phạm vi.
- Backend modular monolith cùng worker; không microservice trong MVP. Stack (D28): backend **Python + FastAPI** (API + worker Docker), web phụ huynh/giáo viên **React + TypeScript**, app học sinh **Flutter + native** (Kotlin/Swift); PostgreSQL, S3, queue theo Technical HLD §9. Chưa có quyết định mua dịch vụ hạ tầng.

## 7. Quy tắc nhận dạng và tutor

Nguồn chuẩn: Technical HLD v1.3 §6.2, §8.2–§8.6; Business HLD v1.3 §4, §5.5.

- AI im lặng khi chưa được gọi. Ngừng viết khoảng 60 giây chỉ hỏi một lần bằng câu mẫu tại máy, không gọi AI cloud (D07).
- **UNKNOWN ≠ WRONG.** Không đọc rõ thì hỏi lại bằng câu hỏi đóng; không chấm sai vì camera hoặc nhận dạng.
- Nhận dạng giữ nguyên những gì trẻ viết (`2 + 3 = 6` giữ 6); prompt nhận dạng chỉ chép lại, không giải bài.
- Tách trạng thái đáp án và cách làm; đáp án đúng không chứng minh cách làm đúng.
- Gợi ý nhỏ nhất: L1 nhắc nhẹ, L2 khái niệm, L3 một bước trung gian chỉ khi trẻ chủ động hỏi thêm. Không tự đưa lời giải đầy đủ; không tăng mức vì hết giờ.
- Gợi ý chỉ dùng kiến thức/phương pháp **trong phạm vi đã học**. Đã học ≠ đã thành thạo.
- History để cá nhân hóa, không để khóa trợ giúp; không gắn nhãn lười.
- Ngôn ngữ SGK lớp 6 (Cánh diều); chỉ nói về bài học.
- Số câu trong vở không rõ hoặc không khớp đề: hỏi "Con đang làm câu mấy?", không đoán.
- Không suy diễn tâm lý hoặc sự tập trung; báo cáo chỉ nói điều có bằng chứng.
- Câu khó, ngoài phạm vi, chưa hỗ trợ **vẫn nằm trong tổng số câu** của đề.
- Mất mạng hoặc provider timeout: báo bằng câu mẫu; không đoán kết quả.

## 8. Dữ liệu và tính nhất quán

Nguồn chuẩn: Technical HLD v1.3 §7.2–§7.4, §8.7, §8.10.

- Mỗi attempt mang `event_id`, `session_id`, `run_id`, `problem_set_id`, `problem_set_version`, `learned_scope_version`, `item_id`, `submission_revision`. Client và server kiểm tra các giá trị này trước khi phát phản hồi; output của run/item/revision cũ bị bỏ.
- Idempotency theo user/session/event_id kèm fingerprint; retry không tạo gợi ý mới.
- Entity chính: User, Student, Consent, LearnedScope (version), SessionProblemSet (version), PromptPage, Item, SessionRun, ItemProgress, Attempt, Result, HintEpisode, Worksheet, ReviewLabel (version), ProviderRequestMap; knowledge store lớp 6 có version và trạng thái duyệt.
- Mỗi attempt ghi `engine`, `model_version`, `prompt_version`, `policy_version`, `learned_scope_version`.

Metadata JSON trong Technical HLD §7.2 là đề xuất, chưa phải schema đã chốt. Thay đổi schema là việc A+.

## 9. KPI và cổng pilot

Nguồn chuẩn: Business HLD v1.3 §8 (KPI), §11 (cổng S, G0, G1, G2 và go/no-go). Kế hoạch pilot (`docs/product/pilot-plan.html`) chỉ phản chiếu §11; đổi ngưỡng phải sửa cả hai.

Mọi con số trong đó là **mục tiêu**, không phải kết quả đã đạt. Không trích dẫn chúng như số đo.

## 10. Ràng buộc nhà cung cấp

- **Nhà cung cấp đã chọn (Sơn, 08/10/2026):** Anthropic (Claude) **chỉ cho nhận dạng ảnh**, ảnh đã ẩn danh hóa (D05, D26); **Viettel AI** cho ASR; **Azure Neural TTS** (giọng nữ tiếng Việt) cho TTS (D27). Không dùng LLM sinh lời trong MVP (D31).
- Chưa bật cho dữ liệu trẻ thật cho tới khi xác minh theo các mục dưới đây và Sơn duyệt. Với Anthropic, sản phẩm có người dùng dưới 18 tuổi phải theo hướng dẫn cho tổ chức phục vụ trẻ vị thành niên (https://support.claude.com/en/articles/9307344), dù chỉ gửi ảnh: thông báo người dùng đang nói chuyện với AI, lọc nội dung, giám sát. Giọng trẻ gửi Viettel AI là dữ liệu trẻ em.
- Chỉ dùng nhà cung cấp có cam kết không huấn luyện trên dữ liệu, lưu tối thiểu, có hồ sơ chuyển dữ liệu ra nước ngoài (Business HLD §7; Technical HLD §6.1).
- Theo context ngày 03/10/2026, Gemini Developer API có hạn chế với API client hướng tới hoặc có khả năng được người dưới 18 tuổi truy cập.
- Không tự suy luận rằng parental consent hoặc chuyển sang một dịch vụ khác tự động giải quyết điều khoản.
- Trước khi gửi **dữ liệu của trẻ thật** (ảnh bài làm, giọng nói) tới provider, kể cả trong spike tuần 1, phải xác minh: độ tuổi, retention, data training, quyền dữ liệu, vị trí xử lý, quota, hợp đồng và cơ chế xóa dữ liệu. Đây là việc A+: trình plan, chờ Sơn duyệt.
- Model mới chỉ được bật khi qua bộ replay và cổng G0 (A29).
- Model self-host: phải xác minh license và năng lực vận hành. Giá và điều khoản phải kiểm tra lại tại thời điểm ra quyết định.

## 11. Nguyên tắc làm việc cho coding agent

Bổ sung cho checklist ở Technical HLD v1.3 §14 và context v0.5 §12.

Trước khi thay đổi code:

1. Đọc file này, `CLAUDE.md`/`AGENTS.md`, `README.md`, cả hai HLD v1.3 và context v0.5.
2. Kiểm kê trạng thái thực tế: code, branch, dependency, test, infrastructure và biến môi trường.
3. Phân biệt rõ: yêu cầu đã được duyệt; đề xuất thiết kế; giả định tài chính/kỹ thuật; dữ liệu hoặc kết quả đã đo.
4. Không tự nhận có EC2, domain, credential, camera integration hoặc provider nếu chưa kiểm chứng.

Khi triển khai:

- Ưu tiên vertical slice nhỏ chạy end-to-end.
- Mọi model qua adapter: `RecognitionEngine`, `Deidentifier`, `ItemResolver`, `ProblemSetBuilder`, `ScopeGate`, `KnowledgeRetriever`, `SpeechRecognizer`, `IntentClassifier`, `TutorProvider`, `TtsProvider`, `MathValidator` + `ValidatorRegistry`, `WorksheetGenerator`, `ReviewQueue`.
- Fake/mock adapter phải gắn nhãn rõ trong code, log và tài liệu. Không dùng output fake để tuyên bố đã giải quyết khả năng đọc bài thực tế.
- Đo token, latency từng stage, retry và chi phí ngay từ đầu.
- Thiết kế idempotency, timeout, retry có giới hạn, xử lý kết quả lỗi thời.
- Mọi luồng trong buổi học có đường không chạm và có test tự động cho điều đó.
- Không triển khai: camera chạy ngầm, ASR luôn bật gửi server, chặn cứng sau ba lần trợ giúp, chấm điểm tập trung, lời giải đầy đủ tự động, gợi ý ngoài phạm vi.
- Không triển khai provider cho trẻ em khi điều khoản chưa được xác nhận.
- Không mở rộng ngoài phạm vi được giao nếu cần thêm quyền hoặc tạo chi phí đáng kể.

Sau khi thay đổi:

1. Chạy test phù hợp với mức rủi ro.
2. Ghi cách chạy, kết quả test và phần chưa kiểm chứng.
3. Cập nhật tài liệu/changelog ngắn.
4. Thay giả định bằng actual khi có bằng chứng; không xóa lịch sử quyết định quan trọng.

## 12. Thứ tự triển khai

Nguồn chuẩn: context v0.5 §12, Technical HLD v1.3 §13.

```text
Spike vision (đề in + bài làm + số câu) và "Cô ơi"/ASR/TTS
→ Harness replay
→ Chụp đề + xác nhận bằng giọng nói + scope gate
→ Attempt: ẩn danh hóa, ItemResolver, ValidatorRegistry, evidence gate, policy, retrieval theo scope, output filter, TTS
→ Tiến độ, end/resume
→ Báo cáo, web phụ huynh, phiếu bài, rà soát shadow teacher
```

Acceptance ưu tiên cho vertical slice: A01, A02, A05, A06, A11, A14, A18, A19, A20, A22, A23, A24, A31, A36, A40, A42, A43, A44, A46 (Technical HLD §15.1).

## 13. Gate trước khi mở rộng

Không tăng quy mô chỉ dựa trên demo. Theo thứ tự cổng ở Business HLD v1.3 §11: **S** 14/10 → **G0** (replay và máy thật) 11/11 → **G1** (alpha 5 gia đình) 18/11 → **G2** (mở 50 gia đình) ≈ 22/11 → **go/no-go** 16/12/2026. Bất kỳ vi phạm An toàn nào (frame có người tới server, dữ liệu định danh tới nhà cung cấp, sự cố dữ liệu, gợi ý ngoài phạm vi bị phát) → dừng ngay.

Các con số kinh doanh trong HLD là giả thuyết, không được dùng như dữ liệu doanh thu thực tế.

## 14. Prompt khởi động đề xuất

> Đọc `CLAUDE_AI_Tutor.md`, cả hai HLD v1.3 và context v0.5 trong `docs/product/`, cùng tài liệu repository. Tóm tắt trạng thái thực tế và kiểm kê môi trường hiện có trước khi thay đổi. Sau đó đề xuất hoặc triển khai vertical slice nhỏ nhất trong phạm vi được giao. Phân biệt rõ fake adapter với integration thật, ghi cách chạy và kết quả kiểm thử. Không dùng nhà cung cấp cho trẻ em khi điều khoản chưa được xác nhận và không ghi secret vào code hoặc tài liệu.

## 15. Nguồn cần kiểm tra lại

- Anthropic, hướng dẫn cho tổ chức phục vụ người dưới 18 tuổi: https://support.claude.com/en/articles/9307344
- Anthropic, child safety guidance for developers: https://support.claude.com/en/articles/15591275
- Điều khoản và giá Viettel AI, Azure AI Speech: kiểm tra tại thời điểm ký hợp đồng.
- Gemini API Terms (bối cảnh cũ): https://ai.google.dev/gemini-api/terms
- Mathpix OCR API (đối chứng benchmark): https://mathpix.com/ocr
- Nguồn R&D nhận dạng trên máy: Technical HLD v1.3 §16.

Không coi nội dung giá hoặc điều khoản đã đọc trước đây là hiện hành nếu chưa kiểm tra lại tại thời điểm triển khai.

## 16. Thay đổi so với bản 03/10/2026

| Bản 03/10 | Bản 08/10 (theo v1.3) |
|---|---|
| Smartphone **hoặc** laptop/USB webcam | Chỉ app Android và iOS trên giá đỡ |
| Phiên học tự do, theo dõi liên tục bước viết, OCR mỗi khi ảnh ổn định | Buổi học theo tờ đề; chỉ gửi ảnh khi có trigger |
| Chờ 20–30 giây rồi tự gợi ý | AI im lặng tới khi trẻ gọi; ngừng viết ~60 giây chỉ hỏi một lần |
| Parent live qua WebRTC P2P/TURN, < 1,5 giây | Ảnh gần trực tiếp; live video sau MVP |
| Realtime voice streaming, voice p95 < 2 giây | Từ gọi trên máy + ASR theo đoạn; âm báo p95 ≤ 1 giây, phản hồi p95 ≤ 5 giây |
| 20–30 dạng bài | Số học và đại số Toán 6 HK1 Cánh diều; hình học sau pilot; gợi ý trong phạm vi đã học |
| Pilot 20–50 học sinh, tối đa 100 hộ | Tối đa 50 gia đình, 10 tuần, cổng S/G0/G1/G2 |
| Learning event và entity tối thiểu (§8 cũ) | Entity theo Technical HLD §8.10 |
| Cửa sổ giờ được phép (ví dụ 20h–24h) | **Bỏ** (D29, RAID I-010). Camera vẫn chỉ chạy trong buổi học (§5) |
| Provider chưa chọn | Anthropic (ảnh, đã ẩn danh hóa), Viettel AI (ASR), Azure (TTS) |

Bản 03/10 vẫn còn trong lịch sử Git. Các draft dựng từ bản này (`docs/capstone/SCOPE-AITUTOR.md`, `docs/capstone/HLD-AITUTOR.md`) đã được đánh dấu SUPERSEDED.
