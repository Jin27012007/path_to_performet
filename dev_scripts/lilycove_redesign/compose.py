import struct, sys
import os
REPO=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))+'/'
ORIG=open(os.path.join(os.path.dirname(__file__),'lilycove_original.bin'),'rb').read()
OW=80
def o(x,y): return struct.unpack_from('<H',ORIG,(y*OW+x)*2)[0]
OX=16            # the map was widened 16 columns to the west; layout coords are logical (x may be negative)
OY=8             # ...and 8 rows to the north (y may be negative)
W,H=80,70
M=[[0]*W for _ in range(H)]
def T(i,col=0,el=3): return i|(col<<10)|(el<<12)
GRASS=T(0x001); GRASS2=T(0x002); FLOWERS=T(0x004); 
DEEP=T(0x170,0,1); SHALLOW=T(0x19e)
COB=T(0x233); COBT=T(0x22b); COBB=T(0x23b)
SAND=T(0x124)
def put(x,y,v):
    x+=OX; y+=OY
    if 0<=x<W and 0<=y<H: M[y][x]=v
def fill(x0,y0,x1,y1,v):
    for y in range(y0,y1):
        for x in range(x0,x1): put(x,y,v)
def norm(v):
    # flatten upper-town elevation 5 to 3
    if (v>>12)==5: v=(v&0x0fff)|(3<<12)
    return v
def stamp(sx0,sy0,sx1,sy1,dx,dy,skip=None):
    for y in range(sy0,sy1):
        for x in range(sx0,sx1):
            v=norm(o(x,y))
            if skip and skip(v&0x3ff): continue
            put(dx+x-sx0,dy+y-sy0,v)
def grid(rows,dx,dy):
    for j,r in enumerate(rows):
        for i,v in enumerate(r):
            if v is not None: put(dx+i,dy+j,v)
def trees(x0,y0,x1,y1,grass_above=True):
    h=y1-y0
    for j in range(h):
        y=y0+j; fromb=h-1-j
        if fromb==0: a,b=0x1e4,0x1e5
        elif j==0 and grass_above: a,b=0x1ce,0x1cf
        elif fromb%2==1: a,b=0x1d4,0x1d5
        else: a,b=0x1dc,0x1dd
        for x in range(x0,x1):
            l=(x-x0)%2==0
            t=a if l else b
            walk = t in (0x1ce,0x1cf)
            put(x,y,T(t,0,3) if walk else T(t,1,0 if fromb==0 else 1))
def tree1(x,y):  # single 2x2 tree with canopy top on grass
    put(x,y,T(0x1ce)); put(x+1,y,T(0x1cf))
    put(x,y+1,T(0x1d6,1,1)); put(x+1,y+1,T(0x1d7,1,1))
    put(x,y+2,T(0x1e6,1,0)); put(x+1,y+2,T(0x1e7,1,0))
def fence(x0,x1,y):
    for x in range(x0,x1): put(x,y,T(0x251,1,0))
    put(x0,y,T(0x250,1,0)); put(x1-1,y,T(0x252,1,0))
def path(x0,y0,x1,y1):
    fill(x0,y0,x1,y1,COB)
def flowers(x0,y0,x1,y1): fill(x0,y0,x1,y1,FLOWERS)
def lamp(x,y): put(x,y,T(0x29a,1,0))
def sign(x,y): put(x,y,T(0x003,1,0))
def pond(x,y):  # 3x2 fountain basin
    for j,r in enumerate([[0xc8,0xc9,0xca],[0xd8,0xd9,0xda]]):
        for i,t in enumerate(r): put(x+i,y+j,T(t,1,0))
def house(x,y):  stamp(35,3,39,7,x,y)          # door at (x+1,y+3)
def pc(x,y):
    for j,r in enumerate([[0x48,0x49,0x4a,0x4b],[0x50,0x51,0x52,0x53],[0x58,0x59,0x5a,0x5b],[0x60,0x61,0x62,0x63]]):
        for i,t in enumerate(r): put(x+i,y+j,T(t,1,0))
    put(x+1,y+3,T(0x061,0,0))                  # door tile walkable
