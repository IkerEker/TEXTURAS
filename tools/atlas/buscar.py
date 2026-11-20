"""Buscar en el atlas usando las fichas de la revisión 100 % (campo `revision` de cada asset).
Funciona desde cualquier carpeta (lee el índice junto a este script).

  python3 tools/atlas/buscar.py papel acuarela                 # palabras en id, ruta, clase, sub, pack y en la ficha
                                                               # (qué es, uso, usar si, color, estilo, familia…)
  python3 tools/atlas/buscar.py goteo --clase productos --min 4 --mejor
  python3 tools/atlas/buscar.py --clase video --sub transiciones/luz --modo trama
  python3 tools/atlas/buscar.py --colocacion mascara --alfa --json      # salida JSON para scripts
  python3 tools/atlas/buscar.py --ficha tx:productos/piezas_neonizador/gotas/gotas_111   # ficha completa
  python3 tools/atlas/buscar.py --familia pieza_burbuja        # toda una familia, mejor primero

Por defecto: ordena por nota (5 → 1) y mejor de familia primero; oculta lo marcado REHACER y lo sustituido
(usa --todo para verlo todo). Los alias en inglés/de plugins se traducen con indice/nombres.json.
La ficha no sustituye a mirar: abre la `hoja` antes de elegir."""
import json, sys, argparse, unicodedata
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser()
ap.add_argument('palabras', nargs='*')
for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo', 'familia'): ap.add_argument('--' + k)
ap.add_argument('--alfa', action='store_true'); ap.add_argument('--tileable', action='store_true')
ap.add_argument('--min', type=int, default=0, help='nota mínima de la revisión (1–5)')
ap.add_argument('--mejor', action='store_true', help='solo el mejor de cada familia')
ap.add_argument('--todo', action='store_true', help='incluir REHACER, sustituidos y dudosos')
ap.add_argument('--json', action='store_true'); ap.add_argument('--ficha')
ap.add_argument('-n', type=int, default=40)
a = ap.parse_args()
idx = json.load(open(R / 'indice' / 'indice.json', encoding='utf-8'))['assets']
if a.ficha:
    for e in idx:
        if e['id'] == a.ficha: print(json.dumps(e, ensure_ascii=False, indent=1))
    sys.exit()
al = json.load(open(R / 'indice' / 'nombres.json', encoding='utf-8'))['alias']
def norm(t):  # sin acentos, minúsculas, _ → espacio
    return ''.join(c for c in unicodedata.normalize('NFD', t.lower()) if unicodedata.category(c) != 'Mn').replace('_', ' ')
EXTRA = {'fire': 'fuego', 'paper': 'papel', 'water': 'agua', 'ink': 'tinta', 'stain': 'mancha', 'tape': 'cinta',
         'texture': 'textura', 'light': 'luz', 'leak': 'fuga', 'film': 'pelicula', 'grain': 'grano', 'scratch': 'rayado',
         'splash': 'salpicadura', 'splatter': 'salpicadura', 'brush': 'pincel', 'pencil': 'lapiz', 'charcoal': 'carbon',
         'wood': 'madera', 'wall': 'pared', 'glass': 'vidrio', 'rain': 'lluvia', 'foam': 'espuma', 'mold': 'moho',
         'spark': 'chispa', 'bubble': 'burbuja', 'flame': 'llama', 'dust': 'polvo', 'pompa': 'burbuja', 'ember': 'brasa', 'sound': 'sonido', 'transition': 'transicion', 'fold': 'pliegue',
         'crumpled': 'arrugado', 'torn': 'rasgado', 'edge': 'borde', 'coffee': 'cafe', 'rust': 'oxido', 'drop': 'gota'}
def raices(w):  # plural → singulares posibles: llamas→llama, papeles→papel, luces→luz, bubbles→bubble
    r = {w}
    if len(w) > 3 and w.endswith('s'): r.add(w[:-1])
    if len(w) > 4 and w.endswith('es') and w[-3] not in 'aeiou': r.add(w[:-2])
    if len(w) > 4 and w.endswith('ces'): r.add(w[:-3] + 'z')
    return r
pal = []  # cada palabra = conjunto de variantes (ella, su singular, su alias, su traducción); basta con una
for p in a.palabras:
    w = p.lower(); vs = raices(w)
    for x in list(vs):
        for t in (al.get(x), EXTRA.get(x)):
            if t: vs |= raices(t)
    pal.append({norm(v) for v in vs})
CAMPOS_FICHA = ('que_es', 'uso', 'usar_si', 'color', 'estilo', 'familia', 'diferencia', 'orient', 'escala', 'comportamiento')
r = []
for e in idx:
    v = e.get('revision', {})
    if any(getattr(a, k) and not str(e.get(k, '')).startswith(getattr(a, k)) for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo')): continue
    if a.familia and v.get('familia') != a.familia: continue
    if a.alfa and not e.get('alfa'): continue
    if a.tileable and not (e.get('tileable') or v.get('tileable')): continue
    if not a.todo and (v.get('rehacer') or e.get('sustituido_por') or v.get('dudoso')): continue
    if (v.get('calidad') or 0) < a.min: continue
    if a.mejor and not v.get('mejor_de_familia'): continue
    txt = ' '.join([str(e.get(k, '')) for k in ('id', 'desc', 'clase', 'sub', 'pack', 'archivo', 'familia')] +
                   [str(v.get(k, '')) for k in CAMPOS_FICHA])
    txt = norm(txt)
    if all(any(v in txt for v in vs) for vs in pal): r.append(e)
r.sort(key=lambda e: (-(e.get('revision', {}).get('calidad') or 0), not e.get('revision', {}).get('mejor_de_familia')))
if a.json:
    print(json.dumps(r[:a.n], ensure_ascii=False, indent=1)); sys.exit()
for e in r[:a.n]:
    v = e.get('revision', {})
    print(f"{v.get('calidad', '-')}{'*' if v.get('mejor_de_familia') else ' '} {e['id']:66} {(e.get('modo') or ''):10} {v.get('que_es', '')[:70]}")
    if v.get('usar_si') not in (None, '-') or v.get('evitar_si') not in (None, '-'):
        print(f"      usar si: {v.get('usar_si', '-')} · evitar si: {v.get('evitar_si', '-')} · hoja: {v.get('hoja') or e.get('hoja')}")
print(f'— {len(r)} resultados (nota, * = mejor de su familia)' + ('' if a.todo else '; ocultos REHACER/sustituidos/dudosos: --todo'))
