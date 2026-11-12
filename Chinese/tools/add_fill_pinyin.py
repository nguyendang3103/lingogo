"""Thêm phiên âm pinyin (fill.r) cho đoạn hội thoại điền từ tiếng Trung trong data/zh.json.
Phiên âm tính trên câu đã điền đáp án đúng (lựa chọn đầu tiên của mỗi [[...]]), mỗi dòng một dòng pinyin.
Cần: pip install pypinyin. Từ được ghép theo danh sách từ vựng của chính app (khớp dài nhất). Chạy lại được nhiều lần; chạy lại sau mỗi lần chạy build.py.
Chạy:  python tools/add_fill_pinyin.py   (từ thư mục Lingogo)
"""
import json, re
from pypinyin import pinyin, Style

P = 'data/zh.json'
d = json.load(open(P, encoding='utf-8'))
fix = lambda s: re.sub(r'([：:])\s+', r'\1 ', re.sub(r'\s+([，。？！：、；,.?!:;])', r'\1', s))
n = 0
WORDS = {re.sub(r'\{[^}]*\}', '', v['w']) for t in d['topics'] for v in t['vocab']}
WORDS = {w for w in WORDS if 2 <= len(w) <= 4}
def cut(line):  # khớp dài nhất theo từ vựng; chữ còn lại tách từng ký tự
    out, i = [], 0
    while i < len(line):
        for k in (4, 3, 2, 1):
            seg = line[i:i + k]
            if k == 1 or seg in WORDS:
                out.append(seg); i += k; break
    return out
def py(line):  # đọc cả câu để chọn đúng âm đa âm (高兴 gāoxìng), rồi ghép âm tiết theo từ
    syl = [x[0] for x in pinyin(line, style=Style.TONE, errors=lambda c: list(c))]
    assert len(syl) == len(line), line
    out, i = [], 0
    for w in cut(line):
        seg = ''.join(syl[i:i + len(w)]) if re.search(r'[\u4e00-\u9fff]', w) else w.strip()
        if seg:
            out.append(seg)
        i += len(w)
    return fix(' '.join(out))
for t in d['topics']:
    f = t.get('fill')
    if not f:
        continue
    full = re.sub(r'\[\[(.+?)\]\]', lambda m: m.group(1).split('|')[0], f['text'])
    f['r'] = '\n'.join(py(line) for line in full.split('\n'))
    n += 1
json.dump(d, open(P, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('Đã thêm pinyin cho', n, 'đoạn hội thoại')
