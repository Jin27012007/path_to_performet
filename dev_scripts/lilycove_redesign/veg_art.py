"""Coconut palm drawn in the PRIMARY tree palette (slot 2), so it shares colours, outline and
shading with Emerald's own trees: dark green outline, three greens on the fronds, brown ringed
trunk, coconuts under the crown. 32x48, top layer."""
import math
PAL_SLOT = 2
# palette 2 indices (General tileset): trees
OUTL, G1, G2, G3, TR_SH, TR, TR_DK, TR_HI = 4, 1, 2, 3, 6, 7, 8, 9

def palm():
    W, H = 32, 48
    c = [[0] * W for _ in range(H)]
    def put(x, y, v):
        if 0 <= x < W and 0 <= y < H: c[y][x] = v
    # trunk: gentle curve, 3 px wide, darker rings every 3 px
    for y in range(16, 46):
        t = (y - 16) / 29.0
        x0 = int(round(15 + 2.0 * math.sin(t * math.pi * 0.9)))
        for dx in range(3):
            v = (TR if dx == 0 else TR_SH)
            if (y - 16) % 3 == 0: v = TR_SH if dx == 0 else TR_DK
            put(x0 + dx, y, v)
    # fronds: a curved rib with leaflets hanging from it (classic pixel-art coconut palm)
    cx, cy = 16, 14
    fronds = [(-1.0, -0.5, 14, 0.55), (1.0, -0.5, 14, 0.55), (-0.55, -1.0, 11, 0.5), (0.55, -1.0, 11, 0.5),
              (-1.0, 0.15, 13, 0.6), (1.0, 0.15, 13, 0.6), (-0.1, -1.0, 8, 0.4)]
    pix = {}
    def mark(x, y, v):
        x = int(round(x)); y = int(round(y))
        if (x, y) not in pix or v < pix[(x, y)]: pix[(x, y)] = v     # lighter wins (G1 < G2 < G3)
    for (dx, dy, L, droop) in fronds:
        n = math.hypot(dx, dy); dx, dy = dx / n, dy / n
        steps = L * 3
        prev = None
        for s_ in range(steps + 1):
            t = s_ / steps
            x = cx + dx * L * t; y = cy + dy * L * t + droop * L * t * t
            mark(x, y, G1 if t < 0.85 else G2)                       # rib
            mark(x, y + 1, G2)
            if s_ % 2 == 0 and t > 0.08:                              # leaflets hanging down
                ln = 4.2 * math.sin(math.pi * min(1.0, t * 1.1)) + 0.8
                for k in range(1, int(ln) + 1):
                    lx = x + (-dx * 0.6) * k * 0.35 + (0.35 if dx > 0 else -0.35) * k * 0.2
                    mark(lx, y + 1 + k, G2 if k < ln * 0.35 else G3)
    for (x, y), v in pix.items(): put(x, y, v)
    # coconuts under the crown
    for (x, y) in ((14, 15), (16, 16), (17, 15)):
        for (ax, ay) in ((0, 0), (1, 0), (0, 1), (1, 1)): put(x + ax, y + ay, TR if (ax, ay) != (0, 0) else TR_HI)
    # dark outline around everything (Emerald style)
    out = [row[:] for row in c]
    for y in range(H):
        for x in range(W):
            if c[y][x] == 0 and any(0 <= x + a < W and 0 <= y + b < H and c[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                out[y][x] = OUTL if y < 20 or any(0 <= x + a < W and c[y][x + a] in (G1, G2, G3) for a in (-1, 1)) else TR_DK
    for x in range(11, 21):                               # small shadow at the foot
        if out[46][x] == 0: out[46][x] = OUTL if x in (11, 20) else 14
    return out
