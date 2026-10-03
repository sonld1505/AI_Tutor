# PM AI Bootcamp — Bộ đề bài dự án mẫu (Project Brief Bank) v2.0

> **Mục đích:** thay vì 300 PM làm chung 1 case "LMS", anh có **6 đề bài cụ thể** để giao cho từng nhóm. Mỗi đề mô tả **requirement đủ kỹ + nền tảng công nghệ rõ ràng** để PM bắt tay làm ngay 6 bài tập **EX-01→EX-06** trong Workbook (Requirement → WBS → Estimation → Risk → Weekly report → Delegation Map).
>
> **Cách dùng:** chọn 1 đề / nhóm PM → PM chạy nguyên 6 bài tập trên đề đó (thay chữ "LMS" trong Workbook bằng mã đề, vd `REQ-PB01.md`, `WBS-PB01.md`…). Giảng viên chấm **phán xử của PM**, không chấm "AI trả lời hay".
>
> **⭐ Nhận đề xong làm gì, theo thứ tự nào?** Xem **Capstone Playbook** — đường ray **11 bước** dắt từ tờ đề → SW spec → Architecture → WBS → build lát cắt dọc **chạy được** → test/gate → RTM/telemetry → viva, lấy đúng chuỗi RevenueOS thật làm mẫu. Playbook là **sợi chỉ xâu 6 drill EX-01→EX-06** lại thành một mạch.
>
> **Đề được viết để DỄ HIỂU:** bài toán quen thuộc, scope gọn cho MVP, công nghệ phổ thông. Mỗi đề cài **1–2 "điểm cần PM làm rõ"** (requirement cố ý thiếu/mâu thuẫn) để luyện phản xạ **hard-stop** ở EX-01. Ngoài ra, scope mỗi đề **cố tình hơi quá sức** cho team + mốc thời gian — để EX-03 bắt buộc PM phải **cắt scope + viết trade-off** (iteration loop).
>
> **Thuật ngữ:** tra cứu tại `docs/GLOSSARY.md` — bảng thuật ngữ thống nhất có cột mapping sang ngành.

---

## Mục lục 6 đề

| Mã | Tên dự án | Domain | Loại nền tảng | Độ khó | Gợi ý giao cho |
|---|---|---|---|---|---|
| **PB-01** | Website bán hàng online (cửa hàng vừa) | E-commerce | Web (FE+BE+DB) | ★★☆ | Nhóm web/full-stack |
| **PB-02** | App đặt lịch khám phòng khám | Booking | Mobile + API | ★★☆ | Nhóm mobile |
| **PB-03** | Hệ thống quản lý kho nội bộ | Internal tool | Web + DB | ★☆☆ | Nhóm mới / dễ nhất |
| **PB-04** | Dashboard báo cáo bán hàng | Data / BI | Data pipeline + Web | ★★☆ | Nhóm data |
| **PB-05** | App tích điểm khách hàng thân thiết | Mobile loyalty | Mobile + Backend | ★★☆ | Nhóm mobile/backend |
| **PB-06** | Tính năng AI tóm tắt & trích xuất hợp đồng | AI feature | AI add-on trên SaaS | ★★★ | Nhóm core (sát chủ đề khoá) |

> **Cấu trúc mỗi đề:** Bối cảnh · Mục tiêu kinh doanh · Phạm vi MVP (In/Out) · Người dùng & stakeholder · Yêu cầu chức năng · Yêu cầu phi chức năng (NFR) · **Nền tảng & công nghệ** · Team & thời gian · Ràng buộc & dữ liệu nhạy cảm · Điểm cần PM làm rõ (cho EX-01) · Gợi ý đáp án cho giảng viên.

---

## PB-01 — Website bán hàng online cho cửa hàng vừa

**Bối cảnh.** Cửa hàng thời trang có 1 showroom + bán qua Facebook/Zalo, đơn ghi tay nên hay sót, không tra cứu được tồn kho. Chủ muốn có **website bán hàng riêng** để khách tự đặt, thanh toán và theo dõi đơn.

**Mục tiêu kinh doanh.** Tăng đơn online, giảm thao tác chốt đơn thủ công, có số liệu doanh thu theo ngày.

**Phạm vi MVP (8 tuần).**
- **In-scope:** danh mục sản phẩm (ảnh, giá, mô tả, size/màu) · tìm kiếm & lọc · giỏ hàng · đặt hàng (không bắt buộc đăng ký) · thanh toán online + COD · trang quản trị cho chủ shop (thêm/sửa sản phẩm, xem & cập nhật trạng thái đơn) · email xác nhận đơn.
- **Out-of-scope (MVP):** app mobile riêng · tích điểm/khuyến mãi nâng cao · nhiều chi nhánh · đa ngôn ngữ · tích hợp đơn vị vận chuyển tự động (giai đoạn sau).

