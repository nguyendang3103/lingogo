"""Thêm phần bổ sung N5 (28/10/2026) vào data/ja.json và data/strokes-ja.json.

Nguồn: thư mục Drive "日本語" của Sally, mục 01. JLPT N5:
  - 02. Kanji N5.xlsx  -> source/n5-extras/kanji-n5.json (bảng kanji theo 14 nhóm chủ đề, 103 chữ)
  - 03. Ngữ pháp - Các thì động từ tiếng Nhật.docx (12 thể của động từ, danh sách 17 động từ nhóm II đặc biệt)

Thêm hai chủ đề vào cuối lộ trình tiếng Nhật:
  15  Kanji N5 bổ sung   : kanji trong bảng mà app chưa có
  16  Thể của động từ    : ngữ pháp 12 thể (ví dụ sinh bằng code chia động từ), động từ nhóm II đặc biệt, câu mẫu

Chạy lại được nhiều lần (xoá hai chủ đề 15, 16 cũ rồi dựng lại). Sau khi chạy build.py thì chạy lại file này.
Chạy:  python tools/add_n5_extras.py   (từ thư mục Lingogo)
"""
import json, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rd = lambda p: json.load(open(os.path.join(ROOT, p), encoding='utf8'))
ja = rd('data/ja.json')
ja['topics'] = [t for t in ja['topics'] if t['pos'] < 15]  # bỏ bản cũ của chủ đề 15, 16 nếu đã chạy trước đó
kanji_xlsx = rd('source/n5-extras/kanji-n5.json')

# ---------- Chia động từ ----------
ROW = {'く': ('き', 'か', 'こ', 'け', 'い'), 'ぐ': ('ぎ', 'が', 'ご', 'げ', 'い'), 'す': ('し', 'さ', 'そ', 'せ', 's'),
       'つ': ('ち', 'た', 'と', 'て', 'っ'), 'ぬ': ('に', 'な', 'の', 'ね', 'ん'), 'ぶ': ('び', 'ば', 'ぼ', 'べ', 'ん'),
       'む': ('み', 'ま', 'も', 'め', 'ん'), 'る': ('り', 'ら', 'ろ', 'れ', 'っ'), 'う': ('い', 'わ', 'お', 'え', 'っ')}
# (thân chữ Hán, cách đọc thân, đuôi từ điển, nhóm, nghĩa tiếng Việt)
V = {
    'nomu': ('飲', 'の', 'む', 1, 'uống'), 'kaku': ('書', 'か', 'く', 1, 'viết'), 'hanasu': ('話', 'はな', 'す', 1, 'nói chuyện'),
    'matsu': ('待', 'ま', 'つ', 1, 'đợi'), 'kau': ('買', 'か', 'う', 1, 'mua'), 'oyogu': ('泳', 'およ', 'ぐ', 1, 'bơi'),
    'asobu': ('遊', 'あそ', 'ぶ', 1, 'chơi'), 'shinu': ('死', 'し', 'ぬ', 1, 'chết'), 'kaeru': ('帰', 'かえ', 'る', 1, 'về'),
    'iku': ('行', 'い', 'く', 1, 'đi'), 'toru': ('撮', 'と', 'る', 1, 'chụp'), 'yomu': ('読', 'よ', 'む', 1, 'đọc'),
    'taberu': ('食', 'た', 'べる', 2, 'ăn'), 'neru': ('寝', 'ね', 'る', 2, 'ngủ'), 'miru': ('見', 'み', 'る', 2, 'xem'),
    'okiru': ('起', 'お', 'きる', 2, 'thức dậy'),
    'suru': ('', '', 'する', 3, 'làm'), 'benkyou': ('勉強', 'べんきょう', 'する', 3, 'học'), 'kuru': ('来', 'く', 'る', 3, 'đến'),
}


