"""Lee por dentro plantillas y proyectos de editor sin abrir el programa: .drt (DaVinci), .prproj (Premiere, gzip XML),
.prfpset (preajustes de Premiere, XML), .mogrt (zip con definition.json) y .aep (After Effects, binario RIFX).
Saca los medios que usa, los efectos, los modos de fusión, las secuencias/composiciones y los parámetros expuestos.
  python3 tools/atlas/leer_plantillas.py <archivo>...   → JSON por línea"""
import sys, json, re, zipfile, gzip, collections

MEDIO = re.compile(r'[\w \-\.\(\)&,+]+\.(mov|mp4|png|jpg|jpeg|wav|mp3|aif|aiff|psd|ai|tif|tiff|exr|cube|mxf|m4a)$', re.I)
FX_PAL = ['blur', 'glow', 'displace', 'warp', 'transform', 'zoom', 'crop', 'opacity', 'track matte', 'luma key', 'key',
          'noise', 'grain', 'lens', 'distort', 'chromatic', 'aberration', 'rgb', 'channel', 'curves', 'levels', 'lumetri',
          'color', 'colour', 'sharpen', 'mosaic', 'glitch', 'vhs', 'scanline', 'shake', 'wave', 'turbulent', 'fractal',
          'mask', 'matte', 'directional', 'gaussian', 'radial', 'motion', 'echo', 'posterize', 'invert', 'tint',
          'vignette', 'flare', 'light', 'fusion', 'ofx', 'composite', 'feather', 'stretch', 'mirror', 'tile', 'offset',
          'bulge', 'spherize', 'twirl', 'ripple', 'datamosh', 'mosh', 'pixel', 'displacement', 'camera', 'film']
MODOS = ['screen', 'add', 'multiply', 'overlay', 'soft light', 'hard light', 'lighten', 'darken', 'difference',
         'color dodge', 'linear dodge', 'subtract', 'exclusion', 'luminosity', 'hue', 'saturation']

def utf16_de_hex(texto):
    out = []
    for h in re.findall(r'\b[0-9a-f]{40,}\b', texto):
        try: b = bytes.fromhex(h if len(h) % 2 == 0 else h[:-1])
        except ValueError: continue
        for enc in ('utf-16-be', 'utf-16-le'):
            s = b.decode(enc, errors='ignore')
            out += re.findall(r'[A-Za-z][A-Za-z0-9 _\-\.\(\)&,+]{3,}', s)
    return out

def cadenas_binario(b):
    s = re.findall(rb'[\x20-\x7e]{4,}', b)
    u = re.findall(rb'(?:[\x20-\x7e]\x00){4,}', b)
    return [x.decode('ascii', 'ignore') for x in s] + [x.decode('utf-16-le', 'ignore') for x in u]

def textos(p):
    ext = p.rsplit('.', 1)[-1].lower(); T = []
    if ext in ('drt', 'mogrt'):
        z = zipfile.ZipFile(p)
        for n in z.namelist():
            if n.endswith(('.xml', '.json')):
                t = z.read(n).decode('utf-8', 'ignore'); T.append(t); T += utf16_de_hex(t)
            elif n.endswith('.aegraphic'):
                T += cadenas_binario(z.read(n)[:30_000_000])
    elif ext == 'prproj':
        t = gzip.open(p).read().decode('utf-8', 'ignore'); T.append(t)
    elif ext == 'prfpset':
        T.append(open(p, encoding='utf-8', errors='ignore').read())
    elif ext == 'aep':
        T += cadenas_binario(open(p, 'rb').read())
    return ext, T

