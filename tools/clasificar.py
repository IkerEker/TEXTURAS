#!/usr/bin/env python3
"""Clasifica cada imagen fuente: categoría, subcategoría, método de procesado, nombre y datos conocidos.
Uso: python3 -I clasificar.py inv2.json RAIZ_REPOS hojas/indice.json salida.json
Usa las tablas que ya existen en las herramientas de los plugins (se leen con ast, sin ejecutarlas)."""
import sys, os, re, json, ast, unicodedata, collections, fnmatch

INV, R, IDXH, OUT = sys.argv[1:5]
P = lambda *a: os.path.join(R, *a)


# ------------------------------------------------------------------ lectura segura de tablas
def ev(node, env):
    if isinstance(node, ast.Constant): return node.value
    if isinstance(node, (ast.List, ast.Tuple)): return [ev(e, env) for e in node.elts]
    if isinstance(node, ast.Set): return {ev(e, env) for e in node.elts}
    if isinstance(node, ast.Dict): return {ev(k, env): ev(v, env) for k, v in zip(node.keys, node.values)}
    if isinstance(node, ast.Name): return env.get(node.id, node.id)
    if isinstance(node, ast.Call) and getattr(node.func, 'id', '') == 'dict':
        return {k.arg: ev(k.value, env) for k in node.keywords}
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add): return ev(node.left, env) + ev(node.right, env)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub): return -ev(node.operand, env)
    if isinstance(node, ast.Call):  # g(...) de trazo: se devuelve la lista de patrones
        return ('CALL', getattr(node.func, 'id', '?'), [ev(a, env) for a in node.args])
    if isinstance(node, ast.Starred): return ev(node.value, env)
    if isinstance(node, ast.ListComp): return []
    if isinstance(node, ast.JoinedStr): return ''
    if isinstance(node, ast.Attribute): return '?'
    raise ValueError(ast.dump(node)[:120])


def tabla(path, var, env=None):
    tree = ast.parse(open(path, encoding='utf-8').read())
    for n in tree.body:
        if isinstance(n, ast.Assign) and any(getattr(t, 'id', None) == var for t in n.targets):
            return ev(n.value, env or {})
    raise KeyError(var)


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    s = re.sub(r'\(\d+\)|-\d+$|\d+$', '', s.strip())
    s = re.sub(r'[^a-zA-Z0-9]+', '_', s.lower()).strip('_')
    return re.sub(r'_+', '_', s)[:60]


GEN = re.compile(r'^(gemini_generated_image.*|[0-9a-f]{16,}.*|\d+)$')

# ------------------------------------------------------------------ conocimiento de los plugins
PT = P('papelator', 'tools')
PAPERS = tabla(os.path.join(PT, 'build_papers.py'), 'PAPERS')
try:
    PAPERS += tabla(os.path.join(PT, 'build_papers.py'), 'PAPERS2')
except KeyError:
    pass
TYPES = tabla(os.path.join(PT, 'build_surfaces.py'), 'TYPES', {'G_PARED': 'paredes', 'G_SUELO': 'suelos_y_piedra', 'G_METAL': 'metal'})
SNAMES = tabla(os.path.join(PT, 'build_surfaces.py'), 'NAMES')
BOARDS = tabla(os.path.join(PT, 'build_boards.py'), 'BOARDS', {'G': 'madera_y_carton', 'N': ''})
FAM = tabla(os.path.join(PT, 'build_overlays.py'), 'FAM')
ITEMS = tabla(os.path.join(PT, 'build_overlays.py'), 'ITEMS')
CATS = tabla(os.path.join(PT, 'build_imperf.py'), 'CATS')
NEW = tabla(os.path.join(PT, 'build_imperf2.py'), 'NEW')
GROUPS = tabla(os.path.join(PT, 'build_folds.py'), 'GROUPS')
IMP = dict(json.load(open(os.path.join(PT, 'indices', 'imp_index.json'))))
NIMP = dict(json.load(open(os.path.join(PT, 'indices', 'nimp_index.json'))))
FOLDS = json.load(open(os.path.join(PT, 'fold_sources.json')))
BSETS = json.load(open(os.path.join(PT, 'bordes_sets.json')))
AM_SOURCES = tabla(P('a-mano', 'tools', 'extract_textures.py'), 'SOURCES')
TZ_OVER = tabla(P('trazo', 'tools', 'build_assets.py'), 'OVERLAYS')

