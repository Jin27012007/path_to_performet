from compose import *
fill(-OX,-OY,W-OX,H-OY,GRASS)
# ================= sea =================
fill(52,-OY,W,H,DEEP); fill(0,42,W,H,DEEP)
# ================= borders =================
trees(0,-OY,52,2,grass_above=False)
trees(0,2,2,20,grass_above=False)
trees(0,24,2,40)
# ================= NORTH BAND (y2-10) =================
museum(2,2)                                  # stairs bottom at (6..9,10)
for cx in (0,1,9,10,11,12): put(2+cx,2,GRASS)
path(6,10,10,11)
house(17,2); house(23,2); house(29,2)        # doors (18,5) (24,5) (30,5)
path(17,6,37,7)
house(17,7); fanclub(23,7)                   # doors (18,10) (25,10)
flowers(29,7,36,8); tree1(30,7); tree1(33,7); put(29,9,FLOWERS); put(35,9,FLOWERS)
path(36,2,38,11)
dept(40,2)                                   # door (44,8)
lamp(39,8); lamp(49,8); flowers(39,9,50,10); 
path(43,9,47,11)
# north street
path(2,11,51,13)
# ================= MIDDLE BAND (y13-19) =================
pc(3,14); house(9,14)                        # doors (4,17) (10,17)
flowers(7,14,9,18); path(3,18,14,20)
# (the Contest Hall is drawn at the end, see CONTEST HALL)

motel(41,13)                                 # door (42,17)
pond(47,14); fence(46,51,16); flowers(46,17,51,18)
path(41,18,46,19)
# ================= AVENUE (y20-22) =================
path(0,20,42,23)

# boulevard lamps
for x in (5,11,35,39): lamp(x,23)
# ================= PLAZA: drawn at the end (see PLAZA section below) =================
# ================= HARBOR (left) =================
harbor(4,26)                                 # door (7,31)
brickfill(2,32,14,36)
tree1(2,23) if False else None
trees(11,24,13,31)
flowers(2,24,4,31)
# ================= PROMENADE + WOODEN BOARDWALK =================
brickfill(2,36,14,40)                  # promenade west of the plaza
# (the boardwalk itself is drawn at the end, after the beach, see boardwalk())
# ================= BEACH (right) =================
SX0,SX1,SY0,SY1=42,49,19,40   # sand area (meets the boardwalk at row 40)
fill(42,19,52,40,SHALLOW)
fill(SX0,SY0,SX1,SY1,T(0x121))
for y in range(SY0,SY1): put(SX0,y,T(0x120))
for x in range(SX0,SX1): put(x,SY0,T(0x119))
put(SX0,SY0,T(0x118))
for y in range(SY0+1,SY1-1): put(SX1-1,y,T(0x19f))
for x in range(SX0+1,SX1-1): put(x,SY1-1,T(0x1a6))
put(SX1-1,SY1-1,T(0x1a7)); put(SX0,SY1-1,T(0x1a5)); put(SX1-1,SY0,T(0x197))
fill(41,20,42,40,GRASS)
for x in range(46,52): put(x,18,T(0x079,1,0))
fill(41,19,42,40,GRASS)
for y in range(2,19): put(51,y,T(0x075,1,0))
# shallow->deep transitions
for y in range(19,40): put(52,y,T(0x1b7,0,1))
# bottom-left corner tidy
trees(0,24,2,40); 
# Aqua cave islet (keeps original warp target)

# promenade planters (avoid pier axes x=7, x=27)
for x in (3,): put(x,37,T(0x005,1,0))
# central fountain on main axis
# sign posts for bg_events
for sx,sy in [(10,10),(47,9),(2,19),(40,17),(3,31),(22,10),(16,5)]: sign(sx,sy)

# ================= FESTIVAL DRESSING (World Contest Season) =================
bunting(2,46,21)                                   # across the avenue
bunting(2,14,38)                                   # promenade (west part)
bunting(16,38,11)                                  # north street
# palms along the promenade
for px_ in (2,10): palm(px_,36,'brick')   # promenade palms, outside the plaza
# beach: umbrellas + palms
# (the beach is drawn at the end, see BEACH)

# ================= PORT: BOARDWALK, PIERS, STALLS, BOATS AND THE CRUISE SHIP =================
fill(-OX,40,52,H,DEEP)
def D(name, walk=True): return T(F[name],0,3) if walk else T(F[name],1,0)
def posts(x0,x1,y):
    for x in range(x0,x1): put(x,y,T(F['dock_posts'],1,1))
def deck(x0,x1,y0,y1,joins_top=(),joins_bottom=(),posts_below=True):
    """rectangle of planks with beams on its outer edges"""
    for y in range(y0,y1):
        for x in range(x0,x1):
            t = y==y0 and x not in joins_top; b = y==y1-1 and x not in joins_bottom
            l = x==x0; r = x==x1-1
            name='dock'+('_'+''.join(k for k,f in zip('tblr',(t,b,l,r)) if f) if (t or b or l or r) else '')
            put(x,y,D(name))
    if posts_below: posts(x0,x1,y1)
def pier(x0,y0,y1):      # 3-wide vertical pier
    for y in range(y0,y1):
        put(x0,y,D('dock_l')); put(x0+1,y,D('dock')); put(x0+2,y,D('dock_r'))

