# TEXTURAS · CARTELATOR

Ficha para la conversación que unifica las texturas de los plugins en la biblioteca común (repo `TEXTURAS`).
Fecha: 19-11-2026. Análisis hecho leyendo el código y ejecutando sus pruebas, **sin cambiar nada del plugin**.

> **Resumen:** Cartelator **no usa ninguna textura**. No lee imágenes al ejecutarse, no incrusta imágenes al
> construirse y no tiene fotos fuente. Todo lo que dibuja es geometría vectorial convertida a píxeles con colores
> planos. Las únicas imágenes que lleva son **22 iconos de interfaz** (4 del plugin y 18 de los botones de
> «Formas básicas»). Pasar a la biblioteca común **no le obliga a cambiar nada**. Más abajo están los materiales
> que podría aprovechar en el futuro (sus referencias tienen papel rasgado, grabado y brocha), marcados como ideas.

---

## 1. Identidad

| Campo | Valor |
|---|---|
| Nombre | **Cartelator** (id `com.cartelator.handlettering`, manifest v5) |
| Versión | **3.7.1** (`src/manifest.json`; se ve en el título del panel) |
| Photoshop | UXP, `minVersion` 25.0.0 (Photoshop 2024 o posterior) |
| Repositorio | **Ninguno.** No está en GitHub: la cuenta `IkerEker` tiene PAPELATOR, analog-fx-plugin, a-mano, NEONIZADOR, TEXTURAS, trazo y ESTILO, pero no Cartelator. El proyecto vive en el espacio de trabajo de esta conversación (`/home/claude/proyectos/cartelator`) y como copia en `Cartelator_proyecto.zip`, entregado el 5-11-2026. |
| Rama / commit | **No hay** (la carpeta no es un repositorio git). |
| Huella de la versión | `main.js` empaquetado: sha256 `4cdf9021700cddf71d00625dc2e93cf94586160eab1b995b3fbaac697edc181d` (276.057 bytes; `tools/build.py` lo reproduce idéntico). `.ccx`: sha256 `75836f395f8e1d3e009262127994c253f7670f65cc954bacfaf08ea465d72c3a` (cambia en cada empaquetado por las fechas del zip; usar la de `main.js`). |
| Estado | **Solo probado en un Photoshop simulado**, nunca en Photoshop real. |

**Qué hace.** Encaja un texto dentro de una **forma vectorial cerrada** como en un cartel tipográfico. El usuario
dibuja o elige una forma (rectángulo, elipse, polígono, pluma o una de las 18 «Formas básicas»), escribe el texto,
marca palabras como **destacada** (B), **protagonista** (B+U) o **pequeña** (i) y pulsa «Generar». El plugin mide
las letras reales de la fuente elegida, reparte el texto en líneas y lo deforma hasta llenar la forma. Lo deja como
**una capa de píxeles** `Cartel · <primeras palabras> #<id>.<versión>`. Con la forma de 4 esquinas sigue su
perspectiva; en bandas curvas se curva; en formas con codos (L, T, U…) recorre sus zonas. «Generar» con la misma
forma o el mismo bloque lo rehace; Ctrl+Z vuelve atrás de una vez.

**Estilos** (`js/build.js → STYLES`):

| id | Nombre en el panel | Qué hace |
|---|---|---|
| `recta` | Recta | Líneas rectas, letras sin deformar, cada línea lo más grande que cabe |
| `bloque` | Bloque | Todas las líneas igual de altas, estiradas de lado a lado (tipo JUST DO IT) |
| `deformada` | Deformada orgánica | Las letras se curvan con la forma, con una deformación suave por línea |
| `deformada_recta` | Deformada recta | Cada letra se estira hasta el borde y sus vecinas; puntas rectas que pueden inclinarse |
| `organica` | Orgánica | Letras montadas, separadas por un hueco **transparente**, que llenan la forma (tipo «this is not new») |
| `loca` | Loca | Letras de tamaños distintos encajadas como un puzle (tipo TYPOGRAPHY), sin girarlas |

Opciones: mayúsculas/minúsculas (como lo escribo, MAYÚS., minús., Título), 1–3 colores (en Orgánica, uno por
línea), otra tipografía para los destacados, partir palabras largas, «Seguir la curva de la forma (cinta)»
(solo en Deformada orgánica), margen, interlineado, alineación, orientación, perspectiva o rellenar.
«Otra distribución» enseña otro reparto. **No hay presets ni modos de textura.**

---

## 2. Estructura

