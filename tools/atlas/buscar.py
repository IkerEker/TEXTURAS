"""BUSCADOR DE LA BIBLIOTECA (v2, 20-11-2026) · ordena por lo que ENCAJA y devuelve un ABANICO VARIADO.

Uso rápido (desde cualquier carpeta; en Windows: python TEXTURAS\\tools\\atlas\\buscar.py …):

  buscar.py papel viejo calido                 # abanico de 12 opciones distintas entre sí (familias, colecciones, aspecto)
  buscar.py papel viejo calido --ver           # + hoja JPG con las miniaturas numeradas (ábrela con Read y ELIGE MIRANDO)
  buscar.py papel viejo calido --mas           # otras 12 distintas de las anteriores (misma semilla)
  buscar.py fuego --n 30 --ver                 # más amplio
  buscar.py --mapa                             # qué hay en toda la biblioteca (clases, subclases, cuántos)
  buscar.py goteo --resumen                    # cuántos encajan en cada clase/sub y familia
  buscar.py --familia pieza_burbuja            # una familia entera (variantes de lo mismo)
  buscar.py --parecidos <id>                   # alternativas que se parecen a una que ya te sirve
  buscar.py --ficha <id>                       # ficha completa de un asset
  buscar.py transicion --clase video --alfa --min 4 --donde 'orient~vertical'    # filtros (ver --help)
  buscar.py goteo --plugin cartelator --apuntar tx:manchas/goteos/fina/goteo_157  # deja constancia de lo que eliges

Cómo funciona:
- Cada palabra se amplía con sinónimos (indice/sinonimos.json), inglés, plurales y género. No hace falta que estén
  todas: puntúa más lo que cumple más palabras y lo que las tiene en «qué es» / familia / clase que en una nota suelta.
  Las palabras raras pesan más que las comunes («acuarela» más que «papel»).
- La nota (1–5) multiplica, pero NO decide sola: hay 4.000+ con nota 5.
- El abanico elige uno por familia y reparte entre colecciones (TEXTURAS, ACIDBITE, originales), clases y aspecto
  (pHash), con algo de azar (la semilla sale en pantalla; --semilla N la repite, --fijo la quita).
- Marca lo que ya usa algún plugin («ya lo usa: …») y lo baja un poco, para que no todos los plugins acaben con lo mismo.
- Esconde lo marcado REHACER, sustituido, dudoso o copia idéntica, y las FUENTES ya procesadas (el original del que
  sale un tx: limpio): --todo / --fuentes para verlas.
El texto no sustituye a mirar: usa --ver y abre la hoja, o la `hoja` de cada asset."""
import json, sys, argparse, unicodedata, re, math, random, collections, operator, os
from pathlib import Path

VERSION = 2
R = Path(__file__).resolve().parents[2]          # …/TEXTURAS
BIB = Path(os.environ.get('TEXTURAS_ROOT') or R.parent)   # …/Biblioteca (las rutas `archivo` son relativas a ella)

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument('palabras', nargs='*')
for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo', 'familia'):
    ap.add_argument('--' + k, help=f'filtra por {k} (empieza por)')
ap.add_argument('--alfa', action='store_true', help='solo con transparencia')
ap.add_argument('--tileable', action='store_true', help='solo repetibles')
ap.add_argument('--min', type=int, default=0, help='nota mínima (1–5)')
ap.add_argument('--mejor', action='store_true', help='solo el mejor de cada familia')
ap.add_argument('--relleno', action='store_true', help='solo piezas de relleno de fondo (partículas para usar en masa)')
ap.add_argument('--todo', action='store_true', help='incluir REHACER, sustituidos, dudosos y copias')
ap.add_argument('--fuentes', action='store_true', help='incluir originales ya procesados (fuentes de un tx:)')
ap.add_argument('--donde', action='append', default=[], metavar='COND',
                help="filtro por cualquier campo, también de la ficha: 'w>=2000' 'orient~vertical' 'color~rojo' "
                     "'medidas.luminancia<0.3' 'fondo=transparente' 'video.duracion<=3'")
