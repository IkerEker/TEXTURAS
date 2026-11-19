"""Índice único del atlas: TEXTURAS (tx:), AcidBite (ab:) y originales de plugins (or:).
Uso (desde la raíz de TEXTURAS): python3 tools/atlas/construir_indice.py
Escribe indice/indice.json. Rutas `archivo` relativas a Biblioteca/ (= TEXTURAS_ROOT)."""
import json, hashlib, os, re, collections
from pathlib import Path

MODO = [  # (patrón, clave común)
    (r'm[aá]scara de lum|mate de luma|luma matte', 'mascara_luma'), (r'mate alfa|matte alpha', 'mascara_alfa'),
    (r'^normal \(alfa\)', 'normal'), (r'multipl|multiply', 'multiplicar'), (r'trama|screen', 'trama'),
    (r'superponer|overlay', 'superponer'), (r'luz suave|soft light', 'luz_suave'), (r'hard light|luz fuerte', 'luz_fuerte'),
    (r'diferencia|difference', 'diferencia'), (r'pin light|luz focal', 'luz_focal'),
    (r'linear dodge|\badd\b|sobreexponer lineal', 'sobreexponer_lineal'), (r'color dodge|sobreexponer color', 'sobreexponer_color'),
    (r'lighter color', 'color_mas_claro'), (r'lighten|aclarar', 'aclarar'), (r'^normal', 'normal')]


def modo_comun(t):
    t = (t or '').lower()
    for rx, k in MODO:
        if re.search(rx, t):
            return k
    return None


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


T = Path('.')
inv = json.load(open('tools/estado/inv2.json'))
md5inv = json.load(open('tools/estado/md5_inventario.json'))
man = json.load(open('originales/MANIFIESTO.json'))
ruta2or = {}
for g in man['originales']:
    for r in g['rutas']:
        ruta2or[r] = g['id']
for h in man['heredado_neonizador']:
    ruta2or[h['ruta_en_repo']] = h['id']

idx = []
# ---------------------------------------------------------------- TEXTURAS
tx = json.load(open('catalogo.json'))['items']
deriv = collections.defaultdict(list)
for e in tx:
    f = T / e['archivo']
    o = e.get('origen') or {}
    org = ruta2or.get(o.get('ruta')) or next((ruta2or[c] for c in (o.get('copias') or []) if c in ruta2or), None)
    a = dict(id='tx:' + e['id'], coleccion='TEXTURAS', archivo='TEXTURAS/' + e['archivo'], tipo=e['tipo'],
             clase=e['cat'], sub=e['sub'], desc=e.get('desc'), md5=md5f(f) if f.exists() else None,
             w=e.get('w'), h=e.get('h'), alfa=e.get('alfa'),
             fondo=e.get('fondo') or e.get('fondo_original') or ('transparente' if e.get('alfa') else None),
             tileable=bool(e.get('tileable')), modo=modo_comun(e.get('modo')), modo_texto=e.get('modo'),
             modo_fuente='TEXTURAS', color=e.get('color'), color_medio=e.get('color_medio'),
             origen=org, origen_ruta=o.get('ruta'), metodo=e.get('metodo'), usado_por=e.get('usado_en'),
             licencia='Gumroad: uso propio, no redistribuir' if 'gumroad' in json.dumps(e).lower() else 'propio')
    if e.get('tile_mm'):
        a['tile_mm'] = e['tile_mm']; a['mm_por_px'] = e.get('mm_por_px')
        if e.get('mm_por_px'): a['ancho_real_mm'] = round(e['w'] * e['mm_por_px'], 2)
    if e.get('tamano_real_mm'): a['tamano_real_mm'] = e['tamano_real_mm']
    if e.get('costura') is not None: a['costura'] = e['costura']
    if e.get('aviso'): a['aviso'] = e['aviso']
    for k in ('recorte', 'pieza', 'piezas', 'pareja', 'medidas', 'relieve_mm', 'desplazamiento_mm', 'aparejo'):
        if e.get(k) is not None: a[k] = e[k]
    if re.search(r'relieve|pliegue', e['archivo']) or e['cat'] == 'pliegues' or 'vidrios' in e['sub']:
        a['desplazamiento'] = 'gris 128 = neutro' if e['cat'] in ('pliegues',) or 'relieve' in e['archivo'] else 'gradiente de la foto (como NEONIZADOR)'
    if e['tipo'] == 'video':
        a['video'] = dict(fps=e.get('fps'), fps_efectivo=e.get('fps_efectivo'), a_saltos=e.get('a_saltos'),
                          duracion=e.get('duracion'), fotogramas=e.get('frames'), alfa=e.get('alfa'),
                          fondo=e.get('fondo'), loop=e.get('loop'), velocidad=e.get('velocidad'),
                          comportamiento=e.get('comportamiento'),
                          version_loop=(e.get('version_loop') or {}).get('archivo'))
        a['tira'] = e.get('tira'); a['procedencia'] = e.get('procedencia')
        tr = e.get('transicion')
        if tr:
            a['transicion'] = dict(tipo='mascara', cubre_s=tr.get('cubre_total_s'), revelado_s=tr.get('cubre_total_s'),
                                   descubre_desde_s=tr.get('descubre_desde_s'), empieza=tr.get('empieza'),
                                   acaba=tr.get('acaba'), criterio='medido por TEXTURAS (tinta cubre y descubre)',
                                   fuente='TEXTURAS')
        a['audio'] = dict(incrustado=False)
    a['hoja'] = 'TEXTURAS/hojas/' + e['carpeta'].replace('/', '__') + '.jpg'
    if org: deriv[org].append(a['id'])
    idx.append({k: v for k, v in a.items() if v is not None})

