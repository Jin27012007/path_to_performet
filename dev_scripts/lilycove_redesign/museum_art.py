"""Lilycove Museum, contemporary style (after the user's reference), Emerald 3/4 view:
standing-seam metal gable roof with hipped ends, white walls with tall windows, a central portico with
a pediment and columns, glass doors. 160 x 96 px (10 x 6 metatiles), doors in metatiles (4,5) and (5,5).
Everything is symmetric and on the 8 px grid so tiles repeat / mirror. Colours: BG palette 12 only."""
from PIL import Image

W, H = 160, 96
OUT = (64, 72, 104); DK = (96, 96, 120)
WH, LG, MG, GG, GY = (248, 248, 248), (216, 216, 216), (168, 176, 184), (136, 144, 152), (128, 128, 136)
GL1, GL2, GL3 = (200, 208, 224), (152, 176, 208), (136, 176, 208)

def building():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); p = im.load()
    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c + (255,)
    def rect(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)): put(x, y, c)
    # roof: front slope seen from above, hipped ends at 45 degrees, standing seams every 8 px
    RT, RB = 8, 40                                         # ridge row, eave row
    for y in range(RT, RB):
        inset = RB - y                                     # 45-degree hips: (0,40) -> (32,8)
        for x in range(inset, W - inset):
            c = GG
            if x % 8 == 0: c = MG                          # seam (lit)
            elif x % 8 == 1: c = GY                        # seam shadow
            if x < inset + 2 or x >= W - inset - 2: c = MG # hip edge trim
            put(x, y, c)
    rect(32, RT - 4, W - 32, RT, MG); rect(32, RT - 4, W - 32, RT - 3, WH)   # ridge cap
    # eave / cornice
    rect(0, RB, W, RB + 4, WH); rect(0, RB + 3, W, RB + 4, MG)
    # walls with tall windows every 16 px (glass bays), pilasters between them
    WT, WB = RB + 4, 88
    rect(0, WT, W, WB, LG)
    for bx in range(8, W - 8, 16):
        if 56 <= bx < 104: continue                        # the portico covers the centre
        rect(bx, 48, bx + 8, 88, OUT)                       # window bands on the 8 px grid (tiles repeat)
        rect(bx + 1, 49, bx + 7, 87, GL2)
        rect(bx + 1, 49, bx + 7, 56, GL1)
        rect(bx + 1, 80, bx + 7, 87, GL3)
    for x in range(0, W, 16): rect(x, WT, x + 1, WB, MG)  # pilaster joints
    rect(0, WB, W, H - 2, MG); rect(0, H - 2, W, H, GY)   # plinth
    # portico: pediment (45-degree), entablature, four columns, glass doors, steps
    PL, PR = 56, 104                                       # 48 px wide, centred on x = 80
    for y in range(24, RB):                                # pediment triangle (apex at y 24)
        half = y - 24
        for x in range(80 - half, 80 + half):
            if PL <= x < PR: put(x, y, WH if y > 26 + abs(x - 80) - (y - 24) + 2 else MG)
    for y in range(24, RB):
        half = y - 24
        put(80 - half, y, OUT); put(80 + half - 1, y, OUT)
    rect(PL - 4, RB, PR + 4, RB + 6, WH); rect(PL - 4, RB + 5, PR + 4, RB + 6, MG)   # entablature
    rect(PL, RB + 6, PR, WB, DK)                           # shaded porch behind the columns
    rect(64, 64, 96, WB, OUT); rect(65, 65, 95, WB, GL2); rect(65, 65, 95, 72, GL1)   # glass doors
    rect(79, 65, 81, WB, OUT)
    for cx in (58, 70, 86, 98):                            # columns (4 px wide)
        rect(cx, RB + 6, cx + 4, WB, WH); rect(cx + 3, RB + 6, cx + 4, WB, MG)
    rect(PL - 4, WB, PR + 4, H - 2, WH); rect(PL - 4, WB + 3, PR + 4, WB + 4, MG)   # steps
    # silhouette outline
    snap = [[p[x, y][3] for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if not snap[y][x] and any(0 <= x + a < W and 0 <= y + b < H and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                p[x, y] = OUT + (255,)
    return im

def sculpture():
    """16 x 32: a modern steel loop on a white pedestal (symmetric, so the second one is a mirror)"""
    im = Image.new('RGBA', (16, 32), (0, 0, 0, 0)); p = im.load()
    def put(x, y, c):
        if 0 <= x < 16 and 0 <= y < 32: p[x, y] = c + (255,)
    for y in range(20, 31):                                # pedestal
        for x in range(3, 13): put(x, y, WH if y < 22 else (LG if 5 <= x <= 10 else MG))
    for y in range(2, 20):                                 # loop: an upright ring with a twist
        for x in range(2, 14):
            d = ((x + 0.5 - 8) / 5.5) ** 2 + ((y - 11) / 8.5) ** 2
            if 0.45 <= d <= 1: put(x, y, MG)
            if 0.45 <= d <= 0.62: put(x, y, WH)
    snap = [[p[x, y][3] for x in range(16)] for y in range(32)]
    for y in range(32):
        for x in range(16):
            if not snap[y][x] and any(0 <= x + a < 16 and 0 <= y + b < 32 and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                p[x, y] = OUT + (255,)
    return im
