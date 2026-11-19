#!/usr/bin/env python3
"""Genera CATALOGO.md (para Iker) y estilos.json (para los plugins) a partir de catalogo.json.
uso: python3 generar_md.py <carpeta_con_catalogo.json>
"""
import json, re, sys, statistics
from pathlib import Path
from collections import Counter, defaultdict

D = Path(sys.argv[1])
cat = json.load(open(D / 'catalogo.json', encoding='utf-8'))
sys.path.insert(0, str(Path(__file__).parent))

CAT_NOMBRES = {
    '01_TRANSICIONES': 'Transiciones', '02_PELICULA': 'Película (grano, marcos, quemados)',
    '03_TEXTURAS_OVERLAYS': 'Texturas y overlays', '04_COLLAGE_MIXED_MEDIA': 'Collage / mixed media',
    '05_ANIMACIONES_ELEMENTOS': 'Animaciones y elementos', '06_PLANTILLAS': 'Plantillas', '07_SONIDO': 'Sonido',
}
ESTILOS_TXT = {
    'luz': 'Cortinillas de luz', 'collage': 'Collage', 'urbano': 'Urbano', 'tecnologico': 'Tecnológico',
    'cine': 'Cine / película', 'vintage': 'Vintage / analógico', 'glitch': 'Glitch', 'organico': 'Orgánico',
    'fondos': 'Fondos', 'grunge': 'Grunge', 'fuego': 'Fuego', 'impacto': 'Impacto',
}

def fmt_s(x):
    return '' if x is None else f'{x:.2f}'.rstrip('0').rstrip('.') + ' s'

activos = [e for e in cat if not e.get('copia_de_plantilla') and not any(
    k in e['ruta'].lower() for k in ('/tutorial', '_save 80%', 'troubleshooting', '/previews/'))]

L = []
L.append('# Biblioteca ACIDBITE · catálogo\n')
L.append('Generado automáticamente a partir del análisis de cada archivo (ffmpeg) y de lo que ACIDBITE indica en los '
         'nombres de archivo y en sus tutoriales. `catalogo.json` tiene todos los datos para los plugins; este documento '
         'es el resumen legible. Cómo aplica ACIDBITE cada pack: ver `COMO_LO_USA_ACIDBITE.md`.\n')
L.append('**Fuentes del modo de fusión:** «ACIDBITE (nombre del archivo)» > «ACIDBITE (tutorial)» > «deducido del análisis».\n')

# ---------------------------------------------------------------- resumen
t = Counter(e['tipo'] for e in activos)
L.append('## Resumen\n')
L.append('| Tipo | Archivos |\n|---|---|')
for k, v in t.most_common():
    L.append(f'| {k} | {v} |')
L.append('')
L.append('| Categoría | Packs | Vídeos | Sonidos |\n|---|---|---|---|')
by_cat = defaultdict(list)
for e in activos:
    by_cat[e['categoria']].append(e)
for c in sorted(by_cat):
    es = by_cat[c]
    L.append(f"| {CAT_NOMBRES.get(c, c)} | {len(set(e['pack'] for e in es))} | "
             f"{sum(1 for e in es if e['tipo'] == 'video')} | {sum(1 for e in es if e['tipo'] == 'audio')} |")
L.append('')

# ---------------------------------------------------------------- estilos
L.append('## Por estilo\n')
est = defaultdict(lambda: defaultdict(int))
for e in activos:
    for s in e.get('estilos', []):
        if e['tipo'] in ('video', 'imagen'):
            est[s][e['pack']] += 1
for s in sorted(est, key=lambda k: -sum(est[k].values())):
    packs = ', '.join(f'{p} ({n})' for p, n in sorted(est[s].items(), key=lambda x: -x[1]))
    L.append(f'- **{ESTILOS_TXT.get(s, s)}**: {packs}')
L.append('')

# ---------------------------------------------------------------- por pack
L.append('## Packs\n')
by_pack = defaultdict(list)
for e in activos:
    by_pack[(e['categoria'], e['pack'])].append(e)