# ---------------------------------------------------------------- originales
for g in man['originales']:
    idx.append(dict(id=g['id'], coleccion='originales', archivo=g['archivo'], tipo=g['tipo'], md5=g['md5'],
                    w=g.get('w'), h=g.get('h'), bytes=g['bytes'], rutas_antiguas=g['rutas'],
                    productos=deriv.get(g['id'], [])))
for h in man['heredado_neonizador']:
    idx.append(dict(id=h['id'], coleccion='originales', sub='heredado/neonizador', archivo=h['archivo'], md5=h['md5'],
                    bytes=h['bytes'], rutas_antiguas=[h['ruta_en_repo']],
                    nota='JPG re-guardado o recorte de NEONIZADOR: se conserva para que su plugin/tex salga igual'))

# ---------------------------------------------------------------- AcidBite
PACK = {
    'Light Transitions': ('video', 'transiciones/luz'), 'Wipe and Light Transitions': ('video', 'transiciones/barrido_luz'),
    'Burning Paper Transitions': ('video', 'transiciones/papel_quemado'), 'Cine Snip Transitions': ('video', 'transiciones/tira_pelicula'),
    'Cracked Glass Transitions': ('video', 'transiciones/cristal_roto'), 'Cyber Transitions': ('video', 'transiciones/glitch'),
    'Pre-Built VHS Transitions': ('video', 'transiciones/vhs'), 'Punch Hole Transitions': ('video', 'transiciones/agujero'),
    'Textile Transitions': ('video', 'transiciones/tela'), 'Tunnel Transitions': ('video', 'transiciones/tunel'),
    '16mm Package': ('video', 'pelicula/16mm'), '35mm Package': ('video', 'pelicula/35mm'), 'Super 8 Package': ('video', 'pelicula/super8'),
    'Film Burns': ('video', 'pelicula/quemados'), 'Film Leaks': ('video', 'pelicula/fugas_de_luz'), 'Viewfinders Plus': ('video', 'pelicula/visores'),
    'Analog Video Package': ('video', 'analogico/video'), 'CRT Elements': ('video', 'analogico/crt'),
    'Dissected Textures': ('video', 'texturas_animadas/grunge'), 'DynamiXXX': ('video', 'texturas_animadas/golpes'),
    'Optical Elements': ('video', 'elementos/refracciones'), 'Super Mixed Media Pack': ('video', 'collage/mixed_media'),
    'Ultimate Paper Pack': ('video', 'collage/papel'), 'Abstracts': ('video', 'fondos/abstractos'), 'Liquids': ('video', 'fondos/liquidos'),
    'Animated Markers': ('video', 'elementos/marcadores'), 'Cinemarkers': ('video', 'elementos/cinemarkers'),
    'Cinemarkers 2': ('video', 'elementos/cinemarkers'), 'Morpheus': ('plantilla', 'morpheus')}
IMG = [(r'Toolkit/Tape', 'imperfecciones', 'cinta_adhesiva'), (r'Toolkit/Textures', 'pliegues', 'hoja_4k'),
       (r'Toolkit/Ink', 'trazos', 'tinta_anotacion'), (r'Toolkit/Marker', 'trazos', 'rotulador_anotacion'),
       (r'Noise Textures', 'desplazamiento', 'ruido'), (r'Shadow Mask|Scanlines', 'superposiciones', 'crt'),
       (r'Mask 1,85', 'superposiciones', 'mascara_formato'), (r'Viewfinders Plus/Assets/PNG', 'superposiciones', 'visores'),
       (r'DIY Still', 'superposiciones', 'visor_camara'), (r'Punch Hole Transitions/Assets/Toolkit|Cinemarkers/Assets/Stills', 'mascaras', 'agujero'),
       (r'Film Gates', 'superposiciones', 'ventanilla'), (r'heavy dust', 'superposiciones', 'pelicula_polvo_y_rayas'),
       (r'Textile', 'superposiciones', 'tela'), (r'Morpheus', 'plantilla', 'morpheus')]
