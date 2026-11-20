"""Mejora recortes PNG RGBA sin tocar la silueta (el alfa se conserva):
  1. Descontamina el color del borde: los píxeles semitransparentes heredan el color de la pintura/objeto más cercano
     (el que está entero), mezclado con el original según su alfa, para que no quede cerco gris, blanco o verde.
  2. Quita el verde del croma (despill) en el borde: G no puede pasar de max(R, B) salvo que el objeto sea verde de verdad.
  3. Recorta la caja al contenido con un margen de 4 px.
Mide antes y después: «halo» = diferencia media de color entre el borde y el interior más cercano (0–255).
  python3 tools/atlas/mejorar_recorte.py medir <png>...      → JSON por línea
  python3 tools/atlas/mejorar_recorte.py arreglar <png> <salida> [--despill]"""
import sys, json, numpy as np
from PIL import Image
from scipy import ndimage as ndi

def cargar(p):
    im = Image.open(p)
    if im.mode != 'RGBA': im = im.convert('RGBA')
    return np.asarray(im).astype(np.float32)

def vecino_solido(rgb, a, umbral=0.9):
    solido = a >= umbral
    if solido.sum() < 20: return None, solido
    _, (iy, ix) = ndi.distance_transform_edt(~solido, return_indices=True)
    return rgb[iy, ix], solido

def medir(p):
    x = cargar(p); rgb, a = x[..., :3], x[..., 3] / 255
    near, solido = vecino_solido(rgb, a)
    borde = (a > 0.08) & (a < 0.9)
    m = dict(w=x.shape[1], h=x.shape[0], borde_px=int(borde.sum()), solido_px=int(solido.sum()))
    if near is None or borde.sum() < 10: m['halo'] = 0.0; m['verde'] = 0.0; return m
    d = np.abs(rgb[borde] - near[borde]).mean(1)
    m['halo'] = round(float(d.mean()), 1)
    m['alfa_parcial'] = round(float(((a > 0.05) & (a < 0.95)).sum() / max(1, (a > 0.05).sum())), 3)
    m['halo_claro'] = round(float((rgb[borde].mean(1) - near[borde].mean(1)).mean()), 1)  # >0: borde más claro que el objeto
    g = rgb[borde]; m['verde'] = round(float(np.clip(g[:, 1] - np.maximum(g[:, 0], g[:, 2]), 0, None).mean()), 1)
    gi = rgb[solido]; m['verde_interior'] = round(float(np.clip(gi[:, 1] - np.maximum(gi[:, 0], gi[:, 2]), 0, None).mean()), 1)
    ys, xs = np.nonzero(a > 0.02)
    m['margen'] = int(min(ys.min(), xs.min(), x.shape[0] - 1 - ys.max(), x.shape[1] - 1 - xs.max())) if len(ys) else 0
    return m

def arreglar(p, out, despill=False, margen=4, fondo='auto', suavizar=False, cerco=0):
    """fondo: 'blanco' (recortado de papel claro), 'negro' (de fondo negro), 'vecino' (solo color del interior) o 'auto'."""
    x = cargar(p); rgb, a = x[..., :3].copy(), x[..., 3] / 255
    near, solido = vecino_solido(rgb, a)
    borde = (a > 0) & ~solido
    if fondo == 'auto':
        m = medir(p); hc = m.get('halo_claro', 0)
        fondo = 'blanco' if hc > 8 else 'negro' if hc < -8 else 'vecino'
    if near is not None:
        aa = np.maximum(a, 1e-3)[..., None]
        if fondo == 'blanco':
            B = np.percentile(rgb[a < 0.05].reshape(-1, 3), 50, axis=0) if (a < 0.05).sum() > 50 and rgb[a < 0.05].mean() > 200 else np.array([250., 250, 248])
            F = (rgb - (1 - aa) * B) / aa
        elif fondo == 'negro':
            F = rgb / aa
        else:
            F = near
        F = np.clip(F, 0, 255)
        # donde el alfa es muy bajo la separación es inestable: se tira hacia el color del interior más cercano
        t = np.clip((a - 0.08) / 0.27, 0, 1)[..., None]
        F = F * t + near * (1 - t)
        rgb = np.where(borde[..., None], F, rgb)
    if cerco and fondo in ('negro', 'blanco'):
        # el contorno opaco suele llevar 1–2 px mezclados con el fondo (cerco oscuro o claro). Con el color del interior
        # cercano (a 'cerco'+1 px hacia dentro) se recalcula cuánto objeto hay de verdad en cada píxel de esa franja.
        A0 = x[..., 3] / 255
        nucleo = ndi.binary_erosion(A0 >= 0.9, iterations=cerco + 1)
        if nucleo.sum() > 20:
            dist, (iy, ix) = ndi.distance_transform_edt(~nucleo, return_indices=True)
            ref = x[..., :3][iy, ix]
            cerca = dist <= cerco + 2   # solo el contorno pegado a una zona maciza; los hilos finos no se tocan
            L = x[..., :3].mean(-1); Lr = ref.mean(-1)
            if fondo == 'negro': frac = np.clip(L / np.maximum(Lr, 1), 0, 1)
            else: frac = np.clip((255 - L) / np.maximum(255 - Lr, 1), 0, 1)
            franja = ((A0 > 0) & ~nucleo & ~ndi.binary_erosion(A0 >= 0.9, iterations=1) | ((A0 > 0) & (A0 < 0.9))) & cerca
            nuevoA = np.where(franja, np.minimum(A0, frac), A0)
            x[..., 3] = nuevoA * 255
            rgb = np.where(franja[..., None], ref, rgb)
            a = nuevoA
    if suavizar:
        # alfa casi binario (escalones): se suaviza solo la franja de 1 px del contorno; dentro y fuera no cambia
        A = x[..., 3] / 255
        dentro = ndi.binary_erosion(A > 0.5, iterations=1); fuera = ndi.binary_erosion(A <= 0.5, iterations=1)
        As = ndi.gaussian_filter(A, 0.7)
        zona = ~dentro & ~fuera
        x[..., 3] = np.where(zona, np.clip(As, 0, 1) * 255, x[..., 3])
        a = x[..., 3] / 255
        if near is not None: rgb = np.where(((a > 0) & (rgb.sum(-1) == 0))[..., None], near, rgb)
    if despill:
        lim = np.maximum(rgb[..., 0], rgb[..., 2])
        rgb[..., 1] = np.where(a < 0.98, np.minimum(rgb[..., 1], lim + 4), rgb[..., 1])
    rgb[a <= 0] = 0
    o = np.dstack([np.clip(np.round(rgb), 0, 255), x[..., 3]]).astype(np.uint8)
    if margen is not None:
        ys, xs = np.nonzero(o[..., 3] > 0)
        if len(ys):
            y0, x0 = max(ys.min() - margen, 0), max(xs.min() - margen, 0)
            o = o[y0:ys.max() + margen + 1, x0:xs.max() + margen + 1]
    Image.fromarray(o, 'RGBA').save(out, optimize=True)
    return fondo, o.shape

if __name__ == '__main__':
    if sys.argv[1] == 'medir':
        for p in sys.argv[2:]:
            try: print(json.dumps(dict(archivo=p, **medir(p))))
            except Exception as e: print(json.dumps(dict(archivo=p, error=str(e)[:80])))
    else:
        print(arreglar(sys.argv[2], sys.argv[3], '--despill' in sys.argv, fondo=next((x.split('=')[1] for x in sys.argv if x.startswith('--fondo=')), 'auto')))
