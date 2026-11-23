"""Builds gTileset_LilycoveCity, a secondary tileset used only by Lilycove City.

It starts from the shared Lilycove tileset (which also serves Routes 121-123 and the
Safari Zone), keeps exactly the metatiles the city map uses -- with the SAME ids, so
door animations and scripts keep working -- and recycles every other tile and
metatile slot for the port art in port_art.py.

Placeholders in the composed map are tuples ('ART', key, collision, elevation) where
key = (art name, mx, my, palette, bottom layer).
"""
import os, struct, json, shutil
from PIL import Image
import port_art

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..'))
SRC = os.path.join(REPO, 'data/tilesets/secondary/lilycove')
DST = os.path.join(REPO, 'data/tilesets/secondary/lilycove_city')
SHORT = [0]
MAX_TILES = 504          # tiles 504-511 of the secondary block are used by door animations
DOORS = (0x246, 0x28E, 0x30C, 0x32D)
SHARED_LAYOUTS = (('Route121', 80, 66),)
# Generic pieces live in the PRIMARY tileset (gTileset_General), so they cost no city tiles and
# also render across the Route 121 seam. Built from a pristine copy in base_tileset/general.
PRIM = os.path.join(REPO, 'data/tilesets/primary/general')
PRIM_BASE = os.path.join(HERE, 'base_tileset/general')
PRIMARY_ART = {'paving', 'lamp_modern', 'lamp_modern_l', 'bunting', 'mall_pokeball', 'bench'} | set(port_art.FLOWER_NAMES)
PRIMARY_BOTTOMS = {'grass', 'paving'}
# General metatiles no General-tileset map uses and no metatile label names (checked over all layouts)
PRIMARY_META_POOL = [0x1ea, 0x1eb, 0x1f8, 0x1f9, 0x1fa, 0x1fb, 0x183, 0x187, 0x18b, 0x18c, 0x199, 0x1a2,
                     0x1b6, 0x1e3, 0x17f, 0x160, 0x161, 0x143, 0x144, 0x13f, 0x13b, 0x13c]
ANIM_TILES = set(range(432, 462)) | set(range(464, 474)) | set(range(480, 490)) | set(range(496, 502)) | set(range(508, 512))

