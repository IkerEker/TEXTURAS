#!/usr/bin/env python3
"""ACIDBITE · convierte el análisis de ffmpeg (_ANALISIS) en catalogo.json + CATALOGO.md.

uso: python3 catalogar.py <carpeta_analisis_descomprimida> <carpeta_salida>
"""
import csv, json, re, sys, math, statistics
from pathlib import Path
from collections import defaultdict, Counter

try:
    from PIL import Image
except ImportError:
    Image = None

ANA = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------- lo que dice ACIDBITE de cada pack
PACKS = {
    'Burning Paper Transitions': dict(estilos=['collage', 'vintage', 'fuego'], acidbite='24 transiciones pre-keyed hechas con fuego real; estilos central y lateral.'),
    'Cine Snip Transitions':     dict(estilos=['cine', 'collage', 'vintage'], acidbite='96 escaneos de tira de película para transiciones analógicas.'),
    'Cracked Glass Transitions': dict(estilos=['urbano', 'impacto'], acidbite='17 transiciones pre-keyed de cristal roto.'),
    'Cyber Transitions':         dict(estilos=['tecnologico', 'glitch'], acidbite='48 transiciones de glitch analógico.'),
    'Light Transitions':         dict(estilos=['luz'], acidbite='100+ transiciones de luz con obturador lento, graded y ungraded, con SFX.'),
    'Wipe and Light Transitions':dict(estilos=['luz'], acidbite='Transiciones de barrido y luz con obturador lento.'),
    'Pre-Built VHS Transitions': dict(estilos=['tecnologico', 'vintage', 'glitch'], acidbite='9 transiciones de salto de fotograma prehechas (Premiere, AE, Resolve, FCPX).'),
    'Punch Hole Transitions':    dict(estilos=['collage', 'cine'], acidbite='Perforaciones pre-keyed: transiciones u overlays que ocultan parte de la imagen; 7 prehechas.'),
    'Textile Transitions':       dict(estilos=['collage', 'organico'], acidbite='Transiciones hechas con tejidos.'),
    'Tunnel Transitions':        dict(estilos=['tecnologico', 'luz'], acidbite='Túneles animados con SFX.'),
    'Dissected Textures':        dict(estilos=['urbano', 'grunge'], acidbite='30 overlays grunge: papel, metal, cuero, óxido, arañazos.'),
    'CRT Elements':              dict(estilos=['tecnologico', 'vintage'], acidbite='260+ texturas de vídeo vintage: flares, flashes (transiciones de luma), glitches, texturas, wipes; LUTs flat-look.'),
    'Analog Video Package':      dict(estilos=['tecnologico', 'vintage', 'glitch'], acidbite='50+ estáticos, glitches, visores y preroll de cámaras y VCR.'),
    'Optical Elements':          dict(estilos=['luz', 'organico'], acidbite='68 refracciones ópticas de cristal real: Subtle, Medium, Hard (también transición) y Particles.'),
    'DynamiXXX':                 dict(estilos=['urbano', 'vintage'], acidbite='65 texturas y transiciones analógicas.'),
    'Super Mixed Media Pack':    dict(estilos=['collage'], acidbite='Transiciones alfa, marcos, arañazos, texturas de impreso/escaneado y overlays; prehechas para Premiere/FCPX/Resolve.'),
    'Ultimate Paper Pack':       dict(estilos=['collage'], acidbite='27 transiciones pre-keyed de rasgado/arrugado, collages, texturas de papel, elementos (cinta, garabatos, tinta).'),
    'Abstracts':                 dict(estilos=['organico', 'fondos'], acidbite='16 bucles de animación 4K.'),
    'Liquids':                   dict(estilos=['organico', 'fondos'], acidbite='14 bucles de animación 4K.'),
    'Animated Markers':          dict(estilos=['collage', 'urbano'], acidbite='300+ animaciones de rotulador.'),
    'Cinemarkers':               dict(estilos=['cine', 'collage'], acidbite='50+ animaciones de marcas de película con SFX.'),
    'Cinemarkers 2':             dict(estilos=['cine', 'collage'], acidbite='105 animaciones de película real: transiciones, marcas, perforaciones, texturas, SFX.'),
    '16mm Package':              dict(estilos=['cine', 'vintage'], acidbite='Granos, quemados, marcos (gates), suciedad y LUTs de 16mm.'),
    '35mm Package':              dict(estilos=['cine', 'vintage'], acidbite='Granos en bucle, 8 gates pre-keyed (16:9 y panorámico), 42 quemados/leaks, texturas, LUTs, SFX.'),
    'Super 8 Package':           dict(estilos=['cine', 'vintage'], acidbite='Granos 8mm, quemados, LUTs, perforaciones, polvo.'),
    'Film Burns':                dict(estilos=['luz', 'cine', 'vintage'], acidbite='33 quemados en Kodak 8mm; como textura o transición: cortar en el momento más brillante.'),
    'Film Leaks':                dict(estilos=['luz', 'cine'], acidbite='34 leaks: transiciones, texturas u overlays ondulados de color.'),
    'Viewfinders Plus':          dict(estilos=['cine', 'tecnologico'], acidbite='Visores de cámara limpio, 16mm y CRT, en 16:9 y panorámico.'),
    'Morpheus':                  dict(estilos=['tecnologico', 'glitch'], acidbite='Plantillas MOGRT/Motion de transiciones glitch + 16 noise plates.'),
    'Dystopia SFX':              dict(estilos=['tecnologico', 'urbano'], acidbite='Pack de efectos de sonido.'),
    'Elements SFX':              dict(estilos=[], acidbite='145+ efectos de sonido.'),
    'Urban SFX':                 dict(estilos=['urbano'], acidbite='140 efectos de sonido urbanos.'),
}


