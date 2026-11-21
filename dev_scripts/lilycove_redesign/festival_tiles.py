#!/usr/bin/env python3
"""Adds the "World Contest Season" festival tiles to the Lilycove secondary tileset.

Idempotent: always starts from base_tileset/ (the untouched Lilycove tileset)
and rewrites data/tilesets/secondary/lilycove/{tiles.png,metatiles.bin,
metatile_attributes.bin,palettes/06.pal,palettes/12.pal}.

New metatile ids are written to festival_ids.json so layout.py can use them.
Palette 6 = festival (red), palette 12 = same art recoloured blue.
"""
import os, json, struct, math
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
TS = os.path.join(REPO, 'data/tilesets/secondary/lilycove')
BASE = os.path.join(HERE, 'base_tileset')

# ---------------------------------------------------------------- palettes
PAL6 = [(0, 0, 0), (248, 248, 248), (248, 232, 184), (248, 208, 48), (248, 144, 40),
        (232, 56, 56), (160, 32, 40), (208, 104, 80), (104, 192, 248), (48, 112, 224),
        (32, 48, 120), (144, 224, 88), (56, 168, 64), (24, 96, 48), (200, 144, 88), (136, 92, 56)]
PAL12 = list(PAL6)
PAL12[5], PAL12[6], PAL12[3] = (48, 112, 224), (32, 48, 120), (248, 248, 248)   # red->blue, yellow->white
PAL12[9], PAL12[10] = (232, 56, 56), (160, 32, 40)                             # blue->red (accents)

def write_pal(path, pal):
    with open(path, 'w', newline='\r\n') as f:
        f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))

# colour index names
_, WH, CR, YE, OR, RE, DR, BR, LB, BL, NV, LG, GR, DG, BN, DB = range(16)

def canvas(w, h): return [[0] * w for _ in range(h)]
def px(c, x, y, v):
    if 0 <= y < len(c) and 0 <= x < len(c[0]): c[y][x] = v
def rect(c, x0, y0, x1, y1, v):
    for y in range(y0, y1):
        for x in range(x0, x1): px(c, x, y, v)

# ---------------------------------------------------------------- art
def brick():
    rows = ['22222222', '77727777', '77727777', '66626666',
            '22222222', '77777772', '77777772', '66666662']
    t = [[int(ch) for ch in r] for r in rows]
    m = {2: CR, 7: BR, 6: DR}
    return [[m[v] for v in r] for r in t]

def carpet():   # 16x16, red carpet with gold borders on both sides
    c = canvas(16, 16); rect(c, 0, 0, 16, 16, RE)
    for y in range(16):
        px(c, 0, y, YE); px(c, 1, y, OR); px(c, 15, y, YE); px(c, 14, y, OR)
        if y % 4 == 0:
            for x in range(3, 13): px(c, x, y, DR) if (x + y) % 8 == 3 else None
    return c