MAIN_PIER=24             # columns 24..26
FISH_PIER=4              # columns 4..6
# boardwalk: 4 rows, from the harbor all the way to the beach (x 0..51)
deck(-OX,52,40,44,joins_bottom=(MAIN_PIER,MAIN_PIER+1,MAIN_PIER+2,FISH_PIER,FISH_PIER+1,FISH_PIER+2),posts_below=False)
for x in range(-OX,52):
    if x not in (MAIN_PIER,MAIN_PIER+1,MAIN_PIER+2,FISH_PIER,FISH_PIER+1,FISH_PIER+2): put(x,44,T(F['dock_posts'],1,1))
# main pier: long, the cruise ship is moored along its east side
pier(MAIN_PIER,44,55)
deck(19,32,55,57,joins_top=(MAIN_PIER,MAIN_PIER+1,MAIN_PIER+2))
# the cruise ship is a sprite (object events OBJ_EVENT_GFX_CRUISE_SHIP_0..3, see map.json)

# fishermen's pier with two finger docks and moored boats
pier(FISH_PIER,44,53)
deck(FISH_PIER+3,13,47,48); deck(FISH_PIER+3,13,51,52)
deck(1,10,53,55,joins_top=(FISH_PIER,FISH_PIER+1,FISH_PIER+2))
# moored fishing boats: Mr. Briney's boat sprite (object events, see map.json)
# market tents along the boardwalk (Slateport-style), with goods around them
decor('tent_green',8,40,walk_rows=2); decor('tent_pots',14,40,walk_rows=2)          # stalls are sprites
decor('tent_flowers',32,40,walk_rows=2); decor('tent_green',38,40,walk_rows=2)
for (n,x,y) in [('basket_orange',13,42),('crate_label',19,41),('basket_green',31,42),('basket_orange',7,42)]:
    art(n,x,y,bottom='dock')
# crates and mooring posts (the father waits next to the crates)
for (x,y) in [(30,42),(30,41),(2,41),(22,41),(37,42),(43,41)]: put(x,y,D('dock_crate',False))
for (x,y) in [(21,43),(33,43),(46,43),(19,56),(31,56)]: put(x,y,D('dock_bollard',False))
# fishing boats around the bay and at the beach

# ================= PLAZA (x14-40, y23-39): grey tiles, inverted brick cross, lawns, fountains ===========
paving(14,23,41,40)                       # grey tiles: contour and walkways
brickfill(25,23,30,40)                    # long arm of the cross, pointing at the Contest Hall
brickfill(16,24,39,27)                    # cross bar, right below the hall
for side,lx0 in (('L',15),('R',31)):      # two lawns (x lx0..lx0+8, rows 28..38), mirrored about x=27
    fill(lx0,28,lx0+9,39,GRASS)
    fx = lx0+2                            # 5-wide fountain centred in the lawn (2 tiles of margin each side)
    ring = {(x,y) for x in range(fx,fx+5) for y in range(31,34)}     # the fountain itself
    corner_trees = [(lx0,28),(lx0+7,28)]
    tree_tiles = {(x+dx,y+dy) for (x,y) in corner_trees for dx in (0,1) for dy in (0,1,2)}
    flowerfield(lx0,28,lx0+9,36,seed=7 if side=='L' else 7,skip=ring|tree_tiles)
    for (tx,ty) in corner_trees: tree1(tx,ty)
    art('fountain_modern',fx,31,bottom='grass')
    flowerbed(lx0,36,9,3)                 # long kerbed flowerbed along the bottom of the lawn
    for x in range(lx0+1,lx0+8):          # ...planted with mixed flowers
        art(FLOWER_KINDS[(x*3)%5],x,37,bottom='grass') if x%3 else put(x,37,T(0x004,1,0))
# modern lamp posts (same spots) with bunting strung between their heads
for y in (28,33,38):
    lamp2(24,y); lamp2(30,y,facing='left'); bunting2(25,30,y-1,'brick')
lamp2(15,25); lamp2(39,25,facing='left'); bunting2(16,39,24,'brick')

# ================= RESIDENTIAL DISTRICT 1 (west): uphill street from the pier to the museum =========
# logical x -16..14 (the map was widened 16 columns to the west and 8 rows to the north for it)
import random as _random
STREET = (-8, -5)                      # street columns -8..-6, stone paving, from the boardwalk up to the museum
SAND = {(1,0,1,0):0x118,(1,0,0,0):0x119,(1,0,0,1):0x11a,(0,0,1,0):0x120,(0,0,0,0):0x121,(0,0,0,1):0x122,
        (0,1,1,0):0x128,(0,1,0,0):0x129,(0,1,0,1):0x12a}
def trail(x0,y0,x1,y1,open_sides='',door_cols=()):
    """dirt trail with soft grass edges (Emerald sand autotile). open_sides: edges that touch
    the street/another floor and get no grass fringe; door_cols: top-row columns under a door."""
    for y in range(y0,y1):
        for x in range(x0,x1):
            t = y==y0 and 't' not in open_sides and x not in door_cols
            b = y==y1-1 and 'b' not in open_sides
            l = x==x0 and 'l' not in open_sides
            r = x==x1-1 and 'r' not in open_sides
            put(x,y,T(SAND[(int(t),int(b),int(l),int(r))]))
