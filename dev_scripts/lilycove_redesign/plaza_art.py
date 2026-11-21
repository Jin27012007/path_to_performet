"""Plaza pieces drawn/recoloured into Lilycove palette 8 (greys + blues), so they sit
with the rest of Emerald's art: grey paving (Slateport's paving pattern, recoloured)
and a round stone fountain with a dark outline and 3-tone shading."""
import math, struct, os
from PIL import Image
import render

PAL8_SLOT = 8
# palette 8 indices
OUT, DGR, MGR, LGR, WH = 7, 6, 5, 8, 11
PALE, LB1, LB2, B1, B2 = 1, 9, 10, 3, 4

def _canvas(w, h): return [[0] * w for _ in range(h)]
def _px(c, x, y, v):
    if 0 <= y < len(c) and 0 <= x < len(c[0]): c[y][x] = v

def paving():
    """16x16 grey square tiles (4 per metatile): light face, subtle grout, top-left highlight."""
    c = _canvas(16, 16)
    for y in range(16):
        for x in range(16):
            gx, gy = x % 8, y % 8
            if gx == 7 or gy == 7: v = PALE                 # grout
            elif gx == 0 or gy == 0: v = WH if (gx + gy) < 6 else LGR
            else: v = LGR
            c[y][x] = v
    return c

def fountain():
    """48x48 round stone fountain seen from above (3/4 view)."""
    c = _canvas(48, 48)
    cx, cy, rx, ry = 23.5, 27.0, 21.0, 14.0
    # front wall of the basin (below the rim)
    for y in range(48):
        for x in range(48):
            e = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            e2 = ((x - cx) / rx) ** 2 + ((y - cy - 5) / ry) ** 2
            if e > 1 and e2 <= 1 and y > cy:
                c[y][x] = MGR if y < cy + ry + 3 else DGR
    # rim + water
    for y in range(48):
        for x in range(48):
            e = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if e <= 1:
                if e > 0.70: c[y][x] = LGR if y < cy else PALE          # stone rim
                else:
                    c[y][x] = LB1 if e < 0.45 else LB2
                    if y < cy - 4 and e > 0.5: c[y][x] = B1               # shadow of the rim
    # ripples
    for (x0, y0) in [(12, 26), (32, 30), (17, 33), (29, 21), (35, 25)]:
        for dx in range(4): _px(c, x0 + dx, y0, WH)
    # pedestal (column) and upper bowl
    for y in range(15, 30):
        for x in range(20, 28): c[y][x] = OUT if x in (20, 27) else (LGR if x < 23 else (MGR if x < 26 else DGR))
    for y in range(9, 19):
        for x in range(12, 36):
            e = ((x - 23.5) / 10.5) ** 2 + ((y - 14) / 4.0) ** 2
            if e <= 1: c[y][x] = (OUT if e > 0.8 and y >= 14 else (LGR if y < 14 else MGR))
            ein = ((x - 23.5) / 7.5) ** 2 + ((y - 13.5) / 2.2) ** 2
            if ein <= 1: c[y][x] = LB1 if y >= 13 else LB2
    # dark outline around the stone parts
    out = [row[:] for row in c]
    for y in range(48):
        for x in range(48):
            if c[y][x] == 0 and any(0 <= y + dy < 48 and 0 <= x + dx < 48 and c[y + dy][x + dx]
                                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = OUT
    # water jet and falling drops (no outline, like Emerald's water effects)
    for y in range(1, 13):
        for x in range(22, 26): out[y][x] = WH if x in (23, 24) else LB1
    for x in range(19, 29): _px(out, x, 1, WH if 21 < x < 26 else LB1)
    for (x, y) in [(18, 3), (17, 5), (16, 7), (29, 3), (30, 5), (31, 7), (15, 9), (32, 9)]:
        _px(out, x, y, LB1)
    for (x, y) in [(17, 4), (30, 4), (16, 8), (31, 8)]:
        _px(out, x, y, WH)
    return out


def fountain_modern():
    """64x48 modern fountain: rounded rectangular pool, stone rim, three water jets."""
    W, H = 64, 48
    c = _canvas(W, H)
    x0, x1, y0, y1, r = 2, 61, 16, 41, 6
    def inside(x, y, x0, x1, y0, y1, r):
        if x < x0 or x > x1 or y < y0 or y > y1: return False
        cx = min(max(x, x0 + r), x1 - r); cy = min(max(y, y0 + r), y1 - r)
        return (x - cx) ** 2 + (y - cy) ** 2 <= r * r
    # front wall (depth) of the pool
    for y in range(y0, y1 + 5):
        for x in range(W):
            if inside(x, y - 4, x0, x1, y0, y1, r) and not inside(x, y, x0, x1, y0, y1, r):
                c[y][x] = MGR if y < y1 + 3 else DGR
    # rim (3 px) and water
    for y in range(H):
        for x in range(W):
            if inside(x, y, x0, x1, y0, y1, r):
                if inside(x, y, x0 + 3, x1 - 3, y0 + 3, y1 - 3, max(1, r - 3)):
                    c[y][x] = LB1
                    if y < y0 + 6: c[y][x] = B1           # shade under the far rim
                    elif y < y0 + 8: c[y][x] = LB2
                else:
                    c[y][x] = LGR if y < (y0 + y1) // 2 else PALE
    # ripple lines on the water
    for (xa, xb, y) in [(8, 16, 30), (22, 28, 34), (36, 44, 29), (48, 55, 35), (12, 18, 37), (40, 47, 37)]:
        for x in range(xa, xb): c[y][x] = WH
    # nozzles (small stone discs) for the three jets
    jets = [(16, 14), (32, 4), (47, 14)]
    for jx, top in jets:
        for x in range(jx - 3, jx + 4):
            for y in range(28, 31): c[y][x] = MGR if y == 30 else LGR
    # dark outline around the stone
    out = [row[:] for row in c]
    for y in range(H):
        for x in range(W):
            if c[y][x] == 0 and any(0 <= y + dy < H and 0 <= x + dx < W and c[y + dy][x + dx]
                                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = OUT
    # jets: thin columns of water with a white core and splash rings
    for jx, top in jets:
        for y in range(top, 28):
            out[y][jx - 1] = LB1; out[y][jx] = WH; out[y][jx + 1] = LB1
        for dx in (-4, -3, 3, 4): _px(out, jx + dx, 27, WH)
        for dx in (-5, 5): _px(out, jx + dx, 28, LB2)
        _px(out, jx - 2, top + 1, LB1); _px(out, jx + 2, top + 1, LB1)
        _px(out, jx - 3, top + 3, WH); _px(out, jx + 3, top + 3, WH)
    return out


def lamp_post():
    """Lilycove's street lamp (metatile 0x29A) without its grass, recoloured to palette 8."""
    mimg = render.build('primary/general', 'secondary/lilycove_city')[0]
    lamp = mimg(0x29a).load(); grass = mimg(0x001).load()
    pal = render_palette8()
    c = _canvas(16, 16)
    for y in range(16):
        for x in range(16):
            if lamp[x, y] != grass[x, y]:
                col = lamp[x, y]
                c[y][x] = min(range(1, 16), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], col)))
    return c

def render_palette8():
    import os
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data/tilesets/secondary/lilycove/palettes/08.pal')
    L = open(p).read().split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in L]