def bunting():  # 16x16 top layer: rope + 4 pennants
    c = canvas(16, 16)
    sag = [2, 2, 3, 3, 3, 4, 4, 4, 4, 4, 4, 3, 3, 3, 2, 2]
    for x in range(16): px(c, x, sag[x], DB)
    cols = [RE, YE, BL, GR]
    for i in range(4):
        x0 = i * 4; top = max(sag[x0:x0 + 4]) + 1
        for d in range(6):
            half = max(0, 2 - (d * 2) // 5)
            for x in range(x0 + 2 - half, x0 + 2 + half):
                px(c, x, top + d, cols[i])
        px(c, x0 + 1, top, WH)
    return c

def umbrella():  # 32x32 top layer
    c = canvas(32, 32)
    cx, cy, r = 15.5, 13.0, 14.5
    for y in range(32):
        for x in range(32):
            dx, dy = x - cx, y - cy
            if dy <= 0 and dx * dx + (dy * 1.9) ** 2 <= r * r:
                seg = int((math.atan2(dy, dx) + math.pi) / (math.pi / 6)) % 2
                col = RE if seg == 0 else WH
                if dx * dx + (dy * 1.9) ** 2 > (r - 1.6) ** 2: col = DR if seg == 0 else CR
                px(c, x, y, col)
    for x in range(1, 31):   # scalloped rim
        if (x // 3) % 2 == 0: px(c, x, 14, DR); px(c, x, 13, DR if c[13][x] else 0)
    rect(c, 15, 14, 17, 29, DB); px(c, 15, 14, BN)
    for y in range(14, 29, 3): px(c, 16, y, BN)
    rect(c, 13, 29, 19, 31, DB)                 # stand
    for x in range(14, 18): px(c, x, 31, BN)
    return c

def palm():      # 32x48 top layer
    c = canvas(32, 48)
    # trunk: slight curve
    for y in range(16, 46):
        off = int(round(1.5 * math.sin((y - 16) / 30 * math.pi / 2)))
        x0 = 14 + off
        rect(c, x0, y, x0 + 4, y + 1, BN)
        px(c, x0, y, DB); px(c, x0 + 3, y, CR if y % 4 == 0 else BN)
        if y % 4 == 0: rect(c, x0, y, x0 + 4, y + 1, DB)
    rect(c, 13, 45, 20, 47, DB)                 # base shadow
    # fronds: arcs radiating from crown
    crown = (16, 15)
    fronds = [(-14, 4), (-13, -6), (-6, -13), (6, -13), (13, -6), (14, 4), (-9, 9), (9, 9)]
    for fx, fy in fronds:
        steps = 40
        for s in range(steps + 1):
            t = s / steps
            x = crown[0] + fx * t
            y = crown[1] + fy * t + 6 * t * t      # droop
            w = 2.4 * (1 - t) + 0.6
            for oy in range(-int(w), int(w) + 1):
                col = GR if oy < 0 else DG
                if abs(oy) == int(w): col = DG
                if oy == -int(w) and t < .7: col = LG
                px(c, int(round(x)), int(round(y + oy)), col)
    for (x, y) in [(14, 16), (17, 17), (15, 18)]:   # coconuts
        rect(c, x, y, x + 2, y + 2, DB); px(c, x, y, BN)
    return c

def banner():    # 16x32 top layer: season banner on a pole
    c = canvas(16, 32)
    rect(c, 2, 0, 4, 31, NV); px(c, 2, 0, YE); px(c, 3, 0, YE)
    rect(c, 4, 3, 14, 21, RE)
    rect(c, 4, 3, 14, 4, YE); rect(c, 4, 20, 14, 21, YE)
    for y in range(21, 24):                     # swallow-tail
        rect(c, 4, y, 8 - (y - 21), y + 1, RE); rect(c, 10 + (y - 21), y, 14, y + 1, RE)
    star = ['...1...', '...1...', '1111111', '.11111.', '..111..', '.11.11.', '1.....1']
    for j, r in enumerate(star):
        for i, ch in enumerate(r):
            if ch == '1': px(c, 5 + i, 8 + j, YE)
    rect(c, 1, 30, 6, 32, DB)
    return c


# ---------------------------------------------------------------- wooden boardwalk
def dock(t=False, b=False, l=False, r=False):  # 16x16 opaque planks with optional edge beams
    c = canvas(16, 16)
    for y in range(16):
        for x in range(16):
            ry = y % 4
            v = OR if ry == 0 else (DB if ry == 3 else BN)
            joint = 5 if (y // 4) % 2 == 0 else 13
            if x == joint and ry != 0: v = DB
            c[y][x] = v
    if t:
        for x in range(16): c[0][x] = DB; c[1][x] = OR
    if b:
        for x in range(16): c[13][x] = OR; c[14][x] = BN; c[15][x] = DB
    if l:
        for y in range(16): c[y][0] = DB; c[y][1] = OR
    if r:
        for y in range(16): c[y][15] = DB; c[y][14] = BN
    return c

def dock_posts():  # top layer over water: shadow of the deck + two wooden pilings
    c = canvas(16, 16)
    for y in range(3):
        for x in range(16):
            if (x + y) % 2 == 0 or y == 0: c[y][x] = NV
    for x0 in (2, 11):
        for y in range(0, 13):
            for x in range(x0, x0 + 3):
                c[y][x] = BN
            c[y][x0] = DB; c[y][x0 + 2] = DB
        for x in range(x0 - 1, x0 + 4): c[13][x] = LB      # ripple
        c[14][x0 + 1] = WH
    return c

def crate():
    c = canvas(16, 16)
    rect(c, 1, 2, 15, 15, BN)
    for i in range(1, 15): c[2][i] = DB; c[14][i] = DB
    for j in range(2, 15): c[j][1] = DB; c[j][14] = DB
    for k in range(3, 14):
        px(c, k, k + 1 - 1, OR); px(c, 15 - k, k, OR)
    rect(c, 1, 15, 15, 16, DB)
    return c

def bollard():
    c = canvas(16, 16)
    rect(c, 5, 4, 11, 14, DB); rect(c, 6, 4, 10, 6, BN); rect(c, 4, 3, 12, 4, DB)
    for x in range(3, 13): px(c, x, 9, CR)                 # rope
    px(c, 3, 10, CR); px(c, 2, 11, CR); px(c, 2, 12, CR)
    rect(c, 5, 14, 11, 15, NV)
    return c

# ---------------------------------------------------------------- tile bank
def split(c):
    h, w = len(c), len(c[0])
    return [[[row[tx * 8:(tx + 1) * 8] for row in c[ty * 8:(ty + 1) * 8]] for tx in range(w // 8)] for ty in range(h // 8)]

class Bank:
    def __init__(self, base_tiles):
        self.tiles = base_tiles; self.index = {}
    def add(self, t):
        if all(v == 0 for r in t for v in r): return None      # -> blank primary tile 0
        key = tuple(tuple(r) for r in t)
        if key not in self.index:
            self.index[key] = 512 + len(self.tiles); self.tiles.append(t)
        return self.index[key]

def entry(tile, pal, blank_ok=True):
    if tile is None: return 0
    return tile | (pal << 12)

SAND = [0x5108, 0x5118, 0x5118, 0x5108]
GRASS = [0x2002, 0x2003, 0x2003, 0x2002]

def main():
    im = Image.open(os.path.join(BASE, 'tiles.png'))
    W, Ht = im.size; p = im.load()
    base = [[[p[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)]
            for ty in range(Ht // 8) for tx in range(W // 8)]
    # drop trailing blank padding? keep as-is to preserve indices
    bank = Bank(base)
    metas = list(struct.unpack('<%dH' % (os.path.getsize(os.path.join(BASE, 'metatiles.bin')) // 2),
                               open(os.path.join(BASE, 'metatiles.bin'), 'rb').read()))
    attrs = list(struct.unpack('<%dH' % (os.path.getsize(os.path.join(BASE, 'metatile_attributes.bin')) // 2),
                               open(os.path.join(BASE, 'metatile_attributes.bin'), 'rb').read()))
    ids = {}
    def add_meta(name, bottom, top, attr=0):
        mid = 512 + len(attrs)
        metas.extend(bottom + top); attrs.append(attr); ids[name] = mid
        return mid
    def tiles_of(c, pal):
        g = split(c)
        return [[[entry(bank.add(t), pal) for t in row] for row in g]]
    # brick + carpet (bottom layer only)
    bt = bank.add(brick())
    BRICK = [bt | 6 << 12] * 4
    add_meta('brick', BRICK, [0] * 4)
    cg = split(carpet())
    add_meta('carpet', [entry(bank.add(cg[0][0]), 6), entry(bank.add(cg[0][1]), 6),
                        entry(bank.add(cg[1][0]), 6), entry(bank.add(cg[1][1]), 6)], [0] * 4)
    COB = [0x9234, 0x9235, 0x9235, 0x9234]
    # bunting
    bg = split(bunting())
    for pal, sfx in ((6, ''), (12, '_blue')):
        top = [entry(bank.add(bg[0][0]), pal), entry(bank.add(bg[0][1]), pal),
               entry(bank.add(bg[1][0]), pal), entry(bank.add(bg[1][1]), pal)]
        for under, nm in ((BRICK, 'brick'), (COB, 'cobble'), (GRASS, 'grass'), (SAND, 'sand')):
            add_meta('bunting_%s%s' % (nm, sfx), under, top)
    # multi-metatile objects
    def obj(name, art, unders, pals):
        g = split(art); mh, mw = len(g) // 2, len(g[0]) // 2
        for pal, sfx in pals:
            for un, unm in unders:
                for my in range(mh):
                    for mx in range(mw):
                        q = [g[my * 2][mx * 2], g[my * 2][mx * 2 + 1], g[my * 2 + 1][mx * 2], g[my * 2 + 1][mx * 2 + 1]]
                        top = [entry(bank.add(t), pal) for t in q]
                        add_meta('%s%s_%s_%d_%d' % (name, sfx, unm, mx, my), un, top)
    # wooden boardwalk / piers
    def quad(art_):
        g = split(art_)
        return [entry(bank.add(g[0][0]), 6), entry(bank.add(g[0][1]), 6), entry(bank.add(g[1][0]), 6), entry(bank.add(g[1][1]), 6)]
    for t in (0, 1):
        for b in (0, 1):
            for l in (0, 1):
                for r in (0, 1):
                    name = 'dock' + ('_' + ''.join(k for k, f in zip('tblr', (t, b, l, r)) if f) if (t or b or l or r) else '')
                    add_meta(name, quad(dock(t, b, l, r)), [0] * 4)
    WATER = [0x41c6, 0x41c7, 0x41c7, 0x41c6]
    add_meta('dock_posts', WATER, quad(dock_posts()))
    PLANK = quad(dock())
    add_meta('dock_crate', PLANK, quad(crate()))
    add_meta('dock_bollard', PLANK, quad(bollard()))
    obj('umbrella', umbrella(), [(SAND, 'sand')], [(6, ''), (12, '_blue')])
    obj('palm', palm(), [(SAND, 'sand'), (GRASS, 'grass'), (BRICK, 'brick')], [(6, '')])
    obj('banner', banner(), [(BRICK, 'brick'), (GRASS, 'grass'), (COB, 'cobble')], [(6, ''), (12, '_blue')])
    assert len(bank.tiles) <= 512, len(bank.tiles)
    assert len(attrs) <= 512, len(attrs)
    # write tiles.png (pad to full rows)
    n = len(bank.tiles); rows = (n + 15) // 16
    out = Image.new('P', (128, rows * 8)); out.putpalette(sum(PAL6, ()) + (0, 0, 0) * 240)
    op = out.load()
    for i, t in enumerate(bank.tiles):
        for y in range(8):
            for x in range(8): op[(i % 16) * 8 + x, (i // 16) * 8 + y] = t[y][x]
    out.save(os.path.join(TS, 'tiles.png'))
    open(os.path.join(TS, 'metatiles.bin'), 'wb').write(struct.pack('<%dH' % len(metas), *metas))
    open(os.path.join(TS, 'metatile_attributes.bin'), 'wb').write(struct.pack('<%dH' % len(attrs), *attrs))
    write_pal(os.path.join(TS, 'palettes/06.pal'), PAL6)
    write_pal(os.path.join(TS, 'palettes/12.pal'), PAL12)
    json.dump(ids, open(os.path.join(HERE, 'festival_ids.json'), 'w'), indent=1)
    print('tiles', n, '/ 512   metatiles', len(attrs), '/ 512   new metatiles', len(ids))

if __name__ == '__main__':
    main()
