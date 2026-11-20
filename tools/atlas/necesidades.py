"""Construye el catálogo de necesidades: indice/necesidades_spec.json → indice/necesidades.json + hojas.

    python3 tools/atlas/necesidades.py            # todas
    python3 tools/atlas/necesidades.py pieza_goteo papel_fondo_calido

Cada necesidad = una búsqueda del buscador (abanico con semilla fija, una por grupo, reparto por colección) +
lo revisado a ojo: «quitar» (ids que no valen) y «poner» (ids que se fijan delante). Las hojas se guardan en
indice/necesidades_hojas/<nombre>.jpg para que el plugin mire UNA imagen y elija."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from biblioteca import Biblioteca, R

N = 16
spec = json.load(open(R / 'indice' / 'necesidades_spec.json', encoding='utf-8'))
B = Biblioteca()
salida = R / 'indice' / 'necesidades.json'
viejo = {n['nombre']: n for n in json.load(open(salida, encoding='utf-8'))['necesidades']} if salida.exists() else {}
solo = set(sys.argv[1:])
out = []
for nd in spec['necesidades']:
    if solo and nd['nombre'] not in solo:
        if nd['nombre'] in viejo: out.append(viejo[nd['nombre']])
        continue
    f = dict(nd.get('f', {})); sin_clase = f.pop('sin_clase', [])
    quitar = set(nd.get('quitar', [])); f['excluir'] = quitar | {i for i in B.por_id if B.clase(B.por_id[i]) in sin_clase}
    f.setdefault('min', 3)
    r = B.buscar(nd.get('consulta', ''), n=N + 8, semilla=nd.get('semilla', 1), **f)
    ids = [i for i in nd.get('poner', []) if i in B.por_id]
    if not nd.get('cerrada'):
        ids += [e['id'] for e in r.sel if e['id'] not in ids][:max(0, N - len(ids))]
    sel = [B.por_id[i] for i in ids]
    hoja = B.hoja(sel, nd['nombre'], carpeta=R / 'indice' / 'necesidades_hojas', T=220, COL=4)
    o = {k: nd[k] for k in ('grupo', 'nombre', 'titulo', 'como') if k in nd}
    o['consulta'] = (nd.get('consulta', '') + ' ' + ' '.join(
        f'--{k} "{v}"' if isinstance(v, str) else f'--{k}' for k, v in nd.get('f', {}).items() if k != 'sin_clase')).strip()
    o['ids'] = ids
    o['hoja'] = 'TEXTURAS/indice/necesidades_hojas/' + nd['nombre'] + '.jpg'
    o['encajan'] = len(r.res)
    o['revisada'] = 'a ojo, una a una (20-11-2026)' if nd.get('cerrada') else 'automática (sonidos y LUT: no se ven; elegidos por subcategoría medida)'
    out.append(o)
    print(f"{nd['nombre']:30} {len(ids):3} de {len(r.res):5} · grupos {len({e['_grupo'] for e in sel})} · "
          f"{dict(__import__('collections').Counter(e['coleccion'] for e in sel))}")
json.dump({'nota': 'Catálogo de necesidades (generado por tools/atlas/necesidades.py desde necesidades_spec.json, '
                   'revisado a ojo). Úsalo con buscar.py --necesidades / --necesidad NOMBRE.', 'necesidades': out},
          open(salida, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
