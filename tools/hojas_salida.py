#!/usr/bin/env python3
"""Hojas de contactos de la biblioteca por carpeta (transparencias sobre damero; tileables repetidos 2x2).
Uso: python3 hojas_salida.py DESTINO DIR_HOJAS [prefijo_carpeta]  -> DIR_HOJAS/<carpeta>.jpg (+ _2, _3…)"""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
Image.MAX_IMAGE_PIXELS = None
DEST, OUT = sys.argv[1:3]
PRE = sys.argv[3] if len(sys.argv) > 3 else ''
T = 220; COLS = 7; PER = 42
os.makedirs(OUT, exist_ok=True)
try:
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
    FB = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
except Exception:
    F = FB = None


def checker(w, h, s=8):
    im = Image.new('RGB', (w, h), (205, 205, 205)); d = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range((y // s % 2) * s, w, 2 * s):
            d.rectangle([x, y, x + s - 1, y + s - 1], fill=(160, 160, 160))
    return im


def thumb(p, tile=False):
    im = Image.open(p); im.draft('RGB', (T * 2, T * 2))
    if tile:
        im = im.convert('RGB'); im.thumbnail((T // 2, T // 2))
        t = Image.new('RGB', (im.width * 2, im.height * 2))
        for i in range(2):
            for j in range(2):
                t.paste(im, (i * im.width, j * im.height))
        return t
    im.thumbnail((T, T - 16))
    if im.mode in ('RGBA', 'LA'):
        im = im.convert('RGBA'); bg = checker(im.width, im.height); bg.paste(im, (0, 0), im); return bg
    return im.convert('RGB')


dirs = sorted({os.path.dirname(p) for p in glob.glob(os.path.join(DEST, '**', '*.*'), recursive=True)
               if p.lower().endswith(('.png', '.jpg'))})
for d in dirs:
    rel = os.path.relpath(d, DEST)
    if not rel.startswith(PRE) or rel.startswith('_') or '/hojas' in rel:
        continue
    fs = sorted(f for f in glob.glob(os.path.join(d, '*')) if f.lower().endswith(('.png', '.jpg')) and not f.endswith('_trama.jpg'))
    tile = rel.startswith('tileables')
    for k in range(0, len(fs), PER):
        ch = fs[k:k + PER]
        rows = (len(ch) + COLS - 1) // COLS
        sh = Image.new('RGB', (COLS * (T + 4), rows * (T + 4) + 26), (28, 28, 28)); dr = ImageDraw.Draw(sh)
        dr.text((6, 4), '%s  (%d-%d de %d)%s' % (rel, k + 1, k + len(ch), len(fs), '  · repetidos 2x2' if tile else ''), fill=(255, 220, 0), font=FB)
        for i, f in enumerate(ch):
            x, y = (i % COLS) * (T + 4), 26 + (i // COLS) * (T + 4)
            try:
                th = thumb(f, tile); sh.paste(th, (x + (T - th.width) // 2, y + 14))
            except Exception as e:
                dr.text((x, y + 40), 'ERR', fill=(255, 0, 0))
            dr.text((x + 2, y), '%d %s' % (i, os.path.basename(f)[:30]), fill=(140, 255, 140), font=F)
        name = rel.replace('/', '__') + ('' if k == 0 else '_%d' % (k // PER + 1))
        sh.save(os.path.join(OUT, name + '.jpg'), quality=82)
print('ok')