def stairs3(x,y0,y1):                  # 3-wide stone stairs (Emerald pieces 0af | 0cf 0cf)
    for y in range(y0,y1): put(x,y,T(0x0af)); put(x+1,y,T(0x0cf)); put(x+2,y,T(0x0cf))
def ledge(x0,x1,y):
    for x in range(x0,x1): put(x,y,T(0x07c,1,0))
def house_sign(x,y): sign(x,y)
def garden(x0,y0,x1,y1,seed,skip=(),shared=False):
    """grass with scattered flowers; shared=True uses only the original red flower (seam strip)"""
    rnd=_random.Random(seed)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if (x,y) in skip: continue
            k=rnd.random()
            if k<0.62: continue
            if shared or k<0.72: put(x,y,FLOWERS)
            else: art(FLOWER_KINDS[int(k*97)%5],x,y,bottom='grass',walk_rows=1)

fill(-16,-8,15,20,GRASS); fill(15,-8,17,11,GRASS); fill(-16,20,14,40,GRASS)     # clear the area
trees(-16,-12,18,-8,grass_above=False)                                   # forest above the museum (rows added north)
trees(-16,-8,-13,1,grass_above=False); trees(-1,-8,17,0,grass_above=False)   # forest around the museum
# --- the Lilycove Museum, contemporary (museum_art.py): on flat ground, a stone terrace and a path to the
# street, lawns with two steel sculptures on pedestals, hedges and flowers; doors (-8,-3) (-7,-3)
import port_art as _pmu
fill(-14, -8, 0, 3, GRASS)
art('museum_new', -11, -8, bottom='paving')                        # 10 x 6, rows -8..-3: centred on the street (-8..-5)
for dx_ in (4, 5):                                                  # the glass doors (walk in -> museum)
    _k = ('museum_new', dx_, 5, None, 'paving'); _pmu.DOOR_KEYS.add(_k); put(-11 + dx_, -3, ('ART', _k, 0, 3))
# everything below mirrors around the street's axis (x -> -13 - x)
paving(-11, -2, -1, -1)                                             # terrace in front of the museum
paving(-14, -8, -11, -1); paving(-1, -8, 0, -1)                     # paved all around the museum (east and west)
paving(-8, -1, -4, 1)                                               # path: the street running up to the doors (4 wide)
paving(-10, 1, -2, 3)                                               # forecourt by the street
art('museum_sculpture', -10, -1, bottom='grass', walk_rows=1)       # two steel sculptures on the lawns
art('museum_sculpture_r', -3, -1, bottom='grass', walk_rows=1)
tree1(-12, -1); tree1(-2, -1)                                       # hedges at the corners
for (fx_, fy_) in ((-9, -1), (-4, -1), (-12, 2), (-11, 2), (-2, 2), (-1, 2)):
    put(fx_, fy_, FLOWERS)
paving(STREET[0],1,STREET[1],40)                                   # the uphill residential street
paving(STREET[1],1,STREET[1]+1,11)                                 # one column wider below the museum (4 wide, on its axis)
paving(-16,11,15,13)                                               # north street (open to Route 121, rows 10..12)
paving(STREET[0],20,14,23)                                         # avenue to the plaza

# --- upper line (row of H5): H5 west of the street, the L houses east of it; back gardens above
# x -16..-9, rows 3..25 is what Route 121 shows across the connection (drawn with the shared Lilycove
# tileset), so that strip only uses original/shared pieces: classic houses, fences and the generic
# pieces of the primary tileset (flowers, lamps, paving).
house(-14,5); paving(-14,9,-11,11); house_sign(-10,8)            # H5 classic, door (-13,8)
garden(-16,1,-10,5,11,shared=False); fence(-16,-14,10); fence(-11,-9,10)
tree1(-16,6) if False else None
house(-4,5);  paving(-4,9,-1,11); house_sign(-5,8)               # L1 classic = House 3, door (-3,8)
art('house_beige_lilac',2,4); paving(3,9,6,11); house_sign(1,8)         # L2 modern beige, door (4,8)
art('house_grey',9,4);  paving(10,9,13,11); house_sign(8,8)      # L3 modern grey, door (11,8)
garden(-4,1,15,4,12); tree1(6,1); tree1(13,1)                 # back gardens with small trees
fill(-4, 1, -1, 3, GRASS); paving(-4, 1, -2, 3); tree1(-2, -1)                 # keep the museum lawn's east half (mirror of the west)
put(-2, 2, FLOWERS); put(-1, 2, FLOWERS)
garden(0,4,2,9,13); garden(7,4,9,9,14); garden(14,4,15,9,15)               # side yards with flowers
fence(-1,1,10) if False else None
for (fx0,fx1) in ((0,3),(6,10),(13,15)): fence(fx0,fx1,10)                  # low front fences
fence(-5,-4,10) if False else None

