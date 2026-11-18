#!/usr/bin/env python3
"""Inventario de todos los assets visuales de los repos de origen.
Uso: python3 -I inventario.py RAIZ_REPOS SALIDA.json
Por archivo: repo, ruta, tamaño, sha1, tipo, y según el tipo:
  imagen -> ancho, alto, modo, alfa (si hay transparencia real), dhash/phash 64 bits, color medio,
            luminancia de las 4 esquinas (para adivinar fondo), proporción
  vídeo  -> ffprobe: códec, fps, duración, frames, resolución, pix_fmt (alfa)
"""
import sys, os, json, hashlib, subprocess
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

IMG = {'.png', '.jpg', '.jpeg', '.tif', '.tiff', '.webp', '.bmp', '.gif', '.psd'}
VID = {'.mp4', '.mov', '.m4v', '.webm', '.avi', '.mkv'}
SKIP_DIRS = {'.git', 'node_modules', '__MACOSX'}

def sha1(p):
    h = hashlib.sha1()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()

def phash(g):
    from scipy.fft import dct
    a = np.asarray(g.resize((32, 32), Image.LANCZOS), dtype=np.float64)
    d = dct(dct(a, axis=0, norm='ortho'), axis=1, norm='ortho')[:8, :8]
    m = np.median(d[1:, 1:]) if False else np.median(d.flatten()[1:])
    bits = (d > m).flatten()
    return '%016x' % int(''.join('1' if b else '0' for b in bits), 2)

def dhash(g):
    a = np.asarray(g.resize((9, 8), Image.LANCZOS), dtype=np.int32)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    return '%016x' % int(''.join('1' if b else '0' for b in bits), 2)

def info_img(p, d):
    with Image.open(p) as im:
        d.update(w=im.width, h=im.height, mode=im.mode, fmt=im.format,
                 frames=getattr(im, 'n_frames', 1))
        im.draft('RGB', (512, 512))
        im.thumbnail((512, 512))
        has_a = im.mode in ('RGBA', 'LA', 'PA') or 'transparency' in im.info
        rgba = im.convert('RGBA')
    a = np.asarray(rgba)
    alpha = a[..., 3]
    d['alfa'] = bool(has_a and alpha.min() < 250)
    if d['alfa']:
        d['alfa_cubre'] = round(float((alpha > 8).mean()), 4)
    rgb = a[..., :3].astype(np.float32)
    lum = rgb @ np.array([0.299, 0.587, 0.114], np.float32)
    d['color_medio'] = [int(x) for x in rgb.reshape(-1, 3).mean(0)]
    d['lum_media'] = round(float(lum.mean()), 1)
    d['lum_std'] = round(float(lum.std()), 1)
    k = max(4, min(lum.shape) // 16)
    corners = [lum[:k, :k], lum[:k, -k:], lum[-k:, :k], lum[-k:, -k:]]
    d['esquinas'] = [round(float(c.mean()), 1) for c in corners]
    cc = [rgb[:k, :k], rgb[:k, -k:], rgb[-k:, :k], rgb[-k:, -k:]]
    d['esquinas_rgb'] = [[int(x) for x in c.reshape(-1, 3).mean(0)] for c in cc]
    # saturación media (para detectar croma verde/fondos de color)
    mx, mn = rgb.max(-1), rgb.min(-1)
    d['sat_media'] = round(float(((mx - mn) / (mx + 1e-3)).mean()), 3)
    g = Image.fromarray(lum.clip(0, 255).astype(np.uint8))
    d['phash'] = phash(g)
    d['dhash'] = dhash(g)
    # costura: diferencia entre bordes opuestos frente a la diferencia entre filas vecinas
    L = lum
    edge = (np.abs(L[0] - L[-1]).mean() + np.abs(L[:, 0] - L[:, -1]).mean()) / 2
    inner = (np.abs(np.diff(L, axis=0)).mean() + np.abs(np.diff(L, axis=1)).mean()) / 2
    d['costura'] = round(float(edge / (inner + 1e-3)), 2)

def info_vid(p, d):
    r = subprocess.run(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_streams',
                        '-show_format', p], capture_output=True, text=True, timeout=120)
    j = json.loads(r.stdout or '{}')
    vs = [s for s in j.get('streams', []) if s.get('codec_type') == 'video']
    au = [s for s in j.get('streams', []) if s.get('codec_type') == 'audio']
    if vs:
        s = vs[0]
        num, den = (s.get('avg_frame_rate') or '0/1').split('/')
        fps = float(num) / float(den) if float(den) else 0
        d.update(codec=s.get('codec_name'), perfil=s.get('profile'), w=s.get('width'), h=s.get('height'),
                 pix_fmt=s.get('pix_fmt'), fps=round(fps, 3), frames=int(s.get('nb_frames') or 0),
                 audio=bool(au))
        d['alfa'] = 'a' in (s.get('pix_fmt') or '').replace('gray', '') and any(
            t in s.get('pix_fmt', '') for t in ('yuva', 'rgba', 'argb', 'bgra', 'abgr', 'ya'))
    fmt = j.get('format', {})
    d['duracion'] = round(float(fmt.get('duration') or 0), 3)

def one(args):
    root, rel = args
    p = os.path.join(root, rel)
    ext = os.path.splitext(rel)[1].lower()
    d = {'repo': rel.split('/')[0], 'ruta': rel, 'bytes': os.path.getsize(p), 'ext': ext}
    try:
        d['sha1'] = sha1(p)
        if ext in IMG:
            d['tipo'] = 'imagen'
            info_img(p, d)
        elif ext in VID:
            d['tipo'] = 'video'
            info_vid(p, d)
    except Exception as e:
        d['error'] = repr(e)[:200]
    return d

def main():
    root, out = sys.argv[1], sys.argv[2]
    todo = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [x for x in dn if x not in SKIP_DIRS]
        for f in fn:
            ext = os.path.splitext(f)[1].lower()
            if ext in IMG or ext in VID:
                todo.append((root, os.path.relpath(os.path.join(dp, f), root)))
    todo.sort(key=lambda t: t[1])
    print(len(todo), 'archivos', flush=True)
    res = []
    with ProcessPoolExecutor(2) as ex:
        for i, d in enumerate(ex.map(one, todo, chunksize=4)):
            res.append(d)
            if i % 300 == 0:
                print(i, d['ruta'][:80], flush=True)
    json.dump(res, open(out, 'w'), ensure_ascii=False, indent=0)
    print('ok', len(res))

if __name__ == '__main__':
    main()
