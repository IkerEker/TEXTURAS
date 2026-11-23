# CONTEXTO COMPLETO · La Biblioteca de Iker (TEXTURAS + ACIDBITE + originales)

*Documento de traspaso. Estado a **23-11-2026** (último trabajo: 20-11-2026, commit `b1740d0`, rama `atlas`).*

**Para qué sirve:**
1. Seguir esta conversación en otra nueva sin perder nada.
2. Explicar a cualquier conversación (plugins, montaje, nuevos proyectos) qué es la biblioteca, cómo está organizada,
   qué archivos usa, cómo se busca, qué reglas hay y qué queda pendiente.

**Cómo usarlo:**
- **Para una conversación nueva que siga este trabajo:** pégale este archivo entero y dile «eres la conversación
  TEXTURAS/Biblioteca; continúa desde aquí».
- **Para un plugin:** basta con los apartados 1–9 y 14. Su orden concreta está en
  `TEXTURAS/plugins/ORDEN_BUSCAR.md`.

**Copias de este archivo:**
- en el repo: `TEXTURAS/CONTEXTO_BIBLIOTECA.md`;
- en el PC: `C:\Users\ikerg\Biblioteca\CONTEXTO_BIBLIOTECA.md`.

---

## Índice

0. Resumen en 20 líneas
1. Quién es Iker y qué quiere (requisitos literales)
2. Reglas permanentes (no se rompen nunca)
3. Hardware y entorno
4. Dónde está todo (carpetas, repos, rutas completas)
5. Qué hay en la biblioteca (números, colecciones, clases, papeles)
6. Identificadores y tipos de archivo
7. El índice y las fichas (campos)
8. Cómo se busca: buscador v3, necesidades y librería
9. Reglas de variedad
10. Herramientas (scripts) y cómo regenerar
11. Productos comunes y formatos
12. Recortes mejorados (20-11-2026)
13. Revisión 100 % a ojo (19→20-11-2026)
14. Los plugins: fichas, pruebas exactas, órdenes enviadas
15. Pedidos («PEDIDO PARA LA BIBLIOTECA»)
16. Historial de lo hecho (cronología)
17. Estado actual y pendientes
18. Cómo trabaja Claude aquí (puente al PC, límites, convenciones)
19. Documentos de referencia (dónde está cada detalle)

---

## 0. Resumen en 20 líneas

1. **Qué es.** Iker tiene varios plugins de Photoshop/After Effects (NEONIZADOR, PAPELATOR, A mano, Analog FX, Trazo,
   Cartelator y otros nuevos) que necesitan texturas, trazos, manchas, vídeos, sonidos… Todo ese material vive en
   **una sola Biblioteca**, en su PC: `C:\Users\ikerg\Biblioteca`.
2. **Qué hay dentro.** La Biblioteca tiene:
   - `TEXTURAS` (repo git privado con lo procesado, el índice y el buscador);
   - `ACIDBITE` (pack de pago, 190 GB);
   - `originales` (fuentes intactas de los plugins);
   - `generadas`;
   - `plugins` (la casa local de cada plugin).
3. **El índice.** `TEXTURAS/indice/indice.json` tiene **9.031 recursos**: 3.668 TEXTURAS, 2.925 ACIDBITE y 2.438
   originales. Cada uno lleva una **ficha revisada a ojo**: qué es, nota 1–5, defectos, familia, uso, modo de fusión,
   cuándo usarlo y cuándo no, color, estilo y medidas.
4. **Cómo se busca.** **Siempre con `TEXTURAS/tools/atlas/buscar.py` (v3).**
   - Lo primero, `--necesidades`: **78 necesidades** con su lista curada a ojo (5–16 opciones variadas) y su hoja de
     miniaturas ya hecha.
   - Si ninguna encaja, búsqueda libre con `--ver`: un abanico de 12 opciones distintas y una hoja JPG.
5. **El problema que se arregló el 20-11.** Los plugins elegían siempre lo mismo.
   - El buscador viejo devolvía los empates en el orden del archivo y nunca enseñaba ACIDBITE.
   - Ahora ordena por lo que encaja, entiende sinónimos, reparte por familias y colecciones, y marca lo que ya usa
     otro plugin.
6. **Regla de oro.** Los plugins funcionan **100 % solos**, sin Claude y sin internet.
   - La biblioteca **solo se usa al construir**: cada plugin lleva dentro lo que usa.
   - **Ningún resultado de un plugin cambia sin que Iker lo sepa.** Cada plugin tiene su prueba exacta.
7. **Material de pago** (ACIDBITE, Gumroad): no se redistribuye y no sale del PC ni de los repos privados.
8. **Ninguna textura se da por buena sin mirarla.**
9. **Órdenes enviadas a los plugins** (archivos en `TEXTURAS/plugins/`):
   - ORDEN 1, `ORDEN_PLUGINS.md`: biblioteca única y velocidad/GPU;
   - ORDEN 2, `ORDEN_CARPETA_LOCAL.md`: dejar GitHub y vivir en `Biblioteca\plugins\<plugin>`;
   - ORDEN 3, `ORDEN_BUSCAR.md`: buscador v3, necesidades y variedad.
10. **Pendiente.** Los plugins están aplicando la ORDEN 3. Producirán **informes** y **PEDIDOS PARA LA BIBLIOTECA**
    (lo que les falte), que Iker traerá aquí para resolverlos.

---

## 1. Quién es Iker y qué quiere (requisitos literales)

Iker crea plugins de Photoshop y After Effects para efectos analógicos, papel, collage, pintura, neón, vídeo…
Habla en español; responder siempre en español, claro y sin jerga.

**Lo que ha pedido, con sus palabras o casi:**
- «Mis plugins tienen que seguir funcionando 100 % solos en mi ordenador, sin Claude y sin internet.»
- «La biblioteca solo se usa al construir.»
- «Repos privados, y el material de pago no se redistribuye.»
- «Ninguna textura se da por buena sin mirarla.»
- «Ningún plugin puede cambiar su resultado sin que yo lo sepa: cada uno tiene su prueba exacta.»
- «No toques el resultado de ningún plugin ni sus archivos.»
- «No borres ni muevas nada en mi ordenador. No toques los zip.»
- «El material de pago (AcidBite, Gumroad) no sale de mi PC ni de repos privados.» ACIDBITE no se hace público nunca.
- No tocar `main` de NEONIZADOR sin permiso.
- «Haz todo lo que puedas tú solo… Si queda más, luego me dices.»
- Sobre la variedad (20-11): los plugins «eligen como siempre la misma textura, todo es lo mismo… es muchísimo material
  que he gastado dinero y tiempo… que no se está utilizando». Quiere que los plugins **no tengan que barrer la
  biblioteca** para encontrar algo, y que **se usen todos los archivos, sobre todo los buenos, con variedad**.
- Quiere **descargables listos para pegar** en las conversaciones de cada plugin, con **rutas completas**.
- Las chispas y pavesas de nota 1–2 sirven como **partículas de relleno de fondo**, para usarlas en masa con
  desenfoque de movimiento (`rol: relleno de fondo`, filtro `--relleno`).
