"""Converts an RGBA image to background tiles that may use a DIFFERENT palette per 8x8 tile
(chosen among `slots` by least colour error). Returns (index canvas, per-tile palette grid)."""
import render
_PALS = {}
def pal(slot):
    if slot not in _PALS:
        base = 'primary/general' if slot < 6 else 'secondary/lilycove_city'
        _PALS[slot] = render.pal(render.R + base + '/palettes/%02d.pal' % slot)
    return _PALS[slot]
def convert(img, slots=(6, 7, 8, 9)):
    W, H = img.size; px = img.load()
    canvas = [[0] * W for _ in range(H)]; grid = [[0] * (W // 8) for _ in range(H // 8)]
    for ty in range(H // 8):
        for tx in range(W // 8):
            cols = [px[tx * 8 + x, ty * 8 + y] for y in range(8) for x in range(8)]
            if not any(c[3] for c in cols): continue
            best = None
            for s in slots:
                P = pal(s); err = 0; idx = []
                for c in cols:
                    if not c[3]: idx.append(0); continue
                    i = min(range(1, 16), key=lambda k: sum((a - b) ** 2 for a, b in zip(P[k], c[:3])))
                    err += sum((a - b) ** 2 for a, b in zip(P[i], c[:3])); idx.append(i)
                if best is None or err < best[0]: best = (err, s, idx)
            grid[ty][tx] = best[1]
            for k, i in enumerate(best[2]): canvas[ty * 8 + k // 8][tx * 8 + k % 8] = i
    return canvas, grid
def unique_tiles(canvas, grid):
    s = set(); H, W = len(canvas), len(canvas[0])
    for ty in range(H // 8):
        for tx in range(W // 8):
            t = tuple(tuple(canvas[ty * 8 + y][tx * 8: tx * 8 + 8]) for y in range(8))
            if not any(any(r) for r in t): continue
            h = tuple(r[::-1] for r in t); v = t[::-1]; hv = tuple(r[::-1] for r in v)
            s.add(min(t, h, v, hv))
    return len(s)
def preview(canvas, grid):
    from PIL import Image
    H, W = len(canvas), len(canvas[0]); im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for y in range(H):
        for x in range(W):
            if canvas[y][x]: im.putpixel((x, y), tuple(pal(grid[y // 8][x // 8])[canvas[y][x]]) + (255,))
    return im
