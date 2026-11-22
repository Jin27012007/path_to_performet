"""Ornaments of the Contest Hall drawn as sprites (one 15-colour object palette): a big crown crest
on the front of the big top, an ornate golden portal over the entrance, two golden trophies on
marble pedestals and two large pennants on the side tents. Index canvases (0 = transparent)."""
import math
PAL = [(0, 0, 0), (40, 32, 64), (255, 244, 168), (248, 208, 72), (224, 160, 40), (168, 104, 32),
       (240, 72, 72), (176, 32, 48), (96, 160, 248), (40, 80, 184), (248, 248, 248), (240, 232, 208),
       (176, 168, 160), (248, 152, 192), (56, 200, 160), (104, 64, 40)]
T, OUT, GH, G1, G2, G3, R1, R2, B1, B2, WH, CR, GR, PK, TL, DK = range(16)

def canvas(w, h): return [[0] * w for _ in range(h)]
def outline(c, col=OUT):
    h, w = len(c), len(c[0]); o = [r[:] for r in c]
    for y in range(h):
        for x in range(w):
            if c[y][x] == 0 and any(0 <= x + a < w and 0 <= y + b < h and c[y + b][x + a] not in (0, OUT)
                                    for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                o[y][x] = col
    return o
def gold(x, y, x0, x1, y0, y1):
    """metallic shading: light at the top-left, dark at the bottom-right of a box"""
    u = (x - x0) / max(1, x1 - x0); v = (y - y0) / max(1, y1 - y0); s = u * 0.6 + v * 0.8
    return GH if s < 0.25 else (G1 if s < 0.7 else (G2 if s < 1.1 else G3))

def crown():
    W, H = 80, 48; c = canvas(W, H)
    # red velvet cap behind the points
    for y in range(14, 32):
        for x in range(18, 62):
            if (x - 40) ** 2 / 22 ** 2 + (y - 32) ** 2 / 18 ** 2 <= 1: c[y][x] = R2 if (x + y) % 7 else R1
    # five points with pearls (centre tallest)
    for (px, top, half) in ((14, 16, 6), (27, 9, 6), (40, 3, 7), (53, 9, 6), (66, 16, 6)):
        for y in range(top + 4, 32):
            w = half * (y - top - 4) / (32 - top - 4) + 1.5
            for x in range(int(px - w), int(px + w) + 1): c[y][x] = gold(x, y, px - half, px + half, top, 32)
        for y in range(top - 1, top + 5):
            for x in range(px - 3, px + 4):
                if (x - px) ** 2 + (y - top - 2) ** 2 <= 9: c[y][x] = WH if (x - px) + (y - top - 2) < 0 else CR
    # band with jewels
    for y in range(30, 40):
        for x in range(8, 72): c[y][x] = gold(x, y, 8, 72, 30, 40)
    for x in range(8, 72): c[30][x] = GH; c[39][x] = G3
    for k, (jx, col) in enumerate(((16, PK), (28, B1), (40, R1), (52, B1), (64, PK))):
        for y in range(32, 38):
            for x in range(jx - 3, jx + 4):
                d = abs(x - jx) + abs(y - 35)
                if d <= 3: c[y][x] = WH if d == 0 or (x - jx, y - 35) == (-1, -1) else col
    # blue contest ribbon under the crown, with forked tails
    for y in range(40, 47):
        for x in range(2, 78):
            if x < 10 and abs(y - 43) > (x - 2): continue
            if x > 69 and abs(y - 43) > (77 - x): continue
            c[y][x] = B1 if y < 43 else B2
    for x in range(10, 70): c[40][x] = G1
    return outline(c)

def portal():
    W, H = 80, 64; c = canvas(W, H)
    # pediment
    for y in range(0, 12):
        half = 4 + y * 3.2
        for x in range(int(40 - half), int(40 + half) + 1):
            if 0 <= x < W: c[y][x] = gold(x, y, 0, 80, 0, 12)
    for x in range(2, 78): c[11][x] = G3; c[12][x] = G2
    for y in range(3, 10):                                   # red medallion in the pediment
        for x in range(34, 47):
            if (x - 40) ** 2 / 36 + (y - 6.5) ** 2 / 9 <= 1: c[y][x] = R1 if (x - 40) ** 2 / 36 + (y - 6.5) ** 2 / 9 > 0.35 else GH
    # columns (fluted) with capitals and bases
    for cx0 in (2, 66):
        for y in range(13, 64):
            for x in range(cx0, cx0 + 12):
                c[y][x] = (GH if (x - cx0) % 4 == 1 else (G1 if (x - cx0) % 4 == 2 else G2)) if 2 <= x - cx0 <= 9 else G3
        for y in range(13, 18):
            for x in range(cx0 - 2, cx0 + 14): c[y][x] = gold(x, y, cx0 - 2, cx0 + 14, 13, 18)
        for y in range(58, 64):
            for x in range(cx0 - 2, cx0 + 14): c[y][x] = CR if y < 61 else GR
    # arch with keystone star
    for y in range(13, 44):
        for x in range(14, 66):
            d = math.hypot(x + 0.5 - 40, y + 0.5 - 40)
            if 22 <= d <= 28 and y < 40: c[y][x] = gold(x, y, 14, 66, 13, 40)
    for y in range(10, 22):
        for x in range(34, 46):
            if abs(x + 0.5 - 40) + abs(y + 0.5 - 16) <= 6: c[y][x] = R1 if abs(x + 0.5 - 40) + abs(y + 0.5 - 16) > 2 else WH
    # red curtains drawn back inside the arch
    for side in (-1, 1):
        for y in range(18, 52):
            depth = int(7 - abs(y - 30) / 4) if y < 40 else 2
            for k in range(max(1, depth)):
                x = 40 + side * (21 - k)
                if 0 <= x < W and c[y][x] == 0: c[y][x] = R1 if k % 3 else R2
        for x in range(40 + side * 22, 40 + side * 15, -side):  # golden tassel tie
            if 0 <= x < W: c[38][x] = G1; c[39][x] = G3
    return outline(c)

def trophy():
    W, H = 32, 48; c = canvas(W, H)
    for y in range(32, 48):                                  # marble pedestal
        for x in range(5, 27):
            c[y][x] = CR if x < 18 else GR
        if y in (32, 47): 
            for x in range(4, 28): c[y][x] = WH if y == 32 else GR
    for y in range(26, 32):                                  # stem and foot
        for x in range(14 - (y - 26) // 2, 18 + (y - 26) // 2): c[y][x] = gold(x, y, 10, 22, 26, 32)
    for y in range(4, 24):                                   # cup
        half = 10 - (y - 4) * 0.35 if y > 8 else 10
        for x in range(int(16 - half), int(16 + half)): c[y][x] = gold(x, y, 6, 26, 4, 24)
    for y in range(9, 19):                                   # handles
        for (hx, s) in ((4, 1), (27, -1)):
            if abs(y - 14) in (4, 5) or y in range(10, 18) and abs(y - 14) < 4 and True:
                pass
        c[y][3] = G2; c[y][28] = G2
    for x in range(3, 7): c[9][x] = G1; c[18][x] = G2
    for x in range(25, 29): c[9][x] = G1; c[18][x] = G2
    for (sx, sy) in ((0, -3), (-1, -2), (0, -2), (1, -2), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (-1, 0), (0, 0), (1, 0), (-2, 1), (2, 1)):
        c[13 + sy][16 + sx] = R1                             # red star on the cup
    for y in range(5, 22): c[y][9] = GH if c[y][9] else 0
    return outline(c)

def pennant():
    """flag on a pole whose foot is at x 7..8 (the middle of the 16 px tile it stands on)"""
    W, H = 32, 48; c = canvas(W, H)
    for y in range(4, 48): c[y][7] = G2; c[y][8] = G3
    for (x, y) in ((7, 1), (8, 1), (6, 2), (7, 2), (8, 2), (9, 2), (7, 3), (8, 3)): c[y][x] = G1
    for y in range(5, 25):                                   # waving swallow-tail flag
        for x in range(9, 31):
            wave = int(2 * math.sin((x - 9) / 6.0))
            yy = y + wave
            if not (5 <= yy < 47): continue
            if x > 25 and abs(y - 15) < (x - 25) * 1.1: continue
            c[yy][x] = B2 if y in (5, 24) else (R1 if y < 20 else R2)
    for (sx, sy) in ((0, -3), (-1, -2), (0, -2), (1, -2), (-3, -1), (-2, -1), (-1, -1), (0, -1), (1, -1), (2, -1), (3, -1), (-1, 0), (0, 0), (1, 0), (-2, 1), (2, 1)):
        x = 17 + sx; y = 13 + sy + int(2 * math.sin((x - 9) / 6.0)); c[y][x] = G1
    return outline(c)

def crown_small():
    """48x32 golden crown finial for the top of the dome (base on the bottom row)"""
    W, H = 48, 32; c = canvas(W, H)
    for y in range(12, 24):
        for x in range(12, 36):
            if (x - 24) ** 2 / 12 ** 2 + (y - 24) ** 2 / 12 ** 2 <= 1: c[y][x] = R2 if (x + y) % 6 else R1
    for (px, top, half) in ((10, 12, 4), (17, 7, 4), (24, 3, 5), (31, 7, 4), (38, 12, 4)):
        for y in range(top + 3, 24):
            w = half * (y - top - 3) / (24 - top - 3) + 1.2
            for x in range(int(px - w), int(px + w) + 1): c[y][x] = gold(x, y, px - half, px + half, top, 24)
        for y in range(top - 1, top + 4):
            for x in range(px - 2, px + 3):
                if (x - px) ** 2 + (y - top - 1) ** 2 <= 4: c[y][x] = WH if (x - px) + (y - top - 1) < 0 else CR
    for y in range(23, 30):
        for x in range(6, 42): c[y][x] = gold(x, y, 6, 42, 23, 30)
    for x in range(6, 42): c[23][x] = GH; c[29][x] = G3
    for (jx, col) in ((12, PK), (18, B1), (24, R1), (30, B1), (36, PK)):
        c[26][jx] = col; c[25][jx] = col; c[26][jx + 1] = col; c[25][jx + 1] = WH
    return outline(c)
