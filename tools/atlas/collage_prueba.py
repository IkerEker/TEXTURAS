"""Hoja de prueba por imagen: original | lo recortado puesto en su sitio sobre magenta | sobre negro | sobre damero.
Si algo de fondo o de sombra se ha colado, se ve en las columnas 2–4 donde en el original solo hay fondo."""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
from collage_hoja import damero

SRC = Path(sys.argv[2]); R = Path('collage/_trabajo/resultados'); inv = json.load(open('collage/_trabajo/inv.json'))
ns = [int(x) for x in sys.argv[3:]]
C = 420
o = Image.new('RGB', (4 * C + 30, len(ns) * (C + 22)), 'white'); d = ImageDraw.Draw(o)
for k, n in enumerate(ns):
    r = json.load(open(R / ('%04d.json' % n)))
    org = Image.open(SRC / inv[n]['rel']).convert('RGB'); W, H = org.size
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for p in r.get('piezas', []):
        x0, y0, w, h = p['recorte']; lay.alpha_composite(Image.open(p['archivo']).convert('RGBA'), (x0, y0))
    ims = [org]
    for bg in [Image.new('RGB', (W, H), (230, 40, 160)), Image.new('RGB', (W, H), (0, 0, 0)), damero(W, H, 48)]:
        b = bg.convert('RGBA'); b.alpha_composite(lay); ims.append(b.convert('RGB'))
    y = k * (C + 22)
    for j, im in enumerate(ims): o.paste(im.resize((C, C)), (j * (C + 10), y))
    d.text((4, y + C + 4), '%d  %s  ·  %d piezas  %s' % (n, inv[n]['rel'][-50:], len(r.get('piezas', [])),
           ' '.join(p['archivo'].split('/')[-1][:-4] + ('[sombra aparte]' if 'sombra' in p else '') for p in r.get('piezas', []))), fill='black')
o.save(sys.argv[1], quality=85)
