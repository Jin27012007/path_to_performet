from compose import *
fill(-OX,0,W-OX,H,GRASS)
# ================= sea =================
fill(52,0,W,H,DEEP); fill(0,42,W,H,DEEP)
# ================= borders =================
trees(0,0,52,2,grass_above=False)
trees(0,2,2,20,grass_above=False)
trees(0,24,2,40)
# ================= NORTH BAND (y2-10) =================
museum(2,2)                                  # stairs bottom at (6..9,10)
for cx in (0,1,9,10,11,12): put(2+cx,2,GRASS)
path(6,10,10,11)
house(17,2); house(23,2); house(29,2)        # doors (18,5) (24,5) (30,5)
path(15,6,37,7)
house(17,7); fanclub(23,7)                   # doors (18,10) (25,10)
flowers(29,7,36,8); tree1(30,7); tree1(33,7); put(29,9,FLOWERS); put(35,9,FLOWERS)
path(15,2,16,11); path(36,2,38,11)
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
art('cruise',18,57)   # moored along the landing platform

# fishermen's pier with two finger docks and moored boats
pier(FISH_PIER,44,53)
deck(FISH_PIER+3,13,47,48); deck(FISH_PIER+3,13,51,52)
deck(1,10,53,55,joins_top=(FISH_PIER,FISH_PIER+1,FISH_PIER+2))
art('boat_side',9,48); art('boat_side_l',0,47); art('boat_side',13,50); art('boat_front',1,50)
# market tents along the boardwalk (Slateport-style), with goods around them
art('tent_green',8,40,bottom='dock',walk_rows=2); art('tent_pots',14,40,bottom='dock',walk_rows=2)
art('tent_flowers',32,40,bottom='dock',walk_rows=2); art('tent_green',38,40,bottom='dock',walk_rows=2)
for (n,x,y) in [('basket_orange',13,42),('crate_label',19,41),('basket_green',31,42),('basket_orange',7,42)]:
    art(n,x,y,bottom='dock')
# crates and mooring posts (the father waits next to the crates)
for (x,y) in [(30,42),(30,41),(2,41),(22,41),(37,42),(43,41)]: put(x,y,D('dock_crate',False))
for (x,y) in [(21,43),(33,43),(46,43),(19,56),(31,56)]: put(x,y,D('dock_bollard',False))
# fishing boats around the bay and at the beach
art('boat_side',15,52); art('boat_side_l',35,56); art('boat_front',44,48); art('boat_side',47,54)
art('boat_side_l',56,45); art('boat_front',58,52); art('boat_side',55,37)
art('boat_side_l',49,32,bottom='shallow'); art('boat_front',49,35,bottom='shallow')

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

# ================= RESIDENTIAL DISTRICT 1 (west): uphill street from the pier to Route 121 =========
# logical x -10..13 (the map was widened 10 columns to the west for it)
STREET = (-2, 1)                       # street columns -2..0, stone paving, from the boardwalk up to row 11
def sand_trail(x0,y0,x1,y1):           # light dirt trail (Emerald sand path) linking a door to the street
    for y in range(y0,y1):
        for x in range(x0,x1): put(x,y,T(0x121))
def house_sign(x,y): sign(x,y)
fill(-10,2,14,40,GRASS)                 # clear the old west part (PC, House 3, trees...)
trees(-10,0,2,10,grass_above=False)     # forest west of the museum, above the Route 121 connection
museum(2,2); path(6,10,10,11)           # (redrawn: the clear above wiped its lower rows)
for cx in (0,1,9,10,11,12): put(2+cx,2,GRASS)
paving(-10,11,14,13)                    # north street, west part, open to Route 121 (rows 10..13)
paving(STREET[0],13,STREET[1],40)       # the uphill residential street
paving(STREET[0],20,14,23)              # avenue to the plaza
# --- west houses, bottom to top: H1, H2 | terrain step with stairs | H3, H4, H5 (upper level)
# The strip x -10..-2, rows 5..24 is what Route 121 shows across the connection (drawn with the
# shared Lilycove tileset), so it only uses original/shared pieces: classic houses there.
fill(-10,5,-3,11,GRASS)                                              # clearing in the forest for H5
house(-8,6);              house_sign(-4,9)                           # H5 classic, door (-7,9) onto the north street
fanclub(-8,13);           sand_trail(-6,17,-2,18); house_sign(-8,17) # H4 "Edificio Lilas" (classic apartments), door (-6,16)
house(-8,19);             sand_trail(-7,23,-2,24); house_sign(-8,23) # H3 classic, door (-7,22)
for x in range(-10,-2): put(x,24,T(0x07c,1,0))                       # low cliff: the terrain step
for y in (24,25): put(-2,y,T(0x0af)); put(-1,y,T(0x0cf)); put(0,y,T(0x07c,1,0))   # stairs on the street
art('apartments',-9,26);  sand_trail(-6,31,-2,32); house_sign(-8,31) # H2 modern apartments, door (-6,30)
art('house_grey',-9,32);  sand_trail(-7,37,-2,38); house_sign(-8,37) # H1 modern grey, door (-7,36)
fence(-10,-8,38); fence(-6,-3,38)
for (fx,fy) in ((-10,23),(-10,31),(-3,19),(-3,20),(-3,21),(-3,13),(-3,14),(-3,15),(-10,16),(-10,15),(-10,39),(-9,39),(-7,39),(-6,39),(-5,39),(-4,39),(-2,26) if False else (-3,26),(-3,27)):
    put(fx,fy,FLOWERS)
# --- the L: three houses along the north street (doors face the avenue)
house(1,14); sand_trail(2,18,3,20); house_sign(0,17)                                  # L1 classic = House 3, door (2,17)
art('house_beige',5,13); sand_trail(7,18,8,20); house_sign(4,17)                      # L2 modern beige, door (7,17)
art('house_grey',10,13); sand_trail(12,18,13,20); house_sign(15,17)                   # L3 modern grey, door (12,17)
for (fx0,fx1) in ((3,6),(9,11)): fence(fx0,fx1,18) if False else None
# --- east of the street (lower level): hedge of trees hides the level change, harbor, Pokémon Center
fill(1,23,14,26,GRASS)
for x in range(3,14): put(x,25,T(0x07c,1,0))                 # low ledge under the avenue level
tree1(1,23); tree1(1,26); trees(1,29,3,32)
harbor(4,26)                                                  # door (7,31)
brickfill(3,32,14,40); pc(10,32)                              # Pokémon Center next to the port, door (11,35)
for x in (4,8): lamp2(x,33,'brick')
palm(1,36,'grass') if False else None
palm(3,36,'brick'); palm(7,36,'brick')
bunting(-2,14,21)                                             # avenue bunting (west part)
for x in (-3,1): lamp2(x,13) if False else None
sign(-10,14); sign(3,31); sign(10,10)                                     # city sign at the Route 121 entrance, harbor sign
