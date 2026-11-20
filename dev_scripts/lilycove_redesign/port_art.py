"""Pixel art for the Lilycove port (drawn in the festival palette, index 0 = transparent).

Every function returns a canvas (list of rows of palette indices) whose size is a
multiple of 16; build_city_tileset.py cuts it into metatiles.
"""
import math
from festival_tiles import canvas, rect, px, WH, CR, YE, OR, RE, DR, BR, LB, BL, NV, LG, GR, DG, BN, DB

# ---------------------------------------------------------------- cruise ship (240x80, bow to the left)
def cruise_ship():
    W, H = 240, 80
    c = canvas(W, H)
    def hull_left(y):  return int(8 + max(0, y - 40) * 0.55)
    def hull_right(y): return int(234 - max(0, y - 58) * 0.9)
    # --- hull
    for y in range(40, 72):
        for x in range(hull_left(y), hull_right(y)):
            c[y][x] = WH
    for y in range(40, 72):                       # outline
        px(c, hull_left(y), y, LB); px(c, hull_right(y) - 1, y, LB)
    for x in range(hull_left(40), hull_right(40)): c[40][x] = LB
    for y in range(44, 46):                       # blue accent stripe
        for x in range(hull_left(y) + 1, hull_right(y) - 1): c[y][x] = BL
    for y in range(63, 72):                       # dark hull bottom
        for x in range(hull_left(y) + 1, hull_right(y) - 1): c[y][x] = NV if y > 64 else BL
    for x in range(16, 228, 8):                   # portholes (two rows)
        for (yy, xo) in ((50, 0), (56, 4)):
            xx = x + xo
            if hull_left(yy) + 3 < xx < hull_right(yy) - 4:
                rect(c, xx, yy, xx + 2, yy + 2, NV); px(c, xx, yy, LB)
    for x in range(30, 52):                       # anchor + name plate at the bow
        if x % 2 == 0: px(c, x, 47, NV)
    rect(c, 22, 50, 25, 54, DB)
    # --- level 1 (promenade deck)
    rect(c, 36, 30, 220, 40, WH)
    for x in range(36, 220): c[30][x] = LB; c[39][x] = LB
    for x in range(40, 216, 8):                   # big windows
        rect(c, x, 33, x + 6, 37, BL); rect(c, x, 33, x + 6, 34, LB)
    # lifeboats hanging on the side
    for x in range(56, 200, 24):
        rect(c, x, 27, x + 14, 31, OR); rect(c, x + 1, 26, x + 13, 27, OR)
        for xx in range(x, x + 14, 2): px(c, xx, 30, DR)
    # --- level 2 (cabins + bridge at the front)
    rect(c, 60, 18, 204, 27, WH)
    for x in range(60, 204): c[18][x] = LB; c[26][x] = LB
    for x in range(66, 200, 8): rect(c, x, 21, x + 4, 24, NV)
    rect(c, 60, 19, 78, 26, WH); rect(c, 62, 20, 76, 24, NV)   # bridge windows
    for x in range(62, 76, 3): px(c, x, 20, LB)
    # pool on the sun deck (seen in perspective) + railing
    rect(c, 120, 14, 160, 18, LB); rect(c, 123, 15, 157, 17, BL)
    for x in range(84, 204, 2): px(c, x, 14, LB)
    # --- funnel (red with white band and black top), slightly raked
    for y in range(2, 18):
        x0 = 176 + (18 - y) // 4
        rect(c, x0, y, x0 + 18, y + 1, RE)
        if 7 <= y <= 9: rect(c, x0, y, x0 + 18, y + 1, WH)
        if y <= 4: rect(c, x0, y, x0 + 18, y + 1, DB)
        px(c, x0, y, DR)
    # mast and flags at the bow
    for y in range(6, 30): px(c, 70, y, DB)
    for i, col in enumerate((RE, YE, BL, GR, RE, YE)):
        rect(c, 46 + i * 4, 12 + i * 3, 49 + i * 4, 15 + i * 3, col)
    # --- foam along the waterline
    for x in range(10, 232):
        if (x * 7) % 5 < 2: px(c, x, 72, WH)
        if (x * 3) % 7 == 0: px(c, x, 73, LB)
    return c

