"""Simple low-income cottage for district 2: front-gable (triangular) roof in Emerald's 3/4 view,
board walls. 64 x 64 px (4 x 4 metatiles), door in metatile (1, 3).
Colours are taken from BG palette 9 (brown roof, cream walls); variants recolour by palette INDEX,
so a variant drawn with the same indices in another palette costs no extra tiles."""
from PIL import Image
import multipal

W = H = 64
def design():
    """index canvas: roof light/mid/dark = 4/5/6, outline 7, boards light/mid/shadow = 1/2/3,
    glass 11/9, frame 8"""
    c = [[0] * W for _ in range(H)]
    def put(x, y, v):
        if 0 <= x < W and 0 <= y < H: c[y][x] = v
    WALL_T, WALL_B = 44, 62            # front wall rows
    GL, GR, APEX = 4, 59, 16           # gable base x range and apex row (45-degree edges through tile corners)
    D = 16                             # roof depth on screen
    cx = (GL + GR) / 2
    # roof planes (behind the gable): band between each gable edge and the same edge D px higher
    for y in range(0, H):
        for x in range(W):
            # height of the gable edge at column x
            ey = WALL_T - min(x - GL, GR - x) if GL <= x <= GR else None
            if ey is None: continue
            if ey - D <= y < ey and y >= APEX - D - 2:
                k = (x - GL) if x < cx else (GR - x)              # mirrored planes (tiles flip)
                v = 5
                if k % 4 == 1: v = 6                                  # course lines
                if k % 4 == 3 and y > ey - 3: v = 4                   # lit lower edge of each course
                put(x, y, v)
    # ridge cap
    for y in range(APEX - D, APEX + 1):
        put(int(cx), y, 4); put(int(cx) + 1, y, 4)
    # gable triangle: horizontal boards
    for y in range(APEX, WALL_T):
        half = y - APEX
        for x in range(int(cx - half), int(cx + half) + 2):
            if GL <= x <= GR: put(x, y, 3 if (y % 4) == 3 else 1)
    # fascia trim along the gable edges (light) + outline above it
    for x in range(GL, GR + 1):
        ey = WALL_T - min(x - GL, GR - x)
        put(x, ey, 1); put(x, ey - 1, 2)
    # eave shadow line and wall
    for x in range(GL, GR + 1): put(x, WALL_T, 7)
    for y in range(WALL_T + 1, WALL_B + 1):
        for x in range(GL + 2, GR - 1):
            put(x, y, 3 if (y % 4) == 0 else 2)
            if x in (GL + 2, GR - 2): put(x, y, 3)
    for x in range(GL + 2, GR - 1): put(x, WALL_T + 1, 3)
    # door (metatile column 1: x 16..31), window (metatile columns 2..3)
    for y in range(48, WALL_B + 1):
        for x in range(19, 29):
            edge = x in (19, 28) or y == 48
            put(x, y, 7 if edge else (6 if x in (20, 27) else 5))
    for y in range(48, 57):                                  # window: two mirrored 8 px halves (x 40..55)
        for x in range(40, 56):
            edge = x in (40, 55) or y in (48, 56)
            put(x, y, 7 if edge else (8 if x in (47, 48) or y == 52 else (11 if y < 52 else 9)))
    for x in range(39, 57): put(x, 57, 1)                                  # sill
    # outline around the silhouette
    snap = [row[:] for row in c]
    for y in range(H):
        for x in range(W):
            if snap[y][x]: continue
            if any(0 <= x + a < W and 0 <= y + b < H and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c[y][x] = 7
    for x in range(GL + 1, GR): c[WALL_B + 1][x] = 7 if WALL_B + 1 < H else 0
    return c

VARIANTS = {'cottage_brown': 9, 'cottage_slate': 8, 'cottage_lilac': 7}
def canvas(slot):
    """the same indices in palette `slot` (one palette for the whole house)"""
    return design(), [[slot] * 8 for _ in range(8)]

def preview(slot):
    c, g = canvas(slot)
    return multipal.preview(c, g)
