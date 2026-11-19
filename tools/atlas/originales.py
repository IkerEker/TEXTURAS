"""Construye originales/MANIFIESTO.json: los originales de los plugins, deduplicados por md5, intactos, con todas
sus rutas antiguas. Lee tools/estado/inv2.json + md5_inventario.json y los anexos de plugins/.
Uso: python3 tools/atlas/originales.py   (desde la raíz de TEXTURAS)"""
import json, collections
inv = json.load(open('tools/estado/inv2.json'))
md5 = json.load(open('tools/estado/md5_inventario.json'))
REPO = {'a-mano': ('IkerEker/a-mano', 'main'), 'analog-fx-plugin': ('IkerEker/analog-fx-plugin', 'main'),
        'papelator': ('IkerEker/papelator', 'main'), 'trazo': ('IkerEker/trazo', 'main'),
        'neonizador': ('IkerEker/neonizador', 'main'),                 # fotos originales (FUEGO/, TEXTURAS*/…)
        'neonizador_bt': ('IkerEker/neonizador', 'biblioteca-texturas')}  # su BIBLIOTECA/ (heredados)
EXTRA = {'a-mano/referencias/texturas/pared_piel_4.jpg', 'a-mano/referencias/texturas/pintura_granos_2.jpg',
         'a-mano/referencias/texturas/pintura_grumos_1.jpg', 'a-mano/referencias/texturas/pintura_grumos_3.jpg'}
grupos = collections.OrderedDict()
for e in inv:
    if e['repo'] not in REPO or e['repo'] == 'neonizador_bt': continue                       # ESTILO fuera, por decisión de Iker
    if not (e['rol'] == 'fuente' or e['ruta'] in EXTRA): continue
    m = md5[e['ruta']]
    g = grupos.setdefault(m, dict(md5=m, bytes=e['bytes'], tipo=e['tipo'], w=e.get('w'), h=e.get('h'), rutas=[]))
    g['rutas'].append(e['ruta'])
pref = ['papelator', 'a-mano', 'analog-fx-plugin', 'trazo', 'neonizador', 'neonizador_bt']
for g in grupos.values():
    g['rutas'].sort(key=lambda r: (pref.index(r.split('/')[0]), r))
    g['id'] = 'or:' + g['md5']
    g['archivo'] = 'originales/' + g['rutas'][0]          # se conserva el nombre (PAPELATOR siembra con él)
    g['duplicados'] = g['rutas'][1:]
# heredados de NEONIZADOR: los archivos de su BIBLIOTECA que build_texpack empaqueta (JPG re-guardados y recortes)
her = []
import fnmatch
ATLAS = ['BIBLIOTECA/elementos/fuego/chispas/*.png', 'BIBLIOTECA/elementos/fuego/pavesas/*.png',
         'BIBLIOTECA/elementos/moho/manchitas/*.png']          # piezas de los atlas fg_chispas, fg_pavesas, mo_manchitas
for x in json.load(open('plugins/neonizador/fuentes.json')):
    if x['empaquetada'] or any(fnmatch.fnmatch(x['ruta'], p) for p in ATLAS):
        her.append(dict(id='or:' + x['md5'], md5=x['md5'], bytes=x['bytes'],
                        archivo='originales/heredado/neonizador/' + x['ruta'], ruta_en_repo='neonizador/' + x['ruta'], clon='neonizador_bt',
                        usada_por_efecto=x['usada_por_efecto']))
out = dict(descripcion='Originales intactos de los plugins (deduplicados por md5). archivo = dónde está en Biblioteca/; '
                       'rutas = todas sus rutas en los repos (la primera es la que se copia).',
           repos={k: dict(repo=v[0], rama=v[1]) for k, v in REPO.items()},
           originales=list(grupos.values()), heredado_neonizador=her,
           heredado_nota='NEONIZADOR construye sus .bin desde estos archivos (re-guardados en JPG y recortes de sus '
                         'extract_*.py). Se conservan para que su plugin/tex salga byte a byte; además se copian los '
                         'catálogos BIBLIOTECA/elementos/**/*.json.')
json.dump(out, open('originales/MANIFIESTO.json', 'w'), ensure_ascii=False, indent=1)
n = len(grupos); dup = sum(len(g['duplicados']) for g in grupos.values())
print('originales únicos', n, '· rutas duplicadas', dup, '· GB', round(sum(g['bytes'] for g in grupos.values()) / 1e9, 2),
      '· heredados NEONIZADOR', len(her), round(sum(h['bytes'] for h in her) / 1e6, 1), 'MB')
print(collections.Counter(g['rutas'][0].split('/')[0] for g in grupos.values()))

# versión ligera para el script de Windows (montar_biblioteca.ps1)
t = [[g['archivo'], g['md5'], g['rutas']] for g in out['originales']] + \
    [[h['archivo'], h['md5'], ['neonizador_bt/' + h['ruta_en_repo'].split('/', 1)[1]]] for h in her]
json.dump(dict(repos=out['repos'], tareas=t), open('originales/montaje.json', 'w'), ensure_ascii=False, separators=(',', ':'))
