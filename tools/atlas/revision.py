"""Revisión 100 % de la Biblioteca por vista (Claude, noche del 19-11-2026).

  python3 tools/atlas/revision.py plan                 → revision/ESTADO.json (lotes en orden de trabajo)
  python3 tools/atlas/revision.py hoja <lote>          → revision/hojas/<lote>.jpg (lo que se mira)
  python3 tools/atlas/revision.py fichas <lote> < txt  → revision/fichas/<lote>.json (lo que se ha visto)
  python3 tools/atlas/revision.py estado               → cuántos revisados / total por colección

Formato de las notas (una línea por elemento, en el orden de la hoja):
  F <familia> = <uso> ; modo <modo> ; usar si <...> ; evitar si <...>      (define/actualiza una familia)
  <n> <nota>[*] <familia> | <qué es> | <defectos o -> [| <en qué se diferencia de sus variantes>]
  nota 1–5 (5 = trabajo final sin tocar; 1 = no usar); * = la mejor de su familia;
  si en defectos aparece REHACER, va a la lista A_REHACER; DUDOSO marca que no está claro qué es.
"""
import hashlib, json, os, re, sys, collections, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
RV = ROOT / 'revision'
TIRAS = Path('/home/claude/rev/tiras')           # fotogramas sacados en el PC (lotes .tar descomprimidos)
COLLAGE_SRC = Path('/mnt/user-data/uploads/Biblioteca/AÑADIDOS/COLLAGE')
MAG = (230, 40, 160)
try:
    FONT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 22)
    FONT_S = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
except Exception:
    FONT = FONT_S = ImageFont.load_default()


def indice():
    return json.load(open(ROOT / 'indice/indice.json'))['assets']


def local(a):
    p = a['archivo']
    if p.startswith('TEXTURAS/'):
        return ROOT / p[len('TEXTURAS/'):]
    return None


