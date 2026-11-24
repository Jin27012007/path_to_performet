"""Route 121 redesign: a more natural route. Fences removed, organic tall grass, flowers, a simple sand
path from Lilycove (east) to the Safari Zone and on to Route 120, and two berry plantations.
Rebuilds data/layouts/Route121/map.bin and the object events of data/maps/Route121/map.json from the
pristine copies next to this script, so it can be re-run."""
import json, math, os, random, struct
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.join(HERE, '..', '..')
W, H = 80, 20
raw = open(os.path.join(HERE, 'base_map.bin'), 'rb').read()
M = [[struct.unpack_from('<H', raw, (y * W + x) * 2)[0] for x in range(W)] for y in range(H)]
mt = lambda x, y: M[y][x] & 0x3ff
def put(x, y, m): M[y][x] = m | (3 << 12)                 # walkable, elevation 3

GRASS, FLOWER, TALL, SOIL = 0x001, 0x004, 0x00d, 0x14c
GRASSLIKE = {0x001, 0x002, 0x004, 0x00d}
STAIRS = {0x0af, 0x0cf}
# 1. clear fences, old tall grass, old soil patches and the old sand decor into plain grass
CLEAR = {0x250, 0x251, 0x252, 0x258, 0x25a, 0x341, 0x00d, 0x002,
         0x273, 0x14c, 0x275, 0x27b, 0x114, 0x27d, 0x103, 0x104, 0x105, 0x2d5, 0x2dd, 0x2e5} | set(range(0x118, 0x12b))
for y in range(H):
    for x in range(W):
        if mt(x, y) in CLEAR: put(x, y, GRASS)

# 2. the sand path (2 wide; cells next to cliffs need no grass rim)
P = set()
def rect(x0, y0, x1, y1):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): P.add((x, y))
rect(70, 6, 79, 7)        # from Lilycove (east edge)
rect(70, 6, 71, 13)       # down to the main path
rect(35, 12, 71, 13)      # main path west to the stairs below the Safari Zone
rect(37, 9, 43, 10)       # between the two stairs
rect(37, 6, 38, 7)        # up to the Safari Zone door
rect(30, 12, 34, 12)      # to the stairs from the west plain
rect(30, 8, 31, 9)        # stairs top -> west path
rect(0, 6, 31, 7)         # west, to Route 120
def pathlike(x, y):
    if not (0 <= x < W and 0 <= y < H): return True
    return (x, y) in P or mt(x, y) not in GRASSLIKE
for (x, y) in P:
    n, s, w, e = (not pathlike(x, y - 1), not pathlike(x, y + 1), not pathlike(x - 1, y), not pathlike(x + 1, y))
    if n: m = 0x118 if w else (0x11a if e else 0x119)
    elif s: m = 0x128 if w else (0x12a if e else 0x129)
    else: m = 0x120 if w else (0x122 if e else 0x121)
    put(x, y, m)

# 3. berry plantations: soft soil rows, trees placed as objects below
FIELDS = [((2, 7), (9, 11)), ((50, 55), (8, 10))]      # (x0, x1), soil rows
FIELD_CELLS = []
for (x0, x1), rows in FIELDS:
    for y in rows:
        for x in range(x0, x1 + 1): put(x, y, SOIL); FIELD_CELLS.append((x, y))
KEEP_CLEAR = set(P) | set(FIELD_CELLS)
for (x0, x1), rows in FIELDS:                           # rows the player walks to reach the trees
    for y in range(min(rows) - 1, max(rows) + 2):
        for x in range(x0 - 1, x1 + 2): KEEP_CLEAR.add((x, y))

# 4. organic tall grass
rnd = random.Random(121)
BLOBS = [(14, 9.3, 3.4, 1.4), (23.5, 8.8, 3.2, 1.3), (4, 12.9, 3.4, 1.0), (49, 14.2, 8.5, 0.9),
         (64, 10, 3.2, 1.5), (47, 9.6, 1.7, 1.8), (62.5, 2.6, 3.6, 1.1), (50, 2.6, 3.4, 1.1), (30.5, 2.6, 3.2, 1.0)]
for cx, cy, rx, ry in BLOBS:
    for y in range(H):
        for x in range(W):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            wob = 0.25 * math.sin(x * 1.7 + y * 2.3) + 0.2 * math.sin(x * 0.9 - y * 1.3)
            if d <= 1.0 + wob and mt(x, y) == GRASS and (x, y) not in KEEP_CLEAR: put(x, y, TALL)

# 5. flowers: along the path, around the plantations and scattered on the lawns
near = lambda x, y, S: any((x + dx, y + dy) in S for dx in (-1, 0, 1) for dy in (-1, 0, 1))
for y in range(H):
    for x in range(W):
        if mt(x, y) != GRASS or (x, y) in KEEP_CLEAR and (x, y) not in P: continue
        p = 0.0
        if near(x, y, P): p = 0.22
        elif near(x, y, set(FIELD_CELLS)) : p = 0.35
        else: p = 0.06
        if rnd.random() < p: put(x, y, FLOWER)

out = b''.join(struct.pack('<H', M[y][x]) for y in range(H) for x in range(W))
open(os.path.join(REPO, 'data/layouts/Route121/map.bin'), 'wb').write(out)

# 6. objects: the 8 original berry trees join the plantations, 16 new ones fill them, NPCs make room
d = json.load(open(os.path.join(HERE, 'base_map.json')))
objs = d['object_events']
spots = FIELD_CELLS                                   # 24 soil cells
old = [o for o in objs if o['graphics_id'] == 'OBJ_EVENT_GFX_BERRY_TREE']
order = spots[:4] + spots[12:16] + spots[4:12] + spots[16:]    # 4 old per field first
for o, (x, y) in zip(old, order[:8]): o['x'], o['y'] = x, y
for i, (x, y) in enumerate(order[8:]):
    objs.append({'graphics_id': 'OBJ_EVENT_GFX_BERRY_TREE', 'x': x, 'y': y, 'elevation': 3,
                 'movement_type': 'MOVEMENT_TYPE_BERRY_TREE_GROWTH', 'movement_range_x': 0, 'movement_range_y': 0,
                 'trainer_type': 'TRAINER_TYPE_NONE', 'trainer_sight_or_berry_tree_id': 'BERRY_TREE_ROUTE_121_FIELD_%02d' % (i + 1),
                 'script': 'BerryTreeScript', 'flag': '0'})
MOVES = {(55, 8): (66, 11), (55, 10): (76, 8), (59, 8): (68, 9), (59, 13): (64, 14), (60, 10): (74, 11),
         (38, 13): (40, 14), (11, 6): (16, 6), (11, 11): (17, 11)}
for o in objs:
    if (o['x'], o['y']) in MOVES and o['graphics_id'] != 'OBJ_EVENT_GFX_BERRY_TREE': o['x'], o['y'] = MOVES[(o['x'], o['y'])]
json.dump(d, open(os.path.join(REPO, 'data/maps/Route121/map.json'), 'w'), indent=2)
open(os.path.join(REPO, 'data/maps/Route121/map.json'), 'a').write('\n')
# sanity: every object stands on a walkable cell that is not a tree/fence
for o in objs:
    v = M[o['y']][o['x']]
    if (v >> 10) & 3 and o['graphics_id'] not in ('OBJ_EVENT_GFX_CUTTABLE_TREE',): print('blocked object', o['graphics_id'], o['x'], o['y'], hex(v & 0x3ff))
print('objects', len(objs))
