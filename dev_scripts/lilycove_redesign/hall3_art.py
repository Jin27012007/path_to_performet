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
    # main wings: marble block, cornice, hipped slate roof (eaves overhang the walls)
    P += [box('wall', 64, CX, 216, 320, 0, 48),
          box('cornice', 60, CX, 212, 324, 44, 52),
          hip('roof', 56, 2 * CX - 56, 208, 328, 52, 60, 0.5)]
    # rotunda: drum standing on the building (the striped dome sits on it, see big_top)
    P += [Cyl('drum', CX, 262, 58, 0, 84), Cyl('dcor', CX, 262, 61, 80, 86)]
    # entrance portico: block, cornice, gable roof with a pediment
    P += [box('porch', 180, CX, 312, 336, 0, 66),
          box('porch_cor', 177, CX, 310, 340, 62, 70),
          gable('porch_roof', 177, 2 * CX - 177, 310, 340, 70, 0.5)]
    # towers: outer (corner, tall) and inner (flanking the portico)
    for (tx, ty, r, h, dr, dz) in ((40, 300, 32, 96, 30, 36), (152, 318, 20, 76, 18, 24)):
        P += [Cyl('tower', tx, ty, r, 0, h), Cyl('tcor', tx, ty, r + 3, h - 6, h + 2), Ell('tdome', tx, ty, h + 2, dr, dz)]
    # front step / plinth
    P += [box('plinth', 0, CX, 300, 346, 0, 4)]
    P += [Ell('bigdome', CX, 262, 86, 58, 42)]
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
    # marble walls (ashlar on the front faces, courses every 8 px of height)
    for nm in ('wall', 'porch', 'plinth'):
        m = names == nm
        setc(m, M1)
        setc(m & top, M0)
        joint = ((Zi % 8) == 0) | (((Xi + 8 * ((Zi // 8) % 2)) % 16) == 0)
        setc(m & front & joint & (Zi > 0), M2)
        setc(m & ~front & ~top, M2)
    setc(names == 'plinth', M1); setc((names == 'plinth') & top, M0); setc((names == 'plinth') & (Zi <= 1) & front, M2)
    for nm in ('cornice', 'porch_cor', 'tcor', 'dcor'):
        m = names == nm
        setc(m, M0); setc(m & front & (Zi <= np.where(nm == 'tcor', 0, 0) + {'cornice': 45, 'porch_cor': 63, 'tcor': 0, 'dcor': 81}[nm]), M2)
    for p in prims:                                         # tower cornice bottom line
        if p.name == 'tcor':
            m = (names == 'tcor') & (Z < p.z0 + 1.5) & (np.abs(X - p.cx) <= p.r + 3); setc(m, M2)
            setc((names == 'tcor') & ~top & (lum < 0.2), M2)
    # roofs: slate shingles (rows every 4 px on screen), side slopes darker, hips highlighted
    for nm in ('roof', 'porch_roof'):
        m = names == nm
        frontish = N[..., 1] > 0.3
        base = np.where(frontish[..., None], np.array(R2), np.array(R3))
        img[m] = np.concatenate([base[m], np.full((m.sum(), 1), 255)], -1).astype(np.uint8)
        row = (sy % 4) == 3
        jt = ((sx + 4 * ((sy // 4) % 2)) % 8) == 0
        setc(m & frontish & (row | (jt & ((sy % 4) >= 1))), R3)
        setc(m & ~frontish & (row | (jt & ((sy % 4) >= 1))), R4)
        setc(m & frontish & ((sy % 4) == 0), R1)
        setc(m & top, R1)
    # cylinders: tower bodies and the drum, shaded by the normal in vertical bands
    for nm in ('tower', 'drum'):
        m = names == nm
        tone = np.select([lum > 0.4, lum > 0.3, lum > 0.15], [1, 2, 3], 4)
        ramp = np.array([M0, M0, M1, M2, M3])
        img[m] = np.concatenate([ramp[tone][m], np.full((m.sum(), 1), 255)], -1).astype(np.uint8)
        course = (sy % 8) == 7
        dark = np.array([M1, M1, M2, M3, M4])
        img[m & course] = np.concatenate([dark[tone][m & course], np.full(((m & course).sum(), 1), 255)], -1).astype(np.uint8)
    # tower domes: ribbed blue, tones by light
    for p in prims:
        if p.name != 'tdome': continue
        m = (names == 'tdome') & (np.abs(X - p.cx) <= p.r + 1)
        az = np.arctan2(X - p.cx, Y - p.cy)
        tone = np.select([lum > 0.93, lum > 0.75, lum > 0.45], [0, 1, 2], 3)
        ramp = np.array([R0, R1, R2, R3, R4])
        rib = (np.abs(((az + math.pi / 12) % (math.pi / 6)) - math.pi / 12) < 0.09) & (Z < p.z0 + p.rz * 0.9)
        tone = np.where(rib, np.minimum(tone + 1, 4), tone)
        img[m] = np.concatenate([ramp[tone][m], np.full((m.sum(), 1), 255)], -1).astype(np.uint8)
        setc(m & (Z < p.z0 + 2.5), G2); setc(m & (Z < p.z0 + 1), G3)
    # big top: stripes by azimuth, gold ring
    for p in prims:
        if p.name != 'bigdome': continue
        m = names == 'bigdome'
        az = np.abs(np.arctan2(X - p.cx, Y - p.cy))
        k = (((az + math.pi / 16) // (math.pi / 8)).astype(int)) % 4
        tones = {0: (CR, YE, YED), 1: (YE, OR, ORD), 2: (R2, BL, NV), 3: (YE, OR, ORD)}
        lv = np.select([lum > 0.9, lum > 0.55], [0, 1], 2)
        for kk, tt in tones.items():
            for lvl in range(3): setc(m & (k == kk) & (lv == lvl), tt[lvl])
        setc(m & (Z < p.z0 + 3), G2); setc(m & (Z < p.z0 + 1.2), G3)
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

def details(img, prims, R, names):
    X, Y, Z, sx, sy = R['X'], R['Y'], R['Z'], R['sx'], R['sy']
    def setc(mask, c): img[mask] = c + (255,)
    def window(face, xc, z0, z1, hw):
        m = face & (np.abs(X - xc) <= hw) & (Z >= z0) & (Z <= z1)
        arch = Z > z1 - hw
        m &= ~arch | ((X - xc) ** 2 + (Z - (z1 - hw)) ** 2 <= hw * hw)
        inner = m & (np.abs(X - xc) <= hw - 1) & (Z >= z0 + 1) & (~arch | ((X - xc) ** 2 + (Z - (z1 - hw)) ** 2 <= (hw - 1) ** 2))
        setc(m, OUT); setc(inner, GL2); setc(inner & (Z > z0 + (z1 - z0) * 0.55), GL1); setc(inner & (Z < z0 + (z1 - z0) * 0.25), GL3)
        setc(face & (np.abs(X - xc) <= hw + 2) & (np.abs(Z - (z0 - 1)) < 1), M0)    # sill
    wing = (names == 'wall') & (R['N'][..., 1] > 0.95)
    for xc in (2 * CX - 80, 2 * CX - 120, 80, 120): window(wing, xc, 10, 36, 6)
    for xc in (CX - 46, CX + 46): window(names == 'drum', xc, 0, 0, 0) if False else None
    # tower windows (front of the cylinders)
    for p in prims:
        if p.name != 'tower': continue
        face = (names == 'tower') & (np.abs(X - p.cx) <= p.r)
        levels = ((14, 38), (52, 76)) if p.r > 24 else ((12, 34), (46, 64))
        for (z0, z1) in levels: window(face, p.cx, z0, z1, 5)
        setc(face & (np.abs(Z - 46 if p.r > 24 else Z - 40) < 1.5) & (np.abs(X - p.cx) <= p.r), M0) if False else None
    for p in prims:
        if p.name != 'drum': continue
        m = names == 'drum'
        az = np.arctan2(X - p.cx, Y - p.cy)
        ph = (az + math.pi / 10) % (math.pi / 5) - math.pi / 10
        setc(m & (np.abs(ph) < 0.05), M0)
        win = m & (np.abs(ph - math.pi / 10 + 0.0) < 0.07) & (Z > 66) & (Z < 77)
        win |= m & (np.abs(ph + math.pi / 10) < 0.07) & (Z > 66) & (Z < 77)
        setc(win, OUT)
    # portico: columns, doors, drapes, pediment emblem
    porch = (names == 'porch') & (R['N'][..., 1] > 0.95)
    for xc in (185, 2 * CX - 185):
        col = porch & (np.abs(X - xc + 0.5) <= 4)
        setc(col, M0); setc(col & (np.abs(X - xc + 0.5) > 2.5), M2); setc(col & (Z > 56), M0)
    door = porch & (np.abs(X - CX) <= 22) & (Z <= 40)
    setc(door, OUT); dg = door & (np.abs(X - CX) <= 20) & (Z <= 38)
    setc(dg, GL3); setc(dg & (Z > 26), GL1); setc(dg & (np.abs(X - CX) < 1), OUT); setc(dg & (np.abs(Z - 24) < 1), M0)
    setc(porch & (np.abs(X - CX) <= 24) & (Z > 40) & (Z <= 43), G2)
    for sgn in (-1, 1):                                                         # red drapes and blue swag
        dx = sgn * (X - CX)
        dr = porch & (dx >= 20) & (dx <= 26) & (Z <= 54) & (Z >= 8 + (dx - 20) * 3)
        setc(dr, RE); setc(dr & (((Xi := np.floor(X).astype(int)) % 3) == 0), DR)
    sw = porch & (np.abs(X - CX) <= 26) & (Z >= 47 + 5 * np.cos((X - CX) / 27 * math.pi / 1.0) * 0) & (np.abs(Z - (50 - 5 * np.sin(np.abs(X - CX) / 27 * math.pi))) < 1.6)
    setc(sw, BL)
    ped = (names == 'porch_roof') & (R['N'][..., 1] > 0.95)
    setc(ped, M0); setc(ped & (Z < 72), M2)
    em = ped & ((X - CX) ** 2 + (Z - 80) ** 2 <= 49)
    setc(em, RE); setc(em & (Z < 80), M0); setc(em & (np.abs(Z - 80) < 1), OUT)
    setc(em & ((X - CX) ** 2 + (Z - 80) ** 2 <= 4), M0); setc(em & (np.abs((X - CX) ** 2 + (Z - 80) ** 2 - 6) < 2.5), OUT)
    # banners on the wings, next to the inner towers
    for (xc, c) in ((100, RE), (2 * CX - 100, BL)):
        b = wing & (np.abs(X - xc + 0.5) <= 3.5) & (Z >= 14) & (Z <= 44)
        setc(b, c); setc(b & (Z > 41), YE); setc(b & (np.abs(X - xc + 0.5) < 1.5) & (np.abs(Z - 34) < 2), YE)
    return img

def proj(x, y, z): return int(round(x)), int(round(K * y - z))

def ornaments(img, prims, h0):
    """finials and flags on the tower domes (BG)"""
    p = img.load()
    def put(x, y, c):
        y -= h0
        if 0 <= x < img.width and 0 <= y < img.height: p[x, y] = c + (255,)
    for q in prims:
        if q.name != 'tdome': continue
        ax, ay = proj(q.cx, q.cy, q.z0 + q.rz)
        for y in range(ay - 5, ay + 1): put(ax - 1, y, G2); put(ax, y, G2)
        for y in range(ay - 8, ay - 5):
            for x in range(ax - 2, ax + 2): put(x, y, G1)
        for y in range(ay - 18, ay - 8): put(ax, y, M4)
        flip = 1 if q.cx < CX else -1
        for y in range(ay - 18, ay - 12):
            for k in range(1, 7 - abs(2 * (y - (ay - 15)) + 1)): put(ax + flip * k if flip > 0 else ax - k, y, RE)
    return img

def big_top_details(img, prims, h0):
    """scalloped valance at the base of the striped dome, bunting and the trophy on top"""
    p = img.load()
    def put(x, y, c):
        y -= h0
        if 0 <= x < img.width and 0 <= y < img.height: p[x, y] = c + (255,)
    q = [d for d in prims if d.name == 'bigdome'][0]
    for x in range(q.cx - q.r, q.cx + q.r + 1):        # valance hanging from the front rim
        dx = x + 0.5 - q.cx
        if abs(dx) > q.r: continue
        yb = q.cy + math.sqrt(q.r * q.r - dx * dx)
        _, sy = proj(x, yb, q.z0)
        u = (x - q.cx + 8) % 16; d = max(1, int(5 - abs(u - 7.5) * 0.55))
        for t in range(d + 1): put(x, sy + t, RE if t < d else DR)
    ax, ay = proj(q.cx, q.cy, q.z0 + q.rz)
    cx = ax
    for y in range(ay - 5, ay + 3):                     # gold cap
        hw = 7 + (y - ay + 5)
        for x in range(cx - hw, cx + hw): put(x, y, G1 if y < ay - 2 else (G2 if y < ay + 1 else G3))
    top = ay - 27
    for y in range(top, top + 16):                      # cup
        half = 8 if y < top + 5 else 8 - (y - top - 5) * 0.45
        for x in range(int(cx - half), int(cx + half)): put(x, y, G1 if x < cx - 2 else G2)
    for y in range(top + 3, top + 11): put(cx - 11, y, G2); put(cx + 10, y, G2)
    for x in range(cx - 11, cx - 7): put(x, top + 3, G2); put(x, top + 10, G2)
    for x in range(cx + 7, cx + 11): put(x, top + 3, G2); put(x, top + 10, G2)
    for y in range(top + 4, top + 11):
        for x in range(cx - 4, cx + 4):
            if (x + 0.5 - cx) ** 2 + (y - top - 7) ** 2 <= 12: put(x, y, RE if y < top + 7 else M0)
    for x in range(cx - 4, cx + 4): put(x, top + 7, OUT)
    for x in range(cx - 3, cx + 3): put(x, top + 16, G3); put(x, top + 17, G2)
    for y in range(top + 17, top + 26):                 # red bow
        for x in range(cx - 10, cx + 10):
            if abs(x + 0.5 - cx) > 2 and abs(y - top - 21) < (abs(x + 0.5 - cx) - 2) * 0.7 + 1: put(x, y, RE)
    for y in range(top + 19, top + 24):
        for x in range(cx - 2, cx + 2): put(x, y, DR)
    # bunting: strings from the cap down along the dome to the rim, pennants in contest colours
    for side in (-1, 1):
        for ang in (0.85,):
            pts = []
            for k in range(41):
                th = k / 40 * (math.pi / 2) * 0.82                # from the apex down to the rim
                rr = q.r * math.sin(th) * 1.02; zz = q.z0 + q.rz * math.cos(th) * 1.02
                x = q.cx + side * rr * math.sin(ang); y = q.cy + rr * math.cos(ang)
                pts.append(proj(x, y, zz + 1))
            for k, (x, y) in enumerate(pts[3:], 3):
                put(x, y, OUT)
                if k % 5 == 0:
                    c = (RE, YE, BL)[(k // 5) % 3]
                    for d in range(1, 4):
                        for w in range(4 - d): put(x + w * side, y + d, c)
    return img

# ---------------- final split: background art + sprites ----------------
SPRITE_PARTS = {'bigdome', 'drum', 'dcor', 'tdome', 'porch', 'porch_cor', 'porch_roof'}
def build():
    """returns (bg RGBA 432x176, full RGBA (rows h0..H), sprite RGBA same size, h0)"""
    P = model(); R = render(P)
    full = big_top_details(ornaments(finish(P, R), P, R['h0']), P, R['h0'])
    P2 = [p for p in P if p.name not in SPRITE_PARTS]; R2 = render(P2)
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
    return Image.fromarray(b).copy(), full, Image.fromarray(spr).copy(), h0

GROUPS = [  # name, canvas box (x0, x1, y0, y1) on the 16 px grid, anchor_up, column/row split
    ('hall_tdi_l', (128, 176, 32, 96), 0, None), ('hall_tdi_r', (256, 304, 32, 96), 0, None),
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
    gi[m & np.isin(names, ['porch', 'porch_cor', 'porch_roof'])] = gidx('hall_porch')
    td = m & (names == 'tdome')
    gi[td & (X < 96)] = gidx('hall_tdo_l'); gi[td & (X >= 96) & (X < CX)] = gidx('hall_tdi_l')
    gi[td & (X > 2 * CX - 96)] = gidx('hall_tdo_r'); gi[td & (X >= CX) & (X <= 2 * CX - 96)] = gidx('hall_tdi_r')
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