def conj(key, form):
    stem, rd_, end, grp, _ = V[key]
    ruby = lambda r: (f'{stem}{{{r}}}' if stem else '')
    if grp == 3:
        if key == 'kuru':
            r = {'masu': 'き', 'neg': 'こ', 'te': 'き', 'vol': 'こ', 'imp': 'こ', 'pot': 'こ', 'caus': 'こ', 'pass': 'こ', 'cp': 'こ'}.get(form, 'く')
            tail = {'masu': 'ます', 'neg': 'ない', 'te': 'て', 'ta': 'た', 'vol': 'よう', 'imp': 'い', 'pot': 'られる', 'caus': 'させる', 'pass': 'られる', 'cp': 'させられる', 'dict': 'る', 'proh': 'るな'}[form]
            if form == 'ta': r = 'き'
            if form == 'imp': return f'{stem}{{こ}}い'
            if form == 'proh': return f'{stem}{{く}}るな'
            if form == 'dict': return f'{stem}{{く}}る'
            return f'{stem}{{{r}}}{tail}'
        pre = (f'{stem}{{{rd_}}}' if stem else '')
        tail = {'masu': 'します', 'neg': 'しない', 'te': 'して', 'ta': 'した', 'vol': 'しよう', 'imp': 'しろ', 'pot': 'できる', 'caus': 'させる', 'pass': 'される', 'cp': 'させられる', 'dict': 'する', 'proh': 'するな'}[form]
        return pre + tail
    base = ruby(rd_)
    if grp == 2:
        body = end[:-1]
        tail = {'masu': 'ます', 'neg': 'ない', 'te': 'て', 'ta': 'た', 'vol': 'よう', 'imp': 'ろ', 'pot': 'られる', 'caus': 'させる', 'pass': 'られる', 'cp': 'させられる', 'dict': 'る', 'proh': 'るな'}[form]
        return base + body + tail
    i, a, o, e, t = ROW[end]
    pre = base + end[:-1]  # không có phần okurigana trước đuôi với nhóm I (đuôi 1 chữ)
    if form == 'dict': return base + end
    if form == 'proh': return base + end + 'な'
    if form == 'masu': return base + i + 'ます'
    if form == 'neg': return base + a + 'ない'
    if form in ('te', 'ta'):
        suf = 'て' if form == 'te' else 'た'
        if key == 'iku': return base + 'っ' + suf
        if end == 'す': return base + 'し' + suf
        if end in 'うつる': return base + 'っ' + suf
        if end in 'むぶぬ': return base + 'ん' + ('で' if form == 'te' else 'だ')
        if end == 'く': return base + 'い' + suf
        if end == 'ぐ': return base + 'い' + ('で' if form == 'te' else 'だ')
    if form == 'vol': return base + o + 'う'
    if form == 'imp': return base + e
    if form == 'pot': return base + e + 'る'
    if form == 'caus': return base + a + 'せる'
    if form == 'pass': return base + a + 'れる'
    if form == 'cp': return base + (a + 'せられる' if end == 'す' else a + 'される')
    raise KeyError((key, form))


GL = {1: 'Nhóm I', 2: 'Nhóm II', 3: 'Nhóm III'}


def table(forms_from, form, keys, gloss):
    out = []
    for k in keys:
        m = V[k][4]
        out.append(f'{conj(k, forms_from)} → {conj(k, form)}　（{gloss.replace("V", m)}）')
    return out


def sec(n, title, rules, rows, ex, ex_vi):
    lines = [str(n), title] + rules + rows
    lines += [f'① {ex}', ex_vi]
    return lines


G = []
G.append(['Phân nhóm động từ',
          'Nhóm I: động từ có âm cột い đứng trước ます (ví dụ 飲{の}みます, 書{か}きます, 話{はな}します, 待{ま}ちます, 買{か}います).',
          'Nhóm II: động từ có âm cột え đứng trước ます (ví dụ 食{た}べます, 寝{ね}ます). Có 18 động từ đặc biệt trông giống nhóm I nhưng thuộc nhóm II (xem danh sách bên dưới).',
          'Nhóm III chỉ có: 来{き}ます (đến), します (làm) và N＋します (danh động từ, ví dụ 勉強{べんきょう}します).',
          'Lưu ý: N＋します ở nhóm III khác với ～します ở nhóm I (ví dụ 話{はな}します là nhóm I, chia 話{はな}さない).',
          'Động từ nhóm II đặc biệt: 起{お}きます, 見{み}ます, 診{み}ます, 借{か}ります, います, 降{お}ります, 浴{あ}びます, できます, 足{た}ります, 着{き}ます, 閉{と}じます, 煮{に}ます, 過{す}ぎます, 似{に}ています, 信{しん}じます, 存{ぞん}じます, 落{お}ちます, 生{い}きます.'])
