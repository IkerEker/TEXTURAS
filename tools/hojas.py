#!/usr/bin/env python3
"""Hojas de contactos de las imágenes fuente definitivas, agrupadas por carpeta.
Uso: python3 -I hojas.py inv2.json RAIZ_REPOS DIR_SALIDA
Cada miniatura lleva un número; DIR_SALIDA/indice.json mapea hoja#n -> ruta.
El alfa se muestra sobre damero.
"""
import sys, os, json, collections
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
T = 200; COLS = 8; ROWS = 5; PAD = 4; LAB = 14

def checker(w, h, s=10):
    im = Image.new('RGB', (w, h), (200, 200, 200))
    dr = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range((y // s % 2) * s, w, 2 * s):
            dr.rectangle([x, y, x + s - 1, y + s - 1], fill=(150, 150, 150))
    return im

def thumb(p):
    im = Image.open(p)
    im.draft('RGB', (T * 2, T * 2))
    im.thumbnail((T, T - LAB))
    if im.mode in ('RGBA', 'LA', 'PA', 'P'):
        im = im.convert('RGBA')
        bg = checker(im.width, im.height)
        bg.paste(im, (0, 0), im)
        return bg
    return im.convert('RGB')

def main():
    inv, root, out = sys.argv[1:4]
    os.makedirs(out, exist_ok=True)
    d = json.load(open(inv))
    sel = [x for x in d if x['rol'] == 'fuente' and x.get('tipo') == 'imagen'
           and x['canonico'] == x['ruta'] and x.get('similar_a', x['ruta']) == x['ruta']]
    grp = collections.defaultdict(list)
    for x in sel:
        grp[os.path.dirname(x['ruta'])].append(x)
    font = ImageFont.load_default()
    indice = {}
    n = 0
    for carpeta in sorted(grp):
        xs = sorted(grp[carpeta], key=lambda x: x['ruta'])
        per = COLS * ROWS
        for k in range(0, len(xs), per):
            chunk = xs[k:k + per]
            rows = (len(chunk) + COLS - 1) // COLS
            sheet = Image.new('RGB', (COLS * (T + PAD), rows * (T + PAD) + 22), (30, 30, 30))
            dr = ImageDraw.Draw(sheet)
            n += 1
            name = 'h%03d' % n
            dr.text((4, 4), '%s  %s  (%d-%d de %d)' % (name, carpeta, k + 1, k + len(chunk), len(xs)),
                    fill=(255, 255, 0), font=font)
            for i, x in enumerate(chunk):
                cx, cy = (i % COLS) * (T + PAD), 22 + (i // COLS) * (T + PAD)
                try:
                    th = thumb(os.path.join(root, x['ruta']))
                    sheet.paste(th, (cx + (T - th.width) // 2, cy + LAB))
                except Exception as e:
                    dr.text((cx, cy + 40), 'ERR', fill=(255, 0, 0), font=font)
                lab = '%d %dx%d%s' % (i, x['w'], x['h'], ' A' if x.get('alfa') else '')
                dr.text((cx + 2, cy + 1), lab, fill=(120, 255, 120), font=font)
                indice['%s#%d' % (name, i)] = x['ruta']
            sheet.save(os.path.join(out, name + '.jpg'), quality=80)
    json.dump(indice, open(os.path.join(out, 'indice.json'), 'w'), ensure_ascii=False, indent=0)
    print(n, 'hojas', len(indice), 'imágenes')

if __name__ == '__main__':
    main()