# ---------------------------------------------------------------- market stall (32x32)
def stall(goods):
    c = canvas(32, 32)
    # posts
    rect(c, 2, 12, 4, 31, BN); rect(c, 28, 12, 30, 31, BN)
    # awning
    for y in range(1, 12):
        for x in range(1, 31):
            c[y][x] = RE if (x // 4) % 2 == 0 else WH
    for x in range(1, 31): c[1][x] = DR
    for x in range(1, 31):                        # scalloped edge
        if x % 4 in (1, 2): px(c, x, 12, RE if (x // 4) % 2 == 0 else WH)
        px(c, x, 11, DR if x % 4 == 0 else c[11][x])
    # counter
    rect(c, 3, 22, 29, 31, BN)
    for x in range(3, 29): c[22][x] = CR; c[23][x] = OR; c[30][x] = DB
    for x in range(6, 29, 6):
        for y in range(24, 30): px(c, x, y, DB)
    # shadow under the awning
    for x in range(5, 27):
        if x % 2: px(c, x, 13, DB)
    # goods on the counter
    if goods == 'fish':
        for i, x in enumerate(range(5, 27, 6)):
            rect(c, x, 18, x + 5, 21, LB if i % 2 else BL); px(c, x + 5, 19, BL); px(c, x + 1, 19, NV)
        rect(c, 4, 16, 28, 18, LB)               # ice
    elif goods == 'fruit':
        cols = (OR, RE, YE, GR, OR, RE)
        for i, x in enumerate(range(5, 27, 4)):
            rect(c, x, 18, x + 3, 21, cols[i % len(cols)]); px(c, x + 1, 18, WH)
        for i, x in enumerate(range(7, 25, 4)):
            rect(c, x, 16, x + 3, 18, cols[(i + 2) % len(cols)])
    else:  # souvenirs: little flags, ribbons and a poster of the season
        for i, x in enumerate(range(5, 27, 4)):
            rect(c, x, 16, x + 1, 22, DB); rect(c, x + 1, 16, x + 4, 19, (RE, BL, YE, GR)[i % 4])
        rect(c, 12, 14, 20, 16, YE)
    return c

# ---------------------------------------------------------------- small fishing boat (32x16, bow right)
def fishing_boat():
    c = canvas(32, 16)
    for y in range(3, 14):
        half = 5.5
        dy = abs(y - 8) / half
        x0 = int(2 + dy * dy * 3)
        x1 = int(30 - dy * 10)
        for x in range(x0, x1): c[y][x] = BN
        px(c, x0, y, DB); px(c, x1 - 1, y, DB)
    for x in range(3, 24): px(c, x, 3, DB); px(c, x, 13, DB)
    for y in range(5, 12):                       # inner deck
        dy = abs(y - 8) / 4.0
        for x in range(int(5 + dy * 2), int(25 - dy * 6)): c[y][x] = CR
    for x in range(4, 26):                       # coloured rim (red / blue by palette)
        if c[4][x]: px(c, x, 4, RE)
        if c[12][x]: px(c, x, 12, RE)
    rect(c, 6, 6, 12, 11, WH); rect(c, 7, 7, 11, 9, NV)   # small cabin
    rect(c, 16, 7, 19, 10, OR)                            # buoy / crate
    for x in range(13, 23, 2): px(c, x, 10, DB)           # net
    for x in range(1, 31):                                # ripples
        if x % 5 == 0: px(c, x, 14, LB)
    return c

ART = {
    'cruise': cruise_ship,
    'stall_fish': lambda: stall('fish'),
    'stall_fruit': lambda: stall('fruit'),
    'stall_souvenir': lambda: stall('souvenir'),
    'boat': fishing_boat,
}
