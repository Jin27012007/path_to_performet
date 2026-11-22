"""The Lilycove Contest Hall as a refined palace, drawn in Emerald's 3/4 top-down view (roofs seen
from above take most of the height, short fronts below, like the Lilycove Museum):
  - wings: white marble terrace roofs with skylights and a gold parapet, one-storey front with
    pilasters and arched windows;
  - centre block (taller): royal-blue slate roof with a gold border and a golden ribbed dome on a
    drum, pediment and marble colonnade below (the ornate portal is a sprite);
  - castle towers at the ends: conical roof seen from above, round body with slit windows
    (the pennant sprites stand on the tips);
  - marble steps with the red carpet in front.
Canvas 368 x 176 = 23 x 11 metatiles, symmetric about the door column. Colours from palettes
6/7/8/9, converted per 8x8 tile by multipal.py."""
from PIL import Image
import math

S0, S1, S2, S3, S4, S5, O9 = (240, 240, 208), (232, 232, 176), (216, 216, 160), (200, 200, 152), (168, 160, 128), (136, 136, 88), (56, 72, 112)
G1, G2, G3, G4, O7 = (248, 248, 64), (216, 216, 56), (168, 168, 48), (128, 128, 32), (8, 32, 88)
RB, RB2, RB3 = (48, 64, 200), (152, 152, 200), (176, 176, 248)
GL0, GL1, GL3, GL4, O8, WH8 = (208, 216, 248), (160, 200, 248), (96, 136, 224), (72, 104, 200), (56, 72, 112), (248, 248, 248)
RE, DR, YE = (232, 56, 56), (160, 32, 40), (248, 208, 48)

W, H = 368, 176
CX = 184
TCX, TR = 40, 20            # tower centre x / radius (left tower; mirrored)