**Người dùng & stakeholder.** Khách mua hàng (web) · Nhân viên/chủ shop (trang quản trị) · Chủ shop = người duyệt nghiệm thu.

**Yêu cầu chức năng (rút gọn — PM sẽ chi tiết hoá ở EX-01).**
1. Khách xem danh sách & chi tiết sản phẩm, lọc theo loại/giá.
2. Khách thêm vào giỏ, đặt hàng với thông tin giao hàng.
3. Khách chọn thanh toán: cổng online hoặc COD.
4. Hệ thống gửi email xác nhận, sinh mã đơn để tra cứu.
5. Quản trị: CRUD sản phẩm, quản lý tồn kho cơ bản, đổi trạng thái đơn (Mới → Đang giao → Hoàn tất/Huỷ).
6. Trang tổng quan doanh thu theo ngày/tuần.

**Yêu cầu phi chức năng (NFR).**
- Tải trang sản phẩm < 2.5s với ~1.000 sản phẩm.
- Chịu được ~200 người dùng đồng thời lúc cao điểm (đợt sale).
- Bảo mật: HTTPS, không tự lưu số thẻ (đẩy cho cổng thanh toán xử lý).
- Responsive (đa số khách vào bằng điện thoại).

**Nền tảng & công nghệ (yêu cầu).**
- **Frontend:** ReactJS (Next.js), responsive web.
- **Backend:** Node.js (NestJS) hoặc Java Spring Boot — REST API.
- **CSDL:** PostgreSQL.
- **Thanh toán:** tích hợp 1 cổng nội địa (VNPay **hoặc** MoMo) qua API.
- **Lưu ảnh:** object storage (AWS S3 hoặc tương đương).
- **Hạ tầng/triển khai:** Docker, deploy lên 1 cloud (AWS/Azure), CI/CD cơ bản (GitHub Actions).
- **Email:** dịch vụ gửi mail (SendGrid/SES).

**Team & thời gian.** 4 người (1 PM kiêm BA · 2 dev fullstack · 1 QA), 8 tuần.

**Ràng buộc & dữ liệu nhạy cảm.** Thông tin khách (tên, SĐT, địa chỉ giao hàng) = dữ liệu cá nhân → cần bảo vệ. Luồng thanh toán = vùng nhạy cảm (đụng tiền).

**🔎 Điểm cần PM làm rõ (cho EX-01).**
- Brief nói "thanh toán online" nhưng **không nói rõ xử lý khi thanh toán thất bại / hoàn tiền** → PM phải hỏi lại, không tự suy diễn.
- "Quản lý tồn kho cơ bản" chưa định nghĩa: tồn kho có trừ ngay khi đặt hay khi xác nhận đơn? (ảnh hưởng oversell).

**🧑‍🏫 Gợi ý cho giảng viên.**
- WBS thường **sót**: tích hợp cổng thanh toán + xử lý callback/đối soát, seed dữ liệu sản phẩm, trang quản trị, kiểm thử thanh toán sandbox.
- Delegation Map: tích hợp thanh toán & sửa trạng thái đơn → **A+ (≈L4)**, người duyệt; sinh mô tả sản phẩm/UI tĩnh → **A (≈L3)**.
- **EX-01 Stakeholder simulation:** ví dụ yêu cầu thêm cho PB-01: *"Anh muốn có mã giảm giá / coupon trong MVP luôn, bán đợt khai trương cần có."* PM đúng nên trả lời: ảnh hưởng timeline + đề xuất "đợt khai trương sửa giá tay, coupon vào phase 2".
- **EX-03 Trade-off:** scope PB-01 (thanh toán online + admin + tồn kho + dashboard) gần chắc vượt 130 MD khả dụng (4 người × 8 tuần trừ meeting). PM **phải cắt** — chấm cái cắt hợp lý + diff v1→v2.
- **EX-05 Hallucination:** dữ liệu tuần 3 không có "doanh thu", "conversion rate", "tốc độ tải trang". Nếu AI bịa → PM phải bắt và thay bằng "N/A".

---

## PB-02 — App đặt lịch khám cho phòng khám

**Bối cảnh.** Phòng khám đa khoa nhỏ đang nhận đặt lịch qua điện thoại → nghẽn máy giờ cao điểm, hay trùng giờ bác sĩ. Muốn có **app cho bệnh nhân tự đặt lịch** và màn quản lý lịch cho lễ tân.

