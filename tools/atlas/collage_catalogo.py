"""Junta las fichas del collage → collage/catalogo.json, collage/CATALOGO.md y hojas de revisión por familia."""
import collections, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from collage_hoja import hoja
from collage_tabla import MAT

R = Path('collage/_trabajo/resultados')
items, fuentes, revisar = [], [], json.load(open('collage/_trabajo/revision.json')) if Path('collage/_trabajo/revision.json').exists() else {}
for f in sorted(R.glob('*.json')):
    r = json.load(open(f))
    fuentes.append({k: v for k, v in r.items() if k != 'piezas'} | dict(piezas=[p['id'] for p in r.get('piezas', [])]))
    for p in r.get('piezas', []):
        nota = revisar.get(p['archivo'].split('/')[-1][:-4])
        if nota:
            if nota.get('descartar'):
                continue
            p.update({k: v for k, v in nota.items() if k != 'descartar'})
        items.append(p)
cat = dict(descripcion='Piezas de collage recortadas de las imágenes de Biblioteca/AÑADIDOS/COLLAGE (generadas con IA por Iker sobre '
                       'fondo liso). PNG RGBA sin premultiplicar: alfa = cobertura real (fibras, bordes y materiales translúcidos con '
                       'alfa parcial), color descontaminado del fondo. Sombra de contacto aparte en *_sombra.png cuando la hay.',
           metodo='tools/atlas/collage.py (fondo = polinomio suave por canal; opacos: proyección I−B sobre F−B; translúcidos: alfa '
                  'mínima respecto al fondo medido)',
           materiales={k: dict(familia=v[0], desc=v[1], optica=v[2], borde=v[3], modo=v[6]) for k, v in MAT.items()},
           total=len(items), por_familia=dict(collections.Counter(i['familia'] for i in items)),
           items=items, fuentes=fuentes)
json.dump(cat, open('collage/catalogo.json', 'w'), ensure_ascii=False, indent=1)

Path('collage/hojas').mkdir(exist_ok=True)
L = ['# collage/ · piezas recortadas para collage', '',
     'Generado por `tools/atlas/collage_catalogo.py`. Total: **%d piezas** de %d imágenes. Todas revisadas a ojo sobre damero, negro y '
     'magenta (`collage/hojas/`).' % (len(items), len(fuentes)), '',
     '| Familia | Piezas | Qué es | Óptica | Hoja |', '|---|---|---|---|---|']
fam = collections.defaultdict(list)
for i in items: fam[i['familia']].append(i)
for k in sorted(fam):
    m = MAT[fam[k][0]['material']]
    h = 'collage/hojas/%s.jpg' % k.replace('/', '__')
    hoja([dict(x, archivo=x['archivo']) for x in fam[k]], h)
    L.append('| `%s` | %d | %s | %s | `%s` |' % (k, len(fam[k]), m[1], m[2], h))
L += ['', '## Piezas', '', '| id | px | color | cobertura | alfa parcial | sombra | fuente |', '|---|---|---|---|---|---|---|']
for i in items:
    L.append('| `%s` | %d×%d | %s | %.2f | %s | %s | %s |' % (i['archivo'].split('/')[-1][:-4], i['w'], i['h'], i['color'], i['cobertura'],
             '%.0f %%' % (100 * i['alfa_parcial']) if 'alfa_parcial' in i else '—', 'sí' if 'sombra' in i else '', i['fuente']['ruta'].split('/')[-1]))
open('collage/CATALOGO.md', 'w').write('\n'.join(L) + '\n')
print(len(items), dict(collections.Counter(i['familia'] for i in items)))
