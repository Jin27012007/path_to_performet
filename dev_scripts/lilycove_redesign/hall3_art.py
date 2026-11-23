"""Contest Hall, take 3: a small 3D model rendered in Emerald's oblique 3/4 projection, so that roofs,
towers and domes really stand on / meet each other, then finished as pixel art (Emerald palettes,
dark outlines, flat tones, textures on the 8 px grid).

Projection: screen x = X, screen y = K*Y - Z (Y grows towards the viewer/south, Z is height).
Canvas = the whole block, 432 x 176 px (map x 14..40, rows 11..21)."""
import math
import numpy as np
from PIL import Image

W, H, K = 432, 176, 0.5
CX = 216
LIGHT = np.array([0.0, 0.45, 0.89]); LIGHT = LIGHT / np.linalg.norm(LIGHT)
USE_SHADOWS = False

# ---- palette tones (all taken from the BG palettes 6/8/9/12 so the art maps 1:1) ----
OUT = (56, 72, 112)
M0, M1, M2, M3, M4 = (248, 248, 248), (216, 216, 216), (168, 176, 184), (136, 144, 152), (96, 96, 120)   # marble
C1, C2 = (240, 240, 208), (200, 200, 152)                                                    # cream trims
R0, R1, R2, R3, R4 = (208, 216, 248), (160, 184, 248), (96, 136, 224), (72, 104, 200), (56, 72, 112)    # slate
G1, G2, G3 = (248, 248, 136), (232, 232, 104), (176, 176, 96)                                 # gold
GL1, GL2, GL3 = (200, 208, 224), (152, 176, 208), (136, 176, 208)                             # glass
RE, DR, YE, OR, ORD, BL, NV, GR = (232, 56, 56), (160, 32, 40), (248, 208, 48), (248, 144, 40), (216, 96, 32), (48, 112, 224), (32, 48, 120), (56, 168, 64)
CR, YED = (248, 232, 184), (232, 176, 32)
GRD, LGR, SKY = (24, 96, 48), (144, 224, 88), (104, 192, 248)
RG0, RG1, RG2, RF2 = (208, 216, 248), (160, 200, 248), (160, 184, 248), (224, 216, 224)   # roof glass (palette 8)

# ---------------- primitives (left half; mirrored) ----------------
class Poly:      # convex polyhedron: list of (a, b) meaning a.P <= b
    def __init__(s, name, planes): s.name, s.planes = name, planes
class Cyl:
    def __init__(s, name, cx, cy, r, z0, z1): s.name, s.cx, s.cy, s.r, s.z0, s.z1 = name, cx, cy, r, z0, z1
class Ell:       # upper half ellipsoid
    def __init__(s, name, cx, cy, z0, r, rz): s.name, s.cx, s.cy, s.z0, s.r, s.rz = name, cx, cy, z0, r, rz

def box(name, x0, x1, y0, y1, z0, z1):
    return Poly(name, [((1, 0, 0), x1), ((-1, 0, 0), -x0), ((0, 1, 0), y1), ((0, -1, 0), -y0), ((0, 0, 1), z1), ((0, 0, -1), -z0)])
def hip(name, x0, x1, y0, y1, z0, rise, slope):
    """hipped roof over [x0,x1]x[y0,y1] starting at z0, planes of the given slope, capped at z0+rise"""
    return Poly(name, [((0, 0, -1), -z0), ((0, 0, 1), z0 + rise),
                       ((0, slope, 1), z0 + slope * y1), ((0, -slope, 1), z0 - slope * y0),
                       ((slope, 0, 1), z0 + slope * x1), ((-slope, 0, 1), z0 - slope * x0)])
def gable(name, x0, x1, y0, y1, z0, slope):
    """gable roof, ridge along Y (the front face is the pediment)"""
    xm = (x0 + x1) / 2
    return Poly(name, [((0, 0, -1), -z0), ((0, 1, 0), y1), ((0, -1, 0), -y0),
                       ((slope, 0, 1), z0 + slope * x1), ((-slope, 0, 1), z0 - slope * x0)])

