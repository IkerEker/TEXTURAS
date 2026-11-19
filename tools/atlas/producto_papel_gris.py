"""Producto común: papeles tileables en gris de detalle, 128 = papel plano, a escala real.
Uso: python3 tools/atlas/producto_papel_gris.py   (lee tileables/papel con tile_mm del catálogo)
Método (determinista, CPU): L = luminancia; base = desenfoque gaussiano con envoltura (wrap: se conserva lo tileable)
de sigma = 4 mm; rel = L/base - 1; ganancia G tal que el percentil 99,5 de |rel| = 100 niveles;
gris = clip(128 + 128·G·rel). Para recuperar el relieve relativo: rel = (gris - 128) / (128·G)."""
import json, os, numpy as np, hashlib
from PIL import Image
from scipy import ndimage
it = json.load(open('catalogo.json'))['items']
OUT = 'productos/papel_gris'; os.makedirs(OUT, exist_ok=True)
fichas = []
for e in it:
    if e['carpeta'] != 'tileables/papel' or not e.get('tile_mm') or not e.get('mm_por_px'): continue
    im = Image.open(e['archivo']).convert('RGB')
    a = np.asarray(im, dtype=np.float64) @ np.array([0.299, 0.587, 0.114])
    sig = max(4.0 / e['mm_por_px'], 8.0)
    base = ndimage.gaussian_filter(a, sig, mode='wrap')
    rel = a / np.maximum(base, 1) - 1
    G = 100 / 128 / max(np.percentile(np.abs(rel), 99.5), 1e-6)
    g = np.clip(np.rint(128 + 128 * G * rel), 0, 255).astype(np.uint8)
    name = e['id'].split('/')[-1] + '_gris'
    Image.fromarray(g, 'L').save(f'{OUT}/{name}.png')
    fichas.append(dict(id=f'tx:productos/papel_gris/{name}', archivo=f'papel_gris/{name}.png', de='tx:' + e['id'],
                       w=g.shape[1], h=g.shape[0], tile_mm=e['tile_mm'], mm_por_px=e['mm_por_px'],
                       px_por_mm=round(1 / e['mm_por_px'], 3), ganancia=round(float(G), 4), sigma_px=round(sig, 2),
                       md5_bytes=hashlib.md5(g.tobytes()).hexdigest(), desc=e.get('desc')))
json.dump(dict(formato='PNG gris 8 bits tileable; 128 = papel plano; rel = (v-128)/(128·ganancia)', papeles=fichas),
          open(f'{OUT}/papeles.json', 'w'), ensure_ascii=False, indent=1)
print(len(fichas))
