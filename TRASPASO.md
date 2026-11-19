# TRASPASO · de la conversación TEXTURAS a la conversación AcidBite

Escrito el 19-11-2026 por la conversación que construyó TEXTURAS. Va dirigido a la conversación que analiza el pack
**AcidBite**. A partir de ahora esa conversación sigue el trabajo de las dos.

Todo lo que sabe la conversación TEXTURAS está **en este repositorio**: no queda nada solo en su memoria. Su carpeta de
trabajo, que no se puede ver desde fuera, está copiada en `tools/estado/`.

**Orden de lectura** (unos 20 minutos, sin saltarse nada):
1. Este documento entero.
2. `CLAUDE.md`, la guía de uso de la biblioteca.
3. `plugins/README.md` y `plugins/CONCILIACION.md`.
4. Las 7 fichas de `plugins/*.md`, al menos los apartados 0/Resumen, 3, 5 y 6 de cada una. Son largas porque son
   exactas; los anexos JSON tienen el detalle archivo por archivo.
5. `tools/README.md` y, por encima, `tools/tx.py`.
6. Mirar 3 o 4 hojas de `hojas/` con Read, para ver la calidad real.

---

## 1. Qué quiere Iker (sus requisitos, tal cual los ha pedido)

- Hace **muchos plugins de Photoshop** (UXP; y NEONIZADOR también para After Effects), cada uno con su repo y con
  muchas texturas repetidas entre ellos. Quiere **una base común**:
  - deduplicada;
  - **procesada**: limpia, recortada, separada por piezas, con los fondos quitados a los trazos;
  - **entendida**: para qué sirve cada cosa y cómo se usa;
  - que Claude encuentre **rapidísimo** desde cualquier conversación de plugin.
- **Vídeos analizados uno a uno:** qué son, fps, velocidad, si empiezan en negro y el efecto aparece, si cubren y
  descubren, si hacen loop.
- **Decidir qué es tileable y qué no**, apoyándose en cómo lo usan ya los plugins.
- «Complementa, mejora, retoca… TODO. Piensa cómo hacerlo aún mejor.» Quiere que se dedique mucho tiempo y que se haga
  bien.
- **Ultra atlas.** Juntar TEXTURAS + AcidBite (~190 GB, pagado) + texturas que se generen en el futuro. Debe decir cómo
  usar cada asset: superposiciones, mapas de desplazamiento, sincronía con audio, combinaciones, tutoriales del pack.
  Claude tiene que saber al instante dónde está cada cosa, para qué sirve y cómo se usa.
- **Los plugins son solo para él.** Todo el material es suyo (pagado). Repos **privados**. No redistribuir lo de
  Gumroad.
- **Los plugins tienen que funcionar 100 % solos en su ordenador**, sin Claude y sin internet. Esto no se negocia.
- Puede trabajar desde **2 o 3 ordenadores**. Trabaja con **2 gráficas** potentes (GPU): todo lo pesado debe poder
  ir por GPU.
- Decisiones ya tomadas:
  - TEXTURAS es privado.
  - Se guarda **solo lo procesado**, con puntero al original.
  - **ESTILO** (dataset de ilustración) se queda fuera.
  - Las referencias de Cartelator son carteles de terceros: **no son fuentes**.
- **Flujo acordado:**
  1. Cada plugin ha entregado su ficha. Ya están las 7.
  2. Esta conversación y la de AcidBite se juntan.
  3. Pasada unificada.
  4. Repo/biblioteca definitiva.
  5. **Un mensaje por plugin** para que su conversación empiece a construir desde la biblioteca común: «todos bebiendo
     del mismo sitio».

---

## 2. Qué hay hecho: el repo TEXTURAS

`https://github.com/IkerEker/TEXTURAS` (privado, rama `main`, ≈ 5 GB). Contenido:

- **1.678 fichas.** De 4.304 archivos de origen (9,4 GB) salieron 1.235 imágenes únicas y 57 vídeos, más los `_trama`
  y los `_loop`.
