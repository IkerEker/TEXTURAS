"""Hoja de contactos de una carpeta de PNG (alfa sobre damero). Uso: hoja.py <carpeta> <salida.jpg> [lado]"""
import sys, glob, os
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]; L = int(sys.argv[3]) if len(sys.argv) > 3 else 110
fs = sorted(glob.glob(os.path.join(src, '*.png')) + glob.glob(os.path.join(src, '*.jpg')))
cols = 14; rows = (len(fs) + cols - 1) // cols
im = Image.new('RGB', (cols * L, max(1, rows) * (L + 12) + 18), (28, 28, 28)); d = ImageDraw.Draw(im)
d.text((4, 3), f'{src}  ({len(fs)})', fill=(255, 210, 0))
ch = Image.new('RGB', (L, L)); dc = ImageDraw.Draw(ch)
for y in range(0, L, 10):
    for x in range(0, L, 10):
        dc.rectangle([x, y, x + 9, y + 9], fill=(150, 150, 150) if (x // 10 + y // 10) % 2 else (100, 100, 100))
for i, f in enumerate(fs):
    t = Image.open(f); t.thumbnail((L - 4, L - 4))
    x, y = (i % cols) * L, (i // cols) * (L + 12) + 18
    if t.mode in ('RGBA', 'LA', 'P'):
        t = t.convert('RGBA'); bg = ch.crop((0, 0) + t.size).convert('RGBA'); bg.alpha_composite(t); t = bg
    im.paste(t.convert('RGB'), (x + 2, y + 12)); d.text((x + 2, y), os.path.basename(f)[:17], fill=(160, 220, 160))
im.save(out, quality=82)