know = {}          # nombre de archivo (basename) o ruta relativa a papelator -> datos
def put(key, **kw):
    know.setdefault(key, {}).update({k: v for k, v in kw.items() if v is not None})

for p in PAPERS:
    pid, name, grp, f, kind, extra = p[:6]
    put('papelator/texturas_tileables/' + f, cat='tileables', sub='papel', id=pid, nombre=name, grupo_papelator=grp,
        tipo_papel=kind, mm=extra.get('mm'), periodo_mm=extra.get('px') or extra.get('py'), onda_mm=extra.get('flute'),
        usado_en='PAPELATOR (papers/%s)' % pid)
for tid, t in TYPES.items():
    grp, colorable, aparejo, docmm, disp, height, files = t
    for i, f in enumerate(files):
        put('papelator/NUEVAS SUPERFICIES/' + f, cat='tileables', sub='superficies', id='%s_%d' % (tid, i + 1),
            nombre='%s %d' % (SNAMES.get(tid, tid), i + 1), grupo=grp, colorable=colorable, aparejo=aparejo, mm=docmm,
            desplazamiento_mm=disp, relieve_mm=height, usado_en='PAPELATOR (%s_%d)' % (tid, i + 1))
for b in BOARDS:
    bid, name, grp, f, kind, extra, mat = b
    rot = f.startswith('ROT:')
    f = f.replace('ROT:', '')
    put('papelator/NUEVAS_NUEVAS/' + f, cat='tileables', sub='madera_y_carton', id=bid, nombre=name, material=mat,
        mm=extra.get('mm'), onda_mm=extra.get('flute'), girar=rot or None, usado_en='PAPELATOR (%s)' % bid)
for fam, files in ITEMS.items():
    for i, f in enumerate(files):
        put('papelator/SOBREPONER/' + f, cat='tileables', sub='vidrios_y_plasticos', id='%s_%d' % (fam, i + 1),
            nombre='%s %d' % (FAM[fam]['name'], i + 1), mm=FAM[fam].get('mm'), modo='trama',
            usado_en='PAPELATOR (Sobreponer › %s)' % FAM[fam]['name'])
for cid, C in CATS.items():
    for i in C['items']:
        if i in IMP:
            put('papelator/' + IMP[i], cat='imperfecciones', sub=cid, nombre=C['name'], modo_papelator=C['mode'],
                tipo=C['kind'], mm=C.get('size'), mm_fuente=C.get('src_mm'), donde=C.get('place'),
                usado_en='PAPELATOR (imperf › %s)' % cid)
for cid, C in NEW.items():
    for i in C['items']:
        if i in NIMP:
            put('papelator/' + NIMP[i], cat='imperfecciones', sub=cid, nombre=C['name'], modo_papelator=C['mode'],
                tipo=C['kind'], mm=C.get('size'), donde=C.get('place'), usado_en='PAPELATOR (imperf › %s)' % cid)
for g, idxs in GROUPS.items():
    for i in idxs:
        f = FOLDS.get(str(i))
        if f:
            put('papelator/' + f, cat='pliegues', sub=('%s_pliegues' % g) if g.isdigit() else g,
                usado_en='PAPELATOR (pliegues › %s)' % g)
for tipo, files in BSETS.items():
    if isinstance(files, list):
        for f in files:
            put('papelator/BORDES/' + f, cat='bordes', sub=tipo, usado_en='PAPELATOR (bordes › %s)' % tipo)
AMT = {'aguada': 'aguada', 'cera': 'cera', 'guache': 'gouache', 'oleo': 'oleo', 'lapiz': 'lapiz', 'carbon': 'carbon',
       'pincel': 'pincel', 'brocha': 'brocha', 'pincelfino': 'pincel_fino', 'gastado': 'rotulador_gastado',
       'rotu': 'rotulador', 'boli': 'boligrafo'}
