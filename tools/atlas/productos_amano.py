"""Productos comunes publicados por A mano: 88 cintas de trazo enderezadas y 50 sellos de relieve (grumos).
Uso: python3 tools/atlas/productos_amano.py <clon de a-mano>
Lee js/texdata.js y js/grumosdata.js (generados por A mano; md5 182e0cdb… y d3ca0cf2…) y los escribe tal cual en PNG."""
import sys, json, re, base64, hashlib, os
import numpy as np
from PIL import Image
A = sys.argv[1]
OUT = 'productos'
def modjs(p):
    t = open(p, encoding='utf-8').read()
    j = t[t.index('module.exports =') + len('module.exports ='):].strip().rstrip(';')
    j = re.sub(r'([{,]\s*)([A-Za-z_]\w*)\s*:', r'\1"\2":', j).replace("'", '"')
    return json.loads(j)
md5 = lambda b: hashlib.md5(b).hexdigest()
assert md5(open(f'{A}/js/texdata.js', 'rb').read()) == '182e0cdba680cba58fea00c0dd254ca5'
assert md5(open(f'{A}/js/grumosdata.js', 'rb').read()) == 'd3ca0cf24cb8a2ba3fa4b8a3869c2eba'
ref = json.load(open('plugins/a-mano.json'))
uso = json.load(open('plugins/a-mano/uso_id.json'))
idsrc = {f['orden']: f['id'] for f in uso['filas'] if f['orden'] < 1000}
NOMBRE = {'boli': 'boligrafo', 'rotu': 'rotulador', 'guache': 'gouache', 'pincelfino': 'pincel_fino'}
td = modjs(f'{A}/js/texdata.js')
os.makedirs(f'{OUT}/cintas_trazo', exist_ok=True)
fichas, mal = [], 0
for i, s in enumerate(td['strips']):
    b = base64.b64decode(s['d']); assert len(b) == s['w'] * s['h']
    r = ref['cintas'][i]
    ok = md5(b) == r['md5']; mal += not ok
    fam = NOMBRE.get(s['f'], s['f'])
    name = f'{fam}_{i:02d}'
    Image.frombytes('L', (s['w'], s['h']), b).save(f'{OUT}/cintas_trazo/{name}.png', optimize=False)
    fichas.append(dict(id=f'tx:productos/cintas_trazo/{name}', archivo=f'cintas_trazo/{name}.png', orden_a_mano=i,
                       familia=fam, familia_a_mano=s['f'], w=s['w'], h=s['h'], mh=s['mh'], ar=s['ar'],
                       md5_bytes=md5(b), igual_que_a_mano=ok, origen=idsrc.get(i), origen_ruta='a-mano/TRAZOS/' + r['src'],
                       src_mh_px=r.get('src_mh')))
json.dump(dict(formato='PNG gris 8 bits; filas a lo largo del trazo (fila 0 = donde empieza la mano), columnas a lo ancho; '
                       '0 = papel, 255 = tinta plena. mh = medio ancho en columnas; ar = compresión a lo largo (1 = ninguna). '
                       'md5_bytes = md5 de los bytes crudos (= los de A mano).',
               fuente='A mano 2.38.0, js/texdata.js (md5 182e0cdba680cba58fea00c0dd254ca5)', cintas=fichas),
          open(f'{OUT}/cintas_trazo/cintas.json', 'w'), ensure_ascii=False, indent=1)
print('cintas', len(fichas), 'distintas de A mano:', mal)
pa = td['paper']; print('papel sintético', {k: v for k, v in pa.items() if k != 'd'})
gd = modjs(f'{A}/js/grumosdata.js')
raw = base64.b64decode(gd['d'])
os.makedirs(f'{OUT}/sellos_relieve', exist_ok=True)
fichas, off = [], 0
CL = dict(zip('SML', gd['cls']))
for cn, (lado, n) in zip('SML', gd['cls']):
    for k in range(n):
        b = raw[off:off + lado * lado]; off += lado * lado
        name = f'grumo_{cn}_{k:02d}'
        Image.frombytes('L', (lado, lado), b).save(f'{OUT}/sellos_relieve/{name}.png')
        src = ref['sellos'][cn][k] if k < len(ref['sellos'][cn]) else {}
        fichas.append(dict(id=f'tx:productos/sellos_relieve/{name}', archivo=f'sellos_relieve/{name}.png', clase=cn,
                           lado=lado, md5_bytes=md5(b), foto=src.get('foto'), radio_px=src.get('R'),
                           x=src.get('x'), y=src.get('y')))
assert off == len(raw)
json.dump(dict(formato='PNG gris 8 bits; 128 = sin efecto, más = luz, menos = sombra; luz desde arriba; borde a 128. '
                       'Clases S 20 px, M 36 px, L 56 px. Orden = el de A mano (js/grumosdata.js).',
               fuente='A mano 2.38.0, js/grumosdata.js (md5 d3ca0cf24cb8a2ba3fa4b8a3869c2eba)', sellos=fichas),
          open(f'{OUT}/sellos_relieve/sellos.json', 'w'), ensure_ascii=False, indent=1)
print('sellos', len(fichas))
