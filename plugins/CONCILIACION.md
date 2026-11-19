# Conciliación de fichas de plugins con TEXTURAS

Estado al 19-11-2026. Fichas recibidas: A mano, Cartelator, Analog FX, NEONIZADOR (Photoshop y vídeo), PAPELATOR.
Pendiente: Trazo. Después: AcidBite y la pasada unificada.

## NEONIZADOR · su `BIBLIOTECA/` paralela (rama `biblioteca-texturas`, commit f7afed1)

Comprobado sobre una copia de la rama (sin vídeos: 2.390 archivos).

| Parte | Archivos | ¿Material nuevo? | Cómo se ha comprobado |
|---|---|---|---|
| `video/` | 57 | **No**: idénticos byte a byte a los que ya procesó TEXTURAS | md5 |
| `texturas/` | 266 | **No**: son las fotos de `neonizador/TEXTURAS*`, Analog FX y PAPELATOR **vueltas a guardar** en JPG con otro nombre (md5 distinto, imagen igual) | hash perceptivo (248) + tamaño, color y contraste (18 papeles cuadriculados) |
| `elementos/*/originales`, `nuevos_originales` | 110 | **No**: son las fotos de fuego, goteos, pompas y moho que ya están | md5 / hash perceptivo |
| `elementos/` recortes | ~2.000 | **No como fuente**: son recortes de láminas que ya están (burbujas ← «Burbujas de jabón iridiscentes…», salpicaduras ← `imperfecciones/Gemini_…kz2v7u…`, gotas ← «Gotas de lluvia sobre cristal negro», goteos ← `GOTAS/`). **Sí como producto**: piezas sueltas más finas que las de TEXTURAS | búsqueda de la pieza dentro de la lámina (muestras) |
| `proyectos_after_effects/` | 2 `.aep` | Sí (no son texturas) | — |

**Conclusión:** la BIBLIOTECA de NEONIZADOR no aporta ni una foto nueva; aporta **otro procesado** de las mismas fotos.
No hay que fusionar fuentes, sino decidir qué productos suyos pasan a la biblioteca común.

### Productos de NEONIZADOR que TEXTURAS no tiene (candidatos)

| Producto | Cantidad | TEXTURAS hoy |
|---|---|---|
| Pavesas sueltas (atlas) | 267 | 11 láminas de chispas |
| Chispas sueltas, giradas a horizontal, con largo | 128 | idem |
| Llamas clasificadas (`lengua`, `masa`, `base`) con `lean` y `base_x` | 24 | 28 llamas sin medidas |
| Gotas de agua sueltas sobre cristal | 140 | solo como tileable de vidrio |
| Salpicaduras sueltas (café/óxido 150, tinta 100) | 250 | 8 láminas |
| Polvo y fibras sueltos | 160 | 7 láminas |
| Pompas sueltas (LA, alfa = luz) e islas de espuma | 6 + 10 + 36 | 18 |
| Tiles sin costura de espuma (10) y moho (4) | 14 | — |
| Goteos con medidas (`ax`, `sw`, `bw`, `len`, `wob`, `cont`, `crack`) | 279 | 219 goteos sin esas medidas |
| Trazos sueltos (tinta de brocha, garabatos, puntos, líneas…) | 640 | 287 |

Antes de adoptarlos: revisar calidad con hoja de contactos frente a lo nuestro, y unificar el método (alfa de fuego
`clip((max − 0,03)/0,72)^0,85` de NEONIZADOR frente a «unmultiply» de `tx.from_black`).

### Para que NEONIZADOR no cambie ni un bit

- Sus `.bin` salen de los JPG re-guardados de su BIBLIOTECA, no de los originales. Para reconstruir idéntico hay que
  conservar **esos 715 archivos (182 MB)** como fuentes heredadas (`originales/heredado/neonizador/…`) o aceptar el cambio.
- Tabla `nombre_en_plugin → id` (287 nombres): `neonizador/mapa_ids.json` (por hacer en la pasada unificada).
- Respetar el orden de las familias numeradas (`gt_`, `fg_`, `bf_`, `mo_`) y fijar las listas que hoy dependen del
  peso del archivo (`ELEMENTS`).
- Las dos fichas coinciden: 140 texturas usadas (143 si se cuentan las 3 `fg_base`, que se cargan pero no se pintan).
  147 empaquetadas sin uso (~90 MB): candidatas a salir del `.ccx`.

## PAPELATOR

- Sus 819 fotos fuente están todas en TEXTURAS (mismo md5; ruta = `papelator/<ruta>`). Nada nuevo que procesar.
- Necesita del índice: **originales intactos (md5)**, `ancho_real_mm` por foto, fondo, tileable, orden estable y los
  **duplicados que usa dos veces** (3 parejas en `imperfecciones/`).
- Trampas: `imperf.json` con ajustes a mano, `build_grids.py` no reproducible, `imperf_tune.py` no idempotente,
  `build_overlays.py` siembra el azar con la longitud del nombre del archivo (si se renombra, cambia la lluvia).
- Ofrece a la biblioteca común: método de alfa de croma `bordes_matte.matte`, escalas reales en mm (bordes, superficies,
  maderas, atlas de imperfecciones), sombreado de pliegues A4 y pendientes de vidrio.
- Le faltan: bordes quemados reales, cartón en planta, moho real (→ las colonias de NEONIZADOR), más orejas, pliegues
  7-8 y enrollados, perforadora/chincheta/cinta entera, papeles nuevos (calco, carbón, térmico, couché, seda, sobres),
  corcho, pizarra, lienzo, plástico mate, polvo de escáner.

## Trazo

- Sus 319 archivos de `TEXTURES/` (commit 83aed67) son idénticos (hash de git) a los que ya procesó TEXTURAS.
- Productos: 9 librerías de pinceladas enderezadas (`pin_*`, cabeza/cuerpo/cola + relieve), tiles de pintura y
  acuarela, 22 manchas con forma, 5 superposiciones 9:16, 19 tiras de grano de grafito, 3 soportes de papel/lienzo
  sintetizados por fase aleatoria (512², ~10 px/mm supuesto).
- Peso muerto (~3,7 MB): `pin_cera`, `pin_pastel`, `ov_carbon`, `ov_goteos` (sin verificar), `ov_grafito`.
- Pide del índice: medio, tipo, tileable, color/temperatura, `q` (1-3), tags de forma, `px_por_mm`, md5.
  Quiere recibir trazos sueltos limpios con máscara, tiles sin costura a resolución completa y fondos de papel limpios;
  el enderezado y la codificación TRZ1 los sigue haciendo él.
- Nombres: `pin_gouache` (para óleo) ≠ `pin_guache` (gouache). Evitar «trazos» como nombre de familia genérica.
- Le falta: papeles reales escaneados sin trazos con escala, más óleo (empaste, espátula), pastel real, grafito por
  durezas, bordes/floraciones/granulación de acuarela reales, más madera de grabado, tinta y rotulador limpios
  (las fuentes ya existen sin usar).
- Antes de migrar: comprobar que su build actual reproduce sus `.bin` (no está verificado).
