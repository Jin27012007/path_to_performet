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
    10: {
        'cruise': A.stretch_tidal,
        'boat_side': lambda: A.briney_boat(2),
        'boat_side_l': lambda: _hflip(A.briney_boat(2)),
        'boat_front': lambda: A.briney_boat(0),
    },
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
