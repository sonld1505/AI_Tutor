# SCOPE-AITUTOR — Bước [0] Làm rõ scope

> **Trạng thái:** `DRAFT — AI soạn, CHƯA qua 🔒 Cổng hiểu`. Chưa được coi là scope đã chốt.
> **Ngày:** 2026-10-03 · **Soạn bởi:** Claude Code (Opus 5.5) · **Người duyệt:** Lê Đình Sơn (chưa duyệt)
> **Input:** `CLAUDE_AI_Tutor.md` (gọi tắt **CT**). Không có `context.md` gốc — mọi nội dung dưới đây chỉ dựa trên CT.
> **Quy trình:** `dev-book/PM-AI-Bootcamp-Capstone-Playbook-v1.0.md` bước [0].

Quy ước nhãn:
- `[ĐÃ DUYỆT]` — đã có trong CT như phạm vi/luật của chủ dự án.
- `[ĐỀ XUẤT]` — AI đề xuất làm giả định mặc định; chủ dự án đồng ý hoặc sửa.
- `[CHỜ LÀM RÕ — không để AI đoán]` — hard-stop; chưa chốt thì bước sau bị chặn ở mục ghi kèm.

---

## 1. Problem statement

Học sinh lớp 6 tự học Toán ở nhà trên sách/vở giấy. Khi các em sai ở **một bước trung gian** (ví dụ phân phối sai `3(x + 2) → 3x + 2`), thường không ai phát hiện kịp, nên lỗi lặp lại. Phụ huynh cũng không biết con vướng ở đâu. Các công cụ hiện có thường chấm **đáp án cuối** hoặc bắt học sinh chuyển sang làm trên app.

AI Study Companion muốn kiểm chứng giả thuyết: **một camera cố định nhìn xuống bàn có thể đọc đủ chính xác các bước viết tay trong một domain hẹp, để tutor can thiệp đúng lúc, ít can thiệp nhầm và ghi lại bằng chứng học tập đáng tin.** *(CT §2)*

Đây là **giả thuyết cần đo**, chưa phải năng lực đã có *(CT §3)*.

## 2. Scope MVP

### 2.1 In-scope MVP v0.1 `[ĐÃ DUYỆT]` *(CT §4)*
- Toán lớp 6, khoảng 20–30 dạng bài, taxonomy lỗi giới hạn.
- Smartphone trên giá nhìn xuống bàn **hoặc** laptop/USB webcam.
- Học trên sách/vở thật; tương tác bằng voice hoặc app.
- Student Model và Parent Dashboard cơ bản.
- Luồng 10 bước: onboarding/ghép thiết bị → cấu hình giờ & vùng bàn → bắt đầu phiên → theo dõi bước viết → OCR khi ảnh ổn định → kiểm chứng toán → chờ tự sửa → hint → learning event → tổng kết phiên.
- Trình tự: thử kỹ thuật nhỏ → pilot.

### 2.2 Lát cắt dọc đầu tiên `[ĐỀ XUẤT]` *(dựa trên CT §12)*
Start session → capture → detect change/quality → OCR observed step → verify step → tutor policy/hint → output → learning event → dashboard.
Mọi khâu chạy được với **mock adapter có nhãn rõ**. Khâu nào thay bằng integration thật thì phụ thuộc quyết định D3 (mục 4).

### 2.3 Out-of-scope `[ĐÃ DUYỆT]` *(CT §4)*
Mọi môn/lớp/kiểu chữ · suy đoán tâm lý/tập trung qua camera · lưu video mặc định · hardware sản xuất · tự huấn luyện foundation model · scale 100.000 học sinh.

### 2.4 Out-of-scope cho lát cắt đầu `[ĐỀ XUẤT]`
- **Parent live view (WebRTC/TURN).** Lý do: CT §12 không đưa vào chuỗi slice; đây là phần rủi ro privacy cao nhất (CT §5) → nên làm ở slice riêng, sau khi có auth và family authorization.
- **Billing/subscription, xuất/xóa dữ liệu tự phục vụ.** Đây là Layer 0 của pilot, chưa cần cho bản thử kỹ thuật.
- **Học sinh thật và dữ liệu trẻ em thật.** Bản thử kỹ thuật chỉ dùng trang viết tay của người lớn hoặc dữ liệu tổng hợp, cho tới khi qua các gate ở CT §10 và §13.

## 3. Giả định đang gánh `[ĐỀ XUẤT]`

