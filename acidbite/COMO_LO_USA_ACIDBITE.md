# Cómo aplica ACIDBITE sus archivos (visto en sus propios tutoriales y nombres de archivo)

Fuente: los vídeos tutoriales que vienen dentro de cada pack (revisados fotograma a fotograma; el audio no se ha
transcrito) y los nombres de los archivos, donde ACIDBITE escribe el modo de fusión entre paréntesis.
Lo que no sale de ahí está marcado como **(deducido)**.

## Regla general
- Todo son clips de vídeo normales (ProRes .mov). Se colocan en pistas por encima del metraje y se les cambia el
  **modo de fusión** en Opacidad. Cuando el nombre trae `(screen)`, `(Overlay)`, `(multiply)`, `(alpha)`,
  `(Pin Light)`, `(difference)`… ese es el modo que ACIDBITE indica.
- Los clips 4K se encajan al tamaño del proyecto con **Set to Frame Size / Scale to Frame Size**.
- Los packs de película están a **24 fps**.

## Pila de capas de "look película" (tutoriales 16mm y 35mm)
De abajo arriba:
1. Metraje (con LUT de película en Lumetri → Creative → Look → Browse, eligiendo el `.cube` del LOG de la cámara;
   si el metraje es Rec.709, el `FilmLUT_Rec709`).
2. **Grano** `(Overlay)` a pantalla completa. Para más presencia lo cambian a **Hard Light**; en 35mm además le
   suben el contraste (Brightness & Contrast, contraste +14).
3. **Gate / marco de película**: `(multiply)` = interior blanco y bordes negros; `(alpha)` = recortado, modo Normal.
   Con gates en alfa escalan el metraje hacia abajo para que quepa dentro de la ventanilla.
4. **Perforaciones** `(screen)` (fondo negro).
5. **Texturas** 35mm `(Pin Light)` sobre gris: manchas/pegamento; una `(Difference)`.
6. **Quemados (burns)** `(screen)`: se colocan **encima del corte** entre dos planos, con su SFX debajo en una pista
   de audio. ACIDBITE: cortar en el momento más brillante.

## Transiciones con máscara de luma (tutorial Burning Paper, Premiere)
Cada transición viene dos veces: el clip del fuego (`Burning Paper N.mov`) y su máscara
(`Burning Paper Luma Mattes/Burning Paper Luma Matte N.mov`).
- V1: plano que sale · V2: plano que entra, con **Track Matte Key** → Matte: la pista de la luma matte,
  Composite using **Matte Luma** (activar **Reverse** según el sentido) · V3: la Luma Matte (no se ve, hace de máscara)
  · V4: el fuego en **Screen** para que se vean las llamas.
- **Recolorean el fuego** con Lumetri → Curvas Hue vs Hue (lo pasan a rosa y a verde). → Útil para el neón.
- Hay tutoriales para Premiere, DaVinci Resolve, Final Cut y Vegas en el propio pack.

## Transiciones con máscara alfa (tutorial Cracked Glass, Premiere)
- Los clips son 3840×2160, 23,976 fps, **alfa recta (straight alpha)** y **llevan el sonido dentro** (estéreo 48 kHz).
- V1: plano que sale · V2: plano que entra con **Track Matte Key → Matte: V3, Composite Using: Matte Alpha** ·
  V3: el clip de cristal. Los trozos de cristal "cortan" el plano nuevo y lo van revelando.
- Gradúan los dos planos con Lumetri para que encajen de color.

## Transiciones de tira de película (tutorial Cine Snip, Premiere)
- Clips 4096×3072 (4:3), 24 fps, 18 fotogramas de media, **con sonido dentro**.
- Van en V2 encima del corte (centrados sobre él). Prueban **Normal, Screen y Difference** según el resultado que
  quieran: el modo es una decisión creativa, no fija.

