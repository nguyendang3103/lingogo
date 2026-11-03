# NóiĐược – Đặc tả sản phẩm & kỹ thuật MVP

Oct 28, 2026 · @Nguyen Dang

## 1. Tóm tắt điều hành

**NóiĐược** là ứng dụng web (PWA) giúp người Việt học ngoại ngữ để *nói được trong tình huống thật*, bắt đầu với tiếng Anh A1–B2, kiến trúc sẵn cho Nhật, Hàn, Trung, Pháp, Đức, Tây Ban Nha.

- **Khác biệt:** mỗi đơn vị bài là một tình huống đời thực có mục tiêu “làm được” rõ ràng; mỗi bài đều có nghe và nói (TTS/STT miễn phí của trình duyệt); từ vựng tự vào hàng ôn tập SRS; gia sư AI nhập vai đúng tình huống vừa học, sửa lỗi bằng tiếng Việt.
- **MVP (đã dựng và chạy thử, 14/14 bài kiểm thử đạt):** đăng ký/đăng nhập, bài xếp lớp 12 câu, 1 chủ đề hoàn chỉnh (“Ở quán cà phê”, 3 bài, 25 mục từ, 6 dạng bài), flashcard SM-2, streak – XP – thành tích, trang tiến độ, gia sư AI có giới hạn lượt, xuất/xóa dữ liệu.
- **Thời gian (ước tính):** 4–6 tuần cho 1 kỹ sư full-stack + 1 giáo viên bán thời gian để mở rộng từ mã hiện có lên 8–10 chủ đề A1–A2 và chạy thử với 50–100 người.
- **Chi phí vận hành giai đoạn thử (ước tính):** hạ tầng ở mức một máy chủ nhỏ; chi phí lớn nhất là API AI, được chặn bằng giới hạn lượt/ngày. Giá cụ thể **cần xác minh** tại thời điểm triển khai (mục 9, 13).

## 2. Giả định và phạm vi

Không có thông tin đầu vào cụ thể nên tài liệu dùng các giả định dưới đây; đổi bất kỳ dòng nào thì các mục liên quan cần điều chỉnh theo.

| Hạng mục | Giả định | Ảnh hưởng nếu khác |
| --- | --- | --- |
| Người học | Người Việt 18–35 tuổi, đi làm hoặc sinh viên, trình độ A1–A2, học trên điện thoại | Dưới 16 tuổi → cần quy trình đồng ý của phụ huynh (V2) |
| Mục tiêu học | Giao tiếp, du lịch, công việc; thi chứng chỉ là nhu cầu phụ | Ưu tiên thi → thêm ngân hàng đề và chấm theo khung bài thi |
| Ngôn ngữ MVP | Tiếng Anh; tiếng Nhật chỉ là bản minh họa dữ liệu | Ngôn ngữ khác → viết nội dung mới, mã giữ nguyên |
| Nền tảng | PWA chạy trên trình duyệt di động và máy tính | App gốc → bọc PWA (Capacitor) hoặc viết lại giao diện React Native |
| Đội ngũ | 1 kỹ sư full-stack + 1 giáo viên bán thời gian + người bản ngữ rà soát theo đợt | Không có giáo viên → chậm và rủi ro chất lượng nội dung cao |
| Ngân sách | Tự bỏ vốn, ưu tiên công cụ miễn phí và mã nguồn mở | Có vốn → thêm TTS/chấm phát âm trả phí sớm hơn |
| Mô hình kinh doanh | Freemium: học miễn phí, trả phí cho gia sư AI không giới hạn | Miễn phí hoàn toàn → cần nhà tài trợ hoặc B2B |
| Công nghệ | Node.js 22 thuần, SQLite, SPA JavaScript không cần build | Đội quen Next.js/React → chuyển frontend, giữ API |

**Trong phạm vi tài liệu:** đặc tả sản phẩm, phương pháp học, thiết kế kỹ thuật, mã MVP chạy được, kế hoạch đo lường và lộ trình 12 tháng.

**Ngoài phạm vi:** app trên kho ứng dụng, thanh toán thật, nội dung đầy đủ A1–B2, chấm phát âm theo âm vị, cộng đồng/bảng xếp hạng.

## 3. Định vị sản phẩm

**Tên:** NóiĐược. **Tagline:** “Học để nói được — mỗi ngày một tình huống thật.” (Cần kiểm tra trùng tên miền, nhãn hiệu tại Cục Sở hữu trí tuệ trước khi dùng chính thức.)

**Vấn đề:** nhiều người Việt học ngữ pháp và từ vựng nhiều năm nhưng vẫn ngại mở lời; ứng dụng phổ biến dạy theo từ rời rạc, ít luyện nói, và giải thích ngữ pháp không theo góc nhìn người Việt (ví dụ trật tự tính từ – danh từ ngược nhau).

**Giá trị khác biệt (giả thuyết cần kiểm chứng):**

1. **Tình huống trước, từ vựng sau:** mỗi đơn vị bài có câu “Sau bài này bạn có thể…”, mọi từ và câu đều phục vụ tình huống đó.
2. **Nói trong mọi bài:** bài nói theo mẫu ở cuối mỗi bài học, không phải tính năng riêng.
3. **Ôn đúng lúc:** từ của bài vừa học tự vào hàng SRS; trang chủ ưu tiên ôn tập khi có thẻ đến hạn.
4. **Gia sư AI nhập vai đúng tình huống vừa học,** giữ đúng trình độ CEFR, sửa một lỗi mỗi lượt bằng tiếng Việt.
5. **Giải thích theo lỗi điển hình của người Việt** (âm cuối, trật tự từ, mạo từ, thì).

### Persona

| Persona | Bối cảnh | Mục tiêu | Rào cản | NóiĐược đáp ứng |
| --- | --- | --- | --- | --- |
| **Lan, 26, nhân viên văn phòng TP.HCM** | Học tiếng Anh từ phổ thông, đọc ổn, nói ngại | Họp với đối tác, đi du lịch tự túc | Ít thời gian, sợ nói sai | Bài 8–10 phút, luyện nói riêng tư với AI |
| **Minh, 20, sinh viên** | Chuẩn bị du học hoặc thi chứng chỉ | Tự tin giao tiếp hằng ngày ở nước ngoài | Học theo đề, thiếu phản xạ | Tình huống sinh hoạt, hội thoại nhập vai |
| **Hoa, 32, chuẩn bị làm việc tại Nhật** | Mới bắt đầu tiếng Nhật | N5–N4, chào hỏi và công việc | Chữ viết mới, kính ngữ | Romaji, ghi chú mức lịch sự, lộ trình JLPT (khi mở khóa tiếng Nhật) |

### Phân tích đối thủ

Nhận định dưới đây ở mức định tính, dựa trên hiểu biết chung về sản phẩm; **mọi số liệu người dùng, doanh thu, giá gói đều chưa xác minh** và cần tra cứu từ nguồn chính thức trước khi trích dẫn.

| Ứng dụng | Điểm mạnh nên học | Khoảng trống NóiĐược nhắm vào |
| --- | --- | --- |
| Duolingo | Thói quen hằng ngày, bài ngắn, trò chơi hóa | Câu thiếu ngữ cảnh đời thực; luyện nói còn hạn chế |
| Babbel | Bài theo hội thoại thực tế, giải thích ngữ pháp | Ít nội dung giải thích bằng tiếng Việt |
| Memrise | Video người bản ngữ, từ vựng theo ngữ cảnh | Ít lộ trình ngữ pháp có cấu trúc |
| Anki | SRS mạnh, tùy biến cao | Không có bài học; người mới khó tự làm thẻ |
| Busuu | Bài theo CEFR, góp ý cộng đồng | Phản hồi phụ thuộc người dùng khác, có độ trễ |
| Elsa Speak | Chấm phát âm chi tiết | Tập trung phát âm, ít lộ trình giao tiếp đầy đủ |

### Chỉ số thành công

Mục tiêu dưới đây là **khuyến nghị chủ quan** cho giai đoạn thử 50–100 người, không phải chuẩn ngành; điều chỉnh sau 4 tuần dữ liệu đầu.

| Chỉ số | Định nghĩa | Mục tiêu thử nghiệm |
| --- | --- | --- |
| D1 / D7 / D30 retention | % người quay lại học vào ngày 1, 7, 30 sau đăng ký | ≥ 40% / ≥ 20% / ≥ 10% |
| Hoàn thành onboarding | % đăng ký học xong bài đầu tiên | ≥ 60% |
| Streak trung vị | Chuỗi ngày học trung vị của người hoạt động | ≥ 4 ngày |
| Từ thuộc / tuần | Thẻ đạt khoảng ôn ≥ 21 ngày | Theo dõi xu hướng từ tuần 4 |
| Tỉ lệ nhớ khi ôn | % lượt ôn chọn Nhớ/Dễ | 80–90% (thấp hơn → thuật toán hoặc bài quá khó) |
| Phút học / ngày | Thời gian học trung bình ngày có hoạt động | 8–15 phút |
| Lượt nói / bài | Bài nói được chấm tự động thay vì tự đánh giá | ≥ 70% trên Chrome/Edge |

