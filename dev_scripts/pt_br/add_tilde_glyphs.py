#!/usr/bin/env python3
"""Adds Portuguese tilde letters (ã õ Ã Õ) to every Latin font.
The tilde is lifted from ñ/Ñ and placed over a/o/A/O. Idempotent."""
import os, re
from PIL import Image
REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
NEW = {0x18: (0xD5, 0x29, 0xE2),   # ã = a + (ñ - n)
       0x1F: (0xE3, 0x29, 0xE2),   # õ = o + (ñ - n)
       0x2F: (0xBB, 0x14, 0xC8),   # Ã = A + (Ñ - N)
       0x30: (0xC9, 0x14, 0xC8)}   # Õ = O + (Ñ - N)
FONTS = {'latin_small_narrow': 'SmallNarrow', 'latin_small': 'Small', 'latin_narrow': 'Narrow',
         'latin_short': 'Short', 'latin_normal': 'Normal', 'latin_narrower': 'Narrower',
         'latin_small_narrower': 'SmallNarrower', 'latin_short_narrow': 'ShortNarrow',
         'latin_short_narrower': 'ShortNarrower'}
def cell(c): return ((c % 16) * 16, (c // 16) * 16)
src = open(os.path.join(REPO, 'src/fonts.c')).read()
for png, tag in FONTS.items():
    path = os.path.join(REPO, 'graphics/fonts', png + '.png')
    im = Image.open(path); p = im.load()
    bg = p[cell(0x18)[0], cell(0x18)[1]] if False else p[0, 0]
    for dst, (base, acc, plain) in NEW.items():
        bx, by = cell(base); ax, ay = cell(acc); nx, ny = cell(plain); dx, dy = cell(dst)
        # rows of the accent: rows where accented glyph differs from plain glyph above the body
        acc_rows = [y for y in range(16) if any(p[ax + x, ay + y] != p[nx + x, ny + y] for x in range(16))]
        acc_rows = [y for y in acc_rows if y < 8]
        body_top = min([y for y in range(16) if any(p[bx + x, by + y] != bg for x in range(16))] or [0])
        for y in range(16):
            for x in range(16):
                p[dx + x, dy + y] = p[bx + x, by + y]
        if not acc_rows: continue
        # shift tilde so it sits just above the body of the base letter
        shift = 0
        for y in acc_rows:
            for x in range(16):
                v = p[ax + x, ay + y]
                if v != p[nx + x, ny + y] and 0 <= y + shift < 16:
                    p[dx + x, dy + y + shift] = v
    im.save(path)
    # widths
    m = re.search(r'(gFont%sLatinGlyphWidths\[\] = \{)(.*?)(\};)' % tag, src, re.S)
    nums = [int(v) for v in re.findall(r'\d+', m.group(2))]
    for dst, (base, _, _) in NEW.items(): nums[dst] = nums[base]
    it = iter(nums)
    body = re.sub(r'\d+', lambda mm: str(next(it)).rjust(len(mm.group(0))), m.group(2))
    src = src[:m.start(2)] + body + src[m.end(2):]
open(os.path.join(REPO, 'src/fonts.c'), 'w').write(src)
cm = os.path.join(REPO, 'charmap.txt'); s = open(cm).read()
if "'ã'" not in s:
    s = s.replace("'á'         = 17\n", "'á'         = 17\n'ã'         = 18\n")
    s = s.replace("'ì'         = 1E\n", "'ì'         = 1E\n'õ'         = 1F\n")
    s = s.replace("'+'         = 2E\n", "'+'         = 2E\n'Ã'         = 2F\n'Õ'         = 30\n")
    open(cm, 'w').write(s)
print('ok')