- `catalogo.json` (`items[]`, más `omitidos`) y `CATALOGO.md`: una ficha por archivo. Los campos están en `CLAUDE.md`:
  - `desc`, `color`, `modo`, `alfa`;
  - `tileable`, `costura`, `mm_por_px`, `tile_mm`, `aviso`;
  - `recorte`, `piezas`;
  - `origen` (repo, ruta, sha1, copias);
  - `usado_en`;
  - en vídeo: `fps_efectivo`, `transicion`, `loop`…
- `hojas/<carpeta>.jpg`: hojas de contactos.
- Carpetas: `tileables/` 416 · `trazos/` 287 · `manchas/` 258 (incluye el banco de 219 goteos) · `imperfecciones/` 167 ·
  `bordes/` 155 · `luz_y_elementos/` 148 · `superposiciones/` 114 · `pliegues/` 76 · `video/` 57 (+10 `_loop`, `_tiras`).
- `tools/`: procesado reproducible (ver `tools/README.md`). `tx.py` contiene los métodos:
  - `from_paper`: alfa de cobertura y color descontaminado;
  - `from_black`: «unmultiply»;
  - `from_black_cover`;
  - `from_chroma`: alfa exacta, despill y color del núcleo opaco;
  - `split_pieces`;
  - `make_tileable`: corte de costura óptimo en altas frecuencias y fundido de las bajas;
  - `make_tileable_periodic`: número entero de periodos, para cuadrículas y aparejos;
  - `relief_gray` y `fold_shading`: 50 % = neutro;
  - `flatten_light`.
- `plugins/`: las 7 fichas de los plugins, sus anexos, `README.md` (tabla resumen) y `CONCILIACION.md` (hallazgos).
- `tools/estado/`: datos de trabajo:
  - `inv2.json`: inventario de los 4.304 archivos con roles fuente/procesado/referencia/ruido, duplicados y hashes
    perceptivos;
  - `clasif.json`: qué método se aplicó a cada fuente;
  - `md5_inventario.json`;
  - `videos_cat.json`;
  - `res_fichas.tgz`: las fichas por fuente;
  - `nz_match.json` y `nz_mapa.json`: cada archivo de la BIBLIOTECA de NEONIZADOR, con su original.

**Lo que NO está en TEXTURAS:** los originales. Siguen en los repos de los plugins (`origen.repo` / `origen.ruta` de
cada ficha). Ver §5: hay que crear `originales/`.

**Limitaciones conocidas de lo hecho:**
- 13 tileables llevan `aviso`: plásticos arrugados y cáusticas con la costura visible.
- La costura numérica no sirve para cuadrículas; se revisaron a ojo.
- El procesado se hizo sin GPU (la sandbox no tiene).
- Los trazos curvos no se enderezan; en TEXTURAS solo están recortados.

---

## 3. Fuentes: los repos de los plugins

| Plugin | Repo (todos de `IkerEker`, privados) | Rama / commit analizado | Fuentes |
|---|---|---|---|
| NEONIZADOR | `neonizador` (GitHub dice que se ha movido a `NEONIZADOR`) | **`biblioteca-texturas`** f7afed1 (`main` está desfasada) | `BIBLIOTECA/` 2.439 archivos, 1,7 GB |
| Analog FX | `analog-fx-plugin` | `main` | `textures-src/` 1,1 GB, `Tintas impresas/`, `GOTAS/`, `BIBLIOTECA/goteos/` |
| PAPELATOR | `papelator` (`PAPELATOR`) | `main` ac22119 | 784 fotos, 1,82 GB |
| A mano | `a-mano` | `main` | `TRAZOS/` 80 (= `APOYO/TRAZOS/` de PAPELATOR), `referencias/texturas/` 4 |
| Trazo | `trazo` | `main` 83aed67 (código de d8867fe) | `TEXTURES/` 319 archivos, 1,3 GB |
| Cartelator | **sin repo** (solo en su conversación y en un zip del 5-11-2026). Se le recomendó crear uno privado | — | no tiene texturas |
| ESTILO | `ESTILO` | — | fuera, por decisión de Iker |

