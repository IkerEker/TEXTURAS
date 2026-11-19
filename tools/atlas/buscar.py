"""Buscar en el atlas. Uso:
  python3 tools/atlas/buscar.py papel acuarela            # palabras (en id, desc, clase, sub, pack, nombre)
  python3 tools/atlas/buscar.py --clase video --sub transiciones/luz --modo trama
  python3 tools/atlas/buscar.py --colocacion mascara --alfa
Los alias en inglés/de plugins se traducen con indice/nombres.json."""
import json, sys, argparse
ap = argparse.ArgumentParser(); ap.add_argument('palabras', nargs='*')
for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo'): ap.add_argument('--' + k)
ap.add_argument('--alfa', action='store_true'); ap.add_argument('--tileable', action='store_true'); ap.add_argument('-n', type=int, default=40)
a = ap.parse_args()
idx = json.load(open('indice/indice.json'))['assets']
al = json.load(open('indice/nombres.json'))['alias']
pal = [al.get(p.lower(), p.lower()) for p in a.palabras]
r = []
for e in idx:
    if any(getattr(a, k) and not str(e.get(k, '')).startswith(getattr(a, k)) for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo')): continue
    if a.alfa and not e.get('alfa'): continue
    if a.tileable and not e.get('tileable'): continue
    txt = ' '.join(str(e.get(k, '')) for k in ('id', 'desc', 'clase', 'sub', 'pack', 'archivo', 'familia')).lower().replace('_', ' ')
    if all(p.replace('_', ' ') in txt for p in pal): r.append(e)
for e in r[:a.n]:
    print(f"{e['id']:70} {e.get('modo') or '':12} {e.get('archivo')}")
print(f'— {len(r)} resultados')
