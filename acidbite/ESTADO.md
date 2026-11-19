# AcidBite · estado del trabajo (19-11-2026)

Escrito por la conversación que analizó el pack **ACIDBITE Complete Collection** antes de unirlo con TEXTURAS.
Todo lo que sabe esa conversación está aquí y en las carpetas de al lado; no depende de su memoria.

| Carpeta | Qué hay |
|---|---|
| `ESTADO.md` | este documento: conclusiones, taxonomía, índice, scripts y decisiones |
| `COMO_LO_USA_ACIDBITE.md` | cómo aplica ACIDBITE cada pack, sacado de sus tutoriales y de sus proyectos de Premiere |
| `datos/catalogo.json` | el índice de AcidBite: 3.215 entradas, una por archivo (esquema en §4) |
| `datos/CATALOGO.md` | el mismo índice en tablas legibles, por categoría, estilo y pack, más las recetas exactas de ACIDBITE |
| `datos/estilos.json` | 5 estilos de montaje (`estilos`) y 29 recetas exactas leídas de sus `.prproj` (`recetas_acidbite`) |
| `datos/plantillas_acidbite.json` | las 29 secuencias de sus proyectos de Premiere: pista, tiempos, modo de fusión, efectos, rol (mate / visible) |
| `datos/presets_acidbite.json` | los parámetros de sus presets de Premiere (`.prfpset`): Track Matte Key (Matte Alpha, Reverse) y efectos |
| `datos/inventario.csv` | los 3.215 archivos tal como quedaron en el ordenador de Iker (id, categoría, pack, ruta, tipo, bytes) |
| `datos/analisis_medidas.tgz` | medidas en bruto: `probe/` (ffprobe), `stats/` (luma `_Y`, movimiento `_D` y alfa `_A` por fotograma), `audio/` (envolvente cada 10 ms) |
| `datos/prproj_xml.tgz` | los `.prproj` de ACIDBITE descomprimidos a XML (para volver a leerlos sin el ordenador de Iker) |
| `hojas/<id>.jpg` | hoja de 8 fotogramas por clip (alfa sobre gris); `<id>_all.jpg` = todos los fotogramas de los clips revisados a mano |
| `scripts/` | todo el código: organizar en el PC, analizar, catalogar, leer `.prproj` y presets |

> **Licencia:** material de pago. Los archivos del pack **no** están en ningún repo: solo el índice, las medidas y
> hojas de miniaturas pequeñas. Repo privado; nada de esto se redistribuye.

---

## 1. Dónde está el pack