## 4. Phương pháp và nội dung học

Mỗi tính năng gắn với một cơ chế học có cơ sở nghiên cứu: **truy hồi chủ động** (trả lời trước khi xem đáp án), **lặp lại ngắt quãng** (ôn đúng lúc sắp quên), **học qua ngữ cảnh** (từ nằm trong câu và tình huống), **phản hồi tức thì** (biết đúng sai và lý do ngay), **đầu ra có hướng dẫn** (nói và viết theo mẫu trước khi tự do).

### Lộ trình tiếng Anh theo CEFR

Mỗi cấp khoảng 8–10 đơn vị tình huống, mỗi đơn vị 3–4 bài. Dưới đây là khung đề xuất; chỉ đơn vị “Ở quán cà phê” đã có nội dung trong MVP.

| Cấp | Đơn vị tình huống tiêu biểu | Ngữ pháp trọng tâm | “Làm được” cuối cấp |
| --- | --- | --- | --- |
| A1 | Chào hỏi, giới thiệu bản thân, **quán cà phê** (có sẵn), mua sắm, hỏi đường, giờ giấc | to be, hiện tại đơn, can/would like, số đếm, giá tiền | Gọi món, hỏi giá, giới thiệu bản thân bằng câu ngắn |
| A2 | Khách sạn, sân bay, khám bệnh, hẹn gặp, kể cuối tuần, gọi điện | quá khứ đơn, tương lai gần, so sánh, giới từ thời gian | Xử lý tình huống du lịch, kể sự việc đã qua |
| B1 | Phỏng vấn xin việc, họp nhóm, phàn nàn dịch vụ, email công việc | hiện tại hoàn thành, câu điều kiện 1–2, bị động, mệnh đề quan hệ | Trình bày ý kiến, giải quyết vấn đề thường gặp |
| B2 | Thuyết trình, đàm phán, thảo luận tin tức, viết báo cáo | điều kiện 3, wish, đảo ngữ, câu gián tiếp | Lập luận, thuyết phục, viết văn bản trang trọng |

Ngôn ngữ khác dùng khung tương ứng (JLPT N5–N3, TOPIK 1–3, HSK 1–4) qua cột `level_framework` của bảng `languages`; mã không cần sửa.

### Dạng bài

| Dạng bài | Kỹ năng | Cơ chế học | Trạng thái |
| --- | --- | --- | --- |
| Thẻ giới thiệu từ (nghe, đọc to, ví dụ) | Từ vựng, phát âm | Mã hóa kép âm + nghĩa + ngữ cảnh | MVP |
| Trắc nghiệm nghĩa | Từ vựng | Truy hồi có gợi ý | MVP |
| Nghe chọn đáp án | Nghe | Nhận diện âm | MVP |
| Đọc hội thoại ngắn rồi trả lời | Đọc hiểu | Hiểu trong ngữ cảnh | MVP |
| Điền từ vào câu | Từ vựng, ngữ pháp | Truy hồi không gợi ý | MVP |
| Sắp xếp câu | Ngữ pháp, trật tự từ | Xây câu, đối chiếu tiếng Việt | MVP |
| Nghe chép chính tả | Nghe, chính tả | Phân đoạn âm thanh | MVP |
| Nói theo mẫu (chấm qua nhận dạng giọng nói) | Nói | Đầu ra có hướng dẫn | MVP |
| Hội thoại nhập vai với AI | Nói, viết, phản xạ | Đầu ra tự do + sửa lỗi | MVP (tùy chọn bật) |
| Thẻ đảo chiều (nghĩa → từ) | Từ vựng | Truy hồi chủ động khó hơn | V1 |
| Viết đoạn ngắn có AI chấm | Viết | Phản hồi chi tiết | V1 |
| Chấm phát âm theo âm vị | Phát âm | Phản hồi tinh | V2 |
| Tập viết chữ (Kana, Hangul, Hán tự) theo thứ tự nét | Chữ viết | Ghi nhớ vận động | V2 |

### Thuật toán lặp lại ngắt quãng

MVP dùng **SM-2** (thuật toán SuperMemo 2) rút gọn thành 4 nút: Quên, Khó, Nhớ, Dễ. Lý do chọn SM-2 thay vì FSRS: đơn giản, dễ kiểm thử, đủ tốt khi chưa có dữ liệu ôn tập. FSRS (thư viện mã nguồn mở `ts-fsrs`) là bước nâng cấp ở V1 khi có vài nghìn lượt ôn để huấn luyện tham số.

Độ dễ cập nhật theo công thức SM-2, với q = 3 (Khó), 4 (Nhớ), 5 (Dễ), chặn dưới 1,3:

```latex
EF' = EF + \left(0.1 - (5 - q)\,(0.08 + (5 - q) \cdot 0.02)\right)
```

| Lượt nhớ thành công | Khó | Nhớ | Dễ |
| --- | --- | --- | --- |
| Lần 1 | 1 ngày | 1 ngày | 4 ngày |
| Lần 2 | 3 ngày | 6 ngày | 8 ngày |
| Từ lần 3 | khoảng cũ × 1,2 | khoảng cũ × EF | khoảng cũ × EF × 1,3 |

Quy tắc bổ sung: **Quên** → học lại sau 10 phút, EF giảm 0,2, đếm một lần quên; khoảng ôn tối đa 365 ngày; thẻ có khoảng ≥ 21 ngày tính là “đã thuộc”. Thẻ bị quên được đưa lại cuối phiên để học lại ngay.

### Bài kiểm tra xếp lớp

12 câu, 3 câu mỗi cấp A1–B2. Đạt một cấp khi đúng ≥ 2/3; trình độ là cấp cao nhất đạt **liên tục** từ thấp lên (trượt A2 thì dừng ở A1 dù may mắn đúng câu B1). Đơn vị dưới trình độ được mở sẵn để người học tự ôn. V1 chuyển sang xếp lớp thích ứng (câu sau phụ thuộc câu trước) và thêm câu nghe.

### Nhắc học

- MVP: trang chủ hiển thị số thẻ đến hạn và nút ôn tập ưu tiên; chuỗi ngày chỉ mất khi bỏ trọn một ngày theo múi giờ người dùng.
- V1: thông báo đẩy Web Push vào giờ người dùng tự chọn, tối đa 1 lần/ngày, không gửi khi đã học hôm đó; email tóm tắt tuần (có nút hủy). Hỗ trợ Web Push trên iOS cần xác minh theo phiên bản hiện hành.

### Bài học mẫu (8–10 phút)

1. **Khởi động (1 phút):** 1 câu trắc nghiệm ôn từ của bài trước.
2. **Học mới (2 phút):** danh sách từ của bài có nút nghe; 2–3 thẻ giới thiệu từ trọng tâm, có ví dụ và ghi chú lỗi người Việt.
3. **Luyện tập (3–4 phút):** trắc nghiệm, nghe chọn, điền từ, sắp xếp câu, đọc hội thoại; mỗi câu có phản hồi và giải thích ngay.
4. **Nghe – nói (2 phút):** chép chính tả một câu; nói to một câu mẫu, máy chấm theo tỉ lệ từ khớp.
5. **Ôn lại (1 phút):** các câu sai được đưa lại cuối bài một lần (không tính điểm lại).
6. **Tổng kết:** số câu đúng, XP, số từ mới vào hàng ôn tập, chuỗi ngày.

### Quy trình tạo và kiểm duyệt nội dung

1. **Giáo viên viết khung đơn vị:** tình huống, mục tiêu “làm được”, danh sách từ và cấu trúc theo cấp (tham chiếu danh mục từ vựng theo CEFR có giấy phép phù hợp).
2. **AI soạn nháp** ví dụ, câu bài tập, phương án nhiễu theo khung, với prompt yêu cầu đúng cấp và tránh chủ đề nhạy cảm; trạng thái `draft`.
3. **Kiểm tra tự động:** độ dài câu theo cấp, từ ngoài danh mục cấp, đáp án trùng phương án nhiễu, trùng lặp, từ cấm.
4. **Giáo viên Việt rà soát:** đúng trình độ, giải thích tiếng Việt chính xác, phù hợp văn hóa; trạng thái `in_review`.
5. **Người bản ngữ rà soát:** tự nhiên, đúng ngữ dụng, ghi `reviewed_by`.
6. **Phát hành** (`published`) rồi theo dõi tỉ lệ sai từng câu; câu sai > 60% hoặc bị báo lỗi → quay lại bước 4.

Máy chủ chỉ hiển thị bài `published`, nên nội dung AI chưa duyệt không thể tới tay người học.

## 5. Đặc tả tính năng và trải nghiệm

MVP chỉ giữ những gì cần để kiểm chứng giả thuyết cốt lõi: *người học quay lại đều đặn khi mỗi bài là một tình huống thật có luyện nói và từ vựng được ôn đúng lúc.*

