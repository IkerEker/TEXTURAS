import json, sys, numpy as np, cv2
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
inv=[x for x in json.load(open('inv2.json')) if x['rol']=='fuente' and x['tipo']=='imagen' and x.get('w') and x['repo'] in('neonizador','analog-fx-plugin','papelator','a-mano','trazo')]
cache={}
def L(im,bg):
    a=np.asarray(im.convert('RGBA')).astype(np.float32); al=a[...,3:]/255; return ((a[...,:3]*al+bg*(1-al))@[.299,.587,.114]).astype(np.float32)
def sheet(x,f):
    k=x['ruta']
    if k not in cache:
        im=Image.open('/home/claude/ikereker/'+k); im.draft('RGB',(600,600)); cache[k]=L(im.resize((round(x['w']*f),round(x['h']*f))),0)
    return cache[k]
for name in sys.argv[1:]:
    c=Image.open('/home/claude/nz_bib/BIBLIOTECA/elementos/'+name); best=[]
    for x in inv:
        f=300/max(x['w'],x['h']); w,h=round(c.width*f),round(c.height*f)
        if w<8 or h<8: continue
        S=sheet(x,f)
        if h>=S.shape[0] or w>=S.shape[1]: continue
        bg=float(np.median(np.concatenate([S[0],S[-1],S[:,0],S[:,-1]])))
        T=L(c.resize((w,h)),bg)
        if T.std()<3: continue
        r=cv2.matchTemplate(S,T,cv2.TM_CCOEFF_NORMED)
        m=cv2.boxFilter(S,-1,(w,h),normalize=True); m2=cv2.boxFilter(S*S,-1,(w,h),normalize=True)
        sd=np.sqrt(np.maximum(m2-m*m,0))[h//2:h//2+r.shape[0], w//2:w//2+r.shape[1]]
        r=np.where((sd[:r.shape[0],:r.shape[1]]>3)&np.isfinite(r),r,-1)
        best.append((float(r.max()),x['ruta']))
    best.sort(reverse=True); print(name, [(round(a,3),b[-60:]) for a,b in best[:2]], flush=True)
