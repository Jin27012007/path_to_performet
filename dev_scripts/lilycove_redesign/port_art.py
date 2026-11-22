"""Port art for Lilycove City, built from Pokémon Emerald's own graphics so it matches
the game's style:

* cruise ship  -> the S.S. Tidal sprite, lengthened (window section repeated)
* fishing boats -> Mr. Briney's boat sprite (side, mirrored and front views)
* market tents and goods -> Slateport's market metatiles (background removed)

Two shared 16-colour palettes are generated (city tileset slots 10 and 11).
ART[name]() returns an index canvas; PAL_OF[name] is its palette slot; PALETTES[slot]
is the palette to write.
"""
from PIL import Image
import authentic_art as A

def _hflip(im): return im.transpose(Image.FLIP_LEFT_RIGHT)

_GROUPS = {
    # slot 10: the cruise ship and the fishing boats are sprites now (object events)
    11: {
        'tent_green': lambda: A.slateport_clean(2, 41, 5, 3),
        'tent_pots': lambda: A.tent_with(10, 43),
        'tent_flowers': lambda: A.slateport_clean(2, 49, 5, 3),
        'basket_orange': lambda: A.slateport_clean(7, 41, 1, 1),
        'crate_label': lambda: A.slateport_clean(7, 42, 1, 1),
        'basket_green': lambda: A.slateport_clean(7, 43, 1, 1),
        'box_wood': lambda: A.slateport_clean(7, 46, 1, 1),
        'fruit': lambda: A.slateport_clean(8, 41, 1, 1),
    },
    12: {   # Rustboro buildings: modern houses and apartments (residential district)
        'house_grey': lambda: A.from_map('RustboroCity', 40, 'secondary/rustboro', 28, 24, 5, 5, bg=0x2bb),
        'house_beige': lambda: A.from_map('RustboroCity', 40, 'secondary/rustboro', 7, 34, 5, 5, bg=0x2bb),
        'apartments': lambda: A.from_map('RustboroCity', 40, 'secondary/rustboro', 24, 30, 7, 5, bg=0x2bb),
    },
}

PALETTES = {}
_CANVAS = {}
PAL_OF = {}
for _slot, _makers in _GROUPS.items():
    _names = list(_makers)
    _pal, _cvs = A.to_palette([_makers[n]() for n in _names])
    PALETTES[_slot] = _pal
    for _n, _c in zip(_names, _cvs):
        _CANVAS[_n] = _c
        PAL_OF[_n] = _slot

ART = {n: (lambda n=n: _CANVAS[n]) for n in _CANVAS}

# plaza art, drawn directly in Lilycove palette 8 (no quantisation needed)
import plaza_art as _P
for _n, _f in (('paving', _P.paving), ('fountain', _P.fountain), ('fountain_modern', _P.fountain_modern), ('lamp', _P.lamp_post), ('lamp_modern', _P.lamp_modern)):
    _CANVAS[_n] = _f()
    PAL_OF[_n] = _P.PAL8_SLOT
    ART[_n] = (lambda n=_n: _CANVAS[n])
FLOOR = {'paving'}   # art drawn in the bottom layer (walkable floor)

# festival bunting as art, so it can hang over any floor (palette 6 red / 12 blue)
import festival_tiles as _F
_CANVAS['bunting'] = _F.bunting(); PAL_OF['bunting'] = 6; ART['bunting'] = lambda: _CANVAS['bunting']
_CANVAS['bunting_blue'] = _F.bunting(); PAL_OF['bunting_blue'] = 12; ART['bunting_blue'] = lambda: _CANVAS['bunting_blue']

for _n in _P.FLOWER_COLOURS:
    _CANVAS[_n] = _P.flower(_n); PAL_OF[_n] = 6; ART[_n] = (lambda n=_n: _CANVAS[n])

_CANVAS['lamp_modern_l'] = [row[::-1] for row in _P.lamp_modern()]; PAL_OF['lamp_modern_l'] = _P.PAL8_SLOT
ART['lamp_modern_l'] = lambda: _CANVAS['lamp_modern_l']

FLOWER_NAMES = list(_P.FLOWER_COLOURS)