- En el ordenador de Iker: `C:\Users\ikerg\Downloads\ADIDBITE\BIBLIOTECA\` (~190 GB descomprimidos; zips originales
  intactos al lado). Rutas del índice relativas a esa carpeta.
- Ahí mismo: `catalogo.json`, `CATALOGO.md`, `estilos.json`, `COMO_LO_USA_ACIDBITE.md`, `plantillas_acidbite.json`,
  `presets_acidbite.json` y `_ANALISIS\` (medidas, hojas y scripts). `_INVENTARIO.csv` y `_ESTADO.txt` en la raíz.
- Versión 4K de todo (Iker la eligió frente a «mobile»; el destino es vertical para móvil: se hace zoom/recorte).

## 2. Taxonomía (cómo quedó ordenado en disco)

`BIBLIOTECA\<categoría>\<pack>\…` con la estructura interna de cada pack intacta (Assets, Tutorial, plantillas):

| Categoría | Packs |
|---|---|
| `01_TRANSICIONES` | Burning Paper, Cine Snip, Cracked Glass, Cyber, Light Transitions, Pre-Built VHS, Punch Hole, Textile, Tunnel, Wipe and Light |
| `02_PELICULA` | 16mm, 35mm, Super 8, Film Burns, Film Leaks, Viewfinders Plus |
| `03_TEXTURAS_OVERLAYS` | Analog Video, CRT Elements, Dissected Textures, DynamiXXX, Optical Elements |
| `04_COLLAGE_MIXED_MEDIA` | Super Mixed Media Pack, Ultimate Paper Pack |
| `05_ANIMACIONES_ELEMENTOS` | Abstracts, Animated Markers, Cinemarkers, Cinemarkers 2, Liquids |
| `06_PLANTILLAS` | Morpheus (MOGRT de After Effects, `.motr` de Final Cut) |
| `07_SONIDO` | Dystopia SFX, Elements SFX, Urban SFX |

Totales: 1.821 vídeos, 671 sonidos, 286 imágenes, 220 LUT, 86 plantillas, 62 PDF, 48 tutoriales, 17 previews y
4 metrajes de demostración. 189,6 GB.

**Estilos** (para montaje automático; un pack puede tener varios): cortinillas de luz, collage, vintage/analógico,
cine/película, urbano, tecnológico, glitch, orgánico, fuego, grunge, fondos, impacto. Detalle en `datos/estilos.json`.

**Colocaciones** (las cinco maneras en que ACIDBITE aplica un asset, vistas en sus tutoriales):
1. `look`: capa durante todo el plano (grano, gate, rejilla CRT, viewfinder).
2. `encima_corte`: unos fotogramas encima del corte (quemados, luces, glitches, golpes de textura).
3. `intercalado`: plano entero entre los dos planos, en la misma pista (Cyber, Wipes & Lights).
4. `mascara`: Track Matte (alfa o luma) para que el plano entrante aparezca dentro de una forma, casi siempre con otra
   copia visible encima. Variante `recorte`: forma fija de collage (Dissected Alpha).
5. `plantilla`: MOGRT / `.prproj` / `.prfpset` / `.drt` / `.motr` donde solo se cambian los planos.
Más `elemento` (se escala y coloca sobre el sujeto: marcadores, flechas) y `fondo` (Abstracts, Liquids).

## 3. Formatos técnicos

- Vídeo: ProRes 4K `.mov`. **422 sin alfa; 4444 con alfa recta.** Muchos (969) llevan el **SFX estéreo 48 kHz dentro**.
- fps: película 24; Burning Paper fuego 48 y sus mattes 50; Animated Markers **10 fps** (2000×2000, alfa); Punch Hole
  Key 25; Viewfinders 25 (CRT 23,976); Wipe & Light 23,976; Cine Snip 4096×3072 (4:3).
- **Light Transitions duran 4–22 fotogramas** (0,2–0,9 s): es su diseño (Graded y Ungraded miden igual).
- LUT `.cube` de 33 o 65 puntos, uno por cámara/LOG (FilmLUT, cooler, warmer, Flat, Utility).
- El **modo de fusión** lo escribe ACIDBITE en el nombre: `(screen)`, `(Overlay)`, `(multiply)`, `(alpha)`,
  `(Pin Light)`, `(difference)`, en la carpeta (`Grain (Overlay)/`) o como sufijo (`_screen`, `_alpha`…).

## 4. El índice (`datos/catalogo.json`)

Lista de entradas. Campos:
- `id` (12 primeros hex del md5 de la ruta relativa en minúsculas: estable mientras no se mueva), `categoria`, `pack`,
  `ruta` (relativa a `BIBLIOTECA\`), `tipo` (`video`, `audio`, `imagen`, `lut`, `plantilla`, `doc`, `tutorial`,
  `preview`, `metraje_demo`), `ext`, `bytes`, `estilos`, `copia_de_plantilla` (copias dentro de carpetas de plantillas).
- `tecnico`: códec, perfil, pix_fmt, `alfa`, ancho, alto, fps, duración, fotogramas, `audio_incrustado`.
- `aspecto`, `color` (tono dominante, saturación), `medidas` (luma media/mediana/p95/máx, pico de brillo, movimiento,
  saltos, cobertura de alfa al inicio/fin/máx).
- `composicion` (modo de fusión), `composicion_fuente` (prioridad: **nombre del archivo > tutorial > plantilla de
  ACIDBITE > análisis**), `composicion_recomendada` cuando el nombre engaña (Viewfinders .mov), `modos_usados_por_acidbite`
  (de sus `.prproj`).
- `colocacion` + `colocacion_texto`, `uso`, `notas`.
- `transicion`: `tipo` (`encima_corte` / `mascara` / `recorte` / `intercalado`) y según el tipo:
  `corte_recomendado_s` + `criterio` + `efecto_desde/hasta_s` o `cubre_desde/hasta_s`; en máscaras `inicio_s`,
  `revelado_completo_s`, `invertir` (Reverse) e `invertir_fuente`; `corte_acidbite_s` si sale de su plantilla.
- `velocidad` (un fotograma / estático / lento / medio / rápido / muy rápido) y `retiming` (cómo jugar con ella).
- Sonido: `sfx` (id del .wav emparejado), `sfx_confianza`, `sfx_por_nombre` (si se corrigió), `sfx_acidbite`
  (de sus plantillas), `sfx_sugeridos` (familia del pack); en el audio: `categoria_sonido`, `envolvente`
  (pico, ataque, forma) y `clips`.
- `combinado_por_acidbite` (qué piezas pone juntas en sus plantillas), `uso_en_plantillas_acidbite`.
- LUT: `lut` (tipo, cámara de entrada, variante, tamaño). Plantillas: `programa`.
- `miniatura`: `sheets/<id>.jpg` (aquí, `hojas/<id>.jpg`).

## 5. Conclusiones (lo verificado)

**Cómo se aplica cada cosa** → `COMO_LO_USA_ACIDBITE.md`. Lo esencial:
- Luz, quemados, fugas, glitches: **Screen** encima del corte, cortando en el **fotograma más brillante** (si el
  blanco dura varios fotogramas, en el centro). Se recolorean (Hue/Color Balance HLS/Hue vs Hue/Tint): sirven a
  cualquier color de neón.
- Película: pila metraje+LUT → grano Overlay (Hard Light para más) → gate Multiply/alfa → perforación Screen → textura
  Pin Light → quemado Screen en el corte, todo a 24 fps.
- Máscaras: el plano entrante empieza a la vez que el clip; el saliente dura hasta `revelado_completo_s`.
  Textile: Matte Alpha con Reverse en 1, 3, 4 y 5 (no en 2, 6, 7, 8), leído de su preset. Punch Hole: el plano que
  sale se anida, se congela y lleva la máscara (Matte Alpha sin Reverse). Burning Paper: luma matte con Reverse.
- **Viewfinders**: los `.mov` se llaman `(Multiply)` pero van en **Screen** (comprobado en su tutorial); los PNG sí en Multiply.
- VHS pre-built: Screen (la 04 Overlay) + `Shadow Mask.png` + `Scanlines.png` + Wave Warp en los planos; corte del
  plano 2 a 0,17/0,13/0,25/0,5/0,5/0,79/0,79/0,79/0,79 s del inicio.
- Analog Video Look: metraje ×3 (Linear Dodge), ajuste 50 % Color Dodge + Gaussian Blur, Wave Warp + Color Emboss +
  Motion Blur, máscara 1,85→1,33.
- Códigos de modo de fusión en `.prproj`: 0 Normal, 4 Multiply, 9 Lighten, 10 Screen, 11 Color Dodge, 12 Linear Dodge,
  13 Lighter Color, 15 Overlay, 16 Soft Light, 20 Pin Light, 23 Difference.

**Puntos de corte** (`transicion`): calculados según el modo real (brillo en Screen/Add/Difference/Normal, oscuridad en
Multiply, cobertura de alfa en clips con alfa, movimiento si no hay pico). Revisados a mano 33 clips de todos los
criterios (hojas `hojas/*_all.jpg`). Quedan 72 «efecto uniforme» (no hay momento fuerte: vale cualquier punto).

**Velocidad**: movimiento medio por fotograma (diferencia) → estático < 1,5, lento < 6, medio < 15, rápido < 28,
muy rápido. Retiming: luz 50–200 % con fusión de fotogramas (el SFX no se estira, se alinea al pico); alfa/collage
70–150 % o conformar a 12/8 fps sin fusión; grano nunca acelerado.

## 6. Audio

- 969 clips con SFX dentro del `.mov`. 127 emparejados con un `.wav` por nombre y número; 96 confirmados por duración.
- **`Collage.02.wav` y `Collage.03.wav` (Ultimate Paper) están cruzados**: emparejados por duración.
- Textile: sonidos según sus plantillas (p. ej. Transition 3 Frame → Sounds 2, 4 y 5).
- CRT Elements, Morpheus y Punch Hole traen cajas de sonidos sin pareja: `sfx_sugeridos` por familia (lens flare
  para flares, analog whoosh para wipes/glitches/flashes, noise para dirt/texturas, Morpheus_sfx, WARP_SFX).
- Packs de sonido: Dystopia (Bonus, Glitch, Hits, Riser, Texture, Whooshes), Elements (Whooshes, Atmos, Footsteps),
  Urban (Atmos, Doors, Hits, Metal & Debris, Risers, Textures, Vehicles, Whooshes). Cada `.wav` tiene `categoria_sonido`
  y envolvente (pico, ataque) → la **sincronía**: alinear el pico del audio con el pico/corte del vídeo.

## 7. Mapas de desplazamiento

AcidBite **no trae mapas de desplazamiento como archivo**. La deformación la hacen efectos sobre los planos:
- Morpheus (AE): `Noise_Precomp` + `SelfDisplace_Adjustment` = desplazamiento por textura de ruido. Modelo directo
  para Neonizador vídeo.
- Wave Warp (VHS, Textile, Analog Look), Spherize y Lens Distortion (Punch Hole, Tunnel).
- Candidatos para **derivar** mapas: Liquids y Abstracts (fondos orgánicos en movimiento), Optical Elements
  (refracciones). Derivar = producto nuevo; no hecho todavía.

## 8. Scripts (`scripts/`)

| Script | Hace |
|---|---|
| `ORGANIZAR_ACIDBITE.bat` + `organizar_acidbite.ps1` | en Windows: descomprime (con `tar` de respaldo), coloca por categoría, inventario con id MD5, instala ffmpeg con winget si falta, mide cada clip (`signalstats`, `tblend`, `alphaextract`, hojas de 8 fotogramas, envolvente de audio) y empaqueta `_ANALISIS_parte*.zip` |
| `catalogar.py <ana> <salida>` | reglas de packs y tutoriales + medidas → `catalogo.json` (colocación, modo, puntos de corte, velocidad, SFX, plantillas y presets de ACIDBITE si están en `<salida>`) |
| `generar_md.py <salida>` | `CATALOGO.md` + `estilos.json` |
| `extraer_plantillas.py <xml> <json>` (usa `leer_prproj.py`) | lee los `.prproj` de ACIDBITE (gzip → XML): secuencias, pistas, tiempos, modos, efectos |
| `leer_presets.py <json> <prfpset…>` | lee presets de Premiere |
| `grids.sh` | rejillas de fotogramas con código de tiempo |

Volver a generar: `python3 catalogar.py ana salida && python3 generar_md.py salida` (con `ana` = `_ANALISIS` del PC).

## 9. Decisiones tomadas (y por qué)

1. **No se recomprime ni se renombra nada del pack**: la estructura de ACIDBITE se conserva dentro de cada pack (sus
   plantillas apuntan a rutas relativas).
2. **Nunca al repo público de NEONIZADOR**; solo índices. (Ahora: repo TEXTURAS privado, sin los archivos del pack.)
3. El modo de fusión manda en este orden: lo que dice ACIDBITE (nombre, tutorial, plantilla) > lo medido. Cuando se
   contradicen, se deja el de ACIDBITE y se añade `composicion_recomendada` con la prueba.
4. Ids por ruta (no por contenido) porque el pack no cambia y así se reconstruyen igual en cualquier PC.
5. 4K como fuente; el vertical se saca recortando (`aspecto`).

## 10. Lo que queda abierto

- Revisión a mano: 33 de 1.747 vídeos (una muestra de cada criterio). El resto, por reglas validadas con esa muestra.
- 72 clips «efecto uniforme».
- Recetas exactas solo de 4 packs (VHS, Textile, Punch Hole, Analog): los otros no traen `.prproj`.
- Mapas de desplazamiento derivados y versiones verticales/proxy: sin hacer.
