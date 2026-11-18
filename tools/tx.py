"""tx · utilidades comunes para la biblioteca TEXTURAS.

Reúne y generaliza lo que ya funcionaba en los plugins:
  - PAPELATOR tools/common.py      -> make_tileable (corte de costura óptimo + fundido de bajas frecuencias),
                                     flatten_light, seam_score
  - PAPELATOR tools/imperf_lib.py  -> estimate_bg (papel de fondo con su degradado), components
  - Analog FX BIBLIOTECA/goteos    -> formato de banco: recortes RGBA + catálogo + hojas de contactos
Todo trabaja en float32 0..1.
"""
import numpy as np
from PIL import Image
from scipy import ndimage

Image.MAX_IMAGE_PIXELS = None


# ---------------------------------------------------------------- E/S
def load(path, mode='RGB'):
    return np.asarray(Image.open(path).convert(mode), dtype=np.float32) / 255.0


def save(arr, path, **kw):
    a = np.clip(np.round(arr * 255.0), 0, 255).astype(np.uint8)
    Image.fromarray(a).save(path, optimize=True, **kw)


def lum(rgb):
    return rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722


def gblur(a, s):
    if s >= 12:                                   # rápido: reducir, desenfocar, ampliar
        k = int(max(2, s // 6))
        h, w = a.shape[:2]
        def one(c):
            sm = np.asarray(Image.fromarray(c.astype(np.float32)).resize((max(2, w // k), max(2, h // k)), Image.BOX), np.float32)
            sm = ndimage.gaussian_filter(sm, s / k, mode='reflect')
            return np.asarray(Image.fromarray(sm).resize((w, h), Image.BILINEAR), np.float32)
        return np.stack([one(a[..., c]) for c in range(a.shape[2])], -1) if a.ndim == 3 else one(a)
    if a.ndim == 3:
        return np.stack([ndimage.gaussian_filter(a[..., c], s, mode='reflect') for c in range(a.shape[2])], -1)
    return ndimage.gaussian_filter(a, s, mode='reflect')


def _down_up(a, k, sigma):
    h, w = a.shape
    sm = np.asarray(Image.fromarray(a.astype(np.float32)).resize((max(1, w // k), max(1, h // k)), Image.BOX), np.float32)
    sm = ndimage.gaussian_filter(sm, sigma)
    return sm, (w, h)


def _up(sm, size):
    return np.asarray(Image.fromarray(sm).resize(size, Image.BILINEAR), np.float32)


# ---------------------------------------------------------------- fondo (de PAPELATOR imperf_lib)
def estimate_bg(rgb, thr=0.06, grow=12):
    """Papel de fondo con su degradado de luz, ignorando lo que se aparta de él (trazo, mancha)."""
    L = lum(rgb)
    b = max(8, min(L.shape) // 60)
    border = np.concatenate([L[:b].ravel(), L[-b:].ravel(), L[:, :b].ravel(), L[:, -b:].ravel()])
    ref = np.median(border)
    sat = rgb.max(-1) - rgb.min(-1)
    bsat = np.median(np.concatenate([sat[:b].ravel(), sat[-b:].ravel()]))
    dev = np.maximum(np.abs(ref - L), (sat - bsat) * 1.2)
    mask = ndimage.binary_dilation(dev > thr, iterations=grow)
    w = (~mask).astype(np.float32)
    k = 8
    ws, size = _down_up(w, k, 12)
    bg = []
    for c in range(3):
        num, _ = _down_up(rgb[..., c] * w, k, 12)
        est = num / np.maximum(ws, 1e-4)
        fill = np.median(rgb[..., c][~mask]) if (~mask).any() else ref
        est = np.where(ws > 0.02, est, fill)
        bg.append(_up(est.astype(np.float32), size))
    return np.stack(bg, -1), mask


# ---------------------------------------------------------------- extracción a RGBA
def from_paper(rgb, solid_pct=65, grain_k=3.0):
    """Trazo/mancha sobre papel claro -> RGBA.
    A = cobertura (1 en el cuerpo de la pintura, parcial en bordes y pincel seco),
    RGB = color real del trazo, descontaminado del papel en los bordes.
    El grano del papel de la foto se elimina con un umbral suave medido en el propio papel."""
    bg, mask = estimate_bg(rgb)
    d = np.clip((bg - rgb) / np.maximum(bg, 1e-3), 0, 1).max(-1)          # distancia al papel (0..1)
    paper = d[~mask] if (~mask).any() else d.ravel()
    t0 = float(np.percentile(paper, 99.5)) + grain_k * float(paper.std())  # ruido del papel
    t0 = min(max(t0, 0.02), 0.25)
    body = d[d > t0 * 2]
    dsolid = float(np.percentile(body, solid_pct)) if body.size > 100 else 1.0
    dsolid = max(dsolid, t0 * 2.5)
    a = np.clip((d - t0) / (dsolid - t0), 0, 1)
    a = a * a * (3 - 2 * a) * 0.35 + a * 0.65                               # rodilla suave
    a3 = np.maximum(a, 1e-3)[..., None]
    col = np.clip((rgb - (1 - a3) * bg) / a3, 0, 1)
    col = np.where(a[..., None] > 0.004, col, 0)
    return np.dstack([col, a]), dict(umbral_papel=round(t0, 4), denso=round(dsolid, 4),
                                     papel_rgb=[round(float(x), 3) for x in np.median(bg.reshape(-1, 3), 0)])


def from_black(rgb, floor=None):
    """Luz/fuego/humo/espuma sobre negro -> RGBA (desmultiplicado). Equivale a usarlo en modo Trama."""
    if floor is None:
        floor = float(np.percentile(rgb.max(-1), 5))
    x = np.clip((rgb - floor) / (1 - floor), 0, 1)
    a = x.max(-1)
    col = np.clip(x / np.maximum(a, 1e-3)[..., None], 0, 1)
    return np.dstack([col, a]), dict(negro=round(floor, 4))


def from_chroma(rgb, lo_frac=0.04, hi_frac=0.96):
    """Objeto sobre verde croma -> RGBA con supresión del verde en los bordes."""
    ex = rgb[..., 1] - np.maximum(rgb[..., 0], rgb[..., 2])                  # exceso de verde
    b = max(8, min(ex.shape) // 60)
    e0 = float(np.median(np.concatenate([ex[:b].ravel(), ex[:, :b].ravel(), ex[:, -b:].ravel()])))
    if e0 < 0.15:
        e0 = float(np.percentile(ex, 95))
    a = 1 - np.clip((ex - e0 * lo_frac) / (e0 * (hi_frac - lo_frac)), 0, 1)
    a = ndimage.gaussian_filter(a, 0.6)
    keycol = np.median(rgb[ex > e0 * 0.8].reshape(-1, 3), 0) if (ex > e0 * 0.8).any() else np.array([0, 1, 0])
    a3 = np.maximum(a, 1e-3)[..., None]
    col = np.clip((rgb - (1 - a3) * keycol) / a3, 0, 1)
    m = np.maximum(col[..., 0], col[..., 2])                                  # despill
    col[..., 1] = np.minimum(col[..., 1], m + 0.01 * a)
    col = edge_color_from_core(col, a)
    avg = (col[..., 0] + col[..., 2]) / 2 + 0.03                              # despill fuerte en el borde
    semi = a < 0.98
    col[..., 1] = np.where(semi, np.minimum(col[..., 1], np.maximum(avg, col[..., 1] * 0 + avg)), col[..., 1])
    col = np.where(a[..., None] > 0.004, col, 0)
    return np.dstack([col, a]), dict(croma=[round(float(x), 3) for x in keycol])


def edge_color_from_core(col, a, core=0.95, sigmas=(2, 6, 18)):
    """En los píxeles semitransparentes, el color se toma del objeto opaco más cercano (como los keyers
    profesionales): adiós a ribetes del fondo en pelos, fibras y bordes finos."""
    w = (a > core).astype(np.float32)
    fg = np.zeros_like(col); acc = np.zeros(a.shape, np.float32)
    for s in sigmas:                                  # de fino a grueso: rellena lo que falte
        num = gblur(col * w[..., None], s); den = ndimage.gaussian_filter(w, s)
        est = num / np.maximum(den, 1e-4)[..., None]
        take = (den > 1e-3) & (acc < 0.5)
        fg[take] = est[take]; acc[take] = 1
    k = np.clip(a / core, 0, 1)[..., None] ** 2      # cuanto más opaco, más color propio
    return np.where(acc[..., None] > 0, col * k + fg * (1 - k), col)


# ---------------------------------------------------------------- piezas sueltas
def split_pieces(rgba, min_frac=0.0015, join_frac=0.012, pad_frac=0.01, thr=0.03):
    """Separa una lámina con varios trazos en piezas. Une lo que está a menos de join_frac del lado
    (salpicaduras de un mismo trazo). Devuelve lista de (rgba_recorte, (y0,y1,x0,x1))."""
    a = rgba[..., 3]
    H, W = a.shape
    side = min(H, W)
    m = a > thr
    joined = ndimage.binary_dilation(m, iterations=max(1, int(side * join_frac)))
    lab, n = ndimage.label(joined)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        own = (lab[sl] == i + 1)
        area = float((m[sl] & own).sum())
        if area < min_frac * H * W:
            continue
        pad = int(side * pad_frac)
        y0, y1 = max(0, sl[0].start - pad), min(H, sl[0].stop + pad)
        x0, x1 = max(0, sl[1].start - pad), min(W, sl[1].stop + pad)
        piece = rgba[y0:y1, x0:x1].copy()
        keep = ndimage.binary_dilation(lab[y0:y1, x0:x1] == i + 1, iterations=2)
        piece[..., 3] *= keep
        out.append((piece, (y0, y1, x0, x1)))
    out.sort(key=lambda p: (p[1][0] // max(1, H // 8), p[1][2]))
    return out


# ---------------------------------------------------------------- tileables (de PAPELATOR common)
def flatten_light(rgb, sigma):
    L = lum(rgb)
    low = gblur(L, sigma)
    ratio = low.mean() / np.maximum(low, 1e-3)
    return np.clip(rgb * ratio[..., None], 0, 1)


def _seam_path(E):
    H, O = E.shape
    C = E.copy()
    back = np.zeros((H, O), np.int32)
    for r in range(1, H):
        prev = C[r - 1]
        left = np.concatenate([[np.inf], prev[:-1]])
        right = np.concatenate([prev[1:], [np.inf]])
        st = np.stack([left, prev, right])
        idx = np.argmin(st, 0)
        C[r] += st[idx, np.arange(O)]
        back[r] = idx - 1
    path = np.zeros(H, np.int32)
    path[-1] = int(np.argmin(C[-1]))
    for r in range(H - 1, 0, -1):
        path[r - 1] = np.clip(path[r] + back[r, path[r]], 0, O - 1)
    return path


def wrap_x(img, s, O, feather=3):
    A = img[:, s:s + O]
    B = img[:, 0:O]
    diff = (A - B) ** 2
    E = diff.sum(-1) if diff.ndim == 3 else diff
    E = ndimage.gaussian_filter(E, 1.0)
    path = _seam_path(E)
    out = img[:, :s].copy()
    w = np.clip((np.arange(O)[None, :] - path[:, None]) / feather + 0.5, 0, 1)
    if img.ndim == 3:
        w = w[..., None]
    out[:, :O] = A * (1 - w) + B * w
    return out


def wrap_y(img, t, O, feather=3):
    if img.ndim == 3:
        return wrap_x(img.transpose(1, 0, 2), t, O, feather).transpose(1, 0, 2)
    return wrap_x(img.T, t, O, feather).T


def blend_wrap(img, s, t, Ox, Oy):
    out = img[:t + Oy, :s].copy()
    w = np.linspace(0, 1, Ox)[None, :]
    if img.ndim == 3:
        w = w[..., None]
    out[:, :Ox] = img[:t + Oy, s:s + Ox] * (1 - w) + img[:t + Oy, :Ox] * w
    out2 = out[:t].copy()
    w = np.linspace(0, 1, Oy)[:, None]
    if img.ndim == 3:
        w = w[..., None]
    out2[:Oy] = out[t:t + Oy] * (1 - w) + out[:Oy] * w
    return out2


def make_tileable(img, O=None, low_sigma=None):
    """img -> tile sin costuras de (H-O)x(W-O). Altas frecuencias por corte óptimo, bajas por fundido amplio."""
    H, W = img.shape[:2]
    O = O or max(48, min(H, W) // 12)
    s, t = W - O, H - O
    if low_sigma is None:
        low_sigma = min(H, W) / 30
    low = gblur(img, low_sigma)
    high = img - low
    lowt = blend_wrap(low, s, t, O, O)
    hight = wrap_y(wrap_x(high, s, O), t, O)
    return np.clip(lowt + hight, 0, 1)


def seam_score(tile):
    a = lum(tile) if tile.ndim == 3 else tile
    ix = np.mean(np.abs(a[:, 1:] - a[:, :-1])); sx = np.mean(np.abs(a[:, 0] - a[:, -1]))
    iy = np.mean(np.abs(a[1:] - a[:-1])); sy = np.mean(np.abs(a[0] - a[-1]))
    return round(float(sx / (ix + 1e-6)), 2), round(float(sy / (iy + 1e-6)), 2)


def tile_preview(tile, n=2, maxside=1400):
    big = np.tile(tile, (n, n, 1) if tile.ndim == 3 else (n, n))
    im = Image.fromarray(np.clip(big * 255, 0, 255).astype(np.uint8))
    im.thumbnail((maxside, maxside))
    return im


def on_checker(rgba, s=16, maxside=900):
    h, w = rgba.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    ch = np.where(((yy // s) + (xx // s)) % 2 == 0, 0.85, 0.65)[..., None]
    out = rgba[..., :3] * rgba[..., 3:4] + ch * (1 - rgba[..., 3:4])
    im = Image.fromarray(np.clip(out * 255, 0, 255).astype(np.uint8))
    im.thumbnail((maxside, maxside))
    return im


# ---------------------------------------------------------------- periodos (aparejos, papeles con patrón)
def autocorr_shift(a, axis, lo, hi):
    a = a - a.mean()
    best, bs = -1e9, lo
    n = a.shape[axis]
    for s in range(lo, hi + 1):
        x, y = (a[:, s:], a[:, :n - s]) if axis == 1 else (a[s:], a[:n - s])
        c = np.mean(x * y) / (np.std(x) * np.std(y) + 1e-9)
        if c > best:
            best, bs = c, s
    return bs, best


def make_tileable_periodic(img, O=None):
    """Para aparejos (ladrillo, azulejo, adoquín…) y papeles con patrón: el tile mide un número entero de piezas
    (periodo por autocorrelación, como PAPELATOR build_surfaces.prepare) y luego se cose."""
    H, W = img.shape[:2]
    O = O or max(48, min(H, W) // 12)
    L = lum(img) if img.ndim == 3 else img
    hp = L - gblur(L, 20)
    step = max(1, W // 700)
    s, cs = autocorr_shift(hp[::step, ::step], 1, int(W * 0.5) // step, (W - O - 4) // step)
    t, ct = autocorr_shift(hp[::step, ::step], 0, int(H * 0.5) // step, (H - O - 4) // step)
    s, t = s * step, t * step
    # refino fino alrededor
    s, cs = autocorr_shift(hp, 1, max(1, s - step), min(W - O - 4, s + step))
    t, ct = autocorr_shift(hp, 0, max(1, t - step), min(H - O - 4, t + step))
    return wrap_y(wrap_x(img, s, O), t, O), dict(periodo_px=[int(s), int(t)], corr=[round(float(cs), 3), round(float(ct), 3)])


def homogeneity(rgb, n=4):
    """0 = muy homogénea (apta para tile), >0.5 = composición con zonas distintas."""
    L = lum(rgb)
    h, w = L.shape
    blocks = [L[i * h // n:(i + 1) * h // n, j * w // n:(j + 1) * w // n] for i in range(n) for j in range(n)]
    m = np.array([b.mean() for b in blocks]); s = np.array([b.std() for b in blocks])
    return float(m.std() / (L.std() + 1e-6)), float(s.std() / (s.mean() + 1e-6))


# ---------------------------------------------------------------- relieve y pliegues
def relief_gray(rgb, gain=None):
    """Relieve horneado en la foto (marcas de grapa, hendiduras, sello en seco) -> gris 0.5 = neutro.
    Se usa en modo Superponer / Luz suave."""
    bg, _ = estimate_bg(rgb, thr=0.03)
    s = lum(rgb) / np.maximum(lum(bg), 1e-3) - 1
    hp = s - gblur(s, 25)
    mag = np.abs(hp)
    k = np.clip((mag - 0.006) / 0.006, 0, 1)
    k = ndimage.gaussian_filter(np.maximum(k, ndimage.maximum_filter(k, 3) * 0.7), 1.0)
    r = hp * k
    if gain is None:
        p = float(np.percentile(np.abs(r), 99.9))
        gain = 0.42 / max(p, 1e-3)
    return np.clip(0.5 + r * gain, 0, 1), round(float(gain), 2)


def fold_shading(rgb):
    """Sombreado de pliegues/arrugas sin la luz de la toma (ajuste cuadrático robusto en log, como PAPELATOR
    build_folds) -> gris 0.5 = papel plano. Modo Superponer o Luz suave; o multiplicar tras subir niveles."""
    L = lum(rgb).astype(np.float64)
    h, w = L.shape
    k = 8
    sm = np.asarray(Image.fromarray(np.log(np.maximum(L, 1e-3)).astype(np.float32)).resize((w // k, h // k), Image.BOX), np.float64)
    yy, xx = np.mgrid[0:sm.shape[0], 0:sm.shape[1]]
    X = (xx / sm.shape[1] - 0.5).ravel(); Y = (yy / sm.shape[0] - 0.5).ravel()
    A = np.stack([np.ones_like(X), X, Y, X * X, Y * Y, X * Y], 1)
    z = sm.ravel(); wgt = np.ones_like(z)
    for _ in range(3):
        c, *_ = np.linalg.lstsq(A * wgt[:, None], z * wgt, rcond=None)
        res = z - A @ c
        wgt = 1 / (1 + (res / (np.median(np.abs(res)) * 3 + 1e-6)) ** 2)
    yy, xx = np.mgrid[0:h, 0:w]
    Xf = xx / w - 0.5; Yf = yy / h - 0.5
    fit = c[0] + c[1] * Xf + c[2] * Yf + c[3] * Xf * Xf + c[4] * Yf * Yf + c[5] * Xf * Yf
    s = np.log(np.maximum(L, 1e-3)) - fit
    s = s - np.median(s)
    p = float(np.percentile(np.abs(s), 99.7))
    return np.clip(0.5 + s * (0.45 / max(p, 1e-3)), 0, 1).astype(np.float32)


def crop_alpha(rgba, thr=0.01, pad_frac=0.02):
    a = rgba[..., 3]
    ys, xs = np.where(a > thr)
    if len(ys) == 0:
        return rgba, (0, rgba.shape[0], 0, rgba.shape[1])
    pad = int(min(a.shape) * pad_frac)
    y0, y1 = max(0, ys.min() - pad), min(a.shape[0], ys.max() + pad + 1)
    x0, x1 = max(0, xs.min() - pad), min(a.shape[1], xs.max() + pad + 1)
    return rgba[y0:y1, x0:x1], (int(y0), int(y1), int(x0), int(x1))


def from_dark_object(rgb):
    """Objeto opaco sobre negro (pintura blanca, moho, líquenes) -> RGBA con cobertura (no desmultiplicado)."""
    inv, info = from_paper(1 - rgb)
    col = np.where(inv[..., 3:4] > 0.004, 1 - inv[..., :3], 0)
    return np.dstack([col, inv[..., 3]]), info


# ---------------------------------------------------------------- color en palabras
def color_name(rgb):
    r, g, b = [float(x) for x in rgb]
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    s = 0 if mx == mn else (mx - mn) / (1 - abs(2 * l - 1) + 1e-6)
    if s < 0.18 or mx - mn < 0.08:
        return 'negro' if l < 0.18 else 'gris oscuro' if l < 0.4 else 'gris' if l < 0.7 else 'gris claro' if l < 0.88 else 'blanco'
    if mx == r: h = ((g - b) / (mx - mn)) % 6
    elif mx == g: h = (b - r) / (mx - mn) + 2
    else: h = (r - g) / (mx - mn) + 4
    h *= 60
    names = [(15, 'rojo'), (40, 'naranja'), (65, 'amarillo'), (160, 'verde'), (195, 'turquesa'), (255, 'azul'), (290, 'violeta'), (335, 'rosa'), (360, 'rojo')]
    n = next(nm for lim, nm in names if h < lim)
    if n in ('naranja', 'amarillo', 'rojo') and l < 0.42 and s < 0.75:
        n = 'marrón'
    if l > 0.8: n += ' claro'
    elif l < 0.3: n += ' oscuro'
    return n


def from_black_cover(rgb, solid_pct=50):
    """Objeto opaco sobre negro PURO (papel, pintura blanca, moho): el fondo es negro conocido, así no se confunde
    con el objeto aunque ocupe más de media imagen. A = cobertura, RGB = color desmezclado del negro."""
    d = rgb.max(-1)
    dark = d[d < 0.10]
    t0 = max(0.025, float(np.percentile(dark, 97)) + 0.01) if dark.size > 100 else 0.04
    body = d[d > t0 * 3]
    dsolid = float(np.percentile(body, solid_pct)) if body.size > 100 else 0.5
    dsolid = max(dsolid * 0.7, t0 * 3)
    a = np.clip((d - t0) / (dsolid - t0), 0, 1)
    col = np.clip(rgb / np.maximum(a, 1e-3)[..., None], 0, 1)
    col = np.where(a[..., None] > 0.004, col, 0)
    return np.dstack([col, a]), dict(negro=round(t0, 4), denso=round(dsolid, 4))


def is_chroma(rgb, frac=0.08):
    g = (rgb[..., 1] > rgb[..., 0] + 0.15) & (rgb[..., 1] > rgb[..., 2] + 0.10)
    return float(g.mean()) > frac