# ---- palette variants (cost no tiles: same tiles, palette slot 10 instead of 12) ----
# slot 10 = Rustboro palette 12 with the grey house's roof/walls (4,5,6) turned coral and the
# beige house's roof/walls (9,10,11) turned lilac. Apartments keep slot 12.
_V = list(PALETTES[12])
_V[4], _V[5], _V[6] = (232, 144, 120), (224, 208, 192), (192, 168, 152)     # coral roof, warm walls
_V[9], _V[10], _V[11] = (168, 136, 192), (192, 168, 216), (216, 200, 232)   # lilac
_V[14], _V[15] = (176, 140, 100), (120, 92, 64)                         # matte wood for the café deck
PALETTES[10] = _V
for _n, _src in (('house_grey_coral', 'house_grey'), ('house_beige_lilac', 'house_beige')):
    _CANVAS[_n] = _CANVAS[_src]; PAL_OF[_n] = 10; ART[_n] = (lambda n=_n: _CANVAS[n])

# ---- seaside café (residential district 1): Emerald pieces mapped onto the market palette 11 ----
# index 6 of palette 11 was unused by the market art: a coral red for roof stripes and umbrellas.
PALETTES[11] = list(PALETTES[11]); PALETTES[11][6] = (232, 88, 64)
def _fixed(im, slot):
    """maps an RGBA image onto an existing palette slot (nearest colour, index 0 = transparent)"""
    pal = PALETTES[slot]; p = im.load(); cache = {}
    ok = [i for i in range(1, 16) if pal[i] != (0, 0, 0)]
    def near(c):
        if c not in cache: cache[c] = min(ok, key=lambda i: sum((a - b) ** 2 for a, b in zip(pal[i], c)))
        return cache[c]
    return [[near(p[x, y][:3]) if p[x, y][3] else 0 for x in range(im.width)] for y in range(im.height)]
for _n, _mk in (('cafe', A.seaside_cafe),
                ('umbrella_red', lambda: A.beach_umbrella(9, 6)),
                ('umbrella_blue', lambda: A.beach_umbrella(24, 3)),
                ('cafe_table', lambda: A.top_layer('primary/building', 'secondary/seashore_house', [0x218, 0x210, 0x219]))):
    _CANVAS[_n] = _fixed(_mk(), 11); PAL_OF[_n] = 11; ART[_n] = (lambda n=_n: _CANVAS[n])

def _wood_fence():
    """low wooden rail fence (palette 6 = festival/dock wood), 16x16, tiles seamlessly"""
    _, WH, CR, YE, OR, RE, DR, BR, LB, BL, NV, LG, GR, DG, BN, DB = range(16)
    c = [[0] * 16 for _ in range(16)]
    for y in (5, 6, 10, 11):                       # two rails
        for x in range(16): c[y][x] = BN if y in (5, 10) else DB
    for x0 in (2, 10):                             # two posts per tile
        for y in range(2, 15):
            c[y][x0] = DB; c[y][x0 + 1] = OR if y < 13 else BN; c[y][x0 + 2] = BN; c[y][x0 + 3] = DB
        c[1][x0 + 1] = DB; c[1][x0 + 2] = DB
        for x in range(x0, x0 + 4): c[15][x] = DB
    return c
_CANVAS['fence_wood'] = _wood_fence(); PAL_OF['fence_wood'] = 6; ART['fence_wood'] = lambda: _CANVAS['fence_wood']

# ---- café furniture v2: small modern table + two red chairs, umbrella sets, potted palms ----
def _chair(right=False):
    """red lounge chair from the Battle Frontier lounge (back on the right = faces left)"""
    im = A.top_layer('primary/building', 'secondary/battle_frontier', [0x3e7])
    return im.transpose(Image.FLIP_LEFT_RIGHT) if right else im
