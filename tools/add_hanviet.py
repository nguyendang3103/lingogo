"""Tạo bảng Hán Việt cho tiếng Nhật: data/ja.json -> khoá "hv" {chữ Hán: âm Hán Việt viết hoa}.

App dùng bảng này để hiện Hán Việt dưới mỗi từ tiếng Nhật và ra câu hỏi "Từ này đọc Hán Việt là gì?".
Thứ tự ưu tiên khi một chữ có nhiều nguồn:
  1. data/zh.json (chars[chữ].hv): âm Hán Việt đã chốt cho từ tiếng Trung
  2. bảng kanji của chính data/ja.json (lấy âm đầu tiên nếu có nhiều âm)
  3. phần bổ sung SUPP bên dưới (do Claude điền ngày 29/10/2026, Sally nên soát lại; chữ chỉ có ở Nhật như 俺 働 咲 込 畑 để trống)
Chạy lại được nhiều lần. Chạy sau add_n5_extras.py:  python tools/add_hanviet.py  (từ thư mục Lingogo)
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ja = json.load(open(os.path.join(ROOT, 'data/ja.json'), encoding='utf8'))
zh = json.load(open(os.path.join(ROOT, 'data/zh.json'), encoding='utf8'))

SUPP = """丁:đinh 世:thế 両:lưỡng 以:dĩ 似:tự 低:đê 使:sử 倒:đảo 借:tá 傘:tản 備:bị 優:ưu 冗:nhũng 切:thiết 利:lợi 制:chế 割:cát 勉:miễn 動:động 務:vụ 卒:tốt 卓:trác 単:đơn 卵:noãn 台:đài 吹:xuy 呂:lữ 周:chu 味:vị 員:viên 喫:khiết 器:khí 困:khốn 図:đồ 園:viên 型:hình 堂:đường 場:trường 変:biến 夜:dạ 夢:mộng 婚:hôn 嫌:hiềm 宅:trạch 実:thực 室:thất 容:dung 宿:túc 寂:tịch 富:phú 寒:hàn 寝:tẩm 寧:ninh 寮:liêu 対:đối 寿:thọ 局:cục 屋:ốc 市:thị 布:bố 師:sư 席:tịch 帳:trướng 幹:cán 広:quảng 店:điếm 庫:khố 庭:đình 康:khang 建:kiến 弁:biện 引:dẫn 張:trương 強:cường 当:đương 役:dịch 彼:bỉ 心:tâm 必:tất 念:niệm 怖:bố 性:tính 恋:luyến 悪:ác 惑:hoặc 憩:khế 所:sở 指:chỉ 掃:tảo 授:thụ 揺:dao 撮:toát 故:cố 教:giáo 敵:địch 料:liệu 断:đoạn 昔:tích 映:ánh 昼:trú 晩:vãn 晴:tình 暇:hạ 暑:thử 暮:mộ 曇:đàm 曜:diệu 曲:khúc 最:tối 末:mạt 札:trát 束:thúc 桜:anh 械:giới 椅:ỷ 業:nghiệp 楽:lạc 横:hoành 機:cơ 欲:dục 歩:bộ 歯:xỉ 歳:tuế 死:tử 残:tàn 氏:thị 汚:ô 泉:tuyền 泣:khấp 洋:dương 活:hoạt 浴:dục 渇:khát 湯:thang 準:chuẩn 漢:hán 濡:nhu 無:vô 焼:thiêu 煮:chử 特:đặc 独:độc 狭:hiệp 猫:miêu 玉:ngọc 理:lý 瓶:bình 甘:cam 産:sản 申:thân 番:phiên 疲:bì 登:đăng 真:chân 眠:miên 知:tri 破:phá 磨:ma 祖:tổ 祭:tế 窓:song 笑:tiếu 符:phù 算:toán 箸:trợ 簡:giản 約:ước 紅:hồng 紙:chỉ 終:chung 結:kết 絵:hội 絶:tuyệt 続:tục 線:tuyến 美:mỹ 者:giả 職:chức 背:bối 腕:uyển 腹:phúc 苦:khổ 菓:quả 落:lạc 蔵:tàng 薬:dược 虫:trùng 袋:đại 複:phức 覚:giác 計:kế 記:ký 診:chẩn 試:thí 誌:chí 誕:đản 説:thuyết 誰:thùy 課:khóa 調:điều 談:đàm 議:nghị 豆:đậu 財:tài 販:phán 資:tư 赤:xích 趣:thú 転:chuyển 輩:bối 輪:luân 辛:tân 辞:từ 迷:mê 週:chu 遅:trì 遊:du 過:quá 道:đạo 達:đạt 部:bộ 郵:bưu 郷:hương 配:phối 野:dã 鉄:thiết 銭:tiền 鍵:kiện 閉:bế 開:khai 除:trừ 陽:dương 隣:lân 雑:tạp 難:nan 青:thanh 静:tĩnh 靴:ngoa 韓:hàn 頑:ngoan 頭:đầu 題:đề 顔:nhan 類:loại 風:phong 飛:phi 飴:di 館:quán 験:nghiệm 鳥:điểu 黄:hoàng 黒:hắc 鼻:tị"""
supp = dict(p.split(':') for p in SUPP.split())

hv = {}
for t in ja['topics']:
    for k in t['kanji']:
        first = re.split(r'[,/;、]', k['hv'])[0].strip()
        if first:
            hv[k['k']] = first.upper()
for c, e in zh['chars'].items():
    if e.get('hv') and c not in hv:
        hv[c] = e['hv'].upper()
for c, v in supp.items():
    if c not in hv:
        hv[c] = v.upper()
# Chữ có trong bảng zh được ưu tiên hơn âm đầu tiên của bảng kanji khi bảng kanji ghi nhiều âm
for t in ja['topics']:
    for k in t['kanji']:
        if re.search(r'[,/;、]', k['hv']) and k['k'] in zh['chars'] and zh['chars'][k['k']].get('hv'):
            hv[k['k']] = zh['chars'][k['k']]['hv'].upper()
# Nghĩa từng chữ (hvm): ưu tiên bảng kanji N5 (Kanji N5.xlsx), rồi bảng chữ tiếng Trung, rồi phần Claude bổ sung (MEAN)
MEAN = """丁:ngăn nắp|七:bảy|三:ba|世:đời, thế giới|両:hai, cả hai|九:chín|二:hai|五:năm|京:kinh đô|以:từ, bằng|似:giống|低:thấp|体:cơ thể|使:dùng, sai khiến|倒:đổ, ngã|借:mượn|傘:ô|備:chuẩn bị|優:ưu tú, dịu dàng|元:gốc, nguồn|兄:anh trai|光:ánh sáng|八:tám|六:sáu|具:dụng cụ|冗:thừa|切:cắt|利:lợi|制:chế định|割:chia, cắt|勉:cố gắng|動:chuyển động|務:nhiệm vụ|卒:tốt nghiệp|卓:cái bàn, xuất sắc|単:đơn, một|卵:trứng|古:cũ|台:bệ, đài|吹:thổi|周:vòng quanh|味:vị|員:nhân viên|喫:ăn, uống|器:đồ dùng|四:bốn|困:khó khăn|図:hình vẽ, bản đồ|園:vườn|型:khuôn, kiểu|堂:sảnh, nhà lớn|場:nơi, chỗ|士:sĩ, người|売:bán|変:thay đổi, lạ|夕:chiều tối|夜:đêm|夢:giấc mơ|太:to, béo|婚:kết hôn|嫌:ghét|宅:nhà|実:thật, quả|室:phòng|容:dung chứa, dáng vẻ|宿:trọ, nghỉ trọ|寂:vắng lặng|富:giàu|寒:lạnh|寝:ngủ|寧:chu đáo|寮:ký túc xá|寺:chùa|対:đối diện, đối với|寿:thọ, tuổi thọ|局:cục, văn phòng|屋:nhà, cửa hiệu|市:thành phố, chợ|布:vải|師:thầy|席:chỗ ngồi|帰:về|帳:sổ|幹:thân, trục chính|広:rộng|店:cửa hàng|庫:kho|庭:sân vườn|康:khỏe mạnh|建:xây dựng|弁:nói, biện luận|引:kéo|張:căng, giương|強:mạnh|当:trúng, đúng|役:vai, chức vụ|彼:anh ấy, kia|心:tim, lòng|必:nhất định|念:nghĩ, niệm|怖:sợ|性:tính, bản chất|恋:yêu|悪:xấu, ác|惑:lầm, bối rối|憩:nghỉ ngơi|所:nơi|指:ngón tay, chỉ|掃:quét|授:trao, dạy|揺:rung, lắc|撮:chụp|故:cũ, cố|教:dạy|敵:địch, kẻ thù|料:vật liệu, phí|断:cắt đứt, quyết định|旅:du lịch, chuyến đi|族:dòng họ|昔:xưa|映:chiếu, phản chiếu|昼:ban ngày, trưa|晩:tối|晴:trời nắng|暇:rảnh|暑:nóng|暗:tối|暮:chiều tối, sống|曇:nhiều mây|曜:ngày trong tuần|曲:cong, bản nhạc|最:nhất|朝:buổi sáng|末:cuối|札:tờ tiền, thẻ|束:bó, hẹn|桜:hoa anh đào|械:máy, khí cụ|森:rừng|椅:ghế|業:nghề, nghiệp|楽:vui, nhạc|横:ngang|機:máy, cơ hội|欲:muốn|歩:bước đi|歯:răng|歳:tuổi|死:chết|残:còn lại|毎:mỗi|毛:lông, tóc|氏:ông, họ|氷:băng, đá|汚:bẩn|泉:suối|泣:khóc|洋:phương Tây, biển|活:sống động|浴:tắm|渇:khát|湯:nước nóng|準:chuẩn|漢:Hán|濡:ướt|無:không có|焼:nướng, cháy|煮:nấu|物:vật|特:đặc biệt|犬:chó|独:một mình|狭:hẹp|猫:mèo|玉:ngọc, bi|理:lý lẽ|瓶:chai, bình|甘:ngọt|産:sinh, sản xuất|申:nói, trình|男:đàn ông|町:phố, thị trấn|界:giới, cõi|番:số thứ tự, lượt|疲:mệt|病:bệnh|登:leo|真:thật|眠:ngủ|知:biết|破:rách, phá|磨:mài, đánh bóng|社:công ty, đền|祖:tổ tiên|祭:lễ hội|窓:cửa sổ|笑:cười|符:phù hiệu, vé|算:tính toán|箸:đũa|簡:giản dị|約:hẹn, khoảng|紅:đỏ thẫm|紙:giấy|終:kết thúc|結:nối, kết|絵:tranh|絶:tuyệt, cắt đứt|続:tiếp tục|線:đường, tuyến|美:đẹp|者:người|職:nghề, chức vụ|肉:thịt|背:lưng|腕:cánh tay|腹:bụng|良:tốt|苦:đắng, khổ|草:cỏ|荷:hàng hóa, gánh|菓:bánh, trái|落:rơi|蔵:kho chứa|薬:thuốc|虫:sâu bọ|袋:túi|複:phức tạp, nhiều lớp|覚:nhớ, tỉnh ra|親:cha mẹ, thân thiết|計:đo, tính|記:ghi chép|診:khám bệnh|試:thử|誌:ghi chép, tạp chí|誕:sinh ra|語:lời nói, ngôn ngữ|説:giải thích, lời nói|誰:ai|課:bài, phòng ban|調:điều chỉnh, tra cứu|談:nói chuyện|議:bàn bạc|豆:đậu|貝:vỏ sò|財:của cải|販:bán|買:mua|資:tiền vốn, tư liệu|赤:đỏ|趣:thú vị, sở thích|転:quay, lăn|軽:nhẹ|輩:bạn bè, lứa|輪:vòng, bánh xe|辛:cay, cực khổ|辞:từ bỏ, lời|迷:lạc, phân vân|週:tuần|遅:muộn|遊:chơi|運:vận chuyển, vận may|過:quá, đi qua|道:đường|達:đạt, tới|部:bộ phận|郵:bưu điện|郷:quê|配:phân phát, lo lắng|酒:rượu|野:đồng nội|鉄:sắt|銀:bạc|銭:tiền xu|鍵:chìa khóa|閉:đóng|開:mở|除:trừ, bỏ|陽:mặt trời|隣:hàng xóm|雑:lẫn lộn|難:khó|雲:mây|青:xanh|静:yên tĩnh|靴:giày|韓:Hàn Quốc|頑:cứng đầu, ngoan cố|頭:đầu|題:đề|顔:mặt|類:loại|風:gió|飛:bay|飯:cơm|飲:uống|飴:kẹo|館:nhà, quán|験:thử nghiệm|髪:tóc|魚:cá|鳥:chim|黄:vàng|黒:đen|鼻:mũi"""
meaning = {}
for o in json.load(open(os.path.join(ROOT, 'source/n5-extras/kanji-n5.json'), encoding='utf8')):
    if o.get('m'):
        meaning[o['k']] = o['m']
for c, e in zh['chars'].items():
    if e.get('m') and c not in meaning:
        meaning[c] = e['m']
for p_ in MEAN.split('|'):
    c, m = p_.split(':', 1)
    if c not in meaning:
        meaning[c] = m
ja['hv'] = hv
ja['hvm'] = {c: meaning[c] for c in hv if c in meaning}
json.dump(ja, open(os.path.join(ROOT, 'data/ja.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))

plain = lambda s: re.sub(r'\{[^}]*\}', '', s)
need = {c for t in ja['topics'] for v in t['vocab'] for c in plain(v['w']) if '一' <= c <= '鿿'}
miss = sorted(c for c in need if c not in hv)
words = [v for t in ja['topics'] for v in t['vocab'] if any('一' <= c <= '鿿' for c in plain(v['w']))]
full = [v for v in words if all(c in hv for c in plain(v['w']) if '一' <= c <= '鿿')]
print('nghĩa từng chữ cho', len(ja['hvm']), 'chữ; thiếu nghĩa:', ''.join(c for c in hv if c not in ja['hvm']), '|', 'Hán Việt cho', len(hv), 'chữ; từ tiếng Nhật có chữ Hán', len(words), '| đủ Hán Việt', len(full), '| chữ còn thiếu', ''.join(miss))