am_pat = [(s[0], AMT.get(s[1], s[1])) for s in AM_SOURCES]
tz_over = {k: kind for kind, keys in TZ_OVER.items() for k in keys}

# 9:16 de Trazo: revisión a ojo de las hojas h062-h064 (índice de hoja -> subtipo)
V916 = {
 'h062': ['grunge_cuadricula', 'pintura_color', 'goteos', 'veta', 'grunge', 'grunge', 'veta', 'pintura_gris', 'grunge', 'pintura_gris',
          'pintura_color', 'pintura_color', 'pintura_color', 'pintura_gris', 'pintura_gris', 'pintura_gris', 'pintura_gris', 'goteos',
          'grafito', 'pintura_gris', 'grafito', 'grunge', 'pintura_color', 'pintura_color', 'pintura_color', 'pintura_gris', 'grafito',
          'pintura_gris', 'aguada', 'pintura_color', 'pintura_color', 'pintura_color', 'pintura_gris', 'pintura_gris', 'goteos', 'veta',
          'pintura_color', 'aguada', 'goteos', 'grunge_cuadricula'],
 'h063': ['grunge_cuadricula', 'pintura_gris', 'grunge', 'grafito', 'pintura_color', 'grunge', 'pintura_gris', 'pintura_color', 'aguada',
          'pintura_gris', 'pintura_color', 'pintura_color', 'pintura_color', 'pintura_color', 'grafito', 'pintura_gris', 'aguada', 'grafito',
          'pintura_color', 'pintura_gris', 'grunge', 'aguada', 'pintura_color', 'goteos', 'pintura_gris', 'ruido', 'grunge_cuadricula',
          'pintura_color', 'pintura_color', 'carbon', 'pintura_color', 'pintura_color', 'pintura_gris', 'aguada', 'pintura_gris', 'carbon',
          'grunge', 'grafito', 'goteos', 'pintura_color'],
 'h064': ['veta', 'pintura_gris', 'pintura_color', 'pintura_color', 'pintura_gris', 'veta', 'grunge', 'aguada', 'pintura_color',
          'pintura_color', 'pintura_color', 'pintura_color', 'aguada', 'aguada', 'aguada', 'aguada', 'aguada', 'aguada', 'aguada'],
}
IDXH_ = json.load(open(IDXH))
v916 = {}
for h, lst in V916.items():
    for i, s in enumerate(lst):
        v916[IDXH_['%s#%d' % (h, i)]] = s