```
cartelator/
├── js/                 código (17 módulos, 5.410 líneas; tools/build.py los une en un solo main.js)
│   ├── main.js         panel, bloques y versiones, «Generar», historia
│   ├── ps.js           puente con Photoshop: forma, medir letras, capa de píxeles por franjas, capas de forma
│   ├── render.js       lienzo RGBA, rasterizado con antialias, huecos/contornos (transformada de distancia)
│   ├── build.js        estilos, marcos, deformaciones, prepareItems (qué se dibuja)
│   ├── columnfill.js   motor de Orgánica y Deformada recta
│   ├── layout.js, region.js, frames.js, geom.js, shape.js, raster.js   maquetación y geometría
│   ├── glyphs.js, textmodel.js, markup.js   palabras, estilos y medidas de las letras
│   ├── loca.js         estilo Loca      shapelib.js   18 formas básicas (vectores)      diag.js   rastro de errores
├── src/                index.html, styles.css, manifest.json, LEEME.txt
├── icons/              plugin.png, plugin@2x.png, panel.png, panel@2x.png
│   └── formas/         18 iconos PNG de los botones de «Formas básicas»
├── tools/build.py      empaqueta el .ccx (única herramienta)
├── tests/              pruebas (Node): motor de texto falso, Photoshop simulado, hojas de resultados
├── referencias/        13 carteles de referencia del usuario (no se usan en el código)
├── dist/               plugin/ (lo empaquetado) y Cartelator_v3.7.1.ccx
├── estado_actual.png   hoja de resultados de pruebas (no se usa)
├── CONTEXTO_CARTELATOR.md, README.md
```

- **No hay** carpetas de fuentes de textura, assets generados ni datos incrustados (ni `.bin`, ni base64, ni
  módulos `*data.js`).
- **Lenguajes:** JavaScript sin dependencias en el plugin (solo las API del anfitrión: `require('photoshop')` →
  `app, core, action, imaging, constants`; `require('uxp')` → `storage`, `entrypoints`). Python 3 con la
  biblioteca estándar para empaquetar.
- **Pruebas:** Node 22 (`v22.23.4`), Playwright 1.63 con Chromium para el panel real con Photoshop simulado,
  Pillow 12.3 para las hojas de imágenes. Las letras de las pruebas salen de fuentes del sistema (sección 3.4).
- **Construcción:** `python3 tools/build.py`:
  1. Une los módulos de `MODS` en `dist/plugin/main.js`, con un `require` interno.
  2. Copia `src/` (index.html, styles.css, manifest.json, LEEME.txt) y toda la carpeta `icons/`.
  3. Comprime todo en `dist/Cartelator_v<versión>.ccx`, un zip con DEFLATE.
- **Pesos:**
  - `.ccx`: **130.686 bytes** (335.010 sin comprimir; `main.js` ocupa 276.057, o 86.135 comprimido).
  - Iconos: 32,6 KB en total.
  - **Fuentes de textura: 0 bytes.**
  - `referencias/`: 7,4 MB, fuera del .ccx.

---

## 3. Cómo usa las texturas

### 3.1 Al ejecutarse

**No lee ninguna textura.** Los únicos accesos a archivos o imágenes en tiempo de ejecución son:

| Qué | Dónde | API | ¿Textura? |
|---|---|---|---|
| Iconos del plugin y del panel | `manifest.json` → `icons`, `entrypoints[0].icons` | los carga Photoshop | No: interfaz |
| Iconos de «Formas básicas» | `js/main.js → renderShapes()` crea `<img src="icons/formas/<id>.png">` (id en minúsculas) | DOM del panel (ruta relativa al plugin) | No: interfaz |
| Rastro de diagnóstico | `js/diag.js` lee y escribe `rastro.txt` en la carpeta de datos | `uxp.storage.localFileSystem.getDataFolder()` | No: texto |
| Ajustes, bloques y versiones | `localStorage` (`cartelator.*`) | DOM | No |

Tampoco usa motivos (*patterns*) ni pinceles de Photoshop, filtros, ruido, modos de fusión ni opacidades. Las
únicas órdenes de Photoshop son `make`, `set`, `select`, `delete`, `get`, `transform`, la capa de texto temporal
para medir, la capa de forma de color sólido y `showColorPicker`. `ps.js` cita `pattern` una sola vez, en
`FILL_KINDS = /solid|gradient|pattern|fill/i`: sirve para **reconocer** si la capa seleccionada es una forma de
relleno, no para pintar un motivo.

### 3.2 Al construirse

**No incrusta nada.** `tools/build.py` solo une JavaScript y copia `src/` e `icons/`; no hay ningún script que
procese imágenes.

### 3.3 Cómo pinta (para saber qué NO necesita textura)

Todo es **procedural**: geometría vectorial convertida a píxeles con colores planos.

1. **Letras.** `ps.measureOutlines` crea una capa de texto temporal con la fuente instalada que elija el usuario,
   la convierte en trazado de trabajo y lee los contornos. `glyphs.wordsFromOutlines` los convierte en letras con
   sus medidas. No se usa ninguna imagen de letra.
2. **Deformación.** Las letras se deforman según el estilo; son funciones matemáticas, sin mapas de
   desplazamiento de imagen:
   - **Perspectiva y bandas** (`geom.js`, `frames.js`): homografía y parche de Coons.
   - **Bandas de cada línea** (`region.bandMap`): mapa de cada franja, que luego se suaviza en
     `build.smoothBandMap` (gaussiana de σ ≈ 0,55·alto de línea).
   - **Orgánica en formas redondas** (`build.smoothGridMap`): rejilla de 64×64 con desenfoque de σ = 1,6
     celdas, borde fijo y **1.200 pasadas de relajación** (mapa armónico).
   - **Orgánica y Deformada recta** (`columnfill.js`): `inkRows` (40 filas), `stretchCurve`, `tipsOf`
     (48 columnas, umbral del 14 % del alto), `straightTips` y `sideExtend`.
