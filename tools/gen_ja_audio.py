"""Tạo âm thanh thu sẵn cho tiếng Nhật bằng Open JTalk (pyopenjtalk-plus, chạy offline).

Mọi câu chữ app có thể đọc (từ vựng, câu mẫu, ví dụ kanji, ví dụ ngữ pháp, kana) được tổng hợp
từ CÁCH ĐỌC đã có trong dữ liệu (kana / furigana), để tránh máy đọc sai âm kanji.
Đầu ra: audio/ja-<bài>.json (base64 MP3) và trường "audio" trong data/ja.json.

Cài: pip install pyopenjtalk-plus   (cần ffmpeg)
Chạy: python tools/gen_ja_audio.py <thư mục dữ liệu đã dựng> <ja-data.json gốc>
"""
import base64, json, os, re, subprocess, sys, tempfile, wave
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pyopenjtalk

OUT = sys.argv[1] if len(sys.argv) > 1 else 'out'
SRC = sys.argv[2] if len(sys.argv) > 2 else 'data/ja-data.json'
plain = lambda s: re.sub(r'\{[^}]*\}', '', s)
furigana = lambda raw: re.sub(r'[㐀-鿿々]+\{([^}]+)\}', r'\1', raw)


def collect():
    j = json.load(open(os.path.join(OUT, 'data/ja.json'), encoding='utf8'))
    gram = json.load(open(SRC, encoding='utf8'))['gram']
    items = {}  # chữ hiển thị → (cách đọc, gói)

    def add(text, reading, bundle):
        text = text.strip()
        if text and text not in items:
            items[text] = (reading.replace('　', '').strip() or text, bundle)

    for t in j['topics']:
        b = t['id']
        for v in t['vocab']:
            add(v['w'], re.split(r'[/／]', v['r'])[0].replace(' ', '').replace('～', ''), b)
        for s in t['sents']:
            add(''.join(s['chunks']), furigana(s['raw']), b)
        for k in t.get('kanji', []):
            add(k['k'], k['k'], b)
            for e in k.get('ex', []):
                add(plain(e[0]), furigana(e[0]), b)
    for ch, lines in gram.items():
        for ln in lines:
            s = ln.strip()
            if re.match(r'^[①-⑳]|^[AB][：:]', s):
                raw = re.sub(r'^[①-⑳]\s*|^[AB][：:]\s*', '', s)
                add(plain(raw), furigana(raw), ch)
    for c in 'あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをん':
        add(c, c, 'kana')
        add(chr(ord(c) + 96), chr(ord(c) + 96), 'kana')
    return j, items


def synth(args):
    text, reading = args
    x, sr = np.zeros(0), 48000
    for src in (reading, text):
        try:
            x, sr = pyopenjtalk.tts(src)
        except Exception:
            continue
        if len(x):
            break
    x = np.asarray(x, dtype=np.float64)
    if not len(x):
        return text, None  # không đọc được (ví dụ chỉ có ký hiệu): app dùng giọng máy

    peak = np.abs(x).max() or 1.0
    x = (x / peak * 0.89 * 32767).astype('<i2')  # chuẩn hóa, không bị vỡ tiếng
    pad = np.zeros(int(sr * 0.08), dtype='<i2')
    x = np.concatenate([pad, x, pad])
    with tempfile.TemporaryDirectory() as d:
        wav, mp3 = os.path.join(d, 'a.wav'), os.path.join(d, 'a.mp3')
        with wave.open(wav, 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes(x.tobytes())
        subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-ac', '1', '-ar', '24000', '-b:a', '40k', mp3], check=True)
        return text, base64.b64encode(open(mp3, 'rb').read()).decode()


if __name__ == '__main__':
    j, items = collect()
    with ProcessPoolExecutor() as ex:
        clips = {t: c for t, c in ex.map(synth, [(t, r) for t, (r, _) in items.items()], chunksize=16) if c}
    items = {t: v for t, v in items.items() if t in clips}
    bundles = {}
    for t, (_, b) in items.items():
        bundles.setdefault(b, {})[t] = clips[t]
    os.makedirs(os.path.join(OUT, 'audio'), exist_ok=True)
    total = 0
    for b, m in bundles.items():
        p = os.path.join(OUT, 'audio', f'ja-{b}.json')
        json.dump(m, open(p, 'w'), separators=(',', ':'))
        total += os.path.getsize(p)
    j['audio'] = {t: b for t, (_, b) in items.items()}
    j['audioKind'] = 'bundle'
    json.dump(j, open(os.path.join(OUT, 'data/ja.json'), 'w', encoding='utf8'), ensure_ascii=False, separators=(',', ':'))
    print(len(items), 'clips in', len(bundles), 'bundles,', total, 'bytes')
