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