| # | Giả định | Nếu sai thì |
|---|---|---|
| A1 | Chữ viết tay của học sinh lớp 6 trong ảnh crop ổn định có thể OCR đủ tốt để đạt ≥90% bước rõ được xử lý (mục tiêu CT §9). | Toàn bộ sản phẩm phải đổi hướng (vd. bắt viết theo mẫu, hoặc chụp chủ động). |
| A2 | Một rules/symbolic engine nhỏ đủ để kiểm chứng 20–30 dạng bài, kể cả lời giải tương đương. | Phải thu hẹp dạng bài hoặc thêm LLM vào khâu verify (rủi ro bịa). |
| A3 | Chờ ~20–30 giây trước khi hint là chấp nhận được về sư phạm. | Cần tham vấn giáo viên; đây là tham số policy. |
| A4 | Phụ huynh chấp nhận một camera nhìn xuống bàn nếu có các cơ chế ở CT §5. | Không thể pilot; giả định này phải kiểm bằng phỏng vấn, không bằng code. |
| A5 | Tìm được ít nhất một provider vision/OCR/voice có điều khoản hợp lệ cho người dùng dưới 18 tuổi, hoặc self-host khả thi. | Chặn pilot; chỉ dừng ở thử kỹ thuật. |
| A6 | Thiết bị smartphone/laptop phổ thông đủ sức chạy edge vision (phát hiện thay đổi, tay che, độ nét). | Phải đẩy nhiều xử lý lên server → tăng chi phí và lượng ảnh gửi đi. |

## 4. Quyết định nền

Ba quyết định **ràng buộc kiến trúc** — phải chốt trước bước [3] Architecture — được đánh dấu ⚑.

| ID | Quyết định | Đề xuất mặc định | Trạng thái |
|---|---|---|---|
| **D1** ⚑ | Thiết bị thu hình cho lát cắt đầu: smartphone hay laptop/USB webcam? | **Laptop + USB webcam chạy trên trình duyệt.** Dễ dev/debug, không cần build app mobile; smartphone để slice sau. | `[ĐỀ XUẤT]` |
| **D2** | Kênh phản hồi cho lát cắt đầu: voice realtime hay text/TTS? | **Text trên màn hình + TTS đơn giản.** Realtime voice (barge-in, turn-taking) là khối phức tạp riêng, lại phụ thuộc provider (D3). | `[ĐỀ XUẤT]` |
| **D3** ⚑ | Có được gửi ảnh tới API vision/OCR/LLM bên ngoài ở **giai đoạn thử kỹ thuật** (chỉ dữ liệu người lớn hoặc tổng hợp, không có trẻ em) không? Hay chỉ mock/self-host? | AI **không tự đề xuất**. Điều khoản provider phải được xác minh tại thời điểm quyết định (CT §10). | `[CHỜ LÀM RÕ — không để AI đoán]` → chặn khâu OCR/verify thật |
| **D4** ⚑ | Phân tách edge vs server: edge chỉ chọn ảnh (change/quality/tay che), còn OCR + verify + policy chạy ở server? | **Có.** Khớp CT §6–7: không gửi video liên tục; API key chỉ ở server. | `[ĐỀ XUẤT]` |
| **D5** | Ngôn ngữ/stack backend | Chưa đề xuất ở bước này. CT §6 ghi rõ "chưa chốt framework, ngôn ngữ hoặc cloud". Đây là việc của bước [3]. | Hoãn tới [3] |
| **D6** | Capstone Tier 1 (code chạy thật) hay Tier 2 (prototype + mock)? | **Tier 1**, vì CT §12 yêu cầu luồng end-to-end chạy lại được, kèm số đo latency/token thật. | `[CHỜ LÀM RÕ]` — người dùng chọn |

## 5. Câu hỏi làm rõ (10)