ap.add_argument('--excluir', action='append', default=[], metavar='ID[,ID…]', help='quitar estos ids')
ap.add_argument('-n', '--n', type=int, default=12, help='cuántos enseñar (abanico de 12 por defecto)')
ap.add_argument('--mas', action='count', default=0, help='la siguiente tanda (repetible: --mas --mas)')
ap.add_argument('--pagina', type=int, default=0, help='tanda N (0 = la primera)')
ap.add_argument('--semilla', type=int, help='repetir exactamente un abanico (sale en pantalla)')
ap.add_argument('--fijo', action='store_true', help='sin azar: siempre el mismo orden')
ap.add_argument('--lista', action='store_true', help='lista por relevancia pura, sin repartir por variedad')
ap.add_argument('--ver', action='store_true', help='hace una hoja JPG con miniaturas numeradas de lo que sale')
ap.add_argument('--plugin', help='tu plugin: marca lo que tú ya usas y lo que usan los demás')
ap.add_argument('--apuntar', nargs='+', metavar='ID', help='apunta ids como usados por --plugin (Biblioteca/_uso/)')
ap.add_argument('--incluir-usados', action='store_true', help='no penalizar lo que ya usan otros plugins')
ap.add_argument('--json', action='store_true', help='salida JSON (los assets completos)')
ap.add_argument('--ficha', help='ficha completa de un id')
ap.add_argument('--familia-de', metavar='ID', help='la familia entera de un id')
ap.add_argument('--resumen', action='store_true', help='cuántos encajan por clase/sub y familia')
ap.add_argument('--mapa', action='store_true', help='mapa de toda la biblioteca')
ap.add_argument('--parecidos', metavar='ID', help='los más parecidos a ese asset')
ap.add_argument('--explicar', action='store_true', help='enseña por qué puntúa cada resultado')
ap.add_argument('--version', action='store_true')
a = ap.parse_args()
if a.version:
    print('buscar.py v%d' % VERSION); sys.exit()
try:
    import signal; signal.signal(signal.SIGPIPE, signal.SIG_DFL)
except Exception: pass
if hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8')
    except Exception: pass

idx = json.load(open(R / 'indice' / 'indice.json', encoding='utf-8'))['assets']
POR_ID = {e['id']: e for e in idx}
def rv(e): return e.get('revision') or {}

# ------------------------------------------------------------------ fichas sueltas
if a.ficha:
    e = POR_ID.get(a.ficha)
    print(json.dumps(e, ensure_ascii=False, indent=1) if e else 'no existe ' + a.ficha); sys.exit()
if a.familia_de:
    e = POR_ID.get(a.familia_de)
    if not e: raise SystemExit('no existe ' + a.familia_de)
    a.familia = rv(e).get('familia')

# ------------------------------------------------------------------ normalizar y raíces
STOP = set('de del la las el los un una unos unas y o u e a al en con sin por para que se su sus lo le les mas muy tipo '
           'como sobre bajo entre algo cosa cosas quiero necesito busco buscar dame algun alguna algunos efecto efectos '
           'of the a an and or for with to in on'.split())