| Nhóm | MVP (đã có trong mã) | V1 (sau 100+ người dùng) | V2 (mở rộng) |
| --- | --- | --- | --- |
| Tài khoản | Email + mật khẩu, xác nhận ≥ 16 tuổi, xuất/xóa dữ liệu | Đăng nhập Google, quên mật khẩu qua email | Tài khoản phụ huynh – con, SSO cho doanh nghiệp |
| Xếp lớp | 12 câu theo cấp, mở sẵn đơn vị thấp hơn | Thích ứng, thêm câu nghe | Xếp lớp theo kỹ năng riêng |
| Bài học | 6 dạng bài, phản hồi tức thì, ôn câu sai cuối bài | Thẻ đảo chiều, viết có AI chấm, 8–10 đơn vị A1–A2 | Video tình huống, B1–B2 đầy đủ |
| Ôn tập | SM-2, 4 mức, học lại ngay khi quên | FSRS, ôn ngoại tuyến rồi đồng bộ | Ôn theo kỹ năng (nghe, nói) |
| Nghe – nói | TTS và nhận dạng giọng nói của trình duyệt, chế độ tự đánh giá | Âm thanh thu sẵn của người bản ngữ | Chấm phát âm theo âm vị |
| Gia sư AI | 2 tình huống nhập vai, sửa 1 lỗi/lượt, giới hạn lượt/ngày | Tình huống theo từng đơn vị, nói bằng giọng | Giải thích ngữ pháp theo yêu cầu, tóm tắt lỗi tuần |
| Động lực | Streak, XP, mục tiêu ngày, 7 thành tích | Nhắc học Web Push, “ngày nghỉ” giữ chuỗi | Bạn học, giải đấu tuần tùy chọn tham gia |
| Tiến độ | Streak, XP 7 ngày, từ đang học/đã thuộc, độ chính xác, tỉ lệ nhớ | Báo cáo theo kỹ năng | Ước tính trình độ CEFR theo thời gian |
| Ngôn ngữ | Tiếng Anh; tiếng Nhật bản minh họa | Tiếng Nhật hoặc Hàn đầy đủ N5/TOPIK 1 | Trung, Pháp, Đức, Tây Ban Nha |
| Nền tảng | PWA cài được, vỏ ứng dụng chạy ngoại tuyến, sáng/tối | Gói ngoại tuyến cho bài đã tải | App kho ứng dụng (bọc PWA) |
| Kinh doanh | Miễn phí | Gói trả phí cho AI không giới hạn | Gói trường học, doanh nghiệp |

### Luồng người dùng chính

1. **Onboarding:** đăng ký (tên, email, mật khẩu, xác nhận tuổi) → chọn khóa → chọn mục đích học → chọn mục tiêu ngày (10/20/30/50 XP ≈ 5/10/15/25 phút).
2. **Xếp lớp:** “Làm bài xếp lớp (3 phút)” → 12 câu → trình độ gợi ý; hoặc “Tôi mới bắt đầu” → cấp đầu tiên.
3. **Học bài:** trang chủ → “Học bài tiếp theo” → danh sách từ mới → các bước bài tập → tổng kết (XP, từ vào hàng ôn, streak, thành tích).
4. **Ôn tập:** trang chủ hiện “Ôn N thẻ ngay” (ưu tiên trên bài mới) → thẻ mặt trước → tự nhớ → “Hiện nghĩa” → chọn Quên/Khó/Nhớ/Dễ → hết phiên.
5. **Hội thoại AI:** tab Gia sư AI → chọn tình huống → gõ hoặc nói → nhận câu trả lời nhập vai + thẻ góp ý sửa lỗi → hết lượt ngày thì báo hẹn mai.
6. **Tiến độ:** tab Tiến độ → chuỗi, XP 7 ngày, số từ, độ chính xác, thành tích.
7. **Nhắc học (V1):** thông báo đúng giờ đã chọn → mở thẳng phiên ôn tập.

### Gamification có chủ đích

- **Streak** thưởng sự đều đặn, không thưởng thời lượng; mất chuỗi không có thông báo gây áp lực, không bán “cứu chuỗi”. V1 cho 1–2 ngày nghỉ miễn phí mỗi tuần.
- **XP** gắn với học thật: bài mới 10 XP + 1/câu đúng + 5 nếu đúng hết; học lại một bài chỉ nhận nửa XP; mỗi lượt ôn 1 XP.
- **Mục tiêu ngày** do người học tự chọn, hiển thị “đã đạt” rồi thôi – không đẩy học quá.
- **Thành tích** đánh dấu cột mốc học (bài đầu, 25 từ, 100 lượt ôn, lần đầu nói với AI), không phải phần thưởng ngẫu nhiên.
- **Bảng xếp hạng** chỉ ở V2, tự chọn tham gia, so theo nhóm cùng trình độ.
- Không vòng quay may mắn, không đồng tiền ảo, không đếm ngược tạo khan hiếm.

### Wireframe văn bản các màn hình chính

```text
[Trang chủ]
Chào Lan!                                  [⚙]
Tiếng Anh giao tiếp · A1
[🔥 3 ngày liên tiếp] [14 XP hôm nay] [11 thẻ cần ôn]
Còn 6 XP để đạt mục tiêu          14/20 XP
[=========-----]
[    Ôn 11 thẻ ngay     ]   (nút nổi bật khi có thẻ đến hạn)
[  Học bài tiếp theo    ]
Lộ trình
┌ Ở quán cà phê                         A1 ┐
│ Mục tiêu: Gọi đồ uống, chọn cỡ, ...      │
│ ✓ Đồ uống và kích cỡ   8 phút · 82%      │
│ ▶ Gọi đồ uống lịch sự  10 phút (viền đậm)│
│ 🔒 Hỏi giá và thanh toán                  │
└──────────────────────────────────────────┘
[Học] [Ôn tập] [Gia sư AI] [Tiến độ]
```

```text
[Bài tập – sắp xếp câu]
[✕] [======-------]  (thanh tiến độ bài)
Cho tôi một ly trà cỡ lớn.
Chạm vào từ để xếp câu
( a ) ( large ) ( ____ )            ← câu đang xếp
- - - - - - - - - - - - - - -
( tea, ) ( please. )                 ← ngân hàng từ
┌ Chưa đúng ─────────────────────┐
│ Đáp án: a large tea please      │
│ 💡 Tính từ chỉ cỡ đứng TRƯỚC     │
│    danh từ, ngược tiếng Việt.    │
│ [🔊 Nghe]                       │
└─────────────────────────────────┘
[          Tiếp tục          ]
```

```text
[Ôn tập flashcard]
Ôn tập                         Còn 11 thẻ
┌──────────────────────────────┐
│ Bạn có nhớ nghĩa từ này?      │
│          coffee              │
│         [🔊 Nghe]             │
│  (sau khi lật) /ˈkɔːfi/       │
│  cà phê                       │
│  “A coffee with milk, please.”│
└──────────────────────────────┘
[ Hiện nghĩa ]  →  [Quên 10 phút] [Khó] [Nhớ] [Dễ]
```

```text
[Gia sư AI – Gọi đồ uống ở quán cà phê]
Còn 18 lượt hôm nay · AI có thể sai
(AI) Hi there! What can I get for you today? [🔊]
                         (Bạn) I want coffee
┌ I want coffee → Can I have a coffee, please? ┐
│ Dùng “Can I have…” để lịch sự hơn.            │
└───────────────────────────────────────────────┘
(AI) Sure! Small, medium or large? [🔊]
[ Nhập bằng tiếng Anh…     ] [🎙] [Gửi]
```

Các màn còn lại (đăng nhập/đăng ký, onboarding 4 bước, xếp lớp, tổng kết bài, tiến độ, cài đặt) đã được dựng trong mã MVP theo cùng bố cục: một cột, nút chính rộng toàn màn hình ở cuối, thanh tab dưới.

### Nguyên tắc UI/UX, truy cập, chế độ tối, ngoại tuyến

- **Một việc mỗi màn hình,** nút chính luôn ở vị trí ngón cái; vùng chạm ≥ 48 px.
- **Phản hồi bằng chữ và màu,** không chỉ bằng màu (người mù màu vẫn đọc được “Chính xác!/Chưa đúng”).
- **Truy cập:** HTML ngữ nghĩa, nhãn cho mọi ô nhập, `aria-live` cho phản hồi và tiến độ, viền focus rõ, liên kết “Bỏ qua đến nội dung”, thuộc tính `lang` đúng cho chữ ngoại ngữ để trình đọc màn hình phát âm đúng, tôn trọng `prefers-reduced-motion`.
- **Chế độ tối:** theo hệ thống mặc định, người dùng chọn Sáng/Tối/Theo hệ thống trong Cài đặt; màu dùng biến CSS nên cả hai chế độ đều đạt độ tương phản.
- **Ngoại tuyến:** service worker lưu vỏ ứng dụng; mất mạng thì hiện thanh thông báo, dữ liệu học cần mạng. V1 lưu bài đã tải và hàng đợi lượt ôn trong IndexedDB rồi đồng bộ khi có mạng.

## 6. Thiết kế kỹ thuật