3. **Rasterizado.** `render.rasterLocal` / `fillPolys` / `composite` calculan la cobertura con antialias de
   cada polígono y la pintan con el operador «sobre» en un lienzo RGBA de 8 bits.
4. **Huecos de la Orgánica.** `render.outlineRaster` dilata cada letra con una transformada de distancia exacta
   (Felzenszwalb, `edt1`). El radio es `R = 0,04 × alto mediano de fila × escala del marco`
   (`build.prepareItems`). Con más de 4 millones de píxeles trabaja a menor resolución (`maxPx = 4e6`).
   `composite(…, erase = true)` **borra el alfa** de lo ya dibujado dentro de esa dilatación y después se pinta
   la letra. Si se pasa `o.outline` con un color, sale un contorno de ese color en vez del hueco.
5. **Color.** Colores planos del usuario (`colors[0..2]`, por tamaño o por línea). Ni degradados ni grano.
6. **Salida.** `ps.putBands`:
   - Divide el dibujo en franjas de `max(64, ⌊4.000.000 / ancho⌋)` filas.
   - `RD.trimCanvas` recorta cada franja; la pasan `imaging.createImageDataFromBuffer` (sRGB IEC61966-2.1) e
     `imaging.putPixels`.
   - Todo va a **una capa de píxeles nueva**, creada con `doc.createPixelLayer({ name })` con su modo y opacidad
     por defecto (Normal, 100 %; el plugin no los cambia).
   - En documentos de 16 bits la escala es `v·32768/255` y en 32 bits, `v/255` (`render.toDepth`). En escala de
     grises usa la luminancia `0,299R + 0,587G + 0,114B` más el alfa.
7. **Azar.** No hay texturas que elegir. `Math.random` solo crea los id de bloque (`main.js → newId`). El estilo
   Loca usa un xorshift con semilla fija (`loca.rng`, semilla `variante·7919 + fila·104729 + 17`), así que todo
   resultado es **reproducible**.
8. **Formas básicas.** `shapelib.js` define 18 formas vectoriales. `ps.makeShapeLayer` crea una capa de forma de
   color sólido (`contentLayer` → `solidColorLayer`).

**Efectos 100 % procedurales (no buscarles textura):** todos los de la lista anterior. Eso incluye la deformación
de cada estilo, la «pompa» de la Orgánica, sus huecos transparentes, las puntas rectas inclinadas de la Deformada
recta, el puzle de la Loca, la perspectiva, la cinta curva y el antialias.

### 3.4 Tabla de archivos fuente

No hay ninguna fuente de textura. Esta tabla recoge **todas** las imágenes y tipografías que hay en el proyecto
o que usan sus pruebas, para que no se confundan con texturas:

