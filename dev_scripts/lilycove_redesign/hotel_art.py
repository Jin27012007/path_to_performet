"""The Lilycove hotel, from the user's assembled example (hotel_ref.png): roof deck, two wings
with two floors of windows and a base band, the curved glass tower in the middle with the entrance
below it. Cleaned up here: binary transparency, 15 colours (one sprite palette), a uniform dark
outline around the silhouette, and the double door centred on a tile boundary.
Returns (RGBA image 224x192, door column) -- the door's two leaves are columns col-1 and col."""
import os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 224, 192
DOOR_CENTER_X = 103.5                     # centre of the glass double door in the cropped example

def building():
    src = Image.open(os.path.join(HERE, 'hotel_ref.png')).convert('RGBA')
    # keep only the building (drop stray pixels outside it): largest connected opaque area
    p = src.load(); w, hh = src.size; seen = set(); best = []
    for y in range(hh):
        for x in range(w):
            if p[x, y][3] and (x, y) not in seen:
                comp = []; st = [(x, y)]; seen.add((x, y))
                while st:
                    a_, b_ = st.pop(); comp.append((a_, b_))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        n = (a_ + dx, b_ + dy)
                        if 0 <= n[0] < w and 0 <= n[1] < hh and n not in seen and p[n][3]: seen.add(n); st.append(n)
                if len(comp) > len(best): best = comp
    keep = set(best)
    for y in range(hh):
        for x in range(w):
            if p[x, y][3] and (x, y) not in keep: p[x, y] = (0, 0, 0, 0)
    bb = src.split()[3].getbbox(); src = src.crop(bb)
    ox = int(W // 2 - DOOR_CENTER_X); oy = H - src.height
    im = Image.new('RGBA', (W, H), (0, 0, 0, 0)); im.alpha_composite(src, (ox, oy))
    return im, (W // 2) // 16

def outline(canvas, out_index):
    """uniform 1 px dark outline on the silhouette (pixels that touch transparency)"""
    h, w = len(canvas), len(canvas[0]); res = [row[:] for row in canvas]
    for y in range(h):
        for x in range(w):
            if canvas[y][x] and any(not (0 <= x + dx < w and 0 <= y + dy < h) or not canvas[y + dy][x + dx]
                                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                res[y][x] = out_index
    return res