def _load_primary():
    im = Image.open(os.path.join(PRIM_BASE, 'tiles.png')); p = im.load(); tw = im.width // 8
    tiles = [[[p[(i % tw) * 8 + x, (i // tw) * 8 + y] & 15 for x in range(8)] for y in range(8)]
             for i in range(tw * (im.height // 8))]
    raw = open(os.path.join(PRIM_BASE, 'metatiles.bin'), 'rb').read()
    metas = [list(struct.unpack_from('<8H', raw, i)) for i in range(0, len(raw), 16)]
    att = open(os.path.join(PRIM_BASE, 'metatile_attributes.bin'), 'rb').read()
    attrs = list(struct.unpack('<%dH' % (len(att) // 2), att))
    used = {e & 0x3ff for m in metas for e in m}
    free = [i for i, t in enumerate(tiles) if i and i not in used and i not in ANIM_TILES
            and all(v == 0 for r in t for v in r)]
    return im, tiles, metas, attrs, free

def _load():
    im = Image.open(os.path.join(SRC, 'tiles.png')); p = im.load()
    tiles = [[[p[tx * 8 + x, ty * 8 + y] & 15 for x in range(8)] for y in range(8)]
             for ty in range(im.height // 8) for tx in range(im.width // 8)]
    raw = open(os.path.join(SRC, 'metatiles.bin'), 'rb').read()
    metas = [list(struct.unpack_from('<8H', raw, i)) for i in range(0, len(raw), 16)]
    att = open(os.path.join(SRC, 'metatile_attributes.bin'), 'rb').read()
    attrs = list(struct.unpack('<%dH' % (len(att) // 2), att))
    return tiles, metas, attrs

def _split16(c, mx, my):
    out = []
    for qy in range(2):
        for qx in range(2):
            out.append([row[mx * 16 + qx * 8: mx * 16 + qx * 8 + 8] for row in c[my * 16 + qy * 8: my * 16 + qy * 8 + 8]])
    return out

def build(M, festival_ids):
    tiles, metas, attrs = _load()
    prim = open(os.path.join(REPO, 'data/tilesets/primary/general/metatiles.bin'), 'rb').read()
    pmeta = lambda m: list(struct.unpack_from('<8H', prim, m * 16))
    BOTTOM = {
        'water': pmeta(0x170)[:4],
        'shallow': pmeta(0x19e)[:4],
        'dock': metas[festival_ids['dock'] - 512][:4],
        'brick': metas[festival_ids['brick'] - 512][:4],
        'grass': pmeta(0x001)[:4],
        'cobble': metas[0x233 - 512][:4],
        'sand': pmeta(0x124)[:4],
    }
    used = {v & 0x3ff for row in M for v in row if isinstance(v, int) and (v & 0x3ff) >= 512} | set(DOORS)
    # Route 121 shares this tileset (connected maps are drawn with the current map's
    # tileset), so its metatiles are kept with their original ids too.
    # Connected maps are drawn with the CURRENT map's tileset: keep the metatiles of
    # Route 121's east strip (visible from Lilycove) with their original ids.
    for shared, width, x0 in SHARED_LAYOUTS:
        d = open(os.path.join(REPO, 'data/layouts', shared, 'map.bin'), 'rb').read()
        h = len(d) // 2 // width
        used |= {struct.unpack_from('<H', d, (y * width + x) * 2)[0] & 0x3ff
                 for y in range(h) for x in range(x0, width)} - set(range(512))
    keep_tiles = set()
    for m in used:
        for e in metas[m - 512]:
            if (e & 0x3ff) >= 512: keep_tiles.add((e & 0x3ff) - 512)
    free_tiles = [i for i in range(MAX_TILES) if i not in keep_tiles and i != 0]
    free_meta = [m for m in range(512, 1024) if m not in used]
    # blank everything that is not used
    new_tiles = [t if i in keep_tiles else [[0] * 8 for _ in range(8)] for i, t in enumerate(tiles[:512])]
    new_tiles += [[[0] * 8 for _ in range(8)] for _ in range(512 - len(new_tiles))]
    new_metas = {m: metas[m - 512] for m in used}
    new_attrs = {m: attrs[m - 512] for m in used}
    # art
    canvases = {}
    tile_index = {}
    art_ids = {}
    pim, ptiles, pmetas, pattrs, pfree = _load_primary()
    pmeta_pool = list(PRIMARY_META_POOL); ptile_index = {}
    def add_ptile(t):
        if all(v == 0 for r in t for v in r): return 0
        k = tuple(tuple(r) for r in t)
        if k not in ptile_index:
            if not pfree: raise SystemExit('primary tileset: out of free tiles')
            i = pfree.pop(0); ptiles[i] = [list(r) for r in t]
            h = tuple(tuple(r[::-1]) for r in k); v = tuple(k[::-1]); hv = tuple(tuple(r[::-1]) for r in k[::-1])
            for key, bits in ((hv, 0xC00), (v, 0x800), (h, 0x400), (k, 0)):
                ptile_index[key] = i | bits
        return ptile_index[k]
    def add_tile(t):
        """Adds an 8x8 tile, reusing an existing one when it matches directly or mirrored
        (the returned value carries the GBA h/v-flip bits)."""
        if all(v == 0 for r in t for v in r): return 0
        k = tuple(tuple(r) for r in t)
        if k not in tile_index:
            if not free_tiles:
                SHORT[0] += 1; return 0
            i = free_tiles.pop(0); new_tiles[i] = [list(r) for r in t]; base = 512 + i
            h = tuple(tuple(r[::-1]) for r in k); v = tuple(k[::-1]); hv = tuple(tuple(r[::-1]) for r in k[::-1])
            for key, bits in ((hv, 0xC00), (v, 0x800), (h, 0x400), (k, 0)):
                tile_index[key] = base | bits
        return tile_index[k]
    keys = sorted({v[1] for row in M for v in row if isinstance(v, tuple)}, key=lambda k: (k[0] not in port_art.FLOOR, str(k)))
    prim_ids = []
    meta_by_sig = {}
    for key in keys:
        name, mx, my, pal, bottom = key
        pal = port_art.PAL_OF.get(name, 0)
        if name == 'nadoor':                       # street floor that behaves as a (non-animated) door
            mid = free_meta.pop(0); new_metas[mid] = (metas[festival_ids['carpet'] - 512][:4] if bottom == 'carpet' else BOTTOM['paving']) + [0] * 4; new_attrs[mid] = 0x0060
            art_ids[key] = mid; continue
        if name.startswith('copy:'):              # an existing metatile's top layer over another floor
            prim = False; top = list(metas[int(name[5:], 16) - 512][4:])
        else:
          if name not in canvases: canvases[name] = port_art.ART[name]()
          prim = name in PRIMARY_ART
          top = []
          tp = port_art.TILEPAL.get(name)
          for qi, q in enumerate(_split16(canvases[name], mx, my)):
            t = add_ptile(q) if prim else add_tile(q)
            pq = tp[my * 2 + qi // 2][mx * 2 + qi % 2] if tp else pal
            top.append(t | (pq << 12) if t else 0)
        if isinstance(bottom, str) and bottom.startswith('top:'):     # another metatile's top layer as the floor
            BOTTOM[bottom] = metas[int(bottom[4:], 16) - 512][4:]
        entries = top + [0] * 4 if name in port_art.FLOOR else BOTTOM[bottom] + top
        if name in port_art.FLOOR: BOTTOM[name] = top
        if prim and (name in port_art.FLOOR or bottom in PRIMARY_BOTTOMS):
            if not pmeta_pool: raise SystemExit('primary tileset: out of free metatiles')
            mid = pmeta_pool.pop(0); pmetas[mid] = entries; pattrs[mid] = 0; prim_ids.append(mid)
        else:
            attr = (0x0060 if key in port_art.DOOR_KEYS else 0) | (0x1000 if name in port_art.COVERED_ART else 0)
            sig = (tuple(entries), attr)
            if sig in meta_by_sig:                  # identical metatile already made: share it
                mid = meta_by_sig[sig]
            else:
                if not free_meta: raise SystemExit('out of metatiles for port art')
                mid = free_meta.pop(0); meta_by_sig[sig] = mid
                new_metas[mid] = entries; new_attrs[mid] = attr
        art_ids[key] = mid
    # resolve placeholders
    out = [[(art_ids[v[1]] | (v[2] << 10) | (v[3] << 12)) if isinstance(v, tuple) else v for v in row] for row in M]
    # write tileset
    os.makedirs(os.path.join(DST, 'palettes'), exist_ok=True)
    for f in os.listdir(os.path.join(SRC, 'palettes')):
        shutil.copy(os.path.join(SRC, 'palettes', f), os.path.join(DST, 'palettes', f))
    for slot, pal in port_art.PALETTES.items():      # authentic port art palettes
        with open(os.path.join(DST, 'palettes', '%02d.pal' % slot), 'w', newline='\r\n') as f:
            f.write('JASC-PAL\n0100\n16\n' + ''.join('%d %d %d\n' % c for c in pal))
    src_png = Image.open(os.path.join(SRC, 'tiles.png'))
    img = Image.new('P', (128, 256)); img.putpalette(src_png.getpalette()); p = img.load()
    for i, t in enumerate(new_tiles):
        for y in range(8):
            for x in range(8): p[(i % 16) * 8 + x, (i // 16) * 8 + y] = t[y][x]
    img.save(os.path.join(DST, 'tiles.png'))
    count = max(new_metas) - 511
    mb = b''.join(struct.pack('<8H', *new_metas.get(512 + i, [0] * 8)) for i in range(count))
    ab = b''.join(struct.pack('<H', new_attrs.get(512 + i, 0)) for i in range(count))
    open(os.path.join(DST, 'metatiles.bin'), 'wb').write(mb)
    open(os.path.join(DST, 'metatile_attributes.bin'), 'wb').write(ab)
    # write the primary tileset (pristine base + generic pieces)
    out_im = Image.new('P', pim.size); out_im.putpalette(pim.getpalette()); op = out_im.load(); tw = pim.width // 8
    for i, t in enumerate(ptiles):
        for y in range(8):
            for x in range(8): op[(i % tw) * 8 + x, (i // tw) * 8 + y] = t[y][x]
    out_im.save(os.path.join(PRIM, 'tiles.png'))
    open(os.path.join(PRIM, 'metatiles.bin'), 'wb').write(b''.join(struct.pack('<8H', *m) for m in pmetas))
    open(os.path.join(PRIM, 'metatile_attributes.bin'), 'wb').write(struct.pack('<%dH' % len(pattrs), *pattrs))
    print('primary tileset: %d generic metatiles, %d free tiles left' % (len(prim_ids), len(pfree)))
    if SHORT[0]: print('*** SHORT OF %d TILES ***' % SHORT[0])
    print('city tileset: %d metatiles used, %d art metatiles, %d free tiles left, %d free metatiles left'
          % (len(used), len(art_ids), len(free_tiles), len(free_meta)))
    return out
