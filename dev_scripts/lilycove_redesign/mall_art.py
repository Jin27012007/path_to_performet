"""Decorations for the new Lilycove shopping mall, drawn in Emerald style with the
festival palette 6: the big contest screen (telão), the Poké Ball on the roof and the
string of pennants. They are top layers over the mall wall (see build_city_tileset)."""
_, WH, CR, YE, OR, RE, DR, BR, LB, BL, NV, LG, GR, DG, BN, DB = range(16)

def canvas(w, h): return [[0] * w for _ in range(h)]

FONT = {   # 5x7
    'P': ["1111.", "1...1", "1...1", "1111.", "1....", "1....", "1...."],
    'O': [".111.", "1...1", "1...1", "1...1", "1...1", "1...1", ".111."],
    'K': ["1...1", "1..1.", "1.1..", "11...", "1.1..", "1..1.", "1...1"],
    'E': ["11111", "1....", "1....", "1111.", "1....", "1....", "11111"],
    'M': ["1...1", "11.11", "1.1.1", "1.1.1", "1...1", "1...1", "1...1"],
    'N': ["1...1", "11..1", "1.1.1", "1..11", "1...1", "1...1", "1...1"],
    'C': [".111.", "1...1", "1....", "1....", "1....", "1...1", ".111."],
    'T': ["11111", "..1..", "..1..", "..1..", "..1..", "..1..", "..1.."],
    'S': [".1111", "1....", "1....", ".111.", "....1", "....1", "1111."],
}
def text(c, s, x0, y0, col, shadow=None):
    x = x0
    for ch in s:
        g = FONT[ch]
        for y in range(7):
            for i in range(5):
                if g[y][i] == '1':
                    if shadow is not None: c[y0 + y + 1][x + i + 1] = shadow
        for y in range(7):
            for i in range(5):
                if g[y][i] == '1': c[y0 + y][x + i] = col
        x += 6

def star(c, cx, cy, col):
    for d in range(-2, 3):
        c[cy][cx + d] = col; c[cy + d][cx] = col
    c[cy - 1][cx - 1] = c[cy - 1][cx + 1] = c[cy + 1][cx - 1] = c[cy + 1][cx + 1] = WH

def screen():
    """96x32 LED screen showing the contest (frame, stage lights, title, stage)"""
    w, h = 96, 32; c = canvas(w, h)
    for y in range(h):
        for x in range(w):
            if x < 3 or x >= w - 3 or y < 2 or y >= h - 2:
                c[y][x] = NV                                   # frame
            else:
                c[y][x] = BL
                if y >= 23: c[y][x] = DR if y >= 26 else RE                    # stage
    for x in range(3, w - 3):                                                  # stage lights (8 px period)
        if x % 8 == 3: c[24][x] = YE
        if x % 8 == 7: c[27][x] = OR
    for x in range(3, w - 3): c[2][x] = LB if x % 2 else BL                     # glass highlight
    text(c, 'POKEMON', 27, 4, YE, NV)
    text(c, 'CONTEST', 27, 13, WH, NV)
    star(c, 15, 12, YE); star(c, 80, 12, YE)
    for x in (44, 52): c[h - 1][x] = NV; c[h - 1][x + 1] = NV                  # mounts
    return c

def pokeball():
    """32x32 Poké Ball sign standing on the roof edge"""
    c = canvas(32, 32); cx, cy, r = 15.5, 15.5, 14.5
    for y in range(32):
        for x in range(32):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
            if d <= r:
                if d > r - 1.3: c[y][x] = NV
                elif abs(y - cy) <= 1.5: c[y][x] = NV
                elif y < cy: c[y][x] = RE if (x - cx) + (y - cy) > -14 else OR
                else: c[y][x] = WH if (x - cx) - (y - cy) < 12 else CR
    for y in range(32):
        for x in range(32):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
            if d <= 5.5: c[y][x] = NV if d > 4 else (WH if d > 2.5 else CR)
    for (x, y) in ((8, 6), (9, 6), (7, 7), (8, 7), (7, 8)): c[y][x] = WH       # shine
    return c

PENNANT_COLS = [(RE, YE), (GR, BL), (OR, LB)]
def pennants(k):
    """16x16 string of two triangular flags (variant k = colours), hanging from the roof"""
    c = canvas(16, 16)
    for x in range(16): c[1][x] = NV
    for i, col in enumerate(PENNANT_COLS[k % 3]):
        x0 = 1 + i * 8
        for y in range(2, 9):
            half = (8 - y) * 3 // 6
            for x in range(x0 + 3 - half - 0, x0 + 3 + half + 1):
                if 0 <= x < 16: c[y][x] = col
        c[2][x0] = c[2][x0 + 6] = NV
    return c

def ticker():
    """96x16 LED band over the doors: 'POKEMON CONTEST' with stage lights"""
    w, h = 96, 16; c = canvas(w, h)
    for y in range(h):
        for x in range(w):
            if x == 0 or x == w - 1 or y == 0 or y == h - 1: c[y][x] = NV
            elif y == 1: c[y][x] = LB
            elif y >= 13: c[y][x] = RE
            else: c[y][x] = BL
    for x in range(2, w - 2):
        if x % 8 == 3: c[13][x] = YE
    text(c, 'POKEMON', 3, 4, YE, NV)
    text(c, 'CONTEST', 51, 4, WH, NV)
    return c

def carpet_mat():
    """32x16 small horizontal red carpet (doormat) for a double door"""
    w, h = 32, 16; c = canvas(w, h)
    for y in range(h):
        for x in range(w):
            edge = min(x, w - 1 - x, y, h - 1 - y)
            c[y][x] = DR if edge == 0 else (YE if edge == 1 else (RE if (x + y) % 4 else DR) if edge > 2 else RE)
    return c
