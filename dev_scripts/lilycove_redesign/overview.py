"""Renders the whole Lilycove map WITH its sprites (cruise ship, boats, decorations) and,
optionally, zone labels: python3 overview.py out.png [--labels]"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
import render, port_art as P, authentic_art as A
from compose import W, OX, OY
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..'))

def build(out, labels=False):
    tmp = out + '.bg.png'
    render.render(os.path.join(REPO, 'data/layouts/LilycoveCity/map.bin'), W, tmp, sec='secondary/lilycove_city')
    im = Image.open(tmp).convert('RGBA'); os.remove(tmp)
    m = json.load(open(os.path.join(REPO, 'data/maps/LilycoveCity/map.json'))); cache = {}
    def idx(c, slot):
        pal = P.PALETTES[slot]; o = Image.new('RGBA', (len(c[0]), len(c)), (0, 0, 0, 0))
        for y, r in enumerate(c):
            for x, v in enumerate(r):
                if v: o.putpixel((x, y), tuple(pal[v]) + (255,))
        return o
    for e in sorted(m['object_events'], key=lambda e: e['y']):
        g = e['graphics_id']; tx, ty = e['x'], e['y']
        if g.startswith('OBJ_EVENT_GFX_LC_'):
            n = g[len('OBJ_EVENT_GFX_LC_'):].lower()
            if n not in cache: cache[n] = idx(P.ART[n](), 11)
            s = cache[n]; im.alpha_composite(s, ((tx - (s.width // 16) // 2) * 16, (ty + 1) * 16 - s.height))
        elif g.startswith('OBJ_EVENT_GFX_CRUISE_SHIP_'):
            s = A.sprite('graphics/object_events/pics/misc/cruise_ship_%s.png' % g[-1], 'graphics/object_events/palettes/ss_tidal.pal')
            im.alpha_composite(s, (tx * 16 + 8 - 32, (ty + 1) * 16 - 48))
        elif g == 'OBJ_EVENT_GFX_MR_BRINEYS_BOAT':
            mv = e['movement_type']; s = A.briney_boat(0 if mv.endswith('DOWN') else 2)
            if mv.endswith('RIGHT'): s = s.transpose(Image.FLIP_LEFT_RIGHT)
            im.alpha_composite(s, (tx * 16 - 8, (ty + 1) * 16 - 32))
    if labels:
        d = ImageDraw.Draw(im)
        try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
        except Exception: font = ImageFont.load_default()
        for x, y, t in LABELS:
            px, py = (x + OX) * 16, (y + OY) * 16
            bb = d.textbbox((px, py), t, font=font)
            d.rectangle([bb[0] - 4, bb[1] - 3, bb[2] + 4, bb[3] + 3], fill=(255, 255, 255, 220), outline=(30, 30, 60, 255))
            d.text((px, py), t, fill=(20, 20, 70, 255), font=font)
    im.convert('RGB').save(out)

LABELS = [(-12, -1, 'Museu'), (-14, 3, 'Casa Neves'), (-1, 1, 'Casas do L'), (-16, 10, 'Rota 121 ←'), (-15, 12, 'Ed. Lilás'),
          (-15, 19, 'Casa Ventura'), (-15, 27, 'Brisa do Mar'), (-15, 34, 'Res. Coral'), (1, 13, 'SHOPPING'), (-1, 23, 'Bicicletário'),
          (0, 28, 'Café Litoral'), (24, 12, 'Centro de Concursos'), (22, 29, 'Praça das Fontes'), (41, 12, 'Motel'),
          (17, 1, 'Bairro 2'), (55, 6, 'Hotel (futuro)'), (50, 33, 'PRAIA'), (20, 42, 'Calçadão / Mercado'),
          (20, 60, 'Cruzeiro'), (3, 55, 'Píer dos pescadores')]

if __name__ == '__main__':
    build(sys.argv[1], '--labels' in sys.argv)
