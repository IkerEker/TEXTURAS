"""Qué es cada imagen de Biblioteca/AÑADIDOS/COLLAGE (revisado a ojo, 19-11-2026, hojas de vista 0–8).

MAT: material → familia (carpeta), descripción, comportamiento óptico, borde, si se rellenan los huecos interiores,
radio para agrupar trozos de una misma pieza (px a 2048), modo recomendado y usos.
  óptica: 'opaco' (alfa = cobertura, bordes y fibras con alfa parcial)
          'translucido' / 'transparente' (alfa mínima respecto al fondo medido: el material deja ver lo de debajo)
IMG: nº de la hoja de vista → material (los nº salen de inv.json, orden alfabético de ruta).
"""

MAT = {
    'papel_blanco':   ('papeles/blanco', 'papel blanco de oficina rasgado a mano', 'opaco', 'rasgado con fibras', False, 15, 'normal'),
    'tira_papel':     ('papeles/tiras', 'tira de papel blanco rasgada', 'opaco', 'rasgado', False, 15, 'normal'),
    'cuaderno':       ('papeles/cuaderno', 'hoja de cuaderno arrancada (perforaciones o espiral)', 'opaco', 'cortado + arrancado por la perforación', False, 15, 'normal'),
    'kraft':          ('papeles/kraft', 'papel/cartón kraft marrón rasgado', 'opaco', 'rasgado con fibras', False, 15, 'normal'),
    'envejecido':     ('papeles/envejecido', 'papel antiguo amarillento con bordes gastados', 'opaco', 'gastado / rasgado', False, 15, 'normal'),
    'periodico':      ('papeles/periodico', 'recorte de periódico antiguo (texto en español)', 'opaco', 'rasgado', False, 15, 'normal'),
    'seda':           ('papeles/seda', 'papel de seda / tisú / vegetal fibroso, translúcido', 'translucido', 'rasgado deshilachado', True, 25, 'normal'),
    'cartulina_azul': ('papeles/cartulina_azul', 'polígono de cartulina azul cobalto cortado a cúter', 'opaco', 'cortado recto', True, 15, 'normal'),
    'estampado':      ('papeles/estampado', 'polígono recortado de papel impreso (azul, rojo y crema)', 'opaco', 'cortado recto', True, 15, 'normal'),
    'cinta_plata':    ('cintas/americana', 'cinta americana gris plateada con trama', 'opaco', 'rasgado con hilos', True, 20, 'normal'),
    'cinta_transp':   ('cintas/transparente', 'celo / cinta de embalaje transparente', 'transparente', 'cortado dentado', True, 25, 'normal'),
    'cinta_ambar':    ('cintas/ambar', 'cinta de embalaje marrón ámbar translúcida', 'translucido', 'cortado', True, 25, 'normal'),
    'cinta_negra':    ('cintas/aislante_negra', 'cinta aislante de vinilo negra', 'opaco', 'cortado a tijera', True, 15, 'normal'),
    'carrocero':      ('cintas/carrocero', 'cinta de carrocero de papel crepé beige', 'opaco', 'rasgado a mano', True, 15, 'normal'),
    'washi':          ('cintas/washi', 'washi tape de papel japonés de color (ligeramente translúcido)', 'opaco', 'rasgado con fibras', True, 15, 'normal'),
    'cinta_tela':     ('cintas/tela_blanca', 'cinta blanca de tela / esparadrapo', 'opaco', 'cortado y rasgado', True, 15, 'normal'),
    'correctora':     ('cintas/correctora', 'trazo de cinta correctora blanca (o tira blanca fina gastada)', 'opaco', 'transferencia con cortes', True, 15, 'normal'),
    'etiq_blanca':    ('etiquetas/blancas', 'etiqueta adhesiva blanca (papel o térmica), algunas con esquina levantada', 'opaco', 'troquelado', True, 15, 'normal'),
    'etiq_vieja':     ('etiquetas/envejecidas', 'etiqueta de papel envejecida, manchas y esquina despegada', 'opaco', 'troquelado gastado', True, 15, 'normal'),
    'etiq_rota':      ('etiquetas/arrancadas', 'pegatina arrancada / rota con capas de papel y restos de adhesivo', 'opaco', 'arrancado (deslaminado)', True, 30, 'normal'),
    'peg_blanca':     ('pegatinas/blancas', 'pegatina blanca mate (círculo, óvalo, rectángulo)', 'opaco', 'troquelado', True, 15, 'normal'),
    'peg_vinilo':     ('pegatinas/vinilo', 'pegatina de vinilo brillante (rojo, azul, verde)', 'opaco', 'troquelado', True, 15, 'normal'),
    'peg_kraft':      ('pegatinas/kraft', 'pegatina de papel kraft', 'opaco', 'troquelado', True, 15, 'normal'),
    'postit':         ('notas/amarillas', 'nota adhesiva amarilla (Post-it)', 'opaco', 'cortado industrial', True, 15, 'normal'),
    'notas':          ('notas/colores', 'nota adhesiva de color (rosa, verde, azul)', 'opaco', 'cortado industrial', True, 15, 'normal'),
    'pintura':        ('pintura/blanca', 'mancha de pintura blanca / corrector líquido seco con relieve', 'opaco', 'pincelada', True, 40, 'normal'),
    'gel':            ('adhesivos/gel', 'gota o parche de gel / cola transparente', 'transparente', 'redondeado', True, 40, 'normal'),
    'residuo':        ('adhesivos/residuos', 'restos de adhesivo y papel al despegar una pegatina', 'transparente', 'irregular', True, 70, 'normal'),
    'grafito':        ('grafito', 'garabatos de grafito / carboncillo sobre papel blanco (hoja entera)', 'grafito', 'hoja entera', False, 0, 'multiplicar'),
}