## Cinemarkers 2 (tutorial)
- Marcos y manchas pintados a mano (negro sobre blanco y viceversa) colocados en V2 sobre el corte; se elige el
  modo de fusión en la lista (Multiply, Screen, etc.) según el clip.
- El audio del clip va pegado al vídeo.

## Analog Video Package (tutorial general + tutorial de proyectos Premiere)
- **Video Noise** `(Overlay)` a pantalla completa, toda la duración (59,94 fps): ruido de VHS/Video8/MiniDV.
- **Glitches** `(Screen)` (a veces `(Overlay)` o `(Multiply)` según el nombre) en pista superior, en momentos
  puntuales; bajan la opacidad (~40 %) y encadenan varios seguidos.
- **Viewfinder**: PNG sueltos (batería, SP, timecode, Lens Cap…) apilados en modo **Normal** para montar tu propio
  visor; o los visores animados `.mov` ya hechos (MiniDV/V8 Play/Rec).
- **Still Overlays**: `Mask 1,85 to 1,33` (PNG) arriba del todo en Normal para pasar a 4:3 con esquinas redondeadas;
  `Scanlines` y `Shadow Mask` encima del metraje.
- **Text and Leaders**: clips sueltos (TV Preroll, Warning, The End) en versión CLEAN y NOISY.
- **Premiere Projects** (Analog Video Look, Star Filter, Vertical Streaks): plantillas anidadas; se mete el metraje
  graduado en la secuencia «_graded footage goes here» y el resultado sale en «_FINAL RESULT». Solo Premiere.

## CRT Elements (tutorial general, Premiere)
- **Dirt** (rejilla RGB de pantalla CRT, gris) en **Overlay** sobre todo el plano.
- **Glitches** en **Screen** sobre el corte (como transición rápida).
- **Flares / Flashes** sobre negro en **Screen**; los recolorean con Lumetri (temperatura) para que tiren a naranja.
- **SFX Toolkit**: whooshes de vídeo analógico, lens flare, mecánica de VCR y ruido; se apilan varias capas de audio.
- **LUTs**: «Flat LUT» (normal, cold, warm) con un `.cube` por cámara/LOG + Utility LUTs; Lumetri → Creative → Look.

## Film Burns (tutorial, Premiere)
- Quemados `(Screen)` en V2 encima del corte, con su SFX debajo. Cuando el quemado enseña la perforación, lo
  **escalan y desplazan** para sacarla de cuadro (lo que ACIDBITE llama "lose the sprocket holes").
- `Filmgate S8 (Multiply)` en una pista superior durante todo el montaje para enmarcar.

## Cyber Transitions (tutorial, Premiere)
- 25 fps, sonido dentro del clip. Carpetas **Clean**, **Glitchy** y **Noise** (`CRT Noise`, `CRT Noise_dirty`).
- Se usan **como plano intercalado**: el clip de glitch (≈1 s) va **en la misma pista, entre los dos planos**
  (o encima del corte en Normal), tapando el cambio. No hace falta modo de fusión: es imagen completa.
- Los Noise van como capa de ruido CRT encima.

## Dissected Textures (tutorial, Premiere)
- 25 fps. El modo viene en el nombre: `(Difference)`, `(Screen)`, `(Multiply)`, `(Overlay)`.
- Se ponen **un instante encima del corte** (≈1 s, con su sonido) como golpe de textura; prueban Difference,
  Overlay y Hard Light: el modo cambia mucho el resultado (papel, óxido, cuero, metal).
- Carpeta **Alpha** (`Dissected Alpha Texture N`): formas recortadas; con **Track Matte Key → Matte Alpha** el
  plano se ve **solo dentro de la forma** de la textura (efecto collage/recorte).

## Animated Markers (tutorial, Premiere)
- **10 fps**: animación de rotulador a saltos (stop motion). Trazo blanco sobre transparente/negro.
- Se colorean con el efecto **Tint** (Map White To = el color que quieras: rojo, azul, verde…). → Encaja con neón.
- **Marcos** (`Frame 16:9`, `Square`) encima del plano, en Normal, para encuadrar a una persona; corazones,
  flechas, círculos, etc. se escalan, giran y colocan sobre el sujeto.