**Mục tiêu kinh doanh.** Giảm cuộc gọi đặt lịch, hạn chế trùng/sót lịch, nhắc bệnh nhân đúng giờ để giảm no-show.

**Phạm vi MVP (8 tuần).**
- **In-scope:** xem danh sách bác sĩ & chuyên khoa · xem khung giờ trống · đặt/huỷ lịch · nhắc lịch (push + SMS) · màn lễ tân quản lý lịch trong ngày · xác nhận/đổi lịch.
- **Out-of-scope (MVP):** hồ sơ bệnh án điện tử · thanh toán viện phí · video khám từ xa · bảo hiểm.

**Người dùng & stakeholder.** Bệnh nhân (app) · Lễ tân (màn quản lý) · Quản lý phòng khám = duyệt nghiệm thu · (Bác sĩ chỉ xem lịch của mình ở MVP).

**Yêu cầu chức năng.**
1. Bệnh nhân đăng ký/đăng nhập bằng số điện thoại (OTP).
2. Chọn chuyên khoa → bác sĩ → khung giờ còn trống → đặt.
3. Nhận xác nhận + nhắc trước giờ khám (push & SMS).
4. Huỷ/đổi lịch trong giới hạn cho phép (vd trước 2 giờ).
5. Lễ tân xem lịch theo ngày, xác nhận bệnh nhân đến, chặn giờ nghỉ của bác sĩ.

**Yêu cầu phi chức năng (NFR).**
- Không cho đặt trùng 1 khung giờ của cùng bác sĩ (khoá tranh chấp).
- Phản hồi đặt lịch < 1.5s.
- Hoạt động ổn trên Android & iOS đời ~3 năm gần đây.
- Dữ liệu bệnh nhân được bảo vệ, có nhật ký thao tác lễ tân.

**Nền tảng & công nghệ (yêu cầu).**
- **Mobile:** Flutter **hoặc** React Native (1 codebase cho cả iOS & Android).
- **Backend:** Node.js (NestJS) hoặc Spring Boot — REST API.
- **CSDL:** PostgreSQL.
- **Push notification:** Firebase Cloud Messaging.
- **SMS/OTP:** dịch vụ SMS brandname (Twilio hoặc nhà cung cấp nội địa).
- **Màn lễ tân:** web (ReactJS).
- **Hạ tầng:** Docker + cloud, CI/CD cơ bản.

**Team & thời gian.** 5 người (1 PM · 2 mobile dev · 1 backend · 1 QA), 8 tuần.

**Ràng buộc & dữ liệu nhạy cảm.** Thông tin bệnh nhân (tên, SĐT, lý do khám) = nhạy cảm. OTP/đăng nhập = vùng bảo mật.

**🔎 Điểm cần PM làm rõ (cho EX-01).**
- Brief vừa muốn "đặt lịch realtime" vừa nói "lễ tân duyệt từng lịch" → hai luồng có thể mâu thuẫn (tự động vs duyệt tay). PM phải làm rõ quy tắc.
- "Nhắc bằng SMS" nhưng chưa rõ ngân sách SMS / số lần nhắc → ràng buộc chi phí.

**🧑‍🏫 Gợi ý cho giảng viên.**
- WBS dễ sót: xử lý tranh chấp khung giờ (concurrency), tích hợp SMS/OTP & chi phí, kiểm thử trên thiết bị thật.
- Delegation Map: đăng nhập/OTP, gửi SMS tới bệnh nhân → **A+ (≈L4)**; sinh màn hình tĩnh, text thông báo → **A (≈L3)**.
- **EX-01 Stakeholder simulation:** ví dụ: *"Bác sĩ muốn xem hồ sơ bệnh án ngay trên app — tiện khám."* PM nên trả lời: hồ sơ bệnh án = out-of-scope MVP + dữ liệu y tế nhạy cảm → phase 2, cần đánh giá compliance.
- **EX-03 Trade-off:** scope mobile + backend + SMS/OTP + lễ tân web → 5 người × 8 tuần sát. PM nên cắt hoặc simplify (vd: bỏ SMS nhắc, dùng push notification thay thế).
- **EX-05 Hallucination:** watch out AI bịa "tỷ lệ no-show" hoặc "số lượt đặt lịch" khi dữ liệu không có.

---

## PB-03 — Hệ thống quản lý kho nội bộ *(đề dễ nhất, hợp nhóm mới)*

**Bối cảnh.** Công ty phân phối đang quản lý kho bằng Excel → khó biết tồn thực tế, hay nhầm khi nhập/xuất. Muốn một **web nội bộ quản lý nhập–xuất–tồn** đơn giản, dùng nội bộ.