# ----------------------------------------------------------------- reglas sacadas de los tutoriales de ACIDBITE
# (pack, palabra en la ruta) -> colocación, modo por defecto si el nombre no lo dice, nota
COLOCACIONES = {
    'look': 'Capa de look durante todo el plano',
    'encima_corte': 'Encima del corte, unos fotogramas',
    'intercalado': 'Plano intercalado entre los dos planos (misma pista)',
    'mascara': 'Máscara (Track Matte) para que el plano entrante aparezca dentro de la forma',
    'elemento': 'Elemento colocado sobre el plano (escalar/girar/posicionar)',
    'fondo': 'Fondo o plano completo',
    'plantilla': 'Plantilla: se sustituyen los planos dentro',
}
REGLAS = [
    # pack, regex sobre la ruta (minúsculas), colocación, modo por defecto, nota
    ('Burning Paper Transitions', r'luma matte', 'mascara', 'mate de luma', 'Máscara de luma de la transición del mismo número; activar Reverse según el sentido.'),
    ('Burning Paper Transitions', r'burning paper \d+', 'encima_corte', 'screen', 'Fuego visible en Screen encima de la máscara; recolorear con Hue vs Hue.'),
    ('Cracked Glass Transitions', r'cracked glass transition', 'mascara', 'mate alfa', 'Track Matte Alpha del plano entrante; los trozos lo revelan.'),
    ('Cine Snip Transitions', r'.', 'encima_corte', 'normal', 'Tira de película 4:3 centrada sobre el corte; probar Screen o Difference.'),
    ('Cyber Transitions', r'/noise/', 'look', 'screen', 'Ruido CRT encima.'),
    ('Cyber Transitions', r'.', 'intercalado', 'normal', 'Glitch a pantalla completa entre los dos planos (≈1 s).'),
    ('Light Transitions', r'.', 'encima_corte', 'screen', 'Encima del corte; recolorear con Color Balance (HLS) → Hue. Pyro también en Difference.'),
    ('Wipe and Light Transitions', r'.', 'intercalado', 'normal', 'Entre los dos planos con fundidos de opacidad en los bordes.'),
    ('Tunnel Transitions', r'.', 'encima_corte', 'normal', 'En V2 en Normal (tiene alfa: transparente al principio y al final). Match cut: zoom hacia un punto del plano y entrar en el túnel; Lens Distortion en el plano saliente.'),
    ('Pre-Built VHS Transitions', r'glitch textures', 'encima_corte', 'screen', 'Encima del corte (modo en el sufijo).'),
    ('Pre-Built VHS Transitions', r'overlays/', 'look', 'normal', 'Scanlines / Shadow Mask / máscara 4:3 encima.'),
    ('Punch Hole Transitions', r'key-transitions', 'mascara', 'screen', 'Dos copias: una en Screen (borde) y otra como Track Matte del plano entrante.'),
    ('Punch Hole Transitions', r'filmburn', 'encima_corte', 'screen', 'Quemado encima del corte.'),
    ('Punch Hole Transitions', r'toolkit/', 'mascara', 'mate alfa', 'Máscara fija (maskinside / maskout).'),
    ('Punch Hole Transitions', r'overlays/', 'encima_corte', None, 'Overlay (modo en el sufijo).'),
    ('Textile Transitions', r'textile frames/transition frames', 'mascara', 'mate alfa', 'Dos telas que se cruzan; el plano entrante dentro del hueco.'),
    ('Textile Transitions', r'textile frames/', 'elemento', 'mate alfa', 'Marco de tela: escalar/girar para enmarcar; Track Matte Alpha.'),
    ('Textile Transitions', r'grunge textures', 'encima_corte', 'screen', 'Grunge sobre negro encima del corte.'),
    ('Textile Transitions', r'textile textures|paper textures', 'encima_corte', 'multiply', 'Textura de tela/papel.'),
    ('Dissected Textures', r'alpha', 'mascara', 'mate alfa', 'Forma recortada: el plano se ve dentro (collage).'),
    ('Dissected Textures', r'.', 'encima_corte', None, 'Golpe de textura ≈1 s encima del corte; probar Difference / Overlay / Hard Light.'),
    ('DynamiXXX', r'.', 'encima_corte', 'difference', 'Ráfaga analógica < 1 s; Screen o Difference; se apilan 2–3.'),
    ('CRT Elements', r'/dirt/', 'look', 'overlay', 'Rejilla CRT en Overlay durante todo el plano.'),
    ('CRT Elements', r'glitch', 'encima_corte', 'screen', 'Glitch encima del corte.'),
    ('CRT Elements', r'flare|flash', 'encima_corte', 'screen', 'Flare/flash; recolorear con temperatura. Flashes también como transición de luma.'),
    ('CRT Elements', r'wipe', 'encima_corte', 'screen', 'Barrido rápido entre planos.'),
    ('CRT Elements', r'textur', 'look', None, 'Textura de vídeo vintage encima.'),
    ('Analog Video Package', r'video noise', 'look', 'overlay', 'Ruido VHS/Video8 todo el plano.'),
    ('Analog Video Package', r'glitch', 'encima_corte', 'screen', 'Glitch puntual, opacidad ≈40 %.'),
    ('Analog Video Package', r'viewfinder|still overlays', 'look', 'normal', 'Visor / máscara 4:3 / scanlines encima.'),
    ('Analog Video Package', r'text and leaders', 'fondo', 'normal', 'Plano suelto (preroll, warning, the end).'),
    ('Optical Elements', r'.', 'encima_corte', 'screen', 'Refracción atravesando el corte; Hard = transición, Subtle = ambiente.'),
    ('Film Burns', r'.', 'encima_corte', 'screen', 'Cortar en el momento más brillante; escalar para sacar la perforación.'),
    ('Film Leaks', r'.', 'encima_corte', 'normal', 'Encima del corte, escalado; también Vivid Light o fondo de título (Color Dodge/Difference).'),
    ('16mm Package', r'burn', 'encima_corte', 'screen', 'Quemado sobre el corte.'),
    ('16mm Package', r'.', 'look', None, 'Capa de look película.'),
    ('35mm Package', r'burns/', 'encima_corte', 'screen', 'Quemado sobre el corte con su SFX.'),
    ('35mm Package', r'gates/', 'look', 'mate alfa', 'Gate recortado; escalar el metraje para que quepa.'),
    ('35mm Package', r'.', 'look', None, 'Capa de look película.'),
    ('Super 8 Package', r'burn', 'encima_corte', 'screen', 'Quemado sobre el corte.'),
    ('Super 8 Package', r'.', 'look', None, 'Capa de look película.'),
    ('Viewfinders Plus', r'crt', 'look', 'screen', 'Visor CRT encima.'),
    ('Viewfinders Plus', r'.', 'look', None, 'Visor de cámara encima.'),
    ('Super Mixed Media Pack', r'alpha transitions', 'mascara', 'mate alfa', 'Dos copias: visible en Normal + Track Matte Alpha del plano entrante.'),
    ('Super Mixed Media Pack', r'overlay transitions', 'encima_corte', 'normal', 'Collage animado a pantalla completa sobre el corte.'),
    ('Super Mixed Media Pack', r'frames/', 'look', 'normal', 'Marco de papel con alfa encima del plano.'),
    ('Super Mixed Media Pack', r'textures', 'look', 'screen', 'Papel arrugado en Screen + Brightness & Contrast.'),
    ('Super Mixed Media Pack', r'opener|scratch', 'encima_corte', 'screen', 'Sobre negro, en Screen.'),
    ('Ultimate Paper Pack', r'rips', 'mascara', 'mate alfa', 'Dos copias: Track Matte Alpha del plano entrante + borde visible.'),
    ('Ultimate Paper Pack', r'textures', 'look', 'multiply', 'Textura de papel (modo en el nombre).'),
    ('Ultimate Paper Pack', r'opener', 'encima_corte', 'screen', 'Opener sobre negro.'),
    ('Ultimate Paper Pack', r'collage|centered|overla', 'encima_corte', 'normal', 'Collage/overlay de papel.'),
    ('Ultimate Paper Pack', r'toolkit', 'elemento', 'normal', 'Tinta, rotulador, cinta: elementos sueltos.'),
    ('Animated Markers', r'backgrounds', 'fondo', 'normal', 'Fondo de garabatos.'),
    ('Animated Markers', r'.', 'elemento', 'normal', 'Rotulador a 10 fps; colorear con Tint; letras para títulos a mano.'),
    ('Cinemarkers', r'alpha transitions', 'mascara', 'mate alfa', 'Mancha que crece: el plano nuevo aparece dentro.'),
    ('Cinemarkers', r'.', 'encima_corte', 'normal', 'Overlay de película pocos fotogramas sobre el corte.'),
    ('Cinemarkers 2', r'.', 'encima_corte', None, 'Marco/mancha pintada a mano en V2 sobre el corte, con su sonido; el modo se elige según el clip: sobre negro → Screen, sobre blanco → Multiply.'),
    ('Abstracts', r'.', 'fondo', 'normal', 'Bucle abstracto: fondo o textura (probar Screen/Overlay).'),
    ('Liquids', r'.', 'fondo', 'normal', 'Bucle líquido: fondo o textura (probar Screen/Overlay).'),
    ('Morpheus', r'noise textures', 'mascara', 'normal', 'Textura de ruido que alimenta el desplazamiento.'),
]
def regla(pack, ruta):
    r = ruta.lower().replace('\\', '/')
    # solo la parte de la ruta dentro del pack (para que «04_COLLAGE…» no cuente como «collage»)
    marca = '/' + pack.lower() + '/'
    if marca in r:
        r = r.split(marca, 1)[1]
    for pk, rx, col, modo, nota in REGLAS:
        if pk == pack and re.search(rx, r):
            return col, modo, nota
    return None, None, None