# --- west lot, below the north street: H4, H3 | terrain step | H2, H1
fanclub(-15,13); paving(-14,17,-8,19); house_sign(-10,16)        # H4 "Edificio Lilas", door (-13,16)
garden(-16,13,-15,17,21,shared=False); garden(-10,13,-8,16,22,shared=False)
fence(-16,-9,19)                                                            # lot boundary
house(-14,20); paving(-14,24,-8,26); house_sign(-10,23)          # H3 classic, door (-13,23)
garden(-16,20,-14,24,23,shared=False); garden(-10,20,-8,23,24,shared=False)
ledge(-16,-8,26); stairs3(STREET[0],26,28)                                  # terrain step + 3-wide stairs
art('apartments',-16,28); paving(-14,33,-8,35); house_sign(-9,32)  # H2 modern apartments, door (-13,32)
garden(-16,27,-8,28,25); garden(-9,28,-8,32,26)
art('house_grey_coral',-15,35); house_sign(-10,38)                               # H1 modern grey, door (-13,39) onto the boardwalk
garden(-16,35,-15,40,27); garden(-10,35,-8,38,28); fence(-10,-8,39) if False else None
# --- east of the street: the old L lot becomes a small neighbourhood garden
# --- the shopping mall (Lilycove Dept. Store) fills the block between the north street and the avenue.
# Built from the original Dept. Store pieces, stretched: blue facade with windows, shop windows with
# awnings (vitrines), two double glass doors; plus the contest screen, the Poké Ball and pennants.
def mall(x0,y0,W=18):
    O=lambda ox,oy: norm(o(ox,oy))
    for r,oy in enumerate((18,19,19,22)):                                # flat roof (Contest Hall roof pieces)
        put(x0,y0+r,O(20,oy)); put(x0+W-1,y0+r,O(26,oy))
        for x in range(x0+1,x0+W-1): put(x,y0+r,O(21,oy))
    for x in range(x0,x0+W):                                             # roof edge over street floor, not grass
        mid = 0x2c0 if x==x0 else (0x2c2 if x==x0+W-1 else 0x2c1)
        put(x,y0,('ART',('copy:%x'%mid,0,0,None,'paving'),1,0))
    y0+=1
    y=y0+3                                                               # facade band under the roof
    put(x0,y,O(23,1)); put(x0+W-1,y,O(31,1))
    for x in range(x0+1,x0+W-1): put(x,y,O(24,1))
    COL={'2fe':23,'2fc':24,'30f':25,'303':26,'304':27,'305':28,'30e':29,'2ff':31}
    seq=['2fe','2fc','30f','303','304','304','305','30e','2fc','2fc','30f','303','304','304','305','30e','2fc','2ff']
    for i,k in enumerate(seq):
        put(x0+i,y0+4,O(COL[k],5)); put(x0+i,y0+5,O(COL[k],6))          # awnings / vitrines and double doors
    art('mall_ticker',x0+6,y,bottom='top:301')                           # LED band "POKEMON CONTEST"
    for x in range(x0+1,x0+W-1):                                         # pennants under the eave
        if not x0+6<=x<x0+12: art('pennants%d'%((x-x0)%3),x,y,bottom='top:301')
    for dx in (0,1):                                                     # Poké Ball on the roof front
        put(x0+8+dx,y0+1,('ART',('mall_pokeball',dx,0,None,'top:2c9'),1,0))
        put(x0+8+dx,y0+2,('ART',('mall_pokeball',dx,1,None,'top:2d1'),1,0))
fill(-5,13,14,20,GRASS)
mall(-4,13)                                                              # doors (0,19) (1,19) and (8,19) (9,19), onto the avenue
for x in (0,8): art('carpet_mat',x,20,walk_rows=1)                       # small red mats at the two double doors
for x in (-1,2,7,10): art('potted_palm',x,20,bottom='paving',walk_rows=1)   # potted palms flanking the doors
paving(-5,13,-4,20)                                                      # strip beside the mall: street floor
lamp2(-5,16,'paving',facing='left'); art('sign_paving',-5,18,bottom='paving')   # lamp and Dept. Store sign on it
for (px_, py_) in ((-9,10),(-9,13),(-9,16),(-9,19),(-9,23)): paving(px_,py_,px_+1,py_+1)   # corners by the street
garden(-5,23,14,26,32)                                                       # upper level, above the step
paving(-3,23,12,26)                                                          # bike parking in front of the mall (a free paving column by each lawn)
BIKES=('bike_yellow','bike_blue','bike_red')
for gx in (-2,5):                                                            # two groups, three rows of three bikes
    for r in range(3):
        for k in range(3): art(BIKES[(r+k+gx)%3],gx+2*k,23+r,bottom='paving')
ledge(-5,14,26)                                                             # the step continues east of the street
# --- seaside café (replaces the Pokémon Center and the harbor building) on the lower level
fill(-5,27,14,40,GRASS)
for y in range(27,34):                                                      # wooden terrace x -4..13, rows 27..33
    for x in range(-4,14): put(x,y,('ART',('terrace',0,0,None,'water'),0,3))
art('cafe',2,27,bottom='terrace')                                           # Café Litoral, door (4,30)
for k,n in enumerate(('vending_water','vending_lemonade','vending_soda')):  # drink machines (row 29 in front is free)
    art(n,10+k,27,bottom='terrace')
decor('umbrella_set_red',-3,27,walk_rows=1)                                 # umbrella + table + two chairs (sprites)
decor('umbrella_set_blue',10,30,walk_rows=1)
decor('table_set',-3,31); decor('table_set',6,32)                            # small modern tables (sprites)
for (px_,py_) in ((1,27),(8,27),(2,31),(5,31)): art('potted_palm',px_,py_,bottom='terrace',walk_rows=1)  # flank café and entrance
for y in range(27,33):                                                      # fence around the terrace...
    art('fence_wood_vl',-4,y,bottom='terrace'); art('fence_wood_vr',13,y,bottom='terrace')