**Mục tiêu kinh doanh.** Biết chính xác tồn kho theo thời gian thực, giảm sai sót nhập/xuất, có lịch sử truy vết.

**Phạm vi MVP (6 tuần).**
- **In-scope:** danh mục hàng hoá · phiếu nhập kho · phiếu xuất kho · xem tồn hiện tại · lịch sử giao dịch · báo cáo tồn theo kỳ · phân quyền 2 vai trò (Thủ kho nhập liệu · Quản lý xem báo cáo).
- **Out-of-scope (MVP):** nhiều kho/chi nhánh · mã vạch/máy quét · tích hợp kế toán · dự báo nhu cầu.

**Người dùng & stakeholder.** Thủ kho (nhập liệu) · Quản lý kho (xem báo cáo, duyệt điều chỉnh) · Trưởng phòng = duyệt nghiệm thu.

**Yêu cầu chức năng.**
1. CRUD danh mục hàng hoá (mã, tên, đơn vị, tồn tối thiểu).
2. Tạo phiếu nhập (nhiều dòng hàng) → tồn tăng.
3. Tạo phiếu xuất → tồn giảm, chặn xuất quá tồn.
4. Xem tồn hiện tại + cảnh báo hàng dưới mức tối thiểu.
5. Báo cáo nhập–xuất–tồn theo khoảng thời gian, xuất Excel.
6. Phân quyền: thủ kho không xem được báo cáo tài chính tổng.

**Yêu cầu phi chức năng (NFR).**
- Tồn kho luôn khớp lịch sử giao dịch (không âm, có kiểm toán).
- ~20 người dùng nội bộ đồng thời.
- Mọi thao tác sửa/xoá đều ghi log ai làm, lúc nào.

**Nền tảng & công nghệ (yêu cầu).**
- **Frontend:** ReactJS (hoặc Vue) — web nội bộ.
- **Backend:** Spring Boot **hoặc** .NET — REST API.
- **CSDL:** MySQL hoặc PostgreSQL.
- **Xuất Excel:** thư viện sẵn (Apache POI / EPPlus).
- **Triển khai:** chạy nội bộ (on-prem server công ty) hoặc cloud nội bộ, Docker.
- **Xác thực:** đăng nhập tài khoản nội bộ (có thể nối LDAP/AD nếu sẵn).

**Team & thời gian.** 3 người (1 PM · 2 dev), 6 tuần.

**Ràng buộc & dữ liệu nhạy cảm.** Dữ liệu nội bộ; điểm nhạy cảm chính là **phân quyền** (thủ kho không được xem/sửa vùng của quản lý) và **điều chỉnh tồn thủ công** (dễ bị lạm dụng).

**🔎 Điểm cần PM làm rõ (cho EX-01).**
- "Chặn xuất quá tồn" nhưng thực tế có trường hợp **điều chỉnh kiểm kê** (tồn lệch do mất/hỏng) → cần cơ chế điều chỉnh có người duyệt, brief chưa nói.
- Phân quyền mới nêu 2 vai trò — ai được **sửa danh mục hàng**? Chưa rõ.

**🧑‍🏫 Gợi ý cho giảng viên.**
- Đề dễ nhất → tốt để dạy WBS sạch & estimation. Sót thường gặp: màn phân quyền, log kiểm toán, nghiệp vụ điều chỉnh tồn.
- Delegation Map: sửa phân quyền & điều chỉnh tồn → **A+ (≈L4)**, người duyệt; CRUD danh mục, báo cáo chỉ-đọc → **A (≈L3)** hoặc thấp hơn.
- **EX-01 Stakeholder simulation:** ví dụ: *"Kho muốn thêm quét barcode từ điện thoại."* PM nên trả lời: quét barcode = scope hardware + mobile app → ngoài MVP 6 tuần, ghi phase 2.
- **EX-03 Trade-off:** đề 3 người × 6 tuần — scope gọn nhưng PM hay quên log kiểm toán + phân quyền; nếu estimate vượt → cắt xuất Excel (dùng CSV thay).
- **EX-05 Hallucination:** AI hay bịa "tỷ lệ phân quyền sai" hoặc "số lượt điều chỉnh tồn" khi data không có → buộc PM bắt.

---

## PB-04 — Dashboard báo cáo bán hàng

**Bối cảnh.** Ban giám đốc đang xem doanh số qua các file Excel gửi rời từ 3 chi nhánh → tổng hợp chậm, số liệu lệch nhau. Muốn một **dashboard điều hành** gom số liệu về một chỗ, cập nhật hằng ngày.

