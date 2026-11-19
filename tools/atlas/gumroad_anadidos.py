"""Gumroad re-descargado (Biblioteca/AÑADIDOS/GUMROAD, 19-11-2026) → originales nuevos.

Compara la lista md5 de lo descargado (gumroad/lista_md5_anadidos_2026-11-19.csv, sacada por REVISAR_GUMROAD.bat)
con MANIFIESTO.json. Lo que no estaba se añade en MANIFIESTO['gumroad_anadidos'] y como tareas de montaje
(se copia de AÑADIDOS/GUMROAD/... a originales/gumroad/...). Lo repetido no se toca.
"""
import csv, json

M = 'originales/MANIFIESTO.json'; MT = 'originales/montaje.json'
man = json.load(open(M)); mon = json.load(open(MT))
known = {e['md5'] for e in man['originales'] + man['heredado_neonizador']}
rows = list(csv.DictReader(open('gumroad/lista_md5_anadidos_2026-11-19.csv', encoding='utf-8-sig')))

def info(r):
    if r.startswith('Cyanotype'):
        t = r.split('/')[1]
        return ('Free Cyanotype Textures', 'imagen', 'cianotipia/' + r.split('/', 1)[1],
                'Textura animada de cianotipia pintada a mano y escaneada (%s, fotograma %s de 10), 1920×1080 PNG opaco' %
                (t.replace('_', ' '), r[-7:-4]))
    if r.startswith('SlitScanFx'):
        rel = r.split('SlitScanFx/SlitScanFx/', 1)[1]
        if rel.endswith('.aep'):
            return ('Easy Slit Scan Effect + AE Project', 'plantilla', 'slitscan/' + rel,
                    'Proyecto de After Effects del autor: Displacement Map con los mapas + Simple Choker + Camera Lens Blur')
        return ('Easy Slit Scan Effect + AE Project', 'video', 'slitscan/' + rel,
                'Mapa de desplazamiento slit-scan %s (%s): degradados en gris animados, 1080×1920, 24 fps, 4 s' %
                (rel.split('/')[-1][:-4], 'horizontal' if 'Horizontal' in rel else 'vertical'))
    rel = r.split('/TransitionPack4K_Gumroad/', 1)[1]
    if rel.startswith('Matte_MOVs'):
        return ('Textured Transition Pack', 'video', 'TransitionPack4K_Gumroad/' + rel,
                'Mate de la transición de tinta %s (ProRes 4444 XQ 4K con ALFA = tinta, RGB negro, 25 fps, 1 s)' % rel.split('/')[-1][:-4])
    return ('Textured Transition Pack', 'video', 'TransitionPack4K_Gumroad/' + rel,
            'Transición de tinta texturada %s en calidad original (ProRes 4444 XQ 4K, sin alfa); la que usaban los plugins era un MP4' %
            rel.split('/')[-1][:-4])

out = []; tareas = []
for x in rows:
    if x['md5'] in known: continue
    r = x['ruta'].replace('\\', '/')
    pack, tipo, dest, desc = info(r)
    src = 'AÑADIDOS/GUMROAD/' + r
    out.append(dict(id='or:' + x['md5'], md5=x['md5'], bytes=int(x['bytes']), tipo=tipo,
                    archivo='originales/gumroad/' + dest, desc=desc, autor='Studio DamDam', pack=pack,
                    licencia='Gumroad (Studio DamDam): uso propio, no redistribuir', origen_biblioteca=src))
    tareas.append(['originales/gumroad/' + dest, x['md5'], [src]])
man['gumroad_anadidos'] = out
man['gumroad_anadidos_nota'] = ('Re-descarga completa del 19-11-2026: %d de %d archivos ya estaban (mismo md5); estos %d son nuevos '
                                '(21 mates, 24 ProRes originales de las transiciones, Cyanotype y SlitScanFx).' %
                                (len(rows) - len(out), len(rows), len(out)))
mon['tareas'] = [t for t in mon['tareas'] if not t[0].startswith('originales/gumroad/')] + tareas
json.dump(man, open(M, 'w'), ensure_ascii=False, indent=1)
json.dump(mon, open(MT, 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(rows), 'descargados ·', len(out), 'nuevos ·', sum(o['bytes'] for o in out) / 1e9, 'GB')
