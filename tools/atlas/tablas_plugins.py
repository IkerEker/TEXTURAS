"""Tabla `nombre_interno -> id` de cada plugin, en su orden exacto, desde los anexos de plugins/.
Uso: python3 tools/atlas/tablas_plugins.py   -> plugins/<plugin>/uso_id.json"""
import json, re, fnmatch, collections, os

man = json.load(open('originales/MANIFIESTO.json'))
md5inv = json.load(open('tools/estado/md5_inventario.json'))
inv = json.load(open('tools/estado/inv2.json'))
indice = json.load(open('indice/indice.json'))['assets']
ruta2or, or2tx = {}, collections.defaultdict(list)
for g in man['originales']:
    for r in g['rutas']:
        ruta2or[r] = g['id']
for h in man['heredado_neonizador']:
    ruta2or[h['ruta_en_repo']] = h['id']
for a in indice:
    if a.get('origen'):
        or2tx[a['origen']].append(a['id'])
nz_mapa = json.load(open('tools/estado/nz_mapa.json'))


def resolver(ruta, md5=None):
    i = ruta2or.get(ruta) or (('or:' + md5) if md5 and any(g['md5'] == md5 for g in man['originales']) else None)
    if not i and ruta in md5inv:
        m = md5inv[ruta]; i = 'or:' + m if any(g['md5'] == m for g in man['originales']) else None
    return i


def escribe(p, filas, nota):
    os.makedirs(f'plugins/{p}', exist_ok=True)
    sin = [f for f in filas if f.get('fuente_ruta') and (not f.get('id') or (isinstance(f['id'], list) and not all(f['id'])))]
    json.dump(dict(plugin=p, nota=nota, total=len(filas), sin_id=len(sin), filas=filas),
              open(f'plugins/{p}/uso_id.json', 'w'), ensure_ascii=False, indent=1)
    print(p, len(filas), 'filas ·', len(sin), 'sin id')


# ---- NEONIZADOR: 287 texturas en el orden de su anexo
nzf = {x['ruta']: x['md5'] for x in json.load(open('plugins/neonizador/fuentes.json'))}
filas = []
for n, e in enumerate(json.load(open('plugins/neonizador/assets.json'))):
    src = e['fuente'].split('  ←')[0].strip()
    if '*' in src:
        pat = src.split(' (')[0]
        src_list = sorted(r for r in nzf if fnmatch.fnmatch(r, pat))
        her = [resolver('neonizador/' + r, nzf[r]) for r in src_list]
        filas.append(dict(orden=n, nombre_interno=e['nombre'], familia=e['familia'], uso=e['uso'], id=her,
                          fuente_ruta=src, formato=e['formato_final'], nota='atlas: piezas en orden alfabético'))
        continue
    ruta = 'neonizador/' + src
    her = ruta2or.get(ruta) or resolver(ruta, e.get('md5_fuente') or nzf.get(src))
    m = nz_mapa.get(e['nombre']) or {}
    orig = ruta2or.get(m.get('original')) if m.get('original') else None
    filas.append(dict(orden=n, nombre_interno=e['nombre'], familia=e['familia'], uso=e['uso'], id=her,
                      fuente_ruta=src, original_real=orig, productos_comunes=m.get('ids') or or2tx.get(orig, []),
                      formato=e['formato_final']))
escribe('neonizador', filas, 'id = archivo heredado exacto (lo que lee hoy build_texpack.py) → .bin idéntico. '
        'original_real/productos_comunes = la foto original y su versión procesada en TEXTURAS (cambiarían el resultado).')

# ---- PAPELATOR: 750 filas del anexo (familias en su orden)
filas = []
for n, e in enumerate(json.load(open('plugins/papelator/anexo.json'))):
    pr = e.get('parametros') or {}
    f = e['fuente']
    fs = f if isinstance(f, list) else [f]
    ids = [resolver('papelator/' + x, pr.get('md5_archivo') if len(fs) == 1 else None) for x in fs]
    i = ids[0] if len(ids) == 1 else ids
    fila = dict(orden=n, familia=e['familia'], uso=e['uso'], fuente_ruta=f, id=i,
                productos_comunes=sum((or2tx.get(x, []) for x in ids if x), []),
                formato=e['formato_final'])
    for k in ('tileMm', 'src_index', 'indice', 'name', 'id'):
        if k in pr: fila['p_' + k] = pr[k]
    filas.append(fila)