| Fuente | Familia | Uso | Formato final / parámetros |
|---|---|---|---|
| `icons/plugin.png`, `plugin@2x.png` | icono_plugin | Icono en la lista de plugins | PNG RGBA 48×48 y 96×96, al .ccx tal cual |
| `icons/panel.png`, `panel@2x.png` | icono_panel | Icono de la pestaña del panel | PNG RGBA 23×23 y 46×46, al .ccx tal cual |
| `icons/formas/*.png` (18: arco, circulo, cruz, cuadrado, elipse, escalera, flecha, l, paralelogramo, perspectiva, rayo, rectangulo, rombo, t, trapecio, triangulo, u, vertical) | icono_forma | Botones de «Formas básicas» (`main.js → renderShapes`) | PNG RGBA 64×64; silueta gris (#AAAAAA–#BBBBBB) con antialias sobre transparente; se muestra a 26×26 px. Los generó un script de un solo uso que no está en el repositorio (**sin verificar** cómo; probablemente Pillow a partir de `shapelib.js`). |
| `referencias/00…12_*.png` (13) | referencia_cartel | **No se usan.** Carteles de referencia de maquetación que dio el usuario | Fuera del .ccx. Son carteles de terceros: **no deben usarse como fuente de textura**. |
| `estado_actual.png` | captura_pruebas | **No se usa.** Hoja de resultados de pruebas | Fuera del .ccx |
| Fuentes del sistema en `tests/fakeText.js`: DejaVuSerif-Bold, TeXGyreHerosCn-Bold, Inter-Black, TeXGyreHeros-Bold, TeXGyreChorus-MediumItalic y Poppins Bold/Medium/Light/Regular | tipografia_pruebas | Solo en las pruebas sin Photoshop: dan los contornos que en Photoshop da la fuente instalada | Fuera del repositorio y del .ccx. No son texturas. |
| `tests/sim/out/*.png`, `tests/out/*` | (generado) | Capturas que crean las pruebas | No son fuentes |

---

## 4. Nombres

- **Estilos** (no son materiales): `recta`, `bloque`, `deformada` (en el panel «Deformada orgánica»),
  `deformada_recta`, `organica`, `loca`. Los modos antiguos se traducen con `main.js → STYLE_OF`:
  `auto`/`cartel` → `deformada`, `texto` → `recta`.
- **Tamaños de palabra:** `normal`, `bold` (destacada), `hero` (protagonista), `small` (pequeña).
- **Formas básicas:** los 18 id de la tabla anterior (`shapelib.js → SHAPES`).
- **Marcos:** `perspectiva`, `curva`, `anotación` (cinta), `libre` y forma por zonas.
- **Posibles choques de nombre en la biblioteca:**
  - `organica` / «orgánica» es aquí un estilo de maquetación, no un material. Conviene no usar ese nombre para
    una familia de textura sin prefijo.
  - `sello`: la referencia `07_once_upon_sello.png` muestra **tinta de grabado o sello de caucho dentro de la
    letra**. No es el `sello_seco` de PAPELATOR (relieve notarial) ni el efecto «Sello de brocha» de NEONIZADOR
    (muro de brochazos).
- **Materiales compartidos con otros plugins:** ninguno, porque no tiene. Sus referencias sí muestran materiales
  que **probablemente ya existan** en otros plugins (**sin verificar** que sean las mismas fotos):

| Lo que se ve en la referencia | Material probable en otro plugin |
|---|---|
| Borde de papel rasgado (`06_avonat_papel_rasgado`) | PAPELATOR, bordes (tira): `artesanal`, `kraft`, `gris`, `viejo`, `viejo_roto`… (`BORDES/`, 20 px/mm) |
| Brocha y pincel (`08_crucible_pincel`, `09_new_pop_brocha`, `10_just_do_it_brocha`) | A mano, cintas `brocha`, `pincel`, `pincelfino`, `guache`; NEONIZADOR `pincel_vert`, `pincel_relieve`, `trazo_seco*`; Trazo (sin verificar) |
| Papel envejecido y tinta de imprenta gastada (`01_bolshevik_rayos`, `02_carteles_constructivistas`, `04_nova_generacia`) | PAPELATOR, papeles `_d.png`; A mano, baldosa de grano de 256×256; NEONIZADOR `papel_fibra`, `papel_rugoso`, `papel_periodico`; Analog FX (sin verificar) |
| Grabado o linóleo dentro de la letra (`07_once_upon_sello`) | No he encontrado ninguno equivalente en los documentos del proyecto (sin verificar) |

---

## 5. Qué necesita de la biblioteca común

**Hoy, nada.** Cartelator no tiene texturas, así que leer de una carpeta `Biblioteca/` con índice JSON **no le
obliga a cambiar nada**: ni el plugin ni `tools/build.py`. Sigue siendo 100 % autónomo (funciona sin internet y
sin Claude) y seguirá siéndolo.

- **Iconos.** Los 22 iconos son **interfaz** propia del plugin. Recomiendo que se queden en `icons/` y **no** pasen
  a la biblioteca de texturas.
- **Referencias.** `referencias/` son carteles de terceros: no deben entrar en la biblioteca como fuentes.

**Lo que le faltaría si algún día tiene «acabados»** (idea mía a partir de sus referencias; **el usuario no lo ha
pedido para Cartelator**):

| Acabado posible | Qué recibiría mejor ya procesado de la biblioteca | Formato que le iría bien |
|---|---|---|
| Borde de papel rasgado en las letras (AVONAT) | Tiras de borde rasgado ya recortadas, con su alfa y la línea del filo | Las tiras de PAPELATOR (RGBA, 20 px/mm, filo marcado) |
| Relleno de tinta de grabado o sello de caucho (ONCE UPON, Nova Generatsia) | Máscaras de densidad de tinta **repetibles**, a escala real | PNG gris de 8 bits (0 = sin tinta, 255 = tinta plena) con su tamaño en mm |
| Bordes de brocha seca (JUST DO IT, NEW POP) | Cintas de trazo enderezadas o máscaras de borde de brocha | El formato de cintas de A mano (densidad 8 bits, filas a lo largo del trazo) |
| Grano de papel o impresión gastada sobre todo el bloque | Baldosas de grano repetibles a escala real | Gris de 8 bits, 128 = neutro, con px/mm |

**Si se añadieran**, el camino que mantiene el .ccx autónomo sería el de A mano:
1. `tools/build.py` leería `Biblioteca/<índice>.json`, elegiría por familia e id estable, convertiría a gris de
   8 bits y escribiría un módulo generado `js/texdata.js` en base64.
2. El plugin **no leería archivos al ejecutarse**.
3. El motor aplicaría la textura en `render.composite`, multiplicando la cobertura de cada letra por la densidad.
   La escala real saldría de `doc.resolution` (px/mm).

Esto es **una propuesta, no código existente**.

**Preguntas para la conversación de la biblioteca:**
- ¿Habrá familias de «tinta de grabado / sello de caucho» y de «borde de brocha seca»? Serían las que más le
  servirían.
- ¿El índice dará la escala real (px/mm) de cada textura repetible?

---

## 6. Cómo comprobar que no se rompe

Como no lee ninguna textura, ningún cambio en la biblioteca puede afectarle. Aun así, para comprobarlo con
números:

1. **El empaquetado no cambia.** Sin escribir nada, el `main.js` que generaría `tools/build.py` tiene que dar el
   mismo sha256:

   ```bash
   cd cartelator && python3 -B -c "import importlib.util,hashlib;s=importlib.util.spec_from_file_location('b','tools/build.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(hashlib.sha256(m.bundle().encode()).hexdigest())"
   # esperado: 4cdf9021700cddf71d00625dc2e93cf94586160eab1b995b3fbaac697edc181d
   ```

   El .ccx tiene que contener exactamente estos 27 archivos (bytes sin comprimir):
   - `LEEME.txt` 6.871, `index.html` 8.985, `main.js` 276.057, `manifest.json` 858, `styles.css` 8.834.
   - `icons/panel.png` 1.096, `panel@2x.png` 2.508, `plugin.png` 3.103, `plugin@2x.png` 6.456.
   - `icons/formas/`: arco 1.616, circulo 1.923, cruz 902, cuadrado 419, elipse 1.426, escalera 768, flecha 1.253,
     l 608, paralelogramo 1.293, perspectiva 1.778, rayo 1.323, rectangulo 428, rombo 1.677, t 703, trapecio 1.378,
     triangulo 1.597, u 700, vertical 450.

2. **Los mismos píxeles.** Los encajes son deterministas: los he ejecutado dos veces y los 62 resultados salen
   idénticos byte a byte. Necesitan las mismas fuentes del sistema (sha256 abreviado: DejaVuSerif-Bold
   `847b33e13925f19f`, texgyreheroscn-bold `ba3b1a5915994b41`, Inter-Black `1dc81aa64047bfb4`) y Node 22.

   ```bash
   node tests/run_styles.js /tmp/ref/styles                  # 6 estilos × 7 formas = 42 casos
   node tests/run_org.js   /tmp/ref/org organica             # 10 casos
   node tests/run_org.js   /tmp/ref/dr  deformada_recta      # 10 casos
   (cd /tmp/ref && find . -name '*.raw' | sed 's|^\./||' | sort | xargs sha256sum)   # comparar con la lista de abajo
   python3 tests/sheet.py /tmp/ref/styles/list.json hoja.png 7      # para verlo (o tests/patsheet.py)
   ```

   <details><summary>sha256 de los 62 renders de referencia (versión 3.7.1)</summary>

   ```
   541a7e99d13789ed2d2a446235c3ea52e7968a10afcda8b3229fa5c95d1b3b80  dr/fargo_persp.raw
   2dd947eccbbbfa7c19b607be337561c95cb7b7a0261d33d7a13588b0c918aaad  dr/laya_rombo.raw
   e9c99147138f53f9ccb33462f1320430767112359fdce39f46d280ca3b2c930a  dr/nadie_cuadrado.raw
   06d7d2e419a92d679c699710640d2f5142149044b1542aac0efc72ae73639464  dr/notnew_circulo.raw
   7c730d39012bcd8748728ae35e8c6cf89379d6eaea1f1d0c21697767389ea47e  dr/notnew_columna.raw
   0e0b41a642e12d58426ded314ec6f96c4c4ae1cafe10e6bff404797ea7b3d9b9  dr/notnew_cuadrado.raw
   7b6e43250063d4f44fd2b294164c2fff22aa61170ae7661fa40b7be5b9df7e96  dr/notnew_triangulo.raw
   8006f17a7e6c7a1d5dac2a87896201079bd79fdf3b8c9d77a73931014a51a906  dr/prueba_L.raw
   29cb5ff4854d3f8243652b2187a94fb77844fdb1a1d21d955e6a7cf1f2534eb6  dr/revol_rect.raw
   6da2e866076c1dbde55da75128c38650623c9a9d2b8608bcf42cc0f31f60412f  dr/solido_elipse.raw
   f2285e7fcc90daa4666d56f371e1baa7e840030c49a4559fedc925c6700a4798  org/fargo_persp.raw
   615979fc46184c19f942ac62540a1f9569dc354c8c15b62decb38ebbfaeb9ea5  org/laya_rombo.raw
   3f93a4c15f015a7f9ece681aa618a69d585d4895827d78799200316f61d2ebb2  org/nadie_cuadrado.raw
   561a2cbdae9b859611b600e781706c68995465fb08216607aad13df1a5db7704  org/notnew_circulo.raw
   2b618c4ce552189dd832c2339285c387ddaeb934889abad83833a16db3004ac9  org/notnew_columna.raw
   d49b5bb23fc61b99f5976baaa1f875ad94c40453bec8a3ea26ee8267cadc23d6  org/notnew_cuadrado.raw
   80d126d3f0795a37c5100a2cf0c9e3059db199098ab361b259e302210d31ea3a  org/notnew_triangulo.raw
   301941df5c2457b671676bdcdb868671f191a484c82eddf6db9d6d75e53a2016  org/prueba_L.raw
   37c0f977c34702d99eed850bbf71df93d4e4db5f675a70e86b83bd3e78680b20  org/revol_rect.raw
   295b21f0b089d412941a03f9ea5a118fa969b44856ba70b73342087767977716  org/solido_elipse.raw
   d33d026d80d1a263319107a5026ec1f755216c75c26089cdecdaf4a7386f3467  styles/bloque_festival_persp.raw
   6e0b9a1f03a6877d8672dc75851668a548e02315e5b85534b29279b37c0290c5  styles/bloque_festival_triangulo.raw
   2574fe13c604815f72f3097f62f6d2f76e6d41507dc887d5971f8581888355a9  styles/bloque_notnew_cuadrado.raw
   f222814503cba6f71ba768e2f45c1835aefe477832b067c0d346c6ccabfbc66c  styles/bloque_prueba_L.raw
   b61eab2b7896ebbbd20d704f7d258015eecd65444654df0ebe31d775eca90f87  styles/bloque_prueba_blob.raw
   43d32508ace223f1373c3887de89bf1d831e9ea35969373094b680161983d0a8  styles/bloque_prueba_elipse.raw
   2d6d9c8e35501413e88046306500795796dfe0f2725df1d07ff85e7d893cb3bb  styles/bloque_typo_columna.raw
   f52f461f3a86d5c993a68a5eafee8da4555d06936dfb88290fb8555071f98eec  styles/deformada_festival_persp.raw
   123b05d22c7ffa475b0491a89d29f1fee5c6db5aa55601dcd2761fc305d8c901  styles/deformada_festival_triangulo.raw
   70e0bb4fdc05240be7ee93e70959a76c9613bc5d38d49441a33f471a8dc80359  styles/deformada_notnew_cuadrado.raw
   1ab476f7401fb770deefd80c86c4ec4818fe4a0165093e57e78ae27e3b08d0ae  styles/deformada_prueba_L.raw
   02b3aab73ebd52b62635d3168e965a57e62c070cb2c287279de1adaac1806876  styles/deformada_prueba_blob.raw
   7d41f16d478337b66ffb8beedf15c77f0432221a08a2245e69aa0ea618f59daa  styles/deformada_prueba_elipse.raw
   3a6386d76e6a5f1014a41ce2c27111a1c7844257c9ad2c46cf01025211c6d99a  styles/deformada_recta_festival_persp.raw
   fe38acdea4b67a4aff5c94b8a736fd1b7e7ea321c58186423319c537876db965  styles/deformada_recta_festival_triangulo.raw
   730c7fb023719592aaa2be3fa58338782f22f2008c6ff4213cca95f89de0e547  styles/deformada_recta_notnew_cuadrado.raw
   799b5e546c08485f4ddf1850815c0f72fba17faaa080ff830b896e2ffaa68d8a  styles/deformada_recta_prueba_L.raw
   cfadd6f296f8c26cdace322fadbc42f99876e2dbb2140f1f43ecf5b6048db759  styles/deformada_recta_prueba_blob.raw
   1393d7a8ac9f30177fda822f819d796208280ded236ad61316dfc11d487e1ca3  styles/deformada_recta_prueba_elipse.raw
   a982c199a405402cac68e7b0cde4dfc62e9dc499373fb2768f3fb76e96dbe8b7  styles/deformada_recta_typo_columna.raw
   a280865c2415070d99b2402cb8c86c44c86f63564f56fb1cbbd893d75f4e7c64  styles/deformada_typo_columna.raw
   588c6ff45112a6a245c99a09c44ffc983b3ce7d654d9e1b786bd44e30c57fc50  styles/loca_festival_persp.raw
   bcd39c40a6109fe4011bb95aeaa4bc7e455107c6726e9099c932a87c02c5e102  styles/loca_festival_triangulo.raw
   a76d33074975a83f9b481917a24e1d36a5b9eff4434ae6335933ff926476970c  styles/loca_notnew_cuadrado.raw
   d6f585aa840bf97af0c3c3458d4bca511a4da47a37808abe4ae9d1a387e798eb  styles/loca_prueba_L.raw
   9862de9e2eeab08186a14826ca0375b436787e6ff2fc6e8f71b4953c498d7857  styles/loca_prueba_blob.raw
   233083859f56821e266fe8fb6a343b592d92f6726fd383bbb207c62a5ec5f040  styles/loca_prueba_elipse.raw
   afde90b94e98fccadda91b5a939aeeaddf008e3886e68677f8f436c0af6bdad1  styles/loca_typo_columna.raw
   988e461dea03ecf0500a28b15b219345a152e81dde3d4537707826c912b8b162  styles/organica_festival_persp.raw
   4b1201623615503024bcf8dd959640679a8e414f33b6ad40f5d39cecdf90fe7d  styles/organica_festival_triangulo.raw
   02b0744eddf73886c57ae8bacc7365671d28c48d8c103a8c410ac990a0cb689c  styles/organica_notnew_cuadrado.raw
   ab057f3203f4fd4af2906967e607bc445c030b0f432abb44290e9049d9e406eb  styles/organica_prueba_L.raw
   de62f4f1fb600f82a53dd20fd6b63fea744e826168e6c312cd01cb0649d9d592  styles/organica_prueba_blob.raw
   6ecae768dcd0bca60f90d88c30456bb367ddb627e29fe05cde0629f2ee85fd45  styles/organica_prueba_elipse.raw
   dbf57557216ed9961c3193460169719fe2814f0080e52ff232502edf68c977bd  styles/organica_typo_columna.raw
   ce5ed358451c04197ad93a9a490b8461fa10070207151002981c0e877bcef6ae  styles/recta_festival_persp.raw
   8ef8a7a2a283697e20373c55d4f8493dc0c78a5837c06690cef46c5906c92a19  styles/recta_festival_triangulo.raw
   d0c030f35aec19c0c64ee01190c6c7303bbcb4d83017ffbebd167ad56daa4cc9  styles/recta_notnew_cuadrado.raw
   e8a5b01637fc85f1358690f43aef0e8e1f8606e5793d0bc598c3b4306a4d6546  styles/recta_prueba_L.raw
   e8a3a016cc91c317064afd20f3598beb8a720336a073164db1b7d9a87bbfce1c  styles/recta_prueba_blob.raw
   55087994d2afbb0a424938f1f051b3f3fffc825eb2defe625c913f66367f8604  styles/recta_prueba_elipse.raw
   3f8f4a22e0e8d4bb5f736de5be3c71cf106f5259de689404c51e522c998fb195  styles/recta_typo_columna.raw
   ```
   </details>

3. **Photoshop simulado.** Ejecuta `python3 tools/build.py` y después estas pruebas:

   | Prueba | Resultado esperado |
   |---|---|
   | `node tests/sim/startup.js` | «Comprobación: todo bien» · «documento igual que antes: true» · 0 errores de modal |
   | `node tests/sim/stress.js` | 0 errores de modal |
   | `node tests/sim/harness.js` | `fallos: [ 'sin forma (debe avisar)' ] errores modal: 0`. Ese «fallo» es esperado: comprueba que avisa cuando no hay forma. Las capturas quedan en `tests/sim/out/`. |

4. **Photoshop real.** Nunca se ha probado. Si se prueba, basta con comprobar que el panel abre, que «Formas
   básicas» enseña sus 18 iconos y que «Generar» deja una capa de píxeles.

---

## 7. Anexo JSON

45 entradas: todas las imágenes del proyecto y las tipografías de sus pruebas. **Ninguna es textura**
(`es_textura: false`).

```json
[
 {
  "fuente": "icons/plugin.png",
  "familia": "icono_plugin",
  "uso": "Icono en la lista de plugins (manifest.json → icons, species pluginList, scale 1)",
  "formato_final": "PNG RGBA 48×48, copiado tal cual al .ccx",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "lo carga Photoshop/UXP desde el manifest",
   "bytes": 3103,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/plugin@2x.png",
  "familia": "icono_plugin",
  "uso": "Ídem a 2× (scale 2)",
  "formato_final": "PNG RGBA 96×96, copiado tal cual al .ccx",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "lo carga Photoshop/UXP desde el manifest",
   "bytes": 6456,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/panel.png",
  "familia": "icono_panel",
  "uso": "Icono de la pestaña del panel (manifest.json → entrypoints[0].icons, species chrome, scale 1)",
  "formato_final": "PNG RGBA 23×23, copiado tal cual al .ccx",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "lo carga Photoshop/UXP desde el manifest",
   "bytes": 1096,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/panel@2x.png",
  "familia": "icono_panel",
  "uso": "Ídem a 2× (scale 2)",
  "formato_final": "PNG RGBA 46×46, copiado tal cual al .ccx",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "lo carga Photoshop/UXP desde el manifest",
   "bytes": 2508,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/cuadrado.png",
  "familia": "icono_forma",
  "uso": "Botón «Cuadrado» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 419,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/rectangulo.png",
  "familia": "icono_forma",
  "uso": "Botón «Rectángulo» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.6)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 428,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/vertical.png",
  "familia": "icono_forma",
  "uso": "Botón «Columna» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 0.55)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 450,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/triangulo.png",
  "familia": "icono_forma",
  "uso": "Botón «Triángulo» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.15)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1597,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/trapecio.png",
  "familia": "icono_forma",
  "uso": "Botón «Trapecio» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.3)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1378,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/perspectiva.png",
  "familia": "icono_forma",
  "uso": "Botón «Perspectiva» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.4)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1778,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/rombo.png",
  "familia": "icono_forma",
  "uso": "Botón «Rombo» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.25)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1677,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/paralelogramo.png",
  "familia": "icono_forma",
  "uso": "Botón «Inclinado» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.6)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1293,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/l.png",
  "familia": "icono_forma",
  "uso": "Botón «L» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 608,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/t.png",
  "familia": "icono_forma",
  "uso": "Botón «T» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 703,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/u.png",
  "familia": "icono_forma",
  "uso": "Botón «U» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 700,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/cruz.png",
  "familia": "icono_forma",
  "uso": "Botón «Cruz» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 902,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/escalera.png",
  "familia": "icono_forma",
  "uso": "Botón «Escalera» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 768,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/rayo.png",
  "familia": "icono_forma",
  "uso": "Botón «Rayo» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 3.2)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1323,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/arco.png",
  "familia": "icono_forma",
  "uso": "Botón «Arco» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.9)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1616,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/circulo.png",
  "familia": "icono_forma",
  "uso": "Botón «Círculo» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1923,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/elipse.png",
  "familia": "icono_forma",
  "uso": "Botón «Elipse» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.55)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1426,
   "es_textura": false
  }
 },
 {
  "fuente": "icons/formas/flecha.png",
  "familia": "icono_forma",
  "uso": "Botón «Flecha» de Formas básicas (main.js → renderShapes: <img src=\"icons/formas/<id>.png\">); al pulsarlo crea una capa de forma vectorial (shapelib.js, proporción 1.6)",
  "formato_final": "PNG RGBA 64×64, silueta gris (#AAAAAA–#BBBBBB) con borde suavizado sobre transparente; se muestra a 26×26 px (styles.css .shp img)",
  "parametros": {
   "en_ccx": true,
   "se_lee_al_ejecutar": "sí, como <img> del panel (solo interfaz)",
   "bytes": 1253,
   "es_textura": false
  }
 },
 {
  "fuente": "referencias/00_resultado_malo_v2_huelga.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (mal resultado de la versión 2 (lo que NO había que hacer))",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 401×467",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 32983,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/01_bolshevik_rayos.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (cartel constructivista en rayos; papel envejecido y tinta de imprenta gastada)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 535×525",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 704869,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/02_carteles_constructivistas.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (mosaico de carteles constructivistas (Fuchsia/Shepard Fairey); tramas y papel)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 564×736",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 840041,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/03_brazil.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (BRAZIL: texto en perspectiva con rayos)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 491×698",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 578420,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/04_nova_generacia.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (Nova Generatsia: tipografía grabada/impresa, papel con grano y tinta irregular)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 591×869",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 1208136,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/05_entuziasm_arcos.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (ENTUZIASM: texto en arcos)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 512×793",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 561152,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/06_avonat_papel_rasgado.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (AVONAT: letras de papel rasgado (borde de rasgado blanco))",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 517×651",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 489293,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/07_once_upon_sello.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (ONCE UPON A TIME IN HOLLYWOOD: letras con textura de grabado/sello de tinta)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 550×721",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 776626,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/08_crucible_pincel.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (THE CRUCIBLE: rotulado a pincel)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 552×378",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 247462,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/09_new_pop_brocha.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (NEW POP: rotulado a brocha seca)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 591×627",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 626978,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/10_just_do_it_brocha.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (JUST DO IT: bloque a brocha/rodillo con bordes rugosos)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 577×802",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 537141,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/11_post_punk.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (POST PUNK: bloque de letras altas)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 553×799",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 574608,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "referencias/12_fargo_perspectiva.png",
  "familia": "referencia_cartel",
  "uso": "NO se usa: referencia visual de maquetación que dio el usuario (FARGO: texto en perspectiva)",
  "formato_final": "ninguno (no va al .ccx); PNG RGBA 606×731",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 246395,
   "es_textura": false,
   "derechos": "carteles de terceros: no usar como fuente de textura"
  }
 },
 {
  "fuente": "estado_actual.png",
  "familia": "captura_pruebas",
  "uso": "NO se usa: hoja de resultados de pruebas para el README",
  "formato_final": "ninguno (no va al .ccx); PNG RGB 2376×760",
  "parametros": {
   "en_ccx": false,
   "se_lee_al_ejecutar": false,
   "bytes": 417683,
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "847b33e13925f19f",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheroscn-bold.otf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "ba3b1a5915994b41",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/fonts/opentype/inter/Inter-Black.otf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "1dc81aa64047bfb4",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "b170162835f4efc2",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrechorus-mediumitalic.otf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "b26e0f8edc4c56d8",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/fonts/truetype/google-fonts/Poppins-Bold.ttf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "983676516167748b",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/fonts/truetype/google-fonts/Poppins-Medium.ttf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "90373e7d838d3246",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/fonts/truetype/google-fonts/Poppins-Light.ttf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "650ba57fa99d12ec",
   "es_textura": false
  }
 },
 {
  "fuente": "/usr/share/fonts/truetype/google-fonts/Poppins-Regular.ttf",
  "familia": "tipografia_pruebas",
  "uso": "Solo pruebas sin Photoshop (tests/fakeText.js): da los contornos de las letras que en Photoshop da la fuente instalada del usuario",
  "formato_final": "ninguno (no va al .ccx; está fuera del repositorio, en el sistema)",
  "parametros": {
   "en_ccx": false,
   "en_repo": false,
   "existe_aqui": true,
   "sha256_16": "7e65201e9b79159e",
   "es_textura": false
  }
 }
]
```
