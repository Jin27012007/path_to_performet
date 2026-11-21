"""Extracts authentic Pokémon Emerald graphics (S.S. Tidal, Mr. Briney's boat, Slateport's
market tents, goods and sailboats) as RGBA images with the background removed, so the
Lilycove port art matches the game's own style."""
import os, struct
from PIL import Image
import render

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))

def jasc(path):
    L = open(path).read().split('\n')[3:19]
    return [tuple(int(v) for v in l.split()) for l in L if l.strip()]

def sprite(png, pal, frame=None, fw=None, fh=None):
    im = Image.open(os.path.join(REPO, png)); P = jasc(os.path.join(REPO, pal)); px = im.load()
    x0, y0, w, h = 0, 0, im.width, im.height
    if frame is not None: x0, w, h = frame * fw, fw, fh
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0)); o = out.load()
    for y in range(h):
        for x in range(w):
            i = px[x0 + x, y0 + y]
            if i: o[x, y] = P[i] + (255,)
    return out

_cache = {}
def _mimg(sec):
    if sec not in _cache: _cache[sec] = render.build('primary/general', sec)[0]
    return _cache[sec]

def from_map(layout, width, sec, x0, y0, w, h, bg):
    """Renders w x h metatiles of a map and removes every pixel equal to metatile bg."""
    d = open(os.path.join(REPO, 'data/layouts', layout, 'map.bin'), 'rb').read()
    mimg = _mimg(sec)
    bgimg = mimg(bg).load()
    out = Image.new('RGBA', (w * 16, h * 16), (0, 0, 0, 0)); o = out.load()
    for my in range(h):
        for mx in range(w):
            m = struct.unpack_from('<H', d, ((y0 + my) * width + x0 + mx) * 2)[0] & 0x3ff
            t = mimg(m).load()
            for y in range(16):
                for x in range(16):
                    if t[x, y] != bgimg[x, y]:
                        o[mx * 16 + x, my * 16 + y] = t[x, y] + (255,)
    return out

def stretch_tidal():
    """S.S. Tidal lengthened: the window section is repeated, bow and stern untouched."""
    s = sprite('graphics/object_events/pics/misc/ss_tidal.png', 'graphics/object_events/palettes/ss_tidal.pal')
    parts = [s.crop((0, 0, 32, 40))] + [s.crop((32, 0, 48, 40))] * 10 + [s.crop((48, 0, 96, 40))]
    w = sum(p.width for p in parts)
    out = Image.new('RGBA', (w, 48), (0, 0, 0, 0)); x = 0
    for p in parts: out.paste(p, (x, 2)); x += p.width     # near the top: hugs the pier
    return out

def slateport(x0, y0, w, h, bg=0x211):
    return from_map('SlateportCity', 40, 'secondary/slateport', x0, y0, w, h, bg)

def briney_boat(frame):
    return sprite('graphics/object_events/pics/misc/mr_brineys_boat.png', 'graphics/object_events/palettes/npc_3.pal', frame, 32, 32)

# colours of Slateport's cobblestone floor (lit and shaded) -> transparent
def _floor_colours():
    m = _mimg('secondary/slateport')
    cols = set()
    for mid in (0x211, 0x210, 0x212, 0x285, 0x205 - 0, 0x235, 0x23d, 0x26c, 0x227, 0x22f):
        pass
    for mid in (0x211, 0x210, 0x212, 0x285):
        cols |= {c for c in m(mid).getdata()}
    return cols

def slateport_clean(x0, y0, w, h):
    img = slateport(x0, y0, w, h); floor = _floor_colours(); p = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if p[x, y][3] and p[x, y][:3] in floor: p[x, y] = (0, 0, 0, 0)
    return img