**Mục tiêu kinh doanh.** Lãnh đạo thấy bức tranh doanh số toàn công ty mỗi sáng, ra quyết định nhanh, hết cảnh "mỗi báo cáo một số".

**Phạm vi MVP (8 tuần).**
- **In-scope:** gom dữ liệu bán hàng từ **3 nguồn** (1 hệ thống bán hàng có API + 2 chi nhánh gửi file Excel) · làm sạch & chuẩn hoá · 1 kho dữ liệu chung · dashboard: doanh thu theo thời gian/chi nhánh/nhóm hàng, top sản phẩm, so sánh kỳ · cập nhật hằng ngày tự động.
- **Out-of-scope (MVP):** dự báo bằng ML · phân tích hành vi khách · realtime từng phút · phân quyền xem theo từng nhân viên.

**Người dùng & stakeholder.** Ban giám đốc & trưởng phòng kinh doanh (xem dashboard) · Bộ phận dữ liệu (vận hành pipeline) · Giám đốc = duyệt nghiệm thu.

**Yêu cầu chức năng.**
1. Kết nối & lấy dữ liệu từ API hệ thống bán hàng.
2. Nhập & đọc file Excel từ 2 chi nhánh (định kỳ).
3. Làm sạch: chuẩn hoá tên cột, đơn vị tiền, ngày tháng, mã sản phẩm khác nhau giữa các nguồn.
4. Lưu vào kho dữ liệu tập trung.
5. Dashboard với bộ lọc thời gian/chi nhánh/nhóm hàng + xuất báo cáo.
6. Lịch chạy tự động mỗi đêm + thông báo nếu có nguồn lỗi.

**Yêu cầu phi chức năng (NFR).**
- Pipeline đêm chạy xong trước 7:00 sáng.
- Có cơ chế báo lỗi khi 1 nguồn thiếu/sai định dạng (không âm thầm bỏ qua).
- Dashboard tải < 3s với dữ liệu 12 tháng.
- Số liệu phải **truy ngược được về nguồn** (đối soát).

**Nền tảng & công nghệ (yêu cầu).**
- **Pipeline/ETL:** Python (Pandas) hoặc công cụ ETL; lập lịch bằng cron/Airflow.
- **Kho dữ liệu:** PostgreSQL (hoặc 1 data warehouse như BigQuery nếu sẵn).
- **Dashboard:** công cụ BI (Power BI / Metabase / Superset) **hoặc** web tự dựng (ReactJS + thư viện chart).
- **Đọc Excel:** thư viện Python (openpyxl/pandas).
- **Hạ tầng:** Docker + cloud, lưu log chạy pipeline.

**Team & thời gian.** 4 người (1 PM · 2 data engineer · 1 dev dashboard), 8 tuần.

**Ràng buộc & dữ liệu nhạy cảm.** Số liệu doanh thu = nhạy cảm nội bộ. **Quan trọng:** đây là dữ liệu lãnh đạo dùng để quyết định → **tuyệt đối không để AI/hệ thống "bịa" số hay nội suy che lỗi**; thiếu dữ liệu phải báo, không tự điền.

**🔎 Điểm cần PM làm rõ (cho EX-01).**
- Brief nói 3 nguồn "đã chuẩn hoá", nhưng 2 chi nhánh gửi Excel **mỗi nơi một mẫu** → việc làm sạch lớn hơn tưởng, PM phải nêu ra.
- "Cập nhật hằng ngày" — nếu 1 chi nhánh nộp file trễ thì dashboard hiển thị gì? Chưa rõ.

**🧑‍🏫 Gợi ý cho giảng viên.**
- Đây là đề tốt nhất để dạy **EX-05 (chống rubber-stamping & AI bịa số)**: yêu cầu PM gắn nguồn cho từng KPI, có cờ "dữ liệu thiếu".
- WBS dễ sót: bước làm sạch/đối chiếu mã sản phẩm giữa nguồn, xử lý nguồn lỗi, đối soát số tổng.
- Delegation Map: pipeline ghi vào kho dữ liệu điều hành → **A+ (≈L4)** có cổng đối soát; sinh truy vấn/biểu đồ nháp → **A (≈L3)**.
- **EX-01 Stakeholder simulation:** ví dụ: *"Sếp muốn dashboard realtime theo từng phút."* PM nên trả lời: realtime cần streaming infra, out-of-scope MVP 8 tuần — batch hằng ngày trước 7h sáng đã đủ cho quyết định lãnh đạo.
- **EX-03 Trade-off:** ETL + làm sạch 3 nguồn + dashboard + đối soát → 4 người × 8 tuần sát. PM nên cắt: bỏ tự build dashboard, dùng Metabase/Superset off-the-shelf.
- **EX-05 Hallucination:** đề "đinh" cho EX-05 — AI dễ bịa "doanh thu dự báo" hoặc nội suy số khi nguồn thiếu. PM phải buộc dashboard hiển thị "N/A — nguồn chưa nộp" thay vì để AI điền.