- Le gustan las respuestas cortas, fáciles de leer y con ejemplos.

---

## 2. Reglas permanentes (no se rompen nunca)

1. Los plugins funcionan solos (sin Claude ni internet). La biblioteca alimenta la **construcción**, no la ejecución.
2. **Prueba exacta** antes y después de cada cambio (tabla del apartado 14). Si un byte o una huella cambia, se para
   y se enseña el antes y el después a Iker. Él decide.
3. **Repos privados.** ACIDBITE y Gumroad no se redistribuyen. Los archivos de ACIDBITE no entran en git: solo su
   índice y sus hojas.
4. **Nunca dar por buena una textura sin mirarla:** hoja de contactos y Read.
5. No borrar ni mover nada en el PC de Iker. No tocar los zip de `C:\Users\ikerg\Downloads\ADIDBITE`.
6. Plugins: trabajar en rama; no fusionar en `main` sin el OK de Iker (y `main` de NEONIZADOR no se toca).
7. Si falta material, no dibujarlo, no descargarlo y no crear bancos dentro de un plugin: **PEDIDO PARA LA
   BIBLIOTECA**.
8. **Cambiar un plugin a material mejor** (por ejemplo un `tx:` con recorte mejorado) cambia su resultado: se propone
   con el antes y el después y se espera el sí de Iker.
9. Una sola fuente de material: la Biblioteca. No hay copias repetidas.

---

## 3. Hardware y entorno

- **PC de Iker** (Windows, usuario `ikerg`): **2 × NVIDIA RTX 4090** (24 GB de VRAM cada una), **64 GB de RAM**.
- **Procesado:**
  - lo que alimenta a un plugin se procesa en **CPU, de forma determinista** (numpy/Pillow), para poder comprobarlo
    bit a bit;
  - la GPU es para lo pesado que no entra en ninguna prueba exacta: proxies, vídeo NVENC/NVDEC, análisis;
  - una versión GPU que no dé idéntico queda apagada hasta que Iker diga sí.
- **Conversaciones de Claude:**
  - se enlazan con el PC mediante la app de escritorio, con **una sola carpeta conectada**: `C:\Users\ikerg\Biblioteca`;
  - en esta conversación también está conectada `C:\Users\ikerg\Downloads\ADIDBITE` (los zip de AcidBite: solo
    lectura, no tocar).
- **Sandbox de la nube de Claude:**
  - red: solo GitHub y los registros de paquetes;
  - sin GPU;
  - disco libre limitado (~5 GB): hay que borrar lo traído del PC después de usarlo.

---

## 4. Dónde está todo (rutas completas)

```
C:\Users\ikerg\Biblioteca\                       = TEXTURAS_ROOT (raíz de todas las rutas «archivo» del índice)
├── CLAUDE.md                                    instrucción de búsqueda (se carga sola al abrir la carpeta)
├── CONTEXTO_BIBLIOTECA.md                       este documento
├── ACTUALIZAR_TEXTURAS.bat                      git pull de TEXTURAS + comprobar buscar.py v3 (log en _ESTADO_ACTUALIZAR.txt)
├── MONTAR_BIBLIOTECA.bat / montar_biblioteca.ps1   montaje inicial (19-11); log en _ESTADO_MONTAJE.txt
├── REVISION_FOTOGRAMAS.bat / .ps1               extracción de fotogramas para la revisión (19-11)
├── ESTADO_BIBLIOTECA.json                       resultado del montaje (2.191 originales; 0 faltan; 0 md5 distintos)
├── TEXTURAS\                                    clon del repo privado IkerEker/TEXTURAS, rama atlas
│   ├── indice\indice.json                       EL ÍNDICE (9.031 recursos con ficha)
│   ├── indice\necesidades.json                  78 necesidades curadas · necesidades_hojas\*.jpg · necesidades_spec.json
│   ├── indice\sinonimos.json · nombres.json · ESQUEMA.md · correcciones.json
│   ├── tools\atlas\buscar.py                    EL BUSCADOR (v3) · biblioteca.py (librería) · necesidades.py …
│   ├── plugins\                                 fichas, tablas uso_id.json, ORDEN_*.md
│   ├── revision\                                revisión 100 % (RESUMEN.md, FICHAS.json, hojas, recortes_mejorados.json…)
│   ├── MAPA.md · CLAUDE.md · DECISIONES.md · TRASPASO.md · CONTEXTO_BIBLIOTECA.md
│   └── tileables\ trazos\ manchas\ imperfecciones\ bordes\ pliegues\ luz_y_elementos\ superposiciones\
│       video\ collage\ productos\ hojas\ tecnicas\ acidbite\ gumroad\ originales\(MANIFIESTO)
├── ACIDBITE\                                    pack de pago (190 GB), sin reordenar: 01_TRANSICIONES … 07_SONIDO
├── originales\                                  fuentes intactas de los plugins, por repo y ruta (id or:<md5>)
│   └── heredado\neonizador\                     los 715 archivos con los que NEONIZADOR construye hoy plugin/tex
├── generadas\                                   lo que se cree a partir de ahora
├── AÑADIDOS\                                    material que Iker añadió (p. ej. COLLAGE en IA); ya indexado como originales
├── _fuentes\<repo>\                             clones de los repos de plugins usados para montar (no borrar)
├── _revision\                                   fotogramas y material de la revisión
├── plugins\<plugin>\  +  plugins\_respaldos\    casa local de cada plugin (ORDEN 2) y sus .bundle
├── _busquedas\                                  hojas JPG que crea buscar.py --ver (se pueden borrar)
└── _uso\<plugin>.json                           qué ids ha apuntado cada plugin (buscar.py --plugin X --apuntar …)

C:\Users\ikerg\Downloads\ADIDBITE\               zips originales de AcidBite: NO TOCAR
```

**Repos en GitHub** (todos privados; cuenta `IkerEker`):

| Repo | Qué es |
|---|---|
| `TEXTURAS` | La biblioteca. Rama de trabajo: **`atlas`**; `main` está sin fusionar y lo decide Iker. Remoto: `https://github.com/IkerEker/TEXTURAS.git`. |
| `neonizador` / `NEONIZADOR` | Plugin. Rama `biblioteca-texturas`; `main` no se toca. |
| `papelator`, `a-mano`, `analog-fx-plugin`, `trazo` | Plugins. |
| `ESTILO` | Dataset de ilustración. No forma parte de la biblioteca. |
| Cartelator | No tenía repo (vivía en local). |

Por la ORDEN 2, los plugins se están mudando a `Biblioteca\plugins\<plugin>` con copia `.bundle`. Iker borrará sus
repos de GitHub a mano después del informe VERIFICADO.

---

## 5. Qué hay en la biblioteca

**Por colección:**