- **Letras** (mayúsculas y `_small`), **números** y **símbolos**: se montan en secuencias anidadas para escribir
  títulos a mano (el tutorial monta «ACIDBITE» letra a letra con símbolos alrededor) sobre un **Background**
  (garabatos de fondo).

## Cinemarkers (tutorial, Premiere)
- **Alpha Transitions**: manchas/agujeros que crecen; con Track Matte (alfa) el plano nuevo aparece dentro.
- **Overlays** (blobs, rayas, cintas, X, perforaciones, «ab»…): en V2 encima de los cortes, en **Normal**, unos
  pocos fotogramas, con su sonido; a veces gradúan el overlay con Lumetri para cambiarle el color.
- El tutorial tiene una parte dedicada a **modos de fusión**: el mismo overlay cambia mucho en Screen, Multiply,
  Difference, etc.

## Film Leaks (tutorial, Premiere)
- 24 fps. En V2 **encima del corte**, en **Normal** y escalados para sacar la perforación de cuadro; también
  prueban **Vivid Light**. Se combinan con un Cross Dissolve debajo.
- Usan el leak como **fondo de título**: texto «ACIDBITE» encima del leak con **Color Dodge** o **Difference**.

## Light Transitions (tutorial, Premiere)
- 3840×2160, 24 fps, sonido dentro. Carpetas **Graded** y **Ungraded**, cada una con Colored Lights, Lights, Pyro
  y Shapes (los mismos clips con y sin etalonar).
- En V2 **encima del corte** (unos 6–12 fotogramas): primero en Normal para ver dónde cae y luego en **Screen**.
  Pyro también lo prueban en **Difference**.
- **Recolorean la luz** con *Color Balance (HLS)* → Hue (p. ej. 210°) y bajan saturación: una luz verde pasa a
  roja/rosa. → Para el neón, cualquier luz se puede llevar al color del rótulo.

## Morpheus (tutorial After Effects)
- Son **MOGRT**: en After Effects se abren con File → Open y se **extraen a una carpeta** como proyecto AE.
- Dentro, cada transición es una composición con: `Noise_Precomp` (una de las 16 `Noise Textures` .jpg con escala
  animada), `Transition_0X`, un **ajuste de auto-desplazamiento** (`SelfDisplace_Adjustment`, efecto tipo
  datamosh) y dos huecos `Placeholder_01_UHD` / `Placeholder_02_UHD` donde van el plano que sale y el que entra.
- Versiones 16:9 y 9:16; también como plantillas de Final Cut (`.motr`) y su SFX (`Morpheus_sfx0X.wav`).
- Para Neonizador (panel de AE) es el ejemplo más directo: transición por **desplazamiento con una textura de ruido**.

## Pre-Built VHS Transitions (tutorial, Premiere)
- Se importa el `.prproj` entero. Cada transición es una carpeta con secuencias anidadas: `0X_first_shot`,
  `0X_second_shot` y `0X_FINAL_RESULT`, con el `0X_GLITCH/VHS_TRANSITION_screen.mov` encima en **Screen**
  (el modo va en el nombre: `_screen`, `_overlay`) y `Scanlines.png` / `Shadow Mask.png`.
- Se sustituyen los planos de first/second shot por los tuyos. 23,976 fps. También `.drt` (Resolve) y `.motr` (FCPX).

## DynamiXXX (tutorial, Premiere)
- 3840×2160, 24 fps, sonido dentro. Golpes de textura analógica (fibras, quemados, manchas) de menos de 1 s.
- En V2 **encima del corte** o de un momento a acentuar; prueban **Screen** y sobre todo **Difference**; apilan
  dos o tres seguidos para una ráfaga.