---

## PB-05 — App tích điểm khách hàng thân thiết

**Bối cảnh.** Chuỗi cà phê ~30 cửa hàng đang phát thẻ giấy tích điểm → khách mất thẻ, không biết điểm, khó làm khuyến mãi. Muốn **app tích điểm** để khách quét tích điểm và đổi quà.

**Mục tiêu kinh doanh.** Tăng khách quay lại, có kênh gửi khuyến mãi, nắm được dữ liệu mua lặp.

**Phạm vi MVP (8 tuần).**
- **In-scope:** đăng ký/đăng nhập · mã QR khách hàng · tích điểm khi mua (thu ngân quét QR) · xem số điểm & lịch sử · danh mục quà & đổi quà · gửi thông báo khuyến mãi · màn quản trị (cấu hình quy tắc tích điểm, duyệt quà, gửi thông báo).
- **Out-of-scope (MVP):** thanh toán trong app · đặt món/giao hàng · tích hợp ví điện tử · hạng thành viên phức tạp nhiều tầng.

**Người dùng & stakeholder.** Khách hàng (app) · Thu ngân (quét QR tích điểm) · Marketing (cấu hình & gửi khuyến mãi) · Quản lý chuỗi = duyệt nghiệm thu.

**Yêu cầu chức năng.**
1. Khách đăng ký bằng SĐT (OTP), nhận mã QR cá nhân.
2. Thu ngân quét QR → cộng điểm theo quy tắc (vd 1 điểm/10k).
3. Khách xem điểm, lịch sử tích/đổi.
4. Đổi điểm lấy quà trong danh mục (trừ điểm, sinh mã đổi).
5. Marketing tạo & gửi thông báo khuyến mãi (push) theo tệp khách.
6. Quản trị cấu hình quy tắc tích điểm & quản lý quà.

**Yêu cầu phi chức năng (NFR).**
- Chống gian lận tích điểm trùng (1 hoá đơn không quét cộng 2 lần).
- Quét & cộng điểm phản hồi < 1.5s tại quầy.
- Bảo vệ dữ liệu khách & lịch sử mua.
- Chạy ổn trên Android & iOS phổ thông.

**Nền tảng & công nghệ (yêu cầu).**
- **Mobile (khách):** Flutter hoặc React Native.
- **App/màn thu ngân:** app quét QR (cùng nền mobile) hoặc web tại quầy.
- **Backend:** Node.js (NestJS) hoặc Spring Boot.
- **CSDL:** PostgreSQL.
- **Push:** Firebase Cloud Messaging.
- **OTP/SMS:** dịch vụ SMS brandname.
- **Hạ tầng:** Docker + cloud, CI/CD.

**Team & thời gian.** 5 người (1 PM · 2 mobile · 1 backend · 1 QA), 8 tuần.

**Ràng buộc & dữ liệu nhạy cảm.** Dữ liệu khách + lịch sử mua = cá nhân. **Gửi push hàng loạt** và **cấu hình quy tắc điểm/đổi quà** = vùng nhạy cảm (sai là mất tiền/spam khách).

**🔎 Điểm cần PM làm rõ (cho EX-01).**
- "Tích điểm khi mua" — quét theo hoá đơn hay theo số tiền nhập tay? Nếu nhập tay thì chống gian lận thế nào? Brief chưa rõ.
- Điểm có **hết hạn** không? Ảnh hưởng nghiệp vụ & dữ liệu.

**🧑‍🏫 Gợi ý cho giảng viên.**
- WBS dễ sót: chống tích trùng, app/màn thu ngân, cấu hình quy tắc điểm, kiểm thử quét QR thực tế.
- Delegation Map: gửi push hàng loạt, đổi quà (trừ điểm), cấu hình quy tắc → **A+ (≈L4)**, người duyệt; sinh UI/nội dung thông báo nháp → **A (≈L3)**.
- **EX-01 Stakeholder simulation:** ví dụ: *"Marketing muốn tích điểm theo combo (mua 2 tặng 1 → bonus point)."* PM nên trả lời: combo logic phức tạp, out-of-scope MVP — phase 1 chỉ cần 1 quy tắc đơn (X điểm / Y đồng).
- **EX-03 Trade-off:** 5 người × 8 tuần nhưng 2 app (khách + thu ngân) + backend + push + OTP → sát. PM nên cắt: bỏ tệp khách cho push (gửi all hoặc manual select), hoặc gộp màn thu ngân vào web thay vì app riêng.
- **EX-05 Hallucination:** AI hay bịa "tỷ lệ đổi quà" hoặc "tỷ lệ khách quay lại" khi chưa có data vận hành thực — PM phải bắt và ghi N/A.