| Colección | Recursos | Qué es |
|---|---:|---|
| TEXTURAS (`tx:`) | 3.668 | Procesado y limpio: tileables con escala en mm, recortes PNG RGBA descontaminados, relieves 50 % gris, vídeos con tiras, collage (475 piezas), productos comunes. |
| ACIDBITE (`ab:`) | 2.925 | Transiciones 4K, película (16mm/35mm/Super 8), CRT/VHS, collage, overlays, marcadores animados, 658 sonidos, LUT, plantillas, tutoriales. Pago. |
| originales (`or:<md5>`) | 2.438 | Fuentes intactas de los plugins (bit a bit), heredados de NEONIZADOR, Gumroad (cianotipia, slit-scan, transiciones de tinta 4K, mates), COLLAGE en IA. |

**Notas de la revisión a ojo:**

| Nota | Recursos |
|---|---:|
| 5 | 4.245 |
| 4 | 2.398 |
| 3 | 1.135 |
| 2 | 501 |
| 1 | 39 |
| sin nota (sonidos y plantillas, que no se pueden ver) | 713 |

- Hay 270 familias.
- 188 recursos son «mejor de su familia».

**Clases principales** (las de TEXTURAS ampliadas con las de ACIDBITE):
- tileables (papel, superficies, madera y cartón, vidrios y plásticos, pintura, grunge, grafito y carbón, líquidos);
- trazos (lápiz, carbón, cera, rotulador, rotulador gastado, bolígrafo, pincel, pincel seco, gouache, óleo, aguada,
  rotulador y tinta de anotación);
- manchas (pincel, pincel grandes, tinta, goteos con 6 clases);
- imperfecciones (café, agua, humedad, grasa, óxido de clip, foxing, quemadura, cera, grapas, clip, pinza, sello en
  seco, escritura en relieve, cinta adhesiva…);
- pliegues (1–6 pliegues, arrugado, muy arrugado);
- bordes (blanco, gris, cartón, kraft, viejo, viejo_roto, washi, acuarela, bisel, espiral, periódico, vegetal; `C_*` =
  esquinas);
- luz_y_elementos (fuego, chispas, humo, fugas de luz, burbujas y espuma, moho);
- superposiciones (9x16, película polvo y rayas, VHS, fotocopia, visores);
- vídeo (transiciones, elementos, película, analógico, texturas animadas, collage, fondos);
- collage (papeles, cintas, etiquetas, pegatinas, notas, pintura, adhesivos, grafito);
- productos (piezas de NEONIZADOR, cintas de trazo, sellos de relieve, papel gris, mates de tinta 4K);
- sonido, lut, plantilla, tutorial, desplazamiento, máscaras.

**Papel de cada recurso.** Se deduce de su ficha y se busca con `--papel`; `buscar.py --papeles` da el recuento:

| Papel | Recursos |
|---|---:|
| pieza (objeto suelto con transparencia) | 2.839 |
| superposición (imagen encima) | 988 |
| transición (vídeo) | 677 |
| sonido | 658 |
| superposición animada | 595 |
| elemento animado | 506 |
| fondo repetible (tile) | 366 |
| relieve (gris 50 %) | 294 |
| imagen | 197 |
| LUT | 161 |
| máscara | 147 |
| fondo animado | 65 |
| plantilla | 52 |
| tutorial | 48 |

**Fondo de cada recurso** (`--fondo`): transparente · sobre negro (va en Trama) · sobre blanco (va en Multiplicar) ·
gris neutro (va en Superponer) · opaco.

**Huecos conocidos**, porque faltan del todo:
- moho realista grande;
- tiza o pastel;
- grafito por durezas;
- spray real;
- sello de goma;
- rodillo;
- tóner;
- neón;
- imagen térmica;
- corcho;
- pizarra.

Los huecos parciales están en `DECISIONES.md` §13 y en `indice/cruce_acidbite.md`.

---

## 6. Identificadores y tipos de archivo

**Prefijos de id:**

| Prefijo | Qué es | Ejemplo |
|---|---|---|
| `tx:` | TEXTURAS, procesado y productos | `tx:tileables/papel/papel_blanco_0995` (ruta sin extensión, estable entre regeneraciones; `nnnn` = nº de fuente) |
| `ab:` | ACIDBITE | `ab:414315c5770e` (12 hex del md5 de la ruta relativa) |
| `or:<md5>` | original bit a bit | Identidad = contenido: no cambia aunque se mueva el archivo. |
| `gen:` | generadas | Reservado para el futuro. |

