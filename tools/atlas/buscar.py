"""BUSCADOR DE LA BIBLIOTECA (v3, 20-11-2026) · ordena por lo que ENCAJA y devuelve un ABANICO VARIADO.
(La lógica está en biblioteca.py, que también pueden importar los scripts de construcción de los plugins.)

EMPIEZA AQUÍ:
  buscar.py --necesidades                      # catálogo de necesidades ya resueltas: listas curadas y revisadas a ojo
  buscar.py --necesidad papel_fondo_calido     # una necesidad: sus mejores opciones + su hoja de miniaturas ya hecha
  buscar.py papel viejo calido --ver           # buscar libre: abanico de 12 distintas + hoja JPG con miniaturas
  buscar.py mancha --papel pieza --ver         # por PAPEL: fondo repetible, superposicion, pieza, relieve, transicion,
                                               #   mascara, elemento animado, superposicion animada, sonido, lut…
  buscar.py --papeles                          # qué papeles hay y cuántos de cada uno
  buscar.py luz --fondo "sobre negro"          # por FONDO: transparente, sobre negro, sobre blanco, gris neutro
  buscar.py papel viejo --mas                  # otras 12 distintas (misma semilla)
  buscar.py --mapa                             # qué hay en toda la biblioteca
  buscar.py goteo --resumen                    # cuántos encajan por clase/sub y familia
  buscar.py --familia pieza_burbuja            # variantes de lo mismo
  buscar.py --parecidos ID · --ficha ID        # parecidas a una que ya te sirve · ficha completa
  buscar.py goteo --sin-usar                   # solo lo que no usa todavía ningún plugin
  buscar.py goteo --plugin cartelator --apuntar ID ID…   # deja constancia de lo que eliges

Cómo ordena: sinónimos (indice/sinonimos.json), inglés, plurales, frases; puntúa por la ficha revisada a ojo (qué es,
familia, clase, papel, uso, color, estilo); el objeto es obligatorio y color/tamaño/estilo matizan; la nota multiplica
pero no decide sola; una por familia y reparto por colección y aspecto, con azar (semilla en pantalla; --semilla N la
repite; --fijo la quita). Marca «ya lo usa: …» y lo baja un poco; lo bueno que nadie usa sube un poco.
Esconde REHACER, sustituidos, dudosos, copias y fuentes ya procesadas (--todo / --fuentes)."""
import json, sys, argparse, re, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from biblioteca import Biblioteca, VERSION, PAPELES, norm

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('palabras', nargs='*')
for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo', 'familia'):
    ap.add_argument('--' + k, help=f'filtra por {k} (empieza por)')
ap.add_argument('--papel', help="fondo repetible, superposicion, pieza, relieve, transicion, mascara, elemento animado, "
                                "superposicion animada, fondo animado, sonido, lut, plantilla, tutorial (varios: con comas)")
ap.add_argument('--fondo', help='transparente, sobre negro, sobre blanco, gris neutro, opaco')
ap.add_argument('--alfa', action='store_true'); ap.add_argument('--tileable', action='store_true')
ap.add_argument('--min', type=int, default=0, help='nota mínima (1–5)')
ap.add_argument('--mejor', action='store_true', help='solo el mejor de cada familia')
ap.add_argument('--relleno', action='store_true', help='solo partículas de relleno de fondo')
ap.add_argument('--estricto', action='store_true', help='todas las palabras obligatorias (también color/tamaño)')
ap.add_argument('--sin-usar', action='store_true', help='solo lo que no usa ningún plugin')
ap.add_argument('--todo', action='store_true'); ap.add_argument('--fuentes', action='store_true')
ap.add_argument('--donde', action='append', default=[], metavar='COND',
                help="'w>=2000' 'orient~vertical' 'color~rojo' 'medidas.luminancia<0.3' 'video.duracion<=3' 'video.loop=True'")
