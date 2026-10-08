# GLOSSARY — Thuật ngữ AI Tutor & PM AI Bootcamp

> **Tình trạng:** bản **tạm, do agent dựng lại** ngày 2026-10-03, vì `docs/GLOSSARY.md` gốc của chương trình bootcamp được các file `dev-book/` trỏ tới nhưng **không có trong repository**.
> Mọi định nghĩa dưới đây **chỉ rút từ nội dung có trong repo**; cột "Nguồn" ghi file gốc. Thuật ngữ được dùng nhưng repo không định nghĩa thì ghi rõ *"chưa có định nghĩa trong repo"* — không tự bịa.
> Khi có bản GLOSSARY chính thức, thay file này bằng bản đó và giữ lại phần "AI Study Companion" nếu bản chính thức không có.

Viết tắt nguồn: **CT** = `CLAUDE_AI_Tutor.md` · **CP** = Capstone Playbook · **WC/WB/WS/WD** = Workbook Common/BA/SA/Dev · **PB** = ProjectBriefs.

## 1. Quản trị ủy quyền cho AI

| Thuật ngữ | Nghĩa | Nguồn |
|---|---|---|
| **Thang L0–L5** | Mức ủy quyền AI: L0 Observe · L1 Draft · L2 Recommend · L3 Execute-bounded · L4 Operate-workflow · L5 Restricted. | WC EX-06 |
| **Leash A / A+** | Hai nấc vận hành cắt từ thang L0–L5, không phải khung khác. **A ≈ L3**: vùng an toàn, AI làm tới bản nháp, không tự release/merge. **A+ ≈ L4**: việc chạm dữ liệu nhạy cảm/phân quyền/bảo mật → bắt buộc người duyệt trước khi dùng. | WC EX-06, CP [6] |
| **Nhóm 5-loại** | Phân loại task khi giao việc: AI-do / Human-do / AI-review / Human-review / AI-không-nên. | WC EX-06, WB EX-06 |
| **Fail-closed (cổng mặc-định-đóng)** | Cổng kiểm mà khi không xác minh được thì **chặn**, không "tạm cho qua". | CP [9], WD EX-04 |
| **BUILT-flagged** | Trạng thái kết quả đã dựng xong nhưng bị gắn cờ **chờ người duyệt** — mọi task A+ đi vào trạng thái này. | WC EX-06, CP [6] |
| **Hard-stop** | Phản xạ dừng lại khi yêu cầu mâu thuẫn/không đủ để quyết; ghi `[CHỜ LÀM RÕ]`, không để AI đoán. | WC EX-01, CP [6] |
| **Rubber-stamping** | Duyệt/ký bừa output AI mà không đọc hiểu, không có dấu vết review. Tiêu chí trượt (tối đa 1 điểm). | WC facilitator notes, CP Quy tắc số 1 |
| **CASAN** | Được dùng cùng "Leash" với tinh thần *con người quyết định — AI là lực thực thi*. **Chưa có định nghĩa đầy đủ trong repo.** | CP, PB-06 |
| **Harness** | Bộ khung quanh model gồm 3 mảnh: **context** (nạp đúng dữ liệu) · **tool** (gọi hàm/API thật) · **gate** (kiểm đầu ra fail-closed). | WD EX-04 |
| **AgentOps** | Ghi log quyết định của agent để theo dõi/vận hành. Repo chỉ nhắc mức "mini". | WD EX-04 |

## 2. Quy trình Capstone & artefact