El campo `archivo` de cada recurso es la ruta dentro de `Biblioteca\` (por ejemplo
`TEXTURAS/tileables/papel/….jpg` o `ACIDBITE/01_TRANSICIONES/…/x.mov`). Los builds de los plugins resuelven
`id → archivo` con el índice (o con `Biblioteca().ruta(id)`) sobre `TEXTURAS_ROOT`.

**Formatos y convenciones:**
- **PNG RGBA** (recortes, piezas, trazos, bordes):
  - alfa = cobertura real;
  - RGB descontaminado del fondo, sin halo blanco, negro ni verde;
  - recortado al contenido con un pequeño margen;
  - sin premultiplicar.
- **`*_trama.jpg`:** el original sobre negro, con la misma caja que su PNG. Va en Trama.
- **Tileables JPG** (calidad 95, 4:4:4):
  - luz aplanada;
  - costura óptima (`costura` ≤ 1 = invisible);
  - los patrones y aparejos miden un número entero de periodos;
  - `tile_mm` y `mm_por_px` dan la escala real cuando se conoce (vienen de PAPELATOR);
  - `aviso` marca las costuras que se pueden notar (13 tileables).
- **Relieves y pliegues:** gris 8 bits, 50 % (128) = sin efecto. Van en Superponer o Luz suave, o como mapa de
  desplazamiento (campo `desplazamiento`).
- **Goteos:** raíz ARRIBA (`orientacion`).
- **Vídeo:**
  - MP4/MOV/ProRes;
  - las tiras de fotogramas están en `TEXTURAS/video/_tiras/` (las de ACIDBITE, en `TEXTURAS/acidbite/hojas/`);
  - los `_loop.mp4` enlazan sin salto;
  - el bloque `transicion` da tipo, `corte_s`, `cubre_s`, `revelado_s` e `invertir`.
- **Sonido:** `.wav` de ACIDBITE.
  - Están medidos (`revision/audio_medido.json`: duración, forma, pico).
  - **No se han escuchado** (`audio_revisado: false`).
  - Sincronía: el pico del sonido va sobre el corte.
- **LUT:** `.cube`, por cámara y log. Hay que mirar para qué cámara es.
- **Plantillas:** `.drt`, `.mogrt`, `.prproj`, `.aep`, `.prfpset`, `.motr`.
  - Se han **leído por dentro sin abrir el programa** (`revision/plantillas_leidas.json`).
  - Hay que comprobarlas antes de usarlas.
- **Nombres:** `<descripción>_<nnnn>[_<pieza>].<ext>`. Los archivos no se renombran. Los alias de los plugins y del
  inglés están en `indice/nombres.json`.
- **Modos de fusión** (clave común): normal, multiplicar, trama, superponer, luz_suave, luz_fuerte, luz_focal,
  diferencia, sobreexponer_lineal, sobreexponer_color, aclarar, color_mas_claro, mascara_alfa, mascara_luma.
  - `modo_fuente` dice quién lo afirma (autor > tutorial > plantilla > plugin > medido).

---

## 7. El índice y las fichas

**`indice/indice.json`** = `{version, raiz, total, por_coleccion, por_clase, assets[]}`.

Campos del asset (esquema completo en `indice/ESQUEMA.md`):
- identidad y clasificación: `id`, `coleccion`, `archivo`, `tipo`, `clase`, `sub`, `pack`, `estilos`, `colocacion`;
- descripción y técnico: `desc`, `familia`, `color`, `md5`, `w`, `h`, `alfa`, `fondo`, `bytes`;
- tileables y escala: `tileable`, `costura`, `tile_mm`, `mm_por_px`;
- uso: `modo`, `modo_fuente`, `desplazamiento`, `orientacion`, `medidas`;
- procedencia: `origen`, `metodo`, `rutas_antiguas`, `productos`, `usado_por`;
- vídeo y audio: `video{…}`, `transicion{…}`, `audio{…}`;
- otros: `conjuntos`, `lut`, `licencia`, `hoja`, `tira`, `recorte`, `pieza`, `recorte_mejorado`.

**La ficha `revision`** (en cada asset, escrita a ojo):
- `que_es`, `calidad` (1–5), `defectos`;
- `familia`, `variante`, `diferencia`, `mejor_de_familia`;
- `uso`, `modo`, `usar_si`, `evitar_si`;
- `escala`, `orient`, `estilo`, `color`, `contenido`, `comportamiento`;
- `medidas` (w, h, color_medio, luminancia, contraste, saturación, **phash**, alfa_parcial, halo…);
- `rol` (p. ej. «relleno de fondo»), `aviso`, `hoja`;
- estado: `rehacer`, `dudoso`, `duplicado_de`, `sustituido_por`, `corregido`;
- audio y plantillas: `audio_medido`, `plantilla_leida`.

**Archivos de la revisión** (`TEXTURAS/revision/`):

| Archivo | Qué es |
|---|---|
| `FICHAS.json` | todas las fichas |
| `fichas/` | las fichas por id |
| `RESUMEN.md` | recuento y lo mejor |
| `A_REHACER.md` | ya resuelto |
| `NO_VISTOS.md` | lo que no se ha visto |
| `familias.json` | las 270 familias |
| `hojas/` | las hojas usadas para revisar |
| `audio_medido.json` | los 658 sonidos medidos |
| `plantillas_leidas.json` | las 55 plantillas leídas por dentro |
| `recortes_mejorados.json` | el registro de los 849 recortes mejorados |
| `recortes_mejorados_antes_despues.jpg` | muestra de los recortes mejorados |

**Cómo se rehace el índice, en este orden:**
1. `python3 tools/atlas/construir_indice.py` (aplica `indice/correcciones.json` y `revision/recortes_mejorados.json`);
2. `python3 tools/atlas/revision_sin_vista.py`;
3. `python3 tools/atlas/revision_resumen.py --indice`.

El índice se reconstruye de forma reproducible.

---

## 8. Cómo se busca (lo más importante)

**Comandos** (en Windows, `python "C:\Users\ikerg\Biblioteca\TEXTURAS\tools\atlas\buscar.py" …`; en la sandbox,
`python3 tools/atlas/buscar.py …` desde el clon):

```
buscar.py --version                       → buscar.py v3
buscar.py --necesidades [palabra]         catálogo de las 78 necesidades (filtrable)
buscar.py --necesidad pieza_goteo         sus opciones + «HOJA YA HECHA: …\indice\necesidades_hojas\pieza_goteo.jpg»
buscar.py papel viejo calido --ver        búsqueda libre: abanico de 12 distintas + HOJA en Biblioteca\_busquedas\
buscar.py "goteo | chorreon | drip"       varias formas a la vez (cualquiera vale)
buscar.py mancha --papel pieza            por papel (fondo repetible, superposicion, pieza, relieve, transicion,
                                          mascara, elemento animado, superposicion animada, fondo animado, sonido, lut…)