# copias que las plantillas de Final Cut / Resolve llevan dentro (no son assets nuevos)
def es_copia_de_plantilla(ruta):
    r = ruta.lower().replace('\\', '/')
    return bool(re.search(r'/(final cut pro x|fcpx|davinci resolve)/.*/media/', r) or re.search(r'\.motr|/media/[^/]+$', r) and '/fcpx/' in r)

# categoría de sonido según la carpeta
CAT_SONIDO = [
    (r'whoosh', 'whoosh'), (r'riser', 'subida (riser)'), (r'\bhits?\b|impact|boom', 'golpe'),
    (r'atmos', 'ambiente'), (r'texture', 'textura'), (r'glitch', 'glitch'), (r'door', 'puerta'),
    (r'metal|debris', 'metal y escombros'), (r'vehicle', 'vehículos'), (r'footstep', 'pasos'),
    (r'burn', 'quemado de película'), (r'warp', 'warp'), (r'transition', 'transición'),
    (r'lens flare', 'destello de lente'), (r'mechanical vcr|camcorder|analog sounds', 'mecánica analógica (VCR / cámara)'),
    (r'/noise_|noise_\d', 'ruido de fondo (bucle)'), (r'flames', 'fuego'), (r'scratch', 'arañazos'),
    (r'/sfx/(centered|collages|opener|overlaps|rips)', 'papel (collage)'), (r'optical elements', 'refracción / destello óptico'),
    (r'morpheus', 'transición digital (morph)'),
]
def cat_sonido(ruta):
    r = ruta.lower().replace('\\', '/')
    for rx, c in CAT_SONIDO:
        if re.search(rx, r):
            return c
    return None

# LUTs: look y cámara a partir del nombre
CAMARAS = [('arri', 'ARRI LogC'), ('logc', 'ARRI LogC'), ('blackmagic', 'Blackmagic Film'), ('canonlog3', 'Canon Log3'),
           ('canon log3', 'Canon Log3'), ('canonlog2', 'Canon Log2'), ('canon log2', 'Canon Log2'), ('canonlog', 'Canon Log'),
           ('canon log', 'Canon Log'), ('dlog', 'DJI D-Log'), ('d-log', 'DJI D-Log'), ('flog2', 'Fuji F-Log2'),
           ('flog', 'Fuji F-Log'), ('n-log', 'Nikon N-Log'), ('nlog', 'Nikon N-Log'), ('v-log', 'Panasonic V-Log'),
           ('vlog', 'Panasonic V-Log'), ('log3g10', 'RED Log3G10'), ('redlogfilm', 'RED LogFilm'), ('redgamma4', 'RED Gamma4'),
           ('slog3', 'Sony S-Log3'), ('s-log3', 'Sony S-Log3'), ('slog2', 'Sony S-Log2'), ('s-log2', 'Sony S-Log2'),
           ('slog', 'Sony S-Log'), ('s-log', 'Sony S-Log'), ('apple', 'Apple Log'), ('rec709', 'Rec.709')]
def info_lut(ruta):
    n = Path(ruta.replace('\\', '/')).name.lower().replace('_', ' ').replace('.cube', '')
    n2 = n.replace(' ', '')
    cam = next((c for k, c in CAMARAS if k.replace(' ', '') in n2), None)
    tipo = 'utilidad (LOG → Rec.709)' if ('utility' in ruta.lower() or ' to rec709' in n) else 'look creativo'
    look = 'cooler' if 'cooler' in n or 'cold' in n else 'warmer' if 'warmer' in n or 'warm' in n else 'neutro'
    m = re.search(r'\b(17|33|65)\b', n)
    return dict(tipo=tipo, camara_entrada=cam, variante=look, tamano=int(m.group(1)) if m else None)

HOSTS = {'mogrt': 'Premiere Pro / After Effects', 'prproj': 'Premiere Pro', 'prfpset': 'Premiere Pro (preset)',
         'drt': 'DaVinci Resolve', 'drp': 'DaVinci Resolve', 'setting': 'DaVinci Resolve', 'motr': 'Final Cut Pro',
         'moti': 'Final Cut Pro', 'motn': 'Apple Motion', 'aep': 'After Effects', 'xml': 'Premiere/FCP (XML)'}

# ----------------------------------------------------------------- lectura de series
def read_series(p: Path):
    if not p.exists():
        return None
    t, v = [], []
    cur = None
    for line in p.read_text(errors='ignore').splitlines():
        if line.startswith('frame:'):
            m = re.search(r'pts_time:([-\d.e]+)', line)
            cur = float(m.group(1)) if m else None
        elif '=' in line:
            try:
                val = float(line.split('=', 1)[1])
            except ValueError:
                continue
            if math.isinf(val) or math.isnan(val):
                val = -120.0
            t.append(cur); v.append(val)
    return (t, v) if v else None

def fnum(x, d=3):
    return None if x is None else round(float(x), d)

def pct(v, q):
    s = sorted(v); k = (len(s) - 1) * q
    f = math.floor(k); c = min(f + 1, len(s) - 1)
    return s[f] + (s[c] - s[f]) * (k - f)

def frac_rate(r):
    try:
        a, b = r.split('/'); return float(a) / float(b) if float(b) else None
    except Exception:
        return None

HUES = [(15, 'rojo'), (40, 'naranja'), (65, 'amarillo'), (160, 'verde'), (200, 'cian'), (255, 'azul'), (290, 'violeta'), (335, 'magenta'), (360, 'rojo')]

