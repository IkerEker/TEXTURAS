"""Monta (o comprueba) la Biblioteca local de Iker, la misma en cada ordenador.

    python montar_biblioteca.py --raiz D:/Biblioteca [--acidbite C:/Users/ikerg/Downloads/ADIDBITE/BIBLIOTECA]
                                [--fuentes D:/fuentes] [--solo-comprobar]

Qué hace (no borra nada en ningún sitio):
1. `TEXTURAS/`: si no existe, clona este repo (git, rama main).
2. `originales/`: copia desde los repos de los plugins (clonados en --fuentes; si no están, los clona con
   `git clone --depth 1`) cada original del MANIFIESTO, **byte a byte**, y comprueba su md5. Los heredados de
   NEONIZADOR van a `originales/heredado/neonizador/` junto con sus catálogos `BIBLIOTECA/elementos/**/*.json`.
3. `ACIDBITE/`: si se da --acidbite y `ACIDBITE/` no existe, **mueve** la carpeta del pack ahí (mismo disco: instantáneo;
   otro disco: copia y deja la original intacta). Comprueba que están los archivos del inventario.
4. `generadas/`: la crea vacía.
5. Escribe `Biblioteca/ESTADO_BIBLIOTECA.json` con lo que hay y lo que falta.

Después, en cada plugin: `TEXTURAS_ROOT=<raiz>` y sus herramientas de construcción leen por id (ver MAPA.md).
Solo usa la biblioteca estándar de Python 3 y git.
"""
import argparse, hashlib, json, os, shutil, subprocess, sys, csv
from pathlib import Path

AQUI = Path(__file__).resolve().parents[2]          # raíz del repo TEXTURAS


def md5(p, n=1 << 20):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(n), b''):
            h.update(b)
    return h.hexdigest()


def clonar(url, destino, rama=None):
    cmd = ['git', 'clone', '--depth', '1'] + (['--branch', rama] if rama else []) + [url, str(destino)]
    print('  ·', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raiz', required=True, help='carpeta Biblioteca (= TEXTURAS_ROOT)')
    ap.add_argument('--fuentes', help='carpeta con los clones de los plugins (por defecto <raiz>/_fuentes)')
    ap.add_argument('--acidbite', help='carpeta actual del pack (la que contiene 01_TRANSICIONES…)')
    ap.add_argument('--solo-comprobar', action='store_true')
    a = ap.parse_args()
    R = Path(a.raiz); R.mkdir(parents=True, exist_ok=True)
    F = Path(a.fuentes) if a.fuentes else R / '_fuentes'
    man = json.load(open(AQUI / 'originales' / 'MANIFIESTO.json', encoding='utf-8'))
    estado = dict(raiz=str(R), faltan=[], md5_distinto=[], copiados=0, ya_estaban=0)

    # 1. TEXTURAS
    if not (R / 'TEXTURAS').exists() and not a.solo_comprobar:
        clonar('https://github.com/IkerEker/TEXTURAS.git', R / 'TEXTURAS')

    # 2. originales
    for repo, info in man['repos'].items():
        if not (F / repo).exists() and not a.solo_comprobar:
            F.mkdir(parents=True, exist_ok=True)
            clonar(f"https://github.com/{info['repo']}.git", F / repo, info['rama'])
    tareas = [(g['archivo'], g['md5'], g['rutas']) for g in man['originales']]
    tareas += [(h['archivo'], h['md5'], ['neonizador_bt/' + h['ruta_en_repo'].split('/', 1)[1]]) for h in man['heredado_neonizador']]
    for archivo, m, rutas in tareas:
        dst = R / archivo
        if dst.exists() and md5(dst) == m:
            estado['ya_estaban'] += 1; continue
        if a.solo_comprobar:
            estado['faltan'].append(archivo); continue
        src = next((F / r for r in rutas if (F / r).exists()), None)
        if src is None:
            estado['faltan'].append(archivo); continue
        if md5(src) != m:
            estado['md5_distinto'].append(str(src)); continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst); estado['copiados'] += 1
    nb = F / 'neonizador_bt' / 'BIBLIOTECA' / 'elementos'
    if nb.exists() and not a.solo_comprobar:
        for j in nb.rglob('*.json'):
            d = R / 'originales' / 'heredado' / 'neonizador' / j.relative_to(F / 'neonizador_bt')
            d.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(j, d)

    # 3. AcidBite
    ab = R / 'ACIDBITE'
    if a.acidbite and not ab.exists() and not a.solo_comprobar:
        src = Path(a.acidbite)
        try:
            os.rename(src, ab); print('  · AcidBite movido a', ab)
        except OSError:
            print('  · otro disco: copiando AcidBite (190 GB) sin tocar el original…'); shutil.copytree(src, ab)
    if ab.exists():
        inv = AQUI / 'acidbite' / 'datos' / 'inventario.csv'
        with open(inv, encoding='utf-8-sig') as f:
            for row in csv.DictReader(f):
                if not (ab / row['ruta'].replace('\\', '/')).exists():
                    estado['faltan'].append('ACIDBITE/' + row['ruta'])
    else:
        estado['faltan'].append('ACIDBITE/ (pásale --acidbite)')

    # 4. generadas
    (R / 'generadas').mkdir(exist_ok=True)
    json.dump(estado, open(R / 'ESTADO_BIBLIOTECA.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f"copiados {estado['copiados']} · ya estaban {estado['ya_estaban']} · faltan {len(estado['faltan'])} · "
          f"md5 distinto {len(estado['md5_distinto'])}")
    sys.exit(1 if estado['faltan'] or estado['md5_distinto'] else 0)


if __name__ == '__main__':
    main()
