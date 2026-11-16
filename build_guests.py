#!/usr/bin/env python3
"""Dựng trang thiệp riêng cho từng khách nhà gái từ index.html + file Excel danh sách.

  python3 build_guests.py "/đường/dẫn/Cưới.xlsx"

Kết quả:
  gai/index.html            -> link chung nhà gái:  .../thiep-cuoi/gai/
  gai/<ten-khach>/index.html -> link riêng:          .../thiep-cuoi/gai/anh-hung/
Cập nhật cột link trong sheet "Link mời nhà gái" của file Excel.
Mỗi lần sửa index.html hoặc danh sách khách, chạy lại script rồi commit + push.
"""
import re, sys, shutil, unicodedata, html
from pathlib import Path
import openpyxl
from openpyxl.styles import Font

ROOT = Path(__file__).resolve().parent
BASE_URL = 'https://doanhdd0210.github.io/thiep-cuoi/'
SHEET = 'Link mời nhà gái'

def slugify(t):
    t = t.replace('đ', 'd').replace('Đ', 'D')
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', t.lower()).strip('-') or 'khach'

def render(tpl, rel, guest, url):
    h = tpl
    h = h.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<base href="%s">' % rel, 1)
    pre = '<script>window.THIEP=%s;</script>\n<script>\n(function' % ('{side:"gai"' + (',guest:%s' % __import__('json').dumps(guest, ensure_ascii=False) if guest else '') + '}')
    assert '<script>\n(function' in h
    h = h.replace('<script>\n(function', pre, 1)
    title = 'Thiệp mời Lễ Vu Quy · Huyền Trang &amp; Đức Doanh'
    if guest: title = 'Thiệp mời %s &amp; người thương · Huyền Trang &amp; Đức Doanh' % html.escape(guest)
    h = re.sub(r'<title>.*?</title>', '<title>%s</title>' % title, h, 1)
    h = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\g<1>' + title, h, 1)
    h = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\g<1>Lễ Vu Quy · 13 giờ 30 · 29.11.2026 · Ninh Bình', h, 1)
    h = re.sub(r'(<meta name="description" content=")[^"]*', r'\g<1>Trân trọng kính mời bạn đến dự Lễ Vu Quy của Huyền Trang &amp; Đức Doanh — 13 giờ 30, 29.11.2026, Ninh Bình.', h, 1)
    h = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\g<1>' + url, h, 1)
    return h

def main(xlsx):
    tpl = (ROOT / 'index.html').read_text(encoding='utf-8')
    gai = ROOT / 'gai'
    for d in gai.iterdir():                      # dọn trang khách cũ
        if d.is_dir(): shutil.rmtree(d)
    (gai / 'index.html').write_text(render(tpl, '../', '', BASE_URL + 'gai/'), encoding='utf-8')
    wb = openpyxl.load_workbook(xlsx); ws = wb[SHEET]
    used = {}; n = 0
    for r in range(2, ws.max_row + 1):
        name = ws.cell(r, 4).value
        if not name: continue
        slug = slugify(name); used[slug] = used.get(slug, 0) + 1
        if used[slug] > 1: slug += '-%d' % used[slug]
        url = BASE_URL + 'gai/%s/' % slug
        d = gai / slug; d.mkdir()
        (d / 'index.html').write_text(render(tpl, '../../', name, url), encoding='utf-8')
        c = ws.cell(r, 6); c.value = url; c.hyperlink = url; c.font = Font(color='0563C1', underline='single')
        n += 1
    i = 2                                         # gắn link vào tên ở sheet gốc (cùng thứ tự: theo cột rồi theo dòng)
    src = wb.worksheets[0]
    for c in range(1, src.max_column + 1):
        for r in range(2, src.max_row + 1):
            v = src.cell(r, c).value
            if v is None or not str(v).strip(): continue
            src.cell(r, c).hyperlink = ws.cell(i, 6).value; i += 1
    wb.save(xlsx)
    print('Đã dựng %d trang khách + trang chung nhà gái' % n)

if __name__ == '__main__':
    main(sys.argv[1])
