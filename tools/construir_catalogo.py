#!/usr/bin/env python3
"""Une todos los resultados en TEXTURAS/catalogo.json y escribe CATALOGO.md.
Uso: python3 construir_catalogo.py DIR_RESULTADOS videos_cat.json inv2.json DESTINO"""
import sys, os, json, glob, collections, datetime

RES, VID, INV, DEST = sys.argv[1:5]
inv = {x['ruta']: x for x in json.load(open(INV))}

NOMBRE_SUB = {
 'tileables/papel': 'Papeles', 'tileables/superficies': 'Paredes, suelos, piedra y metal', 'tileables/madera_y_carton': 'Madera, OSB, aglomerado y cartón',
 'tileables/vidrios_y_plasticos': 'Vidrios y plásticos (para poner DELANTE, en Trama)', 'tileables/pintura': 'Pintura: gouache, óleo, acuarela y aguadas',
 'tileables/grunge': 'Grunge, tintas impresas, fotocopia y ruido', 'tileables/liquidos': 'Agua, espuma, mármol y cáusticas',
 'tileables/grafito_y_carbon': 'Rayado de grafito y carbón', 'tileables/goteos': 'Goteos y salpicaduras que cubren todo',
 'tileables/veta_pintada': 'Vetas y fibras pintadas', 'tileables/naturaleza': 'Moho y líquenes',
}

items = []
omit = []
for f in sorted(glob.glob(os.path.join(RES, '*.json'))):
    for e in json.load(open(f)):
        if 'archivo' in e:
            items.append(e)
        elif 'omitido' in e:
            omit.append(e)
_cl = os.path.join(os.path.dirname(os.path.abspath(RES)), 'clasif.json')
if os.path.exists(_cl):
    for c in json.load(open(_cl)):
        if c.get('metodo') == 'omitir':
            omit.append(dict(omitido=c['src'], motivo=c.get('motivo')))
for e in json.load(open(VID)):
    e['tipo'] = 'video'
    items.append(e)
# banco de goteos de Analog FX (ya procesado, se copia tal cual)
gc = json.load(open(os.path.join(DEST, 'manchas', 'goteos', 'catalogo.json')))
for g in gc:
    items.append(dict(archivo='manchas/goteos/' + g['archivo'], cat='manchas', sub='goteos/' + g['clase'], tipo='imagen',
                      desc='Goteo real de pintura (%s): raíz arriba' % g['clase'], w=g['w'], h=g['h'], alfa=True, modo='normal',
                      metodo='banco de Analog FX (BIBLIOTECA/goteos)', usado_en='Analog FX (gotas reales)',
                      origen=dict(ruta='analog-fx-plugin/GOTAS/' + g['origen'], caja=g.get('origen_caja')),
                      medidas={k: g[k] for k in ('largo', 'ancho_medio', 'ancho_raiz', 'ancho_bulbo', 'bulbo', 'cabeza', 'ondulacion',
                                                'grietas', 'huecos', 'cuelga') if k in g}))

for e in items:
    e.setdefault('tipo', 'imagen')
    e['id'] = os.path.splitext(e['archivo'])[0]
    o = e.get('origen', {})
    src = inv.get(o.get('ruta'))
    if src:
        o['repo'] = src['repo']; o['sha1'] = src['sha1']; o['w'] = src.get('w'); o['h'] = src.get('h')
    for k in [k for k, v in e.items() if v is None]:
        del e[k]
    e['carpeta'] = os.path.dirname(e['archivo'])
    parts = e['carpeta'].split('/')
    e['cat'] = parts[0]; e['sub'] = '/'.join(parts[1:])
    if e.get('tileable') and max(e['costura']) > 1.3 and 'periodos' not in e.get('proceso', ''):
        e['aviso'] = ('la costura puede notarse en el cruce de esquinas (brillos o formas largas): úsala a tamaño grande, '
                      'o gira/mezcla dos lecturas desplazadas')
    if not os.path.exists(os.path.join(DEST, e['archivo'])):
        raise SystemExit('falta ' + e['archivo'])

