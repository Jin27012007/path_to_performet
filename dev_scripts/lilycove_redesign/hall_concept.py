"""The Contest Hall from the user's concept (hall_concept.jpg): striped big-top dome with the
trophy, four towers with blue domes, stone palace with columns, drapes, contest banners and the
glass entrance. Scaled to 17 x 11 metatiles (272 x 176) and cut into 9 sprite chunks
(3 bands x 3 columns); each band has its own 15-colour object palette (hall0/1/2) so the colours
stay vivid. The magenta background is keyed out; a dark outline is put on the silhouette."""
import os
from PIL import Image
import authentic_art as A
HERE = os.path.dirname(os.path.abspath(__file__))
TW, TH = 17, 11
COLS = [(0, 6), (6, 11), (11, 17)]          # chunk columns (tiles)
ROWS = [(0, 4), (4, 8), (8, 11)]            # chunk rows = palette bands
DOOR_COLS = (7, 8, 9)                       # door cells in the bottom row

def _scaled():
    im = Image.open(os.path.join(HERE, 'hall_concept.jpg')).convert('RGB'); W, H = im.size; p = im.load()
    bg = lambda c: c[0] > 190 and c[2] > 190 and c[1] < 110
    bottom = 0                                  # building bottom (ignoring the carpet columns)
    for y in range(H - 1, 0, -1):
        if any(not bg(p[x, y]) for x in list(range(150, 900, 7)) + list(range(1500, 2250, 7))): bottom = y; break
    a = Image.new('L', (W, H)); ap = a.load()
    for y in range(H):
        for x in range(W): ap[x, y] = 0 if bg(p[x, y]) else 255
    rgba = im.convert('RGBA'); rgba.putalpha(a)
    xs = [x for x in range(0, W, 2) if any(not bg(p[x, y]) for y in range(0, bottom, 9))]
    c = rgba.crop((min(xs), 0, max(xs) + 1, bottom + 1))
    small = c.resize((TW * 16, TH * 16), Image.BOX); sp = small.load()
    for y in range(small.height):
        for x in range(small.width):
            r, g, b, al = sp[x, y]; sp[x, y] = (r, g, b, 255 if al >= 128 else 0)
    return small

def build():
    """returns ({palette key: 16 colours}, [(name, tile x, tile y, index canvas, palette key)])"""
    img = _scaled(); pals = {}; pieces = []
    for bi, (r0, r1) in enumerate(ROWS):
        band = img.crop((0, r0 * 16, TW * 16, r1 * 16))
        pal, (canvas,) = A.to_palette([band])
        dark = min(range(1, 16), key=lambda i: sum(pal[i]))
        h, w = len(canvas), len(canvas[0])
        out = [row[:] for row in canvas]                 # outline where the building meets the background
        for y in range(h):
            for x in range(w):
                if canvas[y][x] and any(not (0 <= x + dx < w) or not (0 <= y + dy < h) and False or
                                        (0 <= x + dx < w and 0 <= y + dy < h and not canvas[y + dy][x + dx])
                                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    out[y][x] = dark
        key = 'hall%d' % bi; pals[key] = pal
        for ci, (c0, c1) in enumerate(COLS):
            pieces.append(('hallc_%d_%d' % (bi, ci), c0, r0, [row[c0 * 16:c1 * 16] for row in out], key))
    return pals, pieces
