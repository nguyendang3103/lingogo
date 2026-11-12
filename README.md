# Lingogo

> 🌐 **Link học trực tuyến chính thức:** **[https://nguyendang3103.github.io/lingogo/](https://nguyendang3103.github.io/lingogo/)**
>
> *(Hỗ trợ đầy đủ âm thanh, nhận diện giọng nói chấm phát âm và tập viết chữ. Mở bằng Safari / Chrome trên điện thoại rồi chọn **"Thêm vào màn hình chính"** để dùng như App).*

---

App học Tiếng Anh (IELTS & Giao tiếp), Tiếng Trung (HSK) và Tiếng Nhật (JLPT) trong một giao diện hợp nhất: lộ trình theo chủ đề, ôn tập ngắt quãng (SRS), luyện phát âm chấm điểm AI, luyện viết chữ Hán / Kanji và luyện đề thi.

## Cấu trúc thư mục phân tách theo từng ngôn ngữ

Toàn bộ tài nguyên được phân loại độc lập theo từng ngôn ngữ, giúp dễ dàng sao chép, trích xuất hoặc tái sử dụng cho các ứng dụng chuyên biệt khác:

| Thư mục | Nội dung | Mục đích |
| --- | --- | --- |
| 🇬🇧 **`English/`** | Toàn bộ tài nguyên tiếng Anh: `data/` (bài học `en.json`, `ielts_30day_listening.*`), `audio/` (gói audio base64 `w*.json`, file nghe đọc `mail/en-*.mp3`), `notes/` (`English Practice.md`), `source/`, `tools/` | Gói độc lập cho app học Tiếng Anh / IELTS |
| 🇨🇳 **`Chinese/`** | Toàn bộ tài nguyên tiếng Trung: `data/` (bài học HSK 1–6 `zh.json`, nét chữ Hán `strokes-zh.json`), `audio/` (`zh-*.json`, `mail/zh-*.mp3`), `notes/` (`Chinese Practice.md`), `source/`, `tools/` | Gói độc lập cho app học Tiếng Trung HSK |
| 🇯🇵 **`Japanese/`** | Toàn bộ tài nguyên tiếng Nhật: `data/` (bài học N5–N1 `ja.json`, nét Kanji/Kana `strokes-ja.json`), `audio/` (`ja-*.json`, `mail/ja-*.mp3`), `notes/` (`Japanese Practice.md`), `source/`, `tools/`, `vendor/` | Gói độc lập cho app học Tiếng Nhật JLPT |
| 🌐 **`index.html`** | Ứng dụng web SPA Lingogo đa ngôn ngữ chính (GitHub Pages / PWA). | Hub tích hợp cả 3 ngôn ngữ |
| 🛠️ **`tools/`** | Các công cụ tiện ích dùng chung (build, inline, migrate, kiểm tra lỗi). | Tiện ích hỗ trợ |
| 📝 **`notes/`** | `Lịch học 3 ngôn ngữ.md` và các ghi chú tổng hợp. | Kế hoạch học tập |

## Chạy thử trên máy tính (Local)

```bash
python -m http.server 8000
```
Mở trình duyệt tại http://localhost:8000.

## Đồng bộ tiến độ đám mây qua GitHub (Gist Sync)
App hỗ trợ đồng bộ tự động 2 chiều giữa nhiều thiết bị (PC, điện thoại, tablet) qua GitHub Gist cá nhân:
- Bấm biểu tượng **🔄 Đồng bộ** trên app.
- Nhập **GitHub Personal Access Token** (chỉ cần quyền `gist`).
- Tiến độ bài học, điểm XP, chuỗi ngày streak và danh sách SRS sẽ tự động lưu và đồng bộ ngầm mỗi khi bạn học.
