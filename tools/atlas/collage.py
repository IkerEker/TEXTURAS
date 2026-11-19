"""COLLAGE: de las fotos generadas sobre fondo liso a piezas PNG RGBA limpias + ficha.

python3 tools/atlas/collage.py <carpeta COLLAGE> [n ...]        (sin n = todas)

Por cada imagen (tipo según collage_tabla.py):
 1. Fondo: modelo suave (polinomio de grado 3 por canal) ajustado a los píxeles de fondo → B(x,y). Así se quita el
    viñeteado y el degradado que meten los generadores; ruido del fondo = sigma.
 2. Opacos: núcleo = |I − B| > umbral; color del material cerca del borde F (convolución normalizada del interior);
    alfa del borde = proyección de I−B sobre F−B (las fibras y el antialias quedan con alfa parcial).
    Translúcidos y transparentes: alfa mínima («color a alfa») respecto a B: lo que deja ver el fondo queda transparente.
 3. Color descontaminado: C = B + (I − B)/alfa (sin halo gris del fondo).
 4. Piezas: componentes del núcleo (agrupando migas cercanas); cada una se recorta con margen.
 5. Sombra de contacto (opacos claros): aparte, en <pieza>_sombra.png (negro + alfa), por si se quiere.
Grafito: hoja entera; alfa = oscuridad respecto al papel (papel blanco → transparente), color = gris del grafito.
"""
import hashlib, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
import cv2

sys.path.insert(0, str(Path(__file__).parent))
from collage_tabla import MAT, IMG

SRC = Path(sys.argv[1]); OUT = Path('collage'); OUT.mkdir(exist_ok=True)
inv = json.load(open(OUT / '_trabajo' / 'inv.json')) if (OUT / '_trabajo' / 'inv.json').exists() else None


def poly_terms(h, w, step=1):
    y, x = np.mgrid[0:h:step, 0:w:step].astype(np.float32)
    x = x / w * 2 - 1; y = y / h * 2 - 1
    return np.stack([np.ones_like(x), x, y, x * x, x * y, y * y, x ** 3, x * x * y, x * y * y, y ** 3], -1)