items.sort(key=lambda e: e['archivo'])
ids = collections.Counter(e['id'] for e in items)
assert max(ids.values()) == 1, [k for k, v in ids.items() if v > 1][:5]

por = collections.Counter(e['carpeta'] for e in items)
cat = dict(nombre='TEXTURAS', descripcion='Biblioteca común de texturas, trazos, elementos y vídeos para los plugins de Iker',
           generado=datetime.date.today().isoformat(), total=len(items),
           por_categoria=dict(collections.Counter(e['cat'] for e in items)), por_carpeta=dict(sorted(por.items())),
           omitidos=[dict(ruta=o['omitido'], motivo=o.get('motivo')) for o in omit], items=items)
json.dump(cat, open(os.path.join(DEST, 'catalogo.json'), 'w'), ensure_ascii=False, indent=1)

# ---------------------------------------------------------------- CATALOGO.md
L = ['# Catálogo de TEXTURAS', '', 'Generado el %s · %d archivos. La ficha completa de cada uno está en `catalogo.json`; '
     'las hojas de contactos de cada carpeta, en `hojas/`.' % (cat['generado'], len(items)), '']
L += ['## Resumen', '', '| Carpeta | Archivos |', '|---|---:|']
for k, v in sorted(por.items()):
    if '/goteos/' in k + '/':
        continue
    L.append('| `%s` | %d |' % (k, v))
L.append('| `manchas/goteos/*` (banco de Analog FX) | %d |' % sum(v for k, v in por.items() if k.startswith('manchas/goteos')))
L.append('')
group = collections.defaultdict(list)
for e in items:
    if e['carpeta'].startswith('manchas/goteos'):
        continue
    group[e['carpeta']].append(e)
for k in sorted(group):
    es = group[k]
    L += ['## `%s`' % k, '']
    if NOMBRE_SUB.get(k):
        L += [NOMBRE_SUB[k], '']
    hj = 'hojas/%s.jpg' % k.replace('/', '__')
    if os.path.exists(os.path.join(DEST, hj)):
        L += ['Hoja de contactos: [`%s`](%s)' % (hj, hj), '']
    if es[0]['tipo'] == 'video':
        L += ['| Archivo | Qué es | Tamaño | fps (real) | Duración | Comportamiento | Modo |', '|---|---|---|---|---|---|---|']
        for e in es:
            L.append('| `%s` | %s | %d×%d | %s (%s) | %ss | %s%s | %s |' % (
                os.path.basename(e['archivo']), e['desc'], e['w'], e['h'], e.get('fps'), e.get('fps_efectivo'), e.get('duracion'),
                e.get('comportamiento', ''), ' · loop: `%s`' % os.path.basename(e['version_loop']['archivo']) if e.get('version_loop') else '',
                e.get('modo', '')))
    else:
        L += ['| Archivo | Qué es | Tamaño | Modo | Notas |', '|---|---|---|---|---|']
        for e in es:
            notas = []
            if e.get('tileable'):
                notas.append('tileable (costura %.2f/%.2f)' % tuple(e['costura']))
            if e.get('tile_mm'):
                notas.append('tile = %g×%g mm' % tuple(e['tile_mm']))
            if e.get('tamano_real_mm'):
                notas.append('tamaño real %s mm' % e['tamano_real_mm'])
            if e.get('pareja'):
                notas.append('pareja: `%s`' % os.path.basename(e['pareja']))
            if e.get('usado_en'):
                notas.append('usado en %s' % e['usado_en'])
            L.append('| `%s` | %s | %d×%d%s | %s | %s |' % (os.path.basename(e['archivo']), e.get('desc', ''), e['w'], e['h'],
                                                            ' RGBA' if e.get('alfa') else '', e.get('modo', ''), ' · '.join(notas)))
    L.append('')
open(os.path.join(DEST, 'CATALOGO.md'), 'w').write('\n'.join(L))
print(len(items), 'archivos en el catálogo;', len(omit), 'fuentes omitidas')
print(json.dumps(cat['por_categoria'], ensure_ascii=False))
