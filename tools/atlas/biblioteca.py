"""LIBRERÍA DE LA BIBLIOTECA · lo que usan buscar.py y los scripts de construcción de los plugins.

    import sys; sys.path.insert(0, r'<Biblioteca>/TEXTURAS/tools/atlas')
    from biblioteca import Biblioteca
    B = Biblioteca()                                   # carga el índice una vez (~1–2 s)
    r = B.buscar('papel viejo', n=12, tileable=True)   # abanico variado → r.sel (lista de assets), r.semilla
    r = B.buscar('goteo', n=8, semilla=7)              # el mismo abanico siempre (para builds reproducibles)
    B.ruta('tx:manchas/goteos/fina/goteo_157')         # ruta absoluta del archivo en la Biblioteca
    B.ficha(id) · B.familia('tile_papel') · B.parecidos(id) · B.necesidad('papel_fondo_calido') · B.hoja(lista, 'nombre')

Todo lo que decide qué sale y en qué orden está aquí (una sola fuente de verdad):
- puntuación por campos de la ficha revisada a ojo, con IDF, sinónimos (indice/sinonimos.json), frases, inglés,
  plurales y género; el objeto es obligatorio y color/tamaño/estilo matizan;
- PAPEL de cada recurso (fondo repetible, pieza, superposición, transición, máscara, relieve, elemento animado,
  sonido, LUT…) y FONDO (transparente, sobre negro, sobre blanco) deducidos de la ficha: se buscan y se filtran;
- abanico: una por familia, reparto por colección/clase/aspecto (pHash), azar con semilla;
- lo que ya usan los plugins se marca y se baja un poco; lo bueno que nadie usa sube un poco (para darle vida)."""
import json, re, math, random, collections, operator, os, unicodedata
from pathlib import Path

VERSION = 3
AQUI = Path(__file__).resolve()
R = AQUI.parents[2]                                         # …/TEXTURAS


def norm(t):
    t = ''.join(c for c in unicodedata.normalize('NFD', str(t).lower()) if unicodedata.category(c) != 'Mn')
    return t.replace('_', ' ')


def raiz(w):
    """plural y género fuera: papeles→papel, llamas→llam, rasgada/rasgado→rasgad, luces→luz."""
    if len(w) > 4 and w.endswith('ces'): w = w[:-3] + 'z'
    elif len(w) > 4 and w.endswith('es') and w[-3] not in 'aeiou': w = w[:-2]
    elif len(w) > 3 and w.endswith('s') and not w.endswith('ss'): w = w[:-1]
    if len(w) >= 5 and w[-1] in 'aoe': w = w[:-1]
    return w


def toks(t): return re.findall(r'[a-z0-9]+', norm(t))


STOP = set('de del la las el los un una unos unas y o u e a al en con sin por para que se su sus lo le les mas muy tipo '
           'como sobre bajo entre algo cosa cosas quiero necesito busco buscar dame algun alguna algunos efecto efectos '
           'of the a an and or for with to in on'.split())
CAMPOS = [  # (campo, peso): lo que mejor describe pesa más
    ('que_es', 3.0), ('etiquetas', 2.2), ('familia', 2.2), ('clase', 2.2), ('sub', 2.2), ('uso', 2.0), ('desc', 1.8),
    ('estilo', 1.4), ('color', 1.4), ('material', 1.4), ('estilos', 1.2), ('pack', 1.0), ('comportamiento', 1.0),
    ('usar_si', 0.9), ('modo', 0.8), ('orient', 0.8), ('contenido', 0.6), ('archivo', 0.6), ('diferencia', 0.6), ('rol', 1.0)]