## Optical Elements (tutorial, Premiere)
- Carpetas **Subtle**, **Medium**, **Hard** y **Particles**, más **SFX** separados (Hard/Medium/Particle).
- Refracciones largas (≈3 s) en V2 **atravesando el corte**, en **Screen**; se recolorean con
  *Color Balance (HLS)* → Hue. Los Hard sirven como transición; los Subtle como textura ambiental.

## Super Mixed Media Pack (tutorial, Premiere)
- Proyecto 4K a 25 fps. Carpetas: **Frames**, **Toolbox** (Opener, Scratches, Textures) y **Transitions**
  (Alpha Transitions, Overlay Transitions).
- **Frames**: marcos de papel/collage con alfa y sonido dentro; encima del plano (anidado) en Normal.
- **Textures** (papel gris arrugado): encima en **Screen** + Brightness & Contrast para dosificar.
- **Openers** y **Scratches** (sobre negro): en Screen; los scratches son círculos/garabatos rayados a mano.
- **Overlay Transitions**: animaciones de collage a pantalla completa en **Normal** encima del corte.
- **Alpha Transitions**: el clip se usa **dos veces**: una copia visible en Normal arriba y otra como
  **Track Matte Key → Matte Alpha** del plano entrante, que aparece dentro del hueco del papel.

## Textile Transitions (tutorial Toolkit, Premiere)
- 24 fps. **Toolkit**: Textile Frames (marcos de tela con hueco, alfa), Transition Frames (dos telas que se cruzan),
  Texture Animations (Grunge sobre negro, Paper, Textile) y SFX aparte (`Transition Sound 1–5`).
- Grunge en Normal/Screen encima del corte; Textile textures en **Multiply**.
- Los **frames** se escalan/giran para enmarcar al sujeto; con **Track Matte Key → Matte Alpha** el plano
  entrante se ve dentro del hueco de la tela. Pre-builts para Premiere (`.prproj` + `.prfpset`), Resolve (`.drt`)
  y FCPX (`.motr`).

## Tunnel Transitions (tutorial, Premiere)
- Túneles a pantalla completa (cristal, luces) en tres variantes: `Tunnel_0X`, `_curve` y `_rotate`, más `Bonus`.
- Técnica **match cut**: se hace zoom (Scale animado) hacia un punto del plano (un ojo, un anillo) y el túnel entra en
  V2 en **Normal** justo ahí, como si se atravesara el objeto; al salir, aparece el plano siguiente.
- Al plano saliente le añaden **Transform** (escala/posición con desenfoque de movimiento) y **Lens Distortion**
  animado para que se "deforme" hacia el túnel; gradúan el túnel (temperatura/tinte) para igualarlo al metraje.

## Ultimate Paper Pack (tutorial, Premiere)
- Viene en tres carpetas: **4K**, **Pre-Builds** y **Mobile**. Dentro de Assets: Centered, Collage, Opener, Overlays,
  Rips, SFX, Textures y Toolkit (Ink, Marker, Tape, Textures).
- **Textures**: el modo va en el nombre (`Fold 1 (Multiply)`, `Crumble`, `Handmade Paper Blue (Multiply)`,
  `Linen Cover (Screen)`); encima del plano para que parezca impreso.
- **Rips** (rasgados con alfa): el clip se pone **dos veces** — una como **Track Matte Key → Matte Alpha** del
  plano entrante (que aparece dentro del rasgado) y otra visible en Normal para ver el borde del papel. Encima,
  **Openers** (sobre negro) y su SFX.
- **Pre-Builds**: secuencias «Paper Collages 4K/HD» y «Paper Overlays 4K/HD» con huecos anidados (`O1HD_1`, `_2`,
  `_3`…) donde se sustituyen los planos; collages de varias fotos en un solo encuadre.

