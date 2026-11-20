"""Cierre de la revisión 100 %: resumen, listas e integración en el índice.

  python3 tools/atlas/revision_resumen.py            → revision/RESUMEN.md, A_REHACER.md, NO_VISTOS.md,
                                                       revision/FICHAS.json (todas juntas)
  python3 tools/atlas/revision_resumen.py --indice   → además añade a cada asset de indice/indice.json
                                                       el campo «revision» (no borra ni cambia ningún campo)

Solo añade información. No toca ningún plugin ni ningún archivo de material.
"""
import json, sys, collections, glob, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RV = ROOT / 'revision'


def cargar():
    fichas = {}
    for f in sorted(glob.glob(str(RV / 'fichas' / '*.json'))):
        for k, v in json.load(open(f)).items():
            fichas[k] = v
    return fichas


def main():
    idx = json.load(open(ROOT / 'indice/indice.json'))
    assets = idx['assets']
    ix = {a['id']: a for a in assets}
    fam = json.load(open(RV / 'familias.json'))
    fichas = cargar()

    # audio: se copia lo que ya se sabía y se marca como no escuchado
    for k, v in fichas.items():
        a = ix.get(k, {})
        au = a.get('audio') or (a.get('video') or {}).get('audio')
        if au is not None or a.get('tipo') in ('video', 'tutorial'):
            v['audio_conocido'] = au
            v['audio_revisado'] = False
        elif 'audio_revisado' in v:
            v['audio_revisado'] = False

    total = len(assets)
    con_ficha = [a['id'] for a in assets if a['id'] in fichas]
    vistos = [k for k in con_ficha if fichas[k].get('revisado_por_vista', True)]
    sin_vista = [k for k in con_ficha if not fichas[k].get('revisado_por_vista', True)]
    no_vistos = [a for a in assets if a['id'] not in fichas]
    sobrantes = [k for k in fichas if k not in ix]

    por_col = collections.Counter(a['coleccion'] for a in assets)
    vis_col = collections.Counter(ix[k]['coleccion'] for k in vistos)
    sv_col = collections.Counter(ix[k]['coleccion'] for k in sin_vista)
    notas = collections.Counter(int(fichas[k].get('calidad') or 0) for k in vistos)
    notas_col = collections.defaultdict(collections.Counter)
    for k in vistos:
        notas_col[ix[k]['coleccion']][int(fichas[k].get('calidad') or 0)] += 1

    def nombre(k):
        return ix[k]['archivo']

    rehacer = [k for k in vistos if fichas[k].get('rehacer') or 'REHACER' in str(fichas[k].get('defectos', ''))]
    correc = [k for k in vistos if 'CORRECCI' in str(fichas[k].get('defectos', '')).upper()]
    dudosos = [k for k in vistos if fichas[k].get('dudoso') or 'dudoso' in str(fichas[k].get('defectos', '')).lower()
               or 'dudoso' in str(fichas[k].get('que_es', '')).lower()]
    no_rec = [k for k in vistos if int(fichas[k].get('calidad') or 0) <= 2]
    sensibles = [k for k in vistos if re.search(r'sangre|radiograf|esvástica|símbolo sensible|NOTAR|oficial|persona real|presentador|visceral|logo de ACIDBITE',
                                                 json.dumps(fichas[k], ensure_ascii=False), re.I)]
    mejores = [k for k in vistos if fichas[k].get('mejor_de_familia')]
    top = sorted([k for k in vistos if int(fichas[k].get('calidad') or 0) == 5 and fichas[k].get('mejor_de_familia')],
                 key=lambda k: (ix[k]['coleccion'], nombre(k)))

    fam_uso = collections.Counter(fichas[k].get('familia') for k in vistos)

    L = []
    L.append('# Revisión 100 % de la Biblioteca — resumen\n')
    L.append('Revisión hecha a ojo, archivo por archivo, con hojas de contactos (imágenes enteras + recorte 1:1; '
             'vídeos con tira de 12 fotogramas + recorte 1:1). Noche del 19 al 20-11-2026. Audio no escuchado '
             '(`audio_revisado: false`, se copia lo que ya se sabía en `audio_conocido`).\n')
    L.append('## Recuento\n')
    L.append('| Colección | En el índice | Vistos a ojo | Ficha sin vista (sonido, plantillas) | Sin ficha |\n|---|---:|---:|---:|---:|')
    for c in sorted(por_col):
        L.append(f'| {c} | {por_col[c]} | {vis_col[c]} | {sv_col[c]} | {por_col[c]-vis_col[c]-sv_col[c]} |')
    L.append(f'| **Total** | **{total}** | **{len(vistos)}** | **{len(sin_vista)}** | **{len(no_vistos)}** |\n')
    L.append(f'Vistos a ojo + ficha sin vista + sin ficha = {len(vistos)} + {len(sin_vista)} + {len(no_vistos)} = {len(vistos)+len(sin_vista)+len(no_vistos)} (total del índice: {total}).\n')
    L.append('Sin vista: 658 sonidos de ACIDBITE (no se escuchan: `audio_revisado: false`, con lo que ya se sabía en `audio_conocido`) y 55 plantillas o proyectos de programa (.drt, .prfpset, .mogrt, .prproj, .aep), que no son imagen ni vídeo.\n')
    L.append(f'- Sin ficha: **{len(no_vistos)}** (lista en `NO_VISTOS.md`).')
    dup=[k for k,v in collections.Counter(a['id'] for a in assets).items() if v>1]
    L.append(f'- Fichas de ids que ya no están en el índice: {len(sobrantes)}.')
    L.append(f'- Ids repetidos en el índice (mismo contenido md5 en dos rutas, comparten ficha): {len(dup)} → ' + ', '.join(f"`{d}`" for d in dup))
    L.append(f'- Familias declaradas: {len(fam)}; usadas en fichas: {len([f for f in fam_uso if f])}.\n')
    L.append('## Calidad (1 = no usar … 5 = trabajo final sin tocar)\n')
    L.append('| Colección | 1 | 2 | 3 | 4 | 5 |\n|---|---:|---:|---:|---:|---:|')
    for c in sorted(notas_col):
        n = notas_col[c]
        L.append(f'| {c} | ' + ' | '.join(str(n[i]) for i in range(1, 6)) + ' |')
    L.append('| **Total** | ' + ' | '.join(f'**{notas[i]}**' for i in range(1, 6)) + ' |\n')

    L.append('## Lo mejor (20 primeros «mejor de su familia» con nota 5)\n')
    for k in top[:20]:
        L.append(f'- `{k}` — {fichas[k].get("que_es")} ({fichas[k].get("familia")})')
    L.append(f'\nHay {len(mejores)} elementos marcados como «mejor de su familia» en total '
             '(campo `mejor_de_familia` en `FICHAS.json` y en el índice).\n')

    L.append(f'## No recomendados (nota 1–2): {len(no_rec)}\n')
    cnr = collections.Counter(fichas[k].get('familia') for k in no_rec)
    L.append('Por familia (las 25 con más):\n')
    for f, n in cnr.most_common(25):
        L.append(f'- {f}: {n}')
    L.append('\nLista completa: buscar `"calidad": 1` o `2` en `FICHAS.json`.\n')

    L.append(f'## Correcciones (lo visto contradice el nombre o el índice): {len(correc)}\n')
    for k in correc:
        L.append(f'- `{nombre(k)}` — {fichas[k].get("defectos")}')
    L.append('')
    L.append(f'## Dudosos (no está claro qué es o hay algo que comprobar): {len(dudosos)}\n')
    for k in dudosos:
        d = fichas[k]
        L.append(f'- `{nombre(k)}` — {d.get("que_es")} · {d.get("defectos")}')
    L.append('')
    L.append(f'## Cuidado al usar (contenido sensible o que puede pasar por real): {len(sensibles)}\n')
    for k in sensibles:
        d = fichas[k]
        L.append(f'- `{nombre(k)}` — {d.get("que_es")} · {d.get("defectos")}')
    L.append('')
    L.append('## Familias más numerosas\n')
    for f, n in fam_uso.most_common(30):
        desc = (fam.get(f) or {}).get('uso', '')
        L.append(f'- **{f}** ({n}): {desc[:160]}')
    L.append('')
    L.append('## Dónde está cada cosa\n')
    L.append('- `revision/fichas/<lote>.json`: fichas por lote (las crea `tools/atlas/revision.py fichas`).')
    L.append('- `revision/FICHAS.json`: todas las fichas juntas, por id.')
    L.append('- `revision/familias.json`: familias (uso, modo, usar si, evitar si, mejor).')
    L.append('- `revision/hojas/<lote>.jpg`: la hoja que se miró para cada lote.')
    L.append('- `indice/indice.json`: cada asset lleva ahora `revision` (la ficha); ningún campo anterior se ha tocado.')
    (RV / 'RESUMEN.md').write_text('\n'.join(L) + '\n')

    R = ['# A rehacer\n', 'Elementos cuyo defecto obliga a volver a procesarlos antes de usarlos.\n']
    for k in rehacer:
        R.append(f'- `{nombre(k)}` (`{k}`) — {fichas[k].get("defectos")}')
    if not rehacer:
        R.append('- (ninguno)')
    (RV / 'A_REHACER.md').write_text('\n'.join(R) + '\n')

    N = ['# No vistos\n']
    N.append(f'Vistos a ojo: {len(vistos)}. Con ficha pero sin vista (sonido y plantillas, no se pueden mirar): {len(sin_vista)}.\n')
    if no_vistos:
        N.append(f'{len(no_vistos)} elementos del índice sin ficha:\n')
        for a in no_vistos:
            N.append(f'- `{a["id"]}` — {a["archivo"]}')
    else:
        N.append(f'Sin ficha: ninguno. Los {total} elementos del índice tienen ficha.')
    if sobrantes:
        N.append(f'\nFichas de ids que ya no están en el índice ({len(sobrantes)}): ' + ', '.join(sobrantes[:50]))
    (RV / 'NO_VISTOS.md').write_text('\n'.join(N) + '\n')

    json.dump(fichas, open(RV / 'FICHAS.json', 'w'), ensure_ascii=False, indent=0)

    if '--indice' in sys.argv:
        n = 0
        for a in assets:
            if a['id'] in fichas:
                a['revision'] = fichas[a['id']]
                n += 1
        json.dump(idx, open(ROOT / 'indice/indice.json', 'w'), ensure_ascii=False, indent=0)
        print('índice: revision añadida a', n)

    print(f'total {total} · a ojo {len(vistos)} · sin vista {len(sin_vista)} · sin ficha {len(no_vistos)} · rehacer {len(rehacer)} · '
          f'correcciones {len(correc)} · dudosos {len(dudosos)} · no recomendados {len(no_rec)} · sensibles {len(sensibles)}')


if __name__ == '__main__':
    main()