---

## PB-06 — Tính năng AI tóm tắt & trích xuất hợp đồng *(sát chủ đề khoá học, cho nhóm core)*

**Bối cảnh.** Một sản phẩm SaaS quản lý hợp đồng đã có sẵn (lưu file hợp đồng, tìm kiếm cơ bản). Khách than phải đọc tay hợp đồng dài để tìm điều khoản. Đội muốn thêm **tính năng AI: tự tóm tắt hợp đồng + trích các trường quan trọng** (ngày hiệu lực, giá trị, các bên, ngày hết hạn, điều khoản phạt).

**Mục tiêu kinh doanh.** Giảm thời gian đọc hợp đồng, giúp khách tra nhanh điều khoản, tạo điểm khác biệt cho sản phẩm.

**Phạm vi MVP (8 tuần).**
- **In-scope:** upload/chọn hợp đồng PDF · AI sinh **bản tóm tắt** · AI **trích bảng các trường quan trọng** · người dùng **xem & sửa lại** kết quả AI (con người chốt) · đánh dấu trường AI "không chắc" để người kiểm · lưu kết quả gắn với hợp đồng.
- **Out-of-scope (MVP):** tự động ký · tự động nhắc gia hạn · phân tích pháp lý đưa lời khuyên · đa ngôn ngữ ngoài Việt/Anh.

**Người dùng & stakeholder.** Nhân viên pháp chế/kinh doanh (dùng tính năng) · Quản trị sản phẩm = duyệt nghiệm thu · (Đội kỹ thuật vận hành phần AI).

**Yêu cầu chức năng.**
1. Chọn 1 hợp đồng PDF đã có trong hệ thống → bấm "Phân tích bằng AI".
2. AI trả về: bản tóm tắt ngắn + bảng trường (các bên, ngày hiệu lực, ngày hết hạn, giá trị, điều khoản phạt…).
3. Mỗi trường hiển thị **độ tin cậy / trích từ đoạn nào** để người đối chiếu.
4. Người dùng **sửa/duyệt** trước khi lưu — kết quả AI **không tự động coi là đúng**.
5. Trường AI không tìm thấy/không chắc → đánh dấu rõ, **không bịa**.
6. Lưu kết quả đã duyệt, gắn vào hồ sơ hợp đồng.

**Yêu cầu phi chức năng (NFR).**
- Phân tích 1 hợp đồng ~20 trang < 30s.
- **Không gửi dữ liệu hợp đồng ra ngoài phạm vi cho phép**; nếu dùng API mô hình bên ngoài phải có thoả thuận xử lý dữ liệu.
- Kết quả AI luôn truy được về **đoạn gốc** trong hợp đồng (chống bịa).
- Có nhật ký: ai chạy, ai duyệt, sửa gì.

**Nền tảng & công nghệ (yêu cầu).**
- **AI:** gọi LLM qua API (vd Claude/OpenAI) **hoặc** mô hình self-host nếu yêu cầu bảo mật cao; kèm kỹ thuật trích dẫn nguồn (RAG/grounding) để mỗi trường có đoạn gốc.
- **Đọc PDF:** thư viện trích văn bản (pdfplumber / Apache PDFBox); OCR nếu PDF scan.
- **Backend:** Python (FastAPI) cho phần AI · tích hợp vào backend SaaS sẵn có (REST).
- **Frontend:** thêm màn hình vào web app hiện tại (ReactJS).
- **CSDL:** dùng DB sẵn của SaaS (PostgreSQL) + bảng lưu kết quả + nhật ký.
- **Hạ tầng:** Docker; quản lý khóa API & secret an toàn.

**Team & thời gian.** 4 người (1 PM · 1 AI engineer · 1 backend · 1 frontend), 8 tuần.

**Ràng buộc & dữ liệu nhạy cảm.** **Hợp đồng khách = dữ liệu rất nhạy cảm.** Đưa nội dung hợp đồng vào prompt/API ngoài là vùng rủi ro cao nhất của đề này → đụng thẳng **luật cứng Leash** (không đẩy dữ liệu nhạy cảm ra ngoài tuỳ tiện) và cần **cổng fail-closed** cho output AI.