for (c, p) in sorted(by_pack):
    es = by_pack[(c, p)]
    vids = [e for e in es if e['tipo'] == 'video']
    L.append(f'### {p}  ·  {CAT_NOMBRES.get(c, c)}\n')
    tipos = Counter(e['tipo'] for e in es)
    L.append('Archivos: ' + ', '.join(f'{v} {k}' for k, v in tipos.most_common()))
    if vids:
        res = Counter(f"{e['tecnico']['ancho']}×{e['tecnico']['alto']}" for e in vids if e.get('tecnico'))
        fps = Counter(e['tecnico']['fps'] for e in vids if e.get('tecnico') and e['tecnico'].get('fps'))
        alfa = sum(1 for e in vids if e.get('tecnico', {}).get('alfa'))
        durs = [e['tecnico']['duracion_s'] for e in vids if e.get('tecnico') and e['tecnico'].get('duracion_s')]
        codecs = Counter(f"{e['tecnico'].get('codec')} {e['tecnico'].get('perfil') or ''}".strip() for e in vids if e.get('tecnico'))
        L.append(f"Resolución: {', '.join(f'{k} ({v})' for k, v in res.most_common(3))} · "
                 f"fps: {', '.join(f'{k} ({v})' for k, v in fps.most_common(3))} · con alfa: {alfa}/{len(vids)} · "
                 f"duración: {fmt_s(min(durs)) if durs else ''}–{fmt_s(max(durs)) if durs else ''} "
                 f"(mediana {fmt_s(statistics.median(durs)) if durs else ''}) · códec: {', '.join(k for k, _ in codecs.most_common(2))}")
        comp = Counter(e.get('composicion') for e in vids if e.get('composicion'))
        col = Counter(e.get('colocacion_texto') for e in vids if e.get('colocacion_texto'))
        if comp:
            L.append('Modo de fusión: ' + ', '.join(f'{k} ({v})' for k, v in comp.most_common()))
        if col:
            L.append('Colocación: ' + ', '.join(f'{k} ({v})' for k, v in col.most_common()))
        um = Counter(m for e in vids for m in e.get('modos_usados_por_acidbite', []))
        if um:
            L.append('En sus proyectos de Premiere ACIDBITE usa: ' + ', '.join(f'{k} ({v})' for k, v in um.most_common()))
        notas = Counter(n for e in vids for n in e.get('notas', []) if n.startswith('ACIDBITE (tutorial)'))
        for n, _ in notas.most_common(3):
            L.append(f'> {n}')
    L.append('')
    if vids:
        L.append('| Clip | Dur. | Modo | Colocación | Corte / cubre | Vel. | Color | SFX |\n|---|---|---|---|---|---|---|---|')
        idx = {x['id']: x for x in cat}
        for e in sorted(vids, key=lambda x: x['ruta']):
            tr = e.get('transicion', {})
            if tr.get('tipo') == 'mascara':
                corte = f"entra con el clip · revelado {fmt_s(tr.get('revelado_completo_s'))}" + (' · Reverse' if tr.get('invertir') else '')
            elif tr.get('tipo') == 'recorte':
                corte = 'recorte (forma fija)'
            elif tr.get('tipo') == 'intercalado':
                corte = 'entero, entre planos'
            else:
                corte = fmt_s(tr.get('corte_recomendado_s'))
                if tr.get('corte_acidbite_s') is not None:
                    corte += ' (ACIDBITE)'
                if tr.get('cubre_desde_s') is not None:
                    corte += f" (tapa {fmt_s(tr['cubre_desde_s'])}–{fmt_s(tr['cubre_hasta_s'])})"
            if e.get('tecnico', {}).get('audio_incrustado'):
                sfx = 'dentro'
            elif e.get('sfx_acidbite'):
                sfx = ' + '.join(e['sfx_acidbite']) + ' (ACIDBITE)'
            elif e.get('sfx') in idx:
                sfx = Path(idx[e['sfx']]['ruta']).name + (' ⇄' if e.get('sfx_por_nombre') else '')
            elif e.get('sfx_sugeridos'):
                sfx = 'familia: ' + re.sub(r'[_ ]?\d+$', '', Path(idx[e['sfx_sugeridos'][0]]['ruta']).stem) + f" ({len(e['sfx_sugeridos'])})"
            else:
                sfx = ''
            nombre = '/'.join(Path(e['ruta']).parts[2:])[-60:]
            L.append(f"| {nombre} | {fmt_s(e.get('tecnico', {}).get('duracion_s'))} | {e.get('composicion', '')}{(' ⚠ mejor ' + e['composicion_recomendada']) if e.get('composicion_recomendada') else ''} | "
                     f"{e.get('colocacion', '')} | {corte} | {e.get('velocidad', '')} | {e.get('color', {}).get('color', '')} | {sfx} |")
        L.append('')
    auds = [e for e in es if e['tipo'] == 'audio']
    if auds:
        cs = Counter(e.get('categoria_sonido') or e.get('envolvente', {}).get('forma') or '—' for e in auds)
        L.append('Sonidos: ' + ', '.join(f'{k} ({v})' for k, v in cs.most_common()))
        L.append('')
    luts = [e for e in es if e['tipo'] == 'lut']
    if luts:
        cams = Counter(e['lut'].get('camara_entrada') or '—' for e in luts)
        var = Counter(f"{e['lut']['tipo']} / {e['lut']['variante']}" for e in luts)
        L.append('LUTs: ' + ', '.join(f'{k} ({v})' for k, v in var.most_common()) + '. Cámaras: ' +
                 ', '.join(k for k in cams))
        L.append('')
    pls = [e for e in es if e['tipo'] == 'plantilla']
    if pls:
        L.append('Plantillas: ' + ', '.join(f"{Path(e['ruta']).name} ({e.get('programa', '')})" for e in pls[:12]) +
                 (' …' if len(pls) > 12 else ''))
        L.append('')