MVP là một máy chủ Node.js duy nhất phục vụ cả API JSON và PWA tĩnh, lưu dữ liệu trong một tệp SQLite; dịch vụ ngoài duy nhất là API mô hình ngôn ngữ cho gia sư AI, và nó có thể tắt.

&#91;embedded content: Kiến trúc MVP · trình duyệt, máy chủ, dữ liệu, AI\]

Mọi logic chấm điểm, SRS và giới hạn AI chạy ở máy chủ; trình duyệt chỉ hiển thị, phát âm và nhận dạng giọng nói.

### Lựa chọn công nghệ

| Thành phần | MVP chọn | Lý do | Khi nào đổi |
| --- | --- | --- | --- |
| Máy chủ | Node.js ≥ 22.5, `node:http`, không framework | Không phụ thuộc gói ngoài, dễ đọc, dễ chạy cho người không chuyên | Nhiều route hơn → Fastify/Express hoặc Next.js API |
| CSDL | SQLite qua `node:sqlite` (có sẵn trong Node) | Không cần máy chủ CSDL, sao lưu bằng một tệp | > 1 máy chủ hoặc ghi đồng thời lớn → PostgreSQL |
| Frontend | SPA JavaScript thuần (ES modules), PWA | Không bước build, tải nhanh trên mạng di động | Giao diện phức tạp hơn → React/Next.js; app gốc → React Native |
| Nghe | Web Speech API `speechSynthesis` | Miễn phí, có sẵn | Cần giọng ổn định → âm thanh thu sẵn hoặc TTS đám mây, lưu cache tệp |
| Nói | Web Speech API `SpeechRecognition` | Miễn phí; hỗ trợ khác nhau theo trình duyệt (cần xác minh) | Chấm âm vị → dịch vụ chấm phát âm chuyên dụng |
| Gia sư AI | Claude Messages API, gọi từ máy chủ | Khóa API không lộ ra trình duyệt, giới hạn lượt ở máy chủ | Đổi nhà cung cấp: chỉ sửa `src/ai/tutor.js` |
| Xác thực | scrypt + cookie HttpOnly ký HMAC | Có sẵn trong `node:crypto`, không lưu phiên ở máy chủ | Đăng nhập mạng xã hội → thư viện OAuth |

Lưu ý: `node:sqlite` đang ở trạng thái thử nghiệm trong Node 22 (in cảnh báo khi chạy); API có thể đổi giữa các phiên bản – kiểm tra ghi chú phát hành Node trước khi nâng cấp.

### Lược đồ cơ sở dữ liệu

Đa ngôn ngữ nằm ở mô hình dữ liệu: mọi nội dung gắn `target_lang` và `source_lang`; đặc thù hệ chữ nằm ở `items.reading` (IPA, romaji, pinyin) và `items.extra` (JSON: giống, thanh điệu, kính ngữ, thứ tự nét). Tệp đầy đủ: `src/schema.sql`.

| Bảng | Khóa chính | Cột quan trọng | Vai trò |
| --- | --- | --- | --- |
| `languages` | `code` | `script`, `romanization`, `has_tones`, `level_framework` | Đặc thù ngôn ngữ, khung trình độ |
| `users` | `id` | `email`, `password_hash`, `timezone`, `daily_goal_xp`, `learning_goal` | Tài khoản; múi giờ để tính streak |
| `courses` | `id` | `slug`, `target_lang`, `source_lang` | Khóa học theo cặp ngôn ngữ |
| `units` | `id` | `course_id`, `level`, `can_do` | Đơn vị tình huống theo cấp |
| `lessons` | `id` | `unit_id`, `status` (draft/in\_review/published), `reviewed_by` | Bài học + trạng thái kiểm duyệt |
| `items` | `id`, duy nhất (`lang`, `text`) | `reading`, `meaning_vi`, `example`, `audio_url`, `extra` | Mục từ dùng chung giữa các bài |
| `lesson_items` | (`lesson_id`, `item_id`) | – | Từ thuộc bài nào |
| `exercises` | `id` | `type`, `skill`, `prompt` (JSON gửi client), `answer` (JSON chỉ máy chủ) | Bài tập; đáp án không bao giờ rời máy chủ |
| `user_courses` | (`user_id`, `course_id`) | `level`, `placement_score`, `is_active` | Ghi danh và trình độ |
| `srs_cards` | (`user_id`, `item_id`) | `ease`, `interval_days`, `reps`, `lapses`, `due_at` | Trạng thái ôn tập |
| `review_logs` | `id` | `grade`, `interval_before`, `interval_after` | Lịch sử ôn (dữ liệu huấn luyện FSRS sau này) |
| `lesson_attempts` | `id` | `correct`, `total`, `xp` | Lịch sử học bài |
| `daily_activity` | (`user_id`, `day`) | `xp`, `lessons`, `reviews` | Tổng hợp ngày cho streak và mục tiêu |
| `placement_questions` | `id` | `level`, `options`, `answer_index` | Ngân hàng câu xếp lớp |
| `achievements`, `user_achievements` | `code` / (`user_id`, `code`) | `title_vi`, `earned_at` | Thành tích |
| `ai_usage` | (`user_id`, `day`) | `count` | Giới hạn chi phí AI |
| `events` | `id` | `name` (danh sách cho phép), `props` (chỉ số/chuỗi ngắn) | Phân tích tối giản |

Xóa tài khoản xóa dây chuyền (`ON DELETE CASCADE`) mọi bảng gắn người dùng.

### API chính

Tất cả trả JSON; lỗi có dạng `{"error":{"code","message"}}` với thông điệp tiếng Việt. Mọi route trừ đăng ký, đăng nhập, đăng xuất, health đều cần cookie phiên.

| Phương thức & đường dẫn | Đầu vào | Đầu ra |
| --- | --- | --- |
| `POST /api/auth/register` | `email`, `password` (≥ 8), `displayName`, `ageConfirmed`, `timezone` | 201 `user` + cookie |
| `POST /api/auth/login` | `email`, `password` | `user` + cookie; 429 sau 8 lần sai/15 phút |
| `POST /api/auth/logout` | – | xóa cookie |
| `GET /api/me` · `PATCH /api/me` | sửa: `displayName`, `dailyGoalXp`, `learningGoal`, `timezone` | `user` (kèm khóa đang học, streak) |
| `GET /api/me/export` · `DELETE /api/me` | xóa: `password` | toàn bộ dữ liệu cá nhân JSON · xóa vĩnh viễn |
| `GET /api/courses` · `POST /api/courses/:id/enroll` | – | danh sách khóa · ghi danh |
| `GET /api/placement/:courseId` · `POST …` | gửi: `answers[{id,index}]` | câu hỏi không đáp án · `level`, `score`, kết quả từng cấp |
| `GET /api/courses/:id/path` | – | đơn vị, bài, trạng thái mở khóa, `nextLessonId` |
| `GET /api/lessons/:id` | – | bài, mục từ, bài tập (không đáp án) |
| `POST /api/exercises/:id/check` | `response` | `correct`, `expected`, `note`, `score`, `explainVi` |
| `POST /api/lessons/:id/complete` | `answers[{exerciseId,response}]` | chấm lại ở máy chủ: `correct`, `total`, `xp`, `newCards`, `streak`, `achievements` |
| `GET /api/reviews/due?limit=` | – | `total`, `cards[]` |
| `POST /api/reviews/:itemId` | `grade` 1–4 | trạng thái thẻ mới, thành tích |
| `GET /api/progress` | – | streak, XP 7 ngày, số từ, độ chính xác, tỉ lệ nhớ, thành tích |
| `GET /api/ai/status` · `POST /api/ai/chat` | gửi: `scenario`, `messages[]` | bật/tắt, lượt còn lại, tình huống · `reply`, `correction`, `tipVi` |
| `POST /api/events` | `name` (danh sách cho phép), `props` | 204 |

**Phân quyền:** MVP chỉ có vai trò người học, mỗi người chỉ đọc/ghi dữ liệu của chính mình (mọi truy vấn lọc theo `user_id` lấy từ phiên). V1 thêm vai trò `editor` (soạn, rà soát nội dung) và `admin` (phát hành, xem báo cáo) với giao diện quản trị riêng.

### Tích hợp AI

