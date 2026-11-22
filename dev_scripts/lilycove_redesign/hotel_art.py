"""The Lilycove hotel, assembled from the user's base sheet (hotel_base.png): curved glass tower
on the left, central wing with big windows and the lobby core, rounded glass tower on the right,
one continuous roof deck on top and a glass entrance with a canopy. Returns an RGBA image whose
size is a multiple of 16 (it becomes a sprite, see decor_sprites.py)."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
OUT, GLASS1, GLASS2, GLASS3, FRAME, WALL, WALL2, MINT, TEAL = (
    (80, 88, 112), (128, 184, 232), (72, 136, 200), (232, 248, 224), (56, 104, 112),
    (216, 200, 176), (192, 168, 136), (192, 216, 200), (104, 160, 152))

BAND = (22, 46)                                       # facade rows repeated to add floors

def taller(img, extra):
    """repeats the middle band of a facade piece `extra` times (more floors, same top and base)"""
    if not extra: return img
    a, b = BAND; band = img.crop((0, a, img.width, b))
    out = Image.new('RGBA', (img.width, img.height + extra * (b - a)), (0, 0, 0, 0))
    out.alpha_composite(img.crop((0, 0, img.width, b)), (0, 0))
    for k in range(1, extra + 1): out.alpha_composite(band, (0, a + k * (b - a)))
    out.alpha_composite(img.crop((0, b, img.width, img.height)), (0, b + extra * (b - a)))
    return out

def building(extra=2):
    src = Image.open(os.path.join(HERE, 'hotel_base.png')).convert('RGBA')
    crop = lambda box: taller(src.crop(box), extra)
    FH = 71 + extra * (BAND[1] - BAND[0])            # facade height
    fa, fb = crop((3, 56, 47, 127)), crop((41, 56, 88, 127))
    fc, fd, fe = crop((97, 56, 136, 127)), crop((138, 56, 177, 127)), crop((185, 56, 247, 127))
    roof_l, roof_m, roof_r = src.crop((3, 32, 19, 49)), src.crop((19, 32, 31, 49)), src.crop((46, 32, 63, 49))   # caps + 12 px deck repeat
    facade_w = 33 + fb.width + fc.width + fd.width + fe.width
    W = ((facade_w + 15) // 16) * 16; H = ((FH + 16 + 15) // 16) * 16
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    x0 = (W - facade_w) // 2; top = H - FH            # facade sits on the bottom row
    # one continuous roof deck: framed left cap, repeated deck, frame + green side at the right end
    ry = top - 16
    im.alpha_composite(roof_l, (x0, ry))
    x = x0 + roof_l.width
    while x < x0 + facade_w - roof_r.width:
        im.alpha_composite(roof_m, (x, ry)); x += roof_m.width
    im.alpha_composite(roof_r, (x0 + facade_w - roof_r.width, ry))
    # facade pieces (the green arc of fb hugs the left glass tower)
    im.alpha_composite(fa, (x0, top)); im.alpha_composite(fb, (x0 + 33, top))
    x = x0 + 33 + fb.width
    for p in (fc, fd):
        im.alpha_composite(p, (x, top)); xd = x; x += p.width
    lobby_x = xd                                      # fd = lobby core
    im.alpha_composite(fe, (x, top))
    # glass entrance with a canopy at the bottom of the lobby core, centred on a 16 px column
    dx = ((lobby_x + 12) // 16) * 16                  # door occupies one map column
    p = im.load()
    for yy in range(H - 20, H):
        for xx in range(dx - 2, dx + 18):
            edge = xx in (dx - 2, dx + 17) or yy == H - 20
            p[xx, yy] = (OUT if edge else (FRAME if yy < H - 17 else (GLASS1 if (xx - dx) % 8 < 4 else GLASS2))) + (255,)
        p[dx + 7, yy] = OUT + (255,); p[dx + 8, yy] = OUT + (255,)
    for xx in range(dx - 4, dx + 20):                 # canopy
        for yy in range(H - 23, H - 19):
            p[xx, yy] = (OUT if yy in (H - 23, H - 20) or xx in (dx - 4, dx + 19) else MINT) + (255,)
    return im, dx // 16                               # image, door column (in tiles)