def build():
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); p = im.load()
    def put(x, y, c):
        if 0 <= x < W and 0 <= y < H: p[x, y] = c + (255,)
    def rect(x0, y0, x1, y1, c):
        for y in range(max(0, y0), min(H, y1)):
            for x in range(max(0, x0), min(W, x1)): put(x, y, c)

    # ---------------- wings (x 56..136): terrace roof seen from above + short front ----------------
    WX0, WX1 = 56, 136
    rect(WX0, 56, WX1, 112, S0)                                   # marble terrace
    rect(WX0, 56, WX1, 60, S2); rect(WX0, 60, WX1, 61, S3)        # back edge (in shade)
    for x in range(WX0 + 8, WX1 - 8, 16):                         # skylights
        rect(x, 72, x + 8, 96, O8); rect(x + 1, 73, x + 7, 95, GL3); rect(x + 1, 73, x + 7, 79, GL1)
        rect(x + 1, 88, x + 7, 89, GL4)
    for y in range(64, 108, 8): rect(WX0 + 2, y, WX1 - 2, y + 1, S1)  # marble slabs
    rect(WX0, 106, WX1, 110, G2); rect(WX0, 110, WX1, 112, G4)    # gold parapet (front edge of the roof)
    rect(WX0, 112, WX1, 168, S1)                                  # front wall (one storey)
    for x in range(WX0, WX1, 16):
        rect(x, 112, x + 3, 168, S3)                              # pilasters
        rect(x, 112, x + 1, 168, S4)
    for x in range(WX0 + 5, WX1 - 4, 16):                         # arched windows
        for y in range(120, 158):
            for xx in range(x, x + 9):
                d = (xx + 0.5 - x - 4.5) ** 2 + (y - 125) ** 2
                if y < 125 and d > 20.25: continue
                edge = xx in (x, x + 8) or y == 157 or (y < 125 and d > 12)
                put(xx, y, O8 if edge else (GL1 if y < 132 else GL3))
        rect(x - 1, 158, x + 10, 160, S4)
    rect(WX0, 164, WX1, 168, S3)

    # ---------------- castle towers (body x 24..56): cone roof seen from above + round body ----------------
    cy = 48
    shades = (S0, S1, S3, S4)
    for y in range(cy, 168):
        for x in range(24, 56): put(x, y, shades[(x - 24) // 8])
    for y in range(64, 168, 16): rect(24, y, 56, y + 1, S2)                    # stone courses
    for y in (80, 112, 144):                                                    # slit windows
        rect(36, y, 44, y + 16, O8); rect(37, y + 1, 43, y + 15, GL3); rect(37, y + 1, 43, y + 5, GL1)
    for y in range(cy - 12, cy + 12):                                           # conical roof (ellipse)
        for x in range(TCX - TR - 2, TCX + TR + 2):
            dx = x + 0.5 - TCX; dy = (y + 0.5 - cy) / 0.55
            r = math.hypot(dx, dy)
            if r > TR + 2: continue
            c = RB3 if r < TR * 0.35 else (RB2 if r < TR * 0.7 else RB)       # cone: light near the tip
            if abs(abs(dx) - r * 0.5) < 1.0 and r > 4: c = O7                  # two seams
            if r > TR: c = G2
            put(x, y, c)
    rect(TCX - 1, cy - 2, TCX + 1, cy + 1, G1)                                  # gold tip
    # ---------------- centre block (x 136..232): taller; slate roof + dome, pediment, colonnade ----------------
    BX0, BX1 = 120, 248
    for y in range(32, 72):                                       # flat top: slate courses
        for x in range(BX0, BX1): put(x, y, RB2 if ((y - 16) // 4) % 2 == 0 else RB3)
    for y in range(72, 88):                                       # front slope (darker)
        for x in range(BX0, BX1): put(x, y, RB if ((y - 72) // 4) % 2 == 0 else O7)
    for x in range(BX0 + 8, BX1 - 8, 16):                         # dormers on the slope
        if abs(x + 4 - CX) < 40: continue
        rect(x, 73, x + 8, 87, S0); rect(x + 2, 76, x + 6, 86, GL3); rect(x + 2, 76, x + 6, 79, GL1)
    rect(BX0, 70, BX1, 72, G2)                                    # gold ridge between flat top and slope
    # dome: ellipse seen from above with ribs, on a drum whose front shows
    DR_Y = 66; RX, RY = 40, 34
    for y in range(DR_Y - 2, DR_Y + 22):                           # drum front band
        for x in range(CX - RX, CX + RX):
            dx = x + 0.5 - CX
            if y > DR_Y + math.sqrt(max(0, 1 - (dx / RX) ** 2)) * 12 + 8: continue
            put(x, y, S0 if dx < -10 else (S1 if dx < 18 else S3))
    for x in range(CX - RX + 6, CX + RX - 6, 10):                  # drum windows
        rect(x, DR_Y + 6, x + 4, DR_Y + 16, O8); rect(x + 1, DR_Y + 7, x + 3, DR_Y + 15, GL3)
    for y in range(DR_Y - RY, DR_Y + 2):                          # golden dome with curved meridian ribs
        for x in range(CX - RX, CX + RX):
            dx = x + 0.5 - CX; dy = y + 0.5 - DR_Y
            if dy > 0 or (dx / RX) ** 2 + (dy / RY) ** 2 > 1: continue
            half_w = RX * math.sqrt(max(1e-6, 1 - (dy / RY) ** 2))
            u = abs(dx) / half_w                                   # 0 centre .. 1 edge of this slice
            c = G1 if u < 0.35 else (G2 if u < 0.75 else G3)
            if dy < -RY * 0.75: c = G1
            if any(abs(u - k) < 0.05 + 0.02 * (1 - u) for k in (0.42, 0.8)): c = G4 if c != G1 else G3
            put(x, y, c)
    for y in range(DR_Y - RY, DR_Y - RY + 3):                     # small base for the crown finial (sprite)
        for x in range(CX - 6, CX + 6): put(x, y, G2 if y < DR_Y - RY else G3)
    # pediment and colonnade (front of the centre block)
    rect(BX0, 88, BX1, 92, G2); rect(BX0, 92, BX1, 94, G4)
    rect(BX0, 94, BX1, 112, S1)                                   # wall behind the pediment
    for y in range(94, 116):
        span = (y - 94) * 64 / 22
        for x in range(int(CX - span), int(CX + span)):
            put(x, y, S0 if abs(x + 0.5 - CX) > span - 2 else S1)
    for x in range(CX - 36, CX + 36):
        y = 106 + int(2 * math.sin(abs(x + 0.5 - CX) / 5.0)); put(x, y, G2); put(x, y + 1, G3)
    rect(BX0, 112, BX1, 116, G2); rect(BX0, 116, BX1, 118, G4)
    rect(BX0, 118, BX1, 168, S1)
    for x in range(BX0, BX1, 16):
        rect(x + 3, 120, x + 13, 166, S0); rect(x + 10, 120, x + 13, 166, S3)
        rect(x + 1, 118, x + 15, 122, S2); rect(x + 1, 162, x + 15, 168, S3); rect(x + 6, 124, x + 7, 160, S2)
    rect(CX - 24, 128, CX + 24, 168, RE); rect(CX - 1, 128, CX + 1, 168, DR)   # red door (portal sprite over it)
    # steps and carpet
    rect(16, 168, 352, 176, S2)
    for y in (168, 171, 174): rect(16, y, 352, y + 1, S4)
    rect(CX - 24, 166, CX + 24, 176, RE)
    for y in (168, 171, 174): rect(CX - 24, y, CX + 24, y + 1, DR)

    # mirror the left tower and wing onto the right side
    for y in range(H):
        for x in range(CX):
            p[2 * CX - 1 - x, y] = p[x, y]
    # outline the silhouette
    snap = [[p[x, y][3] for x in range(W)] for y in range(H)]
    for y in range(H):
        for x in range(W):
            if not snap[y][x] and any(0 <= x + a < W and 0 <= y + b < H and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                put(x, y, O7)
    for y in range(0, 32):                                       # keep the two top rows empty (north street)
        for x in range(W): p[x, y] = (0, 0, 0, 0)
    return im
