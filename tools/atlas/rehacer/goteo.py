# Rehecho de piezas marcadas REHACER en la revisión 100 % (20-11-2026). Ver productos/piezas_neonizador/REHECHAS.json.
# Lee los originales del PC copiados a /mnt/user-data/uploads/Biblioteca/originales/… (cambia la ruta si los tienes en otro sitio)
# y escribe en /home/claude/rehacer/; después se copian a productos/piezas_neonizador con el mismo nombre.
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
S='/mnt/user-data/uploads/Biblioteca/originales/neonizador/TEXTURAS_02/Goteos de pintura blanca sobre negro (1).png'
im=np.asarray(Image.open(S).convert('RGB')).astype(np.float32)
x0,y0,x1,y1=104,384,157,676
C=im[y0:y1,x0:x1]; L=C@[.299,.587,.114]
bg=np.percentile(L,20); print('bg',bg)
# alfa = cobertura: rampa suave entre negro de fondo y pintura
a=np.clip((L-bg-12)/(150-bg-12),0,1)
m=a>0.18
lab,n=ndi.label(ndi.binary_dilation(m,iterations=2))
# quitar el goteo grande de la derecha: componentes que tocan el borde derecho en la parte alta
sizes=ndi.sum(np.ones_like(lab),lab,range(1,n+1)); big=1+int(np.argmax(sizes))
keep=lab==big
for i in range(1,n+1):
    c=lab==i; ys,xs=np.nonzero(c)
    if i!=big and c.sum()>=15 and xs.max()<x1-x0-6: keep|=c
a=a*ndi.binary_dilation(keep,iterations=1)
a[:16,36:]=0; a[:16,:12]=0
# raíz: unir con suavidad arriba (fade de 6 px en el corte superior)
a[:6]*=np.linspace(0,1,6)[:,None]
ys,xs=np.nonzero(a>0.02); bb=(max(xs.min()-3,0),max(ys.min()-3,0),xs.max()+4,ys.max()+4)
rgb=np.clip(C/np.maximum(a[...,None],1e-3)*0+C.max(),0,255)
# color sin premultiplicar: el gris de la pintura (luminancia normalizada por alfa)
g=np.clip((C - bg*(1-a[...,None]))/np.maximum(a[...,None],0.05),0,255)
solid=a>0.75
_,(iy,ix)=ndi.distance_transform_edt(~solid,return_indices=True)
g=np.where(solid[...,None],g,C[iy,ix])
out=np.dstack([g,a*255]).astype(np.uint8)[bb[1]:bb[3],bb[0]:bb[2]]
Image.fromarray(out,'RGBA').save('/home/claude/rehacer/goteo_238_06.png'); print(out.shape)