## Viewfinders+ (tutorial, Premiere)
- Carpetas **16mm** (1.78 y Scope), **CRT** (Flat y Scope) y **PNG**. 25 fps (los CRT 23,976).
- **Ojo, el nombre engaña:** todos los `.mov` (16mm y CRT) llevan `(Multiply)` en el nombre, pero son líneas claras
  sobre negro y en el tutorial (min. 2:18 y 2:50) se ven sobre el metraje sumando luz, es decir, en **Screen**. En
  Multiply dejarían la imagen en negro. Los **PNG** del mismo pack sí son línea negra sobre blanco y van en **Multiply**.
  Van encima del plano toda su duración.

## Wipe & Light Transitions (tutorial, Premiere)
- 23,976 fps, sonido dentro. **WIPES** (barridos de cámara con desenfoque de movimiento) y **LIGHTS** (destellos/
  luces desenfocadas), ambos a pantalla completa.
- Se meten **entre los dos planos, en la misma pista** (como plano intercalado de pocos fotogramas) y se suavizan
  los bordes con **fundidos de opacidad**; luego se gradúan con Lumetri (curvas) para igualar el color.

## Punch Hole Transitions (tutorial, Premiere)
- **Key-Transitions** (25 fps): agujeros que se abren, sobre negro con el borde quemado. Se usan **dos copias**:
  una en **Screen** para ver el borde y otra como **Track Matte** del plano entrante (aparece dentro del agujero).
- **Overlays**: el modo va en el sufijo (`COLLAGE0X_alpha`, `MOVINGTEXTURE0X_alpha`, `BLACKWHITE_difference`,
  `FRAME_difference`, `RECTANGLE0X_difference`). **Toolkit**: PNG de máscara (`_maskinside`/`_maskout`) y TIFF.
- **Pre-builts Premiere** = presets `.prfpset` (Punchhole_Warp_01…08, con deformación Spherize/Lens Distortion). En la
  propia línea de tiempo ACIDBITE escribe la receta: *«nest it, freeze it, apply preset, nest again, apply
  trackmatte preset»*. Encima, un **Filmburn** y el **Warp SFX**. También `.drt` (Resolve) y `.motr` (FCPX).

## Super 8 Package (tutorial, Premiere)
- Igual que 16mm/35mm, con el modo escrito en la **carpeta y en el archivo**: `Grain (Overlay)`, `Film Gates
  (Multiply)`, `Film Burns (Screen)`, `Dirt` (`8mm Dirt (Multiply)`, `8mm Dust (Screen)`).
- Pila: metraje → grano en Overlay (todo el plano) → gate en Multiply → polvo/suciedad → quemado en Screen sobre el
  corte (escalado para sacar la perforación) → LUT `FilmLUT(-cooler/-warmer)_<cámara>` en Lumetri (Input LUT).

## Lo que esto implica para los plugins (deducido)
- El modo de fusión se lee del nombre; si no lo trae, se deduce del análisis (fondo negro → Screen/Add; gris medio
  → Overlay; fondo blanco → Multiply; con alfa → Normal).
- Las transiciones de luz/quemado se centran en el corte, con el pico de brillo sobre el corte, y el SFX alineado
  a ese pico.
- **Cinco maneras de colocar un clip** (todas vistas en los tutoriales):
  1. *Capa de look* toda la duración (grano Overlay, gate Multiply/alfa, ruido VHS, polvo, visor).
  2. *Encima del corte* unos fotogramas (quemados, luces, glitches, texturas Dissected/DynamiXXX): Screen, Difference…
  3. *Plano intercalado* en la misma pista entre los dos planos (Cyber, Wipes & Lights, túneles).
  4. *Máscara* (Track Matte alfa o luma) para que el plano entrante aparezca dentro de una forma (fuego, cristal,
     rasgado, agujero, tela), casi siempre con otra copia visible encima.
  5. *Plantilla* (MOGRT, `.prproj`, `.prfpset`, `.drt`, `.motr`) donde solo se sustituyen los planos.