| Thuật ngữ | Nghĩa | Nguồn |
|---|---|---|
| **Customer Zero** | Phase 3 Capstone: tự tay lái AI dựng một hệ thống **chạy được** — bằng chứng tốt nghiệp số 1. Tham chiếu mẫu: RevenueOS. | CP |
| **Lát cắt dọc / Walking Skeleton / Vertical slice** | Một luồng mỏng chạy xuyên mọi tầng (móng → API → màn hình) trước khi mở rộng bề rộng. | CP [2], [7] |
| **Móng ẩn (Layer 0)** | Nền dùng chung: auth, data model, phân quyền, gateway — phải xong trước module bề mặt. | CP [2] |
| **Rolling-Wave** | Wave gần bẻ sâu tới task (~0.5–2 ngày), wave xa để thô (feature/epic) một cách cố ý. | CP [4] |
| **DoR (Definition of Ready)** | Checklist PASS/FAIL trước khi build một lát cắt; chưa PASS thì không build. | CP [7] |
| **🔒 Cổng hiểu** | Điều kiện qua mỗi bước: tự giải thích bằng lời + bắt được ≥1 lỗi AI. | CP |
| **Dev Book (DEVBOOK)** | Nhật ký mỗi lần AI sai → người sửa: AI làm gì, sai đâu, sửa thế nào, mức L, cổng nào chặn. | CP [8] |
| **RTM** | Ma trận truy vết story → code → test; không để story "mồ côi". | CP [10] |
| **SIT / UAT** | Kiểm thử tích hợp hệ thống / kiểm thử nghiệm thu người dùng. | CP [9] |
| **ADR** | Architecture Decision Record: bối cảnh · lựa chọn · lý do · hệ quả · phương án bị loại. | WS EX-01 |
| **4 lăng kính (Design-first)** | Rà thiết kế qua Req / SIT / UAT / Arch. | WS EX-04 |
| **STRIDE** | Threat model: Spoofing / Tampering / Repudiation / Info-disclosure / DoS / Elevation. | WS EX-04 |
| **INVEST** | Tiêu chí story: Independent / Negotiable / Valuable / Estimable / Small / Testable. | WB EX-02 |
| **Gherkin** | AC dạng Given / When / Then. | WB EX-02 |
| **MoSCoW** | Ưu tiên Must / Should / Could / Won't. | WB EX-04 |
| **3-point estimate** | Ước lượng lạc quan / khả dĩ / bi quan, quy ra MD (người-ngày). | WC EX-03 |
| **Tier 1 / Tier 2** | Hai nấc Capstone: Full-stack (code chạy thật) / PM-stack (prototype + API mock + schema + test scenario). | CP [8] |
| **PEP–PDP–RLS** | Được nêu là mô hình "phân quyền 5 lớp" của RevenueOS. **Chi tiết chưa có trong repo.** | CP [3] |

## 3. Telemetry & năng lực

| Thuật ngữ | Nghĩa | Nguồn |
|---|---|---|
| **Telemetry bắt buộc** | Tool · Token (est) · Thời gian · Số vòng lặp · Rework · PM-edit/Dev-edit. | WC, WD |
| **PM-edit / Dev-edit** | ≥1 điểm người sửa sai/nắn intent của AI — bằng chứng phán đoán quan trọng nhất. | WC, WD |
| **est → reconcile** | Token ghi ước tính, cuối kỳ đối chiếu lại nếu có số thật. | WC |
| **Giờ thật** | Thời gian đo bằng giờ người làm thật, không suy từ token. | WC, CP [10] |
| **Nén** | KPI = giờ truyền thống ÷ giờ thật. | CP [10] |
| **MD/1M-token** | KPI hiệu quả token (người-ngày trên 1 triệu token). | CP [10] |
| **C1–C6** | Năng lực: C1 AI Literacy · C2 (AI) Delegation · C3 Workflow Design · C4 Governance & Risk · C5 Telemetry & Economics · C6 Outcome. | WC |

## 4. AI Study Companion (sản phẩm)

> Cập nhật 2026-10-08 theo baseline v1.3 (`docs/product/`). Viết tắt: **BH** = Business HLD v1.3 · **TH** = Technical HLD v1.3 · **CX** = context v0.5. Thuật ngữ của bản 03/10 (Edge Vision liên tục, ROI, chờ tự sửa 20–30 giây, TURN/WebRTC, `page_version`) đã bỏ; xem lịch sử Git.