| # | Câu hỏi | Giả định mặc định nếu chưa trả lời | Nhãn |
|---|---|---|---|
| Q1 | Theo bộ sách giáo khoa lớp 6 nào (Kết nối tri thức / Chân trời sáng tạo / Cánh diều)? Ai chọn danh sách 20–30 dạng bài và taxonomy lỗi? | Lát cắt đầu chỉ làm **1 dạng**: phương trình bậc nhất có dấu ngoặc (khớp ví dụ ở CT §2). Lưu ý: cần xác nhận dạng này có nằm trong chương trình lớp 6 đang chọn hay không. | `[CHỜ LÀM RÕ]` — chặn [1] Spec phần nội dung |
| Q2 | Câu hỏi D3 (provider ở giai đoạn thử kỹ thuật). | Mock-only. | `[CHỜ LÀM RÕ — không để AI đoán]` |
| Q3 | Pilot ghi "20–50 học sinh và tối đa 100 hộ": 100 hộ là trần đăng ký/khảo sát, còn 20–50 là số học sinh dùng thật? Hai con số khác nhau chưa được giải thích. | 100 hộ = trần tuyển chọn; 20–50 = cohort dùng thật. | `[CHỜ LÀM RÕ]` — không chặn lát cắt đầu |
| Q4 | Team, thời gian và ngân sách cho giai đoạn thử kỹ thuật là gì? | Không đặt giả định. Playbook bước [5] cần con số này để đối chiếu. | `[CHỜ LÀM RÕ — không để AI đoán]` — chặn [5] |
| Q5 | Lưu dữ liệu ở đâu (khu vực/cloud)? CT nhắc EC2 nhưng ghi là "chưa có". | Chưa chọn. Khi lập kiến trúc, chỉ dùng local/dev. | `[CHỜ LÀM RÕ]` — chặn deploy, không chặn dev local |
| Q6 | Khung pháp lý bảo vệ dữ liệu cá nhân trẻ em tại Việt Nam áp dụng thế nào (consent, lưu trữ, xuất/xóa)? | AI **không tự diễn giải luật**. Cần chuyên gia pháp lý xác minh trước pilot. | `[CHỜ LÀM RÕ — không để AI đoán]` — chặn pilot |
| Q7 | Dataset để đo OCR lấy từ đâu? Dữ liệu được phép dùng cho đánh giá (CT §13) gồm những gì? | Trang viết tay do người lớn trong đội tự tạo + dữ liệu tổng hợp; không dùng ảnh trẻ em. | `[ĐỀ XUẤT]` |
| Q8 | Giọng/ngôn ngữ tutor: chỉ tiếng Việt? Xưng hô "em"? | Tiếng Việt, xưng "em" như ví dụ ở CT §2. | `[ĐỀ XUẤT]` |
| Q9 | Dashboard của lát cắt đầu dành cho ai: học sinh, phụ huynh hay đội dev? | Trang tổng kết phiên nội bộ cho đội dev (hiện learning events + uncertainty). Parent Dashboard thật làm ở slice sau, khi có auth. | `[ĐỀ XUẤT]` |
| Q10 | Khi OCR không chắc, tutor hỏi lại bằng cách nào: yêu cầu dịch vở, viết lại, hay xác nhận bằng nút bấm? | Hiện thông báo "chưa đọc rõ — dịch vở/viết rõ hơn" và abstain, không đánh giá. | `[ĐỀ XUẤT]` |

## 6. Hard-stop đang mở

1. **D3 / Q2 — provider ở giai đoạn thử kỹ thuật.** Chưa chốt thì lát cắt chỉ chạy mock cho OCR/verify/hint. Không gọi API ngoài nào.
2. **Q4 — team/thời gian/ngân sách.** Thiếu thì bước [5] Estimation không đối chiếu được.
3. **Q6 — pháp lý dữ liệu trẻ em.** Chặn mọi hoạt động có trẻ em thật.
4. **D6 — chọn Tier.**

## 7. Done khi (theo Playbook [0])

- [x] Có problem statement.
- [x] Có danh sách giả định.
- [x] Có quyết định nền và đánh dấu quyết định ràng buộc kiến trúc.
- [x] Có out-of-scope rõ.
- [ ] **Chủ dự án duyệt mục 3–5** (đồng ý/sửa từng `[ĐỀ XUẤT]`, trả lời các `[CHỜ LÀM RÕ]` có thể trả lời).
- [ ] **🔒 Cổng hiểu (người làm, AI không làm thay):**
  1. Chủ dự án nói bằng lời của mình: *MVP này CỐ TÌNH bỏ cái gì, và vì sao bỏ được?*
  2. Chủ dự án chỉ ra **≥1 giả định/đề xuất của AI ở trên mà mình không đồng ý** hoặc sửa lại; ghi vào mục 8.

## 8. Ghi nhận người-sửa (PM-edit)

| # | AI đề xuất | Người sửa thành | Lý do |
|---|---|---|---|
| — | *(chờ chủ dự án điền)* | | |

## 9. Telemetry

| Trường | Giá trị |
|---|---|
| Tool | Claude Code · Opus 5.5 |
| Token (est) | ~15k output cho tài liệu này (ước tính thô, chưa reconcile) |
| Thời gian (giờ người thật) | N/A — chủ dự án điền thời gian review |
| Số vòng lặp | 1 (bản nháp đầu) |
| Rework | Chưa |
| PM-edit | Chưa có — xem mục 8 |
