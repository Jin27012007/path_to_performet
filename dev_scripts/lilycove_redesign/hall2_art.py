"""The Contest Hall in Emerald's 3/4 view, drawn as crisp pixel art at its final size (27 x 11 metatiles,
the whole block), after the user's concept: a stone palace whose slate roof is seen from above, four
blue-domed round towers, the striped big-top dome with the trophy sitting on the roof, and the entrance
portico. Background: palace + towers (symmetric, on the 8 px grid, so tiles repeat/flip).
Sprites: the big-top dome and the entrance portico."""
import math
from PIL import Image

W, H = 432, 176
CX = 216
TILT = math.radians(24)                      # how much of the top we see (3/4 view)
OUT, DK = (64, 72, 104), (96, 96, 120)
ST1, ST2, ST3 = (208, 208, 184), (176, 176, 144), (152, 152, 120)
WH, LG, MG, GG = (248, 248, 248), (216, 216, 216), (168, 176, 184), (136, 144, 152)
GL1, GL2, GL3 = (200, 208, 224), (152, 176, 208), (136, 176, 208)
BD1, BD2, BD3, BD4 = (208, 216, 248), (160, 184, 248), (96, 136, 224), (72, 104, 200)
SL = (56, 72, 112)                           # slate shadow (palette 8)
GO1, GO2, GO3 = (248, 248, 136), (232, 232, 104), (176, 176, 96)
RE, DR, YE, BL, GR, NV = (232, 56, 56), (160, 32, 40), (248, 208, 48), (48, 112, 224), (56, 168, 64), (32, 48, 120)
OR, ORD, YED, CR = (248, 144, 40), (216, 96, 32), (232, 176, 32), (248, 232, 184)

def _img(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))