for x in range(-4,14):                                                      # ...and along the front, entrance at x 3..4
    if x not in (3,4): art('fence_wood',x,33,bottom='terrace')
paving(-5,27,-4,34)                                                         # the strip west of the café: street floor
paving(-5,34,14,36)                                                         # promenade: street -> plaza
paving(-5,36,14,40)                                                         # grey paving down to the boardwalk
decor('tent_flowers',-4,37,walk_rows=2)                                      # flower stall (sprite)
for (px_,py_) in ((3,37),(9,37)): art('potted_palm',px_,py_,bottom='paving',walk_rows=1)
lamp2(12,36,'paving',facing='left')
# --- street lamps along the residential street (east kerb, heads towards the street) and the north street
lamp2(-9,5,'grass'); lamp2(-5,30,'paving',facing='left')
lamp2(-5,37,'paving',facing='left')
for x in (-1,6,13): lamp2(x,10,'paving') if False else None
bunting(-8,14,21)                                                           # avenue bunting (west part)
sign(-16,13); sign(-9,0); sign(-4,0)                                        # city sign, museum signs flanking the path
for (sx,sy) in ((8,8),(1,8),(-5,8),(-10,8),(16,5)): sign(sx,sy)               # house signs over the gardens

# ================= BEACH (east): a natural, horizontal beach under the hotel plateau ==================
# The map was widened 8 columns to the east (logical x up to 71). Terrain is decided per CORNER
# (vertex): S = sand, W = shallow water, D = deep sea; each cell takes the Emerald shore piece that
# matches its 4 corners (the same pieces as the original Lilycove beach).
import math
SHORE = {'SSSS':0x124,'WWWW':0x19e,'DDDD':0x170,
         'WSSS':0x185,'SWSS':0x186,'SSWS':0x18d,'SSSW':0x18e,'WWWS':0x195,'WWSS':0x196,'WWSW':0x197,
         'WSWS':0x19d,'SWSW':0x19f,'WSWW':0x1a5,'SSWW':0x1a6,'SWWW':0x1a7,
         'DWWW':0x19b,'WDWW':0x19c,'WWWD':0x1a4,'DDDW':0x1ad,'DDWW':0x1ae,'DDWD':0x1af,'WDWD':0x1b7,
         'DWDD':0x1bd,'WWDD':0x1be,'WDDD':0x1bf}
SHORE_VAL = {}
for _y in range(0,40):                       # collision/elevation exactly as in the original map
    for _x in range(40,80):
        _v=o(_x,_y)
        SHORE_VAL.setdefault(_v&0x3ff,_v)
# clear the old Dept. Store and the motel: the plateau north of the beach is free for the hotel
fill(39, 2, 78, 11, GRASS); fill(41, 13, 78, 19, GRASS)
BX0, BX1, BY0, BY1 = 40, 78, 19, 40          # beach box (vertices); the boardwalk starts at row 40
def south(vx):                               # sand reaches this vertex row: a gentle, mostly horizontal shore
    if vx <= 44: return 40
    if vx <= 51: return 34 + 6 * (1 + math.cos(math.pi * (vx - 44) / 7)) / 2
    return 34 + 0.9 * math.sin(vx * 0.45) + 0.4 * math.sin(vx * 1.3)
def east(vy):                                # sand reaches this vertex column: rounded east end
    e = 68 + 0.8 * math.sin(vy * 0.5)
    if vy > 27: e -= ((vy - 27) / 7.0) ** 2 * 5
    return e
def is_sand(vx, vy):
    return vx <= east(vy) and vy <= south(vx)
sand_v = {(vx, vy): is_sand(vx, vy) for vx in range(BX0, BX1 + 1) for vy in range(BY0, BY1 + 1)}
def dist_to_sand(vx, vy):
    best = 9
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            if sand_v.get((vx + dx, vy + dy)): best = min(best, math.hypot(dx, dy))
    return best
def terrain(vx, vy):
    if sand_v.get((vx, vy)): return 'S'
    return 'W' if dist_to_sand(vx, vy) <= 3.1 else 'D'
TER = {(vx, vy): terrain(vx, vy) for vx in range(BX0, BX1 + 1) for vy in range(BY0, BY1 + 1)}
for _ in range(40):                          # no Emerald piece for some corner mixes: widen the shallow band there
    changed = False
    for y in range(BY0, BY1):
        for x in range(BX0 + 1, BX1):
            cs = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if ''.join(TER[c] for c in cs) not in SHORE:
                for c in cs:
                    if TER[c] == 'D': TER[c] = 'W'; changed = True
    if not changed: break
terrain = lambda vx, vy: TER[(vx, vy)]
missing = set()
for y in range(BY0, BY1):
    for x in range(BX0 + 1, BX1):
        k = terrain(x, y) + terrain(x + 1, y) + terrain(x, y + 1) + terrain(x + 1, y + 1)
        if k not in SHORE:
            missing.add((k, x, y)); k = 'WWWW' if 'S' not in k else ('SSSS' if k.count('S') >= 2 else 'WWWW')
        mt = SHORE[k]; put(x, y, SHORE_VAL.get(mt, T(mt)))
if missing: print('beach: combos without a piece:', sorted(missing))
# (sand runs straight into the plaza paving: no grass strip in between)