ap.add_argument('--excluir', action='append', default=[], metavar='ID[,ID…]')
ap.add_argument('-n', '--n', type=int, default=12)
ap.add_argument('--mas', action='count', default=0); ap.add_argument('--pagina', type=int, default=0)
ap.add_argument('--semilla', type=int); ap.add_argument('--fijo', action='store_true')
ap.add_argument('--lista', action='store_true', help='relevancia pura, sin repartir')
ap.add_argument('--ver', action='store_true', help='hoja JPG con miniaturas numeradas')
ap.add_argument('--plugin'); ap.add_argument('--apuntar', nargs='+', metavar='ID')
ap.add_argument('--incluir-usados', action='store_true')
ap.add_argument('--json', action='store_true'); ap.add_argument('--ficha'); ap.add_argument('--familia-de', metavar='ID')
ap.add_argument('--resumen', action='store_true'); ap.add_argument('--mapa', action='store_true')
ap.add_argument('--papeles', action='store_true'); ap.add_argument('--parecidos', metavar='ID')
ap.add_argument('--necesidades', nargs='?', const='', metavar='PALABRA', help='catálogo de necesidades (filtrable)')
ap.add_argument('--necesidad', metavar='NOMBRE')
ap.add_argument('--explicar', action='store_true'); ap.add_argument('--version', action='store_true')
a = ap.parse_args()
try:
    import signal; signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except Exception: pass
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass
if a.version: print('buscar.py v%d' % VERSION); sys.exit()

B = Biblioteca(); rv = B.rv
F = dict(clase=a.clase, sub=a.sub, modo=a.modo, colocacion=a.colocacion, coleccion=a.coleccion, pack=a.pack, tipo=a.tipo,
         familia=a.familia, papel=a.papel, fondo=a.fondo, alfa=a.alfa, tileable=a.tileable, min=a.min, mejor=a.mejor,
         relleno=a.relleno, sin_usar=a.sin_usar, estricto=a.estricto, todo=a.todo, fuentes=a.fuentes, donde=a.donde, plugin=a.plugin,
         incluir_usados=a.incluir_usados, excluir={i for x in a.excluir for i in x.split(',') if i})

if a.ficha:
    e = B.ficha(a.ficha); print(json.dumps(e, ensure_ascii=False, indent=1) if e else 'no existe ' + a.ficha); sys.exit()
if a.familia_de:
    e = B.ficha(a.familia_de)
    if not e: raise SystemExit('no existe ' + a.familia_de)
    a.familia = F['familia'] = rv(e).get('familia')
if a.apuntar:
    if not a.plugin: raise SystemExit('--apuntar necesita --plugin <nombre>')
    f, n, malos = B.apuntar(a.plugin, a.apuntar)
    for m in malos: print('AVISO: no existe', m)
    print(f'apuntados en {f}: {n} ids de {a.plugin}'); sys.exit()

def tam(e):
    v = rv(e); m = v.get('medidas') or {}
    w, h = e.get('w') or m.get('w'), e.get('h') or m.get('h')
    t = f'{w}×{h}' if w and h else ''
    vd = e.get('video') or {}
    if vd.get('duracion'): t += f' · {vd["duracion"]:.1f} s' + (' · loop' if vd.get('loop') else '')
    au = v.get('audio_medido') or {}
    if isinstance(au, dict) and au.get('duracion'): t += f' · {au["duracion"]:.1f} s'
    return t
def ensena(sel, explicar=None):
    for i, e in enumerate(sel, 1):
        v = rv(e); usos = sorted(B.usos.get(e['id'], set()))
        print(f"\n{i:2}. [{v.get('calidad') or '-'}/5] {e['id']}" + ('  ★mejor de su familia' if v.get('mejor_de_familia') else ''))
        print(f"    {v.get('que_es', '')}")
        det = [x for x in (e['_papel'], e.get('tipo'), tam(e), 'fondo ' + e['_fondo'],
                           ('modo ' + str(v.get('modo') or e.get('modo'))) if (v.get('modo') or e.get('modo')) else '',
                           v.get('color') or e.get('color'), v.get('estilo')) if x and x != '-']
        print('    ' + ' · '.join(map(str, det)))
        us, ev = v.get('usar_si'), v.get('evitar_si')
        if (us and us != '-') or (ev and ev != '-'): print(f"    usar si: {us or '-'} · evitar si: {ev or '-'}")
        if v.get('defectos') and v['defectos'] not in ('ninguno', '-') and not str(v['defectos']).startswith('(corregido'):
            print(f"    defectos: {v['defectos']}")
        if v.get('aviso'): print(f"    AVISO: {v['aviso']}")
        print(f"    archivo: {e.get('archivo', '')}")
        print(f"    familia: {v.get('familia', '-')}  (variantes: --familia {v.get('familia', '')})" + (f"   · ya lo usa: {', '.join(usos)}" if usos else '   · sin usar'))
        if explicar is not None and e['id'] in explicar:
            s, cob, por = explicar[e['id']]; print(f'    puntos {s:.2f} · cobertura {cob:.0%} · {"; ".join(por)}')