Comprobado: **todas las fuentes de los 7 plugins están ya en TEXTURAS.**
- PAPELATOR, A mano y Trazo: md5 o hash de git idénticos.
- NEONIZADOR: su BIBLIOTECA son las mismas fotos re-guardadas en JPG y renombradas, más recortes de esas fotos (ver
  `plugins/CONCILIACION.md`).

---

## 4. Lo que dicen las 7 fichas (resumen; el detalle está en cada `plugins/*.md`)

**Patrón común:**
- Cada plugin construye con Python sus **propios binarios** a partir de fotos y los mete en el `.ccx`.
- En ejecución lee solo de su carpeta (UXP `getPluginFolder`) o de módulos base64.
- **La biblioteca alimenta la construcción, nunca la ejecución.**
- Todos son deterministas y traen una **prueba exacta**.
- Todos piden lo mismo:
  - originales intactos (md5);
  - id estable;
  - orden fijo;
  - duplicados conservados cuando se usan dos veces;
  - escala real;
  - fondo;
  - tileable;
  - etiquetas.
- El formato final y los parámetros prefieren seguir haciéndolos ellos.

| Plugin | Formato en el `.ccx` | Prueba exacta | Qué pide a la biblioteca | Trampas / notas |
|---|---|---|---|---|
| **A mano** | base64 de 8 bits en `js/texdata.js` (88 cintas de trazo) y `js/grumosdata.js` (50 sellos de grumo); grano de papel sintético | md5 `texdata.js` 182e0cdb…, `grumosdata.js` d3ca0cf2…; huellas de render por preset | originales intactos + id + familia + **inicio del trazo** (top/left); producto común «cintas enderezadas» y «sellos de relieve» | orden de `SOURCES` y duplicados de CERAS/GUACHE cuentan; extractor solo de trazos rectos |
| **Cartelator** | **no usa texturas** | sha256 de `main.js` 4cdf9021… | nada hoy; en el futuro: bordes rasgados, tinta de grabado / sello de caucho, borde de brocha seca, grano con px/mm | sus `referencias/` son carteles ajenos; los iconos no son texturas |
| **Analog FX** | `.bin` gris 8 bits en `plugin/textures/` + `textures.json`; `drips/drips.bin` | md5 de assets + renders `.ppm`; tolerancia PSNR ≥ 40 dB si cambian fuentes | originales con `tono`/`polaridad`, tileables cuadrados, escala física, gotas RGBA clasificadas (ya las produce `build_drips.py`) | **solo carga la `_1` de cada familia** (salvo `desgaste` y `tinta`); `goteo` y `gubia` no se usan |
| **NEONIZADOR** | 287 `.bin` crudos L/LA/RGB/RGBA + `index.json` con `meta` (goteos, llamas, atlas) | md5/sha256 de `plugin/tex`; `golden.js` + `huellas.json`; 49 hashes a intensidad 0,6 | tabla `nombre_plugin → id`; recortes RGBA con medidas (llamas `lean`/`base_x`, goteos `ax`/`sw`/`bw`/`len`/`wob`); tiles reales | `ELEMENTS` elige «los N PNG más pesados»; el orden de las familias `gt_`/`fg_`/`bf_`/`mo_` decide el azar; 147 texturas empaquetadas sin uso (~90 MB); sus `.bin` salen de JPG re-guardados, no de los originales |
| **PAPELATOR** | 822 PNG 8 bits + 6 JSON en `plugin/assets/` (codificaciones `_d`, `_c`, `_ink`, `_r`, `_n`, `_m`, `_k`, `_f`) | md5 de píxeles de los 822 PNG (en su anexo) + md5 de los 6 JSON + 60 renders | **`ancho_real_mm`** (lo más importante), fondo, tileable, orden, duplicados usados dos veces | `imperf.json` lleva ajustes a mano; `build_grids.py` no es reproducible y se ejecuta al importarlo; `imperf_tune.py` no es idempotente; la lluvia depende del nombre del archivo |
| **Trazo** | 20 `.bin` TRZ1 (cabecera JSON + planos uint8) | md5 de los `.bin` (reproducibilidad **sin verificar**) + `tools/run.js` con semilla | medio, tipo, tileable, temperatura, `q` 1–3, tags de forma, `px_por_mm`, md5; trazos sueltos limpios con máscara; fondos de papel limpios | `pin_gouache` (óleo) ≠ `pin_guache` (gouache); ~3,7 MB sin uso |