def model():
    P = []
    # main wings: marble block, cornice, hipped slate roof (deep, so the roof climbs up the screen)
    P += [box('wall', 64, CX, 176, 320, 0, 48),
          box('cornice', 60, CX, 172, 324, 44, 52),
          hip('roof', 56, 2 * CX - 56, 168, 328, 52, 60, 0.5)]
    # rotunda: a drum rising from the roof (the striped dome sits on it)
    P += [Cyl('drum', CX, 268, 52, 50, 92), Cyl('dcor', CX, 268, 56, 90, 100)]
    # entrance portico (open): door wall recessed behind two columns, entablature, gable + pediment, floor
    P += [box('porch_back', 176, CX, 316, 322, 0, 58),
          Cyl('porch_col', 183, 336, 3, 4, 58),
          box('porch_cor', 177, CX, 314, 340, 58, 66),
          gable('porch_roof', 177, 2 * CX - 177, 314, 340, 66, 0.5),
          box('porch_floor', 174, CX, 320, 344, 0, 4)]
    # towers: two at the front corners (tall), two at the back rising out of the roof
    for (tx, ty, r, h, dr, dz) in ((40, 300, 32, 96, 30, 36), (120, 196, 20, 100, 18, 20)):
        P += [Cyl('tower', tx, ty, r, 0, h), Cyl('tcor', tx, ty, r + 3, h - 8, h + 2), Ell('tdome', tx, ty, h + 2, dr, dz)]
    # front step / plinth
    P += [box('plinth', 0, CX, 300, 346, 0, 4)]
    P += [Ell('bigdome', CX, 268, 100, 52, 36)]
    out = []
    for p in P:           # mirror to the right half
        out.append(p)
        if isinstance(p, Poly):
            # mirror: a.P <= b with P' = (2CX - x, y, z)  ->  (-ax) x + ... <= b - ax * 2CX
            q = Poly(p.name, [((-a[0], a[1], a[2]), b - a[0] * 2 * CX) for a, b in p.planes])
            out.append(q)
        elif isinstance(p, Cyl):
            if p.cx != CX: out.append(Cyl(p.name, 2 * CX - p.cx, p.cy, p.r, p.z0, p.z1))
        elif isinstance(p, Ell):
            if p.cx != CX: out.append(Ell(p.name, 2 * CX - p.cx, p.cy, p.z0, p.r, p.rz))
    return out

def render(prims, h0=-48, h1=H):
    """ray cast every pixel; returns dict of arrays: t (height of hit), prim index, normal, X, Y, Z"""
    sy, sx = np.mgrid[h0:h1, 0:W].astype(float)
    X = sx + 0.5; S = sy + 0.5
    best = np.full(X.shape, -1e9); idx = np.full(X.shape, -1); N = np.zeros(X.shape + (3,)); fid = None
    for i, p in enumerate(prims):
        if isinstance(p, Poly):
            lo = np.full(X.shape, -1e9); hi = np.full(X.shape, 1e9); nb = np.zeros(X.shape, int); ok = np.ones(X.shape, bool)
            for j, (a, b) in enumerate(p.planes):
                ax, ay, az = a; c = ay / K + az; d = b - ax * X - ay * S / K
                if abs(c) < 1e-9: ok &= d >= 0
                elif c > 0:
                    u = d / c; m = u < hi; hi = np.where(m, u, hi); nb = np.where(m, j, nb)
                else: lo = np.maximum(lo, d / c)
            hit = ok & (hi >= lo) & (hi < 1e8)
            t = hi
            nrm = np.array([p.planes[j][0] for j in range(len(p.planes))], float)
            nrm = nrm / np.linalg.norm(nrm, axis=1, keepdims=True)
            n = nrm[nb]
        elif isinstance(p, Cyl):
            q = p.r ** 2 - (X - p.cx) ** 2
            sq = np.sqrt(np.maximum(q, 0))
            tlo = np.maximum(K * (p.cy - sq) - S, p.z0); thi_side = K * (p.cy + sq) - S
            t = np.minimum(thi_side, p.z1); hit = (q >= 0) & (t >= tlo)
            side = thi_side < p.z1
            Yh = (S + t) / K
            n = np.stack([np.where(side, (X - p.cx) / p.r, 0), np.where(side, (Yh - p.cy) / p.r, 0), np.where(side, 0, 1.0)], -1)
        else:
            e = S / K - p.cy
            A = 1 / (K * K * p.r * p.r) + 1 / p.rz ** 2
            B = 2 * (e / (K * p.r * p.r) - p.z0 / p.rz ** 2)
            C = (X - p.cx) ** 2 / p.r ** 2 + e * e / p.r ** 2 + p.z0 ** 2 / p.rz ** 2 - 1
            disc = B * B - 4 * A * C
            t = (-B + np.sqrt(np.maximum(disc, 0))) / (2 * A)
            hit = (disc >= 0) & (t >= p.z0)
            Yh = (S + t) / K
            n = np.stack([(X - p.cx) / p.r ** 2, (Yh - p.cy) / p.r ** 2, (t - p.z0) / p.rz ** 2], -1)
            n = n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-9)
        # nearest = largest t
        nearer = hit & (t > best + 1e-6)
        best = np.where(nearer, t, best)
        idx = np.where(nearer, i, idx); N = np.where(nearer[..., None], n, N)
        fid = np.where(nearer, i * 16 + (nb if isinstance(p, Poly) else (np.where(side, 0, 1) if isinstance(p, Cyl) else 0)), fid) if False else fid
    return dict(idx=idx, N=N, X=X, Z=best, Y=(S + best) / K, sx=sx.astype(int), sy=sy.astype(int), h0=h0)