def _table():
    """small round modern table: white top, slim grey pedestal (drawn in Emerald style)"""
    OUT, WH, HI, RIM, DK = (64, 72, 104), (248, 248, 248), (232, 240, 224), (152, 144, 136), (80, 120, 176)
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); p = im.load()
    def put(x, y, c): p[x, y] = c + (255,)
    for y in range(2, 9):                       # tabletop: ellipse 13x7
        for x in range(1, 15):
            dx = (x - 7.5) / 6.5; dy = (y - 5) / 3.4
            if dx * dx + dy * dy <= 1.0:
                put(x, y, WH if y < 6 else (HI if y < 7 else RIM))
    for y in range(2, 9):                       # outline
        for x in range(1, 15):
            if p[x, y][3] and any(not (0 <= x + a < 16 and 0 <= y + b < 16) or not p[x + a, y + b][3] for a, b in ((1,0),(-1,0),(0,1),(0,-1))):
                put(x, y, OUT)
    for y in range(9, 13):                      # pedestal
        put(6, y, OUT); put(7, y, RIM); put(8, y, DK); put(9, y, OUT)
    for x in range(4, 12): put(x, 13, OUT if x in (4, 11) else DK)
    for x in range(5, 11): put(x, 14, OUT)
    return im
def _table_set():
    """chair | table | chair (3x1)"""
    im = Image.new('RGBA', (48, 16), (0, 0, 0, 0))
    for x, part in ((0, _chair(right=True)), (16, _table()), (32, _chair())):
        im.alpha_composite(part, (x, 0))
    return im
def _umbrella_set(x0, y0):
    """3x3: beach umbrella over a small table with two chairs; the pole goes into the table"""
    u = A.beach_umbrella(x0, y0); im = Image.new('RGBA', (48, 48), (0, 0, 0, 0))
    up = u.load(); shadow = (112, 96, 72)
    for y in range(48):                          # 1) shadow on the floor
        for x in range(32):
            if up[x, y][3] and up[x, y][:3] == shadow: im.putpixel((x + 8, y), up[x, y])
    im.alpha_composite(_table_set(), (0, 32))    # 2) chairs and table
    for y in range(48):                          # 3) canopy and the visible part of the pole
        for x in range(32):
            if up[x, y][3] and up[x, y][:3] != shadow and (y < 32 + 5 or not (8 <= x + 8 < 40)):
                im.putpixel((x + 8, y), up[x, y])
    return im
def _potted_palm():
    return A.top_layer('primary/building', 'secondary/battle_frontier', [0x3dc]).crop((0, 0, 16, 16)), \
           A.top_layer('primary/building', 'secondary/battle_frontier', [0x3e4])
def _palm_pot():
    a, b = _potted_palm(); im = Image.new('RGBA', (16, 32), (0, 0, 0, 0)); im.alpha_composite(a, (0, 0)); im.alpha_composite(b, (0, 16)); return im
for _n, _mk in (('table_set', _table_set), ('umbrella_set_red', lambda: _umbrella_set(9, 6)),
                ('umbrella_set_blue', lambda: _umbrella_set(24, 3))):
    _CANVAS[_n] = _fixed(_mk(), 11); PAL_OF[_n] = 11; ART[_n] = (lambda n=_n: _CANVAS[n])

# lighter terrace planks: the dock planks without the saturated orange highlight (OR -> cream)
# light beach-deck planks with soft joints, in the market palette 11 (beige body, brown joints)
_CANVAS['terrace'] = [[{4: 14, 14: 14, 15: 15}.get(v, v) for v in row] for row in _F.dock()]
PAL_OF['terrace'] = 10; ART['terrace'] = lambda: _CANVAS['terrace']; FLOOR.add('terrace')
PALETTES[6] = list(_F.PAL6)        # festival palette (greens for the potted palms); only used for mapping,
_CANVAS['potted_palm'] = _fixed(_palm_pot(), 6); PAL_OF['potted_palm'] = 6; ART['potted_palm'] = lambda: _CANVAS['potted_palm']
del PALETTES[6]                    # slot 6 itself is written by festival_tiles.py (shared with Route 121)

# drink vending machines (Lilycove Dept. Store rooftop): water (teal), lemonade (yellow), soda (red)
_vm = _fixed(A.vending_machine(), 11)
for _n, _to in (('vending_water', 8), ('vending_lemonade', 4), ('vending_soda', 6)):   # bottles = index 10
    _CANVAS[_n] = [[_to if v == 10 else v for v in row] for row in _vm]; PAL_OF[_n] = 11
    ART[_n] = (lambda n=_n: _CANVAS[n])