**Huecos (lo que piden y no existe en ningún sitio):**

- **Papel:**
  - papeles reales escaneados **sin trazos**, con escala y relieve (luz rasante y plana);
  - papel negro;
  - calco, carbón, térmico, couché, seda, sobres.
- **Bordes:**
  - **bordes quemados** reales (PAPELATOR la quitó por fea);
  - cartón visto en planta;
  - más orejas en papel grueso.
- **Moho real:** las colonias de NEONIZADOR le sirven a PAPELATOR.
- **Pliegues** de 7 u 8 veces y hoja enrollada.
- **Objetos y marcas:**
  - perforadora, chincheta, cinta adhesiva entera;
  - sello de goma / tampón;
  - rodillo / brayer;
  - bordes de cinta o plantilla;
  - arañazos sobre tinta.
- **Fibras y tóner:**
  - fibras de celulosa sueltas;
  - tóner y polvo de fotocopia reales.
- **Técnicas de dibujo y pintura:**
  - tiza y pastel;
  - óleo con empaste y espátula;
  - grafito por durezas (2H…8B);
  - rotulador y boli largos y limpios;
  - más brocha;
  - grumos grandes con luz rasante;
  - spray real sobre pared;
  - floraciones y frentes de secado de acuarela recortados.
- **Fuego, humo y agua:**
  - vídeos de fuego y humo sobre negro con alfa (After Effects);
  - más humo y vapor;
  - gotas sobre cristal;
  - cáusticas en vídeo.
- **Otros:**
  - tubos de neón;
  - máscara de fósforo y nieve analógica;
  - imagen térmica;
  - corcho, pizarra, lienzo, madera pintada, madera de grabado;
  - plástico mate;
  - polvo de cristal de escáner.

**AcidBite puede cubrir parte de esto:** hay que cruzar esta lista con su contenido.

---

## 5. Arquitectura propuesta (pendiente de combinar con las conclusiones de AcidBite)

> Esto es la propuesta de la conversación TEXTURAS. **AcidBite ha llegado a sus propias conclusiones tras mucho
> trabajo: no hay que pisarlas.** Ver §6, cómo combinar.

1. **`Biblioteca/` local** en cada ordenador de Iker. El mismo árbol en los 2 o 3 equipos (sincronizado con disco
   externo, NAS o rsync; nunca en GitHub por tamaño):
   - `TEXTURAS/`: clon de este repo.
   - `ACIDBITE/`: el pack, ~190 GB, tal cual o procesado.
   - `originales/`: los originales de todos los plugins, deduplicados por md5, intactos (sin recomprimir) y con su ruta
     antigua anotada. Es imprescindible para que A mano, Analog FX, PAPELATOR y Trazo reconstruyan **bit a bit**. Para
     NEONIZADOR, además, `originales/heredado/neonizador/` con sus ~715 JPG re-guardados (182 MB) o aceptar el cambio.
   - `generadas/`: las texturas que se generen en el futuro.
2. **Índice único**, en un repo privado pequeño (o en TEXTURAS): JSON con rutas **relativas** a `Biblioteca/`. Por cada
   asset:
   - id estable, md5, w/h;
   - categoría/subtipo por contenido, fondo, tileable;
   - `ancho_real_mm` / `px_por_mm`, medio, temperatura, `q`, tags de forma;
   - orientación (inicio del trazo, raíz del goteo);
   - modo de fusión;
   - origen, duplicados;
   - `usado_por`: plugin → nombre interno.
   - En vídeo, además: fps, transición, loop, audio. En AcidBite: tutoriales, desplazamiento, sincronía con audio.
