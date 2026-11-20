# Quita tintes de croma (verde/cian/rosa) en fibras y canto: conserva la luminancia del píxel
# y le da el color (crominancia) del papel sólido más cercano.
import sys, numpy as np
from PIL import Image
from scipy.ndimage import distance_transform_edt, binary_dilation, binary_erosion, gaussian_filter
def lum(x): return x[...,0]*.299+x[...,1]*.587+x[...,2]*.114
def arreglar(p, out, ancho=6, umbral=0.04):
    x=np.asarray(Image.open(p).convert('RGBA')).astype(np.float32)/255
    rgb,a=x[...,:3],x[...,3]
    solid=binary_erosion(a>0.98,iterations=3)
    # color de referencia suavizado del papel sólido (normalizado por luminancia)
    w=gaussian_filter(solid.astype(np.float32),6)+1e-6
    ref=np.dstack([gaussian_filter(rgb[...,i]*solid,6) for i in range(3)])/w[...,None]
    have=w>0.05
    ref=np.where(have[...,None],ref,0)
    _,idx=distance_transform_edt(~have,return_indices=True)
    ref=ref[idx[0],idx[1]]
    zona=(a>0)&~binary_erosion(a>0.98,iterations=ancho)
    Lp=lum(rgb); Lr=np.maximum(lum(ref),1e-3)
    nuevo=np.clip(ref*(Lp/Lr)[...,None],0,1)
    # dif de crominancia
    cp=rgb-Lp[...,None]; cr=nuevo-lum(nuevo)[...,None]
    dev=np.linalg.norm(cp-cr,axis=-1)
    t=np.clip((dev-umbral)/0.06,0,1)*zona
    o=rgb*(1-t[...,None])+nuevo*t[...,None]
    y=np.dstack([o,a]); Image.fromarray((y*255+.5).astype(np.uint8),'RGBA').save(out,optimize=True)
    return float(t.mean()), float((dev*zona).sum()/max(zona.sum(),1))
if __name__=='__main__': print(arreglar(sys.argv[1],sys.argv[2]))