- **Recolorear** luces y fuego (Hue vs Hue, Color Balance HLS, Tint) es parte del flujo normal → el neonizador puede
  llevar cualquier luz/quemado al color del neón.
- Muchos clips de transición traen el **SFX dentro del propio .mov**: no hay que buscar un .wav aparte.
- Las transiciones con luma o alfa matte necesitan tres pistas (saliente, entrante con mate, mate) + la capa visible en Screen.


## Lo que dicen sus propios proyectos de Premiere (leído de los `.prproj` y `.prfpset`)
Esto no es interpretación: son los ajustes exactos que ACIDBITE dejó guardados en sus plantillas.

- **Códigos de modo de fusión de Premiere** (para leer cualquier `.prproj`): 0 Normal, 4 Multiply, 9 Lighten, 10 Screen,
  11 Color Dodge, 12 Linear Dodge (Add), 13 Lighter Color, 15 Overlay, 16 Soft Light, 20 Pin Light, 23 Difference.
- **Pre-built VHS Transitions**: cada transición en **Screen** (la 04 en **Overlay**) encima de los dos planos, con
  `Shadow Mask.png` y `Scanlines.png` debajo de ella y **Wave Warp** en los planos (duplicados en V1 y V2). El plano 2
  entra a 0,17 / 0,13 / 0,25 / 0,5 / 0,5 / 0,79 / 0,79 / 0,79 / 0,79 s del inicio del clip (transiciones 01–09).
- **Textile Transitions**: el *Frame* va dos veces durante toda la transición: una copia sin modo justo debajo, usada
  como **Track Matte Key → Matte Alpha** del plano entrante, y otra visible encima en **Screen** (1, 4, 5, 6, 7),
  **Lighten** (2) o **Difference** (3, 8). **Reverse** activado en las transiciones 1, 3, 4 y 5; desactivado en 2, 6, 7
  y 8. El plano entrante empieza a la vez que el Frame. Al plano saliente le ponen Posterize + Wave Warp. Texturas de
  apoyo: Grunge en **Screen**, Textile Texture Animation en **Multiply** (la 5 en **Soft Light**), Paper en **Screen**.
- **Punch Hole Transitions**: el plano saliente se anida, se congela y se anida otra vez (lo escriben en la propia
  línea de tiempo: *NEST IT, FREEZE IT, APPLY PRESET, NEST AGAIN, APPLY TRACKMATTE PRESET*). El preset de Track Matte
  es **Matte Alpha sin Reverse**: la Key-Transition hace el agujero en el plano saliente y por él se ve el entrante.
  La copia visible de la Key va en **Screen**, **Linear Dodge**, **Color Dodge** o **Lighter Color**; los Filmburn en
  **Difference** con **Invert** y Spherize/Lens Distortion; `FRAME_difference` en **Difference**;
  `BLACKWHITE_difference` lo usan en **Multiply**.
- **Analog Video Look**: metraje tres veces (V1 Normal, V2 y V3 en **Linear Dodge**), capa de ajuste al **50 % en
  Color Dodge** con Gaussian Blur, otra con Wave Warp + Color Emboss (70 %) + Motion Blur + Lumetri, y encima la
  máscara `Mask 1,85 to 1,33 rounded.png` en Normal.

## Otras comprobaciones hechas sobre los archivos
- **Light Transitions** son destellos muy cortos: de 4 a 22 fotogramas (0,2–0,9 s). No es un error de descarga: las
  versiones Graded y Ungraded duran exactamente lo mismo.
- **Ultimate Paper Pack**: los sonidos `Collage.02.wav` y `Collage.03.wav` están cruzados: cada uno dura exactamente
  lo que el clip del otro número. El catálogo ya los empareja por duración.
- **Analog Video Package**: `VHS Glitch Short 5 (Screen)` es casi blanco y `Short 6 (Multiply)` casi negro: son
  golpes de destello o apagón de pocos fotogramas, ese es el efecto.