3. **Capas del atlas:**
   - `tecnicas/`: una receta por técnica (cómo se consigue un efecto combinando assets; aquí entra lo aprendido de los
     plugins y de los tutoriales de AcidBite).
   - fichas por asset.
   - `conjuntos`: piezas que van juntas.
   - `MAPA.md`: la puerta de entrada para Claude.
   - una tabla por plugin `uso → id`.
4. **Productos comunes nuevos**, pedidos por varios plugins:
   - **cintas de trazo enderezadas**: formato de A mano y de Trazo;
   - **sellos de relieve**: los 50 grumos de A mano y las 4 fotos de `a-mano/referencias/texturas/`;
   - **piezas sueltas finas** de NEONIZADOR: pavesas, chispas, salpicaduras, gotas de agua, polvo, fibras, pompas,
     tiles de espuma y moho, llamas y goteos con medidas, tras revisarlas a ojo frente a las de TEXTURAS;
   - alfa de croma con el método `bordes_matte` de PAPELATOR;
   - papeles tileables a escala real en gris 128 = neutro.
5. **Tabla de nombres oficiales**, por contenido:
   - `boli` → `boligrafo`, `rotu` → `rotulador`, `guache` → `gouache`, `pincelfino` → `pincel_fino`;
   - evitar «organica» y «trazos» como familia genérica;
   - «sello» se separa en `sello_seco` (relieve notarial), `sello_tinta` (caucho) y `sello_brocha`;
   - `kraft` papel ≠ `carton_kraft`;
   - `cera` técnica ≠ `cera` de vela;
   - en el plugin cada uno conserva sus nombres y una tabla `id_común → nombre_plugin`.
6. **Regla de uso desde un plugin:** nunca meter la biblioteca entera. Las herramientas del plugin leen `Biblioteca/` por
   id con `TEXTURAS_ROOT` (variable de entorno o argumento), generan sus binarios de siempre y el `.ccx` sigue siendo
   autónomo.

---

## 6. Cómo combinar con lo que ya ha decidido AcidBite (sin perder nada de ninguna de las dos)

1. **Antes de tocar nada, escribir tu propio estado en este repo:** `acidbite/ESTADO.md`, con tus conclusiones,
   taxonomía, índice, scripts y decisiones, más tus datos en `acidbite/`. Así lo tuyo tampoco depende de la memoria de
   una conversación.
2. Hacer `DECISIONES.md` con una fila por decisión de diseño: la postura de TEXTURAS, la de AcidBite, la resolución y el
   porqué. Como mínimo:
   - taxonomía de carpetas y nombres;
   - esquema del índice (los campos de §5.2 y los de AcidBite);
   - dónde viven los archivos pesados;
   - vídeo y audio;
   - mapas de desplazamiento;
   - capas del atlas;
   - procesado en GPU;
   - formato de los productos comunes.

   Si chocan, elegir la que mejor sirva a los plugins, que son quienes consumen. Preguntar a Iker solo lo que de verdad
   sea suyo.
3. **Cruzar contenido:**
   - qué hay en AcidBite que ya esté en TEXTURAS: por hash perceptivo, con `tools/estado/inv2.json`, que trae `phash` y
     `dhash`;
   - qué huecos de §4 cubre AcidBite;
   - qué técnicas de sus tutoriales sirven a qué plugin.
4. Mantener los métodos buenos de las dos. No reprocesar lo que ya está bien sin comparar antes con hoja de contactos.

---

## 7. Plan de la pasada unificada (en orden)

1. Estado de AcidBite en el repo y `DECISIONES.md` (§6).
2. `originales/`: copiar desde los repos de los plugins las fuentes **usadas** (y las demás), deduplicadas por md5,
   intactas, con la tabla de rutas antiguas. Las listas exactas están en los anexos de las fichas y en `inv2.json`.
3. Índice único con los campos de §5.2. Rellenar desde lo que ya saben los plugins: escalas en mm de PAPELATOR
   (`extra.mm`, `TYPES`, `src_mm`, `CFG` de bordes), `q` y tags de Trazo, `inicio` de A mano, `tono`/`polaridad` de
   Analog FX y meta de NEONIZADOR.