# ------------------------------------------------------------------ reglas
def regla(x):
    r = x['ruta']; b = os.path.basename(r); stem = os.path.splitext(b)[0]; low = r.lower()
    k = dict(know.get(r, {}))
    if '/GUMROAD/' in r:
        return dict(metodo='omitir', motivo='fotogramas de las transiciones de Gumroad; ya están en vídeo')
    if r.startswith('neonizador/GOTAS/') or r.startswith('analog-fx-plugin/GOTAS/'):
        return dict(metodo='omitir', motivo='fuente del banco de goteos de Analog FX (se copia el banco ya procesado)')
    # --- trazos sueltos
    if r.startswith('a-mano/TRAZOS/'):
        rel = r[len('a-mano/TRAZOS/'):]
        tec = None
        for pat, t in am_pat:
            if fnmatch.fnmatch(rel, pat):
                tec = t; break
        if tec is None:
            l = rel.lower()
            tec = ('carbon' if 'carb' in l else 'lapiz' if 'grafito' in l else 'rotulador' if ('tinta' in l or 'marcador' in l or 'rotulador' in l)
                   else 'pincel_seco' if 'pincel seco' in l else 'cera' if rel.startswith('CERAS') else 'gouache' if rel.startswith('GUACHE')
                   else 'oleo' if rel.startswith('OLEO') else 'aguada' if rel.startswith('AGUADAS') else 'lapiz' if rel.startswith('LAPIZ')
                   else 'garabatos')
        if 'Composición minimalista' in rel or 'Gemini_Generated_Image_uy13' in rel or 'Gemini_Generated_Image_2tepo' in rel:
            tec = 'lapiz'
        if 'Gemini_Generated_Image_4k0x' in rel:
            tec = 'carbon'
        return dict(cat='trazos', sub=tec, metodo='papel_piezas', usado_en='A mano / Trazo (pinceladas reales)')
    if 'MANCHA CON  FORMA CONCRETA' in r or 'MANCHAS GRANDES' in r:
        return dict(cat='manchas', sub='pincel_grandes' if 'GRANDES' in r else 'pincel', metodo='papel_piezas',
                    usado_en='Trazo (manchas de óleo y gouache)')
    # --- tileables ya hechos (Substance) y 9:16
    if 'MATERIALE_TILEABLES' in r or 'TEXTURAS REALISTAS TILEABLES' in r:
        l = b.lower()
        sub = ('aguada' if 'acuarela' in l else 'pintura_calida' if 'calida' in l else 'pintura_fria' if 'fria' in l
               else 'pintura_gris' if 'grises' in l else 'pintura_gouache')
        return dict(cat='tileables', sub='pintura', variante=sub, metodo='tileable_verificar', usado_en='Trazo (frotados bajo óleo/gouache, acuarela)')
    if 'TEXTURAS EN 9-16' in r:
        sub = v916.get(r, 'otras')
        key = re.sub(r'Gemini_Generated_Image_', '', stem)[:4]
        return dict(cat='superposiciones', sub='9x16_' + sub, metodo='superposicion_y_tile',
                    usado_en=('Trazo (overlay %s)' % tz_over[key]) if key in tz_over else None)
    # --- PAPELATOR (con su tabla)
    if k.get('cat') == 'tileables':
        m = 'tileable_patron' if k.get('tipo_papel') == 'pattern' else 'tileable'
        return dict(metodo=m, **k)
    if k.get('cat') == 'imperfecciones':
        mode = k.get('modo_papelator')
        met = 'relieve' if mode in ('relief',) else 'papel_piezas' if k.get('tipo') == 'sprites' else 'papel_entera'
        if mode == 'hole': met = 'papel_entera'
        if k.get('tipo') == 'lines': met = 'relieve'
        return dict(metodo=met, **k)
    if k.get('cat') == 'pliegues':
        return dict(metodo='pliegue', **k)
    if r.startswith('papelator/NUEVAS/PLIEGUES'):
        return dict(cat='pliegues', sub='sin_clasificar', metodo='pliegue')
    if r.startswith('papelator/BORDES/'):
        sub = k.get('sub')
        return dict(cat='bordes', sub=sub or 'otros', metodo='croma', **{kk: v for kk, v in k.items() if kk not in ('cat', 'sub')})
    if r.startswith('papelator/imperfecciones/') or r.startswith('papelator/NUEVAS/TEXTURA_IMPERF'):
        return dict(cat='imperfecciones', sub='otras', metodo='papel_entera')
    if r.startswith('papelator/texturas_tileables/'):
        return dict(cat='tileables', sub='papel', metodo='tileable')
    if r.startswith('papelator/NUEVAS SUPERFICIES/'):
        return dict(cat='tileables', sub='superficies', metodo='tileable')
    if r.startswith('papelator/NUEVAS_NUEVAS/'):
        return dict(cat='tileables', sub='madera_y_carton', metodo='tileable')
    if r.startswith('papelator/SOBREPONER/'):
        return dict(cat='tileables', sub='vidrios_y_plasticos', metodo='tileable', modo='trama')
    # --- NEONIZADOR / Analog FX
    l = b.lower()
    if r.startswith('analog-fx-plugin/Tintas impresas/'):
        return dict(cat='tileables', sub='grunge', variante='tinta_impresa', metodo='tileable', modo='multiplicar',
                    usado_en='Analog FX (tintas impresas)')
    if 'chispa' in l or 'brizna' in l or 'brasas' in l:
        return dict(cat='luz_y_elementos', sub='chispas', metodo='negro_luz', modo='trama')
    if 'llama' in l or 'fuego' in l:
        return dict(cat='luz_y_elementos', sub='fuego', metodo='negro_luz', modo='trama')
    if 'humo' in l or 'vapor' in l:
        return dict(cat='luz_y_elementos', sub='humo', metodo='negro_luz', modo='trama')
    if 'fuga de luz' in l:
        return dict(cat='luz_y_elementos', sub='fugas_de_luz', metodo='negro_luz', modo='trama')
    if 'vhs' in l:
        return dict(cat='superposiciones', sub='vhs', metodo='negro_luz', modo='trama')
    if 'polvo' in l or 'arañazos' in l or 'película' in l:
        return dict(cat='superposiciones', sub='pelicula_polvo_y_rayas', metodo='negro_luz', modo='trama')
    if 'fotocopia' in l:
        return dict(cat='superposiciones', sub='fotocopia', metodo='superposicion_y_tile', modo='multiplicar')
    if 'quemad' in l:
        return dict(cat='imperfecciones', sub='quemadura_grande', metodo='papel_entera', modo='normal')
    if 'mancha de tinta' in l:
        return dict(cat='manchas', sub='tinta', metodo='papel_entera')
    if 'goteo' in l or 'gotas de pintura' in l:
        return dict(cat='manchas', sub='goteos_pintura_blanca', metodo='negro_objeto')
    if 'moho' in l or 'líquen' in l or 'liquen' in l:
        if 'textura' in l:
            return dict(cat='tileables', sub='naturaleza', variante='moho', metodo='tileable')
        return dict(cat='luz_y_elementos', sub='moho', metodo='negro_objeto')
    if 'mármol' in l or 'marmol' in l:
        return dict(cat='tileables', sub='liquidos', variante='marmol', metodo='tileable')
    if 'caústica' in l or 'reflejos de agua' in l or 'ondas' in l or 'agua ondulante' in l:
        return dict(cat='tileables', sub='liquidos', variante='agua', metodo='tileable')
    if ('espuma' in l and ('aguas oscuras' in l or 'agua oscura' in l or 'macro espuma' in l or 'primer plano' in l
                           or l.startswith('espuma de jabón'))) or 'burbujas sobre agua' in l:
        return dict(cat='tileables', sub='liquidos', variante='espuma', metodo='tileable')
    if 'burbuja' in l or 'espuma' in l:
        return dict(cat='luz_y_elementos', sub='burbujas_y_espuma', metodo='negro_luz', modo='trama')
    if 'horizonte' in l:
        return dict(cat='superposiciones', sub='degradados', metodo='superposicion')
    if 'papel acuarela' in l:
        return dict(cat='tileables', sub='papel', metodo='tileable')
    return dict(cat='sin_clasificar', sub='?', metodo='revisar')