**🔎 Điểm cần PM làm rõ (cho EX-01).**
- Brief kỳ vọng "AI trích xuất chính xác" — PM phải phản biện: AI **không chắc 100%**, nên thiết kế **người duyệt + đánh dấu độ tin cậy**, không hứa tuyệt đối.
- Có được phép gửi hợp đồng ra **API mô hình bên ngoài** không, hay bắt buộc self-host? Đây là quyết định ràng buộc tech stack & rủi ro — phải làm rõ trước khi WBS.

**🧑‍🏫 Gợi ý cho giảng viên (đề "đinh" của khoá).**
- Đề này buộc PM áp **đúng tinh thần CASAN/Leash**: con người giữ quyết định, AI là lực thực thi; output AI qua **cổng fail-closed** (truy được nguồn mới dùng); cảnh giác **rubber-stamping** (duyệt bừa kết quả AI).
- WBS dễ sót: bước đánh giá chất lượng trích xuất (evaluation), xử lý PDF scan/OCR, cơ chế hiển thị nguồn trích, kiểm thử bảo mật dữ liệu.
- Delegation Map (quan trọng nhất ở đề này):
  - Gửi hợp đồng cho mô hình ngoài, lưu kết quả vào hồ sơ chính thức → **A+ (≈L4)** + cổng bảo mật + người duyệt.
  - AI sinh bản tóm tắt nháp để người sửa → **A (≈L3)**.
  - **Tuyệt đối không** để AI tự "chốt" trường pháp lý mà không có người duyệt (đây là chỗ minh hoạ vì sao **L5 không được cấp**).
- **EX-01 Stakeholder simulation:** ví dụ: *"Khách muốn AI tự đánh giá rủi ro pháp lý — 'hợp đồng này an toàn không?'."* PM nên trả lời: tư vấn pháp lý = out-of-scope + trách nhiệm pháp lý nghiêm trọng → chỉ trích xuất, **không phán xử**.
- **EX-03 Trade-off:** AI engineer + backend + frontend + OCR + RAG → 4 người × 8 tuần sát. PM nên cắt: bỏ OCR (chỉ hỗ trợ PDF text, không scan) — giảm ~2 tuần effort.
- **EX-05 Hallucination:** đề "đinh" cho hallucination — AI sẽ bịa điều khoản phạt hoặc tự suy diễn ý nghĩa pháp lý từ đoạn mơ hồ. PM phải buộc: trường không tìm thấy → "Không tìm thấy — kiểm thủ công", **tuyệt đối không để AI điền suy đoán**.

---

## Gợi ý vận hành cho 300 PM

- **Chia nhóm theo đề:** mỗi đề ~50 PM; nhóm mới/ít kinh nghiệm → **PB-03** (dễ nhất); nhóm core → **PB-06** (sát chủ đề AI nhất).
- **Trộn để review đỡ nhàm:** 6 đề khác domain → khi showcase lớp không bị 300 bài giống hệt nhau, dễ so sánh phán xử PM.
- **Giữ nguyên 6 bài tập & rubric** trong Workbook — chỉ đổi case. PM thay tiền tố file theo mã đề (`REQ-PB01.md`, `WBS-PB01.md`, `RISK-PB01.md`, `DELEGATION-MAP-PB01.md`…).
- **Dắt tay từng bước:** phát kèm *Capstone Playbook* để nhóm biết trình tự làm việc trên đề (đề → spec → architecture → WBS → build → test → trace → viva), không chỉ có 6 drill lẻ.
- **Đề "common":** đây là bài toán phổ thông, không gắn chuẩn chuyên ngành. Nhóm có chuẩn riêng (vd lĩnh vực đặc thù) sẽ có bộ đề chuyên sâu riêng ngoài phạm vi training common.

---

**Thuật ngữ:** tra cứu đầy đủ + mapping sang ngành quốc tế tại `docs/GLOSSARY.md`.

---

## Phụ lục — Changelog

| Phiên bản | Ngày | Thay đổi |
|---|---|---|
| v1.0 | 2026-06-30 | Bộ 6 đề bài dự án mẫu (PB-01→PB-06) — requirement chi tiết + nền tảng công nghệ rõ, gắn EX-01→EX-06. |
| v2.0 | 2026-08-24 | Thêm gợi ý giảng viên cho EX-01 stakeholder simulation, EX-03 trade-off, EX-05 hallucination detection ở mỗi PB. Glossary pointer. Changelog chuyển về cuối. |

*PM AI Bootcamp v2.0 — Project Brief Bank · 2026-08-24 · Dùng kèm Workbook Common v2.0.*