| Chức năng | Cách làm | Kiểm soát rủi ro |
| --- | --- | --- |
| Hội thoại nhập vai | Máy chủ ghép prompt hệ thống + câu mở đầu cố định + tối đa 12 tin gần nhất (≤ 500 ký tự/tin), `max_tokens` 400, hết giờ 20 giây | Giới hạn lượt/ngày (`AI_DAILY_LIMIT`), lỗi nhà cung cấp → thông báo thân thiện, nội dung hội thoại không lưu ở máy chủ |
| Sửa lỗi | Mô hình trả JSON `reply` / `correction` / `tip_vi`; máy chủ phân tích, sai định dạng thì dùng văn bản thô | Chỉ 1 lỗi/lượt, chỉ sửa khi chắc chắn, hiển thị “AI có thể sai” |
| Chấm bài viết (V1) | Rubric theo cấp: nhiệm vụ, ngữ pháp, từ vựng, mạch lạc; trả JSON điểm + góp ý | So khớp ngẫu nhiên với giáo viên chấm để đo độ lệch |
| Giải thích ngữ pháp (V1) | Ưu tiên lấy giải thích đã duyệt từ CSDL; AI chỉ diễn đạt lại hoặc cho thêm ví dụ | Cache theo (điểm ngữ pháp, cấp), nút báo lỗi |
| Tạo ví dụ, bài tập | Chỉ trong quy trình soạn nội dung (trạng thái `draft`), không bao giờ sinh trực tiếp cho người học | Kiểm duyệt 2 lớp trước khi `published` |
| TTS | MVP: trình duyệt. V1: TTS đám mây sinh một lần mỗi câu, lưu tệp, phục vụ qua `audio_url` | Chi phí theo số câu, không theo lượt nghe |
| STT và chấm nói | MVP: bản chép lời của trình duyệt so với câu mẫu (tỉ lệ từ khớp theo thứ tự ≥ 80% là đạt; tiếng Nhật/Trung so ký tự) | Không có STT → tự đánh giá, không tính điểm |

**Prompt hệ thống mẫu** (rút gọn từ `src/ai/tutor.js`, các phần trong ngoặc nhọn do máy chủ điền):

```text
You are "Mai", a patient English conversation tutor inside a language-learning app for Vietnamese speakers.

ROLE-PLAY
- You play {role}. Scenario goal: {goal}
- The learner's name is {name}. Their CEFR level is {level}.

LANGUAGE LEVEL RULES
- Reply in English a {level} learner understands (A1–A2: max 12 words per sentence, everyday words).
- 1–3 sentences, end with a question that moves the scenario forward. Stay in the scenario.

CORRECTION RULES
- At most ONE gentle correction per turn, only for errors that affect meaning or are common. Ignore typos.
- Explain in simple Vietnamese (1 sentence). Never shame; start positively.
- Only state grammar rules you are certain are standard English. If unsure, do not correct.

SAFETY
- Content suitable for teenagers and adults; refuse harmful requests and return to the scenario.
- Never ask for phone numbers, addresses, ID numbers or passwords.

OUTPUT: JSON only
{"reply": "...", "correction": null | {"original": "...", "better": "...", "explain_vi": "..."}, "tip_vi": "..."}
```

**Kiểm soát chi phí:** giới hạn lượt/người/ngày; cắt lịch sử 12 tin; `max_tokens` thấp; chọn mô hình nhỏ cho hội thoại, mô hình mạnh hơn chỉ cho chấm bài viết; dùng prompt caching cho phần prompt hệ thống cố định nếu nhà cung cấp hỗ trợ (cần xác minh tính năng và giá); cache mọi nội dung sinh một lần (TTS, giải thích).

### Bảo mật và quyền riêng tư

- **Đã có trong MVP:** mật khẩu băm scrypt có salt; cookie `HttpOnly`, `SameSite=Lax`, `Secure` khi chạy HTTPS; chặn yêu cầu ghi khác nguồn (kiểm tra `Origin`) và chỉ nhận `application/json`; giới hạn đăng nhập sai; CSP chặt (chỉ tài nguyên cùng nguồn); đáp án không gửi về client; khóa API chỉ trong biến môi trường; xuất và xóa dữ liệu tự phục vụ; sự kiện phân tích theo danh sách cho phép, không lưu nội dung người dùng gõ.
- **Dữ liệu giọng nói:** ứng dụng không ghi âm và không lưu âm thanh; chỉ bản chép lời được gửi lên để chấm và không lưu. Một số trình duyệt (như Chrome) xử lý nhận dạng trên máy chủ của hãng – phải nêu rõ trong chính sách quyền riêng tư.
- **Gửi dữ liệu cho bên thứ ba:** tin nhắn hội thoại AI được gửi tới nhà cung cấp mô hình; nêu trong chính sách, khuyên người học không nhập thông tin cá nhân, và kiểm tra điều khoản lưu giữ dữ liệu của nhà cung cấp.
- **Quy định áp dụng (cần xác minh với luật sư hoặc nguồn chính thức):** Nghị định 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân và các văn bản mới hơn về dữ liệu cá nhân tại Việt Nam; GDPR nếu phục vụ người dùng ở EU; quy định của kho ứng dụng nếu phát hành app.
- **Trẻ em:** MVP yêu cầu xác nhận ≥ 16 tuổi. Nếu mở cho người dưới tuổi này: cần đồng ý của phụ huynh, tắt gia sư AI tự do hoặc lọc chặt hơn, không bảng xếp hạng công khai, không thu thập ngoài mức tối thiểu – ngưỡng tuổi cụ thể theo luật hiện hành cần xác minh.

## 7. Mã nguồn MVP

Toàn bộ mã (khoảng 3.200 dòng, 0 gói phụ thuộc ngoài) nằm trong tệp **noiduoc-mvp.zip** gửi kèm cuộc trò chuyện; đã chạy thử trong trình duyệt ở khổ điện thoại và qua 14 bài kiểm thử tự động. Tài liệu này liệt kê từng tệp và trích hai tệp cốt lõi để đội rà soát logic mà không cần mở mã.

### Thứ tự xây dựng (theo phụ thuộc)

1. Lược đồ CSDL và kết nối (`schema.sql`, `db.js`, `config.js`).
2. Logic thuần có kiểm thử: SRS, streak, chấm bài, xác thực.
3. Router HTTP, xử lý lỗi, tệp tĩnh, header bảo mật (`http.js`, `app.js`).
4. API: tài khoản → khóa học/xếp lớp → bài học/chấm → ôn tập → tiến độ → AI.
5. Dữ liệu mẫu và script nạp.
6. Frontend: khung SPA → đăng nhập → onboarding/xếp lớp → trang chủ → bài học → ôn tập → tiến độ → gia sư AI → cài đặt → service worker.
7. Kiểm thử tích hợp và chạy thử trong trình duyệt.

### Danh sách tệp

| Tệp | Nội dung |
| --- | --- |
| `package.json`, `.env.example`, `.gitignore`, `README.md` | Lệnh chạy, biến môi trường mẫu, hướng dẫn |
| `src/server.js` | Khởi chạy HTTP, tắt êm |
| `src/app.js` | Lắp router, kiểm tra nguồn yêu cầu, xác thực, xử lý lỗi thống nhất |
| `src/http.js` | Router tối giản, đọc JSON có giới hạn kích thước, CSP, phục vụ tệp tĩnh chống truy cập ngoài thư mục |
| `src/config.js` | Đọc `.env`, bắt buộc `SESSION_SECRET` khi production |
| `src/schema.sql`, `src/db.js` | Lược đồ 18 bảng, transaction |
| `src/auth.js` | scrypt, token ký HMAC, cookie, giới hạn đăng nhập sai |
| `src/srs.js` | SM-2 4 mức (trích bên dưới) |
| `src/streak.js` | Ngày theo múi giờ, chuỗi hiện tại và dài nhất (trích bên dưới) |
| `src/grading.js` | Chuẩn hóa đáp án, viết tắt tiếng Anh, khoan dung lỗi gõ 1–2 ký tự, chấm bài nói theo dãy từ chung dài nhất |
| `src/services.js` | Khung trình độ, cộng XP theo ngày, thành tích, sự kiện |
| `src/routes/account.js` | Đăng ký, đăng nhập, hồ sơ, xuất/xóa dữ liệu |
| `src/routes/learning.js` | Khóa học, xếp lớp, lộ trình mở khóa, bài học, chấm, hoàn thành, ôn tập |
| `src/routes/progress.js` | Tiến độ, sự kiện phân tích |
| `src/ai/tutor.js`, `src/routes/ai.js` | Prompt hệ thống, gọi API, phân tích JSON, giới hạn lượt |
| `seed/seed.js` | Nạp ngôn ngữ, thành tích, khóa học từ JSON |
| `seed/content/en-vi-cafe.json` | Tiếng Anh “Ở quán cà phê”: 25 mục từ, 3 bài, 34 bài tập, 12 câu xếp lớp |
| `seed/content/ja-vi-greetings.json` | Tiếng Nhật N5 minh họa: 5 mục từ, 1 bài |
| `public/index.html`, `styles.css`, `manifest.webmanifest`, `icon.svg`, `sw.js` | Vỏ PWA, giao diện sáng/tối, cache ngoại tuyến |
| `public/js/app.js`, `api.js`, `dom.js`, `i18n.js`, `speech.js` | Định tuyến, gọi API, tạo DOM an toàn, chuỗi giao diện, TTS/STT |
| `public/js/views/*.js` | 8 màn hình: auth, onboarding + xếp lớp, home, lesson, review, tutor, progress, settings |
| `test/unit.test.js`, `test/api.test.js` | 10 bài đơn vị + 4 bài tích hợp |

### Trích `src/srs.js`

