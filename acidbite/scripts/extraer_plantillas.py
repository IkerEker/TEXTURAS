"""Lee los proyectos de Premiere de ACIDBITE (.prproj) y saca, por secuencia, qué clip va en qué pista,
cuándo, con qué modo de fusión y efectos. Uso: python3 extraer_plantillas.py <carpeta_con_prproj.xml> <salida.json>"""
import sys, re, json, glob, os, importlib.util
spec = importlib.util.spec_from_file_location('lp', os.path.join(os.path.dirname(__file__), 'leer_prproj.py'))
BLEND = {0: 'normal', 1: 'dissolve', 3: 'darken', 4: 'multiply', 5: 'color burn', 6: 'linear burn', 7: 'darker color',
         9: 'lighten', 10: 'screen', 11: 'color dodge', 12: 'linear dodge (add)', 13: 'lighter color',
         15: 'overlay', 16: 'soft light', 17: 'hard light', 18: 'vivid light', 19: 'linear light', 20: 'pin light',
         21: 'hard mix', 23: 'difference', 24: 'exclusion', 25: 'subtract', 26: 'divide',
         28: 'hue', 29: 'saturation', 30: 'color', 31: 'luminosity'}
import xml.etree.ElementTree as ET
src = open(os.path.join(os.path.dirname(__file__), 'leer_prproj.py')).read().split('def main(p):')[0]
ns = {}; exec(src, ns)
def secuencias(p):
    root, byid, byuid = ns['load'](p)
    out = {}
    for seq in root.iter('Sequence'):
        name = seq.findtext('Name')
        tg = ns['ref'](seq.find('.//TrackGroups/TrackGroup/Second'), byid, byuid)
        if not name or tg is None: continue
        capas = []
        for ti_, t in enumerate(tg.iter('Track')):
            tr = ns['ref'](t, byid, byuid)
            if tr is None or 'Video' not in tr.tag: continue
            for it in tr.iter('TrackItem'):
                ti = ns['ref'](it, byid, byuid)
                if ti is None or 'VideoClipTrackItem' not in ti.tag: continue
                st = int(ti.findtext('.//TrackItem/Start') or 0) / ns['TICKS']
                en = int(ti.findtext('.//TrackItem/End') or 0) / ns['TICKS']
                mn, kind = ns['media_name'](ti, byid, byuid)
                modo, opac, efectos = 'normal', 100.0, []
                for m, pr in ns['effects'](ti, byid, byuid):
                    short = m.replace('AE.ADBE ', '').replace('PR.ADBE ', '')
                    if short == 'Opacity':
                        try: modo = BLEND.get(int(float(pr.get('Blend Mode', 0))), pr.get('Blend Mode'))
                        except ValueError: pass
                        try: opac = float(pr.get('Opacity', 100))
                        except ValueError: pass
                    elif short not in ('Motion',):
                        efectos.append(short)
                capas.append(dict(pista=ti_ + 1, inicio_s=round(st, 3), fin_s=round(en, 3), clip=mn, anidada=bool(kind),
                                  modo=modo, opacidad=opac, efectos=efectos))
        if capas:
            capas.sort(key=lambda c: (c['inicio_s'], c['pista']))
            # copias usadas como mate: mismo clip, mismo tramo, sin modo, en la pista justo debajo de la visible
            for c in capas:
                for d in capas:
                    if d is not c and not d['anidada'] and not re.search(r'adjustment|footage|shot', d['clip'] or '', re.I) and d['clip'] == c['clip'] and d['inicio_s'] == c['inicio_s'] and d['pista'] == c['pista'] - 1 \
                            and d['modo'] == 'normal' and c['modo'] != 'normal':
                        d['rol'] = 'mate (Track Matte del plano entrante)'; c['rol'] = 'copia visible'
            seg = [c for c in capas if re.search(r'second|shot ?2', c['clip'] or '', re.I)]
            corte = min(c['inicio_s'] for c in seg) if seg else None
            out[name] = dict(capas=capas, corte_s=corte)
    return out
res = {}
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.prproj.xml'))):
    s = secuencias(f)
    if s: res[os.path.basename(f).replace('.xml', '')] = s
json.dump(res, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
print({k: len(v) for k, v in res.items()})
