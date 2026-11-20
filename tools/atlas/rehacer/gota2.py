# Rehecho de piezas marcadas REHACER en la revisión 100 % (20-11-2026). Ver productos/piezas_neonizador/REHECHAS.json.
# Lee los originales del PC copiados a /mnt/user-data/uploads/Biblioteca/originales/… (cambia la ruta si los tienes en otro sitio)
# y escribe en /home/claude/rehacer/; después se copian a productos/piezas_neonizador con el mismo nombre.
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from scipy.spatial import ConvexHull
S='/mnt/user-data/uploads/Biblioteca/originales/papelator/SOBREPONER/Gotas de lluvia sobre cristal negro.png'
im=np.asarray(Image.open(S).convert('RGB')).astype(np.float32)
Lf=im@[.299,.587,.114]
def gota(cx,cy,R,name,t=30,FR=0.55,ELL=False):
    x0,y0=max(cx-R-6,0),max(cy-R-6,0); x1,y1=cx+R+6,cy+R+6
    C=im[y0:y1,x0:x1]; L=Lf[y0:y1,x0:x1]
    yy,xx=np.mgrid[:L.shape[0],:L.shape[1]]; d=np.hypot(xx-(cx-x0),yy-(cy-y0))
    m=(L>t)&(d<R)
    m=ndi.binary_closing(m,iterations=2)
    lab,n=ndi.label(m); keep=np.zeros_like(m)
    for i in range(1,n+1):
        c=lab==i
        if c.sum()<6: continue
        cyy,cxx=ndi.center_of_mass(c)
        if np.hypot(cxx-(cx-x0),cyy-(cy-y0))<0.85*R: keep|=c
    sizes=ndi.sum(keep,lab,range(1,n+1)); big=lab==(1+int(np.argmax(sizes)))
    sel=big.copy()
    for i in range(1,n+1):
        c=(lab==i)&keep
        if c.sum()<6: continue
        cyy,cxx=ndi.center_of_mass(c)
        if np.hypot(cxx-(cx-x0),cyy-(cy-y0))<FR*R: sel|=c
    pts=np.argwhere(sel)[:,::-1]; h=ConvexHull(pts)
    poly=Image.new('L',(L.shape[1]*4,L.shape[0]*4),0)
    ImageDraw.Draw(poly).polygon([tuple(p*4+2) for p in pts[h.vertices]],fill=255)
    import cv2
    if ELL:
        e=cv2.fitEllipse(pts.astype(np.float32)); (ex,ey),(ew,eh),ang=e
        pe=np.array(poly); cv2.ellipse(pe,((ex*4+2,ey*4+2),(ew*4,eh*4),ang),255,-1,cv2.LINE_AA); poly=Image.fromarray(pe)
    poly=poly.filter(__import__('PIL.ImageFilter',fromlist=['x']).GaussianBlur(6)).point(lambda v:255 if v>128 else 0)
    a=np.asarray(poly.resize((L.shape[1],L.shape[0]),Image.LANCZOS)).astype(np.float32)/255
    a=ndi.gaussian_filter(a,0.6)
    ys,xs=np.nonzero(a>0.02); b=(max(xs.min()-2,0),max(ys.min()-2,0),xs.max()+3,ys.max()+3)
    out=np.dstack([C,a*255]).astype(np.uint8)[b[1]:b[3],b[0]:b[2]]
    Image.fromarray(out,'RGBA').save(f'/home/claude/rehacer/{name}.png'); print(name,out.shape)
gota(720,725,30,'gotas_104',ELL=True)
gota(381,1014,30,'gotas_111')
gota(540,304,24,'gotas_123')
gota(496,171,19,'gotas_133',ELL=True,FR=0.35)