```javascript
// Thuật toán lặp lại ngắt quãng dựa trên SM-2, rút gọn thành 4 nút đánh giá.
// Grade: 1 = Quên, 2 = Khó, 3 = Nhớ, 4 = Dễ. Hàm thuần để dễ kiểm thử và thay bằng FSRS ở V1.
export const GRADES = { AGAIN: 1, HARD: 2, GOOD: 3, EASY: 4 };
const MIN_EASE = 1.3;
const MAX_INTERVAL = 365;
const RELEARN_MINUTES = 10;

export function newCard(now = new Date()) {
  return { ease: 2.5, interval_days: 0, reps: 0, lapses: 0, due_at: now.toISOString(), last_review: null };
}

export function review(card, grade, now = new Date()) {
  if (![1, 2, 3, 4].includes(grade)) throw new RangeError('grade phải là 1–4');
  let { ease, interval_days: interval, reps, lapses } = card;

  if (grade === GRADES.AGAIN) {
    // Quên: học lại sau 10 phút, giảm độ dễ
    return {
      ease: Math.max(MIN_EASE, round2(ease - 0.2)),
      interval_days: 0, reps: 0, lapses: lapses + 1,
      last_review: now.toISOString(),
      due_at: new Date(now.getTime() + RELEARN_MINUTES * 60_000).toISOString(),
    };
  }

  // Ánh xạ sang thang chất lượng SM-2: Khó=3, Nhớ=4, Dễ=5
  const q = grade + 1;
  const newEase = Math.max(MIN_EASE, round2(ease + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))));

  let next;
  if (reps === 0) next = grade === GRADES.EASY ? 4 : 1;
  else if (reps === 1) next = grade === GRADES.HARD ? 3 : grade === GRADES.GOOD ? 6 : 8;
  else if (grade === GRADES.HARD) next = interval * 1.2;
  else if (grade === GRADES.GOOD) next = interval * newEase;
  else next = interval * newEase * 1.3;

  // Luôn tăng ít nhất 1 ngày khi nhớ được, làm tròn và chặn trên
  if (reps >= 2) next = Math.max(interval + 1, Math.round(next));
  next = Math.min(MAX_INTERVAL, next);

  return {
    ease: newEase, interval_days: next, reps: reps + 1, lapses,
    last_review: now.toISOString(),
    due_at: new Date(now.getTime() + next * 86400_000).toISOString(),
  };
}

export const isMature = (card) => card.interval_days >= 21;
function round2(x) { return Math.round(x * 100) / 100; }
```

### Trích `src/streak.js`

```javascript
// 'YYYY-MM-DD' của một thời điểm theo múi giờ người dùng
export function dayKey(date = new Date(), tz = 'Asia/Ho_Chi_Minh') {
  return new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' }).format(date);
}

export function shiftDay(key, n) {
  const d = new Date(`${key}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

// Streak = số ngày liên tiếp có hoạt động, kết thúc ở hôm nay hoặc hôm qua
export function computeStreak(activeDays, today) {
  const set = new Set(activeDays);
  let cursor = set.has(today) ? today : shiftDay(today, -1);
  if (!set.has(cursor)) return { current: 0, activeToday: false };
  let current = 0;
  while (set.has(cursor)) { current += 1; cursor = shiftDay(cursor, -1); }
  return { current, activeToday: set.has(today) };
}
```

### Mẫu dữ liệu một bài tập

Mỗi bài tập tách `prompt` (gửi cho trình duyệt) và `answer` (chỉ máy chủ giữ). Thêm ngôn ngữ mới chỉ cần thêm tệp JSON theo cùng cấu trúc.

```json
{
  "type": "order",
  "skill": "grammar",
  "prompt": { "tokens": ["tea,", "a", "please.", "large"], "translationVi": "Cho tôi một ly trà cỡ lớn." },
  "answer": { "accept": ["a large tea please"] },
  "explain_vi": "Tính từ chỉ cỡ (large) đứng TRƯỚC danh từ (tea), ngược với tiếng Việt “trà lớn”."
}
```

## 8. Cài đặt, chạy, kiểm thử và triển khai

Chỉ cần Node.js 22.5 trở lên; không cài gói nào, không cần máy chủ CSDL.

### Chạy trên máy cá nhân

1. Cài Node.js bản LTS từ trang chính thức nodejs.org (chọn bản ≥ 22.5), mở Terminal và gõ `node --version` để kiểm tra.
2. Giải nén `noiduoc-mvp.zip`, vào thư mục: `cd noiduoc`.
3. Tạo tệp cấu hình: `cp .env.example .env` (Windows: `copy .env.example .env`).
4. Nạp dữ liệu mẫu: `npm run seed`.
5. Chạy: `npm start`, mở `http://localhost:3000` trên trình duyệt. Trên điện thoại cùng Wi-Fi: dùng địa chỉ IP của máy tính thay cho `localhost` (nhận dạng giọng nói và cài PWA có thể cần HTTPS).
6. Khi sửa mã: `npm run dev` tự khởi động lại. Muốn làm lại từ đầu: `npm run reset` (xóa toàn bộ dữ liệu).

### Biến môi trường

| Biến | Mặc định | Ý nghĩa |
| --- | --- | --- |
| `PORT` | 3000 | Cổng máy chủ |
| `DB_PATH` | `./data/noiduoc.db` | Tệp SQLite |
| `SESSION_SECRET` | (bắt buộc đổi khi production) | Khóa ký phiên đăng nhập, chuỗi ngẫu nhiên ≥ 48 byte |
| `COOKIE_SECURE` | false | `true` khi chạy sau HTTPS |
| `NODE_ENV` | – | `production` để bật kiểm tra cấu hình bắt buộc |
| `ANTHROPIC_API_KEY` | trống | Bật gia sư AI; trống thì tính năng tự tắt |
| `AI_MODEL` | `claude-haiku-5-5` | Tên mô hình – xác minh danh sách hiện hành tại docs.claude.com |
| `AI_DAILY_LIMIT` | 20 | Lượt AI tối đa mỗi người/ngày |

### Kiểm thử

- `npm test` chạy 14 bài: SRS (khoảng ôn, quên, chặn ease), streak theo múi giờ, chấm bài (viết tắt, lỗi gõ, thứ tự từ, bài nói, tiếng Nhật), phân tích đầu ra AI, xác thực; và tích hợp chạy máy chủ thật với CSDL trong bộ nhớ qua toàn bộ luồng người học, AI giả lập (không tốn phí), bảo mật (CSRF, giới hạn đăng nhập, truy cập ngoài thư mục), và khóa tiếng Nhật.
- **Kiểm thử thủ công trước mỗi đợt phát hành:** đăng ký → onboarding → xếp lớp → hoàn thành 1 bài (cả câu sai) → ôn 5 thẻ → tiến độ → chế độ tối → xuất dữ liệu → xóa tài khoản; trên Chrome Android, Safari iOS và một trình duyệt máy tính.
- **Kiểm tra nội dung:** `npm run reset` rồi làm mọi bài với đáp án đúng; mọi câu phải chấm đúng, mọi TTS phải đọc được.

### Triển khai

Yêu cầu nơi chạy: tiến trình Node chạy liên tục và **ổ đĩa bền vững** cho tệp SQLite (nền tảng serverless xóa đĩa sau mỗi lần chạy không phù hợp nếu chưa chuyển sang PostgreSQL).

| Lựa chọn | Phù hợp khi | Điều cần xác minh |
| --- | --- | --- |
| VPS nhỏ (trong nước hoặc quốc tế) + Caddy/Nginx làm HTTPS | Muốn chi phí cố định thấp, toàn quyền | Giá gói, băng thông, vị trí máy chủ gần người dùng |
| PaaS có volume gắn kèm (ví dụ Fly.io, Railway, Render) | Không muốn tự quản trị máy chủ | Gói miễn phí/thấp còn tồn tại không, volume có trong gói không, máy có ngủ khi không dùng không |
| PaaS + PostgreSQL quản lý | Khi vượt một máy chủ | Cần đổi lớp `db.js` sang PostgreSQL |

Các bước trên VPS: cài Node ≥ 22.5 → chép mã → tạo `.env` với `NODE_ENV=production`, `SESSION_SECRET` ngẫu nhiên, `COOKIE_SECURE=true` → `npm run seed` → chạy bằng systemd hoặc pm2 để tự khởi động lại → reverse proxy HTTPS → sao lưu `data/noiduoc.db` mỗi ngày ra nơi khác (ví dụ lệnh `sqlite3 noiduoc.db ".backup backup.db"` theo lịch cron).

### Mở rộng

- **Thêm chủ đề/ngôn ngữ:** thêm tệp `seed/content/*.json`, chạy `npm run seed`.
- **Thêm dạng bài:** thêm giá trị vào ràng buộc `type` trong `schema.sql`, một nhánh trong `grading.js`, một renderer trong `public/js/views/lesson.js`.
- **Đổi nhà cung cấp AI:** chỉ sửa `callTutor` trong `src/ai/tutor.js`.
- **Thêm ngôn ngữ giao diện:** thêm từ điển trong `public/js/i18n.js`.

## 9. Đo lường, mô hình kinh doanh và chi phí vận hành

