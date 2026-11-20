"""Hoja de contactos de una carpeta de productos/piezas_neonizador (mismo estilo que las de productos/hojas).
  python3 tools/atlas/hoja_piezas.py burbujas gotas goteos/sueltos burbujas_foto/tiles
Transparencias sobre damero; 14 por fila, celda 110 px."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

P = Path('productos/piezas_neonizador'); H = Path('productos/hojas')
COL, PASO, T, CAB, ALTO = 14, 110, 104, 20, 121


def damero(w, h, c=8):
    im = Image.new('RGB', (w, h), (110, 110, 110)); d = ImageDraw.Draw(im)
    for y in range(0, h, c):
        for x in range(0, w, c):
            if (x // c + y // c) % 2: d.rectangle((x, y, x + c - 1, y + c - 1), fill=(150, 150, 150))
    return im


def hoja(sub):
    fs = sorted((P / sub).glob('*.png'))
    filas = (len(fs) + COL - 1) // COL
    W = Image.new('RGB', (COL * PASO, CAB + filas * ALTO), (28, 28, 28)); d = ImageDraw.Draw(W)
    d.text((4, 4), 'productos/piezas_neonizador/%s (%d)' % (sub, len(fs)), fill=(255, 200, 60))
    for i, f in enumerate(fs):
        x, y = (i % COL) * PASO, CAB + (i // COL) * ALTO
        im = Image.open(f); im.thumbnail((T, T))
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); c = damero(im.width, im.height); c.paste(im, (0, 0), im)
        else:
            c = im.convert('RGB')
        W.paste(c, (x, y + 15)); d.text((x + 2, y + 2), f.name[:17], fill=(140, 230, 140))
    out = H / ('neonizador__' + sub.replace('/', '_') + '.jpg'); W.save(out, quality=88); print(out, len(fs))


for s in sys.argv[1:]: hoja(s)