# --- hotel plateau to the north (future hotel): grass, cliff edge to the beach, forest behind
trees(52, -8, 72, 2, grass_above=False)
for y in range(2, 19): put(71, y, T(0x075, 1, 0))
for x in range(41, 71): put(x, 18, T(0x079, 1, 0))
fill(72, -8, 78, 19, DEEP)
# --- sand road: from the end of the north street down a stair in the cliff to the beach (west of the hotel)
fill(44, 11, 71, 13, GRASS)                                  # the north street now ends at x 43
trail(41, 13, 44, 18, 't')
put(41, 18, T(0x0af)); put(42, 18, T(0x0cf)); put(43, 18, T(0x0cf))   # 3-wide stair down the cliff

# --- HOTEL COVE LILY: fenced lot with the hotel building (sprite chunks, see hotel_art.py), a big pool,
# palms, trees, planters and flowers
HX0, HX1 = 45, 71                                             # lot x 45..70, rows -7..17 (fence included)
fill(45, -7, 71, 2, GRASS); trees(45, -12, 71, -7, grass_above=False)  # forest behind the hotel
for y in range(-7, 2): put(71, y, T(0x075, 1, 0))             # cliff on the east side, up to the new top
put(71, 18, ('ART', ('pcopy:07a', 0, 0, None, 'water'), 1, 0))   # corner where the east cliff meets the bottom one, over the sea
# metal fence all around the lot; the vertical runs sit exactly on the end posts of the horizontal ones
fence(HX0, HX1, -7); fence(HX0, HX1, 17)                      # top and bottom (end posts at x 45 and x 70)
for y in range(-6, 17):
    if y not in (11, 12): put(HX0, y, T(0x258, 1, 0))         # west side (post on the left), gate at rows 11..12
    put(HX1 - 1, y, T(0x25a, 1, 0))                           # east side (post on the right)
paving(44, 11, 49, 13)                                        # entrance through the gate, up to the deck
paving(49, 6, 65, 7); paving(49, 7, 68, 14)                   # hotel forecourt + pool deck (a clean rectangle)
art('hotel_pool', 50, 8, bottom='paving')                     # 16x5 pool
import port_art as _port_art
HOTEL_X, HOTEL_Y = 50, -6                                     # 14x12 building, bottom row 5
decor('hotel', HOTEL_X, HOTEL_Y, walk_rows=1, anchor_up=1)
HOTEL_DOORS = [(HOTEL_X + _port_art.HOTEL_DOOR_COL - 1, 5), (HOTEL_X + _port_art.HOTEL_DOOR_COL, 5)]
for (dx_, dy_) in HOTEL_DOORS: put(dx_, dy_, ('ART', ('nadoor', 0, 0, None, 'paving'), 0, 3))   # walk in -> warp
# vegetation: palm rows, shade trees, kerbed flowerbeds and potted palms on the pool deck
for (px_, py_) in ((49, 14), (53, 14), (57, 14), (61, 14), (65, 14)): palm(px_, py_, 'grass')   # palm row by the beach
for (px_, py_) in ((46, -6), (46, -2), (46, 2), (67, -6), (67, -2), (67, 2)): palm(px_, py_, 'grass')   # palms flanking the hotel
for (tx_, ty_) in ((48, -5), (48, -1), (64, -5), (64, -1), (46, 7)): tree1(tx_, ty_)
fill(71, -12, 72, -7, DEEP)                                   # sea next to the forest (NE corner)
for (fx0, fy0) in ((46, 14), (68, 14)): flowerbed(fx0, fy0, 2, 3) if False else None
for (px_, py_) in ((48, 7), (68, 7), (48, 13), (68, 13)): art('potted_palm', px_, py_, bottom='grass', walk_rows=1)   # on the lawn by the deck
flowerfield(46, 10, 48, 11, seed=21); flowerfield(68, 10, 70, 11, seed=22)
flowerfield(46, 13, 48, 14, seed=23); flowerfield(66, 13, 70, 14, seed=24) if False else None
for (fx_, fy_) in ((48, 5), (64, 5), (49, 4), (63, 4), (46, 16), (69, 16), (51, 16), (55, 16), (59, 16), (63, 16)): put(fx_, fy_, FLOWERS)
sign(48, 6)                                                   # HOTEL COVE LILY sign by the forecourt
# the south lawn: benches facing the pool, flowers
for bx_ in (51, 55, 59, 63): art('bench', bx_, 15, bottom='grass')   # benches between the palms, facing the pool
for (fx_, fy_) in ((47, 15), (47, 16), (68, 15), (68, 16), (53, 16), (61, 16)): put(fx_, fy_, FLOWERS)

# --- beach dressing: palms and small festival umbrellas (tileset), umbrella+chair sets (sprites)
for (px_, py_) in ((45, 20), (50, 19), (59, 20), (46, 31), (55, 28), (65, 20), (62, 27)): palm(px_, py_, 'sand')
decor('beach_set_red', 47, 22, walk_rows=1); decor('beach_set_blue', 53, 24, walk_rows=1)
decor('beach_set_red_l', 57, 21, walk_rows=1); decor('beach_set_red', 50, 29, walk_rows=1)
decor('beach_set_blue', 43, 35, walk_rows=1); decor('beach_set_blue', 64, 25, walk_rows=1)