def leer(p):
    ext, T = textos(p); todo = '\n'.join(T)
    tokens = set(re.findall(r'>([^<>]{3,120})<', todo)) | set(x for x in T if len(x) < 140)
    tokens |= set(re.findall(r'"(?:name|displayName|label|strDB)"\s*:\s*"([^"]{2,120})"', todo))
    medios = sorted({m.strip() for t in tokens for m in [t.strip().split('/')[-1].split('\\')[-1]] if MEDIO.match(m.strip())})
    fx = collections.Counter()
    RUIDO = re.compile(r'(Rotate|Orientation|^Scale$|Layer Styles|Bevel|Sync Offset|Geometry2|Angle Control|Slider Control|Group|Params|Position|Anchor|Vectors|Overrides|Root|End$|BA$|Prefs|\.Cfg|Version|^UI_|FOLDER_|^[A-Z0-9_]+$|Envir|Built In|Marker|Label)')
    binario = ext in ('aep', 'mogrt')
    for t in tokens:
        t = t.strip(); tl = t.lower()
        if binario or not (3 < len(t) < 50) or RUIDO.search(t) or MEDIO.match(t) or re.search(r'[{}<>=;|^]', t): continue
        if ' ' in t and re.fullmatch(r'[A-Za-z][A-Za-z0-9 \-\(\)]+', t) and any(k in tl for k in FX_PAL): fx[t] += 1
    for m in re.findall(r'(?:AE\.|PR\.)?ADBE ([A-Za-z0-9 ]{2,40}?)(?=[^A-Za-z0-9 ]|$)', todo):
        m = m.strip()
        if not RUIDO.search(m): fx[m] += 2
    modos = sorted({m for m in MODOS if re.search(r'(?i)(blend|composite|mode)[^\n]{0,60}\b' + m + r'\b', todo)})
    r = dict(tipo=ext, medios=medios[:60], n_medios=len(medios), efectos=[k for k, _ in fx.most_common(40)], modos_fusion=modos)
    if ext == 'mogrt':
        try:
            d = json.loads(zipfile.ZipFile(p).read('definition.json'))
            st = lambda x: (x or {}).get('strDB', [{}])[0].get('str') if isinstance(x, dict) and (x or {}).get('strDB') else None
            cc = d.get('clientControls', [])
            r['mogrt'] = dict(nombre=d.get('capsuleName'), app=d.get('authorApp'), efectos_usados=d.get('usedEffects'),
                              parametros=[f"{st(c.get('uiName'))} ({c.get('width')}×{c.get('height')})" if c.get('type') == 14 else st(c.get('uiName')) for c in cc],
                              duracion_s=round(max([c.get('endtime', 0) / c.get('timescale', 1) for c in cc if c.get('timescale')] or [0]), 2))
            raise StopIteration
            r['mogrt'] = dict(nombre=(d.get('capsuleName') or {}).get('strDB', [{}])[0].get('str') if isinstance(d.get('capsuleName'), dict) else d.get('capsuleName'),
                              duracion=d.get('duration'), tamano=d.get('sourceInfo', {}).get('framesize') if isinstance(d.get('sourceInfo'), dict) else None,
                              parametros=[(c.get('capPropName') or {}).get('strDB', [{}])[0].get('str') for c in d.get('clientControls', []) if isinstance(c.get('capPropName'), dict)])
        except StopIteration: pass
        except Exception as e: r['mogrt'] = dict(error=str(e)[:80])
    if ext in ('prproj', 'prfpset'):
        r['secuencias'] = sorted(set(re.findall(r'<Sequence[^>]*>\s*<Name>([^<]+)</Name>', todo)))[:20]
        r['presets'] = sorted(set(re.findall(r'<PresetName>([^<]+)</PresetName>|<Name>([^<]*[Pp]reset[^<]*)</Name>', todo)))[:20]
        r['presets'] = [a or b for a, b in r['presets']]
    if ext == 'drt':
        z = zipfile.ZipFile(p); pj = z.read('project.xml').decode('utf-8', 'ignore')
        nm = re.search(r'<ProjectName>([^<]+)', pj); r['proyecto'] = nm.group(1) if nm else None
        dur = [int(x) for x in re.findall(r'<Start>(\d+)</Start>\s*<Duration>(\d+)', todo) for x in []]  # (reservado)
        ends = [int(a) + int(b) for a, b in re.findall(r'<Start>(\d+)</Start>[\s\S]{0,400}?<Duration>(\d+)</Duration>', todo)]
        r['duracion_fotogramas'] = max(ends) if ends else None
    partes = []
    if r.get('mogrt', {}).get('parametros'): partes.append(f"plantilla para Premiere con {len(r['mogrt']['parametros'])} huecos/controles: " + ', '.join(x for x in r['mogrt']['parametros'] if x)[:200] + (f" ({r['mogrt']['duracion_s']} s)" if r['mogrt'].get('duracion_s') else ''))
    if medios: partes.append(f'usa {len(medios)} medios (' + ', '.join(medios[:6]) + (', …' if len(medios) > 6 else '') + ')')
    if r['efectos']: partes.append('efectos/ajustes: ' + ', '.join(r['efectos'][:8]))
    if modos: partes.append('modos de fusión: ' + ', '.join(modos))
    if r.get('duracion_fotogramas'): partes.append(f"línea de tiempo de {r['duracion_fotogramas']} fotogramas")
    r['resumen'] = 'leído por dentro: ' + ('; '.join(partes) if partes else 'sin datos legibles')
    return r

if __name__ == '__main__':
    for p in sys.argv[1:]:
        try: print(json.dumps(dict(archivo=p, **leer(p)), ensure_ascii=False))
        except Exception as e: print(json.dumps(dict(archivo=p, error=str(e)[:120]), ensure_ascii=False))
