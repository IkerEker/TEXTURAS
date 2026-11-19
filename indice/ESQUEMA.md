# indice/indice.json · esquema

`{version, raiz, total, por_coleccion, por_clase, assets[]}`. Un asset por archivo. Rutas `archivo` relativas a
`Biblioteca/` (= `TEXTURAS_ROOT`). Campos (solo aparecen si tienen valor):

| Campo | Qué es |
|---|---|
| `id` | `tx:` TEXTURAS (procesado y productos) · `ab:` AcidBite · `or:<md5>` original de plugin |
| `coleccion` | `TEXTURAS`, `ACIDBITE`, `originales` |
| `archivo` | ruta dentro de `Biblioteca/` |
| `tipo` | imagen, video, audio, lut, plantilla, tutorial |
| `clase`, `sub` | taxonomía común por contenido (TEXTURAS ampliada: video/transiciones/…, pelicula/…, sonido, lut, desplazamiento, mascaras, productos) |
| `pack`, `estilos`, `colocacion` | AcidBite: pack, estilos de montaje, colocación (look, encima_corte, intercalado, mascara, elemento, fondo) |
| `desc`, `familia`, `color`, `color_medio`, `aspecto` | descripción |
| `md5` / `md5_bytes` | md5 del archivo / de los píxeles crudos (productos) |
| `w`, `h`, `alfa`, `fondo`, `bytes` | técnico |
| `tileable`, `costura`, `aviso` | repetible y calidad de la costura (≤ 1 invisible) |
| `tile_mm`, `mm_por_px`, `px_por_mm`, `ancho_real_mm`, `tamano_real_mm` | escala real |
| `modo` | clave común: normal, multiplicar, trama, superponer, luz_suave, luz_fuerte, luz_focal, diferencia, sobreexponer_lineal, sobreexponer_color, aclarar, color_mas_claro, mascara_alfa, mascara_luma |
| `modo_texto`, `modo_fuente`, `modos_acidbite` | el texto original, quién lo dice (autor > tutorial > plantilla > plugin > medido) y los modos que ACIDBITE usa en sus proyectos |
| `desplazamiento` | si sirve como mapa y su convención (gris 128 = neutro, gradiente, ruido) |
| `orientacion` | p. ej. goteos «raíz arriba» |
| `medidas` | medidas de pieza (llamas `lean`, `base_x`; goteos `ax`, `sw`, `bw`, `len`, `wob`, `cont`, `crack`; pavesas/chispas `len`, `ang`, `elong`) |
| `origen`, `origen_ruta`, `metodo` | original del que sale (`or:`), ruta en el repo, método de procesado |
| `rutas_antiguas`, `productos` | (originales) todas sus rutas en los repos de plugins y los `tx:` que salen de él |
| `usado_por` | qué plugin lo usa (detalle exacto en `plugins/<p>/uso_id.json`) |
| `video` | `fps, fps_efectivo, a_saltos, duracion, fotogramas, alfa, fondo, loop, version_loop, velocidad, retiming, comportamiento, codec` |
| `transicion` | `tipo` (encima_corte, mascara, recorte, intercalado), `corte_s`, `cubre_s` [desde, hasta], `efecto_s`, `revelado_s`, `invertir`, `criterio`, `fuente`, `nota` |
| `audio` | `incrustado`, `sfx` [ids], `sfx_acidbite`, `sfx_familia`, `confianza`; en sonidos: `duracion`, `envolvente`, `clips` |
| `conjuntos` | piezas que ACIDBITE pone juntas en sus plantillas |
| `lut`, `programa` | LUT (cámara, variante, tamaño) / programa de la plantilla |
| `licencia` | propio · Gumroad (no redistribuir) · ACIDBITE (pago, no redistribuir) |
| `hoja`, `tira` | hoja de contactos / tira de fotogramas para mirarlo |

Otros archivos: `nombres.json` (nombres oficiales y alias), `cruce_acidbite.md`, `cruce_phash_acidbite.json`.
Regenerar: `python3 tools/atlas/originales.py && python3 tools/atlas/construir_indice.py && python3 tools/atlas/tablas_plugins.py`.