PL = D / 'plantillas_acidbite.json'
RECETAS = {}
if PL.exists():
    plant = json.loads(PL.read_text(encoding='utf-8'))
    L.append('## Recetas exactas sacadas de los proyectos de Premiere de ACIDBITE\n')
    L.append('Leídas directamente de sus `.prproj` (pista, tiempos, modo de fusión y efectos). «mate» = copia usada como '
             'Track Matte del plano; «visible» = copia que se ve encima. Los tiempos son de su línea de tiempo.\n')
    for proy, seqs in plant.items():
        L.append(f'### {proy}\n')
        for sn, sq in seqs.items():
            capas = sorted(sq['capas'], key=lambda c: (-c['pista'], c['inicio_s']))
            L.append(f"**{sn}**" + (f" · corte (entra el plano 2) a {fmt_s(sq['corte_s'])}" if sq.get('corte_s') is not None else ''))
            L.append('')
            rec = []
            for c in capas:
                extra = []
                if c.get('rol'): extra.append(c['rol'].split(' (')[0])
                if c['efectos']: extra.append(', '.join(c['efectos']))
                if c['opacidad'] != 100: extra.append(f"opacidad {c['opacidad']:.0f} %")
                L.append(f"- V{c['pista']} · {fmt_s(c['inicio_s'])}–{fmt_s(c['fin_s'])} · {c['clip']} · **{c['modo']}**" + (f" · {'; '.join(extra)}" if extra else ''))
                rec.append(dict(pista=c['pista'], desde_s=c['inicio_s'], hasta_s=c['fin_s'], clip=c['clip'], modo=c['modo'],
                                rol=c.get('rol'), efectos=c['efectos'], opacidad=c['opacidad']))
            L.append('')
            RECETAS[f'{proy} · {sn}'] = dict(corte_s=sq.get('corte_s'), capas=rec)
(D / 'CATALOGO.md').write_text('\n'.join(L), encoding='utf-8')