def hoja(sel, nombre):
    f = B.hoja(sel, nombre)
    if f: print(f'\nHOJA: {f}   ← ábrela con Read y elige MIRANDO (los números son los de la lista)')
    else: print('\n(--ver necesita Pillow: python -m pip install pillow)')
def slug(t): return re.sub(r'[^a-z0-9]+', '_', norm(t)).strip('_')[:50] or 'busqueda'

# ------------------------------------------------------------------ catálogo de necesidades
if a.necesidades is not None:
    q = norm(a.necesidades)
    ns = [n for n in B.NEC.get('necesidades', []) if not q or q in norm(json.dumps(n, ensure_ascii=False))]
    print(f"NECESIDADES YA RESUELTAS ({len(ns)}): listas curadas, revisadas a ojo, variadas y con hoja de miniaturas.")
    print("Abre una con --necesidad NOMBRE. Si ninguna encaja, busca libre (buscar.py palabras --ver).\n")
    grupo = None
    for n in ns:
        if n.get('grupo') != grupo: grupo = n.get('grupo'); print(f'— {grupo}')
        print(f"   {n['nombre']:34} {n.get('titulo', '')}  ({len(n.get('ids', []))})")
    sys.exit()
if a.necesidad:
    if a.necesidad not in B.nec:
        cand = [k for k in B.nec if norm(a.necesidad) in norm(k)]
        raise SystemExit(f'no existe la necesidad {a.necesidad}' + (f'; ¿quizá {", ".join(cand)}?' if cand else '; mira --necesidades'))
    nd = B.nec[a.necesidad]; sel = B.necesidad(a.necesidad)
    if a.json: print(json.dumps(sel, ensure_ascii=False, indent=1)); sys.exit()
    print(f"NECESIDAD {nd['nombre']}: {nd.get('titulo', '')}")
    if nd.get('como'): print(f"Cómo se usa: {nd['como']}")
    print(f"{len(sel)} opciones revisadas a ojo, de {len({rv(e).get('familia') for e in sel})} familias, "
          f"{dict(collections.Counter(e['coleccion'] for e in sel))}. Todas valen: elige por lo que necesitas.")
    ensena(sel)
    h = nd.get('hoja')
    if h:
        for c in B.donde(h):
            if c.exists(): print(f'\nHOJA YA HECHA: {c}   ← ábrela con Read'); break
    if a.ver: hoja(sel, 'necesidad_' + nd['nombre'])
    print(f"\n— Más de lo mismo: buscar.py {nd.get('consulta', '')} --ver (abanico nuevo) · variantes: --familia NOMBRE")
    sys.exit()
if a.papeles:
    c = collections.Counter(e['_papel'] for e in B.idx if B.pasa(e, {}))
    print('PAPELES (qué función cumple cada recurso; filtra con --papel):')
    for p, k in c.most_common(): print(f'  {k:5}  {p:24} {PAPELES.get(p, "")}')
    sys.exit()
if a.mapa:
    c = collections.Counter((B.clase(e), (e.get('sub') or '').split('/')[0]) for e in B.idx if B.pasa(e, {}))
    ej = {}
    for e in B.idx:
        k = (B.clase(e), (e.get('sub') or '').split('/')[0])
        if k not in ej and B.pasa(e, {}) and (rv(e).get('calidad') or 4) >= 4: ej[k] = rv(e).get('que_es', '')[:60]
    porclase = collections.Counter()
    for (cl, _), n in c.items(): porclase[cl] += n
    print(f'BIBLIOTECA: {sum(c.values())} recursos utilizables. Antes de buscar libre, mira --necesidades. Por clase:')
    for cl, n in porclase.most_common():
        print(f'\n{cl}  ({n})   → buscar.py --clase {cl}')
        for (c1, s), m in sorted(((k, m) for k, m in c.items() if k[0] == cl), key=lambda x: -x[1])[:14]:
            print(f'   {m:5}  {s or "—":28} p. ej.: {ej.get((c1, s), "")}')
    print('\nColecciones:', dict(collections.Counter(e['coleccion'] for e in B.idx if B.pasa(e, {}))))
    print('Papeles: buscar.py --papeles')
    sys.exit()
