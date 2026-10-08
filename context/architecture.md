# Architecture Context

> File điều hướng cho agent. Kiến trúc là **đề xuất** của Technical HLD v1.3; chưa có code, benchmark hay capacity đã xác nhận.

| Chủ đề | Nguồn |
|---|---|
| 12 quyết định kiến trúc | `docs/product/technical-hld-v1.3.md` §1 |
| Sơ đồ logic client/server | `docs/product/technical-hld-v1.3.md` §3 |
| Giọng nói, từ gọi, thẻ lệnh, TTS | `docs/product/technical-hld-v1.3.md` §4 |
| Pipeline client (chụp đề, attempt, phiếu, ảnh gần trực tiếp, lifecycle) và ẩn danh hóa | `docs/product/technical-hld-v1.3.md` §5, §5.7 |
| Model portfolio, adapter, chính sách chọn model | `docs/product/technical-hld-v1.3.md` §6 |
| API, metadata attempt, idempotency | `docs/product/technical-hld-v1.3.md` §7 |
| Backend: scope gate, evidence gate, ValidatorRegistry, tutor, tiến độ, data store, rà soát shadow teacher | `docs/product/technical-hld-v1.3.md` §8 |
| Stack và deployment pilot | `docs/product/technical-hld-v1.3.md` §9 |
| NFR, privacy, observability | `docs/product/technical-hld-v1.3.md` §11 |
| State machine, acceptance A01–A46 | `docs/product/technical-hld-v1.3.md` §15 |
| Ràng buộc nhà cung cấp AI | `CLAUDE_AI_Tutor.md` §10 |
| Delivery / CI/CD / quality gates | `CLAUDE.md`, `AGENTS.md`, `Jenkinsfile`, `scripts/` |

ADR sẽ được thêm dưới `docs/architecture/` khi có quyết định được duyệt. `docs/capstone/HLD-AITUTOR.md` đã SUPERSEDED.
