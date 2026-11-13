# Lingogo UI & Design Guidelines

## Quy tắc thiết kế giao diện (UI & Layout Preference)

- **Giao diện danh mục tiêu đề (Accordion / Collapsible Master-Detail)**:
  - Khi một tab hoặc màn hình có nhiều lựa chọn, nhiều chuyên đề, tài liệu, đề thi hoặc cẩm nang dài: **luôn thiết kế dạng danh mục tiêu đề gọn gàng trước**.
  - Mỗi mục hiển thị rõ: Icon đại diện + Tiêu đề chính + Subtitle tóm tắt 1 câu + Chip nhãn phân loại + Mũi tên chỉ thị trạng thái (`▾`/`▴`).
  - **Chỉ khi người dùng bấm vào tiêu đề bài/mục nào thì nội dung chi tiết mới mở bung ra** để đọc, bấm lại thì thu gọn.
  - Tránh hiển thị dàn trải toàn bộ nội dung dài cùng lúc trên một màn hình gây cuộn mỏi và khó theo dõi.
  - Hỗ trợ công cụ tiện ích (như `📖 Mở tất cả` / `📁 Thu gọn tất cả`) để người dùng linh hoạt khi muốn đọc toàn bộ.

## Quy tắc âm thanh bài học (Audio & Voice Guideline)

- **Luôn có audio giọng người thật đính kèm khi tạo chủ đề mới**:
  - Khi tạo chủ đề mới hoặc mở rộng bài học trong app (từ vựng, câu ví dụ, hội thoại, câu hỏi luyện nói Coach): **bắt buộc phải tạo gói audio chất lượng cao đính kèm** (bundle JSON trong thư mục `<Lang>/audio/w<id>.json` với key là SHA-1 12 ký tự của câu/từ).
  - Khai báo ánh xạ âm thanh tương ứng vào trường `d.audio[text] = [bundleId, sha1Key]` trong `<Lang>/data/<lang>.json`.
  - Không để bài học chỉ dựa vào giọng máy robot (SpeechSynthesis TTS) vì chất lượng giọng máy không tự nhiên và phụ thuộc thiết bị. Người học cần nghe giọng chuẩn tự nhiên, chuẩn bản xứ trong mọi bài học.