def sheet_color(p: Path):
    if Image is None or not p.exists():
        return None
    im = Image.open(p).convert('RGB').resize((96, 27))
    hsv = im.convert('HSV')
    px = list(hsv.getdata()) if not hasattr(hsv, 'get_flattened_data') else list(hsv.get_flattened_data())
    if px and not isinstance(px[0], tuple):
        px = [tuple(px[i:i + 3]) for i in range(0, len(px), 3)]
    sats = [s for h, s, v in px]
    bright = [(h, s, v) for h, s, v in px if v > 60 and s > 60]
    sat = statistics.mean(sats) / 255
    if len(bright) < len(px) * 0.03:
        return dict(saturacion=round(sat, 2), color='neutro')
    hx = sum(math.cos(h / 255 * 2 * math.pi) * s for h, s, v in bright)
    hy = sum(math.sin(h / 255 * 2 * math.pi) * s for h, s, v in bright)
    deg = (math.degrees(math.atan2(hy, hx)) + 360) % 360
    name = next(n for lim, n in HUES if deg <= lim)
    return dict(saturacion=round(sat, 2), color=name if sat > 0.12 else 'neutro', tono_grados=round(deg))

# ----------------------------------------------------------------- modo de fusión escrito por ACIDBITE en el nombre
MODOS = {
    'screen': 'screen', 'add': 'add (linear dodge)', 'linear dodge': 'add (linear dodge)', 'multiply': 'multiply',
    'overlay': 'overlay', 'soft light': 'soft light', 'softlight': 'soft light', 'hard light': 'hard light',
    'alpha': 'normal (alfa)', 'difference': 'difference', 'color dodge': 'color dodge', 'lighten': 'lighten',
    'darken': 'darken', 'normal': 'normal', 'luma': 'mate de luma', 'luma matte': 'mate de luma',
    'linear light': 'linear light', 'exclusion': 'exclusion', 'subtract': 'subtract',
    'mate alfa': 'mate alfa (Track Matte)', 'mate de luma': 'mate de luma (Track Matte)',
    'pin light': 'pin light', 'vivid light': 'vivid light', 'hard mix': 'hard mix', 'color burn': 'color burn',
    'linear burn': 'linear burn', 'lighter color': 'lighter color', 'darker color': 'darker color',
}
def _modo_de(texto):
    for g in reversed(re.findall(r'\(([^)]+)\)', texto)):
        g = g.strip()
        if g in MODOS:
            return g
    m = re.search(r'[_\- ](screen|multiply|overlay|alpha|add|softlight|difference)$', texto)
    return m.group(1) if m else None

def modo_en_nombre(ruta):
    p = Path(ruta.replace('\\', '/'))
    # primero el propio archivo; si no lo dice, la carpeta que lo contiene (p. ej. «Grain (Overlay)/»)
    for parte in [p.stem.lower()] + [q.lower() for q in reversed(p.parent.parts)]:
        m = _modo_de(parte.strip())
        if m:
            return m
    return None