def _wood_fence_v(cx):
    """vertical run of the low wooden fence (a rail seen from above with a post every 8 px);
    cx = rail centre, matching the posts of the horizontal fence (x 2..5 or x 10..13)"""
    _, WH, CR, YE, OR, RE, DR, BR, LB, BL, NV, LG, GR, DG, BN, DB = range(16)
    c = [[0] * 16 for _ in range(16)]
    for y in range(16):                            # rail
        c[y][cx - 2] = DB; c[y][cx - 1] = OR; c[y][cx] = BN; c[y][cx + 1] = DB
    for y0 in (1, 9):                              # posts
        for y in range(y0, y0 + 5):
            for x in range(cx - 3, cx + 3): c[y][x] = DB if x in (cx - 3, cx + 2) or y in (y0, y0 + 4) else (OR if x == cx - 2 else BN)
    return c
for _n, _cx in (('fence_wood_vl', 4), ('fence_wood_vr', 12)):   # left / right side of an enclosure
    _CANVAS[_n] = _wood_fence_v(_cx); PAL_OF[_n] = 6; ART[_n] = (lambda n=_n: _CANVAS[n])

# ---- shopping mall decorations (palette 6, top layers over the mall wall) ----
import mall_art as _M
for _n, _mk in (('mall_screen', _M.screen), ('mall_pokeball', _M.pokeball),
                ('pennants0', lambda: _M.pennants(0)), ('pennants1', lambda: _M.pennants(1)), ('pennants2', lambda: _M.pennants(2))):
    _CANVAS[_n] = _mk(); PAL_OF[_n] = 6; ART[_n] = (lambda n=_n: _CANVAS[n])
for _n, _mk in (('mall_ticker', _M.ticker), ('carpet_mat', _M.carpet_mat)):
    _CANVAS[_n] = _mk(); PAL_OF[_n] = 6; ART[_n] = (lambda n=_n: _CANVAS[n])
FLOOR.add('carpet_mat')

# ---- parked bikes (Rydel's Cycles display, Mauville), mapped onto palette 11 ----
def _bike(cols, y0):
    """one parked bike, 32x16 (the display bikes are ~22 px wide, over two metatile columns)"""
    h = len(cols[0]); im = Image.new('RGBA', (32, 16 * h), (0, 0, 0, 0))
    for cx, col in enumerate(cols):
        for r, m in enumerate(col): im.alpha_composite(A.top_layer('primary/building', 'secondary/bike_shop', [m]), (16 * cx, 16 * r))
    return im.crop((0, y0, 32, y0 + 16))
for _n, _cols, _y0 in (('bike_yellow', [[0x211, 0x219], [0x212, 0x21a]], 8),
                       ('bike_blue', [[0x221, 0x206], [0x222, 0x207]], 8),
                       ('bike_red', [[0x253, 0x245], [0x254, 0x246]], 0)):
    _CANVAS[_n] = _fixed(_bike(_cols, _y0), 11); PAL_OF[_n] = 11; ART[_n] = (lambda n=_n: _CANVAS[n])

# ---- beach sets (sprites): Route 109 umbrella with Route 109 lounge chairs beside it ----
def _beach_set(ux, uy, chairs):
    u = A.beach_umbrella(ux, uy); ch = A.from_map('Route109', 40, 'secondary/slateport', 17, 8, 1, 3, bg=0x124)
    w = 32 + 16 * len(chairs); im = Image.new('RGBA', (w, 48), (0, 0, 0, 0))
    x = 0
    if 'L' in chairs: im.alpha_composite(ch, (0, 0)); x = 16
    im.alpha_composite(u, (x, 0))
    if 'R' in chairs: im.alpha_composite(ch, (x + 32, 0))
    return im
for _n, _mk in (('beach_set_red', lambda: _beach_set(9, 6, 'LR')), ('beach_set_blue', lambda: _beach_set(24, 3, 'R')),
                ('beach_set_red_l', lambda: _beach_set(9, 6, 'L'))):
    _CANVAS[_n] = _fixed(_mk(), 11); PAL_OF[_n] = 11; ART[_n] = (lambda n=_n: _CANVAS[n])