def norm(t):
    t = ''.join(c for c in unicodedata.normalize('NFD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    return t.replace('_', ' ').replace('ñ', 'n')
def raiz(w):
    """plural y género fuera: papeles→papel, llamas→llam, rasgada/rasgado→rasgad, luces→luz."""
    if len(w) > 4 and w.endswith('ces'): w = w[:-3] + 'z'
    elif len(w) > 4 and w.endswith('es') and w[-3] not in 'aeiou': w = w[:-2]
    elif len(w) > 3 and w.endswith('s') and not w.endswith('ss'): w = w[:-1]
    if len(w) >= 5 and w[-1] in 'aoe': w = w[:-1]
    return w
def toks(t): return [w for w in re.findall(r'[a-z0-9]+', norm(t))]

# tesauro: sinónimos + alias de plugins + inglés
GRUPOS, MODS = [], set()
try:
    _s = json.load(open(R / 'indice' / 'sinonimos.json', encoding='utf-8'))
    GRUPOS = _s['grupos']
    for g in GRUPOS:
        if g[0] in _s.get('modificadores', []): MODS |= {raiz(w) for x in g for w in toks(x)}
except Exception: pass
try:
    nom = json.load(open(R / 'indice' / 'nombres.json', encoding='utf-8'))
    for k, v in (nom.get('oficiales') or {}).items(): GRUPOS.append([k] + list(v))
    for k, v in (nom.get('alias') or {}).items(): GRUPOS.append([k, v] if isinstance(v, str) else [k] + list(v))
except Exception: pass
SIN = collections.defaultdict(set)   # raíz de palabra → frases (tuplas de raíces) equivalentes
FRASES = {}                          # frase de varias palabras («cinta adhesiva») → equivalentes
for g in GRUPOS:
    frases = {tuple(raiz(w) for w in toks(x)) for x in g if toks(x)}
    for f in frases:
        if len(f) == 1:
            SIN[f[0]] |= frases
        else:
            FRASES[f] = FRASES.get(f, set()) | frases

# ------------------------------------------------------------------ texto de cada asset por campos (con peso)
CAMPOS = [  # (de dónde, peso)
    ('que_es', 3.0), ('familia', 2.2), ('clase', 2.2), ('sub', 2.2), ('uso', 2.0), ('desc', 1.8), ('estilo', 1.4),
    ('color', 1.4), ('material', 1.4), ('estilos', 1.2), ('pack', 1.0), ('comportamiento', 1.0), ('usar_si', 0.9),
    ('modo', 0.8), ('orient', 0.8), ('contenido', 0.6), ('archivo', 0.6), ('diferencia', 0.6), ('rol', 1.0)]
def campo(e, k):
    v = rv(e)
    if k in ('que_es', 'uso', 'usar_si', 'estilo', 'familia', 'comportamiento', 'orient', 'contenido', 'diferencia', 'rol'):
        x = v.get(k) or (e.get(k) if k == 'familia' else None)
    elif k == 'color': x = ' '.join(str(s) for s in (v.get('color'), e.get('color')) if s)
    elif k == 'modo': x = ' '.join(str(s) for s in (v.get('modo'), e.get('modo'), e.get('modo_texto')) if s)
    elif k == 'archivo': x = str(e.get('archivo', '')).rsplit('.', 1)[0]
    elif k == 'estilos': x = ' '.join(e.get('estilos') or [])
    else: x = e.get(k)
    return '' if x in (None, '-') else (' '.join(map(str, x)) if isinstance(x, list) else str(x))
ROOTS = {}   # id → {campo: set(raíces)}
DF = collections.Counter()
for e in idx:
    d = {}
    for k, w in CAMPOS:
        rs = {raiz(t) for t in toks(campo(e, k)) if t not in STOP}
        if rs: d[k] = rs
    ROOTS[e['id']] = d
    for r_ in set().union(*d.values()) if d else (): DF[r_] += 1
N = len(idx)
def idf(r_): return math.log((N + 1) / (DF.get(r_, 0) + 1)) + 1.0
PESO = dict(CAMPOS)

# ------------------------------------------------------------------ la consulta → conceptos
conceptos, es_mod = [], []   # cada concepto = lista de (frase de raíces, peso de la variante)
_q = [t for p in a.palabras for t in toks(p) if t not in STOP and len(t) >= 2]
i = 0
while i < len(_q):
    hecho = False
    for k in (3, 2):   # frases conocidas: «cinta adhesiva», «fuga de luz», «stop motion»…
        fr = tuple(raiz(t) for t in _q[i:i + k])
        if len(fr) == k and fr in FRASES:
            var = {fr: 1.0}
            for f in FRASES[fr]: var.setdefault(f, 0.8)
            for f in SIN.get(fr[0], ()): var.setdefault(f, 0.7)
            conceptos.append(list(var.items())); es_mod.append(False); i += k; hecho = True; break
    if hecho: continue
    r0 = raiz(_q[i]); i += 1
    var = {(r0,): 1.0}
    for f in SIN.get(r0, ()):
        var.setdefault(f, 0.8)
    conceptos.append(list(var.items())); es_mod.append(r0 in MODS)
if all(es_mod): es_mod = [False] * len(es_mod)   # solo matices («rojo»): entonces son el objeto
FALTAN = collections.Counter()
def puntua(e, explicar=False):
    d = ROOTS[e['id']]
    if not conceptos: return 1.0, 1.0, []
    total, hechos, por, oblig = 0.0, 0, [], True
    for var, mod in zip(conceptos, es_mod):
        best, bwhy = 0.0, None
        for frase, wv in var:
            for k, rs in d.items():
                if all(x in rs for x in frase):
                    s = PESO[k] * wv * sum(idf(x) for x in frase) / len(frase)
                    if s > best: best, bwhy = s, f'{"+".join(frase)}@{k}'
        if best > 0: hechos += 1; total += best; por.append(bwhy)
        elif not mod: oblig = False
    cobertura = hechos / len(conceptos)
    if not oblig: return 0.0, cobertura, por
    return total * cobertura ** 2.5, cobertura, por

# ------------------------------------------------------------------ usos por plugins (para repartir)
USOS = collections.defaultdict(set)
def leer_usos():
    for base in (R / 'plugins', BIB / 'plugins'):
        for p in list(base.glob('*/uso_id.json')) + list(base.glob('*/*/uso_id.json')):
            try: d = json.load(open(p, encoding='utf-8'))
            except Exception: continue
            nombre = d.get('plugin') or p.parent.name
            for f in d.get('filas', []):
                for k in ('id', 'productos_comunes', 'original_real'):
                    v = f.get(k)
                    for i in (v if isinstance(v, list) else [v]):
                        if isinstance(i, str) and ':' in i: USOS[i].add(nombre)
    for p in (BIB / '_uso').glob('*.json') if (BIB / '_uso').exists() else ():
        try:
            for i in json.load(open(p, encoding='utf-8')).get('ids', []): USOS[i].add(p.stem)
        except Exception: pass
    for e in idx:
        u = e.get('usado_por')
        for x in ([u] if isinstance(u, str) else (u or [])):
            x = x if isinstance(x, str) else str(x.get('plugin', x))
            USOS[e['id']].add(x.split(' (')[0].strip().lower())
leer_usos()
if a.apuntar:
    if not a.plugin: raise SystemExit('--apuntar necesita --plugin <nombre>')
    (BIB / '_uso').mkdir(exist_ok=True); f = BIB / '_uso' / (a.plugin + '.json')
    d = json.load(open(f, encoding='utf-8')) if f.exists() else {'plugin': a.plugin, 'ids': []}
    for i in a.apuntar:
        if i not in POR_ID: print('AVISO: no existe', i); continue
        if i not in d['ids']: d['ids'].append(i)
    json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'apuntados en {f}: {len(d["ids"])} ids de {a.plugin}'); sys.exit()

# ------------------------------------------------------------------ filtros
OPS = [('>=', operator.ge), ('<=', operator.le), ('!=', operator.ne), ('>', operator.gt), ('<', operator.lt), ('~', None), ('=', operator.eq)]
def valor(e, c):
    v = rv(e); m = v.get('medidas') or {}
    for fuente in (e, v, m):
        x = fuente
        for parte in c.split('.'):
            x = x.get(parte) if isinstance(x, dict) else None
        if x is not None: return x
    return None
def cumple(e, cond):
    for op, f in OPS:
        if op in cond:
            c, val = cond.split(op, 1); x = valor(e, c.strip()); val = val.strip()
            if x is None: return False
            if f is None: return norm(val) in norm(json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)
            try: return f(float(x), float(val))
            except (TypeError, ValueError): return f(norm(str(x)), norm(val))
    raise SystemExit('filtro --donde mal escrito: ' + cond)
def clase_de(e): return e.get('clase') or ('original' if e['id'].startswith('or:') else '—')
EXCL = {i for x in a.excluir for i in x.split(',') if i}
def es_fuente(e):
    v = rv(e)
    return e['id'].startswith('or:') and (e.get('productos') or norm(v.get('uso', '')).startswith('fuente'))
def pasa(e):
    v = rv(e)
    if e['id'] in EXCL: return False
    for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo'):
        f = getattr(a, k)
        if f and not norm((clase_de(e) if k == 'clase' else None) or e.get(k) or v.get(k) or '').startswith(norm(f)): return False
    if a.familia and v.get('familia') != a.familia: return False
    if a.alfa and not (e.get('alfa') or (e.get('video') or {}).get('alfa')): return False
    if a.tileable and not (e.get('tileable') or v.get('tileable')): return False
    if not a.todo and (v.get('rehacer') or e.get('sustituido_por') or v.get('dudoso') or v.get('duplicado_de')): return False
    if not (a.todo or a.fuentes or a.familia) and es_fuente(e): return False
    if (v.get('calidad') or 0) < a.min: return False
    if a.mejor and not v.get('mejor_de_familia'): return False
    if a.relleno and v.get('rol') != 'relleno de fondo': return False
    if a.donde and not all(cumple(e, c) for c in a.donde): return False
    return True

# ------------------------------------------------------------------ mapa de toda la biblioteca
if a.mapa:
    c = collections.Counter((clase_de(e), (e.get('sub') or '').split('/')[0]) for e in idx if pasa(e))
    ej = {}
    for e in idx:
        k = (clase_de(e), (e.get('sub') or '').split('/')[0])
        if k not in ej and pasa(e) and (rv(e).get('calidad') or 4) >= 4: ej[k] = rv(e).get('que_es', '')[:60]
    porclase = collections.Counter()
    for (cl, _), n in c.items(): porclase[cl] += n
    print(f'BIBLIOTECA: {sum(c.values())} assets utilizables (sin REHACER/copias/fuentes). Por clase y subclase:')
    for cl, n in porclase.most_common():
        print(f'\n{cl}  ({n})   → buscar.py --clase {cl}')
        for (c1, s), m in sorted(((k, m) for k, m in c.items() if k[0] == cl), key=lambda x: -x[1])[:14]:
            print(f'   {m:5}  {s or "—":28} p. ej.: {ej.get((c1, s), "")}')
    print('\nColecciones:', dict(collections.Counter(e['coleccion'] for e in idx if pasa(e))))
    sys.exit()

# ------------------------------------------------------------------ parecidos
def phash(e): return (rv(e).get('medidas') or {}).get('phash')
def hd(x, y):
    try: return bin(int(x, 16) ^ int(y, 16)).count('1')
    except Exception: return 64
if a.parecidos:
    base = POR_ID.get(a.parecidos)
    if not base: raise SystemExit('no existe ' + a.parecidos)
    hb, fb = phash(base), rv(base).get('familia')
    def dist(e):
        return hd(phash(e), hb) - (20 if rv(e).get('familia') == fb else 0) - (6 if e.get('sub') == base.get('sub') else 0)
    cand = [e for e in idx if e['id'] != base['id'] and e.get('tipo') == base.get('tipo') and pasa(e)]
    sel = sorted(cand, key=dist)[:a.n]
    conceptos = []
else:
    # -------------------------------------------------------------- puntuar
    res = []
    for e in idx:
        if not pasa(e): continue
        s, cob, por = puntua(e)
        if conceptos and (s <= 0 or (len(conceptos) >= 2 and cob < 0.5 and not any(es_mod))): continue
        v = rv(e); q = v.get('calidad') or 3
        s *= 0.55 + 0.09 * q + (0.04 if v.get('mejor_de_familia') else 0)
        ev = ROOTS[e['id']]
        evit = {raiz(t) for t in toks(v.get('evitar_si', ''))}
        if conceptos and any(fr[0] in evit for var in conceptos for fr, _ in var[:1]): s *= 0.7
        if v.get('rol') == 'relleno de fondo' and not a.relleno and not any(
                fr[0] in ('relleno', 'particul', 'fondo', 'pavesa', 'chisp') for var in conceptos for fr, _ in var[:1]):
            s *= 0.6
        if not a.clase and clase_de(e) in ('tutorial', 'plantilla', 'lut') and not any(
                fr[0] in ('tutorial', 'plantill', 'lut', 'etalonaj', 'look', 'drt', 'mogrt') for var in conceptos for fr, _ in var):
            s *= 0.45   # tutoriales, plantillas y LUT solo si se piden
        if not a.clase and not a.tipo and clase_de(e) == 'sonido' and not any(
                fr[0] in ('sonid', 'audio', 'sfx', 'whoosh', 'swoosh', 'golpe', 'impact', 'hit', 'riser', 'subid', 'ambient', 'sound', 'efecto de sonid')
                for var in conceptos for fr, _ in var):
            s *= 0.4    # sonidos solo si se piden
        usos = USOS.get(e['id'], set()) - ({a.plugin} if a.plugin else set())
        if usos and not a.incluir_usados: s *= 0.85
        res.append((s, e, cob, por))
    res.sort(key=lambda x: -x[0])
    if a.resumen:
        c1 = collections.Counter(f"{clase_de(e)}/{e.get('sub', '—')}" for _, e, _, _ in res)
        c2 = collections.Counter(rv(e).get('familia', '—') for _, e, _, _ in res)
        c3 = collections.Counter(e['coleccion'] for _, e, _, _ in res)
        print(f'{len(res)} encajan · {len(c2)} familias · colecciones {dict(c3)}. Por clase/sub:')
        for k, n in c1.most_common(40): print(f'  {n:5}  {k}')
        print('Familias (ábrelas con --familia NOMBRE):')
        for k, n in c2.most_common(60): print(f'  {n:5}  {k}')
        sys.exit()
    # -------------------------------------------------------------- abanico variado (MMR + azar)
    semilla = a.semilla if a.semilla is not None else random.randrange(1, 10 ** 6)
    rnd = random.Random(semilla)
    pagina = a.pagina + a.mas
    quiero = a.n * (pagina + 1)
    if a.lista or a.familia or not res:
        orden = [e for _, e, _, _ in res][:quiero]
    else:
        top = res[0][0]
        llenos = [x for x in res if x[2] >= 0.999]
        base = llenos if len(llenos) >= 3 * quiero else res      # si hay de sobra que cumplen TODO, solo esos
        buenos = [x for x in base if (rv(x[1]).get('calidad') or 3) >= 3]
        if len(buenos) >= 2 * quiero: base = buenos               # notas 1–2 solo si no hay bastante con 3+
        pool = [(s, e) for s, e, _, _ in base if s >= 0.25 * base[0][0]][:600]
        if len(pool) < quiero: pool = [(s, e) for s, e, _, _ in base][:max(600, quiero)]
        tau = 0 if a.fijo else 0.18
        rel = {e['id']: (s / base[0][0]) * math.exp(tau * -math.log(-math.log(rnd.random() or 1e-9))) for s, e in pool}
        def sim(x, y):
            vx, vy = rv(x), rv(y)
            m = 0.0
            if vx.get('familia') and vx.get('familia') == vy.get('familia'): m = max(m, 0.9)
            if re.sub(r'_(trama|relieve|gris|loop)$', '', x['id']) == re.sub(r'_(trama|relieve|gris|loop)$', '', y['id']): m = max(m, 0.97)
            if x.get('origen') and x.get('origen') == y.get('origen'): m = max(m, 0.7)
            if x.get('foto_origen') and x.get('foto_origen') == y.get('foto_origen'): m = max(m, 0.6)
            h = hd(phash(x), phash(y))
            if h <= 6: m = max(m, 0.85)
            elif h <= 12: m = max(m, 0.5)
            if (clase_de(x), x.get('sub')) == (clase_de(y), y.get('sub')): m = max(m, 0.45)
            if x.get('pack') and x.get('pack') == y.get('pack'): m = max(m, 0.35)
            if x['coleccion'] == y['coleccion']: m = max(m, 0.12)
            return m
        orden, resto = [], [e for _, e in pool]
        maxsim = {e['id']: 0.0 for e in resto}
        lam = 0.8
        usadas = collections.Counter()   # familias ya puestas: una por familia hasta que no queden otras
        while resto and len(orden) < quiero:
            minimo = min(usadas[rv(e).get('familia')] for e in resto)
            cand = [e for e in resto if usadas[rv(e).get('familia')] == minimo]
            b = max(cand, key=lambda e: rel[e['id']] - lam * maxsim[e['id']])
            orden.append(b); resto.remove(b); usadas[rv(b).get('familia')] += 1
            for e in resto: maxsim[e['id']] = max(maxsim[e['id']], sim(e, b))
    sel = orden[a.n * pagina: a.n * (pagina + 1)]
    INFO = {e['id']: (s, cob, por) for s, e, cob, por in res}

# ------------------------------------------------------------------ salida
def ruta(e): return str(e.get('archivo', ''))
def tam(e):
    v = rv(e); m = v.get('medidas') or {}
    w, h = e.get('w') or m.get('w'), e.get('h') or m.get('h')
    t = f'{w}×{h}' if w and h else ''
    vd = e.get('video') or {}
    if vd.get('duracion'): t += f' · {vd["duracion"]:.1f} s' + (' · loop' if vd.get('loop') else '')
    au = v.get('audio_medido') or {}
    if isinstance(au, dict) and au.get('duracion'): t += f' · {au["duracion"]:.1f} s'
    return t
if a.json:
    print(json.dumps(sel, ensure_ascii=False, indent=1)); sys.exit()
if not a.parecidos:
    fams = {rv(e).get('familia') for _, e, _, _ in res}
    cols = collections.Counter(e['coleccion'] for _, e, _, _ in res)
    print(f'«{" ".join(a.palabras)}»: {len(res)} encajan · {len(fams)} familias · {dict(cols)}'
          + ('' if (a.lista or a.familia) else f' · abanico variado, semilla {semilla}') + (f' · tanda {pagina + 1}' if pagina else ''))
    for var, mod in zip(conceptos, es_mod):
        if mod and res and not any(any(all(x in rs for x in fr) for fr, _ in var for rs in ROOTS[e['id']].values()) for _, e, _, _ in res):
            print(f'  (ninguno es «{var[0][0][0]}»: se enseña lo más cercano; si es una pieza, se puede recolorear)')
    if not res:
        print('Nada. Prueba otras palabras (sinónimos, inglés, el material o el uso), quita filtros o mira --mapa.')
for i, e in enumerate(sel, 1):
    v = rv(e)
    usos = sorted(USOS.get(e['id'], set()))
    marca = ('  ★mejor de su familia' if v.get('mejor_de_familia') else '')
    print(f"\n{i:2}. [{v.get('calidad') or '-'}/5] {e['id']}{marca}")
    print(f"    {v.get('que_es', '')}")
    det = [x for x in (e.get('tipo'), tam(e), 'alfa' if e.get('alfa') else '', 'repetible' if (e.get('tileable') or v.get('tileable')) else '',
                       ('modo ' + str(v.get('modo') or e.get('modo'))) if (v.get('modo') or e.get('modo')) else '',
                       v.get('color') or e.get('color'), v.get('estilo')) if x and x != '-']
    print('    ' + ' · '.join(map(str, det)))
    us, ev = v.get('usar_si'), v.get('evitar_si')
    if (us and us != '-') or (ev and ev != '-'): print(f"    usar si: {us or '-'} · evitar si: {ev or '-'}")
    if v.get('defectos') and v['defectos'] not in ('ninguno', '-') and not str(v['defectos']).startswith('(corregido'):
        print(f"    defectos: {v['defectos']}")
    if v.get('aviso'): print(f"    AVISO: {v['aviso']}")
    print(f"    archivo: {ruta(e)}")
    print(f"    familia: {v.get('familia', '-')}  (variantes: --familia {v.get('familia', '')})" + (f"   · ya lo usa: {', '.join(usos)}" if usos else ''))
    if a.explicar and not a.parecidos:
        s, cob, por = INFO[e['id']]; print(f'    puntos {s:.2f} · cobertura {cob:.0%} · {"; ".join(por)}')

# ------------------------------------------------------------------ hoja de miniaturas
def hoja(sel, nombre):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print('\n(--ver necesita Pillow: python -m pip install pillow)'); return None
    Image.MAX_IMAGE_PIXELS = None
    T, COL = 256, 4
    filas = (len(sel) + COL - 1) // COL
    W = Image.new('RGB', (COL * (T + 8), filas * (T + 40) + 8), (30, 30, 30)); d = ImageDraw.Draw(W)
    try: F = ImageFont.truetype('arial.ttf', 13)
    except Exception:
        try: F = ImageFont.truetype('DejaVuSans.ttf', 13)
        except Exception: F = ImageFont.load_default()
    def damero(w, h):
        im = Image.new('RGB', (w, h), (120, 120, 120)); dd = ImageDraw.Draw(im)
        for y in range(0, h, 12):
            for x in range(0, w, 12):
                if (x // 12 + y // 12) % 2: dd.rectangle((x, y, x + 11, y + 11), fill=(165, 165, 165))
        return im
    def donde(rel):   # funciona en la Biblioteca del PC y en un clon suelto de TEXTURAS
        rel = str(rel); c = [BIB / rel, R / rel]
        if rel.startswith('TEXTURAS/'): c.append(R / rel[9:])
        return c
    def mini(e):
        cands = []
        p = BIB / ruta(e)
        if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff', '.bmp'): cands += donde(ruta(e))
        for k in ('hoja',):
            for h in (e.get(k), rv(e).get(k)):
                if h: cands += donde(h)
        for c in cands:
            try:
                if not c.exists(): continue
                im = Image.open(c); im.draft('RGB', (T * 2, T * 2)); im.thumbnail((T, T))
                if max(im.size) < T * 0.6:   # piezas diminutas: se amplían para que se vean
                    k = T * 0.6 / max(im.size); im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))))
                if im.mode in ('RGBA', 'LA', 'P'):
                    im = im.convert('RGBA'); b = damero(*im.size); b.paste(im, (0, 0), im); im = b
                q = str(c).replace('\\', '/')
                return im.convert('RGB'), ('fotogramas' if ('acidbite/hojas' in q or '_tiras' in q) else ('hoja' if c.name != p.name else ''))
            except Exception: continue
        return None, ''
    for i, e in enumerate(sel):
        x, y = 8 + (i % COL) * (T + 8), 8 + (i // COL) * (T + 40)
        im, es_hoja = mini(e)
        if im: W.paste(im, (x + (T - im.width) // 2, y + 22 + (T - im.height) // 2))
        else: d.text((x + 8, y + T // 2), '(sin vista previa: ' + str(e.get('tipo')) + ')', fill=(200, 200, 200), font=F)
        t = f"{i + 1}. [{rv(e).get('calidad') or '-'}] " + rv(e).get('que_es', '')
        while len(t) > 8 and d.textlength(t, font=F) > T: t = t[:-2]
        d.text((x, y + 2), t, fill=(255, 220, 90), font=F)
        if es_hoja: d.text((x, y + T + 22), '(fotogramas del vídeo)' if es_hoja == 'fotogramas' else '(hoja de su grupo: --ficha para ver cuál)', fill=(150, 150, 150), font=F)
    out = BIB / '_busquedas'
    try: out.mkdir(exist_ok=True)
    except Exception:
        import tempfile; out = Path(tempfile.gettempdir()) / '_busquedas'; out.mkdir(exist_ok=True)
    f = out / (nombre + '.jpg'); W.save(f, quality=86)
    return f
if a.ver and sel:
    nombre = re.sub(r'[^a-z0-9]+', '_', norm(' '.join(a.palabras) or a.familia or a.parecidos or 'busqueda')).strip('_')[:50]
    nombre += f'_{"p" if a.parecidos else semilla}' + (f'_t{pagina + 1}' if not a.parecidos and pagina else '')
    f = hoja(sel, nombre)
    if f: print(f'\nHOJA: {f}   ← ábrela con Read y elige MIRANDO (los números son los de la lista)')
if not a.parecidos and res:
    print('\n— Es un abanico: todas encajan; la 1 no es «la buena». Mira (--ver), compara y elige por lo que necesitas.'
          f'\n— Más: --mas · Otra mezcla: sin --semilla · Repetir esta: --semilla {semilla}'
          ' · Variantes de una: --familia NOMBRE · Parecidas: --parecidos ID · Ficha: --ficha ID'
          if not (a.lista or a.familia) else '')