# ----------------------------------------------------------------- clasificación de vídeo
def classify_video(row, probe, Y, D, A, color):
    v = next((s for s in probe.get('streams', []) if s.get('codec_type') == 'video'
              and not s.get('disposition', {}).get('attached_pic')), None)
    a_stream = next((s for s in probe.get('streams', []) if s.get('codec_type') == 'audio'), None)
    fmt = probe.get('format', {})
    dur = float(fmt.get('duration') or 0)
    w, h = int(v.get('width', 0)), int(v.get('height', 0))
    fps = frac_rate(v.get('avg_frame_rate', '')) or frac_rate(v.get('r_frame_rate', ''))
    pix = v.get('pix_fmt', '')
    alpha = bool(re.match(r'^(yuva|rgba|argb|bgra|abgr|gbrap|ya|pal8)', pix or ''))
    ratio = w / h if h else 0
    aspecto = ('vertical' if ratio < 0.9 else 'cuadrado' if ratio < 1.1 else
               '4:3' if ratio < 1.5 else '16:9' if ratio < 1.9 else 'panoramico' if ratio < 2.6 else 'tira')
    e = dict(
        tecnico=dict(codec=v.get('codec_name'), perfil=v.get('profile'), pix_fmt=pix, alfa=alpha,
                     ancho=w, alto=h, fps=fnum(fps), duracion_s=fnum(dur, 2),
                     fotogramas=int(v['nb_frames']) if str(v.get('nb_frames', '')).isdigit() else None,
                     audio_incrustado=bool(a_stream)),
        aspecto=aspecto,
    )
    if color:
        e['color'] = color
    if not Y:  # imagen fija o vídeo sin estadísticas (tutoriales)
        modo = modo_en_nombre(row['ruta'])
        if modo:
            e['composicion'] = MODOS[modo]; e['composicion_fuente'] = 'ACIDBITE (nombre del archivo)'
        elif alpha:
            e['composicion'] = 'normal (alfa)'; e['composicion_fuente'] = 'deducido del análisis'
        return e
    tY, y = Y
    y_mean, y_med = statistics.mean(y), statistics.median(y)
    y_p95, y_max = pct(y, 0.95), max(y)
    i_peak = y.index(y_max)
    m = dict(luma_media=fnum(y_mean, 1), luma_mediana=fnum(y_med, 1), luma_p95=fnum(y_p95, 1),
             luma_max=fnum(y_max, 1), luma_desv=fnum(statistics.pstdev(y), 1), pico_brillo_s=fnum(tY[i_peak], 3),
             pico_distintivo=bool((y_max - y_med) > 12),
             mitad_s=fnum((tY[0] + tY[-1]) / 2, 3))
    if D:
        d = D[1]
        m['movimiento_medio'] = fnum(statistics.mean(d), 2)
        m['movimiento_p95'] = fnum(pct(d, 0.95), 2)
        # cortes duros: saltos muy por encima de lo normal
        base = statistics.median(d) or 0.01
        m['saltos'] = sum(1 for x in d if x > max(25, base * 8))
    cov = None
    if A:
        tA, al = A
        cov = [x / 255 for x in al]
        m['alfa_cobertura_media'] = fnum(statistics.mean(cov), 3)
        m['pico_cobertura_s'] = fnum(tA[cov.index(max(cov))], 3)
        m['alfa_cobertura_inicio'] = fnum(cov[0], 3)
        m['alfa_cobertura_fin'] = fnum(cov[-1], 3)
        m['alfa_cobertura_max'] = fnum(max(cov), 3)
    e['medidas'] = m

    # ---- cómo se compone
    lowsat = (color or {}).get('saturacion', 1) < 0.12
    comp, uso, notas = None, [], []
    tl = {}
    if alpha and cov:
        cmax, cmean = max(cov), statistics.mean(cov)
        full = [i for i, c in enumerate(cov) if c >= 0.97]
        if full:
            comp = 'normal (alfa)'
            uso = ['transicion']
            tl = dict(cubre_desde_s=fnum(tA[full[0]], 3), cubre_hasta_s=fnum(tA[full[-1]], 3),
                      corte_recomendado_s=fnum(tA[(full[0] + full[-1]) // 2], 3))
            notas.append('Tapa la pantalla entera: el corte entre planos va mientras está cubierta.')
        elif statistics.pstdev(cov) < 0.02 and m.get('movimiento_medio', 9) < 4:
            comp = 'normal (alfa)'; uso = ['marco']
            notas.append('Cobertura casi constante: marco/gate o máscara fija.')
        else:
            comp = 'normal (alfa)'; uso = ['elemento', 'overlay']
            if cmax > 0.6:
                uso.append('transicion_parcial')
    else:
        if y_med < 45:
            comp = 'screen / add'
            uso = ['overlay_luz']
            notas.append('Fondo negro: el negro desaparece en Screen/Add.')
        elif 95 <= y_mean <= 160 and m['luma_desv'] < 12 and lowsat:
            comp = 'overlay / soft light'
            uso = ['grano_textura']
            notas.append('Gris medio estable: textura/grano para Overlay, Soft Light o Linear Light.')
        elif y_mean > 175:
            comp = 'multiply'
            uso = ['textura_clara']
            notas.append('Fondo claro: en Multiply desaparece el blanco.')
        else:
            comp = 'normal / screen'
            uso = ['imagen_completa']
        # destello: sube a casi blanco => transición de luz o mate de luma
        if y_max > 200 and (y_max - y_med) > 60:
            uso.append('transicion_luz')
            tl = dict(pico_s=fnum(tY[i_peak], 3), corte_recomendado_s=fnum(tY[i_peak], 3))
            hi = [i for i, x in enumerate(y) if x > 200]
            tl['blanco_desde_s'], tl['blanco_hasta_s'] = fnum(tY[hi[0]], 3), fnum(tY[hi[-1]], 3)
            notas.append('Cortar en el fotograma más brillante (lo recomienda ACIDBITE para los quemados).')
            if lowsat and y[0] < 30 and (y[-1] > 200 or y[-1] < 30):
                uso.append('mate_luma')
    # lo que dice ACIDBITE en el nombre del archivo manda sobre lo deducido
    modo = modo_en_nombre(row['ruta'])
    if modo:
        e['composicion'] = MODOS[modo]
        e['composicion_fuente'] = 'ACIDBITE (nombre del archivo)'
        if comp and MODOS[modo].split(' ')[0] not in comp:
            notas.append(f'El análisis sugería «{comp}», pero se usa el modo que indica ACIDBITE.')
        if modo in ('screen', 'add', 'linear dodge', 'lighten', 'color dodge') and 'overlay_luz' not in uso and 'transicion_luz' not in uso:
            uso = ['overlay_luz'] + [u for u in uso if u != 'imagen_completa']
        if modo == 'overlay' or modo == 'soft light':
            uso = ['grano_textura'] + [u for u in uso if u not in ('imagen_completa', 'grano_textura')]
        if modo == 'multiply' and not alpha and y_med < 50 and 'viewfinders' in row['ruta'].lower():
            notas.append('OJO: el nombre dice (Multiply), pero el .mov es línea clara sobre negro y en el tutorial de '
                         'Viewfinders+ se ve sobre el metraje como Screen (las líneas suman luz). Usar Screen. '
                         'Los PNG del mismo pack sí son línea negra sobre blanco y van en Multiply.')
            e['composicion_recomendada'] = 'screen'
            e['composicion_recomendada_fuente'] = 'ACIDBITE (tutorial Viewfinders+), comprobado en el vídeo'
        elif modo == 'multiply' and not alpha and y_med < 30:
            notas.append('Fondo casi negro en Multiply: oscurece casi todo el plano. Es un golpe/glitch de pocos '
                         'fotogramas: el apagón forma parte del efecto.')
        if modo == 'screen' and not alpha and y_med > 200:
            notas.append('Fondo casi blanco en Screen: destello a blanco de pocos fotogramas; forma parte del efecto.')
        if modo == 'multiply' and 'imagen_completa' in uso:
            uso = ['textura_clara' if 'marco' not in uso else 'marco'] + [u for u in uso if u != 'imagen_completa']
    else:
        e['composicion'] = comp
        e['composicion_fuente'] = 'deducido del análisis'
    e['uso'] = uso
    if tl:
        e['transicion'] = tl
    if notas:
        e['notas'] = notas

    # ---- velocidad y cómo jugar con ella
    mv = m.get('movimiento_medio')
    if mv is None and len(y) <= 2:
        e['velocidad'] = 'un fotograma'
        e['retiming'] = 'Es un golpe de 1–2 fotogramas: se usa tal cual, o se congela/repite para alargarlo.'
    if mv is not None:
        vel = 'un fotograma' if len(y) <= 1 else 'estatico' if mv < 1.5 else 'lento' if mv < 6 else 'medio' if mv < 15 else 'rapido' if mv < 28 else 'muy rapido'
        e['velocidad'] = vel
        if 'grano_textura' in uso:
            e['retiming'] = 'Mantener a velocidad nativa (en bucle). Acelerar el grano lo delata.'
        elif 'overlay_luz' in uso or 'transicion_luz' in uso:
            e['retiming'] = 'Admite 50–200 % con fusión de fotogramas; el SFX no se estira: se alinea al pico.'
        elif comp and comp.startswith('normal (alfa)'):
            e['retiming'] = 'Admite 70–150 %; para collage/stop motion, conformar a 12 u 8 fps (sin fusión).'
    return e


# ---------------------------------------------------------------- punto de corte
LUZ = ('screen', 'add', 'linear dodge', 'lighten', 'color dodge', 'difference', 'normal / screen', 'screen / add')
def _prominente(v, i):
    med = statistics.median(v)
    rng = (max(v) - min(v)) or 1e-6
    return (v[i] - med) > max(6.0, 0.25 * (med + 10)) or (v[i] - med) / rng > 0.6 and (v[i] - med) > 4

def _ventana(t, v, frac=0.5):
    lo, hi = min(v), max(v)
    thr = lo + (hi - lo) * frac
    idx = [i for i, x in enumerate(v) if x >= thr]
    return (fnum(t[idx[0]], 3), fnum(t[idx[-1]], 3)) if idx else (None, None)


def _centro_meseta(v, i, tol=0.04):
    """Si el máximo dura varios fotogramas (p. ej. un blanco total), devuelve el centro de esa meseta."""
    top = v[i]; rng = (max(v) - min(v)) or 1
    a = b = i
    while a > 0 and top - v[a - 1] <= tol * rng: a -= 1
    while b < len(v) - 1 and top - v[b + 1] <= tol * rng: b += 1
    return (a + b) // 2

def punto_de_corte(ent, col, Y, D, A):
    """Devuelve el bloque 'transicion' según la colocación y el modo real del clip."""
    if not Y or col not in ('encima_corte', 'mascara', 'intercalado'):
        return None
    tY, y = Y
    dur = ent.get('tecnico', {}).get('duracion_s') or (tY[-1] if tY else 0)
    modo = (ent.get('composicion_recomendada') or ent.get('composicion') or '').lower()
    alpha = ent.get('tecnico', {}).get('alfa')
    cov = [x / 255 for x in A[1]] if A else None
    tA = A[0] if A else None
    if col == 'intercalado':
        return dict(tipo='intercalado', criterio='plano entre los dos planos (misma pista)',
                    nota='Va entero entre el plano que sale y el que entra; suavizar las uniones con fundidos de 2–4 fotogramas.')
    if col == 'mascara':
        usa_alfa = cov and alpha and ('alfa' in modo or (max(cov) - min(cov)) > 0.3 and 'luma' not in modo and 'screen' not in modo)
        if usa_alfa:
            serie, ts, que = cov, tA, 'alfa'
        else:
            serie, ts, que = [v / 255 for v in y], tY, 'luma'
        if re.search(r'dissected alpha|_mask(inside|out)', ent.get('ruta', '').lower()):
            return dict(tipo='recorte', criterio=f'forma por {que}: el plano se ve solo dentro de la forma durante todo el clip',
                        nota='No es una entrada/salida: es un recorte de collage. Se puede alargar congelando o en bucle.')
        up = serie[-1] >= serie[0]
        objetivo = max(serie) * 0.97 if up else min(serie) + 0.03
        idx = [i for i, v in enumerate(serie) if (v >= objetivo if up else v <= objetivo)]
        r = dict(tipo='mascara', inicio_s=0.0, criterio=f'máscara por {que}: el plano entrante empieza a la vez que el clip',
                 revelado_completo_s=fnum(ts[idx[0]], 3) if idx else None,
                 nota='El plano que sale debe durar al menos hasta revelado_completo_s.')
        if not up:
            r['invertir'] = True
            r['nota'] += (' El hueco por donde entra el plano nuevo es la parte ' + ('transparente' if que == 'alfa' else 'oscura') +
                          ' y crece: activar Reverse en el Track Matte (' + ('Alpha Inverted' if que == 'alfa' else 'Luma Inverted') + ').')
        return r
    # encima del corte
    if alpha and cov:
        full = [i for i, c in enumerate(cov) if c >= 0.97]
        if full:
            return dict(tipo='encima_corte', criterio='pantalla tapada por el clip (alfa)',
                        cubre_desde_s=fnum(tA[full[0]], 3), cubre_hasta_s=fnum(tA[full[-1]], 3),
                        corte_recomendado_s=fnum(tA[(full[0] + full[-1]) // 2], 3))
        i = cov.index(max(cov))
        d, h = _ventana(tA, cov)
        return dict(tipo='encima_corte', criterio='máxima cobertura del alfa', corte_recomendado_s=fnum(tA[i], 3),
                    efecto_desde_s=d, efecto_hasta_s=h)
    if 'multiply' in modo:
        inv = [255 - v for v in y]
        i = inv.index(max(inv))
        if _prominente(inv, i):
            d, h = _ventana(tY, inv)
            i = _centro_meseta(inv, i)
            return dict(tipo='encima_corte', criterio='fotograma más oscuro (Multiply)', corte_recomendado_s=fnum(tY[i], 3),
                        efecto_desde_s=d, efecto_hasta_s=h)
    elif any(k in modo for k in LUZ) or modo.startswith('normal'):
        i = y.index(max(y))
        if _prominente(y, i):
            d, h = _ventana(tY, y)
            i = _centro_meseta(y, i)
            return dict(tipo='encima_corte', criterio='fotograma más brillante', corte_recomendado_s=fnum(tY[i], 3),
                        efecto_desde_s=d, efecto_hasta_s=h)
        if (max(y) - min(y)) > 4:
            d, h = _ventana(tY, y)
            if d is not None and h is not None and (h - d) < 0.8 * (tY[-1] - tY[0] + 1e-6):
                return dict(tipo='encima_corte', criterio='centro del tramo con más efecto (brillo)',
                            corte_recomendado_s=fnum((d + h) / 2, 3), efecto_desde_s=d, efecto_hasta_s=h)
    if D and len(D[1]) > 4:
        tD, dd = D
        n = len(dd); lo, hi = max(1, n // 10), n - max(1, n // 10)
        j = max(range(lo, hi), key=lambda k: dd[k]) if hi > lo else dd.index(max(dd))
        if _prominente(dd, j):
            return dict(tipo='encima_corte', criterio='mayor cambio de imagen (movimiento)',
                        corte_recomendado_s=fnum(tD[j], 3))
    return dict(tipo='encima_corte', criterio='efecto uniforme: sin momento fuerte, vale cualquier punto',
                corte_recomendado_s=fnum(dur / 2, 3),
                nota='Centrado sobre el corte por defecto; se puede desplazar sin que cambie el resultado.')

# ----------------------------------------------------------------- audio
def classify_audio(row, probe, E):
    a = next((s for s in probe.get('streams', []) if s.get('codec_type') == 'audio'), {})
    fmt = probe.get('format', {})
    dur = float(fmt.get('duration') or 0)
    e = dict(tecnico=dict(codec=a.get('codec_name'), sample_rate=int(a.get('sample_rate', 0) or 0),
                          canales=a.get('channels'), duracion_s=fnum(dur, 2)))
    if not E:
        return e
    t, db = E
    pk = max(db); i = db.index(pk)
    tpk = t[i] or 0
    above = [x for x in db if x > pk - 20]
    act = len(above) / len(db)
    # ataque: desde -30 dB bajo el pico hasta el pico
    j = i
    while j > 0 and db[j] > pk - 30:
        j -= 1
    ataque = (tpk - (t[j] or 0))
    pos = tpk / dur if dur else 0
    if dur > 8 and act > 0.5:
        forma = 'ambiente / bucle'
    elif ataque < 0.03 and pos < 0.35:
        forma = 'golpe'
    elif pos > 0.7 and ataque > 0.3:
        forma = 'subida (riser)'
    elif 0.2 <= pos <= 0.8 and ataque > 0.1:
        forma = 'whoosh / barrido'
    else:
        forma = 'textura / mixto'
    e['envolvente'] = dict(pico_dbfs=fnum(pk, 1), pico_s=fnum(tpk, 3), ataque_s=fnum(ataque, 3),
                           actividad=fnum(act, 2), forma=forma)
    e['sincronia'] = 'Alinear pico_s con el corte (o el pico de la transición).'
    return e

# ----------------------------------------------------------------- principal
inv = list(csv.DictReader(open(ANA / 'inventario.csv', encoding='utf-8-sig')))
cat = []
for r in inv:
    idn = r['id']
    ent = dict(id=idn, categoria=r['categoria'], pack=r['pack'], ruta=r['ruta'].replace('\\', '/'),
               tipo=r['tipo'], ext=r['ext'], bytes=int(r['bytes']))
    info = PACKS.get(r['pack'])
    if info:
        ent['estilos'] = list(info['estilos'])
    pj = ANA / 'probe' / f'{idn}.json'
    probe = None
    if pj.exists():
        try:
            probe = json.loads(pj.read_text(encoding='utf-8-sig') or '{}')
        except json.JSONDecodeError:
            probe = None
    rl = r['ruta'].lower()
    if r['tipo'] == 'video' and re.search(r'tutorial', rl):
        ent['tipo'] = 'tutorial'
    elif r['tipo'] == 'video' and re.search(r'/previews?/|preview|teaser', rl.replace('\\', '/')):
        ent['tipo'] = 'preview'
    if es_copia_de_plantilla(r['ruta']) or re.search(r'/(fcpx|final cut pro x)/', rl.replace('\\', '/')):
        ent['copia_de_plantilla'] = True
    if r['tipo'] == 'video' and re.search(r'(test|demo)?footage_?\d|pbvhs_footage', Path(rl).name):
        ent['tipo'] = 'metraje_demo'
    col, modo_def, nota = regla(r['pack'], r['ruta'])
    if r['tipo'] == 'lut':
        ent['lut'] = info_lut(r['ruta'])
    if r['tipo'] == 'plantilla':
        ent['programa'] = HOSTS.get(r['ext'], r['ext'])
    if r['tipo'] == 'audio':
        c = cat_sonido(r['ruta'])
        if c:
            ent['categoria_sonido'] = c
    try:
        if r['tipo'] in ('video', 'imagen') and ent['tipo'] not in ('tutorial',) and probe:
            ent.update(classify_video(r, probe,
                                      read_series(ANA / 'stats' / f'{idn}_Y.txt'),
                                      read_series(ANA / 'stats' / f'{idn}_D.txt'),
                                      read_series(ANA / 'stats' / f'{idn}_A.txt'),
                                      sheet_color(ANA / 'sheets' / f'{idn}.jpg')))
            if (ANA / 'sheets' / f'{idn}.jpg').exists():
                ent['miniatura'] = f'sheets/{idn}.jpg'
            if col:
                ent['colocacion'] = col
                ent['colocacion_texto'] = COLOCACIONES[col]
                ent.setdefault('notas', []).insert(0, 'ACIDBITE (tutorial): ' + nota)
                if modo_def and ent.get('composicion_fuente') != 'ACIDBITE (nombre del archivo)':
                    ent['composicion'] = MODOS.get(modo_def, modo_def)
                    ent['composicion_fuente'] = 'ACIDBITE (tutorial)'
                elif not modo_def and ent.get('composicion_fuente') == 'deducido del análisis':
                    ent['composicion_fuente'] = 'ACIDBITE (tutorial: según el clip) + fondo medido'
            if ent.get('medidas'):
                tc = punto_de_corte(ent, col, read_series(ANA / 'stats' / f'{idn}_Y.txt'),
                                    read_series(ANA / 'stats' / f'{idn}_D.txt'),
                                    read_series(ANA / 'stats' / f'{idn}_A.txt'))
                if tc:
                    prev = ent.get('transicion') or {}
                    for k in ('blanco_desde_s', 'blanco_hasta_s'):
                        if k in prev: tc[k] = prev[k]
                    ent['transicion'] = tc
        elif r['tipo'] == 'audio' and probe:
            ent.update(classify_audio(r, probe, read_series(ANA / 'audio' / f'{idn}_E.txt')))
    except Exception as ex:
        ent['error_analisis'] = str(ex)
    cat.append(ent)

# emparejar SFX con su clip (mismo pack, misma palabra clave y mismo número)
STOP = {'sfx', 'acidbite', '4k', 'prores', 'mov', 'wav', 'mp4', 'hd', 'uhd'}
def clave(ruta):
    stem = Path(ruta).stem.lower()
    stem = re.sub(r'\([^)]*\)', ' ', stem)               # fuera el modo de fusión
    toks = [t for t in re.split(r'[^a-z0-9]+', stem) if t]
    nums = [int(t) for t in toks if t.isdigit()]
    words = {t for t in toks if not t.isdigit() and t not in STOP and not re.fullmatch(r'\d+mm', t)}
    return words, (nums[-1] if nums else None)

by_pack = defaultdict(list)
for e in cat:
    by_pack[e['pack']].append(e)
for pack, items in by_pack.items():
    auds = [(a, *clave(a['ruta'])) for a in items if a['tipo'] == 'audio']
    if not auds:
        continue
    for v in (e for e in items if e['tipo'] == 'video'):
        wv, nv = clave(v['ruta'])
        best, bs = None, 0
        for a, wa, na in auds:
            if nv is None or na != nv:
                continue
            shared = len(wv & wa)
            # bonus si la carpeta del audio comparte palabra con el clip (SFX/Burns <-> Burns/...)
            dirs = set(re.split(r'[^a-z0-9]+', str(Path(a['ruta']).parent).lower()))
            vdirs = set(re.split(r'[^a-z0-9]+', str(Path(v['ruta']).parent).lower()))
            sc = shared * 2 + len((dirs & vdirs) - {'assets', 'sfx', ''})
            if shared and sc > bs:
                best, bs = a, sc
        if best:
            v['sfx'] = best['id']
            best.setdefault('clips', []).append(v['id'])


# ---- duraciones: si el SFX emparejado por nombre no coincide y otro del mismo pack sí, ACIDBITE cruzó los nombres
for pack, items in by_pack.items():
    auds = {a['id']: a for a in items if a['tipo'] == 'audio'}
    for v in (e for e in items if e['tipo'] == 'video' and e.get('sfx')):
        a = auds.get(v['sfx']); dv = v.get('tecnico', {}).get('duracion_s')
        da = (a or {}).get('tecnico', {}).get('duracion_s')
        if not a or dv is None or da is None:
            continue
        if abs(dv - da) <= 0.05:
            v['sfx_confianza'] = 'nombre y duración coinciden'
            continue
        alt = [x for x in auds.values() if x['id'] != a['id'] and Path(x['ruta']).parent == Path(a['ruta']).parent
               and abs((x.get('tecnico', {}).get('duracion_s') or -9) - dv) <= 0.05
               and re.sub(r'\d+', '', Path(x['ruta']).stem) == re.sub(r'\d+', '', Path(a['ruta']).stem)]
        if len(alt) == 1:
            v['sfx_por_nombre'] = v['sfx']; v['sfx'] = alt[0]['id']
            v['sfx_confianza'] = (f'por duración: el nombre apunta a «{Path(a["ruta"]).name}», pero dura {da} s y el clip {dv} s; '
                                  f'«{Path(alt[0]["ruta"]).name}» dura exactamente lo mismo (ACIDBITE cruzó los nombres)')
        else:
            v['sfx_confianza'] = f'por nombre (duraciones distintas: clip {dv} s, sonido {da} s; alinear el golpe al pico)'

# ---- combinaciones de ACIDBITE: carpetas Media de sus plantillas (FCPX/Resolve) y proyectos de Premiere
by_name = defaultdict(list)
for e in cat:
    if not e.get('copia_de_plantilla') and e['tipo'] in ('video', 'imagen', 'audio'):
        by_name[(e['pack'], Path(e['ruta']).name.lower())].append(e)
grupos = defaultdict(list)
for e in cat:
    r = e['ruta']
    if e.get('copia_de_plantilla') and '/Media/' in r:
        grupos[(e['pack'], r.split('/Media/')[0])].append(e)
for (pack, carpeta), items in grupos.items():
    nombres = [Path(x['ruta']).name for x in items]
    plantilla = carpeta.split('/')[-1]
    for x in items:
        for orig in by_name.get((pack, Path(x['ruta']).name.lower()), []):
            otros = sorted(n for n in nombres if n != Path(x['ruta']).name)
            orig.setdefault('combinado_por_acidbite', [])
            if not any(c['plantilla'] == plantilla for c in orig['combinado_por_acidbite']):
                orig['combinado_por_acidbite'].append(dict(plantilla=plantilla, con=otros))
            if orig['tipo'] == 'video':
                sons = [n for n in otros if n.lower().endswith(('.wav', '.mp3', '.aif', '.aiff'))]
                if sons and pack in ('Textile Transitions',):
                    orig['sfx_acidbite'] = sorted(set(orig.get('sfx_acidbite', [])) | set(sons))

PLANT = OUT / 'plantillas_acidbite.json'
if PLANT.exists():
    plant = json.loads(PLANT.read_text(encoding='utf-8'))
    for proy, seqs in plant.items():
        for seqn, sq in seqs.items():
            for c in sq['capas']:
                nm = (c.get('clip') or '').lower()
                for orig in [e for (pk, n), L in by_name.items() if n == nm for e in L]:
                    u = dict(proyecto=proy, secuencia=seqn, pista=f"V{c['pista']}", modo=c['modo'],
                             dura_s=round(c['fin_s'] - c['inicio_s'], 3))
                    if c.get('rol'): u['rol'] = c['rol']
                    if c['efectos']: u['efectos'] = c['efectos']
                    if c['opacidad'] != 100: u['opacidad'] = c['opacidad']
                    if sq.get('corte_s') is not None:
                        u['corte_desde_inicio_del_clip_s'] = round(sq['corte_s'] - c['inicio_s'], 3)
                    orig.setdefault('uso_en_plantillas_acidbite', []).append(u)
    for e in cat:
        us = [u for u in e.get('uso_en_plantillas_acidbite', []) if u.get('rol') != 'mate (Track Matte del plano entrante)']
        modos = sorted({u['modo'] for u in us})
        if modos:
            e['modos_usados_por_acidbite'] = modos
            if e.get('composicion') and not any(m.split(' ')[0] in (e.get('composicion_recomendada') or e['composicion']) for m in modos):
                e.setdefault('notas', []).append('En sus proyectos de Premiere ACIDBITE lo usa en: ' + ', '.join(modos) + '.')
        cortes = [u['corte_desde_inicio_del_clip_s'] for u in us if 'corte_desde_inicio_del_clip_s' in u]
        if cortes and e.get('transicion', {}).get('tipo') == 'encima_corte':
            e['transicion']['corte_acidbite_s'] = cortes[0]
            e['transicion']['criterio'] += ' · ACIDBITE en su plantilla corta a ' + str(cortes[0]) + ' s'
            e['transicion']['corte_recomendado_s'] = cortes[0]

# ---- SFX genéricos de los packs que traen una caja de herramientas de sonido sin emparejar
GEN = {
    'CRT Elements': [(r'/flares/', r'lens flare'), (r'/(wipes|glitches|flashes)/', r'analog video whoosh'),
                     (r'/(dirt|textures)/', r'noise_'), (r'.', r'mechanical vcr')],
    'Morpheus': [(r'.', r'morpheus_sfx')],
    'Punch Hole Transitions': [(r'.', r'warp_sfx')],
}
for pack, reglas in GEN.items():
    auds = [a for a in by_pack.get(pack, []) if a['tipo'] == 'audio' and not a.get('copia_de_plantilla')]
    for v in (e for e in by_pack.get(pack, []) if e['tipo'] == 'video' and not e.get('copia_de_plantilla') and not e.get('sfx')):
        rl = v['ruta'].lower()
        for rx, arx in reglas:
            if re.search(rx, rl):
                cands = sorted(a['id'] for a in auds if re.search(arx, Path(a['ruta']).name.lower()))
                if cands:
                    v['sfx_sugeridos'] = cands
                    v['sfx_confianza'] = 'familia de sonidos del pack (ACIDBITE no los empareja uno a uno)'
                break


# ---- presets de ACIDBITE (Track Matte Key exacto)
PRES = OUT / 'presets_acidbite.json'
if PRES.exists():
    pres = json.loads(PRES.read_text(encoding='utf-8'))
    tex = [e for L in pres.get('ACIDBITE Textile Transitions Presets.prfpset', {}).values() for e in L if 'Track Matte' in e['efecto']]
    for n, tm in enumerate(tex, start=1):
        rev = tm['params'].get('Reverse') == 'true'
        for e in cat:
            nm = Path(e['ruta']).name
            if e['pack'] == 'Textile Transitions' and not e.get('copia_de_plantilla') and re.fullmatch(rf'Transition {n} Frame( \d)?\.mov', nm):
                t = e.setdefault('transicion', {})
                auto = bool(t.get('invertir'))
                t['invertir'] = rev
                t['invertir_fuente'] = (f'ACIDBITE (preset «Transition {n} Shot 2»: Track Matte Key, Matte Alpha, Reverse {"sí" if rev else "no"})'
                                        + ('' if auto == rev else ' — corrige lo medido'))
                t['nota'] = ('Receta ACIDBITE: plano entrante con Track Matte Key (Matte Alpha' + (', Reverse' if rev else '') +
                             ') usando una copia del Frame en la pista de debajo; otra copia visible encima en '
                             + ', '.join(e.get('modos_usados_por_acidbite', ['Screen'])) + '. El plano que sale sigue debajo hasta el final del Frame.')
    for e in cat:
        if e['pack'] == 'Punch Hole Transitions' and '/Key-Transitions/' in e['ruta'] and not e.get('copia_de_plantilla'):
            t = e.setdefault('transicion', {})
            t['nota'] = ('Receta ACIDBITE (proyecto PUNCHHOLE TRANSITIONS 2024 y presets *_trackmattekey): el plano que sale se anida, '
                         'se congela y se anida otra vez; lleva Track Matte Key (Matte Alpha, sin Reverse) con una copia de esta clave '
                         'en la pista de debajo, así el agujero deja ver el plano entrante. Otra copia visible encima en '
                         + ', '.join(e.get('modos_usados_por_acidbite', ['screen'])) + '.')
            t['invertir'] = False
            t['invertir_fuente'] = 'ACIDBITE (preset Punchhole_Warp_*_trackmattekey: Matte Alpha, Reverse no; la máscara va en el plano que sale)'


# ---- Textile 6: el «Frame 1» ACIDBITE lo pone solo, en Normal, antes del corte (no como máscara)
for e in cat:
    if e['pack'] == 'Textile Transitions' and Path(e['ruta']).name == 'Transition 6 Frame 1.mov' and not e.get('copia_de_plantilla'):
        e['colocacion'] = 'encima_corte'; e['colocacion_texto'] = COLOCACIONES['encima_corte']
        e['composicion'] = 'normal (alfa)'; e['composicion_fuente'] = 'ACIDBITE (plantilla Textile Transition 6)'
        e['transicion'] = dict(tipo='encima_corte', criterio='como en la plantilla ACIDBITE: entra 0,08 s antes del corte',
                               corte_recomendado_s=0.083, corte_acidbite_s=0.083,
                               nota='Primera parte de la transición 6: tela en Normal sobre el plano que sale; luego entra «Frame 2» como máscara.')

(OUT / 'catalogo.json').write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding='utf-8')
print('entradas:', len(cat))
print(Counter(e['tipo'] for e in cat))
print(Counter(e.get('composicion') for e in cat if e['tipo'] == 'video'))