Chi phí biến đổi lớn nhất là API AI; mọi con số dưới đây là **ước tính** theo giả định nêu rõ, còn đơn giá dịch vụ **cần xác minh** tại thời điểm triển khai rồi nhân vào.

### Kế hoạch kiểm thử sản phẩm

| Loại | Nội dung | Khi nào |
| --- | --- | --- |
| Đơn vị | SRS, streak, chấm bài, xác thực, phân tích AI (đã có) | Mỗi lần sửa mã |
| Tích hợp | Luồng người học qua API thật, CSDL bộ nhớ (đã có) | Mỗi lần sửa mã |
| Người dùng thử | 5–8 người mỗi persona làm onboarding + 1 bài + ôn tập, nói to suy nghĩ; ghi chỗ vấp | Trước mở thử và sau mỗi thay đổi lớn về luồng |
| Nội dung | Giáo viên + người bản ngữ duyệt từng bài; theo dõi câu có tỉ lệ sai > 60% | Mỗi đợt nội dung mới |
| Thiết bị | Chrome Android, Safari iOS, trình duyệt máy tính; chế độ tối; trình đọc màn hình | Trước mỗi đợt phát hành |

### Sự kiện phân tích

Đã có endpoint `POST /api/events` với danh sách cho phép; bảng `events` chỉ lưu số và chuỗi ngắn, không lưu nội dung người dùng gõ.

| Sự kiện | Thuộc tính | Câu hỏi trả lời |
| --- | --- | --- |
| `onboarding_started`, `onboarding_completed` | `placement`, `daily` | Rơi ở bước nào; mục tiêu ngày phổ biến |
| `placement_completed` | `level`, `score` | Phân bố trình độ người dùng |
| `lesson_started`, `lesson_completed` | `lessonId`, `correct`, `total` | Tỉ lệ bỏ giữa bài; bài quá khó |
| `review_session_started`, `review_session_completed` | `due`, `reviewed` | Người học có ôn khi đến hạn không |
| `ai_chat_started` | `scenario` | Mức quan tâm gia sư AI |
| `tts_played`, `speech_recognition_unavailable` | – | Mức dùng nghe; tỉ lệ thiết bị không chấm được nói |
| `pwa_installed` | – | Tỉ lệ cài ứng dụng |

Retention D1/D7/D30 và streak tính trực tiếp từ `daily_activity`, không cần sự kiện riêng.

### Thử nghiệm A/B ưu tiên

1. Xếp lớp bắt buộc vs tùy chọn → tác động lên hoàn thành onboarding.
2. Trang chủ đặt ôn tập trước bài mới vs ngược lại → tỉ lệ nhớ và D7.
3. Mục tiêu ngày mặc định 10 vs 20 XP → D7 và phút học/ngày.
4. Bài nói ở giữa bài vs cuối bài → tỉ lệ hoàn thành bài.

Với 50–100 người thử, A/B khó đạt ý nghĩa thống kê; giai đoạn này dùng phỏng vấn và số liệu định tính, A/B chỉ chạy khi có vài nghìn người hoạt động/tháng.

### Vòng phản hồi

Nút “Báo lỗi câu này” trong mỗi bài tập (V1) → hàng đợi giáo viên; khảo sát 1 câu sau bài thứ 5; nhóm Zalo/Facebook cho người thử sớm; họp tổng hợp phản hồi mỗi 2 tuần.

### Mô hình kinh doanh

**Freemium (khuyến nghị):** toàn bộ bài học, ôn tập, nghe – nói theo mẫu miễn phí; gói trả phí mở gia sư AI nhiều lượt hơn, chấm bài viết, tình huống nâng cao, gói ngoại tuyến. Lý do: phần tốn chi phí biên (AI) là phần thu tiền; phần học cốt lõi không bị khóa nên không mâu thuẫn mục tiêu học.

Giá gói và tỉ lệ chuyển đổi là **giả định cần thử nghiệm**: thử 2–3 mức giá tháng/năm với người dùng thử trước khi cố định; tham khảo giá các ứng dụng học ngoại ngữ tại Việt Nam ở thời điểm đó (cần xác minh). Kênh phụ V2: gói trường học, trung tâm ngoại ngữ, doanh nghiệp đào tạo nhân viên.

### Chi phí vận hành – 3 kịch bản (tháng thứ 6)

Giả định chung: 30% người hoạt động tháng (MAU) dùng gia sư AI, mỗi người 6 buổi × 8 lượt = 48 lượt/tháng; mỗi lượt khoảng 1.600 token đầu vào (prompt hệ thống + lịch sử ≤ 12 tin) và 150 token đầu ra. Đơn giá token, giá máy chủ, giá giờ công là biến cần điền.

| Hạng mục | Thận trọng | Cơ sở | Lạc quan |
| --- | --- | --- | --- |
| Người hoạt động/tháng (MAU) | 200 | 1.000 | 5.000 |
| Lượt AI/tháng | \~2.900 | \~14.400 | \~72.000 |
| Token AI vào / ra mỗi tháng | \~4,6 triệu / \~0,4 triệu | \~23 triệu / \~2,2 triệu | \~115 triệu / \~11 triệu |
| Chi phí AI | token × đơn giá mô hình nhỏ (cần xác minh); giảm thêm nếu dùng prompt caching | như bên trái | như bên trái; cân nhắc hạ giới hạn lượt cho gói miễn phí |
| Hạ tầng | 1 VPS nhỏ + tên miền + sao lưu | 1 VPS vừa | 2 máy + PostgreSQL quản lý + CDN tệp âm thanh |
| Nội dung | 8–10 đơn vị: mỗi đơn vị \~8–12 giờ giáo viên + \~2–3 giờ người bản ngữ (ước tính) | như bên trái + 4 đơn vị/tháng | thêm một ngôn ngữ thứ hai |
| Nhân sự | 1 kỹ sư + 1 giáo viên bán thời gian | + 1 người làm nội dung/cộng đồng | + 1 kỹ sư, 1 thiết kế |

Nhân sự và nội dung là chi phí lớn nhất ở cả ba kịch bản; chi phí AI tăng tuyến tính theo người dùng nên được chặn bằng `AI_DAILY_LIMIT` và gói trả phí.

### Thu hút và giữ chân người dùng

- **Ban đầu (0–500 người):** mời từ cộng đồng học tiếng Anh, nhóm du học, nhóm người đi làm trên Facebook/Zalo/TikTok; nội dung ngắn “1 tình huống – 3 câu nói được ngay” dẫn về bài học miễn phí; hợp tác 2–3 giáo viên/trung tâm cho học viên dùng làm bài tập về nhà.
- **Giữ chân:** ôn tập đúng lúc là lý do quay lại mỗi ngày; nhắc học theo giờ người dùng chọn (V1); báo cáo tuần “bạn đã nói được thêm X câu”; mỗi tháng thêm tình huống mới theo góp ý.
- **Lan tỏa:** chia sẻ thẻ thành tích, lời mời bạn học cùng (V2); không dùng ưu đãi gây áp lực.

## 10. Lộ trình theo giai đoạn

Mỗi giai đoạn chỉ mở khi đạt tiêu chí nghiệm thu của giai đoạn trước; mốc thời gian là ước tính với đội 1–2 người.

| Giai đoạn | Đầu ra | Nhân sự | Rủi ro chính | Tiêu chí nghiệm thu |
| --- | --- | --- | --- | --- |
| **0–30 ngày: Thử nghiệm kín** | Triển khai MVP có HTTPS; 4–5 đơn vị A1 đã duyệt; chính sách quyền riêng tư; bật AI có giới hạn; 30–50 người thử | 1 kỹ sư, 1 giáo viên bán thời gian, người bản ngữ theo giờ | Nội dung chậm; nhận dạng giọng nói kém trên iOS | ≥ 60% hoàn thành bài đầu; D7 ≥ 20%; không lỗi chặn luồng; ≥ 15 phỏng vấn người dùng |
| **31–90 ngày: V1** | 8–10 đơn vị A1–A2; thẻ đảo chiều; FSRS; nhắc học Web Push; đăng nhập Google, quên mật khẩu; nút báo lỗi câu; giao diện quản trị nội dung; âm thanh thu sẵn cho từ vựng; mở rộng 300–1.000 người | + 1 người làm nội dung/cộng đồng | Chi phí AI tăng; hàng đợi duyệt nội dung tắc | D30 ≥ 10%; tỉ lệ nhớ khi ôn 80–90%; chi phí AI/người trong ngân sách; tỉ lệ câu bị báo lỗi < 2% |
| **3–6 tháng: Kiếm tiền và mở rộng** | Gói trả phí (AI nhiều lượt, chấm bài viết); B1; ôn ngoại tuyến; chuyển PostgreSQL nếu cần; bản thử ngôn ngữ thứ hai (Nhật hoặc Hàn) | 2 kỹ sư, 1–2 giáo viên, 1 thiết kế bán thời gian | Chuyển đổi trả phí thấp; mở rộng nội dung kéo giảm chất lượng | Tỉ lệ trả phí đạt mức giả định trong mô hình; doanh thu bù chi phí AI; NPS dương |
| **6–12 tháng: Tăng trưởng** | B2; ngôn ngữ thứ hai đầy đủ cấp đầu; chấm phát âm theo âm vị; bạn học, giải đấu tùy chọn; gói trường học/doanh nghiệp; cân nhắc app kho ứng dụng | Đội 5–7 người | Cạnh tranh từ ứng dụng lớn; quy định dữ liệu thay đổi | Tăng trưởng MAU ổn định theo tháng; ít nhất 1 khách hàng tổ chức; hòa vốn vận hành (không tính lương sáng lập) |

