# DECISIONES · cómo se unen TEXTURAS y AcidBite en un único atlas

19-11-2026. Una fila por punto de diseño: lo que proponía TEXTURAS (`TRASPASO.md` §5), lo que concluyó AcidBite
(`acidbite/ESTADO.md`), lo que se decide y por qué. Criterio para desempatar: **lo que mejor sirve a los plugins**,
que son quienes consumen, sin que ninguno cambie su resultado sin que Iker lo sepa.

Reglas fijas que ninguna decisión toca:
- Los plugins funcionan 100 % solos, sin Claude ni internet. La biblioteca **solo se usa al construir**.
- Repos privados. El material de pago (AcidBite, Gumroad) **no se redistribuye** y sus archivos no entran en git.
- Ninguna textura se da por buena sin mirarla (hoja de contactos).
- Cada plugin conserva su prueba exacta (ficha §6) y la pasa antes de dejar sus fuentes.

---

## 1. Dónde viven los archivos

| | |
|---|---|
| **TEXTURAS proponía** | `Biblioteca/` local idéntica en los 2–3 ordenadores (`TEXTURAS/`, `ACIDBITE/`, `originales/`, `generadas/`), sincronizada por disco/NAS/rsync, nunca en GitHub. |
| **AcidBite tenía** | El pack en `Downloads\ADIDBITE\BIBLIOTECA\` (190 GB), ordenado por categoría y pack, con su índice al lado. |
| **Se decide** | La `Biblioteca/` de TEXTURAS, con AcidBite dentro tal cual: `Biblioteca/ACIDBITE/<categoría>/<pack>/…` = lo que hoy es `ADIDBITE\BIBLIOTECA\` (se mueve la carpeta entera, sin renombrar nada dentro). `Biblioteca/TEXTURAS/` = clon de este repo. `Biblioteca/originales/` = fuentes intactas de los plugins (§4). `Biblioteca/generadas/` = lo que se cree en el futuro, incluidos derivados de AcidBite. |
| **Por qué** | Una sola raíz → una sola variable (`TEXTURAS_ROOT` = la carpeta `Biblioteca`) para todos los plugins. AcidBite no se reordena porque sus plantillas (`.prproj`, `.drt`, `.motr`) usan rutas relativas dentro de cada pack y porque así se reconstruye igual en cualquier PC. |

## 2. Taxonomía y carpetas

| | |
|---|---|
| **TEXTURAS** | Carpetas por **contenido** (`tileables/papel`, `trazos/carbon`, `luz_y_elementos/fuego`…), un archivo procesado por ficha. |
| **AcidBite** | Carpetas por **uso de montaje** (`01_TRANSICIONES`… `07_SONIDO`) y por pack; vídeo 4K sin procesar. |
| **Se decide** | **No se mueve nada físicamente** entre las dos: las carpetas siguen siendo las suyas. La taxonomía común vive en el **índice**: cada asset lleva `clase` y `sub` por contenido (la de TEXTURAS, ampliada con las clases que trae AcidBite: `transiciones_luz`, `pelicula`, `glitch`, `collage`, `marcadores`, `sonido`, `lut`, `plantilla`) y además `coleccion`, `pack` y `colocacion`. |
| **Por qué** | Los plugins buscan por contenido («un papel», «una llama»); los montajes buscan por uso («algo para encima del corte»). El índice da las dos entradas sin duplicar 190 GB ni romper rutas. |

## 3. Identificadores

| | |
|---|---|
| **TEXTURAS** | `id` = ruta sin extensión (`tileables/papel/papel_blanco_0995`), estable entre regeneraciones (`nnnn` = nº de fuente). |
| **AcidBite** | `id` = 12 hex del md5 de la ruta relativa. |
| **Se decide** | Id común con prefijo de colección: `tx:<id TEXTURAS>`, `ab:<id AcidBite>`, `or:<md5>` para originales de plugins, `gen:<…>` para generadas. Cada asset lleva además `md5` del archivo. Los plugins citan **originales por `or:<md5>`** (identidad = contenido: no cambia aunque se mueva o se renombre) y productos por `tx:`/`ab:`. |
| **Por qué** | Las fichas piden «id estable» y «los mismos píxeles»: el md5 garantiza las dos cosas a la vez para las fuentes. Los ids de TEXTURAS y AcidBite ya existen y se citan en documentos: se conservan con prefijo para no chocar. |

## 4. Originales de los plugins

| | |
|---|---|
| **TEXTURAS** | Crear `originales/`: deduplicados por md5, intactos, con su ruta antigua. Para NEONIZADOR, además, `originales/heredado/neonizador/` con sus JPG re-guardados, «o aceptar el cambio». |
| **Se decide** | `originales/<repo>/<ruta original>` para la primera copia de cada md5 (se conserva el **nombre**: `build_overlays.py` de PAPELATOR siembra el azar con la longitud del nombre). La tabla `originales/MANIFIESTO.json` da, por md5, todas las rutas antiguas (duplicados incluidos). NEONIZADOR: **se conservan los heredados** (`originales/heredado/neonizador/BIBLIOTECA/…`, solo los que alimentan su `plugin/tex`). |
| **Por qué** | Es la única forma de que A mano, Analog FX, PAPELATOR, Trazo y NEONIZADOR reconstruyan **bit a bit** (sus fichas §5 lo exigen). Los heredados ocupan poco y evitan un cambio de resultado que Iker no ha pedido; si algún día se quiere pasar NEONIZADOR a los originales buenos, será un cambio decidido y medido con su prueba. |

## 5. Esquema del índice

| | |
|---|---|
| **TEXTURAS** | §5.2: id, md5, w/h, categoría/subtipo, fondo, tileable, `ancho_real_mm`/`px_por_mm`, medio, temperatura, `q`, tags de forma, orientación, modo, origen, duplicados, `usado_por`; vídeo: fps, transición, loop, audio. |
| **AcidBite** | `tecnico`, `medidas`, `composicion` (+ fuente), `colocacion`, `transicion` estructurada (tipo, corte, cubre, revelado, invertir), `velocidad`/`retiming`, `sfx`, `combinado_por_acidbite`, `estilos`, `lut`. |
| **Se decide** | La **unión** de los dos, con nombres comunes (lista completa en `indice/ESQUEMA.md`). Lo de vídeo se unifica así: `video{fps, fps_efectivo, duracion, fotogramas, alfa, fondo, loop, velocidad, retiming}`, `transicion{tipo, corte_s, cubre_s, revelado_s, invertir, criterio, fuente}`, `audio{incrustado, sfx[], pico_s}`. El `modo` común guarda **el valor y su fuente** (`modo_fuente`: autor del pack > tutorial > plantilla > plugin > medido). |
| **Por qué** | Los campos de TEXTURAS son los que piden los plugins para construir; los de AcidBite son los que hacen falta para montar vídeo. Ninguno sobra. La fuente del modo evita repetir el error de Viewfinders (el nombre decía Multiply y ACIDBITE lo usa en Screen). |

## 6. Vídeo

| | |
|---|---|
| **TEXTURAS** | 57 vídeos procesados (copias sin recomprimir, `_loop` que enlazan, tiras de fotogramas); `transicion` como texto («cuándo cubre y descubre»), `comportamiento`, `fps_efectivo`. |
| **AcidBite** | 1.821 vídeos sin tocar; puntos de corte numéricos según el modo, máscaras con Reverse leído de sus presets, colocación de sus tutoriales. |
| **Se decide** | Los dos métodos se conservan; el índice expresa los dos con el bloque `transicion` común. Las transiciones de tinta de TEXTURAS pasan a `tipo: mascara` (mate de luma) con `cubre_s`/`revelado_s` sacados de sus medidas. Los `_loop` de TEXTURAS se mantienen (AcidBite no tiene bucles). |
| **Por qué** | Mismo lenguaje para el montaje automático (Neonizador vídeo y futuros plugins de montaje) sea cual sea la colección. |

## 7. Audio

| | |
|---|---|
| **TEXTURAS** | Sin audio (los vídeos se copiaron sin audio). |
| **AcidBite** | 671 `.wav` con categoría y envolvente; 969 vídeos con SFX dentro; emparejado clip ↔ sonido con nivel de confianza. |
| **Se decide** | Se adopta el modelo de AcidBite: `audio.sfx` (ids), `audio.pico_s` y la regla de sincronía «el pico del sonido sobre el corte/pico del vídeo». Clase `sonido` en la taxonomía. |
| **Por qué** | Es el único material con audio; ningún plugin de Photoshop lo usa hoy, pero el montaje sí. |

## 8. Mapas de desplazamiento

| | |
|---|---|
| **TEXTURAS** | Relieves y pliegues en gris (50 % = neutro); vidrios cuyo gradiente usa NEONIZADOR como desplazamiento. |
| **AcidBite** | No trae mapas; desplaza con efectos (Morpheus `SelfDisplace` con sus 16 `Noise Textures`, Wave Warp, Spherize, Lens Distortion). |
| **Se decide** | Campo `desplazamiento` en el índice para lo que sirve como mapa: relieves, pliegues, vidrios, `Noise_01-16` de Morpheus, papeles plegados/arrugados de Ultimate Paper. Convención común: **gris 8 bits, 128 = sin desplazamiento**. Los mapas derivados (pendientes de vidrio de PAPELATOR, normales) quedan como producto común pendiente. |
| **Por qué** | Es la convención que ya usan TEXTURAS, PAPELATOR y A mano (grumos); así cualquier plugin puede usar cualquier mapa. |

## 9. Capas del atlas

| | |
|---|---|
| **TEXTURAS** | `MAPA.md` (puerta de entrada), fichas por asset, `tecnicas/` (recetas), `conjuntos`, una tabla `uso → id` por plugin. |
| **AcidBite** | Catálogo legible por estilo y pack, estilos de montaje, recetas exactas de sus proyectos, colocaciones. |
| **Se decide** | `MAPA.md` en la raíz → `indice/indice.json` (fichas) → `tecnicas/` (una receta por técnica: las de los plugins y las de ACIDBITE) → `conjuntos` dentro del índice (piezas que van juntas: plantillas ACIDBITE, parejas fuego/mate, duplicados que un plugin usa dos veces) → `plugins/<plugin>/uso_id.json`. Los estilos de montaje de AcidBite pasan a `tecnicas/montaje_*.md`. |

## 10. Procesado y GPU

| | |
|---|---|
| **TEXTURAS** | Todo lo pesado debe poder ir por GPU (Iker tiene 2). La sandbox no tiene GPU. |
| **AcidBite** | Análisis con ffmpeg en el PC de Iker (CPU). |
| **Se decide** | Lo que **alimenta a un plugin** se procesa siempre en **CPU y de forma determinista** (numpy/Pillow con versiones fijadas): es lo único que permite comprobar bit a bit. La GPU queda para lo pesado que no entra en ninguna prueba exacta: proxies y versiones verticales de AcidBite (decodificación/codificación NVDEC/NVENC), extracción de fotogramas y análisis. Los scripts aceptan `--gpu` cuando ffmpeg tenga CUDA. |
| **Por qué** | Dos GPU distintas no dan los mismos bytes en flotante (lo avisa la ficha de NEONIZADOR vídeo). |

## 11. Productos comunes (formato)

| Producto | Formato decidido | De dónde sale |
|---|---|---|
| Cintas de trazo enderezadas | PNG gris 8 bits, filas a lo largo (fila 0 = inicio de la mano) + JSON `{familia, mh, ar, origen or:md5, orden}`; exactamente las 88 de A mano | `a-mano/js/texdata.js` (A mano las publica) |
| Sellos de relieve | PNG gris 8 bits, 128 = neutro, luz desde arriba, borde a 0 + JSON clase/lado | `a-mano/js/grumosdata.js` (50 sellos) |
| Piezas sueltas finas | PNG RGBA sin premultiplicar + JSON con sus medidas en px del recorte (`lean`, `base_x`, ángulo, largo, `ax`, `sw`, `bw`, `len`, `wob`, `cont`, `crack`) | `neonizador` rama `biblioteca-texturas`, `BIBLIOTECA/elementos/` (revisadas con hoja) |
| Papeles tileables gris 128 | PNG gris 8 bits, 128 = neutro (detalle de alta frecuencia), con `tile_mm` | `tx:tileables/papel/*` con escala conocida |
| Alfa de croma | método `bordes_matte.matte` de PAPELATOR, copiado a `tools/` | `papelator/tools/bordes_matte.py` |
| Cinta adhesiva, tinta, rotulador, papel plegado (nuevo, de AcidBite) | se usan tal cual (PNG RGBA de Ultimate Paper) desde `ab:` | Ultimate Paper Pack `Toolkit/` |

**Por qué:** son los formatos que los propios plugins pidieron en su ficha §5; quien produce hoy cada cosa la sigue produciendo igual, pero una sola vez y para todos.

## 12. Nombres

| | |
|---|---|
| **TEXTURAS** | Tabla oficial por contenido (`boli`→`boligrafo`, `rotu`→`rotulador`, `guache`→`gouache`, `pincelfino`→`pincel_fino`; `sello_seco` / `sello_tinta` / `sello_brocha`; `kraft` ≠ `carton_kraft`; `cera` técnica ≠ `cera` de vela). Cada plugin conserva sus nombres internos con una tabla `id_común → nombre_plugin`. |
| **AcidBite** | Nombres de ACIDBITE intactos (sus plantillas los usan). |
| **Se decide** | `indice/nombres.json`: nombre oficial ← alias (de plugins y de AcidBite en inglés: `scotch tape` → `cinta_adhesiva`, `burn` → `quemado_pelicula`, `light leak` → `fuga_de_luz`, `grain` → `grano_pelicula`, `gate` → `ventanilla`, `sprocket` → `perforacion`…). Los archivos no se renombran. |

## 13. Lo que AcidBite aporta a los huecos de las fichas

Cruce hecho (`indice/cruce_acidbite.md`): por hash perceptivo **no hay ningún asset de AcidBite repetido en
TEXTURAS** (los 14 parecidos más cercanos, revisados a ojo, son falsos: superficies casi lisas). Cubre estos huecos:

| Hueco (TRASPASO §4) | AcidBite | Grado |
|---|---|---|
| Cinta adhesiva entera | Ultimate Paper `Toolkit/Tape` (34: celo arrugado, cinta americana, de pintor, de color) | **Cubierto** |
| Pliegues / hoja arrugada | Ultimate Paper `Toolkit/Textures` (Fold 1–5, Crumble 1–2) en Multiply | Parcial (hoja entera 4K, sin contar pliegues) |
| Rotulador y pincel limpios | Ultimate Paper `Toolkit/Marker` (40) e `Ink` (31), PNG con alfa; Animated Markers (308, animados) | Parcial (trazos de anotación, no cintas largas) |
| Máscara de fósforo, nieve analógica | `Shadow Mask.png`, `Scanlines.png`; CRT Elements `Dirt`; Morpheus `Noise_01-16` | **Cubierto** |
| Rayas de tracking VHS en vídeo | Analog Video, Pre-Built VHS, Cyber | **Cubierto** |
| Polvo y rayas de película | 16mm/35mm/Super 8: grano, dirt, dust, gates | **Cubierto** (vídeo) |
| Vídeos de fuego sobre negro con alfa | Burning Paper (fuego 4K con alfa recta) | Parcial (fuego de papel, sin humo) |
| Bordes quemados reales | Burning Paper (fotogramas del avance del fuego + luma mattes) | Parcial: hay que extraer fotogramas |
| Mapas de desplazamiento | Morpheus `Noise_01-16` | Parcial |
| Arañazos sobre tinta / grunge | Dissected Textures, DynamiXXX | Parcial (vídeo) |
| Lienzo / tela | Textile Transitions (texturas textiles, `Textille Texture.png`) | Parcial |
| Gotas en cristal, cáusticas en vídeo | Optical Elements (refracciones), Liquids | Parcial |
| Perforadora | Punch Hole `Toolkit` (agujeros con máscara dentro/fuera) | Parcial (agujero de película, redondo) |
| Moho, tiza/pastel, grafito por durezas, spray real, sello de goma, rodillo, fibras, tóner, neón, térmico, papeles nuevos, corcho, pizarra | — | **Sigue faltando** |

## 14. Lo que decide Iker (preguntas abiertas)

1. **Dónde va `Biblioteca/`** en cada ordenador y cómo se sincroniza entre los 2–3 (disco externo, NAS o rsync).
   Hasta que lo diga, los scripts piden la ruta con `TEXTURAS_ROOT`.
2. **Fusionar la rama `atlas` en `main`** de TEXTURAS cuando lo haya revisado.
3. **Analog FX**: ¿adopta los tileables nuevos (resultado algo distinto) o sigue con los originales (idéntico)? Por
   defecto, idéntico.
