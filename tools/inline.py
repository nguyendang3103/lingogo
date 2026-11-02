#!/usr/bin/env python3
"""Tạo bản index.html có nhúng sẵn dữ liệu bài học và nét chữ (dùng cho artifact trên Claude).

Vì sao cần: trên iPad (ứng dụng Claude) việc tải thêm file riêng như data/en.json có thể bị chặn (lỗi 403),
nên bài học không mở được. Bản này đưa các file dữ liệu vào chính trang HTML; index.html (getJSON) đọc bản nhúng
trước, không có thì tải qua mạng như thường. Âm thanh (audio/, ~88 MB) quá lớn để nhúng, nên vẫn tải qua mạng;
nếu không tải được thì app tự dùng giọng đọc của máy.

Dùng:  python3 tools/inline.py OUTPUT_HTML      (chạy từ thư mục gốc của repo)
"""
import json, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = ['data/en.json', 'data/zh.json', 'data/ja.json', 'data/strokes-zh.json', 'data/strokes-ja.json']
MARK = '<script src="https://cdn.jsdelivr.net/npm/hanzi-writer'

def block(rel):
    data = json.loads((ROOT / rel).read_text(encoding='utf-8'))
    text = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    text = text.replace('<', '\\u003c')  # '<' chỉ nằm trong chuỗi JSON nên thay bằng < là an toàn, tránh đóng thẻ script sớm
    return '<script type="application/json" data-file="%s">%s</script>\n' % (rel, text)

def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    if html.count(MARK) != 1:
        sys.exit('Không tìm thấy đúng một chỗ để chèn dữ liệu (%r)' % MARK)
    inline = ''.join(block(f) for f in FILES)
    out = html.replace(MARK, inline + MARK)
    pathlib.Path(sys.argv[1]).write_text(out, encoding='utf-8')
    print('đã ghi %s: %.2f MB (trang gốc %.2f MB + dữ liệu nhúng %.2f MB)' % (sys.argv[1], len(out.encode()) / 1048576, len(html.encode()) / 1048576, len(inline.encode()) / 1048576))

main()
