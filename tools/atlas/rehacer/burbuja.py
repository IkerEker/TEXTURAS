# Rehecho de piezas marcadas REHACER en la revisión 100 % (20-11-2026). Ver productos/piezas_neonizador/REHECHAS.json.
# Lee los originales del PC copiados a /mnt/user-data/uploads/Biblioteca/originales/… (cambia la ruta si los tienes en otro sitio)
# y escribe en /home/claude/rehacer/; después se copian a productos/piezas_neonizador con el mismo nombre.
import numpy as np, cv2, json
from PIL import Image, ImageDraw
D='/mnt/user-data/uploads/Biblioteca/originales/neonizador/TEXTURAS_02/'
F={'228':'Burbujas de jabón iridiscentes sobre negro.png','229':'Burbujas iridiscentes flotando en la oscuridad.png','230':'Burbujas iridiscentes sobre fondo negro.png'}
IM={k:np.asarray(Image.open(D+f).convert('RGB')).astype(np.float32) for k,f in F.items()}
def refina(S,cx,cy,r):
    mx=S.max(-1); H,W=mx.shape
    yy,xx=np.mgrid[0:H,0:W]
    d=np.hypot(xx-cx,yy-cy); m=(d<r*1.25)&(d>r*0.6)&(mx>45)
    pts=np.argwhere(m)[:,::-1].astype(np.float32)
    # ajuste de círculo por mínimos cuadrados (Kasa), con pesos por brillo
    x,y=pts[:,0],pts[:,1]; A=np.c_[2*x,2*y,np.ones_like(x)]; b=x*x+y*y
    for _ in range(3):
        c=np.linalg.lstsq(A,b,rcond=None)[0]; ccx,ccy=c[0],c[1]; rr=np.sqrt(c[2]+ccx**2+ccy**2)
        res=np.abs(np.hypot(x-ccx,y-ccy)-rr); k=res<max(6,0.12*rr); A,b,x,y=A[k],b[k],x[k],y[k]
    return ccx,ccy,rr
def burbuja(src,cx,cy,r,name,ref=True):
    S=IM[src]; H,W,_=S.shape
    if ref: cx,cy,r=refina(S,cx,cy,r)
    R=r*1.10
    x0,y0,x1,y1=int(max(cx-R-6,0)),int(max(cy-R-6,0)),int(min(cx+R+6,W)),int(min(cy+R+6,H))
    C=S[y0:y1,x0:x1]; mx=C.max(-1)
    a=np.clip(1.2*(mx-3),0,255)/255
    yy,xx=np.mgrid[y0:y1,x0:x1]; d=np.hypot(xx-cx,yy-cy)
    mask=np.clip((r*1.10-d)/(r*0.05),0,1)
    a=a*mask
    col=np.clip(C/np.maximum(a[...,None],1/255),0,255)
    out=np.dstack([col,a*255]).astype(np.uint8)
    ys,xs=np.nonzero(out[...,3]>2); b=(max(xs.min()-3,0),max(ys.min()-3,0),xs.max()+4,ys.max()+4)
    out=out[b[1]:b[3],b[0]:b[2]]
    edge=[cx-r*1.1<1,cy-r*1.1<1,cx+r*1.1>W-1,cy+r*1.1>H-1]
    Image.fromarray(out,'RGBA').save(f'/home/claude/rehacer/{name}.png')
    print(name,src,(round(cx),round(cy),round(r)),out.shape,'toca borde foto' if any(edge) else 'completa')
    return dict(src=F[src],cx=round(float(cx),1),cy=round(float(cy),1),r=round(float(r),1))
J={}
J['burbujas_229_09']=burbuja('229',961,189,76,'burbujas_229_09')  # misma pompa que 229_06: la vieja (369,50) toca el borde de la foto
J['burbujas_229_04']=burbuja('229',351,1084,56,'burbujas_229_04')
J['burbujas_229_05']=burbuja('229',585,519,118,'burbujas_229_05')
J['burbujas_229_07']=burbuja('228',355,1059,130,'burbujas_229_07')
J['burbujas_229_11']=burbuja('228',720,804,26,'burbujas_229_11')
J['burbujas_230_03']=burbuja('228',910,903,168,'burbujas_230_03')
J['burbujas_230_05']=burbuja('229',358,365,148,'burbujas_230_05')
json.dump(J,open('/home/claude/rehacer/burbujas_origen.json','w'),ensure_ascii=False,indent=1)
