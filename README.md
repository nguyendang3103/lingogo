# Lingogo

App học tiếng Anh thương mại, tiếng Trung và tiếng Nhật trong một chỗ: lộ trình theo chủ đề, ôn tập ngắt quãng (SRS), luyện nói và tập viết chữ Hán, kana.

- **Bản chạy trực tiếp (GitHub Pages):** https://nguyendang3103.github.io/lingogo/
- **Bản Claude Artifact:** https://claude.ai/artifact/M4569cod66nCfxNbu3YGR6
- **Kho tri thức & ghi chú học tập:** Được theo dõi trong bộ não thứ hai (kho `sallysbrain`, thư mục `wiki/learn/Lingogo/notes/`).

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

## Đóng gói cho Claude Artifact / iPad (tránh lỗi 403 CORS)

```bash
python tools/inline.py index-inline.html
```
File `index-inline.html` tạo ra có nhúng sẵn dữ liệu, dùng để dán hoặc publish vào Claude Artifact.
