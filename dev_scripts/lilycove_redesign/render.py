import sys, struct
from PIL import Image
import os
R=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','data','tilesets'))+'/'
def pal(path):
    L=open(path).read().split('\n')[3:19]
    return [tuple(int(x) for x in l.split()) for l in L if l.strip()]
def load(ts):
    im=Image.open(R+ts+'/tiles.png'); w=im.width//8; h=im.height//8
    px=im.load(); tiles=[]
    for ty in range(h):
        for tx in range(w):
            tiles.append([[px[tx*8+x,ty*8+y]&15 for x in range(8)] for y in range(8)])
    mt=open(R+ts+'/metatiles.bin','rb').read()
    mts=[struct.unpack('<8H',mt[i:i+16]) for i in range(0,len(mt),16)]
    pals=[pal(R+ts+'/palettes/%02d.pal'%i) for i in range(16)]
    return tiles,mts
def build(prim,sec):
    pt,pm=load(prim); st,sm=load(sec)
    pals=[pal(R+prim+'/palettes/%02d.pal'%i) for i in range(6)]+[pal(R+sec+'/palettes/%02d.pal'%i) for i in range(6,13)]
    tiles=pt+[None]*(512-len(pt))+st
    mts=pm+[(0,)*8]*(512-len(pm))+sm
    cache={}
    def mimg(m):
        if m in cache: return cache[m]
        img=Image.new('RGB',(16,16),(255,0,255)); p=img.load()
        e=mts[m] if m<len(mts) else (0,)*8
        for layer in range(2):
            for q in range(4):
                v=e[layer*4+q]; ti=v&0x3ff; hf=v>>10&1; vf=v>>11&1; pl=v>>12
                if ti>=len(tiles) or tiles[ti] is None: continue
                t=tiles[ti]; ox=(q%2)*8; oy=(q//2)*8
                for y in range(8):
                    for x in range(8):
                        c=t[7-y if vf else y][7-x if hf else x]
                        if layer==1 and c==0: continue
                        if pl<len(pals) and c<len(pals[pl]): p[ox+x,oy+y]=pals[pl][c]
        cache[m]=img; return img
    return mimg,mts
def render(mapbin,w,out,prim='primary/general',sec='secondary/lilycove',grid=False):
    from PIL import ImageDraw
    mimg,_=build(prim,sec)
    d=open(mapbin,'rb').read(); n=len(d)//2; h=n//w
    img=Image.new('RGB',(w*16,h*16))
    for i in range(n):
        v=struct.unpack_from('<H',d,i*2)[0]
        img.paste(mimg(v&0x3ff),((i%w)*16,(i//w)*16))
    if grid:
        dr=ImageDraw.Draw(img)
        for x in range(0,w,5): dr.line([(x*16,0),(x*16,h*16)],fill=(255,0,0) if x%10==0 else (255,150,150))
        for y in range(0,h,5): dr.line([(0,y*16),(w*16,y*16)],fill=(255,0,0) if y%10==0 else (255,150,150))
    img.save(out)
if __name__=='__main__':
    render(sys.argv[1],int(sys.argv[2]),sys.argv[3],grid=len(sys.argv)>4)