spec = [
    (1, 'Thể lịch sự (ます)', ['Kết thúc bằng ます, dùng với mọi đối tượng: cấp trên, khách hàng, bạn bè, đồng nghiệp, người mới gặp. Chỉ cần học thuộc; về sau có thể chia ngược từ các thể khác về thể ます.'],
     [], '毎朝{まいあさ}、コーヒーを飲{の}みます。', 'Mỗi sáng tôi uống cà phê.'),
    (2, 'Thể từ điển (Vる)', ['Chia từ thể ます: nhóm I đổi âm cột い trước ます sang cột う; nhóm II bỏ ます thêm る; します → する; 来{き}ます → 来{く}る.'],
     ('masu', 'dict', ['nomu', 'hanasu', 'taberu', 'suru', 'kuru'], 'V'), '私{わたし}は日本語{にほんご}を勉強{べんきょう}する。', 'Tôi học tiếng Nhật.'),
    (3, 'Thể phủ định (Vない)', ['Nhóm I: âm cột い trước ます đổi sang cột あ rồi thêm ない; riêng ～います → ～わない.', 'Nhóm II: bỏ ます thêm ない. Nhóm III: します → しない, 来{き}ます → 来{こ}ない.'],
     ('masu', 'neg', ['nomu', 'iku', 'kau', 'taberu', 'suru', 'kuru'], 'không V'), '今日{きょう}はお酒{さけ}を飲{の}まない。', 'Hôm nay tôi không uống rượu.'),
    (4, 'Thể て (Vて)', ['Dùng trong rất nhiều mẫu ngữ pháp từ N5 lên N1. Nhóm I theo đuôi: い, ち, り → って; み, に, び → んで; き → いて, ぎ → いで; し → して. Ngoại lệ: 行{い}きます → 行{い}って.', 'Nhóm II: bỏ ます thêm て. Nhóm III: します → して, 来{き}ます → 来{き}て.'],
     ('masu', 'te', ['kau', 'matsu', 'kaeru', 'nomu', 'asobu', 'shinu', 'kaku', 'iku', 'oyogu', 'hanasu', 'taberu', 'suru', 'kuru'], 'thể て của V'), '窓{まど}を開{あ}けて、掃除{そうじ}をします。', 'Mở cửa sổ rồi dọn dẹp.'),
    (5, 'Thể quá khứ (Vた)', ['Ngắn hơn ました; chia giống thể て (て → た, で → だ).'],
     ('masu', 'ta', ['kau', 'nomu', 'kaku', 'iku', 'hanasu', 'taberu', 'suru', 'kuru'], 'đã V'), '昨日{きのう}、友達{ともだち}と映画{えいが}を見{み}た。', 'Hôm qua tôi đã xem phim với bạn.'),
    (6, 'Thể ý chí (Vよう)', ['Diễn đạt ý muốn làm, dùng khi mời, rủ rê. Lịch sự hơn là ～ましょう.', 'Nhóm I: âm cột い trước ます đổi sang cột お rồi thêm う. Nhóm II: bỏ ます thêm よう. Nhóm III: します → しよう, 来{き}ます → 来{こ}よう.'],
     ('masu', 'vol', ['nomu', 'iku', 'hanasu', 'taberu', 'suru', 'kuru'], 'V thôi'), '一緒{いっしょ}に昼{ひる}ご飯{はん}を食{た}べよう。', 'Cùng ăn trưa nhé.'),
    (7, 'Thể mệnh lệnh', ['Ra lệnh, sai khiến; chỉ dùng khi khẩn cấp, quân đội, bố mẹ với con, hoặc khi cực kỳ tức giận. Không dùng với người bình thường vì dễ bị coi là thô lỗ.', 'Nhóm I: âm cột い trước ます đổi sang cột え. Nhóm II: bỏ ます thêm ろ. Nhóm III: しろ, 来{こ}い.'],
     ('masu', 'imp', ['nomu', 'iku', 'taberu', 'suru', 'kuru'], 'V đi!'), '早{はや}く起{お}きろ！', 'Dậy nhanh lên!'),
    (8, 'Thể cấm chỉ (Vるな)', ['Mệnh lệnh phủ định, hay gặp trên biển báo cảnh báo. Thể từ điển ＋ な: cấm, không được làm.'],
     ('dict', 'proh', ['taberu', 'toru', 'iku', 'suru'], 'cấm V'), 'ここで写真{しゃしん}を撮{と}るな。', 'Cấm chụp ảnh ở đây.'),
    (9, 'Thể khả năng', ['Diễn đạt năng lực, khả năng làm việc gì. Nhóm I: âm cột い trước ます đổi sang cột え rồi thêm る. Nhóm II: bỏ ます thêm られる. Nhóm III: します → できる, 来{き}ます → 来{こ}られる.', 'Lưu ý: 見{み}えます, 聞{き}こえます, わかります, 知{し}っています đã mang nghĩa khả năng nên không chia. います, あります không chia sang thể khả năng.'],
     ('masu', 'pot', ['yomu', 'nomu', 'taberu', 'suru', 'kuru'], 'có thể V'), '私{わたし}は漢字{かんじ}が読{よ}める。', 'Tôi đọc được chữ Hán.'),
    (10, 'Thể sai khiến', ['Cho phép hoặc bắt ép người khác làm gì. Nhóm I: âm cột い trước ます đổi sang cột あ rồi thêm せる (～います → ～わせる). Nhóm II: bỏ ます thêm させる. Nhóm III: します → させる, 来{き}ます → 来{こ}させる.'],
     ('masu', 'caus', ['kaku', 'nomu', 'taberu', 'suru', 'kuru'], 'cho phép/bắt V'), '先生{せんせい}は学生{がくせい}に漢字{かんじ}を書{か}かせた。', 'Thầy cho/bắt học sinh viết chữ Hán.'),
    (11, 'Thể bị động', ['Diễn tả đối tượng chịu tác động của người khác. Hành động tích cực dịch là "được", tiêu cực dịch là "bị". Nhóm I: âm cột い trước ます đổi sang cột あ rồi thêm れる (～います → ～われる). Nhóm II: bỏ ます thêm られる. Nhóm III: します → される, 来{き}ます → 来{こ}られる.'],
     ('masu', 'pass', ['yomu', 'taberu', 'suru', 'kuru'], 'được/bị V'), '子供{こども}は先生{せんせい}にほめられた。', 'Đứa trẻ được thầy khen.'),
    (12, 'Thể sai khiến bị động', ['Dịch là "bị bắt", dùng khi ai đó bị người khác bắt phải làm gì. Nhóm I: âm cột い trước ます đổi sang cột あ rồi thêm される (cách 1) hoặc せられる (cách 2). Riêng nhóm I đuôi ～す chỉ dùng cách 2: 話{はな}す → 話{はな}させられる.', 'Nhóm II: bỏ ます thêm させられる. Nhóm III: します → させられる, 来{き}ます → 来{こ}させられる.'],
     ('masu', 'cp', ['kaku', 'hanasu', 'taberu', 'suru', 'kuru'], 'bị bắt V'), '私{わたし}は毎日{まいにち}野菜{やさい}を食{た}べさせられる。', 'Hằng ngày tôi bị bắt ăn rau.'),
]
for n, title, rules, tb, ex, exv in spec:
    rows = table(*tb) if tb else [f'{conj(k, "masu")}　（{V[k][4]}）' for k in ('nomu', 'taberu', 'suru', 'kuru')]
    # bảng thể ます: không có phần "→"
    G.append(sec(n, title, rules, rows, ex, exv))

