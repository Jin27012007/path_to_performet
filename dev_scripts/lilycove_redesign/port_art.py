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
PALETTES[10] = _V
for _n, _src in (('house_grey_coral', 'house_grey'), ('house_beige_lilac', 'house_beige')):
    _CANVAS[_n] = _CANVAS[_src]; PAL_OF[_n] = 10; ART[_n] = (lambda n=_n: _CANVAS[n])