# ================= DISTRICT 2 (north of the Contest Hall): the low-income quarter ======================
# Six Hoenn houses (Petalburg's, from the General tileset: no tiles; roof colours are palette swaps,
# as Slateport does), sand streets, a wooden fence around the quarter with a gate onto the main street.
fill(16, -11, 41, 11, GRASS)
trees(16, -12, 42, -11, grass_above=False)                   # the forest ends at row -12
HOUSE_MT = [[0x008, 0x009, 0x009, 0x009, 0x00a], [0x010, 0x011, 0x011, 0x011, 0x012],
            [0x018, 0x00b, 0x019, 0x00b, 0x01a], [0x020, 0x013, 0x021, 0x013, 0x022]]
def hoenn_house(x, y, slot, wall=5):
    """5 x 4 Hoenn house, door at (x+2, y+3); slot = roof palette (1 = Petalburg red),
    wall = wall palette (5 = the original orange wood)"""
    for j, row in enumerate(HOUSE_MT):
        for i, m in enumerate(row):
            if m == 0x021: put(x + i, y + j, T(m, 0, 3)); continue                   # the door
            roof = slot if j < 3 else 1
            if roof == 1 and wall == 5: put(x + i, y + j, T(m, 1, 0)); continue
            put(x + i, y + j, ('ART', ('remap:%03x:%d:%d' % (m, roof, wall), 0, 0, None, 'water'), 1, 0))
B2 = {}
def b2_sand(x0, y0, x1, y1):
    for y in range(y0, y1):
        for x in range(x0, x1): B2[(x, y)] = True
# a natural layout: houses at staggered heights and offsets, short sand paths from each door to the
# vertical street, trees and flowers in the gaps; a fruit stall on a little square at the top
# (the whole quarter sits 2 rows higher than the gate row, clear of the Contest Hall's towers)
b2_sand(30, -6, 32, 11)                                       # vertical street, through the gate to the main street
b2_sand(26, -6, 36, -4)                                       # the square in front of the stall
b2_sand(20, 1, 37, 2); b2_sand(20, -1, 21, 1)                 # upper path (and a spur to the north-west house)
b2_sand(19, 7, 37, 8); b2_sand(19, 6, 20, 7)                  # lower path (and a spur to the west house)
DISTRICT2 = [  # (x, y, roof palette, wall palette, interior) -- door at (x+2, y+3); palette 7 = dark-brown roofs
    (23, 3, 7, 5, 'HOUSE4'),                                  # the protagonist's house (orange wood), by the gate
    (17, 2, 7, 70, 'HOUSE1'),                                 # pink (palette 7 copy of the wall tiles, wine outline)
    (24, -3, 7, 8, 'HOUSE2'),                                 # pale yellow
    (18, -5, 7, 7, None),                                     # weathered brown wood
    (33, 3, 7, 1, 'MOVE_DELETERS_HOUSE'),                     # barn red
    (34, -3, 7, 0, 'POKEMON_TRAINER_FAN_CLUB'),               # faded blue
]
for (_x, _y, _s, _wl, _w) in DISTRICT2:
    hoenn_house(_x, _y, _s, _wl)
    if not _w: put(_x + 2, _y + 3, T(0x021, 1, 0))            # this house has no interior
art('stall', 29, -8, bottom='grass')                          # fruit stall (2 x 3), facing the square
for (tx_, ty_) in ((17, -8), (21, -8), (37, -8), (39, -8), (38, 2), (17, -1), (28, 3), (38, 7)):
    tree1(tx_, ty_)
def _free(x, y):
    v = M[y + OY][x + OX]
    return (x, y) not in B2 and isinstance(v, int) and (v & 0x3ff) in (0x001, 0x002)
for (fx_, fy_) in ((23, -4), (23, -5), (29, -2), (29, -1), (22, 2), (17, 6), (18, 6), (22, 6), (28, 6), (33, -1), (32, 0),
                   (39, 1), (36, 2), (33, 2), (39, 6), (27, -7), (28, -7), (33, -7), (36, -7), (17, -4), (21, -6),
                   (18, 9), (23, 9), (26, 8), (27, 9), (33, 9), (35, 8), (39, 9)):
    if _free(fx_, fy_): put(fx_, fy_, FLOWERS)
# forests around the quarter, redrawn with their 2-column tree pairs aligned (no half trees)
# The whole northern forest, redrawn as one pattern: tree pairs start on even columns and every block's
# trunk row is on an odd row, so neighbouring blocks line up (no half trees, no mismatched rows).
fill(-14, -8, -13, 2, GRASS)                                  # a grass column between the west forest and the museum
trees(-16, -12, -14, 2, grass_above=False)                    # west edge, down to row 1
paving(-14, -8, -13, -1)                                      # ...paved beside the museum
trees(-14, -12, 0, -8, grass_above=False)                     # above the museum (trunks on row -9)
trees(0, -12, 16, 0, grass_above=False)                       # west of district 2, above district 1 (trunks on row -1)
trees(16, -12, 42, -8, grass_above=False)                     # north of district 2 (trunks on row -9)
fill(41, -8, 45, 11, GRASS); trees(42, -12, 44, 2, grass_above=False)   # strip between district 2 and the hotel (whole trees only)
fill(44, -8, 71, -7, GRASS); fill(70, -12, 71, -8, GRASS)      # (the hotel's forest ends on row -9; grass by the sea)
trees(44, -12, 70, -8, grass_above=False)                     # behind the hotel (trunks on row -9)
# (no fence: the quarter opens onto the forest and the main street)
# sand autotile: a grass edge on each side that touches grass
for (x, y) in B2:
    def _g(xx, yy):
        v = M[yy + OY][xx + OX]
        return (xx, yy) not in B2 and isinstance(v, int) and (v & 0x3ff) in (0x001, 0x002, 0x004)
    put(x, y, T(SAND.get((int(_g(x, y - 1)), int(_g(x, y + 1)), int(_g(x - 1, y)), int(_g(x + 1, y))), 0x121)))