ab = json.load(open('acidbite/datos/catalogo.json'))
abid = {e['id']: e for e in ab}
for e in ab:
    if e.get('copia_de_plantilla') or e['tipo'] in ('doc', 'preview', 'metraje_demo'):
        continue
    clase, sub = PACK.get(e['pack'], ('otros', e['pack']))
    if e['tipo'] == 'imagen':
        clase, sub = next(((c, s) for rx, c, s in IMG if re.search(rx, e['ruta'])), ('superposiciones', 'acidbite'))
    elif e['tipo'] == 'audio':
        clase, sub = 'sonido', (e.get('categoria_sonido') or 'otros').replace(' ', '_')
    elif e['tipo'] == 'lut':
        clase, sub = 'lut', (e.get('lut') or {}).get('camara_entrada') or 'general'
    elif e['tipo'] == 'tutorial':
        clase, sub = 'tutorial', e['pack']
    elif e['tipo'] == 'plantilla':
        clase, sub = 'plantilla', e['pack']
    t = e.get('tecnico', {})
    modo_t = e.get('composicion_recomendada') or e.get('composicion')
    a = dict(id='ab:' + e['id'], coleccion='ACIDBITE', pack=e['pack'], archivo='ACIDBITE/' + e['ruta'], tipo=e['tipo'],
             clase=clase, sub=sub, w=t.get('ancho'), h=t.get('alto'), alfa=t.get('alfa'), bytes=e['bytes'],
             modo=modo_comun(modo_t), modo_texto=modo_t,
             modo_fuente=(e.get('composicion_recomendada_fuente') if e.get('composicion_recomendada') else e.get('composicion_fuente')),
             modos_acidbite=e.get('modos_usados_por_acidbite'), colocacion=e.get('colocacion'), estilos=e.get('estilos'),
             color=(e.get('color') or {}).get('color'), aspecto=e.get('aspecto'), notas=e.get('notas'),
             licencia='ACIDBITE: pago, uso propio, no redistribuir', hoja='TEXTURAS/acidbite/hojas/' + e['id'] + '.jpg')
    if e['tipo'] == 'video':
        a['video'] = dict(fps=t.get('fps'), duracion=t.get('duracion_s'), fotogramas=t.get('fotogramas'),
                          alfa=t.get('alfa'), codec=f"{t.get('codec')} {t.get('perfil') or ''}".strip(),
                          velocidad=e.get('velocidad'), retiming=e.get('retiming'), loop=False)
        tr = e.get('transicion')
        if tr:
            a['transicion'] = dict(tipo=tr.get('tipo'), corte_s=tr.get('corte_recomendado_s'),
                                   cubre_s=[tr['cubre_desde_s'], tr['cubre_hasta_s']] if 'cubre_desde_s' in tr else None,
                                   efecto_s=[tr['efecto_desde_s'], tr['efecto_hasta_s']] if tr.get('efecto_desde_s') is not None else None,
                                   revelado_s=tr.get('revelado_completo_s'), invertir=tr.get('invertir'),
                                   criterio=tr.get('criterio'), fuente=tr.get('invertir_fuente') or ('ACIDBITE (plantilla)' if tr.get('corte_acidbite_s') is not None else 'medido'),
                                   nota=tr.get('nota'))
            a['transicion'] = {k: v for k, v in a['transicion'].items() if v is not None}
        au = dict(incrustado=t.get('audio_incrustado'))
        if e.get('sfx'): au['sfx'] = ['ab:' + e['sfx']]
        if e.get('sfx_acidbite'): au['sfx_acidbite'] = e['sfx_acidbite']
        if e.get('sfx_sugeridos'): au['sfx_familia'] = ['ab:' + x for x in e['sfx_sugeridos']]
        if e.get('sfx_confianza'): au['confianza'] = e['sfx_confianza']
        a['audio'] = au
        if e.get('combinado_por_acidbite'): a['conjuntos'] = e['combinado_por_acidbite']
    if e['tipo'] == 'audio':
        a['audio'] = dict(duracion=t.get('duracion_s'), envolvente=e.get('envolvente'),
                          clips=['ab:' + x for x in e.get('clips', [])])
    if e['tipo'] == 'lut': a['lut'] = e.get('lut')
    if e['tipo'] == 'plantilla': a['programa'] = e.get('programa')
    if clase == 'desplazamiento': a['desplazamiento'] = 'ruido gris (Morpheus SelfDisplace)'
    if sub == 'hoja_4k': a['desplazamiento'] = 'pliegues/arrugas en gris (Multiply)'
    idx.append({k: v for k, v in a.items() if v is not None})

os.makedirs('indice', exist_ok=True)
out = dict(version='2026-11-19', raiz='Biblioteca/ (variable TEXTURAS_ROOT)', total=len(idx),
           por_coleccion=dict(collections.Counter(a['coleccion'] for a in idx)),
           por_clase=dict(collections.Counter(a.get('clase', '—') for a in idx)), assets=idx)
json.dump(out, open('indice/indice.json', 'w'), ensure_ascii=False, indent=0)
print(out['total'], out['por_coleccion'])
print(sorted(out['por_clase'].items(), key=lambda x: -x[1]))
