"""Lilycove Museum, contemporary style (after the user's reference), Emerald 3/4 view:
standing-seam metal gable roof with hipped ends, white walls with tall windows, a central portico with
a pediment and columns, glass doors. 160 x 96 px (10 x 6 metatiles), doors in metatiles (4,5) and (5,5).
Everything is symmetric and on the 8 px grid so tiles repeat / mirror. Colours: BG palette 12 only."""
from PIL import Image

W, H = 160, 96
OUT = (64, 72, 104); DK = (96, 96, 120)
TL = (96, 152, 168); TD = (64, 112, 136)          # teal roof (palette 12 slots 14, 15)
WH, LG, MG, GG, GY = (248, 248, 248), (216, 216, 216), (168, 176, 184), (136, 144, 152), (128, 128, 136)
GL1, GL2, GL3 = (200, 208, 224), (152, 176, 208), (136, 176, 208)

def building():
    """3/4 view: a tall hipped metal roof (standing seams) seen from above, crossed in the middle by the
    portico's own gable roof (its two slopes visible: lit left, shaded right) that runs from the main
    ridge forward to a pediment; low white walls with tall windows below."""
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); p = im.load()
    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c + (255,)
    def rect(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)): put(x, y, c)
    RT, RB = 16, 56                                        # top of the central roof, eave row
    # side roofs: one rectangular metal slab behind, seen from above (standing seams every 8 px)
    ST = 24
    for y in range(ST, RB):
        for x in range(W):
            c = GG
            if x % 8 in (3, 4): c = MG if x % 8 == 3 else GY
            put(x, y, c)
    rect(0, ST, W, ST + 3, MG); rect(0, ST, W, ST + 1, WH)            # back edge (cap)
    rect(112, ST + 3, 116, RB, GY)                                     # shadow of the central roof
    CL, CR, AP = 48, 112, 40                                # low pediment: 1:2 slope, apex at y 40
    def ped_top(x): return AP + (abs(2 * x - 159) - 1) // 4
    for y in range(RT - 8, RB):
        for x in range(CL, CR):
            if y >= ped_top(x): continue
            c = TL                                               # the central roof in teal (the sides stay grey)
            if y % 8 == 7: c = TD                                # seams
            if x in (79, 80): c = GL1                            # ridge
            put(x, y, c)
    rect(CL, RT - 8, CL + 1, RB, OUT); rect(CR - 1, RT - 8, CR, RB, OUT)
    rect(CL, RT - 8, CR, RT - 4, TD); rect(CL + 1, RT - 8, CR - 1, RT - 7, GL1)      # ridge cap of the central roof      # the gable's side edges
    # pediment (front of the cross gable), white with a grey frame
    for x in range(CL, CR):
        t = ped_top(x)
        for y in range(t, RB): put(x, y, WH)
        put(x, t, MG)
    for x in range(CL, CR): put(x, RB - 1, MG)
    # eave / cornice
    rect(0, RB, W, RB + 3, WH); rect(0, RB + 3, W, RB + 4, MG)
    # low walls with tall windows (bands on the 8 px grid)
    WT, WB = RB + 4, 88
    rect(0, WT, W, WB, LG)
    for bx in (16, 32, 120, 136):
        rect(bx, 64, bx + 8, 85, OUT)
        rect(bx + 1, 65, bx + 7, 84, GL2)
        rect(bx + 1, 65, bx + 7, 72, GL1)
        rect(bx + 1, 78, bx + 7, 84, GL3)
    for x in (8, 151): rect(x, WT, x + 1, WB, MG)
    rect(0, WB, W, H - 1, MG); rect(0, H - 1, W, H, GY)
    # portico under the pediment: shaded porch, four columns, glass doors, steps
    rect(CL, WT, CR, WB, DK)
    rect(64, 68, 96, WB, OUT); rect(65, 69, 95, WB, GL2); rect(65, 69, 95, 75, GL1); rect(79, 69, 81, WB, OUT)
    for cx in (52, 60, 96, 104):
        rect(cx, WT, cx + 4, WB, WH)
    rect(CL - 8, WB, CR + 8, H, WH); rect(CL - 8, WB + 2, CR + 8, WB + 3, MG)
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