## 11. Rủi ro và cách giảm thiểu

Rủi ro lớn nhất không phải kỹ thuật mà là **chất lượng và tốc độ làm nội dung**: mã đã chạy, nhưng giá trị sản phẩm nằm ở các bài học đã duyệt.

| Nhóm | Rủi ro | Mức | Cách giảm thiểu |
| --- | --- | --- | --- |
| Nội dung | Sai ngữ pháp, không tự nhiên, sai trình độ | Cao | Quy trình 6 bước, người bản ngữ ký duyệt, chỉ hiển thị bài `published`, theo dõi câu sai nhiều |
| Nội dung | AI ảo giác khi sửa lỗi hoặc giải thích | Cao | Prompt cấm bịa quy tắc, 1 lỗi/lượt, nhãn “AI có thể sai”, giải thích ngữ pháp ưu tiên lấy từ CSDL đã duyệt |
| Nội dung | Vi phạm bản quyền (sách, đề thi, âm thanh) | Trung bình | Chỉ dùng nội dung tự viết hoặc có giấy phép rõ; ghi nguồn trong trường `_license`; không chép đề thi chứng chỉ |
| Kỹ thuật | Nhận dạng giọng nói không có hoặc kém trên một số trình duyệt | Cao | Chế độ tự đánh giá không tính điểm; đo bằng sự kiện `speech_recognition_unavailable`; V2 dịch vụ chấm riêng |
| Kỹ thuật | `node:sqlite` thử nghiệm, SQLite một máy chủ | Trung bình | Ghim phiên bản Node; lớp `db.js` mỏng để chuyển PostgreSQL; sao lưu hằng ngày |
| Kỹ thuật | Chi phí và độ trễ API AI | Trung bình | Giới hạn lượt, cắt lịch sử, mô hình nhỏ, hết giờ 20 giây, tắt được bằng một biến môi trường |
| Kỹ thuật | Mất dữ liệu | Trung bình | Sao lưu ngày ra nơi khác, thử khôi phục mỗi tháng |
| Bảo mật | Chiếm tài khoản, CSRF, XSS | Trung bình | scrypt, cookie HttpOnly/SameSite, kiểm tra Origin, CSP, DOM không dùng innerHTML, giới hạn đăng nhập; V1 thêm quên mật khẩu an toàn |
| Pháp lý | Không tuân thủ quy định bảo vệ dữ liệu cá nhân | Trung bình | Thu tối thiểu, chính sách rõ, xuất/xóa tự phục vụ, rà soát với luật sư trước mở công khai |
| Pháp lý | Người dùng dưới tuổi | Trung bình | Xác nhận ≥ 16 tuổi; luồng phụ huynh trước khi nhắm học sinh |
| Pháp lý | Trùng tên/nhãn hiệu | Thấp | Tra cứu nhãn hiệu, tên miền trước khi đầu tư thương hiệu |
| Thị trường | Ứng dụng lớn có sẵn người dùng, tính năng AI tương tự | Cao | Tập trung người Việt: giải thích theo lỗi người Việt, tình huống địa phương, giá phù hợp; hợp tác giáo viên/trung tâm |
| Thị trường | Người dùng không trả tiền | Trung bình | Thử giá sớm; kênh B2B; giữ chi phí biến đổi thấp |
| Đạo đức | Gamification gây áp lực, học vì chuỗi chứ không vì tiến bộ | Thấp | Không bán cứu chuỗi, không phần thưởng ngẫu nhiên, mục tiêu ngày tự chọn, ngày nghỉ (V1) |

## 12. Checklist hành động 7 ngày đầu

- [ ] Ngày 1: Cài Node ≥ 22.5, chạy MVP trên máy, làm hết 3 bài mẫu và chạy `npm test`.
- [ ] Ngày 1: Quyết định ngôn ngữ, đối tượng và nền tảng có giữ theo giả định ở mục 2 không.
- [ ] Ngày 2: Tra cứu tên “NóiĐược”: tên miền, nhãn hiệu, trùng ứng dụng.
- [ ] Ngày 2: Tìm 1 giáo viên tiếng Anh và 1 người bản ngữ rà soát; thống nhất mẫu JSON nội dung.
- [ ] Ngày 3: Nhờ người bản ngữ rà soát 3 bài mẫu, sửa và ghi `reviewed_by` thật.
- [ ] Ngày 3: Xác minh giá và giới hạn API AI, chọn mô hình, đặt `AI_DAILY_LIMIT` theo ngân sách.
- [ ] Ngày 4: Chọn nơi triển khai (VPS hoặc PaaS có volume), kiểm tra điều kiện gói hiện hành.
- [ ] Ngày 4: Triển khai với HTTPS, `NODE_ENV=production`, `SESSION_SECRET` ngẫu nhiên, sao lưu tự động.
- [ ] Ngày 5: Viết chính sách quyền riêng tư và điều khoản (nêu rõ dữ liệu gửi nhà cung cấp AI và nhận dạng giọng nói của trình duyệt); nhờ người có chuyên môn pháp lý xem.
- [ ] Ngày 5–6: Giáo viên soạn đơn vị thứ 2 (“Chào hỏi và giới thiệu”) theo quy trình mục 4.
- [ ] Ngày 6: Thử nghiệm với 5 người quen theo kịch bản usability; ghi lại chỗ vấp.
- [ ] Ngày 7: Tổng hợp phản hồi, chọn 3 sửa đổi ưu tiên, mời 30–50 người thử đợt đầu.

## 13. Hạn chế và điều cần tự xác minh

Tài liệu này không tra cứu trực tuyến giá, giới hạn hay chính sách của bên thứ ba; mọi mục dưới đây cần kiểm tra từ nguồn chính thức trước khi ra quyết định.

| Hạng mục | Cần xác minh | Nguồn nên xem |
| --- | --- | --- |
| API AI | Tên mô hình hiện hành, giá token, giới hạn tốc độ, prompt caching, điều khoản lưu giữ dữ liệu | docs.claude.com và trang giá của nhà cung cấp |
| TTS / STT trình duyệt | Mức hỗ trợ `SpeechRecognition` và giọng `speechSynthesis` trên Chrome, Safari iOS, Firefox; dữ liệu giọng nói có rời thiết bị không | Tài liệu của từng trình duyệt, MDN |
| Web Push trên iOS | Điều kiện hỗ trợ (cài PWA, phiên bản iOS) | Tài liệu Apple, MDN |
| Node.js | Trạng thái `node:sqlite`, phiên bản LTS hiện hành | nodejs.org, ghi chú phát hành |
| Hosting | Gói miễn phí/giá thấp còn không, có volume bền vững không, máy có ngủ không | Trang giá từng nền tảng |
| Quy định dữ liệu | Văn bản hiện hành về bảo vệ dữ liệu cá nhân tại Việt Nam (Nghị định 13/2023/NĐ-CP và văn bản mới hơn nếu có), ngưỡng tuổi cần đồng ý phụ huynh, GDPR nếu có người dùng EU | Cổng thông tin pháp luật chính thức, luật sư |
| Kho ứng dụng | Chính sách ứng dụng bọc web, mua trong ứng dụng, ứng dụng cho trẻ em | Hướng dẫn của Apple App Store, Google Play |
| Đối thủ | Số người dùng, giá gói, tính năng hiện tại ở mục 3 | Báo cáo chính thức, trang sản phẩm |
| Danh mục từ theo CEFR | Giấy phép sử dụng các danh mục từ vựng/ngữ pháp tham chiếu | Trang của tổ chức phát hành |

**Giới hạn của MVP cần biết:**

- Nội dung mẫu do AI soạn theo yêu cầu, chưa qua người bản ngữ; trường `reviewed_by: demo-reviewer` chỉ là ví dụ.
- Chấm nói dựa trên bản chép lời của trình duyệt (đúng từ chứ không đúng âm); không thay thế giáo viên phát âm.
- Văn bản cần nghe trong bài nghe/chép chính tả nằm trong dữ liệu gửi về trình duyệt, người rành kỹ thuật có thể xem; chấp nhận được khi không có điểm số quan trọng, V1 chuyển sang tệp âm thanh.
- Giới hạn đăng nhập sai lưu trong bộ nhớ, mất khi khởi động lại và không chia sẻ giữa nhiều máy chủ.
- Chưa có quên mật khẩu, xác minh email, thông báo đẩy, ôn tập ngoại tuyến.
- Gia sư AI chỉ chạy cho khóa tiếng Anh; AI có thể sai và không nên coi góp ý của nó là chuẩn mực.
