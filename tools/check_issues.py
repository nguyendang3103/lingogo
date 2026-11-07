#!/usr/bin/env python3
"""
tools/check_issues.py - Kiểm tra danh sách báo lỗi và góp ý từ người dùng trên GitHub.
Sử dụng:
  python tools/check_issues.py
"""

import sys
import json
import urllib.request
import urllib.error

# Ensure UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

REPO = 'nguyendang3103/lingogo'
URL = f'https://api.github.com/repos/{REPO}/issues?state=open&sort=created&direction=desc'

def main():
    req = urllib.request.Request(
        URL,
        headers={
            'User-Agent': 'Lingogo-Issue-Checker/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        print(f"Lỗi khi kết nối GitHub API: {e.code} {e.reason}", file=sys.stderr)
        return
    except Exception as e:
        print(f"Lỗi: {e}", file=sys.stderr)
        return

    # Filter out pull requests
    issues = [it for it in data if 'pull_request' not in it]

    if not issues:
        print(">> Hien tai khong co bao loi hay gop y nao dang mo tren GitHub (0 issues).")
        return

    print(f">> Tim thay {len(issues)} gop y / bao loi dang mo:")
    print("=" * 60)
    for issue in issues:
        num = issue.get('number')
        title = issue.get('title')
        user = issue.get('user', {}).get('login', 'An danh')
        created_at = issue.get('created_at')
        body = issue.get('body', '').strip()
        url = issue.get('html_url')

        print(f"\n[Issue #{num}] {title}")
        print(f"   Nguoi gui: @{user} | Thoi gian: {created_at}")
        print(f"   Link: {url}")
        print("   --- Noi dung ---")
        for line in body.split('\n'):
            print(f"   {line}")
        print("-" * 60)

if __name__ == '__main__':
    main()