4. Productos comunes (§5.4), revisados a ojo.
5. Tabla de nombres (§5.5) y tablas `uso → id` por plugin, generadas desde los anexos.
6. `MAPA.md`, `tecnicas/` y la actualización de `CLAUDE.md` y de la skill de búsqueda para que busquen en TEXTURAS y en
   AcidBite.
7. Mensajes a los plugins (§8).

---

## 8. El mensaje para cada plugin (lo que tendrá que dar esta conversación al final)

Uno por plugin, para pegar en su conversación. Cada uno debe llevar:

- **Qué ha cambiado:** a partir de ahora todos los plugins construyen desde la misma `Biblioteca/`. Dónde está, cómo se
  clona o sincroniza y la variable `TEXTURAS_ROOT`.
- **Su tabla `nombre_interno → id`**, completa y en el orden exacto.
- **Qué herramientas tocar**, y solo esas: las que lista su ficha en §5.1. El motor y el panel no se tocan.
- **Cómo comprobar que no cambia nada:** su propia prueba exacta, la de su ficha §6, con los valores de referencia. Si
  algo cambia, la tolerancia y qué hacer.
- **Qué deja de hacer:** borrar sus carpetas de fotos del repo cuando la prueba pase, dejar de extraer lo que la
  biblioteca ya da, y no crear bancos sueltos nunca más.
- **Qué gana:** productos comunes que le sirven, huecos cubiertos por AcidBite y peso muerto que puede quitar del `.ccx`.
- **Regla para el futuro:** si necesita una textura, primero la busca en la biblioteca; si no está, se añade allí (no
  en el plugin).
- **Recordatorio:** el plugin sigue 100 % autónomo.

Cosas concretas por plugin:
- **NEONIZADOR:**
  - trabajar en la rama `biblioteca-texturas`;
  - fijar `ELEMENTS`;
  - fuentes heredadas o aceptar el cambio;
  - puede quitar las 147 texturas sin uso conservando las familias completas.
- **PAPELATOR:**
  - no regenerar milimetrados ni imperfecciones;
  - conservar los 3 duplicados.
- **A mano:**
  - orden de `SOURCES`;
  - las cintas y grumos que publica pasan a ser producto común.
- **Analog FX:**
  - decidir si adopta los tileables nuevos (el resultado cambia un poco) o si sigue con los originales (resultado
    idéntico).
- **Trazo:**
  - primero verificar que su build actual se reproduce;
  - renombrar `pin_gouache` / `pin_guache` en la tabla.
- **Cartelator:**
  - crear su repo privado;
  - sin cambios por ahora.

---

## 9. Avisos técnicos del entorno de Claude

- **Acceso a los repos:** usar `add_repo` (owner `IkerEker`). Para TEXTURAS, con acceso de **escritura**. Clonar con
  `git clone --depth 1`, y con `--filter=blob:none --sparse` si solo hacen falta carpetas: TEXTURAS pesa ≈ 5 GB.
- **Subir cambios:** por lotes de menos de ~500 MB, con `git -c push.negotiate=true push`. GitHub avisa de que el repo
  «se ha movido» (mayúsculas); funciona igual.
- **Red de la sandbox:** solo GitHub y los registros de paquetes; pip puede estar bloqueado. No hay GPU. El disco es
  limitado: borrar el `.git` de los clones de fuentes una vez inventariados.
- **AcidBite (190 GB) está en el ordenador de Iker**, no en GitHub. Para trabajar con él:
  - el puente al ordenador (herramientas `mcp__remote-devices__*`, cuando la conversación está enlazada con la app de
    escritorio y la carpeta está conectada), o
  - scripts que Iker ejecute en local con sus GPU, que escriban el índice y las hojas en el repo.
- Los vídeos y los packs de **Gumroad** son de pago: repo privado y no redistribuir.
- **Nunca dar por buena una textura sin mirarla:** hoja de contactos y Read.
