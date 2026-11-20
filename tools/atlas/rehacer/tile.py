# Rehecho de piezas marcadas REHACER en la revisión 100 % (20-11-2026). Ver productos/piezas_neonizador/REHECHAS.json.
# Lee los originales del PC copiados a /mnt/user-data/uploads/Biblioteca/originales/… (cambia la ruta si los tienes en otro sitio)
# y escribe en /home/claude/rehacer/; después se copian a productos/piezas_neonizador con el mismo nombre.
import numpy as np, cv2, json, sys
from PIL import Image
from scipy import ndimage as ndi
D='/mnt/user-data/uploads/Biblioteca/originales/neonizador/Nuevos recursos/'
SRC={'02':'Burbujas brillantes sobre negro','03':'Burbujas de espuma sobre negro (1)','05':'Espectacular racimo de burbujas sobre negro','09':'Macro de espuma jabonosa brillante','10':'Racimo brillante de burbujas sobre negro'}
def mascara(g):
    b=cv2.GaussianBlur(g,(0,0),18); m=b>18
    m=ndi.binary_closing(m,iterations=10); m=ndi.binary_fill_holes(m)
    return ndi.binary_erosion(m,iterations=8)
def mayor_cuadrado(m):
    # DP de mayor cuadrado de unos
    H,W=m.shape; dp=np.zeros((H+1,W+1),np.int32); best=(0,0,0)
    mm=m.astype(np.int32)
    for y in range(H):
        row=dp[y+1]; prev=dp[y]
        for x in np.nonzero(mm[y])[0]:
            v=min(prev[x],prev[x+1],row[x])+1; row[x+1]=v
            if v>best[0]: best=(v,y,x)
    s,y,x=best; return x-s+1,y-s+1,s
def _dp(e,p0=None):
    H,W=e.shape; c=e.copy()
    if p0 is not None: c[0]=np.inf; c[0,p0]=e[0,p0]
    for y in range(1,H):
        p=c[y-1]; l=np.r_[np.inf,p[:-1]]; r=np.r_[p[1:],np.inf]; c[y]+=np.minimum(np.minimum(l,p),r)
    return c
def costura(A,B,periodico=False):
    # A = lo que queda a la izquierda del corte, B = a la derecha; corte de error mínimo
    # periodico: el corte empieza y acaba en la misma columna, para que case al repetir en el otro eje
    e=ndi.gaussian_filter((A-B)**2,1.0); H,W=e.shape; e[:,:6]=1e12; e[:,-6:]=1e12
    if periodico:
        best=None
        for p0 in range(6,W-6,2):
            c=_dp(e,p0)
            if best is None or c[-1,p0]<best[0]: best=(c[-1,p0],p0,c)
        _,p0,c=best; end=p0
    else:
        c=_dp(e); end=int(np.argmin(c[-1]))
    path=np.zeros(H,int); path[-1]=end
    for y in range(H-2,-1,-1):
        x=path[y+1]; lo,hi=max(x-1,0),min(x+2,W); path[y]=lo+np.argmin(c[y,lo:hi])
    m=(np.arange(W)[None,:]<path[:,None]).astype(np.float32)  # 1 = A
    m=ndi.gaussian_filter(m,(0,1.2))
    return A*m+B*(1-m), path
def envolver_x(P,T,periodico=False):
    o=P.shape[1]-T
    izq,_=costura(P[:,T:T+o],P[:,:o],periodico); out=P[:,:T].copy(); out[:,:o]=izq; return out
def tile(k):
    rgb=np.asarray(Image.open(D+SRC[k]+'.png').convert('RGB')).astype(np.float32)
    g=np.asarray(Image.open(D+SRC[k]+'.png').convert('L')).astype(np.float32)
    m=mascara(g); x,y,s=mayor_cuadrado(m)
    P=g[y:y+s,x:x+s]
    # luz aplanada: quitar la caída hacia el borde de la isla (bajas frecuencias), conservar la media
    lo=ndi.gaussian_filter(P,s/6); P=P-lo+lo.mean()
    o=int(round(s*0.2)); T=s-o
    Q=envolver_x(P,T)               # ancho T, alto s
    Q=envolver_x(Q.T,T,True).T           # alto T
    Q=np.clip(Q,0,255).astype(np.uint8)
    Image.fromarray(Q,'L').save(f'/home/claude/rehacer/espuma_tile_{k}.png')
    print(k,'cuadrado',(x,y,s),'tile',T)
    return dict(src=SRC[k]+'.png',recorte=[int(x),int(y),int(s),int(s)],solape=int(o),w=int(T),h=int(T))
J={k:tile(k) for k in (sys.argv[1:] or SRC)}
json.dump(J,open('/home/claude/rehacer/tiles_origen.json','w'),ensure_ascii=False,indent=1)