PESO = dict(CAMPOS)
OPS = [('>=', operator.ge), ('<=', operator.le), ('!=', operator.ne), ('>', operator.gt), ('<', operator.lt), ('~', None), ('=', operator.eq)]
PAPELES = {  # papel → explicación (para --papel y para enseñar)
    'fondo repetible': 'textura que se repite sin costura (tile): fondos, superficies',
    'superposicion': 'imagen a pantalla completa que va ENCIMA (multiplicar/trama/superponer)',
    'pieza': 'objeto suelto con transparencia para colocar (mancha, cinta, borde, llama…)',
    'relieve': 'mapa en gris (50 % = neutro) para superponer/luz suave o desplazar',
    'transicion': 'vídeo que cubre y descubre la imagen',
    'mascara': 'mate/máscara (luma o alfa) para recortar o revelar',
    'elemento animado': 'vídeo de un elemento (humo, fuego, tinta, burbujas…) para poner encima',
    'superposicion animada': 'vídeo a pantalla completa encima (película, polvo, CRT, papel animado)',
    'fondo animado': 'vídeo de fondo',
    'sonido': 'efecto de sonido', 'lut': 'LUT de color (.cube)', 'plantilla': 'plantilla de programa (AE/Premiere/Resolve)',
    'tutorial': 'vídeo tutorial', 'fuente': 'foto original sin procesar (hay versión limpia tx:)'}


class Resultado:
    def __init__(self, sel, res, semilla, avisos, conceptos):
        self.sel, self.res, self.semilla, self.avisos, self.conceptos = sel, res, semilla, avisos, conceptos
    @property
    def ids(self): return [e['id'] for e in self.sel]