# ---------------- point-in-solid (cast shadows) ----------------
def inside(p, X, Y, Z):
    if isinstance(p, Poly):
        m = np.ones(X.shape, bool)
        for (a, b) in p.planes: m &= a[0] * X + a[1] * Y + a[2] * Z <= b + 1e-6
        return m
    if isinstance(p, Cyl): return ((X - p.cx) ** 2 + (Y - p.cy) ** 2 <= p.r ** 2) & (Z >= p.z0) & (Z <= p.z1)
    return (((X - p.cx) / p.r) ** 2 + ((Y - p.cy) / p.r) ** 2 + ((Z - p.z0) / p.rz) ** 2 <= 1) & (Z >= p.z0)

def shadows(prims, R):
    hit = R['idx'] >= 0; sh = np.zeros(hit.shape, bool)
    X, Y, Z = R['X'], R['Y'], R['Z']
    for s in range(3, 60, 2):
        Xs, Ys, Zs = X + LIGHT[0] * s, Y + LIGHT[1] * s, Z + LIGHT[2] * s
        for p in prims: sh |= inside(p, Xs, Ys, Zs)
    return sh & hit

# ---------------- finishing ----------------
def finish(prims, R, only=None, skip=()):
    """returns an RGBA image (canvas rows h0..H) of the shaded model with textures and details.
    only: set of names kept (others transparent); skip: names made transparent."""
    idx, N, X, Y, Z, sx, sy = R['idx'], R['N'], R['X'], R['Y'], R['Z'], R['sx'], R['sy']
    hgt, wid = idx.shape
    img = np.zeros((hgt, wid, 4), np.uint8)
    names = np.array([p.name for p in prims] + ['bg'])[idx]
    lum = (N * LIGHT).sum(-1)
    SH = shadows(prims, R)
    Zi = np.floor(Z + 1e-3).astype(int); Xi = np.floor(X).astype(int)
    def setc(mask, c): img[mask] = c + (255,)
    front = N[..., 1] > 0.95; top = N[..., 2] > 0.95
    def ramp_set(m, tone, ramp):
        ramp = np.array(ramp)
        img[m] = np.concatenate([ramp[tone][m], np.full((m.sum(), 1), 255)], -1).astype(np.uint8)
    # glass curtain walls (palette 12): mullions every 16 px, transom, light streaks, concrete base
    for nm in ('wall', 'porch_back'):
        m = names == nm
        setc(m, GL2); setc(m & (Zi > 30), GL1); setc(m & (Zi <= 10), GL3)
        streak = (((Xi + Zi) % 16) < 2) & (Zi > 8) & (Zi < 40)
        setc(m & front & streak, GL1)
        setc(m & front & ((Xi % 16) == 0), M2); setc(m & front & (Zi == 24), M2)
        setc(m & (Zi <= 2), M3); setc(m & top, M1); setc(m & ~front & ~top, M2)
    for nm in ('porch_floor', 'plinth'):
        m = names == nm
        setc(m, M1); setc(m & top, M0); setc(m & front & (Zi <= 1), M2)
        setc(m & top & ((Xi % 16) == 0), M1)
    # white steel cornices and rings
    for nm in ('cornice', 'porch_cor', 'tcor', 'dcor'):
        m = names == nm
        setc(m, M0); setc(m & ~top & (lum < 0.25), M1)
    for p in prims:
        if p.name in ('tcor', 'dcor', 'cornice', 'porch_cor'):
            m = (names == p.name) & front & (Z < (p.z0 if hasattr(p, 'z0') else 0) + 1.5) if p.name in ('tcor', 'dcor') else None
            if m is not None: setc(m, M2)
    setc((names == 'cornice') & front & (Zi <= 45), M2); setc((names == 'porch_cor') & front & (Zi <= 59), M2)
    # glass roofs (palette 8): steel grid, light reflections, white hip frames
    for nm in ('roof', 'porch_roof'):
        m = names == nm
        frontish = N[..., 1] > 0.3
        setc(m & frontish, RG1); setc(m & ~frontish, RG2)
        cu, cv_ = sx % 32, sy % 16                                            # a glint in every pane
        setc(m & frontish & (cv_ >= 3) & (cv_ <= 9) & ((cu - (12 - cv_)) % 32 < 2), RG0)
        setc(m & ((sy % 16) == 15), RF2); setc(m & ((sx % 32) == 0) & frontish, RF2)
        edge = np.zeros(m.shape, bool)
        for dy, dx in ((1, 0), (0, 1), (0, -1)):
            nbn = np.roll(np.roll(N, dy, 0), dx, 1); nbm = np.roll(np.roll(names, dy, 0), dx, 1)
            edge |= m & (nbm == nm) & ((N * nbn).sum(-1) < 0.98)
        setc(edge, M0)
    # towers: concrete pillar on the front, glass to the sides (front towers); all glass (back towers)
    for p in prims:
        if p.name != 'tower': continue
        m = (names == 'tower') & (np.abs(X - p.cx) <= p.r + 0.5)
        ad = np.abs(X - p.cx)
        tone = np.select([ad < 8, ad < 16, ad < 24], [0, 0 if p.r > 24 else 1, 1], 2)    # bands on the 8 px grid
        ramp_set(m, tone, [GL1, GL2, GL3])
        setc(m & (sy % 16 == 15), M2)
        if p.r > 24:
            conc = m & (ad < 16)
            setc(conc, M1); setc(conc & (sy % 32 == 31), M2); setc(conc & (ad >= 15), M2)
        else:
            setc(m & (np.floor(X).astype(int) % 8 == 0), M2)
    for nm in ('drum',):
        m = names == nm
        tone = np.select([lum > 0.4, lum > 0.25], [0, 1], 2)
        ramp_set(m, tone, [GL1, GL2, GL3])
        az = np.arctan2(X - CX, Y - 268)
        setc(m & (np.abs(((az + 0.2) % 0.4) - 0.2) < 0.04), M2)
    pc = names == 'porch_col'
    setc(pc, M1); setc(pc & (X < 183) & (X > 216 - 40) | pc & (X > 249), M2)
    # geodesic glass domes on the towers: triangulated steel frame
    for p in prims:
        if p.name != 'tdome': continue
        m = (names == 'tdome') & (np.abs(X - p.cx) <= p.r + 1)
        az = np.arctan2(X - p.cx, Y - p.cy); lat = np.arcsin(np.clip((Z - p.z0) / p.rz, 0, 1))
        tone = np.select([lum > 0.85, lum > 0.6, lum > 0.35], [0, 1, 2], 3)
        ramp_set(m, tone, [RG0, GL1, GL2, GL3])
        v = lat / (math.pi / 2) * 4; band = np.floor(v)
        u = az / (2 * math.pi) * 14 + 0.5 * (band % 2)
        fu = (u + (v - band) * 0.5) % 1; gu = (u - (v - band) * 0.5) % 1
        line = (np.abs(v - np.round(v)) < 0.09) | (np.minimum(fu, 1 - fu) < 0.06) | (np.minimum(gu, 1 - gu) < 0.06)
        setc(m & line & (v < 3.6), M2)
        setc(m & ((((X - p.cx) * 0.7 - (Z - p.z0)) % 24) < 2) & (lum > 0.5), M0)
    # the big dome: rainbow segments (red, yellow, green, blue), two tones by light
    for p in prims:
        if p.name != 'bigdome': continue
        m = names == 'bigdome'
        az = np.abs(np.arctan2(X - p.cx, Y - p.cy))
        k = (((az + math.pi / 12) // (math.pi / 6)).astype(int)) % 4
        tones = {0: (GR, GRD), 1: (YE, YED), 2: (RE, DR), 3: (BL, NV)}
        lv = np.where(lum > 0.55, 0, 1)
        for kk, tt in tones.items():
            for lvl in range(2): setc(m & (k == kk) & (lv == lvl), tt[lvl])
        sep = np.abs(((az + math.pi / 12) % (math.pi / 6)) - math.pi / 12) > math.pi / 12 - 0.035
        setc(m & sep, M0)
    # cast shadows: one tone darker
    darker = {M0: M1, M1: M2, M2: M3, M3: M4, R0: R1, R1: R2, R2: R3, R3: R4, CR: YE, YE: YED, OR: ORD, BL: NV, G2: G3, G1: G2}
    shm = SH & (names != "bigdome") & USE_SHADOWS
    for a, b in darker.items():
        mm = shm & np.all(img[..., :3] == a, -1); img[mm] = b + (255,)
    img = details(img, prims, R, names)
    # outlines: silhouette + where a nearer surface overlaps a farther one
    sol = img[..., 3] > 0
    out = np.zeros(sol.shape, bool)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nb_sol = np.roll(np.roll(sol, dy, 0), dx, 1)
        nb_Z = np.roll(np.roll(Z, dy, 0), dx, 1); nb_idx = np.roll(np.roll(idx, dy, 0), dx, 1)
        out |= ~sol & nb_sol
        far = sol & nb_sol & (nb_idx != idx) & (Z + 2.5 < nb_Z)
        out |= far
    img[out] = OUT + (255,)
    keep = np.ones(sol.shape, bool)
    if only is not None: keep = np.isin(names, list(only)) | (out & ~np.isin(names, list(skip)))
    if skip: keep &= ~np.isin(names, list(skip))
    img[~keep] = 0
    return Image.fromarray(img.copy(), 'RGBA').copy()

FONT = {'C': ('111', '100', '100', '100', '111'), 'O': ('111', '101', '101', '101', '111'),
        'N': ('101', '111', '111', '111', '101'), 'T': ('111', '010', '010', '010', '010'),
        'E': ('111', '100', '110', '100', '111'), 'S': ('111', '100', '111', '001', '111')}
def screen_art():
    """40 x 16 'CONTEST' screen (palette 6 colours only, so it maps to one BG palette)"""
    a = np.zeros((16, 40, 3), int); a[:] = NV
    a[1:8, 1:39] = RE
    x = 6
    for ch in 'CONTEST':
        for r, row in enumerate(FONT[ch]):
            for c, bit in enumerate(row):
                if bit == '1': a[2 + r, x + c] = M0
        x += 4
    for xx in range(34, 38): a[3:6, xx] = YE if xx < 36 else SKY            # little Poke-star
    for i, col in enumerate((YE, OR, RE, SKY, GR)): a[9:15, 2 + i * 2:4 + i * 2] = col
    for yy in range(9, 15):
        for xx in range(2, 12):
            d = (xx + 0.5 - 7) ** 2 + (yy + 0.5 - 12) ** 2
            if d <= 7: a[yy, xx] = RE if yy < 12 else M0
    for (yy, ln, col) in ((10, 16, LGR), (12, 11, YE), (14, 18, LGR)):
        a[yy, 15:15 + ln] = col
    return a

def details(img, prims, R, names):
    X, Y, Z, sx, sy = R['X'], R['Y'], R['Z'], R['sx'], R['sy']
    def setc(mask, c): img[mask] = c + (255,)
    wing = (names == 'wall') & (R['N'][..., 1] > 0.95)
    sc = screen_art()
    for x0 in (104, 2 * CX - 144):                                    # two 'CONTEST' screens (not mirrored)
        m = wing & (X >= x0) & (X < x0 + 40) & (Z > 16) & (Z <= 32)
        u = np.clip(np.floor(X - x0).astype(int), 0, 39); v = np.clip(np.floor(32 - Z + 1e-3).astype(int), 0, 15)
        img[m] = np.concatenate([sc[v[m], u[m]], np.full((m.sum(), 1), 255)], -1).astype(np.uint8)
    # portico: glass doors in a steel frame, carpet and steps, glass gable
    back = (names == 'porch_back') & (R['N'][..., 1] > 0.95)
    setc(back & (Z > 44), M1); setc(back & (np.abs(Z - 44) < 1), M2)
    door = back & (np.abs(X - CX) <= 22) & (Z <= 42)
    setc(door, OUT); dg = door & (np.abs(X - CX) <= 20) & (Z <= 40)
    setc(dg, GL3); setc(dg & (Z > 30), GL2)
    setc(dg & ((((X - CX) + Z) % 12) < 2) & (Z > 6), GL1)
    setc(dg & ((np.abs(X - CX) < 1) | (np.abs(np.abs(X - CX) - 10) < 0.6)), M3)
    setc(dg & (np.abs(Z - 30) < 0.8), M3)
    flo = (names == 'porch_floor')
    car = flo & (np.abs(X - CX) <= 24)
    setc(car, RE); setc(car & (R['N'][..., 1] > 0.95), DR)
    setc(car & (np.abs(np.abs(X - CX) - 21) < 1), YE)
    ped = (names == 'porch_roof') & (R['N'][..., 1] > 0.95)              # glass pediment with a frame
    setc(ped, GL1); setc(ped & ((np.floor(X).astype(int) % 12) == 0), M2); setc(ped & (Z < 68), M0)
    return img

def _outline(im, col):
    p = im.load(); w, h = im.size
    snap = [[p[x, y][3] for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            if not snap[y][x] and any(0 <= x + a < w and 0 <= y + b < h and snap[y + b][x + a] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                p[x, y] = col + (255,)

def proj(x, y, z): return int(round(x)), int(round(K * y - z))

def ornaments(img, prims, h0):
    """small steel finial on the geodesic domes"""
    p = img.load()
    def put(x, y, c):
        y -= h0
        if 0 <= x < img.width and 0 <= y < img.height: p[x, y] = c + (255,)
    for q in prims:
        if q.name != 'tdome': continue
        ax, ay = proj(q.cx, q.cy, q.z0 + q.rz)
        for y in range(ay - 3, ay + 1): put(ax - 1, y, M2); put(ax, y, M1)
        put(ax - 1, ay - 4, OUT); put(ax, ay - 4, OUT)
    return img

def big_top_details(img, prims, h0):
    """big Poke Ball emblem on the front of the rainbow dome and a silver trophy on top"""
    p = img.load()
    def put(x, y, c):
        y -= h0
        if 0 <= x < img.width and 0 <= y < img.height: p[x, y] = c + (255,)
    q = [d for d in prims if d.name == 'bigdome'][0]
    lat = math.radians(32)
    ex, ey = proj(q.cx, q.cy + q.r * math.cos(lat), q.z0 + q.rz * math.sin(lat))
    rx, ry = 15, 13
    for y in range(ey - ry - 2, ey + ry + 3):
        for x in range(ex - rx - 2, ex + rx + 3):
            d = ((x + 0.5 - ex) / rx) ** 2 + ((y + 0.5 - ey) / ry) ** 2
            if d <= 1.25: put(x, y, OUT)
            if d <= 1: put(x, y, (RE if x - ex < 6 else DR) if y < ey - 1 else (M0 if x - ex < 6 else M1))
            if d <= 1 and abs(y + 0.5 - ey) < 1.6: put(x, y, OUT)
            dc = (x + 0.5 - ex) ** 2 + (y + 0.5 - ey) ** 2
            if dc <= 30: put(x, y, OUT)
            if dc <= 13: put(x, y, M0)
            if dc <= 3: put(x, y, M1)
    for x in range(ex - 5, ex - 1):
        put(x, ey - ry + 3, M0)                                              # shine
    ax, ay = proj(q.cx, q.cy, q.z0 + q.rz)
    cx = ax
    base_img = img; img = Image.new('RGBA', base_img.size, (0, 0, 0, 0)); p = img.load()
    for y in range(ay - 6, ay + 2):                                          # pedestal
        hw = 6 + max(0, y - ay + 3)
        for x in range(cx - hw, cx + hw): put(x, y, M1 if y < ay - 2 else M2)
    top = ay - 29
    for y in range(top, top + 18):                                           # silver cup
        half = 11 if y < top + 5 else 11 - (y - top - 5) * 0.62
        for x in range(int(cx - half), int(cx + half) + 1):
            put(x, y, M0 if x < cx - 4 else (M1 if x < cx + 4 else M2))
    for y in range(top, top + 2):
        for x in range(cx - 11, cx + 12): put(x, y, M0)
    for y in range(top + 3, top + 12): put(cx - 14, y, M1); put(cx + 14, y, M2)  # handles
    for x in range(cx - 14, cx - 10): put(x, top + 3, M1); put(x, top + 11, M1)
    for x in range(cx + 11, cx + 15): put(x, top + 3, M2); put(x, top + 11, M2)
    for y in range(top + 18, top + 24):                                      # stem + base
        for x in range(cx - 2, cx + 3): put(x, y, M1)
    for y in range(ay - 9, ay - 6):
        for x in range(cx - 7, cx + 8): put(x, y, M2 if y > ay - 8 else M1)
    for y in range(top + 5, top + 14):                                       # Poke Ball on the cup
        for x in range(cx - 5, cx + 5):
            d = (x + 0.5 - cx) ** 2 + (y + 0.5 - top - 9.5) ** 2
            if d <= 20: put(x, y, RE if y < top + 9 else M0)
            if d <= 20 and y == top + 9: put(x, y, OUT)
            if d <= 3: put(x, y, M0)
    _outline(img, OUT)
    base_img.alpha_composite(img)
    return base_img

# ---------------- final split: background art + sprites ----------------
SPRITE_PARTS = {'bigdome', 'drum', 'dcor', 'tdome', 'tcor', 'porch_back', 'porch_col', 'porch_cor', 'porch_roof', 'porch_floor'}
def _is_sprite(p): return p.name in SPRITE_PARTS or (p.name == 'tower' and p.cy < 250)   # back towers: whole
def build():
    """returns (bg RGBA 432x176, full RGBA (rows h0..H), sprite RGBA same size, h0)"""
    P = model(); R = render(P)
    full = big_top_details(ornaments(finish(P, R), P, R['h0']), P, R['h0'])
    P2 = [p for p in P if not _is_sprite(p)]; R2 = render(P2)
    bg = ornaments(finish(P2, R2), P2, R2['h0'])
    a = np.array(full); b = np.array(bg)
    spr = a.copy(); spr[~((a != b).any(-1) & (a[..., 3] > 0))] = 0
    # background pixels hidden under opaque sprite pixels: make them cheap (tile-wise)
    h0 = R['h0']; b = b[-h0:-h0 + H].copy(); cover = spr[-h0:-h0 + H, :, 3] > 0
    cands = []
    for ty in range(H // 8):
        for tx in range(W // 8):
            if not cover[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].any(): cands.append(b[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8].copy())
    for t in list(cands):
        cands += [t[:, ::-1], t[::-1], t[::-1, ::-1]]
    cands.append(np.zeros((8, 8, 4), np.uint8))
    C = np.stack(cands)
    for ty in range(H // 8):
        for tx in range(W // 8):
            cv = cover[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            if not cv.any(): continue
            blk = b[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8]
            ok = ((C == blk[None]).all(-1) | cv[None]).all((1, 2))
            if ok.any(): b[ty * 8:ty * 8 + 8, tx * 8:tx * 8 + 8] = C[np.nonzero(ok)[0][-1]]
            else: blk[cv] = 0                    # hidden: transparent, so it cannot sway the tile's palette
    return Image.fromarray(b).copy(), full, Image.fromarray(spr).copy(), h0

GROUPS = [  # name, canvas box (x0, x1, y0, y1) on the 16 px grid, anchor_up, column/row split
    ('hall_tdb_l', (96, 144, -32, 48), 0, None), ('hall_tdb_r', (288, 336, -32, 48), 0, None),
    ('hall_tdo_l', (0, 80, -16, 80), 1, None), ('hall_tdo_r', (352, 432, -16, 80), 1, None),
    ('hall_porch', (176, 256, 64, 176), 2, None),
    ('hall_dome', (144, 288, -32, 112), 0, ((5, 4), (5, 4))),
]
def sprites():
    """splits the sprite layer into the GROUPS; returns {name: RGBA crop}"""
    P = model(); R = render(P)
    bg, full, spr, h0 = build()
    a = np.array(spr); hgt = a.shape[0]
    names = np.array([p.name for p in P] + ['bg'])[R['idx']]
    X = R['X']
    gi = np.full(names.shape, -1)
    def gidx(n): return [g[0] for g in GROUPS].index(n)
    m = a[..., 3] > 0
    gi[m & np.isin(names, ['bigdome', 'drum', 'dcor'])] = gidx('hall_dome')
    gi[m & np.isin(names, ['porch_back', 'porch_col', 'porch_cor', 'porch_roof', 'porch_floor'])] = gidx('hall_porch')
    td = m & ((names == 'tdome') | (names == 'tcor') | ((names == 'tower') & (np.abs(X - CX) < 120) & (np.abs(X - CX) > 70)))
    gi[td & (X < 96)] = gidx('hall_tdo_l'); gi[td & (X >= 96) & (X < CX)] = gidx('hall_tdb_l')
    gi[td & (X > 2 * CX - 96)] = gidx('hall_tdo_r'); gi[td & (X >= CX) & (X <= 2 * CX - 96)] = gidx('hall_tdb_r')
    for _ in range(3):                       # outlines next to a part join it
        un = m & (gi < 0)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = np.roll(np.roll(gi, dy, 0), dx, 1)
            take = un & (nb >= 0) & (gi < 0); gi[take] = nb[take]
    sy = np.arange(hgt)[:, None] + h0; sx = np.arange(W)[None, :]
    for k, (n, (x0, x1, y0, y1), up, sp) in enumerate(GROUPS):   # ornaments (flags, trophy): by box
        inb = (sx >= x0) & (sx < x1) & (sy >= y0) & (sy < y1)
        take = m & (gi < 0) & inb; gi[take] = k
    out = {}
    for k, (n, (x0, x1, y0, y1), up, sp) in enumerate(GROUPS):
        sel = gi == k
        ys, xs = np.nonzero(sel)
        if len(ys) and (xs.min() < x0 or xs.max() >= x1 or ys.min() + h0 < y0 or ys.max() + h0 >= y1):
            print('WARNING %s spills: x %d..%d y %d..%d' % (n, xs.min(), xs.max(), ys.min() + h0, ys.max() + h0))
        im = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
        for (y, x) in zip(ys, xs):
            if x0 <= x < x1 and y0 <= y + h0 < y1: im[y + h0 - y0, x - x0] = a[y, x]
        out[n] = Image.fromarray(im).copy()
    left = m & (gi < 0)
    if left.any(): print('WARNING: %d sprite pixels in no group' % left.sum())
    return bg, out