# ================= CONTEST HALL (hall3_art.py: 3D model in Emerald's 3/4 projection) ===================
# 27 x 11 metatiles over the whole block (x 14..40, rows 11..21): background palace, roofs and towers
# (rows 11..12 hang over the north street, walk behind) + 9 sprites: the striped dome on its drum
# (4 chunks), the entrance portico (glass doors at x 26..28, row 21) and the four tower domes.
art('hall_top', 14, 11, bottom='paving', walk_rows=2)
art('hall_body', 14, 13, bottom='paving')
paving(14, 22, 41, 23)                                       # forecourt in front of the hall
import hall3_art as _H3
for (_n, (_x0, _x1, _y0, _y1), _up, _sp) in _H3.GROUPS:
    _top = 11 + _y0 // 16
    decor(_n, 14 + _x0 // 16, _top, walk_rows=max(0, 13 - _top), anchor_up=_up)
import port_art as _pa3                                      # row 21: walkable where only the wall's foot line shows
_hb_c = _pa3._CANVAS['hall_body']
for x in range(14, 41):
    if 25 <= x <= 29: continue                                # portico
    cells = [_hb_c[yy][(x - 14) * 16 + xx] for yy in range(130, 144) for xx in range(16)]
    if not any(cells):
        v = M[21 + OY][x + OX]; M[21 + OY][x + OX] = (v[0], v[1], 0, 3) if isinstance(v, tuple) else v
for x in (26, 27, 28):                                       # the glass double door (walk in -> lobby)
    put(x, 21, ('ART', ('nadoor', 0, 0, None, 'carpet'), 0, 3))
    for y in (22, 23): put(x, y, T(F['carpet']))             # red carpet from the door to the plaza bricks
# forecourt: potted palms by the building, modern benches facing the plaza
for px_ in (16, 24, 30, 38): art('potted_palm', px_, 22, bottom='paving', walk_rows=1)
for bx_ in (18, 21, 32, 35): art('bench', bx_, 23, bottom='paving')
sign(44, 10)                                                 # beach / hotel sign at the top of the sand road

# ================= soft grass fringe wherever plain paving meets grass ==================================
def _grassy(v):
    if isinstance(v, int): return (v & 0x3ff) in (0x001, 0x002, 0x004)
    return isinstance(v, tuple) and v[0] == 'ART' and v[1][4] == 'grass'
_PAVE = ('paving', 0, 0, None, 'water')
# potted palms on the paving that touch grass stand on grass instead (the paving around them then
# gets the fringe like any other paving cell at the lawn's edge)
for Y in range(1, H - 1):
    for X in range(1, W - 1):
        v = M[Y][X]
        if isinstance(v, tuple) and v[0] == 'ART' and v[1][0] == 'potted_palm' and v[1][4] == 'paving':
            col = X  # the pot (bottom row) and its head share the decision
            cells = [(X, Y), (X, Y + 1) if isinstance(M[Y + 1][X], tuple) and M[Y + 1][X][1][0] == 'potted_palm' else (X, Y - 1)]
            if any(_grassy(M[cy + dy][cx + dx]) for (cx, cy) in cells for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                for (cx, cy) in cells:
                    w = M[cy][cx]
                    if isinstance(w, tuple) and w[1][0] == 'potted_palm':
                        M[cy][cx] = (w[0], w[1][:4] + ('grass',), w[2], w[3])
_new = {}
for Y in range(1, H - 1):
    for X in range(1, W - 1):
        v = M[Y][X]
        if not (isinstance(v, tuple) and v[1] == _PAVE): continue
        if 14 <= X - OX <= 40 and 23 <= Y - OY <= 39: continue                  # the plaza keeps clean kerbs
        n, s, w, e = (_grassy(M[Y - 1][X]), _grassy(M[Y + 1][X]), _grassy(M[Y][X - 1]), _grassy(M[Y][X + 1]))
        bits = ''.join(ch for ch, f in (('N', n), ('S', s), ('W', w), ('E', e)) if f)
        for ch, (dx, dy), (o1, o2) in (('a', (-1, -1), (n, w)), ('b', (1, -1), (n, e)), ('c', (-1, 1), (s, w)), ('d', (1, 1), (s, e))):
            if not o1 and not o2 and _grassy(M[Y + dy][X + dx]): bits += ch
        if bits:
            name = ('fringeP_' if X - OX <= -9 and 3 <= Y - OY <= 25 else 'fringe_') + bits   # strip seen from Route 121 (x <= -9, rows 3..25): primary
            _new[(X, Y)] = ('ART', (_pa3.fringe_art(name, bits), 0, 0, None, 'paving'), v[2], v[3])
for (X, Y), v in _new.items(): M[Y][X] = v