SENTS = ['毎朝{まいあさ}、　コーヒーを　飲{の}みます。', '私{わたし}は　日本語{にほんご}を　勉強{べんきょう}する。', '今日{きょう}は　お酒{さけ}を　飲{の}まない。',
         '窓{まど}を　開{あ}けて、　掃除{そうじ}を　します。', '昨日{きのう}、　友達{ともだち}と　映画{えいが}を　見{み}た。', '一緒{いっしょ}に　昼{ひる}ご飯{はん}を　食{た}べよう。',
         '早{はや}く　起{お}きろ！', 'ここで　写真{しゃしん}を　撮{と}るな。', '私{わたし}は　漢字{かんじ}が　読{よ}める。', '先生{せんせい}は　学生{がくせい}に　漢字{かんじ}を　書{か}かせた。',
         '子供{こども}は　先生{せんせい}に　ほめられた。', '私{わたし}は　毎日{まいにち}　野菜{やさい}を　食{た}べさせられる。']
plain = lambda s: re.sub(r'\{[^}]*\}', '', s)
sents = []
for s in SENTS:
    ch = [plain(c) for c in re.split(r'　+', s) if c.strip()]
    if 3 <= len(ch) <= 8 and ch[-1].endswith(('。', '！')):
        sents.append({'raw': s, 'chunks': ch})

