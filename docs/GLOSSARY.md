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

| Thuật ngữ | Nghĩa | Nguồn |
|---|---|---|
| **Student Learning Model** | Mô hình dài hạn mỗi học sinh: concept, lỗi lặp, mức hỗ trợ, khả năng tự sửa, retention, hiệu quả từng kiểu hint. | CT §2 |
| **Learning event** | Bản ghi một sự kiện học (concept, bước quan sát, loại lỗi, hint level, tự sửa, chất lượng bằng chứng). Schema **chưa chốt**. | CT §8 |
| **Edge Vision** | Xử lý tại thiết bị: phát hiện đổi trang/chữ mới/tay che/độ nét, sampling theo sự kiện. | CT §6 |
| **Quality gate (ảnh)** | Điều kiện ảnh đủ ổn định/rõ trước khi OCR. | CT §6–7 |
| **ROI (vùng bàn học)** | Vùng ảnh được cấu hình để quan sát. | CT §4, §6 |
| **Abstain / abstention** | Tutor chủ động không kết luận khi bằng chứng chưa đủ; được đo riêng. | CT §7, §9 |
| **Coverage** | Tỷ lệ bước được xử lý trong domain hỗ trợ (mục tiêu pilot ≥90% bước rõ). | CT §9 |
| **False intervention** | Can thiệp sửa sai nhầm khi học sinh không sai (mục tiêu pilot <2%). | CT §9 |
| **Hint level** | Cấp gợi ý đi từ nhẹ đến cụ thể; hạn chế đưa đáp án. | CT §7 |
| **Chờ tự sửa** | Policy sư phạm chờ ~20–30 giây trước khi gợi ý; không phải latency hệ thống. | CT §7 |
| **TTL** | Thời gian sống của ảnh tạm/phiên; hết hạn thì xoá. | CT §5–6 |
| **TURN fallback** | Relay khi WebRTC P2P không kết nối được cho parent live. | CT §6 |
| **page_version / problem_version** | Trường phiên bản trong event để chống lặp, sai thứ tự, hint cho trạng thái cũ. | CT §8 |