def fondo(I):
    h, w, _ = I.shape
    s = 4 if h > 1500 else 3
    small = cv2.resize(I, (w // s, h // s), interpolation=cv2.INTER_AREA)
    small = cv2.medianBlur(small.astype(np.uint8), 5).astype(np.float32)
    hs, ws, _ = small.shape
    bd = np.concatenate([small[:6].reshape(-1, 3), small[-6:].reshape(-1, 3), small[:, :6].reshape(-1, 3), small[:, -6:].reshape(-1, 3)])
    b0 = np.median(bd, 0)
    T = poly_terms(hs, ws).reshape(-1, 10)
    m = (np.abs(small - b0).max(-1) < 22)
    # solo lo conectado al borde
    lab, _ = ndi.label(m)
    edge = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])); edge = edge[edge > 0]
    m = np.isin(lab, edge)
    for it in range(3):
        idx = m.reshape(-1)
        coef = np.linalg.lstsq(T[idx], small.reshape(-1, 3)[idx], rcond=None)[0]
        Bs = (T @ coef).reshape(hs, ws, 3)
        r = np.abs(small - Bs).max(-1)
        sig = 1.4826 * np.median(np.abs(r[m] - np.median(r[m]))) + np.median(r[m])
        m = m & (r < max(5.0, 3.5 * sig)) | (r < max(3.0, 2 * sig))
        m = ndi.binary_erosion(m, iterations=2)
    Tf = poly_terms(h, w, 1).reshape(-1, 10)
    B = (Tf @ coef).reshape(h, w, 3).astype(np.float32)
    rr = np.abs(cv2.resize(I, (w // s, h // s), interpolation=cv2.INTER_AREA) - Bs)
    sigma = float(np.std((cv2.resize(I, (w // s, h // s), interpolation=cv2.INTER_AREA) - Bs)[m]))
    return B, sigma, b0, m.mean()


def norm_conv(I, M, sig):
    k = int(sig * 3) * 2 + 1
    num = cv2.GaussianBlur(I * M[..., None], (k, k), sig)
    den = cv2.GaussianBlur(M.astype(np.float32), (k, k), sig)
    return num / np.maximum(den[..., None], 1e-4), den


def c2a(D, B, sigma):
    """alfa mínima para que I = a·F + (1−a)·B con F dentro de [0,255] («color a alfa» respecto al fondo medido)."""
    Bc = np.clip(B, 1, 254)
    a = np.where(D > 0, D / (255 - Bc), -D / Bc).max(-1)
    n0 = 2.5 * sigma / 128.0
    return np.clip((a - n0) / (1 - n0), 0, 1)


def disk(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def procesar(n, rel, mat):
    fam, desc, optica, borde, rellenar, grupo, modo = MAT[mat]
    path = SRC / rel
    raw = path.read_bytes(); md5 = hashlib.md5(raw).hexdigest()
    I = np.asarray(Image.open(path).convert('RGB')).astype(np.float32)
    h, w, _ = I.shape; esc = w / 2048.0
    if optica == 'grafito':
        return grafito(n, rel, mat, I, md5)
    B, sigma, b0, frac_fondo = fondo(I)
    D = I - B
    dist = np.sqrt((D ** 2).sum(-1))
    distb = cv2.GaussianBlur(dist, (0, 0), 1.2)
    thr_core = max(18.0, 6 * sigma) if optica == 'opaco' else max(7.0, 4 * sigma)
    if mat == 'washi':   # papel de color apagado casi del tono del fondo
        thr_core = max(9.0, 4 * sigma)
    core = (distb > thr_core).astype(np.uint8)
    core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, disk(max(2, int((8 if mat == 'washi' else 3) * esc))))
    if optica != 'opaco':
        core = cv2.morphologyEx(core, cv2.MORPH_CLOSE, disk(max(2, int((10 if optica == 'transparente' else 4) * esc))))
    core = core.astype(bool)
    LIGHT = optica == 'opaco' and mat not in ('cinta_negra', 'cinta_plata', 'peg_vinilo', 'estampado', 'cartulina_azul')
    dLum = D.mean(-1)
    dChr = np.abs(D - dLum[..., None]).max(-1)
    sombra_px = (dLum < -3 * sigma) & (dChr < 25)
    if LIGHT:
        # material claro o de color: es pieza lo que aclara el fondo o cambia su color; lo que solo lo oscurece es sombra
        dl = cv2.GaussianBlur(dLum, (0, 0), 1.2); dc = cv2.GaussianBlur(dChr, (0, 0), 1.2)
        core_orig = core.copy()
        core = core & ((dl > thr_core * 0.8) | (dc > 25))
        # una sombra que cae SOBRE la propia pieza es parte de la pieza: se recupera. Se distingue de la sombra en el
        # suelo por su borde con el fondo: la de la pieza acaba en el canto del papel (salto brusco), la del suelo se
        # desvanece suave.
        core |= (ndi.binary_fill_holes(core) & core_orig)
        Lg = cv2.GaussianBlur(I.mean(-1), (0, 0), 1.0)
        G = np.hypot(cv2.Sobel(Lg, cv2.CV_32F, 1, 0, ksize=3), cv2.Sobel(Lg, cv2.CV_32F, 0, 1, ksize=3)) / 8
        canto = cv2.dilate((G > 6).astype(np.uint8), disk(1)) > 0   # cantos nítidos: separan sombra-en-pieza de sombra-en-suelo
        quit_all = core_orig & ~core
        quit_ = quit_all & ~canto
        rl, rn = ndi.label(quit_)
        if rn:
            limpio = ~core_orig
            objs = ndi.find_objects(rl)
            for i, sl in enumerate(objs):
                if sl is None: continue
                y0_, y1_ = max(0, sl[0].start - 3), sl[0].stop + 3; x0_, x1_ = max(0, sl[1].start - 3), sl[1].stop + 3
                comp = rl[y0_:y1_, x0_:x1_] == i + 1
                if comp.sum() < 30 * esc * esc: continue
                bb = cv2.dilate(comp.astype(np.uint8), disk(2)) > 0
                bb &= ~comp & limpio[y0_:y1_, x0_:x1_]
                if bb.sum() < 10 or np.median(G[y0_:y1_, x0_:x1_][bb]) > 6:
                    core[y0_:y1_, x0_:x1_] |= comp

        core = cv2.morphologyEx(core.astype(np.uint8), cv2.MORPH_OPEN, disk(max(1, int(2 * esc)))) > 0
        core = cv2.morphologyEx(core.astype(np.uint8), cv2.MORPH_CLOSE, disk(max(2, int(3 * esc)))) > 0
    # huecos: los pequeños siempre; los grandes solo si el material no los tiene (cuaderno, papeles rasgados, arrancadas)
    holes = ndi.binary_fill_holes(core) & ~core
    hl, hn = ndi.label(holes)
    if hn:
        areas = ndi.sum(np.ones_like(hl), hl, range(1, hn + 1))
        lim = 1e12 if rellenar else 400 * esc * esc
        keep = np.zeros(hn + 1, bool); keep[1:] = areas < 400 * esc * esc
        core |= keep[hl]
        big_h = np.zeros(hn + 1, bool); big_h[1:] = (areas >= 400 * esc * esc) & (areas < lim)
        Hbig = big_h[hl]
    else:
        Hbig = np.zeros_like(core)
    core0 = core.copy(); core = core | Hbig
    # piezas: componentes grandes; migas cercanas se unen a su pieza; el resto se descarta
    lab, nl = ndi.label(core)
    areas = ndi.sum(np.ones_like(lab), lab, range(1, nl + 1)) if nl else np.array([])
    min_area = (0.002 if optica == 'opaco' else 0.001) * h * w
    big = [i + 1 for i, a in enumerate(areas) if a >= min_area]
    if not big:
        return dict(n=n, rel=rel, error='sin piezas', md5=md5)
    grp = cv2.dilate(core.astype(np.uint8), disk(max(2, int(grupo * esc)))) > 0
    if optica != 'transparente' and mat != 'pintura':
        # cada componente grande es una pieza; las migas y el borde van a la pieza más cercana (no se funden piezas vecinas)
        bigm = np.isin(lab, big)
        # trozos grandes a menos de ~8 px son la misma pieza (p. ej. una esquina quemada separada por una franja oscura)
        jl, _ = ndi.label(cv2.dilate(bigm.astype(np.uint8), disk(max(3, int(8 * esc)))) > 0)
        lab2 = np.where(bigm, jl, 0)
        dist_t, (iy, ix) = ndi.distance_transform_edt(~bigm, return_indices=True)
        glab = np.where(grp, lab2[iy, ix], 0) * (dist_t <= grupo * esc + 12 * esc)
        piezas_g = sorted(set(lab2[bigm].tolist()) - {0})
    else:
        glab, gn = ndi.label(grp)
        piezas_g = sorted(set(glab[np.isin(lab, big)].tolist()) - {0})
    # alfa
    if optica == 'opaco':
        er = cv2.erode(core0.astype(np.uint8), disk(max(2, int(4 * esc)))) > 0
        # color del material: del interior hondo (lejos del canto, donde los generadores meten halos de luz);
        # en piezas finas, del interior que haya
        erF = cv2.erode(core0.astype(np.uint8), disk(max(4, int(30 * esc)))) > 0
        F, den = norm_conv(I, erF.astype(np.float32), 14 * max(esc, .6))
        F2, den2 = norm_conv(I, erF.astype(np.float32), 45 * max(esc, .6))
        F3, den3 = norm_conv(I, er.astype(np.float32), 6 * max(esc, .6))
        F = np.where((den < 0.05)[..., None], np.where((den2 < 0.05)[..., None], F3, F2), F)
        FB = F - B
        nfb = (FB ** 2).sum(-1)
        a = (D * FB).sum(-1) / np.maximum(nfb, 1e-3)
        band = cv2.dilate(core.astype(np.uint8), disk(max(3, int(8 * esc)))) > 0
        a = np.clip(a, 0, 1)
        weak = nfb < (30.0 ** 2)  # material casi del color del fondo: alfa del núcleo suavizado
        a = np.where(weak, cv2.GaussianBlur(core.astype(np.float32), (0, 0), 1.0), a)
        # borde del núcleo: lo que no llega a medio camino entre fondo y material es halo (brillo del generador), no pieza
        zona = core & ~(cv2.erode(core.astype(np.uint8), disk(max(5, int(40 * esc)))) > 0)
        dl0 = D.mean(-1)
        liso = np.abs(dl0 - cv2.GaussianBlur(dl0, (0, 0), 4)) < 8
        entre = (dl0 * (F - B).mean(-1)) > 0   # el velo es una versión débil del material (mismo sentido de luz)
        cand = zona & (a < 0.5) & ~weak & liso & entre
        cl, cn = ndi.label(cand | ~core)
        ext = np.unique(cl[~core]); ext = ext[ext > 0]
        core = core & ~(cand & np.isin(cl, ext))   # solo el velo pegado por fuera; lo de dentro de la pieza se queda
        er = er & core
        fuera = ~core
        cerca = fuera & (cv2.dilate(core.astype(np.uint8), disk(1)) > 0)
        # fuera: solo detalle fino (fibras, hilos) que destaque del fondo cercano; el halo es suave y no pasa
        dl = D.mean(-1)
        nb, _ = norm_conv(dl[..., None].repeat(3, -1), fuera.astype(np.float32), 4 * max(esc, .6))
        hp = np.abs(dl - nb[..., 0])
        a_fib = np.clip((hp - 3 * sigma - 5) / 20, 0, 1) * np.clip(np.maximum(a, c2a(D, B, sigma)) * 3, 0, 1)
        if LIGHT:   # en materiales claros una línea oscura y sin color fuera de la pieza es sombra de contacto, no fibra
            a_fib = a_fib * ~((dLum < 0) & (dChr < 25))
        a = np.where(core, a, np.where(cerca, np.clip((a - 0.10) / 0.90, 0, 1), a_fib))
        a = np.where(er, 1.0, a) * band
        if Hbig.any():   # huecos grandes dentro de la pieza (adhesivo, capas finas): alfa mínima, deja ver el fondo
            if mat == 'etiq_rota':   # capas finas y adhesivo al aire: dejan ver el fondo
                ah = c2a(D, B, sigma)
            else:                    # el material no tiene agujeros: lo que parece fondo dentro de la pieza es pieza
                ah = np.ones_like(a)
            a = np.where(cv2.dilate(Hbig.astype(np.uint8), disk(1)) > 0, ah, a)
            if mat != 'etiq_rota':   # sin costuras alrededor de los huecos rellenados
                a = np.where(cv2.erode(core.astype(np.uint8), disk(max(2, int(4 * esc)))) > 0, 1.0, a)
        a[a < 0.04] = 0
    else:
        a = c2a(D, B, sigma)
        if optica == 'transparente':   # realce suave: un plástico casi invisible tiene que leerse
            a = 1 - (1 - a) ** 2
        reg = cv2.dilate(core.astype(np.uint8), disk(max(4, int(10 * esc)))).astype(np.float32)
        reg = cv2.GaussianBlur(reg, (0, 0), 3 * max(esc, .6))
        a = a * reg
        a = cv2.GaussianBlur(a, (0, 0), 0.6)
        a[a < 0.02] = 0
        F = None
    # color descontaminado
    with np.errstate(divide='ignore', invalid='ignore'):
        C = B + D / np.maximum(a, 1e-3)[..., None]
    if F is not None:
        C = np.where((a < 0.2)[..., None], F, C)
    C = np.clip(C, 0, 255)
    # sombra (opacos claros): más oscuro que el fondo, sin color, fuera del núcleo
    sombra = None
    if optica == 'opaco':
        LB = B.mean(-1); LI = I.mean(-1)
        chroma = np.abs(D - D.mean(-1, keepdims=True)).max(-1)
        s = np.clip((LB - LI) / np.maximum(LB, 1) - 2.5 * sigma / 255, 0, 1) * (chroma < 10)
        near = (cv2.dilate(core.astype(np.uint8), disk(int(45 * esc))) > 0) & ~(cv2.dilate(core.astype(np.uint8), disk(1)) > 0)
        s = cv2.GaussianBlur(s * near, (0, 0), 1.5)
        sombra = s
    res = []
    for k, g in enumerate(piezas_g):
        mk = glab == g
        mk_d = cv2.dilate(mk.astype(np.uint8), disk(max(3, int(10 * esc)))) > 0
        ap = a * mk_d
        ys, xs = np.nonzero(ap > 0.02)
        if len(ys) == 0: continue
        m = int(12 * esc) + 4
        y0, y1, x0, x1 = max(0, ys.min() - m), min(h, ys.max() + m + 1), max(0, xs.min() - m), min(w, xs.max() + m + 1)
        rgba = np.dstack([C[y0:y1, x0:x1], ap[y0:y1, x0:x1] * 255]).round().astype(np.uint8)
        base = '%s_%04d_%d' % (mat, n, k + 1)
        d = OUT / fam; d.mkdir(parents=True, exist_ok=True)
        f = d / (base + '.png')
        Image.fromarray(rgba, 'RGBA').save(f, optimize=True)
        A = ap[y0:y1, x0:x1]
        cub = A > 0.5
        col = C[y0:y1, x0:x1][cub].mean(0) if cub.any() else C[y0:y1, x0:x1][A > 0].mean(0)
        ficha = dict(id='tx:collage/%s/%s' % (fam, base), archivo='collage/%s/%s.png' % (fam, base),
                     familia=fam, material=mat, desc=desc, optica=optica, borde=borde,
                     w=int(x1 - x0), h=int(y1 - y0), alfa=True,
                     cobertura=round(float(A.mean()), 4),
                     alfa_parcial=round(float(((A > 0.05) & (A < 0.95)).sum() / max(1, (A > 0.05).sum())), 4),
                     opacidad_media=round(float(A[A > 0.05].mean()), 3) if (A > 0.05).any() else 0,
                     color_medio=[int(v) for v in col],
                     color='#%02x%02x%02x' % tuple(int(v) for v in col),
                     modo=modo, recorte=[int(x0), int(y0), int(x1 - x0), int(y1 - y0)],
                     fuente=dict(ruta='AÑADIDOS/COLLAGE/' + rel, md5=md5, w=w, h=h, n=n,
                                 fondo_medido='#%02x%02x%02x' % tuple(int(v) for v in b0), ruido_fondo=round(sigma, 2)),
                     procedencia='generada con IA (Gemini) por Iker', md5=hashlib.md5(f.read_bytes()).hexdigest())
        if sombra is not None:
            sp = sombra[y0:y1, x0:x1] * mk_d[y0:y1, x0:x1]
            if sp.max() > 0.08 and (sp > 0.05).sum() > 200 * esc * esc:
                sf = d / (base + '_sombra.png')
                z = np.zeros((y1 - y0, x1 - x0, 3), np.uint8)
                Image.fromarray(np.dstack([z, (np.clip(sp * 1.0, 0, 1) * 255).round().astype(np.uint8)]), 'RGBA').save(sf, optimize=True)
                ficha['sombra'] = dict(archivo='collage/%s/%s_sombra.png' % (fam, base), max=round(float(sp.max()), 3),
                                       modo='multiplicar o normal, misma posición que la pieza')
        res.append(ficha)
    return dict(n=n, rel=rel, md5=md5, material=mat, piezas=res, fondo_medido='#%02x%02x%02x' % tuple(int(v) for v in b0),
                ruido_fondo=round(sigma, 2), fraccion_fondo=round(float(frac_fondo), 3))


def grafito(n, rel, mat, I, md5):
    fam, desc, optica, borde, _, _, modo = MAT[mat]
    L = I.mean(-1)
    paper = np.percentile(L, 97)
    # papel blanco (algo irregular): se normaliza con un fondo muy suave por encima del grafito
    hi = ndi.maximum_filter(cv2.resize(L, (256, 256), interpolation=cv2.INTER_AREA), size=15)
    hi = cv2.GaussianBlur(hi, (0, 0), 6)
    P = cv2.resize(hi, (I.shape[1], I.shape[0]), interpolation=cv2.INTER_CUBIC)
    P = np.maximum(P, L)
    dens = np.clip(1 - L / np.maximum(P, 1), 0, 1)
    ink = np.percentile(I[dens > np.percentile(dens, 99.5)], 50, axis=0)  # gris del grafito más denso
    amax = np.clip(1 - ink.mean() / paper, 0.3, 1)
    a = np.clip(dens / amax, 0, 1)
    a[a < 0.015] = 0
    rgba = np.dstack([np.broadcast_to(ink, I.shape), a * 255]).round().astype(np.uint8)
    d = OUT / fam; d.mkdir(parents=True, exist_ok=True)
    base = '%s_%04d' % (mat, n)
    f = d / (base + '.png'); Image.fromarray(rgba, 'RGBA').save(f, optimize=True)
    gris = (np.clip(L / np.maximum(P, 1), 0, 1) * 255).round().astype(np.uint8)
    fg = d / (base + '_multiplicar.jpg'); Image.fromarray(gris, 'L').save(fg, quality=95)
    ficha = dict(id='tx:collage/%s/%s' % (fam, base), archivo='collage/%s/%s.png' % (fam, base), familia=fam, material=mat,
                 desc=desc, optica='trazo (alfa = densidad del grafito)', borde='hoja entera', w=I.shape[1], h=I.shape[0], alfa=True,
                 cobertura=round(float(a.mean()), 4), color='#%02x%02x%02x' % tuple(int(v) for v in ink),
                 color_medio=[int(v) for v in ink], modo='normal (RGBA) o multiplicar (_multiplicar.jpg, papel = blanco puro)',
                 version_multiplicar='collage/%s/%s_multiplicar.jpg' % (fam, base),
                 fuente=dict(ruta='AÑADIDOS/COLLAGE/' + rel, md5=md5, w=I.shape[1], h=I.shape[0], n=n),
                 procedencia='generada con IA (Gemini) por Iker', md5=hashlib.md5(f.read_bytes()).hexdigest())
    return dict(n=n, rel=rel, md5=md5, material=mat, piezas=[ficha])


if __name__ == '__main__':
    inv = json.load(open(OUT / '_trabajo' / 'inv.json'))
    sel = [int(x) for x in sys.argv[2:]] or list(range(len(inv)))
    out = OUT / '_trabajo' / 'resultados'; out.mkdir(parents=True, exist_ok=True)
    for n in sel:
        e = inv[n]
        if e['dup_de'] is not None:
            json.dump(dict(n=n, rel=e['rel'], md5=e['md5'], duplicado_de=e['dup_de']), open(out / ('%04d.json' % n), 'w'), ensure_ascii=False)
            continue
        r = procesar(n, e['rel'], IMG[n])
        json.dump(r, open(out / ('%04d.json' % n), 'w'), ensure_ascii=False, indent=0)
        print(n, IMG[n], len(r.get('piezas', [])), r.get('fondo_medido'), r.get('ruido_fondo'), r.get('error', ''), flush=True)