# ---------- Từ vựng: 17 động từ nhóm II đặc biệt (bỏ từ đã có trong app) ----------
SPECIAL = [('見ます', 'みます', 'xem'), ('診ます', 'みます', 'khám (bệnh)'), ('借ります', 'かります', 'vay, mượn'), ('降ります', 'おります', 'xuống (xe)'),
           ('できます', 'できます', 'có thể'), ('着ます', 'きます', 'mặc'), ('閉じます', 'とじます', 'đóng, nhắm'), ('煮ます', 'にます', 'nấu'),
           ('過ぎます', 'すぎます', 'quá'), ('似ています', 'にています', 'giống'), ('信じます', 'しんじます', 'tin tưởng'),
           ('存じます', 'ぞんじます', 'biết (khiêm nhường)'), ('生きます', 'いきます', 'sống')]
have_w = {v['w'] for t in ja['topics'] for v in t['vocab']}
nv = max(int(v['id'][1:]) for t in ja['topics'] for v in t['vocab']) + 1
vocab = []
for w, r, m in SPECIAL:
    if w in have_w:
        continue
    vocab.append({'id': f'v{nv}', 'w': w, 'r': r, 'm': m, 'd': 'V nhóm II đặc biệt', 'ex': '', 'exr': '', 'exm': ''})
    nv += 1

# ---------- Kanji bổ sung ----------
have_k = {k['k'] for t in ja['topics'] for k in t['kanji'] if t['pos'] < 15}
EX = {'天': [['天{てん}気{き}', 'thời tiết']], '姉': [['お姉{ねえ}さん', 'chị gái (người khác)'], ['姉{あね}', 'chị gái (mình)']],
      '私': [['私{わたし}', 'tôi']], '弟': [['弟{おとうと}', 'em trai (mình)']], '妹': [['妹{いもうと}', 'em gái (mình)']],
      '力': [['力{ちから}', 'sức mạnh']], '岩': [['岩{いわ}', 'tảng đá']], '畑': [['畑{はたけ}', 'ruộng, vườn']],
      '駅': [['駅{えき}', 'ga'], ['東京駅{とうきょうえき}', 'ga Tokyo']], '名': [['名前{なまえ}', 'tên']],
      '国': [['国{くに}', 'đất nước'], ['中国{ちゅうごく}', 'Trung Quốc']]}
kid = max(int(k['id'][1:]) for t in ja['topics'] for k in t['kanji']) + 1
kanji = []
for o in kanji_xlsx:
    if o['k'] in have_k:
        continue
    kanji.append({'id': f'k{kid}', 'ch': 15, 'k': o['k'], 'hv': o['hv'], 'kun': o['kun'], 'on': o['on'], 'ex': EX.get(o['k'], [])})
    kid += 1

topics = [t for t in ja['topics'] if t['pos'] < 15]
topics.append({'id': '15', 'pos': 15, 'title': 'Kanji N5', 'sub': 'Kanji bổ sung', 'phase': 'Sơ cấp N5–N4', 'vocab': [], 'quiz': [], 'speak': [], 'coach': [], 'fill': None,
               'gram': [], 'kanji': kanji, 'sents': []})
topics.append({'id': '16', 'pos': 16, 'title': '動詞の形', 'sub': 'Thể của động từ', 'phase': 'Sơ cấp N5–N4', 'vocab': vocab, 'quiz': [], 'speak': [], 'coach': [], 'fill': None,
               'gram': [{'lines': g} for g in G], 'kanji': [], 'sents': sents})
ja['topics'] = topics
json.dump(ja, open(os.path.join(ROOT, 'data/ja.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))

# ---------- Nét chữ ----------
sp_path = os.path.join(ROOT, 'data/strokes-ja.json')
js = json.load(open(sp_path, encoding='utf8'))
gmap = {}
for f in ('graphicsJa.txt', 'graphicsJaKana.txt'):
    for line in open(os.path.join(ROOT, 'vendor', f), encoding='utf8'):
        o = json.loads(line); gmap[o['character']] = o
need = {c for k in kanji for c in k['k']} | {c for v in vocab for c in v['w'] if '぀' <= c <= '鿿'}
added = [c for c in sorted(need) if c not in js and c in gmap]
for c in added:
    js[c] = {'strokes': gmap[c]['strokes'], 'medians': gmap[c]['medians']}
json.dump(js, open(sp_path, 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
print('kanji mới', len(kanji), '| từ vựng mới', len(vocab), '| mẫu ngữ pháp', len(G), '| câu mẫu', len(sents), '| nét chữ thêm', len(added), 'chữ; thiếu nét:', [c for c in need if c not in js])
