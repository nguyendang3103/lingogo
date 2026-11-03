# Lingogo

> 🌐 **Link học trực tuyến chính thức:** **[https://nguyendang3103.github.io/lingogo/](https://nguyendang3103.github.io/lingogo/)**
>
> *(Hỗ trợ đầy đủ âm thanh, nhận diện giọng nói chấm phát âm và tập viết chữ. Mở bằng Safari / Chrome trên điện thoại rồi chọn **"Thêm vào màn hình chính"** để dùng như App).*

---

App học tiếng Anh thương mại, tiếng Trung và tiếng Nhật trong một chỗ: lộ trình theo chủ đề, ôn tập ngắt quãng (SRS), luyện nói và tập viết chữ Hán, kana.

- **Link chạy trực tiếp:** https://nguyendang3103.github.io/lingogo/
- **Kho tri thức & ghi chú học tập:** Nằm trong thư mục `notes/` (`English Practice.md`, `Chinese Practice.md`, `Japanese Practice.md`).

## Cấu trúc thư mục

| Đường dẫn | Là gì |
| --- | --- |
| `index.html` | App web SPA chạy độc lập cho GitHub Pages và trình duyệt di động (PWA). |
| `data/` | Dữ liệu bài học: `en.json` (32 chủ đề tiếng Anh), `zh.json` (45 chủ đề tiếng Trung), `ja.json` (16 bài tiếng Nhật N5), `strokes-*.json` (nét vẽ). |
| `audio/` | Các gói âm thanh MP3 mã hóa base64 theo chủ đề. |
| `tools/` | Các công cụ xử lý dữ liệu: `inline.py` (nhúng data vào HTML cho Claude/iPad), `add_hanviet.py`, `add_fill_pinyin.py`, `add_n5_extras.py`, `build.py`, `gen_ja_audio.py`. |
| `source/` | Dữ liệu nguồn và bản xuất trung gian phục vụ các script trong `tools/`. |
| `vendor/` | Dữ liệu nét chữ animCJK gốc. |

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

## Đóng gói cho Claude Artifact / iPad (tránh lỗi 403 CORS)

```bash
python tools/inline.py index-inline.html
```
File `index-inline.html` tạo ra có nhúng sẵn dữ liệu, dùng để dán hoặc publish vào Claude Artifact.