def museum(x,y): stamp(6,0,19,8,x,y); stamp(10,8,14,9,x+4,y+8)
def dept(x,y):   stamp(23,0,32,7,x,y)          # door (x+4,y+6)
def contest(x,y):stamp(20,18,27,25,x,y)        # door (x+3,y+6)
def motel(x,y):  stamp(36,20,42,25,x,y)        # door (x+1,y+4)
def fanclub(x,y):stamp(37,11,42,15,x,y)        # door (x+2,y+3)
def harbor(x,y): stamp(9,27,16,33,x,y)         # door (x+3,y+5)
# ---------------- festival tiles (see festival_tiles.py) ----------------
import json as _json
F=_json.load(open(os.path.join(os.path.dirname(__file__),'festival_ids.json')))
def fobj(name,x,y,w,h,walk_rows=1):
    for j in range(h):
        for i in range(w):
            m=F['%s_%d_%d'%(name,i,j)]
            put(x+i,y+j,T(m,0,3) if j<walk_rows else T(m,1,0))
def umbrella(x,y,blue=False): fobj('umbrella_sand',x,y,2,2)
def palm(x,y,under='sand'): fobj('palm_'+under,x,y,2,3)
def banner(x,y,under='brick',blue=False): fobj('banner_%s'%under,x,y,1,2)
def brickfill(x0,y0,x1,y1): fill(x0,y0,x1,y1,T(F['brick']))
def carpet(x,y0,y1):
    for y in range(y0,y1): put(x,y,T(F['carpet']))
def bunting(x0,x1,y,under='cobble'):
    for x in range(x0,x1):
        cur=M[y+OY][x+OX]&0x3ff if isinstance(M[y+OY][x+OX],int) else -1
        if cur==F['brick']: u='brick'
        elif cur in (0x233,0x22b,0x23b): u='cobble'
        elif cur in (0x001,0x002): u='grass'
        elif cur in (0x121,0x124): u='sand'
        else: continue
        put(x,y,T(F['bunting_%s'%u]))

# ---------------- port art (resolved by build_city_tileset.py) ----------------
import port_art as _pa
_ART_SIZE={}
def art(name,x,y,pal=None,bottom='water',walk_rows=0):
    if name not in _ART_SIZE:
        c=_pa.ART[name](); _ART_SIZE[name]=(len(c[0])//16,len(c)//16)
    w,h=_ART_SIZE[name]
    for my in range(h):
        for mx in range(w):
            walk = my<walk_rows
            put(x+mx,y+my,('ART',(name,mx,my,pal,bottom),0 if walk else 1,3 if walk else 0))

def paving(x0,y0,x1,y1):
    for y in range(y0,y1):
        for x in range(x0,x1): put(x,y,T(F['paving']))
CURB={'tl':0x3d,'t':0x3e,'tr':0x3f,'l':0x45,'c':0x46,'r':0x47,'bl':0x4d,'b':0x4e,'br':0x4f}
def flowerbed(x0,y0,w,h):
    """Emerald white stone kerb with red flowers inside (solid)."""
    for j in range(h):
        for i in range(w):
            t = j==0; b = j==h-1; l = i==0; r = i==w-1
            if t: k='tl' if l else ('tr' if r else 't')
            elif b: k='bl' if l else ('br' if r else 'b')
            else: k='l' if l else ('r' if r else None)
            put(x0+i,y0+j,T(CURB[k],1,0) if k else T(0x004,1,0))

def lamp2(x,y,under='paving',facing='right'):   # modern lamp: head at row y-1 (walk behind it), pole at row y
    art('lamp_modern' if facing=='right' else 'lamp_modern_l',x,y-1,bottom=under,walk_rows=1)
def bunting2(x0,x1,y,under='paving'):
    for x in range(x0,x1):
        art('bunting',x,y,bottom=under,walk_rows=1)
def string_lights(xa,xb,y,under='paving'):
    """two lamp posts with bunting strung between them"""
    lamp2(xa,y,under); lamp2(xb,y,under); bunting2(xa+1,xb,y,under)

import random as _random
FLOWER_KINDS = ['flower_yellow','flower_white','flower_blue','flower_red','flower_orange']
def flowerfield(x0,y0,x1,y1,seed=1,skip=()):
    rnd=_random.Random(seed)
    for y in range(y0,y1):
        for x in range(x0,x1):
            if (x,y) in skip: continue
            k=rnd.random()
            if k<0.18: put(x,y,FLOWERS)                       # original red/peach flowers
            else: art(FLOWER_KINDS[int((k-0.18)/0.82*5)%5],x,y,bottom='grass',walk_rows=1)