| Thuật ngữ | Nghĩa | Nguồn |
|---|---|---|
| **D01–D31 / U01–U25 / A01–A46** | Mã quyết định / use case / acceptance của baseline v1.3. Số giữ nguyên qua phiên bản; mã mới nhận số tiếp theo. Mã cũ (SC-xx, U01–U17, A01–A31) không dùng nữa. | BH §0, §5.3; TH §15 |
| **Tờ đề / bộ đề (SessionProblemSet)** | Đề in (giáo viên/phụ huynh) hoặc phiếu hệ thống, **tối đa 1 trang**, chụp đầu buổi, xác nhận câu/ý bằng giọng nói; có version. | BH D11, D16; TH §5.1 |
| **Số câu trong vở (nhãn câu)** | Trẻ ghi số câu ở lề trái vở trước khi làm (`1) 5x + 3 = 28`); `ItemResolver` đọc để gắn lời giải với câu; lệnh "Câu N" là dự phòng. | BH D15; TH §5.3, §8.3 |
| **Item** | Một câu/ý trong bộ đề; đơn vị chấm và báo cáo. | TH §8.7 |
| **Run (SessionRun)** | Một lượt học trên bộ đề; học tiếp tạo `run_id` mới, output run cũ bị loại. | TH §8.7 |
| **ItemProgress** | `NOT_STARTED`, `IN_PROGRESS`, `STUDENT_MARKED_DONE`, `NEEDS_REVISION`, `UNVERIFIED`, `VERIFIED`; cờ `NEEDS_SCOPE_REVIEW`, `UNSUPPORTED`. | TH §8.7 |
| **Phạm vi đã học (LearnedScope)** | Danh sách bài/kỹ năng trẻ đã học, có version; gợi ý không được vượt ra ngoài. Đã học ≠ đã thành thạo. Trong pilot do shadow teacher xác nhận. | BH D13, D25; TH §8.2 |
| **Shadow teacher** | Giáo viên đồng hành của dự án: xác nhận phạm vi đã học và rà, gán nhãn từng phản hồi AI qua lịch sử học tập; không đứng giữa trẻ và AI lúc học. | BH D25, U25; TH §8.11 |
| **Ẩn danh hóa (Deidentifier)** | Trước khi gửi nhà cung cấp AI: bỏ metadata ảnh, che dải đầu trang, không gửi mã người dùng/học sinh/phiên. | BH D26; TH §5.7; A43 |
| **ValidatorRegistry** | Bộ đăng ký bộ chấm theo domain; MVP có số học/đại số; hình học thêm sau pilot không đổi pipeline. | BH D30; TH §8.5; A45 |
| **Scope gate** | Kiểm mỗi item có ít nhất một phương pháp giải trong phạm vi đã học; không chắc → `NEEDS_SCOPE_REVIEW`. | TH §8.2 |
| **Evidence gate** | Kiểm đủ bằng chứng trước khi kết luận Toán; thiếu → hỏi lại, không tính là gợi ý. | TH §8.4 |
| **UNKNOWN ≠ WRONG** | Không chắc thì không phán sai; hỏi lại bằng câu hỏi đóng. | CX §2; TH §1 |
| **Dòng sai gốc** | Dòng đầu tiên làm sai trong lời giải; cô chỉ nhắm vào dòng này. | TH §8.5 |
| **L1 / L2 / L3** | Mức gợi ý: nhắc nhẹ / khái niệm / một bước trung gian (chỉ khi trẻ hỏi thêm). | BH §5.5 |
| **Output filter** | Chặn gợi ý lộ đáp án ở L1/L2, ngoài lề, ngoài phạm vi, sai so với validator. | TH §8.6 |
| **Từ gọi "Cô ơi"** | Wake word nhận diện trên máy; chỉ đoạn sau từ gọi được gửi lên ASR. | BH D24; TH §4.2 |
| **Thẻ lệnh** | Thẻ in KIỂM TRA, GIÚP CON, XONG có marker; dự phòng cho giọng nói. | TH §4.3 |
| **Rảnh tay / không chạm máy** | Mọi bước trong buổi học, kể cả chụp đề, không bắt trẻ chạm máy. | BH D03 |
| **Ảnh gần trực tiếp** | Ảnh vùng giấy độ phân giải thấp, mỗi vài giây, khi phụ huynh đang xem; không phải live video. | BH D17; TH §5.5 |
| **Chặn người (`person_check`)** | Frame có người/khuôn mặt bị chặn trên máy; server từ chối ảnh khi `person_check != PASSED`. | TH §1, §7.1 |
| **Đồng ý loại 1 / loại 2** | Dùng dịch vụ (bắt buộc) / dùng ảnh cải thiện hệ thống (tùy chọn, rút được). | BH §7 |
| **Phiếu bài hệ thống (worksheet)** | Phiếu sinh theo lỗ hổng từ template + CAS, có dấu bốn góc và mã phiếu. | BH D16; TH §8.8 |
| **North Star** | Tỷ lệ câu/ý đúng ở lần kiểm tra đầu trên tổng câu/ý của các đề đã làm. | BH §8.1 |
| **Cổng S / G0 / G1 / G2 / go-no-go** | Cổng pilot: spike tuần 1 / replay và máy thật tuần 5 / alpha tuần 6 / mở 50 gia đình tuần 7 / quyết định cuối tuần 10. | BH §11 |
| **Harness replay** | Chạy ảnh đề, bài làm, âm thanh thật qua hệ thống, chấm theo acceptance; model mới phải qua trước khi bật. | TH §12; A29 |
| **Fake adapter** | Adapter giả cho vertical slice; phải gắn nhãn, không trình bày như kết quả thật. | TH §14 |
| **TTL ảnh** | Ảnh tự xóa sau 7 ngày hoặc theo cài đặt phụ huynh; text đề và tiến độ vẫn giữ. | BH D20; A39 |
