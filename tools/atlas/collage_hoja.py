"""Hojas de revisión del collage: cada pieza sobre damero, sobre negro y sobre un color fuerte (delatan halos y alfa mala)."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw

def damero(w, h, s=16):
    im = Image.new('RGB', (w, h), (200, 200, 200)); d = ImageDraw.Draw(im)
    for y in range(0, h, s):
        for x in range((y // s % 2) * s, w, 2 * s): d.rectangle([x, y, x + s - 1, y + s - 1], fill=(150, 150, 150))
    return im

def hoja(fichas, out, cel=230, cols=4):
    rows = (len(fichas) + cols - 1) // cols
    W = cols * (3 * cel + 10); H = rows * (cel + 16)
    o = Image.new('RGB', (W, H), (255, 255, 255)); d = ImageDraw.Draw(o)
    for k, f in enumerate(fichas):
        p = Image.open(f['archivo']).convert('RGBA'); p.thumbnail((cel - 6, cel - 6))
        x0 = (k % cols) * (3 * cel + 10); y0 = (k // cols) * (cel + 16)
        for j, bg in enumerate([damero(cel, cel), Image.new('RGB', (cel, cel), (0, 0, 0)), Image.new('RGB', (cel, cel), (230, 40, 160))]):
            b = bg.copy(); b.paste(p, ((cel - p.width) // 2, (cel - p.height) // 2), p); o.paste(b, (x0 + j * cel, y0))
        d.text((x0 + 2, y0 + cel + 2), f['archivo'].split('/')[-1][:-4] + ('  +sombra' if 'sombra' in f else ''), fill=(0, 0, 0))
    o.save(out, quality=82)

if __name__ == '__main__':
    R = Path('collage/_trabajo/resultados')
    fs = []
    for n in sys.argv[2:] or sorted(p.stem for p in R.glob('*.json')):
        r = json.load(open(R / ('%04d.json' % int(n))))
        fs += r.get('piezas', [])
    hoja(fs, sys.argv[1])