# ---------------------------------------------------------------- estilos.json para los plugins
ESTILOS = {
    'cortinillas_de_luz': dict(
        descripcion='Transiciones con luz: destellos, quemados, leaks y refracciones encima del corte.',
        packs=['Light Transitions', 'Wipe and Light Transitions', 'Film Burns', 'Film Leaks', 'Optical Elements', 'CRT Elements'],
        colocacion=['encima_corte', 'intercalado'], modos=['screen', 'add (linear dodge)'],
        reglas=['Pico de brillo sobre el corte', 'SFX alineado al pico', 'Recolorear al color del neón (Hue)']),
    'collage': dict(
        descripcion='Papel, cinta, rasgados, marcos y recortes; ritmo a saltos.',
        packs=['Ultimate Paper Pack', 'Super Mixed Media Pack', 'Textile Transitions', 'Punch Hole Transitions',
               'Animated Markers', 'Cinemarkers', 'Cinemarkers 2', 'Dissected Textures', 'Burning Paper Transitions'],
        colocacion=['mascara', 'encima_corte', 'elemento', 'look'], modos=['normal', 'mate alfa (Track Matte)', 'multiply', 'screen'],
        reglas=['Máscara alfa + copia visible del borde', 'Conformar a 12 u 8 fps', 'Texturas de papel en Multiply todo el plano']),
    'urbano': dict(
        descripcion='Grunge, cristal roto, sonido de calle, rotulador.',
        packs=['Dissected Textures', 'Cracked Glass Transitions', 'DynamiXXX', 'Animated Markers', 'Urban SFX'],
        colocacion=['encima_corte', 'mascara', 'elemento'], modos=['difference', 'overlay', 'mate alfa (Track Matte)'],
        reglas=['Golpes de textura < 1 s sobre el corte', 'Hits y metal de Urban SFX en el corte']),
    'tecnologico': dict(
        descripcion='CRT, VHS, glitch, túneles, datamosh, visores.',
        packs=['CRT Elements', 'Analog Video Package', 'Cyber Transitions', 'Pre-Built VHS Transitions', 'Tunnel Transitions',
               'Morpheus', 'Viewfinders Plus', 'Dystopia SFX'],
        colocacion=['intercalado', 'encima_corte', 'look'], modos=['normal', 'screen', 'overlay'],
        reglas=['Ruido/rejilla CRT en Overlay todo el plano', 'Glitch intercalado ≈1 s', 'Glitch SFX de Dystopia']),
    'cine': dict(
        descripcion='Emulación de película: grano, gate, perforaciones, quemados, LUT.',
        packs=['35mm Package', '16mm Package', 'Super 8 Package', 'Film Burns', 'Film Leaks', 'Cine Snip Transitions',
               'Cinemarkers', 'Cinemarkers 2'],
        colocacion=['look', 'encima_corte'], modos=['overlay', 'multiply', 'screen', 'mate alfa (Track Matte)'],
        reglas=['Pila: metraje+LUT → grano Overlay → gate → perforación Screen → quemado Screen en el corte',
                'Proyecto a 24 fps', 'LUT según el LOG de la cámara']),
}
ESTILOS['tecnologico']['reglas'].append('Look analógico de ACIDBITE (Analog Video Look.prproj): metraje x3 en Linear Dodge, capa de ajuste al 50 % en Color Dodge con Gaussian Blur, Wave Warp + Color Emboss + Motion Blur, y la máscara 1,85→1,33 encima')
ESTILOS['tecnologico']['reglas'].append('VHS de ACIDBITE: transición en Screen (la 04 en Overlay) con Shadow Mask.png y Scanlines.png encima y Wave Warp en los planos; corte a 0,13–0,79 s del inicio del clip según la transición')
ESTILOS['collage']['reglas'].append('Textile/Punch Hole de ACIDBITE: Track Matte Key Matte Alpha con copia del frame debajo y otra visible encima (Screen, Lighten, Difference o Linear Dodge)')
salida = dict(estilos=ESTILOS, recetas_acidbite=RECETAS)
json.dump(salida, open(D / 'estilos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('CATALOGO.md:', len(L), 'líneas · estilos:', len(ESTILOS))
