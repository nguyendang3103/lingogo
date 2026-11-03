"""Chuẩn hóa dữ liệu ba app cũ (Anh, Trung, Nhật) về một định dạng chung cho NóiĐược.

Chạy từ thư mục Lingogo:
  node tools/extract_zh.js source/old-apps/chinese-practice.html source   (một lần, tạo zh-audio/zh-strokes)
  python tools/build.py
Đầu ra (thư mục build/) — chép build/data và build/audio đè lên data/ và audio/ khi muốn cập nhật app.
  data/en.json, data/zh.json, data/ja.json  — chủ đề, từ vựng, trắc nghiệm, câu nói, điền từ, ngữ pháp
  data/strokes-zh.json, data/strokes-ja.json — dữ liệu nét chữ cho phần Viết (định dạng Make Me a Hanzi)
  audio/zh-<n>.json                          — âm thanh thu sẵn tiếng Trung, tách theo gói
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DATA, OUT = (os.path.join(ROOT, p) for p in ('source/old-apps', 'source', 'build'))
os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
os.makedirs(os.path.join(OUT, 'audio'), exist_ok=True)


def dump(path, obj):
    with open(os.path.join(OUT, path), 'w', encoding='utf8') as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))
    return os.path.getsize(os.path.join(OUT, path))


def fill_ok(text):
    """'[[đúng|sai|sai]]' → câu đúng, dùng để kiểm tra dữ liệu."""
    return re.sub(r'\[\[([^|\]]+)[^\]]*\]\]', r'\1', text)


# ---------------- Tiếng Anh ----------------
lines = open(os.path.join(SRC, 'english-practice.html'), encoding='utf8').read().split('\n')
raw = next(l for l in lines if l.startswith('<script type="application/json" id="data">'))
EN = json.loads(re.sub(r'^.*?>', '', raw, count=1).rsplit('</script>', 1)[0])
en_topics = []
for pos, w in enumerate([w for w in EN['weeks'] if not w.get('mix')], 1):
    n = w['n']
    en_topics.append({
        'id': str(n), 'pos': pos, 'title': w['en'], 'sub': w.get('vi') or '', 'phase': w.get('ph') or '',
        'vocab': [{'id': v['id'], 'w': v['en'], 'r': '', 'm': v.get('vn') or v.get('vi'), 'd': v.get('vi') if v.get('vn') else '',
                   'ex': v.get('ex') or '', 'exr': '', 'exm': ''} for v in w['vocab']],
        'quiz': [{'id': q.get('id') or f'q{n}-{i}', 'q': q['s'], 'o': q['o'], 'a': 0, 'why': q.get('why') or ''} for i, q in enumerate(w['quiz'])],
        'speak': [{'id': s.get('id') or f's{n}-{i}', 'title': s['s'], 'lines': [{'t': t, 'r': '', 'm': ''} for t in s['l']]} for i, s in enumerate(w['speak'])],
        'coach': [{'id': c.get('id') or f'c{n}-{i}', 'q': c['q'], 'vi': c.get('vi') or '', 'st': c.get('st') or '', 'ph': c.get('ph') or [],
                   'sa': c.get('sa') or '', 'ss': c.get('ss') or [], 'sc': c.get('sc') or ''} for i, c in enumerate(w.get('coach') or [])],
        'fill': {'text': w['email'], 'trans': ''} if w.get('email') else None,
        'gram': [],
    })
# Lộ trình tiếng Anh tập trung tiếng Anh thương mại (không còn chủ đề A1 quán cà phê)
for i, t in enumerate(en_topics):
    t['pos'] = i + 1
en = {'code': 'en', 'name': 'Tiếng Anh', 'tts': 'en-US', 'size': 5, 'topics': en_topics, 'audio': EN['audio'], 'audioKind': 'bundle'}
print('en', len(en_topics), 'topics', sum(len(t['vocab']) for t in en_topics), 'words', dump('data/en.json', en), 'bytes')

# ---------------- Tiếng Trung ----------------
Z = json.load(open(os.path.join(DATA, 'zh-data.json'), encoding='utf8'))
grammar = {g['id']: {'t': g['vi'], 'zh': g['zh'], 'f': g.get('f') or '', 'notes': [g['n'][0]] if g.get('n') else [],
                     'ex': [[e[0], e[1], e[2]] for e in g.get('ex', [])]} for g in Z['GR']}
zh_topics = []
for x in [w for w in Z['W'] if not w.get('mix')]:
    src = x['src'][0] if isinstance(x['src'], list) else x['src']
    gid = Z['GMAP'].get(str(src))
    zh_topics.append({
        'id': str(x['id']), 'pos': len(zh_topics) + 1, 'title': x['t'], 'sub': x['tv'], 'phase': x.get('lv') or x.get('ph') or '',
        'vocab': [{'id': v['id'], 'w': v['zh'], 'r': v['py'], 'm': v['vi'], 'd': '', 'ex': v.get('ex') or '', 'exr': v.get('exp') or '',
                   'exm': v.get('exv') or ''} for v in x['vocab']],
        'quiz': [{'id': q['id'], 'q': q['s'], 'o': q['o'], 'a': q['o'].index(q['ok']) if q.get('ok') in q['o'] else 0, 'why': q.get('why') or ''}
                 for q in x['quiz']],
        'speak': [{'id': s['id'], 'title': s['s'], 'lines': [{'t': l['zh'], 'r': l.get('py') or '', 'm': l.get('vi') or ''} for l in s['l']]}
                  for s in x['speak']],
        'coach': [],
        'fill': {'text': x['f'], 'trans': x.get('fv') or ''} if x.get('f') else None,
        'gram': [gid] if gid and gid in grammar else [],
    })
# Thông tin chữ Hán: âm Hán Việt và nghĩa, dùng trong phần Viết
chars = {c: {'hv': Z['HV'].get(c, ''), 'm': (Z['CH'].get(c) or {}).get('v', ''), 'rad': (Z['CH'].get(c) or {}).get('r', '')}
         for c in set(Z['HV']) | set(Z['CH'])}
zh = {'code': 'zh', 'name': 'Tiếng Trung', 'tts': 'zh-CN', 'size': 4, 'topics': zh_topics, 'grammar': grammar, 'chars': chars,
      'audio': Z['AU'], 'audioKind': 'zh'}
print('zh', len(zh_topics), 'topics', sum(len(t['vocab']) for t in zh_topics), 'words', dump('data/zh.json', zh), 'bytes')

audio = json.load(open(os.path.join(DATA, 'zh-audio.json'), encoding='utf8'))
tot = 0
for b, clips in audio.items():
    tot += dump(f'audio/zh-{b}.json', clips)
print('zh audio', len(audio), 'files', tot, 'bytes')

strokes = json.load(open(os.path.join(DATA, 'zh-strokes.json'), encoding='utf8'))
print('zh strokes', len(strokes), dump('data/strokes-zh.json', {c: {'strokes': s['strokes'], 'medians': s['medians']} for c, s in strokes.items()}))

# ---------------- Tiếng Nhật ----------------
J = json.load(open(os.path.join(DATA, 'ja-data.json'), encoding='utf8'))
PART = ['は', 'が', 'を', 'に', 'で', 'の', 'も', 'と', 'へ']
plain = lambda s: re.sub(r'\{[^}]*\}', '', s)


def clean_word(w):
    w = w.strip()
    return w.replace(' ', '') if re.search(r'[぀-鿿]', w) else w


# Ngữ pháp mỗi chương là danh sách dòng chữ (trích từ giáo trình); giữ nguyên để hiển thị
gram_by_ch = {int(ch): [lines_] for ch, lines_ in J['gram'].items()}

ja_topics = []
seen = set()
for ch in range(1, 15):
    vocab = [v for v in J['vocab'] if v['ch'] == ch]
    sents = []
    for blocks in gram_by_ch.get(ch, []):
        for ln in blocks:
            m = re.match(r'^[①-⑳]\s*(.+)$', ln) or re.match(r'^[AB][：:]\s*(.+)$', ln)
            if not m:
                continue
            rawl = m.group(1).strip()
            pl = plain(rawl)
            if re.search(r'[→～・：:（）()\/／A-Za-z★、]', pl) or not pl.endswith('。') or pl.count('。') != 1 or rawl in seen:
                continue
            chunks = [c.strip() for c in re.split(r'　+', rawl) if c.strip()]
            if not 3 <= len(chunks) <= 8:
                continue
            seen.add(rawl)
            sents.append({'raw': rawl, 'chunks': [plain(c) for c in chunks]})
    gram = [{'lines': b} for b in gram_by_ch.get(ch, [])]
    kanji = [k for k in J['kanji'] if k['ch'] == ch]
    ja_topics.append({
        'id': str(ch), 'pos': ch, 'title': f'第{ch}課', 'sub': f'Bài {ch}', 'phase': 'Sơ cấp N5–N4',
        'vocab': [{'id': f'v{J["vocab"].index(v)}', 'w': clean_word(v['w']), 'r': v['r'].replace(' ', ''), 'm': v['m'], 'd': v.get('pos') or '',
                   'ex': '', 'exr': '', 'exm': ''} for v in vocab],
        'quiz': [], 'speak': [], 'coach': [], 'fill': None,
        'gram': gram, 'kanji': [{'id': f'k{J["kanji"].index(k)}', **k} for k in kanji], 'sents': sents,
    })
ja = {'code': 'ja', 'name': 'Tiếng Nhật', 'tts': 'ja-JP', 'size': 8, 'topics': ja_topics, 'audio': {}, 'audioKind': 'tts'}
print('ja', len(ja_topics), 'topics', sum(len(t['vocab']) for t in ja_topics), 'words',
      sum(len(t['sents']) for t in ja_topics), 'sentences', dump('data/ja.json', ja), 'bytes')

G = {}
for f in ('graphicsJa.txt', 'graphicsJaKana.txt'):
    for line in open(os.path.join(ROOT, 'vendor', f), encoding='utf8'):
        o = json.loads(line)
        G[o['character']] = o
need = set(''.join(k['k'] for k in J['kanji']))
need |= {chr(c) for c in range(0x3041, 0x3097)} | {chr(c) for c in range(0x30A1, 0x30FB)}
need |= {c for v in J['vocab'] for c in v['w'] if '぀' <= c <= '鿿'}
js = {c: {'strokes': G[c]['strokes'], 'medians': G[c]['medians']} for c in sorted(need) if c in G}
print('ja strokes', len(js), 'of', len(need), dump('data/strokes-ja.json', js))
