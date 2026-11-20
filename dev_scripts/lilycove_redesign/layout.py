from compose import *
fill(0,0,W,H,GRASS)
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
# ================= PLAZA (y23-35) =================
brickfill(14,23,41,36)
for gx in (15,31):
    fill(gx,25,gx+9,34,GRASS)
    flowers(gx,25,gx+9,26); flowers(gx,33,gx+9,34)
    flowers(gx,26,gx+1,33); flowers(gx+8,26,gx+9,33)
    pond(gx+3,28)
    lamp(gx+2,27); lamp(gx+6,27); lamp(gx+2,31); lamp(gx+6,31)
# central axis: avenue of lamps & flower pots towards pier
for y in (25,33): lamp(25,y); lamp(29,y)
lamp(24,29); lamp(30,29)
# ================= HARBOR (left) =================
harbor(4,26)                                 # door (7,31)
brickfill(2,32,14,36)
tree1(2,23) if False else None
trees(11,24,13,31)
flowers(2,24,4,31)
# ================= PROMENADE + SEAWALL =================
brickfill(2,36,42,40)
for x in range(2,42): put(x,40,T(0x07c,1,0)); put(x,41,T(0x189,0,1))
# piers
def pier(px,py0,py1,dx0,dx1):
    for y in range(py0,py1): put(px,y,T(0x0f4,0,3))
    for x in range(dx0,dx1): put(x,py1,T(0x0f1,0,3)); put(x,py1+1,T(0x0f5,1,0))
pier(27,40,46,21,34)
pier(7,40,44,4,11)
# ================= BEACH (right) =================
SX0,SX1,SY0,SY1=42,49,19,39   # sand area
fill(42,19,52,42,SHALLOW)
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
for y in range(19,42): put(52,y,T(0x1b7,0,1))
for x in range(42,52): put(x,42,T(0x1be,0,1))
put(52,42,T(0x1bf,0,1)); put(41,42,T(0x1bd,0,1))
# bottom-left corner tidy
trees(0,24,2,40); 
for x in range(0,2): put(x,40,T(0x07c,1,0)); put(x,41,T(0x189,0,1))
# Aqua cave islet (keeps original warp target)
stamp(66,0,76,8,54,0)
for yy in range(4,8): put(54,yy,SHALLOW)

# promenade planters (avoid pier axes x=7, x=27)
for x in (3,15,23,31): put(x,37,T(0x005,1,0))
# central fountain on main axis
pond(26,29)
# sign posts for bg_events
for sx,sy in [(10,10),(47,9),(2,19),(31,19),(40,17),(3,31),(22,10),(16,5)]: sign(sx,sy)

# ================= FESTIVAL DRESSING (World Contest Season) =================
carpet(27,20,29)                                   # red carpet hall -> fountain
for bx,blue in ((23,False),(31,True)): banner(bx,17,'grass',blue)
for bx,by,blue in ((14,24,True),(40,24,False),(14,34,False),(40,34,True)): banner(bx,by,'brick',blue)
bunting(2,46,21)                                   # across the avenue
bunting(15,40,24)                                  # plaza north edge
bunting(2,42,38)                                   # promenade
bunting(16,38,11)                                  # north street
# palms along the promenade
for px_ in (10,18,35,38): palm(px_,35,'brick')
# beach: umbrellas + palms
umbrella(44,22); umbrella(46,28,True); umbrella(43,33)
palm(43,25); palm(46,33)