class Biblioteca:
    def __init__(self, bib=None, indice=None):
        self.R = R
        self.BIB = Path(bib or os.environ.get('TEXTURAS_ROOT') or R.parent)   # rutas `archivo` relativas a esta
        self.idx = json.load(open(indice or R / 'indice' / 'indice.json', encoding='utf-8'))['assets']
        self.por_id = {e['id']: e for e in self.idx}
        self._tesauro()
        self._necesidades()
        self.usos = collections.defaultdict(set); self._leer_usos()
        self.ROOTS, self.DF = {}, collections.Counter()
        for e in self.idx:
            e['_papel'], e['_fondo'] = self.papel(e), self.fondo(e)
            d = {}
            for k, _ in CAMPOS:
                rs = {raiz(t) for t in toks(self._campo(e, k)) if t not in STOP}
                if rs: d[k] = rs
            self.ROOTS[e['id']] = d
            for r_ in set().union(*d.values()) if d else (): self.DF[r_] += 1
        self.N = len(self.idx)
        # «grupo» para repartir: la familia; si la familia es muy grande (p. ej. todas las superficies), familia +
        # subcarpeta + primera palabra de «qué es» (granito ≠ ladrillo ≠ azulejo dentro de tile_superficie)
        tf = collections.Counter(self.rv(e).get('familia') for e in self.idx)
        for e in self.idx:
            f = self.rv(e).get('familia') or e['id']
            if tf[f] > 24:
                pal = [raiz(t) for t in toks(self.rv(e).get('que_es', '')) if t not in STOP and len(t) > 2 and not t.isdigit()]
                f = f'{f}|{str(e.get("sub", "")).split("/")[-1]}|{pal[0] if pal else ""}'
            e['_grupo'] = f

    # ------------------------------------------------------------- datos
    @staticmethod
    def rv(e): return e.get('revision') or {}
    def clase(self, e): return e.get('clase') or ('original' if e['id'].startswith('or:') else '—')
    def papel(self, e):
        v, c, sub = self.rv(e), self.clase(e), norm(e.get('sub') or '')
        modo = norm(' '.join(str(x) for x in (v.get('modo'), e.get('modo'), e.get('colocacion')) if x))
        arch = norm(e.get('archivo', ''))
        if c in ('sonido', 'lut', 'plantilla', 'tutorial'): return c
        if self.es_fuente(e): return 'fuente'
        if e.get('tipo') == 'video' or c == 'video':
            uso = norm(v.get('uso', ''))
            if sub.startswith('transicion') or (e.get('transicion') or {}).get('tipo') == 'mascara': return 'transicion'
            if 'mascara' in modo or 'mate' in modo: return 'mascara'
            if uso.startswith('transicion') and not e.get('transicion'): return 'transicion'
            if sub.startswith('fondos') or uso.startswith('fondo'): return 'fondo animado'
            if sub.startswith('elementos') or '/elementos/' in arch: return 'elemento animado'
            return 'superposicion animada'
        if (norm(v.get('que_es', '')).startswith(('relieve', 'mapa de relieve')) or e.get('desplazamiento') or 'relieve' in arch or c == 'pliegues' or 'gris 50' in norm(v.get('color', ''))
                or ('superponer' in modo and ('gris' in norm(v.get('color', '')) or 'relieve' in norm(v.get('que_es', ''))))): return 'relieve'
        if e.get('tileable') or v.get('tileable'): return 'fondo repetible'
        if 'mascara' in modo or c in ('mascara', 'mascaras'): return 'mascara'
        if e.get('alfa') or e.get('fondo') == 'transparente' or 'alfa' in modo: return 'pieza'
        if 'superposicion' in arch or c in ('superposicion', 'superposiciones') or 'trama' in modo or 'multiplicar' in modo: return 'superposicion'
        return 'imagen'
    def fondo(self, e):
        v = self.rv(e); modo = norm(' '.join(str(x) for x in (v.get('modo'), e.get('modo')) if x)); col = norm(v.get('color') or e.get('color') or '')
        if e.get('alfa') or e.get('fondo') == 'transparente' or 'alfa' in modo: return 'transparente'
        if 'sobre negro' in col or modo.startswith('trama') or 'screen' in modo: return 'sobre negro'
        if 'sobre blanco' in col or 'sobre papel blanco' in col or modo.startswith('multiplicar'): return 'sobre blanco'
        if 'superponer' in modo or 'gris 50' in col: return 'gris neutro'
        return 'opaco'
    def es_fuente(self, e):
        return e['id'].startswith('or:') and bool(e.get('productos') or norm(self.rv(e).get('uso', '')).startswith('fuente'))
    def _campo(self, e, k):
        v = self.rv(e)
        if k in ('que_es', 'uso', 'usar_si', 'estilo', 'familia', 'comportamiento', 'orient', 'contenido', 'diferencia', 'rol'):
            x = v.get(k) or (e.get(k) if k == 'familia' else None)
        elif k == 'etiquetas':
            ex = []
            if e.get('transicion'): ex.append('transicion sobre el corte' if (e['transicion'] or {}).get('tipo') == 'encima_corte' else 'transicion')
            if (e.get('video') or {}).get('loop'): ex.append('loop bucle')
            if e.get('tileable') or v.get('tileable'): ex.append('repetible tileable')
            if v.get('rol'): ex.append(v['rol'])
            mo = norm(' '.join(str(x) for x in (v.get('modo'), e.get('modo'), e.get('colocacion')) if x))
            if 'mascara' in mo or 'mate' in mo or 'luma' in mo: ex.append('mascara mate')
            x = ' '.join([e.get('_papel', ''), e.get('_fondo', '')] + ex + list(v.get('etiquetas') or []))
        elif k == 'color': x = ' '.join(str(s) for s in (v.get('color'), e.get('color')) if s)
        elif k == 'modo': x = ' '.join(str(s) for s in (v.get('modo'), e.get('modo'), e.get('modo_texto')) if s)
        elif k == 'archivo': x = str(e.get('archivo', '')).rsplit('.', 1)[0]
        elif k == 'estilos': x = ' '.join(e.get('estilos') or [])
        elif k == 'clase': x = self.clase(e)
        else: x = e.get(k)
        return '' if x in (None, '-') else (' '.join(map(str, x)) if isinstance(x, list) else str(x))
    def ruta(self, i):
        """ruta absoluta del archivo de un id (en la Biblioteca del PC o en un clon suelto de TEXTURAS)."""
        e = self.por_id[i] if isinstance(i, str) else i
        for c in self.donde(e.get('archivo', '')):
            if c.exists(): return c
        return self.BIB / e.get('archivo', '')
    def donde(self, rel):
        rel = str(rel); c = [self.BIB / rel, R / rel]
        if rel.startswith('TEXTURAS/'): c.append(R / rel[9:])
        return c
    def ficha(self, i): return self.por_id.get(i)
    def phash(self, e): return (self.rv(e).get('medidas') or {}).get('phash')
    @staticmethod
    def hd(x, y):
        try: return bin(int(x, 16) ^ int(y, 16)).count('1')
        except Exception: return 64

    # ------------------------------------------------------------- tesauro, necesidades y usos
    def _tesauro(self):
        grupos, self.MODS = [], set()
        try:
            s = json.load(open(R / 'indice' / 'sinonimos.json', encoding='utf-8'))
            grupos = s['grupos']
            for g in grupos:
                if g[0] in s.get('modificadores', []): self.MODS |= {raiz(w) for x in g for w in toks(x)}
        except Exception: pass
        try:
            nom = json.load(open(R / 'indice' / 'nombres.json', encoding='utf-8'))
            for k, v in (nom.get('oficiales') or {}).items(): grupos.append([k] + list(v))
            for k, v in (nom.get('alias') or {}).items(): grupos.append([k, v] if isinstance(v, str) else [k] + list(v))
        except Exception: pass
        self.SIN, self.FRASES = collections.defaultdict(set), {}
        for g in grupos:
            frases = {tuple(raiz(w) for w in toks(x)) for x in g if toks(x)}
            for f in frases:
                if len(f) == 1: self.SIN[f[0]] |= frases
                else: self.FRASES[f] = self.FRASES.get(f, set()) | frases
    def _necesidades(self):
        try: self.NEC = json.load(open(R / 'indice' / 'necesidades.json', encoding='utf-8'))
        except Exception: self.NEC = {'necesidades': []}
        self.nec = {n['nombre']: n for n in self.NEC.get('necesidades', [])}
    def _leer_usos(self):
        for base in (R / 'plugins', self.BIB / 'plugins'):
            for p in list(base.glob('*/uso_id.json')) + list(base.glob('*/*/uso_id.json')):
                try: d = json.load(open(p, encoding='utf-8'))
                except Exception: continue
                nombre = (d.get('plugin') or p.parent.name).lower()
                for f in d.get('filas', []):
                    if f.get('nombre_interno') is None and 'NO SE USA' in str(f.get('uso', '')): continue
                    for k in ('id', 'productos_comunes', 'original_real'):
                        v = f.get(k)
                        for i in (v if isinstance(v, list) else [v]):
                            if isinstance(i, str) and ':' in i: self.usos[i].add(nombre)
        u = self.BIB / '_uso'
        if u.exists():
            for p in u.glob('*.json'):
                try:
                    for i in json.load(open(p, encoding='utf-8')).get('ids', []): self.usos[i].add(p.stem.lower())
                except Exception: pass
        for e in self.idx:
            x = e.get('usado_por')
            for y in ([x] if isinstance(x, str) else (x or [])):
                y = y if isinstance(y, str) else str(y.get('plugin', y))
                self.usos[e['id']].add(y.split(' (')[0].strip().lower())
        # una fuente usada cuenta como usado su producto y al revés
        for e in self.idx:
            for p in e.get('productos') or []:
                if self.usos.get(e['id']): self.usos[p] |= self.usos[e['id']]
    def apuntar(self, plugin, ids):
        u = self.BIB / '_uso'; u.mkdir(exist_ok=True); f = u / (plugin + '.json')
        d = json.load(open(f, encoding='utf-8')) if f.exists() else {'plugin': plugin, 'ids': []}
        malos = [i for i in ids if i not in self.por_id]
        for i in ids:
            if i in self.por_id and i not in d['ids']: d['ids'].append(i)
        json.dump(d, open(f, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        return f, len(d['ids']), malos

    # ------------------------------------------------------------- consulta
    def conceptos(self, palabras):
        q = [t for p in ([palabras] if isinstance(palabras, str) else palabras) for t in toks(p) if t not in STOP and len(t) >= 2]
        con, mod, i = [], [], 0
        while i < len(q):
            hecho = False
            for k in (3, 2):
                fr = tuple(raiz(t) for t in q[i:i + k])
                if len(fr) == k and fr in self.FRASES:
                    var = {fr: 1.0}
                    for f in self.FRASES[fr]: var.setdefault(f, 0.8)
                    for f in self.SIN.get(fr[0], ()): var.setdefault(f, 0.7)
                    con.append(list(var.items())); mod.append(False); i += k; hecho = True; break
            if hecho: continue
            r0 = raiz(q[i]); i += 1
            var = {(r0,): 1.0}
            for f in self.SIN.get(r0, ()): var.setdefault(f, 0.8)
            con.append(list(var.items())); mod.append(r0 in self.MODS)
        if mod and all(mod): mod = [False] * len(mod)
        if getattr(self, '_estricto', False): mod = [False] * len(mod)
        return con, mod
    def idf(self, r_): return math.log((self.N + 1) / (self.DF.get(r_, 0) + 1)) + 1.0
    def puntua(self, e, con, mod, campos=None):
        d = self.ROOTS[e['id']]
        if campos: d = {k: v for k, v in d.items() if k in campos}
        if not con: return 1.0, 1.0, []
        total, hechos, por, oblig = 0.0, 0, [], True
        for var, m in zip(con, mod):
            best, bwhy = 0.0, None
            for frase, wv in var:
                for k, rs in d.items():
                    if all(x in rs for x in frase):
                        s = PESO[k] * wv * sum(self.idf(x) for x in frase) / len(frase)
                        if s > best: best, bwhy = s, f'{"+".join(frase)}@{k}'
            if best > 0: hechos += 1; total += best; por.append(bwhy)
            elif not m: oblig = False
        cob = hechos / len(con)
        return (total * cob ** 2.5 if oblig else 0.0), cob, por

    # ------------------------------------------------------------- filtros
    def valor(self, e, c):
        v = self.rv(e); m = v.get('medidas') or {}
        for fuente in (e, v, m):
            x = fuente
            for parte in c.split('.'):
                x = x.get(parte) if isinstance(x, dict) else None
            if x is not None: return x
        return None
    def cumple(self, e, cond):
        for op, f in OPS:
            if op in cond:
                c, val = cond.split(op, 1); x = self.valor(e, c.strip()); val = val.strip()
                if x is None: return False
                if f is None: return norm(val) in norm(json.dumps(x, ensure_ascii=False) if isinstance(x, (list, dict)) else x)
                try: return f(float(x), float(val))
                except (TypeError, ValueError): return f(norm(str(x)), norm(val))
        raise ValueError('filtro mal escrito: ' + cond)
    def pasa(self, e, f):
        v = self.rv(e)
        if e['id'] in f.get('excluir', ()): return False
        for k in ('clase', 'sub', 'modo', 'colocacion', 'coleccion', 'pack', 'tipo'):
            x = f.get(k)
            if x and not norm((self.clase(e) if k == 'clase' else None) or e.get(k) or v.get(k) or '').startswith(norm(x)): return False
        if f.get('subs') and (e.get('sub') or '') not in f['subs']: return False
        if f.get('papel') and not any(norm(e['_papel']) == norm(p).strip() for p in str(f['papel']).split(',')): return False
        if f.get('fondo') and not norm(e['_fondo']).startswith(norm(f['fondo'])): return False
        if f.get('familia') and v.get('familia') != f['familia']: return False
        if f.get('alfa') and not (e.get('alfa') or (e.get('video') or {}).get('alfa')): return False
        if f.get('tileable') and not (e.get('tileable') or v.get('tileable')): return False
        if not f.get('todo') and (v.get('rehacer') or e.get('sustituido_por') or v.get('dudoso') or v.get('duplicado_de')): return False
        if not (f.get('todo') or f.get('fuentes') or f.get('familia') or f.get('papel') == 'fuente') and self.es_fuente(e): return False
        if (v.get('calidad') if v.get('calidad') is not None else 3) < (f.get('min') or 0): return False
        if f.get('mejor') and not v.get('mejor_de_familia'): return False
        if f.get('relleno') and v.get('rol') != 'relleno de fondo': return False
        if f.get('sin_usar') and self.usos.get(e['id']): return False
        for c in f.get('donde') or []:
            if not self.cumple(e, c): return False
        return True

    # ------------------------------------------------------------- búsqueda
    def puntuar_todo(self, palabras='', **f):
        texto = palabras if isinstance(palabras, str) else ' '.join(palabras)
        alts = [x.strip() for x in texto.split('|')] if '|' in texto else [texto]   # «goteo | chorreon | drip» = cualquiera
        self._estricto = bool(f.get('estricto'))
        cm = [self.conceptos(x) for x in alts if x]
        if not cm: cm = [([], [])]
        con, mod = cm[0] if len(cm) == 1 else ([v for c, _ in cm for v in c], [m for _, m in cm for m in m])
        pedidos = {fr[0] for var in con for fr, _ in var}
        def pide(*xs): return any(x in pedidos for x in xs)
        res = []
        for e in self.idx:
            if not self.pasa(e, f): continue
            mejor = None
            for c_, m_ in cm:
                s, cob, por = self.puntua(e, c_, m_, f.get('campos'))
                if c_ and (s <= 0 or (len(c_) >= 2 and cob < 0.5 and not any(m_))): continue
                if mejor is None or s > mejor[0]: mejor = (s, cob, por)
            if mejor is None: continue
            s, cob, por = mejor
            v = self.rv(e); q = v.get('calidad') or 3
            s *= 0.55 + 0.09 * q + (0.04 if v.get('mejor_de_familia') else 0)
            evit = {raiz(t) for t in toks(v.get('evitar_si', ''))}
            if con and any(var[0][0][0] in evit for var in con): s *= 0.7
            if v.get('rol') == 'relleno de fondo' and not f.get('relleno') and not pide('relleno', 'particul', 'fondo', 'pavesa', 'chisp'): s *= 0.6
            c = self.clase(e)
            if not f.get('clase') and not f.get('papel') and c in ('tutorial', 'plantilla', 'lut') and not pide('tutorial', 'plantill', 'lut', 'etalonaj', 'look', 'drt', 'mogrt', 'gradacion'): s *= 0.45
            if not f.get('clase') and not f.get('tipo') and not f.get('papel') and c == 'sonido' and not pide(
                    'sonid', 'audio', 'sfx', 'whoosh', 'swoosh', 'golpe', 'impact', 'hit', 'riser', 'subid', 'ambient', 'sound'): s *= 0.4
            usos = self.usos.get(e['id'], set()) - ({f['plugin'].lower()} if f.get('plugin') else set())
            if usos and not f.get('incluir_usados'): s *= 0.85
            elif not usos and q >= 4: s *= 1.06          # lo bueno que nadie usa sube un poco: darle vida
            res.append((s, e, cob, por))
        res.sort(key=lambda x: -x[0])
        return res, con, mod
    def sim(self, x, y):
        vx, vy = self.rv(x), self.rv(y); m = 0.0
        if x['_grupo'] == y['_grupo']: m = 0.9
        elif vx.get('familia') and vx.get('familia') == vy.get('familia'): m = 0.55
        if re.sub(r'_(trama|relieve|gris|loop|mate)$', '', x['id']) == re.sub(r'_(trama|relieve|gris|loop|mate)$', '', y['id']): m = max(m, 0.97)
        if x.get('origen') and x.get('origen') == y.get('origen'): m = max(m, 0.7)
        if x.get('foto_origen') and x.get('foto_origen') == y.get('foto_origen'): m = max(m, 0.6)
        h = self.hd(self.phash(x), self.phash(y))
        if h <= 6: m = max(m, 0.85)
        elif h <= 12: m = max(m, 0.5)
        if (self.clase(x), x.get('sub')) == (self.clase(y), y.get('sub')): m = max(m, 0.45)
        if x.get('pack') and x.get('pack') == y.get('pack'): m = max(m, 0.35)
        if x['coleccion'] == y['coleccion']: m = max(m, 0.12)
        return m
    def buscar(self, palabras='', n=12, pagina=0, semilla=None, fijo=False, lista=False, **f):
        """abanico variado. Devuelve Resultado(sel, res, semilla, avisos, conceptos)."""
        res, con, mod = self.puntuar_todo(palabras, **f)
        if semilla is None: semilla = random.randrange(1, 10 ** 6)
        rnd = random.Random(semilla); quiero = n * (pagina + 1)
        if lista or f.get('familia') or not res:
            orden = [e for _, e, _, _ in res][:quiero]
        else:
            llenos = [x for x in res if x[2] >= 0.999]
            base = llenos if len(llenos) >= 3 * quiero else res
            buenos = [x for x in base if (self.rv(x[1]).get('calidad') or 3) >= 3]
            if len(buenos) >= 2 * quiero: base = buenos
            top = base[0][0]
            pool = [(s, e) for s, e, _, _ in base if s >= 0.25 * top][:600]
            if len(pool) < quiero: pool = [(s, e) for s, e, _, _ in base][:max(600, quiero)]
            tau = 0 if fijo else 0.25
            rel = {e['id']: (s / top) * math.exp(tau * -math.log(-math.log(rnd.random() or 1e-9))) for s, e in pool}
            orden, resto = [], [e for _, e in pool]
            maxsim = {e['id']: 0.0 for e in resto}; usadas = collections.Counter()
            while resto and len(orden) < quiero:
                minimo = min(usadas[e['_grupo']] for e in resto)
                cand = [e for e in resto if usadas[e['_grupo']] == minimo]
                b = max(cand, key=lambda e: rel[e['id']] - 0.8 * maxsim[e['id']])
                orden.append(b); resto.remove(b); usadas[b['_grupo']] += 1
                for e in resto: maxsim[e['id']] = max(maxsim[e['id']], self.sim(e, b))
        sel = orden[n * pagina: n * (pagina + 1)]
        avisos = []
        for var, m in zip(con, mod):
            if m and res and not any(any(all(x in rs for x in fr) for fr, _ in var for rs in self.ROOTS[e['id']].values()) for _, e, _, _ in res):
                avisos.append(f'ninguno es «{var[0][0][0]}»: se enseña lo más cercano; si es una pieza, se puede recolorear')
        return Resultado(sel, res, semilla, avisos, con)
    def familia(self, nombre):
        return sorted((e for e in self.idx if self.rv(e).get('familia') == nombre and self.pasa(e, {'familia': nombre})),
                      key=lambda e: (-(self.rv(e).get('calidad') or 0), not self.rv(e).get('mejor_de_familia')))
    def parecidos(self, i, n=12, **f):
        base = self.por_id[i]; hb, fb = self.phash(base), self.rv(base).get('familia')
        cand = [e for e in self.idx if e['id'] != i and e.get('tipo') == base.get('tipo') and self.pasa(e, f)]
        return sorted(cand, key=lambda e: self.hd(self.phash(e), hb) - (20 if self.rv(e).get('familia') == fb else 0)
                      - (6 if e.get('sub') == base.get('sub') else 0))[:n]
    def necesidad(self, nombre):
        """lista curada (revisada a ojo) de una necesidad de indice/necesidades.json → assets."""
        nd = self.nec[nombre]
        return [self.por_id[i] for i in nd.get('ids', []) if i in self.por_id]

    # ------------------------------------------------------------- hoja de miniaturas
    def hoja(self, sel, nombre, carpeta=None, T=256, COL=4):
        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError:
            return None
        Image.MAX_IMAGE_PIXELS = None
        filas = (len(sel) + COL - 1) // COL
        W = Image.new('RGB', (COL * (T + 8), filas * (T + 40) + 8), (30, 30, 30)); d = ImageDraw.Draw(W)
        F = None
        for fn in ('arial.ttf', 'DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'):
            try: F = ImageFont.truetype(fn, 13); break
            except Exception: pass
        F = F or ImageFont.load_default()
        def damero(w, h):
            im = Image.new('RGB', (w, h), (120, 120, 120)); dd = ImageDraw.Draw(im)
            for y in range(0, h, 12):
                for x in range(0, w, 12):
                    if (x // 12 + y // 12) % 2: dd.rectangle((x, y, x + 11, y + 11), fill=(165, 165, 165))
            return im
        def mini(e):
            p = Path(e.get('archivo', ''))
            cands = self.donde(e.get('archivo', '')) if p.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp', '.tif', '.tiff', '.bmp') else []
            if e.get('tipo') == 'video':   # tira de fotogramas propia (TEXTURAS/video/_tiras) o la del producto
                for i in [e['id']] + list(e.get('productos') or []):
                    x = self.por_id.get(i)
                    if x: cands += self.donde('TEXTURAS/video/_tiras/' + Path(x.get('archivo', '')).stem + '.jpg')
            for h in (e.get('hoja'), self.rv(e).get('hoja')):
                if h: cands += self.donde(h)
            for c in cands:
                try:
                    if not c.exists(): continue
                    im = Image.open(c); im.draft('RGB', (T * 2, T * 2)); im.thumbnail((T, T))
                    if max(im.size) < T * 0.6:
                        k = T * 0.6 / max(im.size); im = im.resize((max(1, int(im.width * k)), max(1, int(im.height * k))))
                    if im.mode in ('RGBA', 'LA', 'P'):
                        im = im.convert('RGBA'); b = damero(*im.size); b.paste(im, (0, 0), im); im = b
                    q = str(c).replace('\\', '/')
                    return im.convert('RGB'), ('fotogramas' if ('acidbite/hojas' in q or '_tiras' in q) else ('hoja' if c.name != p.name else ''))
                except Exception: continue
            return None, ''
        for i, e in enumerate(sel):
            x, y = 8 + (i % COL) * (T + 8), 8 + (i // COL) * (T + 40)
            im, tipo = mini(e)
            if im: W.paste(im, (x + (T - im.width) // 2, y + 22 + (T - im.height) // 2))
            else: d.text((x + 8, y + T // 2), '(sin vista previa: ' + str(e.get('tipo')) + ')', fill=(200, 200, 200), font=F)
            t = f"{i + 1}. [{self.rv(e).get('calidad') or '-'}] " + self.rv(e).get('que_es', '')
            while len(t) > 8 and d.textlength(t, font=F) > T: t = t[:-2]
            d.text((x, y + 2), t, fill=(255, 220, 90), font=F)
            if tipo: d.text((x, y + T + 22), '(fotogramas del vídeo)' if tipo == 'fotogramas' else '(hoja de su grupo: --ficha para ver cuál)', fill=(150, 150, 150), font=F)
        out = Path(carpeta) if carpeta else self.BIB / '_busquedas'
        try: out.mkdir(parents=True, exist_ok=True)
        except Exception:
            import tempfile; out = Path(tempfile.gettempdir()) / '_busquedas'; out.mkdir(exist_ok=True)
        f = out / (nombre + '.jpg'); W.save(f, quality=86)
        return f
