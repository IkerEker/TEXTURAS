"""Mates de las transiciones de tinta 4K (Studio DamDam, Textured Transition Pack → Matte_MOVs).

Entrada: los 21 Matte_MOVs (ProRes 4444 XQ 4K, RGB negro + ALFA = tinta) desde Biblioteca.
Salida: productos/mates_tinta_4k/<dir>/<dir>_<n>_mate.mp4 = el alfa como luminancia (blanco = tinta, cubre),
H.264 4K 25 fps 4:2:0 crf 12, y mates.json con la cobertura medida fotograma a fotograma.
Uso: python3 tools/atlas/producto_mates_tinta.py <carpeta Matte_MOVs>
"""
import json, subprocess, sys, hashlib
from pathlib import Path
import numpy as np

SRC = Path(sys.argv[1]); OUT = Path('productos/mates_tinta_4k')
DIRS = {'Diagonal': 'diagonal', 'Horizontal': 'horizontal', 'Vertical': 'vertical'}
res = []
for d, dd in DIRS.items():
    for i in range(1, 8):
        f = SRC / d / f'{d[0]}{i}.mov'
        o = OUT / dd / f'{dd}_{i}_mate.mp4'; o.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(f), '-vf', 'alphaextract,format=gray,format=yuv420p',
                        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '12', '-an', '-movflags', '+faststart', str(o)], check=True)
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(f), '-vf', 'alphaextract,scale=480:270,format=gray',
                              '-f', 'rawvideo', '-'], capture_output=True, check=True).stdout
        a = np.frombuffer(raw, np.uint8).reshape(-1, 270, 480) / 255.0
        cov = [round(float((x > .5).mean()), 4) for x in a]
        n = len(cov); fps = 25.0
        distintos = 1 + sum(1 for k in range(1, n) if np.abs(a[k] - a[k - 1]).mean() > 1e-3)
        full = [k for k, c in enumerate(cov) if c >= 0.995]
        cubre = round(full[0] / fps, 3) if full else None
        desc = None
        if full:
            after = [k for k in range(full[0], n) if cov[k] < 0.995]
            desc = round(after[0] / fps, 3) if after else None
        res.append(dict(id=f'tx:productos/mates_tinta_4k/{dd}/{dd}_{i}_mate', archivo=f'mates_tinta_4k/{dd}/{dd}_{i}_mate.mp4',
                        pareja=f'tx:video/transiciones/tinta_4k/{dd}/{dd}_{i}', direccion=dd, n=i,
                        w=3840, h=2160, fps=fps, fotogramas=n, fotogramas_distintos=distintos, duracion=n / fps,
                        cubre_total_s=cubre, descubre_desde_s=desc, cobertura=cov,
                        md5=hashlib.md5(o.read_bytes()).hexdigest(), bytes=o.stat().st_size,
                        origen_ruta=f'gumroad/TransitionPack4K_Gumroad/Matte_MOVs/{d}/{d[0]}{i}.mov'))
        print(dd, i, distintos, cubre, desc, o.stat().st_size // 1024, 'KB')
json.dump(dict(descripcion='Mates limpios (alfa del autor) de las 21 transiciones de tinta 4K de Studio DamDam. '
                           'Blanco = tinta (cubre), negro = deja ver lo de debajo. Misma duración y ritmo que su pareja '
                           'texturada en video/transiciones/tinta_4k.',
               licencia='Gumroad (Studio DamDam): uso propio, no redistribuir', mates=res),
          open(OUT / 'mates.json', 'w'), ensure_ascii=False, indent=1)