# ------------------------------------------------------------------ plan
def plan():
    d = indice()
    vistos, lotes = set(), []

    def lote(nombre, ids, por):
        ids = [i for i in ids if i not in vistos]
        for i in ids: vistos.add(i)
        for k in range(0, len(ids), por):
            lotes.append(dict(lote='%s-%02d' % (nombre, k // por + 1), ids=ids[k:k + por], hecho=False))

    tx = [a for a in d if a['coleccion'] == 'TEXTURAS']
    # 1. TEXTURAS por clase (las subcarpetas seguidas) — imágenes de 15 en 15, vídeos de 6 en 6
    porcl = collections.defaultdict(list)
    for a in tx:
        if a.get('clase') in ('productos', 'collage'): continue
        porcl[a['clase']].append(a)
    for c, L in sorted(porcl.items()):
        L.sort(key=lambda a: (a.get('sub') or '', a['archivo']))
        lote('tx_' + c, [a['id'] for a in L], 6 if L[0]['tipo'] == 'video' else 15)
    # 2. productos
    prod = collections.defaultdict(list)
    for a in tx:
        if a.get('clase') == 'productos': prod[a['sub'].split('/')[0]].append(a)
    for s, L in sorted(prod.items()):
        L.sort(key=lambda a: (a['sub'], a['archivo']))
        lote('pr_' + s, [a['id'] for a in L], 6 if L[0]['tipo'] == 'video' else (24 if s == 'piezas' else 15))
    # 3. collage: piezas y sus fotos originales
    col = sorted([a for a in tx if a.get('clase') == 'collage'], key=lambda a: (a['sub'], a['archivo']))
    lote('co', [a['id'] for a in col], 15)
    oc = sorted([a for a in d if a['coleccion'] == 'originales' and a.get('sub') == 'collage'], key=lambda a: a['archivo'])
    lote('or_collage', [a['id'] for a in oc], 15)
    # 4. AcidBite (orden del .bat del PC), 5. originales
    man = json.load(open('/home/claude/rev/revision_tareas.json'))['tareas']
    byid = {a['id']: a for a in d}
    grupos = collections.OrderedDict()
    for i, rel, kind in man:
        a = byid[i]
        if a['coleccion'] == 'ACIDBITE':
            g = 'ab_' + re.sub(r'\W+', '_', (a.get('pack') or a.get('tipo'))).strip('_') + ('_' + kind if kind != 'video' else '')
            if a.get('tipo') == 'tutorial': g = 'ab_tutoriales'
        else:
            g = 'or_' + re.sub(r'\W+', '_', '/'.join(rel.split('/')[1:3])).strip('_')
        grupos.setdefault(g, []).append((i, kind))
    for g, L in grupos.items():
        lote(g, [i for i, _ in L], 6 if L[0][1] == 'video' else 15)
    # 6. lo que no se ve con los ojos (sonido, plantillas, proyectos): ficha por datos
    resto = [a['id'] for a in d if a['id'] not in vistos]
    noimg = collections.Counter(byid[i].get('tipo') for i in resto)
    json.dump(dict(creado='2026-11-19', total_indice=len({a['id'] for a in d}), lotes=lotes,
                   sin_vista=dict(ids=resto, por_tipo=dict(noimg))),
              open(RV / 'ESTADO.json', 'w'), ensure_ascii=False, indent=0)
    print(len(lotes), 'lotes ·', len(vistos), 'para ver ·', len(resto), 'sin imagen', dict(noimg))


# ------------------------------------------------------------------ hojas
def fit(im, w, h, bg=MAG):
    im = im.copy(); im.thumbnail((w, h))
    c = Image.new('RGB', (w, h), bg)
    if im.mode == 'RGBA':
        c.paste(im, ((w - im.width) // 2, (h - im.height) // 2), im)
    else:
        c.paste(im.convert('RGB'), ((w - im.width) // 2, (h - im.height) // 2))
    return c


def crop11(im, s, bg=MAG):
    """trozo 1:1 del centro de lo que hay (si tiene alfa, centrado en la pieza)."""
    cx, cy = im.width // 2, im.height // 2
    if im.mode == 'RGBA':
        a = np.asarray(im.split()[3])
        ys, xs = np.nonzero(a > 128)
        if len(xs):  # borde de la pieza: donde más se ve si el recorte es limpio
            e = (a > 128) ^ (np.asarray(Image.fromarray((a > 128).astype(np.uint8) * 255).filter(
                __import__('PIL.ImageFilter', fromlist=['x']).MinFilter(9))) > 128)
            ey, ex = np.nonzero(e)
            if len(ex):
                k = len(ex) // 3
                cx, cy = int(ex[k]), int(ey[k])
    box = (max(0, cx - s // 2), max(0, cy - s // 2), min(im.width, cx + s // 2), min(im.height, cy + s // 2))
    return fit(im.crop(box), s, s, bg) if (box[2] - box[0] < s or box[3] - box[1] < s) else _paste(im.crop(box), s, bg)


def _paste(c, s, bg):
    o = Image.new('RGB', (s, s), bg)
    if c.mode == 'RGBA': o.paste(c, (0, 0), c)
    else: o.paste(c.convert('RGB'), (0, 0))
    return o


def tile2x2(im):
    w, h = im.size
    o = Image.new(im.mode, (2 * w, 2 * h))
    for x in (0, w):
        for y in (0, h): o.paste(im, (x, y))
    return o


def video_tira(path, w=1200):
    """12 fotogramas repartidos de un vídeo local, en rejilla 4×3 sobre magenta."""
    out = Path('/tmp/rev_vid'); out.mkdir(exist_ok=True)
    for f in out.glob('*.png'): f.unlink()
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                               capture_output=True, text=True).stdout.strip() or 1)
    fr = []
    for k in range(12):
        f = out / ('%02d.png' % k)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '%.3f' % (dur * (k + .5) / 12), '-i', str(path), '-frames:v', '1',
                        '-vf', 'scale=384:-2', str(f)], capture_output=True)
        if f.exists(): fr.append(Image.open(f).convert('RGBA'))
        elif fr: fr.append(fr[-1])
    cw, ch = 384, 216
    o = Image.new('RGB', (4 * cw + 12, 3 * ch + 8), 'white')
    for k, im in enumerate(fr):
        o.paste(fit(im, cw, ch, (40, 40, 40)), ((k % 4) * (cw + 4), (k // 4) * (ch + 4)))
    return o, dur


def hoja(lote_id):
    est = json.load(open(RV / 'ESTADO.json'))
    L = next(l for l in est['lotes'] if l['lote'] == lote_id)
    byid = {a['id']: a for a in indice()}
    items = [byid[i] for i in L['ids']]
    es_video = items[0]['tipo'] in ('video', 'tutorial') or lote_id.startswith('ab_tutoriales')
    cells = []
    for n, a in enumerate(items, 1):
        p = local(a)
        lab = '%d  %s' % (n, Path(a['archivo']).name[:58])
        info = '%sx%s %s %s' % (a.get('w', '?'), a.get('h', '?'), a.get('modo') or '', ('fondo ' + a['fondo']) if a.get('fondo') else '')
        if a['coleccion'] == 'TEXTURAS' and a['tipo'] == 'video':
            t, dur = video_tira(p)
            info += ' · %.2f s' % dur
            cells.append((lab, info, t.resize((900, int(900 * t.height / t.width))), None))
            continue
        if a['coleccion'] == 'TEXTURAS':
            im = Image.open(p)
            im = im.convert('RGBA') if im.mode in ('RGBA', 'LA', 'P') else im.convert('RGB')
            vis = tile2x2(im) if a.get('tileable') else im
            cells.append((lab, info, fit(vis, 330, 330), crop11(im, 330)))
            continue
        sid = a['id'].replace(':', '_').replace('/', '__')
        f, f1 = TIRAS / (sid + '.jpg'), TIRAS / (sid + '_1a1.jpg')
        if a['coleccion'] == 'originales' and a.get('sub') == 'collage':
            src = COLLAGE_SRC / a['archivo'].split('originales/collage/', 1)[1]
            im = Image.open(src).convert('RGB')
            cells.append((lab, info, fit(im, 330, 330), crop11(im, 330)))
            continue
        if not f.exists():
            cells.append((lab, 'SIN FOTOGRAMAS (no llegó del PC)', Image.new('RGB', (330, 330), (90, 0, 0)), None))
            continue
        im = Image.open(f).convert('RGB')
        c1 = Image.open(f1).convert('RGB') if f1.exists() else None
        if es_video:
            cells.append((lab, info, im.resize((900, int(900 * im.height / im.width))), c1.resize((300, 300)) if c1 else None))
        else:
            cells.append((lab, info, fit(im, 330, 330), c1.resize((330, 330)) if c1 else None))
    # montaje
    if es_video:
        W = 1240; rows = []
        for lab, info, big, c1 in cells:
            h = big.height + 34
            r = Image.new('RGB', (W, h), 'white'); dr = ImageDraw.Draw(r)
            dr.text((4, 2), lab, fill='black', font=FONT); dr.text((520, 8), info, fill=(60, 60, 60), font=FONT_S)
            r.paste(big, (0, 32))
            if c1: r.paste(c1, (W - 330, 32))
            rows.append(r)
        o = Image.new('RGB', (W, sum(r.height + 6 for r in rows)), (200, 200, 200)); y = 0
        for r in rows: o.paste(r, (0, y)); y += r.height + 6
    else:
        cols = 4 if len(cells) > 15 else 3; cw = 670 if cols == 3 else 490; chh = (330 if cols == 3 else 240) + 34
        o = Image.new('RGB', (cols * cw, ((len(cells) + cols - 1) // cols) * chh), 'white'); dr = ImageDraw.Draw(o)
        for k, (lab, info, a1, a2) in enumerate(cells):
            x, y = (k % cols) * cw, (k // cols) * chh
            dr.text((x + 3, y + 1), lab[:40], fill='black', font=FONT_S); dr.text((x + 3, y + 17), info[:70], fill=(90, 90, 90), font=FONT_S)
            s2 = 330 if cols == 3 else 240
            o.paste(a1.resize((s2, s2)), (x, y + 34))
            if a2: o.paste(a2.resize((s2, s2)), (x + s2 + 4, y + 34))
    (RV / 'hojas').mkdir(parents=True, exist_ok=True)
    out = RV / 'hojas' / (lote_id + '.jpg')
    o.save(out, quality=82)
    print(out, o.size, len(cells))


# ------------------------------------------------------------------ fichas
def phash(im):
    g = np.asarray(im.convert('L').resize((32, 32), Image.LANCZOS), dtype=np.float32)
    from scipy.fft import dctn
    d = dctn(g, norm='ortho')[:8, :8]
    b = (d > np.median(d)).flatten()
    return '%016x' % int(''.join('1' if x else '0' for x in b), 2)


def medir(a):
    """medidas objetivas: tamaño, alfa, color medio, luminancia, pHash (de la imagen o de la tira)."""
    m = {}
    try:
        p = local(a)
        if p is None or a.get('tipo') not in ('imagen',):
            sid = a['id'].replace(':', '_').replace('/', '__')
            p = TIRAS / (sid + '.jpg')
            if a['coleccion'] == 'originales' and a.get('sub') == 'collage':
                p = COLLAGE_SRC / a['archivo'].split('originales/collage/', 1)[1]
            m['fuente_medida'] = 'tira' if p.name.startswith(('ab_', 'or_', 'tx_')) else 'imagen'
        if not p.exists(): return m
        im = Image.open(p); im.thumbnail((512, 512))
        m['w'], m['h'] = a.get('w'), a.get('h')
        if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
            im = im.convert('RGBA'); A = np.asarray(im)[..., 3] / 255.0
            m['alfa_cobertura'] = round(float((A > .5).mean()), 3)
            m['alfa_parcial'] = round(float(((A > .05) & (A < .95)).sum() / max(1, (A > .05).sum())), 3)
            rgb = np.asarray(im)[..., :3][A > .5]
        else:
            rgb = np.asarray(im.convert('RGB')).reshape(-1, 3)
        if len(rgb):
            c = rgb.mean(0); m['color_medio'] = '#%02x%02x%02x' % tuple(int(x) for x in c)
            L = rgb.mean(1); m['luminancia'] = round(float(L.mean() / 255), 3); m['contraste'] = round(float(L.std() / 255), 3)
            mx, mn = rgb.max(1).astype(float), rgb.min(1).astype(float)
            m['saturacion'] = round(float(((mx - mn) / np.maximum(mx, 1)).mean()), 3)
        m['phash'] = phash(im)
    except Exception as e:
        m['error_medida'] = str(e)[:80]
    return m


def fichas(lote_id, txt):
    est = json.load(open(RV / 'ESTADO.json'))
    L = next(l for l in est['lotes'] if l['lote'] == lote_id)
    fp = RV / 'familias.json'
    fam = json.load(open(fp)) if fp.exists() else {}
    byid = {a['id']: a for a in indice()}
    out, n_ok = {}, 0
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('F '):
            k, _, rest = line[2:].partition('=')
            k = k.strip(); parts = [p.strip() for p in rest.split(';')]
            f = fam.setdefault(k, dict(miembros=[]))
            f['uso'] = parts[0]
            for p in parts[1:]:
                for key in ('modo', 'usar si', 'evitar si'):
                    if p.startswith(key): f[key.replace(' ', '_')] = p[len(key):].strip()
            continue
        m = re.match(r'(\d+)\s+(\d)(\*?)\s+(\S+)\s*\|(.*)', line)
        if not m: raise SystemExit('línea mal formada: ' + line)
        n, nota, mejor, k, rest = int(m[1]), int(m[2]), m[3] == '*', m[4], m[5]
        parts = [p.strip() for p in rest.split('|')]
        if n < 1 or n > len(L['ids']): raise SystemExit('número fuera del lote: %d' % n)
        if k not in fam: raise SystemExit('familia sin definir: ' + k)
        aid = L['ids'][n - 1]
        defe = '' if parts[1] in ('-', '') else parts[1]
        f = fam[k]
        if aid not in f['miembros']: f['miembros'].append(aid)
        if mejor: f['mejor'] = aid
        extra = {}
        if len(parts) > 3:
            for kv in '|'.join(parts[3:]).split(';'):
                if '=' in kv:
                    kk, vv = kv.split('=', 1); extra[kk.strip()] = vv.strip()
        fam_info = {kk: f[kk] for kk in ('uso', 'modo', 'usar_si', 'evitar_si') if kk in f}
        out[aid] = dict(que_es=parts[0], calidad=nota, defectos=defe, familia=k,
                        variante=f['miembros'].index(aid) + 1, diferencia=parts[2] if len(parts) > 2 else '',
                        mejor_de_familia=mejor,
                        **{kk: extra.get(kk, fam_info.get(kk)) for kk in ('uso', 'modo', 'usar_si', 'evitar_si') if extra.get(kk) or fam_info.get(kk)},
                        **{kk: vv for kk, vv in extra.items() if kk not in ('uso', 'modo', 'usar_si', 'evitar_si')},
                        medidas=medir(byid[aid]),
                        rehacer='REHACER' in defe, dudoso='DUDOSO' in (parts[0] + defe),
                        revisado_por_vista=True, nivel='completo' if extra else 'basico',
                        fecha='2026-11-19', hoja='revision/hojas/%s.jpg' % lote_id)
        n_ok += 1
    falta = [i for i in L['ids'] if i not in out]
    if falta: raise SystemExit('faltan %d elementos del lote: %s' % (len(falta), [L['ids'].index(i) + 1 for i in falta]))
    (RV / 'fichas').mkdir(exist_ok=True)
    json.dump(out, open(RV / 'fichas' / (lote_id + '.json'), 'w'), ensure_ascii=False, indent=0)
    json.dump(fam, open(fp, 'w'), ensure_ascii=False, indent=0)
    L['hecho'] = True
    json.dump(est, open(RV / 'ESTADO.json', 'w'), ensure_ascii=False, indent=0)
    print(lote_id, n_ok, 'fichas ok')


def estado():
    est = json.load(open(RV / 'ESTADO.json'))
    byid = {a['id']: a for a in indice()}
    tot, hecho = collections.Counter(), collections.Counter()
    for l in est['lotes']:
        for i in l['ids']:
            c = byid[i]['coleccion']; tot[c] += 1
            if l['hecho']: hecho[c] += 1
    pend = [l['lote'] for l in est['lotes'] if not l['hecho']]
    print({c: '%d/%d' % (hecho[c], tot[c]) for c in tot}, '· lotes pendientes', len(pend), '· siguiente', pend[:3])


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'plan': plan()
    elif cmd == 'hoja': hoja(sys.argv[2])
    elif cmd == 'fichas': fichas(sys.argv[2], sys.stdin.read())
    elif cmd == 'estado': estado()
    elif cmd == 'reempaquetar':   # junta los lotes pendientes de imágenes en lotes de N (ahorra hojas)
        N = int(sys.argv[2]); est = json.load(open(RV / 'ESTADO.json'))
        byid = {a['id']: a for a in indice()}
        nuevos, pend = [], collections.OrderedDict()
        for l in est['lotes']:
            g = l['lote'].rsplit('-', 1)[0]
            vid = byid[l['ids'][0]].get('tipo') in ('video', 'tutorial') or g == 'ab_tutoriales' or any(
                (byid[i].get('archivo') or '').lower().endswith(('.mov', '.mp4')) for i in l['ids'])
            if l['hecho'] or vid: nuevos.append(l); continue
            pend.setdefault(g, []).extend(l['ids'])
        for g, ids in pend.items():
            for k in range(0, len(ids), N):
                nuevos.append(dict(lote='%s-r%02d' % (g, k // N + 1), ids=ids[k:k + N], hecho=False))
        orden = {l['lote'].rsplit('-', 1)[0]: n for n, l in enumerate(est['lotes'])}
        nuevos.sort(key=lambda l: (not l['hecho'], orden.get(l['lote'].rsplit('-', 1)[0], 9999)))
        est['lotes'] = nuevos; json.dump(est, open(RV / 'ESTADO.json', 'w'), ensure_ascii=False, indent=0)
        print(len(nuevos), 'lotes')
    elif cmd == 'siguiente':
        est = json.load(open(RV / 'ESTADO.json'))
        pref = sys.argv[2] if len(sys.argv) > 2 else ''
        l = next((l for l in est['lotes'] if not l['hecho'] and l['lote'].startswith(pref)), None)
        if l: hoja(l['lote'])
        else: print('NADA PENDIENTE', pref)
