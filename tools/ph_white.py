import sys, json, os, numpy as np
sys.path.insert(0,'/home/claude/work')
from inventario import phash, dhash
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
Image.MAX_IMAGE_PIXELS=None
def one(p):
    try:
        im=Image.open(p); im.draft('RGB',(512,512)); im.thumbnail((256,256))
        a=np.asarray(im.convert('RGBA')).astype(np.float32)
        al=a[...,3:]/255; rgb=a[...,:3]*al+255*(1-al)
        L=rgb@[.299,.587,.114]; g=Image.fromarray(L.clip(0,255).astype(np.uint8))
        return p, phash(g), dhash(g), a.shape[1]/a.shape[0]
    except Exception as e: return p,None,None,None
if __name__=='__main__':
    roots=sys.argv[2:]; ps=[]
    for r in roots:
        for dp,dn,fn in os.walk(r):
            if '/.git' in dp or '/hojas' in dp or '/video' in dp: continue
            ps+= [os.path.join(dp,f) for f in fn if f.endswith('.png') and not f.endswith('_trama.jpg')]
    with ProcessPoolExecutor(4) as ex: out=list(ex.map(one,ps,chunksize=16))
    json.dump(out,open(sys.argv[1],'w'))
    print(len(out))
