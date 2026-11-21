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
contest(24,13)                               # door (27,19)
flowers(16,14,23,15); flowers(32,14,39,15)
tree1(17,15); tree1(20,15); tree1(33,15); tree1(36,15)
lamp(22,18); lamp(32,18); lamp(23,15); lamp(31,15)

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
for sx,sy in [(10,10),(47,9),(2,19),(31,19),(40,17),(3,31),(22,10),(16,5)]: sign(sx,sy)

# ================= FESTIVAL DRESSING (World Contest Season) =================
for bx,blue in ((23,False),(31,True)): banner(bx,17,'grass',blue)
bunting(2,46,21)                                   # across the avenue
bunting(2,14,38)                                   # promenade (west part)
bunting(16,38,11)                                  # north street
# palms along the promenade
for px_ in (2,10): palm(px_,36,'brick')   # promenade palms, outside the plaza
# beach: umbrellas + palms
umbrella(44,22); umbrella(46,28,True); umbrella(43,33)
palm(43,25); palm(46,33)

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
art('tent_green',8,40,bottom='dock',walk_rows=2); art('tent_pots',14,40,bottom='dock',walk_rows=2)
art('tent_flowers',32,40,bottom='dock',walk_rows=2); art('tent_green',38,40,bottom='dock',walk_rows=2)
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
trees(-16,-8,-13,1,grass_above=False); trees(-1,-8,17,0,grass_above=False)   # forest around the museum
museum(-13,-8)                                                     # museum on the hill, doors (-8,-3) (-7,-3), stairs x -9..-6 row 0
for cx in (0,1,9,10,11,12): put(-13+cx,-8,T(0x1e4 if cx%2==0 else 0x1e5,1,0) if False else GRASS)
paving(-10,1,-4,3)                                                 # museum forecourt
paving(STREET[0],1,STREET[1],40)                                   # the uphill residential street
paving(-16,11,15,13)                                               # north street (open to Route 121, rows 10..12)
paving(STREET[0],20,14,23)                                         # avenue to the plaza

# --- upper line (row of H5): H5 west of the street, the L houses east of it; back gardens above
# x -16..-9, rows 3..25 is what Route 121 shows across the connection (drawn with the shared Lilycove
# tileset), so that strip only uses original/shared pieces: classic houses, fences and the generic
# pieces of the primary tileset (flowers, lamps, paving).
house(-14,5); trail(-14,9,-11,11,'b',(-13,)); house_sign(-10,8)            # H5 classic, door (-13,8)
garden(-16,1,-10,5,11,shared=False); fence(-16,-14,10); fence(-11,-9,10)
tree1(-16,6) if False else None
house(-4,5);  trail(-4,9,-1,11,'b',(-3,)); house_sign(-5,8)               # L1 classic = House 3, door (-3,8)
art('house_beige_lilac',2,4); trail(3,9,6,11,'b',(4,)); house_sign(1,8)         # L2 modern beige, door (4,8)
art('house_grey',9,4);  trail(10,9,13,11,'b',(11,)); house_sign(8,8)      # L3 modern grey, door (11,8)
garden(-4,1,15,4,12); tree1(-1,1); tree1(6,1); tree1(13,1)                 # back gardens with small trees
garden(0,4,2,9,13); garden(7,4,9,9,14); garden(14,4,15,9,15)               # side yards with flowers
fence(-1,1,10) if False else None
for (fx0,fx1) in ((0,3),(6,10),(13,15)): fence(fx0,fx1,10)                  # low front fences
fence(-5,-4,10) if False else None

# --- west lot, below the north street: H4, H3 | terrain step | H2, H1
fanclub(-15,13); trail(-14,17,-8,19,'r',(-13,)); house_sign(-10,16)        # H4 "Edificio Lilas", door (-13,16)
garden(-16,13,-15,17,21,shared=False); garden(-10,13,-8,16,22,shared=False)
fence(-16,-9,19)                                                            # lot boundary
house(-14,20); trail(-14,24,-8,26,'r',(-13,)); house_sign(-10,23)          # H3 classic, door (-13,23)
garden(-16,20,-14,24,23,shared=False); garden(-10,20,-8,23,24,shared=False)
ledge(-16,-8,26); stairs3(STREET[0],26,28)                                  # terrain step + 3-wide stairs
art('apartments',-16,28); trail(-14,33,-8,35,'r',(-13,)); house_sign(-9,32)  # H2 modern apartments, door (-13,32)
garden(-16,27,-8,28,25); garden(-9,28,-8,32,26)
art('house_grey_coral',-15,35); house_sign(-10,38)                               # H1 modern grey, door (-13,39) onto the boardwalk
garden(-16,35,-15,40,27); garden(-10,35,-8,38,28); fence(-10,-8,39) if False else None
# --- east of the street: the old L lot becomes a small neighbourhood garden
garden(-5,13,14,20,31,skip={(x,y) for x in range(-5,-3) for y in range(13,20)})
for (tx,ty) in ((0,13),(5,15),(10,13)): tree1(tx,ty)
garden(-5,23,14,26,32)                                                       # upper level, above the step
ledge(-5,14,26)                                                             # the step continues east of the street
# --- seaside café (replaces the Pokémon Center and the harbor building) on the lower level
fill(-5,27,14,40,GRASS)
deck(-3,14,27,34,posts_below=False)                                         # wooden terrace x -3..13, rows 27..33
art('cafe',2,27,bottom='dock')                                              # Café Litoral, door (4,30)
art('tent_pots',9,27,bottom='dock',walk_rows=2)                             # juice kiosk
art('umbrella_red',-2,27,bottom='dock',walk_rows=1); art('cafe_table',-3,30,bottom='dock')
art('umbrella_blue',0,30,bottom='dock',walk_rows=1)
art('umbrella_red',10,30,bottom='dock',walk_rows=1); art('cafe_table',7,32,bottom='dock')
for x in range(-3,14):                                                      # low wooden fence, entrance at x 3..5
    if not 3<=x<=5: art('fence_wood',x,33,bottom='dock')
for (fx,fy) in ((-5,28),(-4,28),(-4,32)): put(fx,fy,FLOWERS)
palm(-5,31,'grass') if False else None
paving(-5,34,14,36)                                                         # promenade: street -> plaza
brickfill(-5,36,14,40)                                                      # brick by the boardwalk
art('tent_flowers',-4,37,bottom='brick',walk_rows=2)                        # flower stall
palm(3,37,'brick'); palm(9,37,'brick')
lamp2(12,36,'brick',facing='left')
# --- street lamps along the residential street (east kerb, heads towards the street) and the north street
for y in (5,16,30): lamp2(-5,y,'grass',facing='left')
lamp2(-5,37,'brick',facing='left')
for x in (-1,6,13): lamp2(x,10,'paving') if False else None
bunting(-8,14,21)                                                           # avenue bunting (west part)
sign(-16,13); sign(-4,2)                                                    # city sign, museum sign
for (sx,sy) in ((8,8),(1,8),(-5,8),(-10,8),(16,5)): sign(sx,sy)               # house signs over the gardens
