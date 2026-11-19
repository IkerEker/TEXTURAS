import json, sys, numpy as np, glob, os
from PIL import Image
from scipy.fft import dct
T='/home/claude/texturas'; A=T+'/acidbite'
def ph(g):
    a=np.asarray(g.resize((32,32),Image.LANCZOS),dtype=np.float64)
    d=dct(dct(a,axis=0,norm='ortho'),axis=1,norm='ortho')[:8,:8]
    return int(''.join('1' if b else '0' for b in (d>np.median(d.flatten()[1:])).flatten()),2)
def lum(im):
    a=np.asarray(im.convert('RGB')).astype(np.float32)
    return Image.fromarray((a@np.array([.299,.587,.114],np.float32)).clip(0,255).astype(np.uint8))
inv=json.load(open(T+'/tools/estado/inv2.json'))
ref=[(int(e['phash'],16),e['ruta'],'img') for e in inv if e.get('phash')]
# fotogramas de los vídeos de TEXTURAS (tiras)
for f in glob.glob(T+'/video/_tiras/*.jpg'):
    im=Image.open(f); h=im.height; n=max(1,round(im.width/(h*16/9))) 
    # tiras: fotogramas de igual ancho; estimar por ancho/alto del vídeo no fiable -> trocear en cuadros de alto h * aspecto
    w=im.width
    for k in range(8):
        x0=int(w*k/8); x1=int(w*(k+1)/8)
        ref.append((ph(lum(im.crop((x0,0,x1,h)))),'video/_tiras/'+os.path.basename(f)+f'#{k}','vid'))
R=np.array([r[0] for r in ref],dtype=np.uint64)
cat=json.load(open(A+'/datos/catalogo.json'))
out=[]
def ham(x):
    v=np.bitwise_xor(R,np.uint64(x)); 
    return np.array([bin(int(t)).count('1') for t in v])
for e in cat:
    if e['tipo'] not in ('video','imagen') or e.get('copia_de_plantilla'): continue
    f=f"{A}/hojas/{e['id']}.jpg"
    if not os.path.exists(f): continue
    im=Image.open(f); W,H=im.size
    tiles=[im] if e['tipo']=='imagen' else [im.crop((c*W//4,r*H//2,(c+1)*W//4,(r+1)*H//2)) for r in range(2) for c in range(4)]
    best=(99,None)
    for t in tiles:
        g=lum(t); a=np.asarray(g)
        if a.std()<6: continue
        h=ham(ph(g)); i=int(h.argmin())
        if h[i]<best[0]: best=(int(h[i]),ref[i][1])
    out.append(dict(id=e['id'],ruta=e['ruta'],dist=best[0],mas_parecido=best[1]))
out.sort(key=lambda x:x['dist'])
json.dump(out,open('indice/cruce_phash_acidbite.json','w'),ensure_ascii=False,indent=0)
import collections
print(collections.Counter(min(o['dist'],20) for o in out))
for o in out[:25]: print(o['dist'],o['ruta'][-55:],'->',o['mas_parecido'])