def _outline(im, col):
    p = im.load(); w, h = im.size
    snap = [[p[x, y][3] for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            if not snap[y][x] and any(0 <= x + a < w and 0 <= y + b < h and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                p[x, y] = col + (255,)

def dome3d(put, cx, by, R, colour, light=(0.0, 0.55, 0.84)):
    """hemisphere of radius R whose base circle is centred at (cx, by), seen from above-front at TILT.
    colour(lon, lat, lum) -> rgb.  Returns nothing; the base ellipse's front arc ends the silhouette."""
    ca, sa = math.cos(TILT), math.sin(TILT)
    for sy in range(by - R - 1, by + int(R * sa) + 2):
        for sx in range(cx - R, cx + R):
            x = sx + 0.5 - cx; yu = by - (sy + 0.5)
            d2 = R * R - x * x - yu * yu
            if d2 < 0: continue
            dep = math.sqrt(d2)
            Z = yu * ca + dep * sa; Y = -yu * sa + dep * ca
            if Z < 0: continue
            lum = (x * light[0] + Y * light[1] + Z * light[2]) / R
            put(sx, sy, colour(math.atan2(x, Y), math.asin(min(1, Z / R)), lum))

def ring(put, cx, by, rx, thick, cols):
    """the front half of an ellipse band (drum / rim) under a dome; cols = (top, bottom)"""
    ry = rx * math.sin(TILT)
    for sx in range(cx - rx, cx + rx):
        x = sx + 0.5 - cx
        yb = by + ry * math.sqrt(max(0, 1 - (x / rx) ** 2))
        for t in range(thick): put(sx, int(yb) + t, cols[0] if t < thick - 1 else cols[1])

def body():
    im = _img(W, H); p = im.load()
    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c + (255,)
    def rect(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)): put(x, y, c)
    def ashlar(x0, y0, x1, y1, shade=None):
        for y in range(y0, y1):
            for x in range(x0, x1):
                r = y % 16; off = 8 if (y // 16) % 2 else 0
                c = ST2
                if r == 0: c = ST1
                if r == 15 or (x + off) % 16 == 15: c = ST3
                if shade:
                    s = shade(x)
                    if s < 0: c = {ST1: ST2, ST2: ST3, ST3: GG}[c]
                    elif s > 0 and c == ST2: c = ST1 if r < 2 else c
                put(x, y, c)
    def window(x0, y0, w, h):
        cx = x0 + (w - 1) / 2; rr = (w - 1) / 2
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if y < y0 + rr and (x - cx) ** 2 + (y - y0 - rr) ** 2 > rr * rr + 0.5: continue
                edge = x in (x0, x0 + w - 1) or y == y0 + h - 1 or (y < y0 + rr and (x - cx) ** 2 + (y - y0 - rr) ** 2 > (rr - 1.2) ** 2)
                put(x, y, OUT if edge else (GL1 if y < y0 + h * 0.4 else (GL2 if y < y0 + h * 0.7 else GL3)))
        rect(x0 - 2, y0 + h, x0 + w + 2, y0 + h + 2, WH)
    # ---- slate roof of the palace, seen from above (rear ridge at y 32, front eave at y 104)
    for y in range(36, 104):
        for x in range(56, CX):
            r = (y - 36) % 8; off = 4 if ((y - 36) // 8) % 2 else 0
            c = BD3
            if r == 0: c = BD2
            if r == 7: c = BD4
            if r >= 5 and (x + off) % 8 == 7: c = BD4
            put(x, y, c)
    rect(56, 32, CX, 36, GO2); rect(56, 32, CX, 33, GO1)                               # ridge cap
    # front eave: gold trim + white cornice with dentils, seen slightly from above
    rect(56, 104, CX, 106, GO2); rect(56, 106, CX, 110, WH); rect(56, 110, CX, 112, LG)
    for x in range(56, CX, 4): put(x + 1, 111, MG); put(x + 2, 111, MG)
    # ---- facade (short, as in Emerald): ashlar, pilasters, windows, banners
    ashlar(56, 112, CX, 164)
    for px_ in (104, 168):                                                           # pilasters
        rect(px_, 112, px_ + 8, 164, LG); rect(px_ + 6, 112, px_ + 8, 164, MG); rect(px_ + 1, 114, px_ + 2, 162, WH)
    for wx in (120, 144):
        window(wx, 120, 16, 32)
    for (bx, col) in ((136, RE),):                                         # contest banners
        rect(bx, 112, bx + 8, 142, col); rect(bx, 112, bx + 8, 115, YE)
        for (sx, sy) in ((3, 6), (4, 6), (2, 7), (3, 7), (4, 7), (5, 7), (3, 8), (4, 8)): put(bx + sx, 116 + sy, YE)
        for x in range(bx, bx + 8, 2): put(x, 142, col)
    # ---- round towers: cylinder body (lit from the front), rim, ribbed blue dome, flag
    def tower(cx, top, half, R):
        lt, dk = (0, 16) if half > 16 else (0, 8)              # shading bands on the 8 px grid
        shade = lambda x: -1 if abs(x + 0.5 - cx) > dk else (1 if abs(x + 0.5 - cx) < lt else 0)
        ashlar(cx - half, top, cx + half, 164, shade)
        for wy in range(top + 20, 140, 40): window(cx - 8, wy, 16, 28)
        ry = int((half + 2) * math.sin(TILT))
        for y in range(top - ry, top + ry + 1):                                       # rim seen from above
            for x in range(cx - half - 2, cx + half + 2):
                if ((x + 0.5 - cx) / (half + 2)) ** 2 + ((y - top) / (ry + 0.5)) ** 2 <= 1: put(x, y, WH)
        ring(put, cx, top, half + 2, 3, (LG, MG))
        def col(lon, lat, lum):
            rib = min(abs(lon - k * math.pi / 4) for k in range(-4, 5)) < 0.09
            c = BD1 if lum > 0.85 else (BD2 if lum > 0.55 else (BD3 if lum > 0.2 else BD4))
            return BD4 if rib and c != BD4 else (SL if rib else c)
        dome3d(put, cx, top - 1, R, col)
        ring(put, cx, top - 1, R, 3, (GO2, GO3))
        ap = top - 1 - int(R * math.cos(TILT))
        rect(cx - 1, ap - 5, cx + 1, ap + 1, GO2); rect(cx - 2, ap - 8, cx + 2, ap - 5, GO1)
        for y in range(ap - 18, ap - 8): put(cx, y, DK)
        for y in range(ap - 18, ap - 12):
            for x in range(cx + 1, cx + 1 + (7 - abs(2 * (y - (ap - 15)) + 1))): put(x, y, RE)
    tower(88, 88, 16, 16)                                                            # inner (lower)
    tower(32, 64, 24, 22)                                                            # outer (taller, corner)
    # plinth / steps along the front
    rect(0, 164, CX, 176, ST1); rect(0, 164, CX, 166, ST3); rect(0, 170, CX, 171, ST2)
    for y in range(H):
        for x in range(CX): p[2 * CX - 1 - x, y] = p[x, y]
    for y in range(112, 143):                                                        # right banner: blue
        for x in range(W - 144, W - 136):
            if p[x, y][:3] in (RE,): p[x, y] = BL + (255,)
    ashlar(176, 112, 256, 164)                                                       # hidden by the portico
    _outline(im, OUT)
    return im

# ---------------- sprites ----------------
DOME_W, DOME_H, DOME_Y = 176, 128, -16       # canvas position (128, -16): map x 22..32, rows 10..17
def big_top():
    im = _img(DOME_W, DOME_H); p = im.load()
    def put(x, y, c):
        if 0 <= x < DOME_W and 0 <= y < DOME_H: p[x, y] = c + (255,)
    cx, by, R = 88, 98, 74
    TONES = {YE: (CR, YE, YED), OR: (YE, OR, ORD), BL: (BD3, BL, NV)}
    seq = [YE, OR, BL, OR]
    def col(lon, lat, lum):
        k = int((abs(lon) + math.pi / 16) / (math.pi / 8)) % 4
        t = TONES[seq[k]]
        return t[0] if lum > 0.8 else (t[1] if lum > 0.3 else t[2])
    dome3d(put, cx, by, R, col, light=(-0.35, 0.5, 0.79))
    ring(put, cx, by, R, 4, (GO2, GO3))
    ry = R * math.sin(TILT)
    for sx in range(cx - R, cx + R):                                                 # scalloped valance
        x = sx + 0.5 - cx; yb = by + 3 + ry * math.sqrt(max(0, 1 - (x / R) ** 2))
        u = (sx - cx + 8) % 16; d = int(5 - abs(u - 7.5) * 0.55)
        for t in range(max(1, d)): put(sx, int(yb) + 1 + t, RE if t < d - 1 else DR)
    ap = by - int(R * math.cos(TILT))                                                # apex
    # bunting: strings from the apex down the dome, with pennants
    for side in (-1, 1):
        for (ex, ey) in ((54, 40), (78, 70)):
            n = 40
            for k in range(n):
                t = k / n
                x = cx + side * int(6 + ex * t); y = ap + 4 + int(ey * t * t * 0.9 + 6 * math.sin(t * math.pi))
                put(x, y, DK)
                if k % 5 == 2:
                    c = (RE, YE, BL, GR)[(k // 5) % 4]
                    for d in range(1, 5):
                        for w in range(4 - d + 1): put(x + side * w, y + d, c)
    # trophy on a gold cap, red bow
    for y in range(ap - 6, ap + 4):
        hw = 10 + (y - ap + 6)
        for x in range(cx - hw, cx + hw): put(x, y, GO1 if y < ap - 3 else (GO2 if y < ap + 1 else GO3))
    top = ap - 30
    for y in range(top, top + 18):
        half = 9 if y < top + 5 else 9 - (y - top - 5) * 0.45
        for x in range(int(cx - half), int(cx + half)): put(x, y, GO1 if x < cx - 2 else GO2)
    for y in range(top + 3, top + 12): put(cx - 12, y, GO2); put(cx + 11, y, GO2)
    for x in range(cx - 12, cx - 8): put(x, top + 3, GO2); put(x, top + 11, GO2)
    for x in range(cx + 8, cx + 12): put(x, top + 3, GO2); put(x, top + 11, GO2)
    for y in range(top + 5, top + 12):
        for x in range(cx - 4, cx + 4):
            if (x + 0.5 - cx) ** 2 + (y - top - 8) ** 2 <= 13: put(x, y, RE if y < top + 8 else WH)
    for x in range(cx - 4, cx + 4): put(x, top + 8, OUT)
    for x in range(cx - 3, cx + 3): put(x, top + 18, GO3); put(x, top + 19, GO2)
    for y in range(top + 18, top + 28):
        for x in range(cx - 11, cx + 11):
            if abs(x + 0.5 - cx) > 2 and abs(y - top - 23) < (abs(x + 0.5 - cx) - 2) * 0.7 + 1: put(x, y, RE)
    for y in range(top + 21, top + 26):
        for x in range(cx - 2, cx + 2): put(x, y, DR)
    _outline(im, OUT)
    return im

ENT_W, ENT_H, ENT_X, ENT_Y = 80, 80, 176, 96   # map x 25..29, rows 17..21
def entrance():
    """projecting portico: slate roof seen from above, Poke Ball pediment, columns, drapes, glass doors"""
    im = _img(ENT_W, ENT_H); p = im.load()
    def put(x, y, c):
        if 0 <= x < ENT_W and 0 <= y < ENT_H: p[x, y] = c + (255,)
    def rect(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(ENT_H, y1)):
            for x in range(max(0, x0), min(ENT_W, x1)): put(x, y, c)
    cx = 40
    for y in range(2, 18):                                                          # portico roof (above)
        for x in range(2, 78):
            r = (y - 2) % 6; c = BD2 if r == 0 else (BD4 if r == 5 else BD3)
            put(x, y, c)
    rect(2, 0, 78, 2, GO1)
    rect(0, 18, 80, 20, GO2); rect(0, 20, 80, 26, WH); rect(0, 26, 80, 28, LG)       # entablature
    for x in range(2, 78, 4): put(x, 27, MG); put(x + 1, 27, MG)
    for y in range(10, 27):                                                         # Poke Ball crest
        for x in range(cx - 8, cx + 8):
            if (x + 0.5 - cx) ** 2 + (y - 18.5) ** 2 <= 64: put(x, y, RE if y < 18 else WH)
    for x in range(cx - 8, cx + 8): put(x, 18, OUT)
    for x in range(cx - 2, cx + 2):
        for y in range(17, 21): put(x, y, OUT if x in (cx - 2, cx + 1) or y in (17, 20) else WH)
    for x0 in (2, 70):                                                              # columns
        rect(x0, 28, x0 + 8, 72, LG); rect(x0 + 6, 28, x0 + 8, 72, MG); rect(x0 + 2, 30, x0 + 3, 70, WH)
        rect(x0 - 1, 28, x0 + 9, 31, WH); rect(x0 - 1, 69, x0 + 9, 72, MG)
    rect(10, 28, 70, 72, ST2)
    rect(16, 40, 64, 72, OUT); rect(18, 42, 62, 72, GL3); rect(18, 42, 62, 47, GL1)  # glass doors
    rect(cx - 1, 42, cx + 1, 72, OUT)
    for x in (26, 54): rect(x, 44, x + 1, 72, GL2)
    rect(16, 54, 64, 56, WH)
    for side in (-1, 1):                                                            # drapes + swag
        for y in range(28, 60):
            sw = max(2, int(9 - abs(y - 36) * 0.35))
            for k in range(sw):
                put(cx + side * (29 - k), y, (RE if k % 4 < 2 else DR) if y < 52 else BL)
        for k in range(29):
            x = cx + side * k; y = 29 + int(6 * math.sin(k / 29 * math.pi))
            for d in range(3): put(x, y, BL if d < 2 else NV)
    rect(4, 72, 76, 80, ST1); rect(4, 72, 76, 73, ST3); rect(4, 76, 76, 77, ST2)    # step
    rect(28, 72, 52, 80, RE)
    _outline(im, OUT)
    return im