escribe('papelator', filas, 'Los derivados (plugin/assets) no se regeneran: basta con que cada fuente id tenga su md5. '
        'Las 3 parejas duplicadas de imperfecciones citan el mismo id dos veces (mismo orden que hoy).')

# ---- A MANO: 88 cintas (orden = posición en js/texdata.js) y 4 fotos de grumos
am = json.load(open('plugins/a-mano.json'))
filas = []
for c in am['cintas']:
    ruta = 'a-mano/TRAZOS/' + c['src']
    filas.append(dict(orden=c['i'], nombre_interno=f"cinta #{c['i']}", familia=c['f'], fuente_ruta='TRAZOS/' + c['src'],
                      id=resolver(ruta), md5_cinta=c['md5'], w=c['w'], h=c['h'], mh=c['mh'], ar=c['ar']))
for s in am['assets']:
    pass
fotos = sorted({x['foto'] for cl in am['sellos'].values() for x in cl}) if isinstance(am['sellos'], dict) else []
for k, f in enumerate(fotos):
    filas.append(dict(orden=1000 + k, nombre_interno='grumos ' + f, familia='grumos', fuente_ruta='referencias/texturas/' + f,
                      id=resolver('a-mano/referencias/texturas/' + f)))
src_ord = []
for s in am['assets']:
    if not s.get('fuente'): continue
    src_ord.append(dict(fuente=s['fuente'], id=resolver('a-mano/' + s['fuente'], s.get('md5')), familia=s.get('familia'),
                        inicio=(s.get('parametros') or {}).get('inicio'), estado=s.get('estado')))
escribe('a-mano', filas, 'Orden = el de SOURCES (ver «fuentes_en_orden»). Los duplicados de CERAS/GUACHE se citan dos veces.')
d = json.load(open('plugins/a-mano/uso_id.json')); d['fuentes_en_orden'] = src_ord
json.dump(d, open('plugins/a-mano/uso_id.json', 'w'), ensure_ascii=False, indent=1)

# ---- ANALOG FX: 294 filas
filas = []
for n, e in enumerate(json.load(open('plugins/analog-fx/anexo.json'))):
    f = e['fuente']
    i = resolver('analog-fx-plugin/' + f)
    filas.append(dict(orden=n, nombre_interno=e.get('id_plugin'), familia=e.get('familia'), uso=e['uso'], fuente_ruta=f,
                      id=i, productos_comunes=or2tx.get(i, []), formato=e.get('formato_final')))
escribe('analog-fx', filas, 'Solo las filas con nombre_interno se usan. Para resultado idéntico: originales (id). '
        'Para adoptar los tileables nuevos: productos_comunes (cambia un poco; prueba 3 con PSNR ≥ 40 dB).')

# ---- TRAZO: familias con patrones -> archivos en orden alfabético
tr_rutas = sorted(e['ruta'][len('trazo/'):] for e in inv if e['repo'] == 'trazo' and e['rol'] == 'fuente')
filas = []
for e in json.load(open('plugins/trazo/anexo.json')):
    for parte in re.split(r';\s*', e['fuente'] or ''):
        m = re.match(r'\s*(.*?)(?:\s*\((q\d)\))?\s*$', parte); pat, q = m.group(1), m.group(2)
        pats = []
        b = re.match(r'(.*)\{(.*)\}(.*)', pat)
        if b:
            pats = [b.group(1) + x.strip() + b.group(3) for x in b.group(2).split(',')]
        elif pat:
            pats = [pat]
        for p in pats:
            hits = [r for r in tr_rutas if fnmatch.fnmatch(r, p) or fnmatch.fnmatch(r, p + '/*')]
            for r in hits:
                filas.append(dict(familia=e['familia'], uso=e['uso'], patron=p, q=q, fuente_ruta=r,
                                  id=resolver('trazo/' + r)))
for k, f in enumerate(filas): f['orden'] = k
escribe('trazo', filas, 'Patrones de build_assets.py resueltos contra TEXTURES/ (orden alfabético, como glob ordenado). '
        'Verificar primero que el build actual se reproduce (ficha §6.1).')
