"""Tabla de nombres oficiales: nombre_oficial <- alias (plugins, TEXTURAS, ACIDBITE en inglés).
Uso: python3 tools/atlas/nombres.py -> indice/nombres.json"""
import json
N = {
 # técnicas de dibujo y pintura
 'boligrafo': ['boli', 'bic', 'ballpoint'], 'rotulador': ['rotu', 'marker', 'rotulador_anotacion'],
 'gouache': ['guache', 'pin_guache', 'gouache_opaco'], 'oleo': ['pin_gouache (Trazo: óleo)', 'pin_oleo', 'oil'],
 'pincel_fino': ['pincelfino'], 'pincel_seco': ['brocha seca', 'dry brush'], 'aguada': ['aguadas', 'wash', 'tinta aguada'],
 'acuarela': ['watercolor', 'acuarela_grano', 'acuarela_aguada'], 'lapiz': ['lápiz', 'grafito (trazo)', 'pencil'],
 'carbon': ['carboncillo', 'charcoal'], 'cera': ['ceras', 'crayon', 'cera (técnica)'], 'tinta': ['ink', 'tinta_brocha', 'tinta_anotacion'],
 'pastel': ['pin_pastel'],
 # sellos y relieves
 'sello_seco': ['sello en seco', 'relieve notarial'], 'sello_tinta': ['sello de caucho', 'tampón', 'stamp (tinta)'],
 'sello_brocha': ['sello (NEONIZADOR: efecto de brocha)'], 'sello_relieve': ['grumo', 'grumos', 'lump'],
 # papel y soporte
 'papel_kraft': ['kraft (papel)'], 'carton_kraft': ['kraft (cartón)', 'cardboard'], 'cera_vela': ['cera (de vela)'],
 'papel_periodico': ['periodico', 'newspaper'], 'papel_acuarela': ['acuarela (papel)', 'papel_rugoso'],
 'papel_plegado': ['paper fold', 'pliegue', 'fold'], 'papel_arrugado': ['paper crumble', 'crumble', 'arrugado'],
 'lienzo': ['canvas', 'linen', 'tela'], 'cinta_adhesiva': ['scotch tape', 'tape', 'cinta', 'celo', 'gaffer'],
 'borde_rasgado': ['rip', 'rips', 'rasgado'], 'borde_quemado': ['burning paper', 'quemado (borde)'],
 # película y analógico
 'grano_pelicula': ['grain', 'film grain'], 'ventanilla': ['gate', 'film gate', 'filmgate'], 'perforacion': ['sprocket', 'sprocket holes'],
 'quemado_pelicula': ['burn', 'film burn', 'filmburn'], 'fuga_de_luz': ['light leak', 'leak', 'fuga'],
 'polvo_y_rayas': ['dust', 'dirt', 'scratches', 'polvo_aranazos'], 'visor': ['viewfinder'],
 'mascara_fosforo': ['shadow mask', 'rejilla RGB', 'CRT dirt'], 'lineas_de_barrido': ['scanlines'],
 'nieve_analogica': ['noise', 'video noise', 'static'], 'glitch': ['cyber', 'glitchy', 'datamosh', 'mosh'],
 'vhs': ['video home system', 'tracking'],
 # elementos
 'llama': ['flame', 'fg_lengua', 'fg_masa', 'fg_base', 'lengua', 'masa'], 'pavesa': ['ember', 'brasa', 'fg_pavesas'],
 'chispa': ['spark', 'fg_chispas'], 'humo': ['smoke', 'fg_humo', 'humo_v'], 'goteo': ['drip', 'gt_', 'gota (pintura que cuelga)'],
 'gota_agua': ['water drop', 'gotas_cristal', 'gotas'], 'salpicadura': ['splatter', 'splash', 'salpicaduras'],
 'pompa': ['bubble', 'bf_suelta', 'burbuja'], 'espuma': ['foam', 'bf_tile', 'espuma_tile'], 'moho': ['mold', 'mo_colonia', 'mo_tile'],
 'refraccion': ['optical elements', 'prisma', 'lens'], 'marcador_animado': ['animated markers', 'cinemarkers'],
 # transiciones (colocación)
 'encima_corte': ['overlay transition', 'sobre el corte'], 'mascara': ['track matte', 'mate', 'matte'],
 'intercalado': ['plano intercalado', 'wipe (entre planos)'],
}
MODOS = {'normal': ['Normal'], 'multiplicar': ['Multiply'], 'trama': ['Screen', 'Pantalla'], 'superponer': ['Overlay'],
         'luz_suave': ['Soft Light'], 'luz_fuerte': ['Hard Light'], 'luz_focal': ['Pin Light'], 'diferencia': ['Difference'],
         'sobreexponer_lineal': ['Linear Dodge (Add)', 'Add', 'Añadir'], 'sobreexponer_color': ['Color Dodge'],
         'aclarar': ['Lighten'], 'color_mas_claro': ['Lighter Color'], 'mascara_alfa': ['Track Matte Alpha', 'Matte Alpha'],
         'mascara_luma': ['Track Matte Luma', 'Matte Luma', 'Luma Matte']}
alias = {}
for k, v in N.items():
    for a in v: alias.setdefault(a.lower(), k)
json.dump(dict(nota='Los archivos NO se renombran. Cada plugin conserva sus nombres internos (ver plugins/<p>/uso_id.json). '
                    'Evitar «organica» y «trazos» como familia genérica.',
               oficiales=N, alias=alias, modos=MODOS), open('indice/nombres.json', 'w'), ensure_ascii=False, indent=1)
print(len(N), 'nombres,', len(alias), 'alias')
