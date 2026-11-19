"""Hojas de revisión compactas por familia: por imagen, original | recorte en su sitio sobre magenta | sobre negro."""
import json, sys, collections
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
from collage_tabla import IMG, MAT
SRC = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
R = Path('collage/_trabajo/resultados'); inv = json.load(open('collage/_trabajo/inv.json'))
C = 290; PER = 14
fam = collections.defaultdict(list)
for n in range(len(inv)):
    if inv[n]['dup_de'] is None: fam[MAT[IMG[n]][0]].append(n)
SEL=[int(x) for x in sys.argv[3:]]
for f, ns in sorted(fam.items()):
    ns=[n for n in ns if not SEL or n in SEL]
    if not ns: continue
    for s in range(0, len(ns), PER):
        chunk = ns[s:s + PER]; rows = (len(chunk) + 1) // 2
        o = Image.new('RGB', (2 * (3 * C + 4) + 20, rows * (C + 16)), 'white'); d = ImageDraw.Draw(o)
        for k, n in enumerate(chunk):
            r = json.load(open(R / ('%04d.json' % n)))
            org = Image.open(SRC / inv[n]['rel']).convert('RGB'); W, H = org.size
            lay = Image.new('RGBA', (W, H), (0, 0, 0, 0))
            for p in r.get('piezas', []):
                x0, y0, w, h = p.get('recorte', [0, 0, 0, 0]); lay.alpha_composite(Image.open(p['archivo']).convert('RGBA'), (x0, y0))
            x = (k % 2) * (3 * C + 24); y = (k // 2) * (C + 16)
            o.paste(org.resize((C, C)), (x, y))
            for j, bg in enumerate([(230, 40, 160), (0, 0, 0)]):
                b = Image.new('RGBA', (W, H), bg + (255,)); b.alpha_composite(lay); o.paste(b.convert('RGB').resize((C, C)), (x + (j + 1) * (C + 2), y))
            d.text((x + 2, y + C + 2), '%d · %d piezas · %s' % (n, len(r.get('piezas', [])), inv[n]['rel'][-40:]), fill='black')
        o.save(OUT / ('%s_%d.jpg' % (f.replace('/', '__'), s // PER + 1)), quality=80)
        print(OUT / ('%s_%d.jpg' % (f.replace('/', '__'), s // PER + 1)))