def to_palette(images, ncolors=15):
    """Builds one 16-colour palette (index 0 = transparent) shared by all images and
    returns (palette, [index canvases])."""
    cols = {}
    for im in images:
        for c in im.getdata():
            if c[3]: cols[c[:3]] = cols.get(c[:3], 0) + 1
    if len(cols) <= ncolors:
        pal = list(cols)
    else:
        # weight colours by how many pixels use them, so dominant colours survive
        pix = [c for c, n in cols.items() for _ in range(n)]
        strip = Image.new('RGB', (len(pix), 1)); strip.putdata(pix)
        q = strip.quantize(ncolors, method=Image.Quantize.MEDIANCUT, kmeans=4)
        qp = q.getpalette()[:ncolors * 3]
        pal = [tuple(qp[i * 3:i * 3 + 3]) for i in range(ncolors)]
        # keep the darkest outline colour exact (Emerald art relies on it)
        darkest = min(cols, key=lambda c: sum(c))
        if darkest not in pal:
            j = min(range(len(pal)), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], darkest)))
            pal[j] = darkest
    def nearest(c):
        return min(range(len(pal)), key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], c)))
    lut = {c: nearest(c) + 1 for c in cols}
    canvases = []
    for im in images:
        p = im.load()
        canvases.append([[lut[p[x, y][:3]] if p[x, y][3] else 0 for x in range(im.width)] for y in range(im.height)])
    pal16 = [(0, 0, 0)] + [tuple(v // 8 * 8 for v in c) for c in pal]
    pal16 += [(0, 0, 0)] * (16 - len(pal16))
    return pal16, canvases

def tent_with(goods_x, goods_y):
    """Full-width Slateport tent with the goods row taken from another tent."""
    t = slateport_clean(2, 41, 5, 3)
    goods = slateport_clean(goods_x, goods_y, 2, 1)
    clear = Image.new('RGBA', (32, 16), (0, 0, 0, 0))
    t.paste(clear, (16, 32)); t.paste(goods, (16, 32), goods)
    return t

def _region_colours(layout, width, sec, rects):
    cols = set()
    for (x0, y0, w, h) in rects:
        im = from_map(layout, width, sec, x0, y0, w, h, bg=0x3ff)
        cols |= {c[:3] for c in im.getdata() if c[3]}
    return cols

def rustboro(x0, y0, w, h):
    """A Rustboro building with ground, shadows and grass keyed out."""
    ground = _region_colours('RustboroCity', 40, 'secondary/rustboro',
                             [(19, 24, 3, 5), (12, 31, 3, 2), (14, 26, 1, 3), (20, 40, 3, 2), (25, 28, 1, 1), (28, 35, 2, 1)])
    img = from_map('RustboroCity', 40, 'secondary/rustboro', x0, y0, w, h, bg=0x3ff)
    p = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if p[x, y][3] and p[x, y][:3] in ground: p[x, y] = (0, 0, 0, 0)
    return img


def top_layer(prim, sec, ids):
    """Renders only the TOP layer of some metatiles side by side (furniture over a floor)."""
    pt, pm = render.load(prim); st, sm = render.load(sec); R = render.R
    pals = [render.pal(R + prim + '/palettes/%02d.pal' % i) for i in range(6)] + \
           [render.pal(R + sec + '/palettes/%02d.pal' % i) for i in range(6, 13)]
    tiles = pt + [None] * (512 - len(pt)) + st; mts = pm + [(0,) * 8] * (512 - len(pm)) + sm
    out = Image.new('RGBA', (16 * len(ids), 16), (0, 0, 0, 0)); o = out.load()
    for k, m in enumerate(ids):
        e = mts[m]
        for q in range(4):
            v = e[4 + q]; t = tiles[v & 0x3ff]; hf = v >> 10 & 1; vf = v >> 11 & 1; pl = v >> 12
            for y in range(8):
                for x in range(8):
                    c = t[7 - y if vf else y][7 - x if hf else x]
                    if c: o[k * 16 + (q % 2) * 8 + x, (q // 2) * 8 + y] = tuple(pals[pl][c]) + (255,)
    return out

SAND_SHADOW = {(216, 152, 56), (224, 176, 88), (232, 208, 112)}
def beach_umbrella(x0, y0, shadow=(112, 96, 72)):
    """Route 109 beach umbrella (2x3); its shadow on the sand becomes a dithered shadow."""
    im = from_map('Route109', 40, 'secondary/slateport', x0, y0, 2, 3, bg=0x124); p = im.load()
    for y in range(im.height):
        for x in range(im.width):
            if p[x, y][3] and p[x, y][:3] in SAND_SHADOW:
                p[x, y] = shadow + (255,) if (x + y) % 2 == 0 else (0, 0, 0, 0)
    return im

def seaside_cafe():
    """Route 104's Pretty Petal shop (orange roof, striped awning) with warm cream walls."""
    im = from_map('Route104', 40, 'secondary/rustboro', 3, 15, 6, 4, bg=0x001); p = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = p[x, y]
            if a and g > r + 15 and g >= b:          # green walls / boxes -> cream and wood
                lum = (r + g + b) // 3
                p[x, y] = ((238, 222, 196) if lum > 170 else (214, 184, 150) if lum > 125 else (156, 120, 92)) + (255,)
    return im