buscar.py luz --fondo "sobre negro"       por fondo (transparente, sobre negro, sobre blanco, gris neutro, opaco)
buscar.py --papeles · --mapa              qué papeles hay / qué hay en toda la biblioteca
buscar.py goteo --resumen                 cuántos encajan por clase/sub y familia
buscar.py --familia NOMBRE · --familia-de ID · --parecidos ID · --ficha ID
buscar.py X --mas                         la siguiente tanda de 12 (misma semilla) · --semilla N repite · --fijo sin azar
buscar.py X --sin-usar                    solo lo que no usa ningún plugin
buscar.py X --min 4 --mejor --alfa --tileable --relleno --clase C --sub S --tipo T --pack P --excluir IDs
buscar.py X --donde 'w>=2000' --donde 'orient~vertical' --donde 'medidas.luminancia<0.3' --donde 'video.loop=True'
buscar.py X --estricto                    todas las palabras obligatorias (también color/tamaño)
buscar.py X --json · --lista · --explicar · -n 30
buscar.py --plugin cartelator --apuntar ID ID …    deja constancia en Biblioteca\_uso\cartelator.json
buscar.py X --plugin cartelator           marca lo tuyo y no lo penaliza
```

**Cómo ordena** (`tools/atlas/biblioteca.py`, una sola fuente de verdad):
1. **Entiende cómo se llama cada cosa.** Usa sinónimos (`indice/sinonimos.json`, 102 grupos y más de 560 palabras),
   alias de los plugins (`nombres.json`), inglés, plurales y género (raíces) y frases («cinta adhesiva», «fuga de
   luz»).
2. **Puntúa por campos de la ficha**, con más peso en lo que mejor describe:
   - qué es: 3;
   - papel/fondo: 2,2;
   - familia, clase y sub: 2,2;
   - uso: 2;
   - desc: 1,8;
   - estilo, color y material: 1,4;
   - y menos el resto.

   Las palabras raras pesan más (IDF).
3. **El objeto es obligatorio; los matices no.** El color, el tamaño, el estilo y la orientación solo suben la nota.
   «goteo rojo» trae goteos con los rojos primero, y si ninguno es rojo lo avisa (se recolorea).
4. **La nota multiplica, pero no decide sola** (hay más de 4.000 con nota 5).
   - Lo que el recurso dice evitar baja la nota.
   - Las partículas de relleno bajan salvo que se pidan.
   - Tutoriales, plantillas, LUT y sonidos solo salen si se piden.
5. **Lo que ya usa otro plugin baja un 15 %; lo bueno (nota ≥ 4) que nadie usa sube un 6 %.** Así se da vida al
   material sin usar.
6. **Abanico (MMR):**
   - una por «grupo» (la familia; en las familias de más de 24, familia + subcarpeta + primera palabra de qué es);
   - penaliza los parecidos (misma familia, mismo original, pHash cercano, mismo pack o colección);
   - azar con semilla (Gumbel τ = 0,25);
   - si hay de sobra que cumplen todo, solo esos;
   - las notas 1–2 solo entran si no hay bastantes de 3 o más.
7. **Esconde** lo marcado REHACER, lo sustituido, lo dudoso, las copias idénticas y las **fuentes ya procesadas**
   (`--todo` y `--fuentes` las enseñan).
8. **Hoja de miniaturas (`--ver`):**
   - 4 columnas, números iguales a los de la lista;
   - transparencias sobre damero;
   - los vídeos con su tira de fotogramas;
   - si no hay imagen propia, la hoja de su grupo (avisado).

**Necesidades** (el atajo que evita barrer la biblioteca):
- `indice/necesidades.json`: 78 necesidades en grupos:
  - FONDOS: 12;
  - SUPERPOSICIONES: 9;
  - RELIEVES: 4;
  - PIEZAS SUELTAS: 18;
  - TRAZOS: 8;
  - LUZ Y ELEMENTOS: 4;
  - VÍDEO: 15;
  - SONIDO: 7;
  - COLOR: 1.
- **70 se eligieron mirando una a una** (`revisada`: a ojo). Las 8 de sonido y LUT son automáticas, por subcategoría
  medida, porque no se pueden ver.
- Cada una trae `titulo`, `como` (cómo se usa), `consulta` (para buscar más), `ids` (5–16) y `hoja`
  (`TEXTURAS/indice/necesidades_hojas/<nombre>.jpg`).
- **Para ampliar o corregir:** editar `indice/necesidades_spec.json` (`consulta`, `f` con los filtros, `poner` con los
  ids fijados a mano y `cerrada: true`, `quitar`) y regenerar con `python3 tools/atlas/necesidades.py [nombres]`.
  Conviene `TEXTURAS_ROOT` apuntando a una Biblioteca con los originales y ACIDBITE, para que las hojas tengan
  miniatura.

**Las 78 necesidades** (nombre = clave para `--necesidad`):
- **Fondos:** papel_fondo_blanco, papel_fondo_calido, papel_fondo_kraft_carton, papel_fondo_pauta,
  papel_fondo_acuarela_grano, superficie_pared, superficie_piedra_hormigon, superficie_madera, superficie_metal_oxido,
  fondo_pintura_frotado, fondo_grunge, fondo_grafito_carbon.
- **Superposiciones:** sup_grunge_manchas, sup_fotocopia_semitono, sup_polvo_rayas, sup_aguada_tinta,
  sup_vidrio_plastico, sup_lluvia_gotas, sup_agua_causticas, sup_luz_fuga_bokeh, sup_visor_camara.
- **Relieves:** relieve_pliegues, relieve_arrugado, relieve_marcas, relieve_textura_material.
- **Piezas:** pieza_mancha_tinta, pieza_mancha_pincel, pieza_salpicadura, pieza_goteo, pieza_gotas_agua,
  pieza_cafe_cerco, pieza_humedad_moho, pieza_quemadura, pieza_borde_rasgado, pieza_borde_viejo, pieza_esquinas,
  pieza_cinta_adhesiva, pieza_pegatina_etiqueta, pieza_notas_papeles, pieza_fibras_pelos, pieza_huella,
  pieza_sello_tampon, pieza_adhesivo_residuo.
- **Trazos:** trazo_lapiz, trazo_carbon_cera, trazo_rotulador, trazo_boligrafo, trazo_pincel, trazo_acuarela_aguada,
  trazo_anotacion, trazo_cinta_estirable.
- **Luz y elementos:** elem_fuego, elem_chispas_pavesas, elem_humo, elem_burbujas.
- **Vídeo:** video_transicion_papel, video_transicion_tinta, video_transicion_quemado, video_transicion_luz,
  video_transicion_glitch, video_transicion_tela_formas, video_mascara_mate, video_pelicula_polvo, video_vhs_crt,
  video_papel_animado, video_humo_fuego, video_agua_tinta, video_marcadores, video_luz_elementos, video_fondo.
- **Sonido:** sonido_whoosh, sonido_papel, sonido_golpe, sonido_riser, sonido_glitch_analogico, sonido_fuego_quemado,
  sonido_ambiente.
- **Color:** lut_pelicula.

**Desde un script de construcción:**
```python
import sys; sys.path.insert(0, r'C:\Users\ikerg\Biblioteca\TEXTURAS\tools\atlas')
from biblioteca import Biblioteca
B = Biblioteca()                                    # carga el índice (~2 s)
for e in B.necesidad('pieza_goteo'): print(e['id'], B.ruta(e['id']))
r = B.buscar('papel viejo', n=8, semilla=7, papel='fondo repetible')   # semilla fija = build reproducible
B.familia('tile_papel'); B.parecidos(id); B.ficha(id); B.hoja(lista, 'nombre')
```

**Nunca** se elige abriendo carpetas, con `catalogo.json` o `CATALOGO.md` (son viejos: 1.678 recursos y nada de
ACIDBITE) ni leyendo el índice a mano y cogiendo los primeros. Era la causa de que todos los plugins repitieran lo
mismo.

---

## 9. Reglas de variedad (lo que Iker pide expresamente)

1. Para efectos de textura, papel, mancha, luz, polvo, transición y similares:
   - **6–12 variantes por efecto**;
   - de **al menos 3 familias**;
   - de más de una colección si las hay.

   El plugin las ofrece como variantes o elige entre ellas con semilla. Si un efecto solo lleva una, hay que
   explicarle a Iker por qué.
2. **Una por familia.** Se repite familia solo cuando ya se han cubierto las demás.
3. **ACIDBITE cuenta.** Si encaja y no se usa, se justifica.
4. **No copiar lo que «ya lo usa» otro plugin**, salvo que sea claramente lo mejor (y se dice).
5. Si Iker pide «otra» o «más variedad»: `--mas`, otras palabras u otra clase; nunca repetir la misma búsqueda.
6. La nota no desempata.
7. **Apuntar lo usado** (`--plugin X --apuntar ids`) y anotar en `uso_id.json` para qué se usa y con qué búsquedas.

---

## 10. Herramientas (scripts) y cómo regenerar

**`TEXTURAS/tools/atlas/`:**

| Script | Qué hace |
|---|---|
| `buscar.py` | El buscador (CLI v3). |
| `biblioteca.py` | La librería: `Biblioteca()`, `.buscar`, `.necesidad`, `.ruta`, `.familia`, `.parecidos`, `.hoja`, `.apuntar`. Cada recurso lleva `_papel`, `_fondo` y `_grupo`. |
| `necesidades.py` | Genera `necesidades.json` y sus hojas desde `necesidades_spec.json`. |
| `construir_indice.py` | Construye el índice. |
| `revision.py`, `revision_resumen.py`, `revision_sin_vista.py` | Fichas y resumen de la revisión. |
| `originales.py` | Manifiesto de los originales. |
| `tablas_plugins.py` | Tablas `uso_id.json`. |
| `nombres.py` | Nombres oficiales y alias. |
| `montar_biblioteca.py`, `montar_biblioteca.ps1`, `MONTAR_BIBLIOTECA.bat` | Montaje de la Biblioteca. |
| `medir_audio.py` | Medición de los sonidos. |
| `leer_plantillas.py` | Lectura de plantillas sin abrir el programa. |
| `hoja.py`, `hoja_piezas.py` | Hojas de contactos. |
| `mejorar_recorte.py` | `medir` y `arreglar`: desmezcla blanco/negro, cerco, suavizar, despill. |
| `quitar_tinte_croma.py` | Fibras teñidas por el croma → color del papel. |
| `metodo_bordes_matte_papelator.py` | Matte de croma de PAPELATOR. |
| `collage*.py` | Las 475 piezas de collage. |
| `producto_*.py`, `productos_amano.py` | Productos comunes. |
| `rehacer/` | burbuja, gota, goteo y tile (las 21 piezas rehechas). |
| `cruce_phash.py` | Cruce por pHash con AcidBite. |
| `gumroad_anadidos.py` | Material de Gumroad añadido. |

**`TEXTURAS/tools/` (pipeline TEXTURAS):** `inventario.py` → `clasificar.py` → `procesar.py` → `video_proc.py` →
`hojas_salida.py DEST DIR_HOJAS [prefijo]` → `construir_catalogo.py`. Detalle en `tools/README.md`.

**Añadir material nuevo:**
1. Meterlo en `Biblioteca\AÑADIDOS\` o en `TEXTURAS\_entrada\`.
2. Procesarlo.
3. Revisar las hojas.
4. Ficha en `revision`.
5. `construir_indice.py`.
6. Si encaja en una necesidad, añadirlo a `necesidades_spec.json` y regenerar.

**ACTUALIZAR_TEXTURAS.bat** (en la raíz de Biblioteca): hace `git pull --ff-only` de `TEXTURAS` y `buscar.py
--version`, y deja el log en `_ESTADO_ACTUALIZAR.txt`.

---

## 11. Productos comunes (hechos una vez para todos)

| Producto | Formato | Dónde |
|---|---|---|
| Cintas de trazo enderezadas (88, las de A mano) | PNG gris 8 bits, fila 0 = inicio + JSON | `productos/cintas_trazo` |
| Sellos de relieve (50 grumos) | PNG gris, 128 = neutro, luz arriba | `productos/sellos_relieve` |
| Piezas de NEONIZADOR (goteos, gotas, burbujas, fuego/chispas/pavesas/humo, moho, quemado, salpicaduras, fibras, polvo…) | PNG RGBA + medidas | `productos/piezas_neonizador/*` (21 rehechas: `REHECHAS.json`) |
| Papel gris 128 (relieves de papel) | PNG gris con `tile_mm` | `productos/papel_gris` |
| Mates de tinta 4K | máscaras de las transiciones de tinta | `productos/mates_tinta_4k` |
| Hojas de contactos de productos | JPG | `productos/hojas/` (`hoja_piezas.py`) |

Recetas por técnica: `TEXTURAS/tecnicas/` (collage_papel, fuego, goteos, look_analogico, look_pelicula,
mascara_track_matte, montaje_cortinilla_luz, montaje_por_estilo, papel_acabado, pintado_a_mano_damdam,
relieve_desplazamiento, sincronia_audio, trazo_cintas). Cómo usa ACIDBITE su material:
`acidbite/COMO_LO_USA_ACIDBITE.md`. Packs de Gumroad (Studio DamDam): `gumroad/ESTADO.md`.

---

## 12. Recortes mejorados (20-11-2026)

**849 recortes `tx:`** rehechos y sustituidos en su sitio (mismo nombre, tamaño y caja):

| Qué | Cuántos | Qué se arregló |
|---|---:|---|
| Goteos (`manchas/goteos` y piezas de NEONIZADOR) | 452 | sin línea oscura en el contorno y con los escalones suavizados |
| Salpicaduras de tinta y de óxido/café | 248 | sin cerco claro |
| Fibras | 65 | sin cerco claro |
| Trazos | 38 | sin cerco claro |
| Bordes rehechos con el matte de PAPELATOR | 18 | sin velo ni bandas de croma en el fondo |
| Bordes de papel blanco o gris con fibras teñidas | 29 | las fibras vuelven al color del papel |

Detalles del registro:
- Están en `revision/recortes_mejorados.json`, y en el índice cada uno lleva `recorte_mejorado`.
- Los anteriores siguen en el historial de git.
- **Ningún plugin lee esos `tx:`** (leen sus `or:` exactos), así que ningún resultado cambió.

**Se dejaron como estaban, a propósito, porque el arreglo los empeoraba:**
- gotas, burbujas, fuego y chispas (el alfa es la propia luz);
- moho (salían motas negras);
- quemado, café y foxing (se volvían rosados);
- collage (los brillos y cantos son del material);
- lápiz, cera y gouache;
- bordes de cartón marrón y de papel azul.

Para mejorarlos habría que rehacerlos uno a uno desde la foto original con otro método.

---

## 13. Revisión 100 % a ojo (noche del 19 al 20-11-2026)

- **Cobertura:** 9.031 recursos.
  - 8.318 vistos a ojo, con hojas de contactos (imagen entera + recorte 1:1; los vídeos, con tira de 12 fotogramas +
    1:1).
  - 713 sin vista: 658 sonidos y 55 plantillas.
- **Lo que se resolvió después:**
  - 86 dudosos;
  - 92 correcciones;
  - 21 piezas rehechas;
  - 658 sonidos medidos;
  - 55 plantillas leídas por dentro;
  - 384 chispas y pavesas → `rol: relleno de fondo`.
- **Estado final:** «rehacer 0 · correcciones 0 · dudosos 0 · no recomendados 540 · sensibles 25».
  - Los sensibles son, por ejemplo, recortes de ojos de una persona real en Super Mixed Media: no usarlos si no se
    quiere un rostro real.

---

## 14. Los plugins

**Fichas** (escritas por cada plugin el 19-11, sin cambiar código): `TEXTURAS/plugins/<plugin>.md`. Tablas
`nombre interno → id`: `plugins/<plugin>/uso_id.json`. Conciliación: `plugins/CONCILIACION.md`. Pasos de migración:
`plugins/MENSAJES.md`.

| Plugin | Cómo lleva las texturas | Prueba exacta | Notas |
|---|---|---|---|
| NEONIZADOR (Photoshop, UXP 1.0.7) | 287 `.bin` (L/LA/RGB/RGBA) + `index.json` en `plugin/tex/`; 143 usados | sha256 `index.json` `3db2fb598471d78e`; `.bin` concatenados `3be83b02c7c0874e`; `refhash.js`, `golden.js`, `uxptest.js` (49 efectos × 3 intensidades) | lee los `or:` heredados (idénticos); `main` no se toca; repo privado (lleva Gumroad) |
| NEONIZADOR vídeo (AE, CEP 2.6.0) | los mismos `.bin` en el panel | sha256 `index.json` y `.bin`; 49 huellas a 0,6 | WebGL2; la GPU varía por tarjeta: la referencia son los `.bin` y las huellas CPU |
| PAPELATOR | 822 PNG 8 bits + 6 JSON en `plugin/assets/` (escala física en mm, luz relativa 128) | `verificar_assets.py` → 0 distintos; md5 de los 6 JSON; 60 renders deterministas | `imperf.json` tiene ajustes a mano (no regenerar); `build_grids.py` no es reproducible |
| A mano | base64 en `main.js`: 88 cintas, 50 sellos, grano sintético | los dos módulos generados byte a byte | publica cintas y sellos en `productos/` |
| Analog FX (0.9.21) | `.bin` en `plugin/textures/` + `drips.bin` | ficha §6 | Iker aún no ha decidido si adopta los tileables nuevos (por defecto, idéntico); JS puro, candidato a GPU |
| Trazo (1.13.0) | 20 `.bin` TRZ1 | md5 de los 20 `.bin` + renders `tools/run.js` | verificar primero que el build se reproduce; `pin_gouache` = óleo |
| Cartelator (3.7.1) | **no usa texturas** (vectorial) | sha256 del `main.js` empaquetado | la parte A vale para lo nuevo |
| Plugins nuevos | — | — | buscan con la ORDEN 3 |

**Órdenes enviadas** (Iker las pega en cada conversación de plugin):
1. **ORDEN 1**, `plugins/ORDEN_PLUGINS.md`:
   - biblioteca única;
   - método de búsqueda (ya en v3);
   - autorrevisión de velocidad y GPU;
   - REGLAS PERMANENTES que cada plugin copia a su `CLAUDE.md`.
2. **ORDEN 2**, `plugins/ORDEN_CARPETA_LOCAL.md`:
   - dejar GitHub;
   - clonar todo con ramas y etiquetas en `Biblioteca\plugins\<plugin>`;
   - `.bundle` en `plugins\_respaldos`;
   - verificar uno a uno;
   - sin repetidos;
   - solo la carpeta Biblioteca;
   - Iker borra los repos tras el informe VERIFICADO.
3. **ORDEN 3**, `plugins/ORDEN_BUSCAR.md` (enviada como `ORDEN_3_BIBLIOTECA.md`):
   - mejoras (buscador v3, necesidades, recortes, fichas);
   - actualizar y comprobar v3;
   - cambiar la línea de búsqueda en su `CLAUDE.md`;
   - usar el método nuevo en todo lo nuevo;
   - repasar lo que ya tienen y proponer variedad sin cambiar resultados sin el sí;
   - apuntar lo usado;
   - informe con tabla por efecto y PEDIDOS.

**Texto corto para pegar** a un plugin (con rutas completas):
```
Orden de Iker, permanente. Lee entero y cumple, en este orden, este archivo:
C:\Users\ikerg\Biblioteca\TEXTURAS\plugins\ORDEN_BUSCAR.md
Antes: ejecuta C:\Users\ikerg\Biblioteca\ACTUALIZAR_TEXTURAS.bat (o git -C "C:\Users\ikerg\Biblioteca\TEXTURAS" pull --ff-only)
y comprueba: python "C:\Users\ikerg\Biblioteca\TEXTURAS\tools\atlas\buscar.py" --version  → v3
Lee entero el método: C:\Users\ikerg\Biblioteca\CLAUDE.md
Para buscar, empieza SIEMPRE por: python "C:\Users\ikerg\Biblioteca\TEXTURAS\tools\atlas\buscar.py" --necesidades
(hojas ya hechas en C:\Users\ikerg\Biblioteca\TEXTURAS\indice\necesidades_hojas\)
Si no está: buscar.py PALABRAS --ver (hoja en C:\Users\ikerg\Biblioteca\_busquedas\)
Apunta lo que uses: buscar.py --plugin TU_PLUGIN --apuntar ID ID ...
Termina con el informe que pide la orden. No cambies ningún resultado ya entregado sin mi sí.
```

**Uso registrado** a 20-11, en `Biblioteca\_uso\`:
- `neonizador.json` (15:57);
- `papelator-video.json` (15:37).

Además había 6 hojas en `_busquedas` (goteo, chorreón, cerco de café, mancha de agua, acuarela, aguada). Todo eso es de
la ORDEN 3 en su versión v2; tras la v3 aún no había nada nuevo.

---

## 15. Pedidos («PEDIDO PARA LA BIBLIOTECA»)

- **Qué son.** Cuando un plugin no encuentra algo, no lo dibuja ni lo descarga: termina su respuesta con un bloque
  «PEDIDO PARA LA BIBLIOTECA:», que dice qué le falta, para qué, el formato, el tamaño y el modo.
- **Dónde están.** Se quedan en la conversación de cada plugin. Esta conversación no los ve: Iker los copia aquí,
  indicando de qué plugin es cada uno.
- **Cómo se resuelven:**
  1. Comprobar si de verdad falta (con `buscar.py`, `--necesidades` y varias formulaciones). Si ya está, contestar
     con los ids exactos y la hoja.
  2. Si falta, sacarlo de lo existente: originales, ACIDBITE (extraer fotogramas, recortar del Toolkit…), productos.
  3. Procesarlo con el formato pedido, revisarlo a ojo, darle ficha e id y meterlo en el índice. Si encaja, añadirlo a
     una necesidad.
  4. Darle a Iker el texto de respuesta para el plugin: ids, rutas, modo, cómo usarlo.
- **A 23-11 no ha llegado ninguno todavía.** Los huecos que ya se sabe que faltan están en el apartado 5.

---

## 16. Historial de lo hecho (cronología)

**19-11-2026:**
- Atlas unificado (TEXTURAS + AcidBite + originales) con `DECISIONES.md`.
- Montaje de la Biblioteca en el PC (`MONTAR_BIBLIOTECA.bat`): AcidBite movido de
  `Downloads\ADIDBITE\BIBLIOTECA` a `Biblioteca\ACIDBITE`, clones, 2.191 originales copiados y verificados por md5.
- Gumroad: 132 originales nuevos (21 mates, ProRes, Cianotipia, SlitScan) y producto `mates_tinta_4k`.
- Collage: 475 piezas recortadas (opacos, translúcidos, grafito) con sombras aparte.
- Revisión 100 % a ojo (774 lotes) durante la noche.

**20-11-2026:**
- **Mañana:**
  - cierre de la revisión;
  - 21 piezas rehechas;
  - ORDEN 1 (con hardware y método de búsqueda);
  - buscador con fichas (`--resumen`, `--parecidos`, `--donde`…);
  - 86 dudosos y 92 correcciones;
  - 658 sonidos medidos;
  - 55 plantillas leídas;
  - chispas como relleno;
  - ORDEN 2.
- **13:48 a 14:35:** recortes mejorados (849).
- **14:42:** Iker avisa de que los plugins repiten siempre lo mismo.
  - Buscador v2: relevancia, sinónimos, abanico y miniaturas.
  - `Biblioteca/CLAUDE.md` y `ACTUALIZAR_TEXTURAS.bat`.
  - ORDEN 3.
- **16:52:** Iker pide darle una vuelta completa → v3:
  - librería `biblioteca.py`;
  - papel y fondo de cada recurso;
  - 78 necesidades (70 elegidas a ojo una a una con hojas de 32 candidatos);
  - sugerencias de necesidades al buscar;
  - lo bueno sin usar sube;
  - miniaturas de vídeo con tira;
  - `"a | b | c"`;
  - `--sin-usar`.
- **17:38:** el PC de Iker actualizado a v3 (comprobado en su pantalla).

**23-11-2026:** este documento.

Commits clave en `atlas`:

| Commit | Qué |
|---|---|
| `c1accec` | recortes (1) |
| `2d247e3`, `68be530`, `0173eef` | recortes |
| `5cb39fa` | buscador v2 |
| `71097e5` | ORDEN 3 |
| `163c8b0` | v3 y necesidades |
| `b1740d0` | sin `__pycache__` |

---

## 17. Estado actual y pendientes

**Hecho y funcionando:**
- índice con 9.031 recursos y ficha;
- buscador v3;
- 78 necesidades;
- instrucción de la raíz;
- recortes mejorados;
- PC actualizado.

**Pendiente:**
1. **Informes y PEDIDOS de los plugins** tras la ORDEN 3. Esperarlos, resolver los pedidos (apartado 15) y revisar
   que cada plugin aplica la variedad (6–12 por efecto, al menos 3 familias, ACIDBITE).
2. **ORDEN 2:** confirmar los informes VERIFICADO de cada plugin antes de que Iker borre los repos de GitHub.
3. **Decisiones de Iker** (`DECISIONES.md` §14):
   - sincronizar la Biblioteca entre sus 2–3 ordenadores;
   - fusionar `atlas` en `main` de TEXTURAS;
   - si Analog FX adopta los tileables nuevos.
4. **Ampliar el catálogo de necesidades** con lo que pidan los plugins (editar `necesidades_spec.json` y regenerar).
5. **Recursos buenos poco visibles.** Unos 970 de los 5.281 buenos (nota ≥ 4) no salen nunca entre los 12 primeros de
   una búsqueda libre: son variantes casi iguales de chispas, goteos y vídeos de ACIDBITE. Se llega a ellos con
   `--familia`, `--mas` y `--sin-usar`. Se puede mejorar con más necesidades o etiquetas propias.
6. **Sonidos sin escuchar** (solo medidos) y **plantillas sin abrir** (solo leídas): hay que comprobarlos antes de
   usarlos.
7. **Recortes que no se pudieron mejorar con el método automático** (apartado 12): habría que rehacerlos a mano desde
   la foto.
8. **Huecos de material** (apartado 5).
9. `catalogo.json` y `CATALOGO.md` siguen siendo los de TEXTURAS antiguos (1.678): solo para procesar. No se borran.

---

## 18. Cómo trabaja Claude aquí

**Repo en la sandbox:**
- `/home/claude/texturas` (clon de `atlas`).
- Si no está: `add_repo` (owner `IkerEker`, repo `TEXTURAS`, acceso `push`) y
  `git clone --depth 1 --branch atlas --filter=blob:none https://github.com/IkerEker/TEXTURAS.git`.
- Pesa unos 3,5 GB; `--sparse` si solo hacen falta carpetas.
- Push: `git push -q origin atlas`. GitHub avisa «repository moved» (mayúsculas); funciona igual. Lotes de menos de
  ~500 MB.

**Commits:**
- Mensaje en español.
- Terminan con:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01VPHAR9QioEyKrt81wNbmE6
  ```
  (la URL de la sesión cambia con cada conversación).

**Puente al PC de Iker** (herramientas `mcp__remote-devices__*`):

| Herramienta | Para qué | Límites |
|---|---|---|
| `device_list_dir` | listar carpetas | — |
| `device_stage_files` | traer archivos a `/mnt/user-data/uploads/Biblioteca/...` | ≤ 50 archivos y ≤ 500 MB por llamada |
| `device_commit_files` | escribir en el PC desde `/mnt/user-data/outputs/...` | `force: true` para sobrescribir |

Más reglas del puente:
- No hay terminal en el PC: lo que Iker tenga que ejecutar va en un `.bat` y se lo dice.
- Borrar del sandbox lo traído después de usarlo, porque el disco es corto.
- Los originales de un `tx:` se encuentran con `A[A[id]['origen']]['archivo']`.
- Para que las hojas tengan miniatura de `or:` y `ab:`, se traen esos archivos y se ejecuta con
  `TEXTURAS_ROOT=/mnt/user-data/uploads/Biblioteca`.

**Cómo comunicarse con Iker:**
- Español y frases cortas.
- Descargables listos para pegar, con rutas completas de Windows.
- Decir lo que no se ha podido hacer.
- No preguntar lo que se puede decidir solo («haz todo lo que puedas tú solo»).
- Mirar siempre las hojas antes de dar algo por bueno.

**Áreas de trabajo de la sandbox** (temporales, no están en el repo):
- `/home/claude/recortes/` (registro de los recortes: `registro.json`, `antes/`);
- `/home/claude/vida/` (candidatos de las necesidades: `candidatos.json`, `elegir.py`, `candidatos.py`);
- `/home/claude/pend/fx.py` (editar fichas).

Si se pierden, lo esencial ya está en el repo.

---

## 19. Documentos de referencia

| Documento | Qué tiene |
|---|---|
| `Biblioteca\CLAUDE.md` (= `TEXTURAS/biblioteca_raiz/CLAUDE.md`) | método de búsqueda y reglas de variedad para cualquier conversación |
| `TEXTURAS/MAPA.md` | puerta de entrada: dónde está cada cosa |
| `TEXTURAS/CLAUDE.md` | guía de la parte TEXTURAS (formatos, carpetas, pipeline) |
| `TEXTURAS/DECISIONES.md` | por qué está organizado así (ids, originales, vídeo, audio, GPU, nombres, huecos, preguntas abiertas) |
| `TEXTURAS/TRASPASO.md` | traspaso antiguo (19-11) entre TEXTURAS y AcidBite |
| `TEXTURAS/indice/ESQUEMA.md` | campos del índice |
| `TEXTURAS/revision/RESUMEN.md` | la revisión a ojo en números |
| `TEXTURAS/plugins/*.md`, `CONCILIACION.md`, `MENSAJES.md`, `ORDEN_*.md` | plugins |
| `TEXTURAS/tecnicas/*.md` | recetas de uso |
| `TEXTURAS/acidbite/COMO_LO_USA_ACIDBITE.md`, `acidbite/ESTADO.md` | ACIDBITE |
| `TEXTURAS/gumroad/ESTADO.md` | packs de Gumroad (Studio DamDam) |
| `TEXTURAS/productos/README.md` | productos comunes |
| `TEXTURAS/collage/README.md` | las 475 piezas de collage |
| `TEXTURAS/tools/README.md` | pipeline TEXTURAS |
