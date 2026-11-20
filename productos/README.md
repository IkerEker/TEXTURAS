# productos/ · productos comunes (los pedían varios plugins)

| Producto | Carpeta | Formato | Origen | Para |
|---|---|---|---|---|
| Cintas de trazo enderezadas (88) | `cintas_trazo/` + `cintas.json` | PNG gris 8 bits, filas a lo largo (fila 0 = arranque), 0 = papel, 255 = tinta; `mh`, `ar`, familia, origen `or:` | A mano 2.38.0 `js/texdata.js` (**byte a byte**: md5 de cada cinta = el de A mano) | A mano, Trazo, Cartelator, NEONIZADOR (sello/arrastre) |
| Sellos de relieve (50) | `sellos_relieve/` + `sellos.json` | PNG gris 8 bits, 128 = neutro, luz desde arriba; S 20, M 36, L 56 px | A mano `js/grumosdata.js` (byte a byte) | A mano, cualquiera con relieve de pintura |
| Piezas sueltas finas (1.328) | `piezas_neonizador/` (+ `fuego.json`, `goteos.json`, `catalogo.json` con medidas) | PNG RGBA/LA sin premultiplicar, alfa = luz o cobertura; medidas en px del recorte | NEONIZADOR rama `biblioteca-texturas` f7afed1, `BIBLIOTECA/elementos` (copias exactas, **salvo 17 rehechas el 20-11-2026**: estaban cortadas, con costura o con croma; mismo nombre, ver `piezas_neonizador/REHECHAS.json`; la copia exacta vieja sigue como original heredado `or:` y NEONIZADOR no lee ninguna) | NEONIZADOR, PAPELATOR (moho, quemaduras), Analog FX/A mano (goteos) |
| Papeles grises a escala (32) | `papel_gris/` + `papeles.json` | PNG gris 8 bits tileable, 128 = papel plano, `tile_mm`, `px_por_mm`, `ganancia` | `tileables/papel` con escala conocida (`tools/atlas/producto_papel_gris.py`) | A mano (grano real), Trazo (soportes), NEONIZADOR, Cartelator |
| Mates de tinta 4K (21) | `mates_tinta_4k/` + `mates.json` | MP4 H.264 4K gris, 25 fps, 1 s; blanco = tinta (cubre), negro = deja ver; cobertura medida por fotograma | Studio DamDam `Matte_MOVs` (alfa del autor, `tools/atlas/producto_mates_tinta.py`) · Gumroad: no redistribuir | NEONIZADOR vídeo, montaje automático (pareja de `video/transiciones/tinta_4k`) |
| Alfa de croma | `tools/atlas/metodo_bordes_matte_papelator.py` | método | PAPELATOR `tools/bordes_matte.py` | cualquiera con fotos sobre verde |

Hojas de contactos: `productos/hojas/` (todo revisado a ojo el 19-11-2026). Las piezas de NEONIZADOR no incluyen sus
640 trazos sueltos (mismas fotos que `trazos/` de TEXTURAS; pendientes de comparar).
Regenerar: `python3 tools/atlas/productos_amano.py <a-mano>` · `python3 tools/atlas/producto_papel_gris.py`.