_G = {}
def _a(mat, *ns):
    for n in ns: _G[n] = mat
_a('estampado', 0, 1, 3, 21, 29, 43, 50, 231)
_a('kraft', 2, 9, 16, 33, 53, 55, 224, 225)
_a('papel_blanco', 4, 5, 6, 24, 39, 44, 46, 51, 216, 217, 218, 219, 220, 221, 232)
_a('tira_papel', 17, 23, 25, 47, 54, 247, 248, 249, 250)
_a('envejecido', 7, 18, 31, 213, 214, 223)
_a('seda', 8, 10, 11, 12, 20, 26, 27, 38, 45, 49, 61, 222, 226)
_a('periodico', 13, 14, 15, 22, 35, 36, 41, 233, 234)
_a('cuaderno', 19, 28, 30, 34, 56, 57, 58, 59, 60, 215)
_a('cartulina_azul', 32, 37, 40, 42, 48, 52, 227, 228, 229, 230)
_a('cinta_plata', 62, 65, 94, 116, 118, 120, 130, 132, 211)
_a('cinta_transp', 63, 66, 70, 175, 176, 210)
_a('cinta_ambar', 64, 67, 68, 69, 101, 121, 138, 177, 193, 194)
_a('etiq_vieja', 71, 77, 78, 79, 81, 91, 106, 109, 133, 135, 139)
_a('etiq_rota', 72, 80, 83, 92, 102, 112, 119, 124, 134)
_a('etiq_blanca', 73, 74, 75, 76, 117, 128)
_a('gel', 82, 140, 149, 150, 151, 198, 199, 200, 206)
_a('peg_kraft', 84, 100, 127)
_a('cinta_tela', 85, 86, 136, 137)
_a('pintura', 87, 97, 110, 141, 142, 160, 173, 201, 202, 203, 204, 205)
_a('cinta_negra', 88, 93, 103, 188, 189, 190, 191, 192, 209)
_a('postit', 89, 115, 122, 143, 144, 145)
_a('washi', 90, 104, 129, 195, 196, 197)
_a('peg_blanca', 95, 107, 126, 152, 153, 154)
_a('carrocero', 96, 98, 123, 184, 185, 186, 187, 207)
_a('peg_vinilo', 99, 113, 125, 155, 156, 157, 158, 159, 212)
_a('notas', 105, 108, 111, 114, 131, 146, 147, 148)
_a('residuo', 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172)
_a('correctora', 174, 178, 179, 180, 181, 182, 183, 208)
_a('grafito', *range(235, 247))
IMG = _G
assert sorted(IMG) == list(range(251)), sorted(set(range(251)) - set(IMG))