if a.parecidos:
    if a.parecidos not in B.por_id: raise SystemExit('no existe ' + a.parecidos)
    sel = B.parecidos(a.parecidos, a.n, **F)
    if a.json: print(json.dumps(sel, ensure_ascii=False, indent=1)); sys.exit()
    print(f'Parecidos a {a.parecidos}:'); ensena(sel)
    if a.ver: hoja(sel, 'parecidos_' + slug(a.parecidos))
    sys.exit()

# ------------------------------------------------------------------ búsqueda libre
pagina = a.pagina + a.mas
if a.resumen:
    res, _, _ = B.puntuar_todo(a.palabras, **F)
    c1 = collections.Counter(f"{B.clase(e)}/{e.get('sub', '—')}" for _, e, _, _ in res)
    c2 = collections.Counter(rv(e).get('familia', '—') for _, e, _, _ in res)
    c3 = collections.Counter(e['coleccion'] for _, e, _, _ in res); c4 = collections.Counter(e['_papel'] for _, e, _, _ in res)
    print(f'{len(res)} encajan · {len(c2)} familias · colecciones {dict(c3)}\nPor papel: {dict(c4.most_common())}\nPor clase/sub:')
    for k, n in c1.most_common(40): print(f'  {n:5}  {k}')
    print('Familias (ábrelas con --familia NOMBRE):')
    for k, n in c2.most_common(60): print(f'  {n:5}  {k}')
    sys.exit()
R = B.buscar(a.palabras, n=a.n, pagina=pagina, semilla=a.semilla, fijo=a.fijo, lista=a.lista, **F)
if a.json: print(json.dumps(R.sel, ensure_ascii=False, indent=1)); sys.exit()
fams = {rv(e).get('familia') for _, e, _, _ in R.res}
print(f'«{" ".join(a.palabras)}»: {len(R.res)} encajan · {len(fams)} familias · {dict(collections.Counter(e["coleccion"] for _, e, _, _ in R.res))}'
      + ('' if (a.lista or a.familia) else f' · abanico variado, semilla {R.semilla}') + (f' · tanda {pagina + 1}' if pagina else ''))
from biblioteca import raiz, toks
con, _ = B.conceptos(a.palabras)
def _encaja(n):
    rs = {raiz(t) for t in toks(n['nombre'].replace('_', ' ') + ' ' + n.get('titulo', '') + ' ' + n.get('consulta', '').split(' --')[0].replace('|', ' '))}
    return sum(any(all(x in rs for x in fr) for fr, _ in var) for var in con)
_sc = sorted(((_encaja(n), n['nombre']) for n in B.NEC.get('necesidades', [])), reverse=True)
sug = [nm for sc, nm in _sc if con and sc == len(con)][:4] or [nm for sc, nm in _sc if con and sc >= 1 and sc == _sc[0][0]][:3]
if sug: print(f'  Necesidades ya resueltas que pueden servir: {", ".join(sug)}  (--necesidad NOMBRE)')
for x in R.avisos: print('  (' + x + ')')
if not R.res: print('Nada. Prueba otras palabras (sinónimos, inglés, el material o el uso), quita filtros o mira --necesidades / --mapa.')
ensena(R.sel, {e['id']: (s, c, p) for s, e, c, p in R.res} if a.explicar else None)
if a.ver and R.sel:
    hoja(R.sel, slug(' '.join(a.palabras) or a.familia or 'busqueda') + f'_{R.semilla}' + (f'_t{pagina + 1}' if pagina else ''))
if R.res and not (a.lista or a.familia):
    print('\n— Es un abanico: todas encajan; la 1 no es «la buena». Mira (--ver), compara y elige por lo que necesitas.'
          f'\n— Más: --mas · Otra mezcla: sin --semilla · Repetir: --semilla {R.semilla} · Variantes: --familia NOMBRE'
          ' · Parecidas: --parecidos ID · Ficha: --ficha ID · Solo sin usar: --sin-usar')