def main():
    d = json.load(open(INV))
    sel = [x for x in d if x['rol'] == 'fuente' and x.get('tipo') == 'imagen' and x['canonico'] == x['ruta']
           and x.get('similar_a', x['ruta']) == x['ruta']]
    res = []
    for x in sorted(sel, key=lambda x: x['ruta']):
        c = regla(x)
        c['src'] = x['ruta']
        c['w'], c['h'] = x['w'], x['h']
        stem = os.path.splitext(os.path.basename(x['ruta']))[0]
        c['desc_origen'] = None if GEN.match(slug(stem) or '0') else re.sub(r'[-_ ]?\(?\d+\)?$', '', stem).strip()
        c['copias'] = [y['ruta'] for y in d if y.get('sha1') == x['sha1'] and y['ruta'] != x['ruta']] + \
                      [y['ruta'] for y in d if y.get('similar_a') == x['ruta'] and y['ruta'] != x['ruta']]
        res.append(c)
    json.dump(res, open(OUT, 'w'), ensure_ascii=False, indent=1)
    cnt = collections.Counter((c.get('cat', '-'), c.get('sub', '-'), c['metodo']) for c in res)
    for k, v in sorted(cnt.items(), key=lambda kv: (str(kv[0]))):
        print('%4d  %-18s %-28s %s' % (v, k[0], k[1], k[2]))
    print(len(res))


main()
