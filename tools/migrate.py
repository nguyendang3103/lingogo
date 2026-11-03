"""Gộp tiến độ của English Practice và Chinese Practice thành tài liệu tiến độ của NóiĐược."""
import json, os, sys, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda l: json.loads(json.load(open(os.path.join(ROOT, 'progress', l, 'data/users/me/progress.json')))['json'])
en_old, zh_old = load('en'), load('zh')
en = json.load(open(os.path.join(ROOT, 'out/data/en.json')))
zh = json.load(open(os.path.join(ROOT, 'out/data/zh.json')))

S = {'v': 2, 'name': '', 'goal': 20, 'lang': 'en', 'days': {}, 'srs': {}, 'lessons': {}, 'spoken': {}, 'written': {}, 'fill': {}, 'ach': {}, 't': 0}
for code, old in (('en', en_old), ('zh', zh_old)):
    for k, v in (old.get('srs') or {}).items():
        S['srs'][code + ':' + k] = {'b': v['b'], 'due': v['due'], 'last': v.get('last', -1)}
    for d, xp in (old.get('xpDay') or {}).items():
        S['days'][d] = S['days'].get(d, 0) + xp

def nlessons(size, t):
    return (len(t['vocab']) + size - 1) // size + 1

# Tiếng Anh: bài cũ n-d (d = 1..5) → bài mới d-1 cùng chủ đề (cả hai đều 4 bài học + 1 bài ôn)
days = en_old.get('days') or {}
for t in en['topics']:
    n = nlessons(5, t)
    for d in range(1, 6):
        if days.get(f"{t['id']}-{d}") and d - 1 < n:
            S['lessons'][f"en:{t['id']}-{d - 1}"] = 'cũ'
# Tiếng Trung: bài cũ T<id>-d (1..5); bài mới: 2 bài học + 1 bài ôn
zd = zh_old.get('days') or {}
if isinstance(zd, str):
    zd = json.loads(zd.replace("'", '"'))
mapping = {0: [1, 2], 1: [3], 2: [5, 4]}
for t in zh['topics']:
    for new_i, olds in mapping.items():
        if any((zd.get(f"T{t['id']}-{o}") or 0) >= 2 for o in olds):
            S['lessons'][f"zh:{t['id']}-{new_i}"] = 'cũ'
for k, v in (en_old.get('email') or {}).items():
    S['fill']['en:' + k.split('-')[0]] = v
S['t'] = int(time.time() * 1000)
json.dump({'json': json.dumps(S, ensure_ascii=False), 't': S['t']}, open(os.path.join(ROOT, 'progress', 'merged.json'), 'w'), ensure_ascii=False)
print('srs', len(S['srs']), 'days', S['days'], 'lessons', S['lessons'], 'fill', S['fill'])
