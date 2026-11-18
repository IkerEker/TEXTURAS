#!/usr/bin/env python3
"""Asigna un rol a cada archivo del inventario y agrupa duplicados exactos y casi-duplicados.
Uso: python3 -I roles.py inventario.json salida.json
Roles:
  fuente      material subido por el usuario (lo que hay que procesar)
  procesado   ya procesado por algún plugin (reutilizable tal cual o como referencia de método)
  referencia  obras/fotos de estudio (no son assets; van aparte)
  ruido       capturas de prueba, iconos, miniaturas de UI, dist
"""
import sys, json, re, collections

def rol(r):
    p = r.lower()
    if re.search(r'/(icons|thumbs|dist|dist_ae|tests?)/', p) or re.match(r'a-mano/[^/]+\.png$', p) \
       or 'plugin/assets/swatches' in p or p.startswith('analog-fx-plugin/docs/') \
       or p.startswith('analog-fx-plugin/tools/') or 'resumen_seleccion' in p:
        return 'ruido'
    if 'referencias/' in p or p.startswith('estilo/') or p.startswith('neonizador/muestras/'):
        return 'referencia'
    if p.startswith('papelator/plugin/assets/') or p.startswith('analog-fx-plugin/biblioteca/') \
       or '/hojas/' in p:
        return 'procesado'
    return 'fuente'

def ham(a, b):
    return bin(int(a, 16) ^ int(b, 16)).count('1')

def main():
    d = json.load(open(sys.argv[1]))
    for x in d:
        x['rol'] = rol(x['ruta'])
    # duplicados exactos
    by = collections.defaultdict(list)
    for x in d:
        by[x['sha1']].append(x)
    for v in by.values():
        v.sort(key=lambda x: (x['rol'] != 'fuente', len(x['ruta']), x['ruta']))
        for x in v:
            x['copias'] = len(v)
            x['canonico'] = v[0]['ruta']
    # casi duplicados entre canónicos de imagen (fuente), por phash+dhash
    can = [v[0] for v in by.values() if v[0].get('tipo') == 'imagen' and v[0]['rol'] == 'fuente']
    parent = {x['ruta']: x['ruta'] for x in can}
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for i in range(len(can)):
        a = can[i]
        ra = a['w'] / a['h']
        for j in range(i + 1, len(can)):
            b = can[j]
            if abs(ra - b['w'] / b['h']) > 0.03 * ra:
                continue
            if ham(a['phash'], b['phash']) <= 6 and ham(a['dhash'], b['dhash']) <= 10:
                parent[find(a['ruta'])] = find(b['ruta'])
    grupos = collections.defaultdict(list)
    for x in can:
        grupos[find(x['ruta'])].append(x)
    ng = 0
    for g in grupos.values():
        if len(g) > 1:
            ng += 1
            # mejor versión: más píxeles, luego png sobre jpg, luego más bytes
            g.sort(key=lambda x: (-(x['w'] * x['h']), x['ext'] != '.png', -x['bytes']))
            for x in g:
                x['similar_a'] = g[0]['ruta']
                x['grupo_similar'] = len(g)
    json.dump(d, open(sys.argv[2], 'w'), ensure_ascii=False, indent=0)
    cnt = collections.Counter(x['rol'] for x in d)
    ucnt = collections.Counter(v[0]['rol'] for v in by.values())
    print('archivos por rol', dict(cnt))
    print('únicos por rol', dict(ucnt))
    print('grupos casi-duplicados entre fuentes:', ng,
          'archivos que sobran:', sum(len(g) - 1 for g in grupos.values() if len(g) > 1))
    fin = [x for x in can if x.get('similar_a', x['ruta']) == x['ruta']]
    vids = [v[0] for v in by.values() if v[0].get('tipo') == 'video' and v[0]['rol'] == 'fuente']
    print('imágenes fuente definitivas:', len(fin), ' vídeos fuente únicos:', len(vids))

if __name__ == '__main__':
    main()
