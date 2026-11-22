"""The new Lilycove Contest Hall ("big top") for the background, designed to be cheap in tiles:
straight 1:2 tent slopes, stripes on a 16 px period centred on the door, repeating bays, and a
symmetric layout (right half = mirrored left half). Colours from palettes 6 (festival), 7, 8, 9;
multipal.py converts it per 8x8 tile. Canvas 368 x 176 = 23 x 11 metatiles: the top two rows (the
centre peak and the crown) hang over the north street; the door is column 11 of the last row."""
from PIL import Image

WH, CR, YE, OR, RE, DR = (248, 248, 248), (248, 232, 184), (248, 208, 48), (248, 144, 40), (232, 56, 56), (160, 32, 40)
BR, LB, BL, NV = (184, 112, 96), (104, 192, 248), (48, 112, 224), (32, 48, 120)
GL1, GL2, GL3, O8 = (208, 216, 248), (160, 184, 248), (96, 136, 224), (56, 72, 112)
S1, S2, S3, S4, S5, O9 = (240, 240, 208), (232, 232, 176), (200, 200, 152), (168, 160, 128), (136, 136, 88), (56, 72, 112)

W, H = 368, 176
CX = 184
BODY_BOTTOM = 104            # valance bottom
FACADE_TOP = 104

def build():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); p = im.load()
    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c + (255,)
    def get(x, y): return p[x, y][:3] if 0 <= x < W and 0 <= y < H and p[x, y][3] else None

    def stripe_on(x, cx):                    # symmetric 8 px stripes around cx
        return (((x - cx) // 8) % 2 == 0) if x >= cx else (((cx - 1 - x) // 8) % 2 == 0)

    def tent(x0, x1, peak, colours, light_rows):
        a, b, sa, sb = colours; cx = (x0 + x1) // 2
        for x in range(x0, x1):
            top = peak + abs(x + 0.5 - cx) // 2 * 1     # slope 1:2
            top = int(peak + (abs(x - cx + 0.5) - 0.5) // 2)
            for y in range(top, BODY_BOTTOM):
                on = stripe_on(x, cx)
                c = a if on else b
                if y >= BODY_BOTTOM - 24: c = sa if on else sb                # shade band
                if y < top + light_rows: c = CR if on else (LB if b == BL else OR)   # sunlit rim
                put(x, y, c)
            put(x, top, NV)
    # side tents first (behind), then the big centre tent
    tent(16, 144, 56, (WH, BL, CR, NV), 2)
    tent(224, 352, 56, (WH, BL, CR, NV), 2)
    tent(96, 272, 16, (YE, RE, OR, DR), 2)
    # sides of the canopy
    for y in range(88, BODY_BOTTOM):
        put(15, y, NV); put(352, y, NV)
    # golden ropes with blue drapes from the crown down to the shoulders of the centre tent
    for side in (-1, 1):
        for k in range(0, 80):
            x = CX + side * k; y = 16 + k // 2 + 6
            put(x, y, YE); put(x, y + 1, OR)
            if k % 16 < 12:                                           # drapes hanging from the rope
                depth = [0, 2, 3, 4, 4, 5, 5, 5, 5, 4, 4, 3][k % 16]
                for d in range(2, 2 + depth): put(x, y + d, BL if d > 2 + depth - 2 else LB)
    # valance: gold band + red scallops, 16 px period, across the whole canopy
    for x in range(16, 352):
        put(x, BODY_BOTTOM - 10, NV)
        for y in range(BODY_BOTTOM - 9, BODY_BOTTOM - 6): put(x, y, YE if y == BODY_BOTTOM - 8 else OR)
        u = (x - CX) % 16
        depth = int(5 - abs(u - 7.5) * 0.6)
        for y in range(BODY_BOTTOM - 6, BODY_BOTTOM - 6 + depth + 1): put(x, y, RE if y < BODY_BOTTOM - 6 + depth else DR)
    # crown on the top of the centre peak (rows 0..16)
    crown = [
        "..........y..........",
        ".........yRy.........",
        "...y......y......y...",
        "..yBy....yyy....yBy..",
        "...y....yyyyy....y...",
        "...yy..yyyyyyy..yy...",
        "...yyyyyyyyyyyyyyy...",
        "...yyyyyyyyyyyyyyy...",
        "...yRyyyByyyByyyRy...",
        "...yyyyyyyyyyyyyyy...",
        "...ooooooooooooooo...",
        "....ooooooooooooo....",
    ]
    for j, row in enumerate(crown):
        for i, ch in enumerate(row):
            c = {'y': YE, 'o': OR, 'R': RE, 'B': BL}.get(ch)
            if c: put(CX - 10 + i, 2 + j, c)
    snap = [[get(x, y) for x in range(W)] for y in range(16)]
    for y in range(16):                                       # outline the crown
        for x in range(CX - 14, CX + 14):
            if snap[y][x] is None and any(0 <= y + b < 16 and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                put(x, y, NV)
    # flags on the side peaks
    for fx in (80, 288):
        for y in range(40, 56): put(fx, y, NV)
        for y in range(40, 47):
            for x in range(fx + 1, fx + 1 + (7 - abs(y - 43)) ): put(x, y, RE)

    # ---------- facade (symmetric) ----------
    for x in range(16, 352):
        for y in range(FACADE_TOP, H): put(x, y, S2)
    for x in range(16, 352):
        for y in range(FACADE_TOP, FACADE_TOP + 4): put(x, y, YE if y == FACADE_TOP + 1 else OR)   # gold cornice
        put(x, FACADE_TOP + 4, NV)
        for y in range(H - 8, H): put(x, y, S3 if y > H - 8 else O9)                               # plinth
    for bx in list(range(16, CX - 40, 32)) + [2 * CX - 8 - b for b in range(16, CX - 40, 32)]:
        for y in range(FACADE_TOP + 5, H - 8):                                                    # column
            for dx in range(8):
                put(bx + dx, y, O9 if dx in (0, 7) else (S1 if dx in (1, 2) else (S3 if dx in (5, 6) else S2)))
        for dx in range(-1, 9): put(bx + dx, FACADE_TOP + 6, YE); put(bx + dx, FACADE_TOP + 7, OR)    # gold capital
    for wx in list(range(24, CX - 40, 32)) + [2 * CX - 24 - w for w in range(24, CX - 40, 32)]:
        if wx + 24 > CX - 40 and wx < CX: continue
        if wx < CX + 40 and wx + 24 > CX: continue
        for y in range(FACADE_TOP + 12, H - 14):                                                  # tall window
            for x in range(wx, wx + 24):
                edge = x in (wx, wx + 23) or y in (FACADE_TOP + 12, H - 15)
                put(x, y, O8 if edge else (GL1 if (y - FACADE_TOP) % 16 < 3 else (GL2 if (y - FACADE_TOP) % 16 < 9 else GL3)))
        for y in range(FACADE_TOP + 10, FACADE_TOP + 44):                                         # contest banner
            for x in range(wx + 8, wx + 16):
                put(x, y, YE if y == FACADE_TOP + 10 else (DR if x in (wx + 8, wx + 15) else RE))
        for (sx, sy) in ((3, 8), (4, 8), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (2, 10), (3, 10), (4, 10), (5, 10), (2, 11), (5, 11)):
            put(wx + 8 + sx, FACADE_TOP + 10 + sy, YE)
    # ---------- grand entrance ----------
    ex0, ex1 = CX - 40, CX + 40
    for y in range(FACADE_TOP - 2, H - 8):                     # gold portal
        for x in range(ex0, ex1):
            put(x, y, YE if (x - ex0) % 8 in (1, 2) else OR)
        put(ex0, y, NV); put(ex1 - 1, y, NV)
    for x in range(ex0 - 4, ex1 + 4):                          # red canopy over the door
        for y in range(FACADE_TOP + 14, FACADE_TOP + 22):
            put(x, y, RE if (x - CX) % 16 < 8 else DR)
        put(x, FACADE_TOP + 13, NV); put(x, FACADE_TOP + 22, NV)
    for x in range(ex0 - 4, ex1 + 4, 8):
        for y in range(FACADE_TOP + 22, FACADE_TOP + 26): put(x + 3, y, RE); put(x + 4, y, RE)
    # star crest on the portal
    for y in range(FACADE_TOP - 2, FACADE_TOP + 12):
        for x in range(CX - 8, CX + 8):
            d = ((x + 0.5 - CX) ** 2 + (y + 0.5 - FACADE_TOP - 5) ** 2) ** 0.5
            if d < 7: put(x, y, NV if d > 6 else (RE if d > 4.5 else WH))
    for (sx, sy) in ((0, -2), (-1, -1), (0, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1)):
        put(CX + sx, FACADE_TOP + 5 + sy, YE); put(CX - 1 - sx, FACADE_TOP + 5 + sy, YE)
    # red double doors with gold handles
    dy0 = FACADE_TOP + 28
    for y in range(dy0, H - 8):
        for x in range(CX - 24, CX + 24):
            c = RE if (x - CX + 24) % 16 not in (0, 15) else DR
            if y == dy0: c = NV
            put(x, y, c)
        put(CX - 1, y, DR); put(CX, y, DR)
    for x in (CX - 4, CX + 3, CX - 20, CX + 19):
        for y in range(dy0 + 18, dy0 + 22): put(x, y, YE)
    for y in range(H - 8, H):                                  # steps with the red carpet
        for x in range(CX - 24, CX + 24): put(x, y, RE if y % 3 else DR)
    return im
