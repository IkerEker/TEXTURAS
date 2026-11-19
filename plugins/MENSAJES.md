# Mensajes para pegar en la conversación de cada plugin (TRASPASO §8)

Cada bloque es autónomo: cópialo entero en la conversación de ese plugin.

---

## NEONIZADOR

> **Cambio: a partir de ahora NEONIZADOR construye desde la biblioteca común.**
>
> **Qué ha cambiado.** Existe un único atlas de texturas: el repo privado `IkerEker/TEXTURAS` (rama `atlas` hasta que Iker
> la fusione) más una carpeta local `Biblioteca/` igual en cada ordenador (`TEXTURAS/`, `ACIDBITE/`, `originales/`,
> `generadas/`). Se monta con `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca>`. Las herramientas leen la
> raíz de la variable `TEXTURAS_ROOT` (o un argumento). Lee primero `MAPA.md` y `DECISIONES.md` del repo (`add_repo`
> IkerEker/TEXTURAS, lectura).
>
> **Tu tabla `nombre_interno → id`:** `plugins/neonizador/uso_id.json`, 287 filas en el orden de tu anexo. El `id` de cada fila
> es el **archivo heredado exacto** que hoy lee `build_texpack.py` (`originales/heredado/neonizador/BIBLIOTECA/…`, 715
> archivos, 182 MB, md5 comprobado contra tu `fuentes.json`), así que los `.bin` salen idénticos. Los atlas
> (`fg_pavesas`, `fg_chispas`, `mo_manchitas`) traen la lista de piezas en orden. Cada fila trae además `original_real` y
> `productos_comunes` (la foto original y su versión de TEXTURAS) por si algún día decides cambiar: eso sí cambiaría el
> resultado y requiere decisión de Iker.
>
> **Qué tocar (solo esto), en la rama `biblioteca-texturas`:** `tools/build_texpack.py` → `ruta(id)` leyendo
> `Biblioteca/TEXTURAS/indice/indice.json` y la tabla en lugar de `B = R + '/BIBLIOTECA'`, `PACK`, `VIDEO_FRAMES` y
> `ELEMENTS`. **Fija `ELEMENTS`** con la lista exacta (`quemadura1-4` = `mancha_circular_de_quemadura_c_{03,04,06,07}.png`),
> no «los N más pesados». Conserva el orden de `goteos.json` y la numeración de `gt_`/`fg_`/`bf_`/`mo_`. Los
> `extract_*.py` pueden apuntar a `originales/` o dejarse: sus salidas ya están en la biblioteca. Motor, panel UXP,
> `ae/lib/motor.js` y `build_ae.js`: **no se tocan**.
>
> **Prueba exacta (ficha §6), antes y después:** `cd plugin/tex && sha256sum index.json | cut -c1-16` → `3db2fb598471d78e`;
> `cat $(ls *.bin | sort) | sha256sum | cut -c1-16` → `3be83b02c7c0874e` (287 `.bin`, 178 809 764 bytes). Después,
> `refhash.js` (49 efectos, intensidad 0,6, semilla 3) contra los valores de tu ficha y `golden.js` contra
> `huellas.json`; `node tools/dev/uxptest.js` → `ok`. Si un `.bin` cambia: `sha256sum *.bin` contra la copia de
> `plugin/tex` para localizarlo; no se acepta ningún cambio sin decírselo a Iker.
>
> **Qué dejas de hacer:** cuando la prueba pase, borrar `BIBLIOTECA/` del repo (está entera en la biblioteca común:
> heredados en `originales/`, piezas en `productos/piezas_neonizador/`, fotos originales en TEXTURAS). No vuelvas a crear
> bancos de texturas dentro del plugin.
>
> **Qué ganas:** puedes quitar del `.ccx` las 144 texturas sin uso (~88 MB) **conservando familias completas** (las que el
> motor recorre por prefijo y numeración). Material nuevo que pedía tu ficha: `Shadow Mask.png`, `Scanlines.png`, CRT
> `Dirt` y `Noise_01-16` (fósforo, rejilla, nieve, desplazamiento) para crt/fosforo/vhs; vídeo VHS/glitch real y fuego 4K
> con alfa (Burning Paper) para la versión de After Effects; hojas plegadas/arrugadas 4K; tiles reales de papel
> (`tileable=true`) para repetir con `wrap: 1` en vez de espejo. Recetas: `tecnicas/fuego.md`, `look_analogico.md`,
> `relieve_desplazamiento.md`, `montaje_cortinilla_luz.md`.
>
> **Regla:** si necesitas una textura, primero búscala (`python3 tools/atlas/buscar.py …`); si no está, se añade a la
> biblioteca, nunca al plugin. **El plugin sigue 100 % autónomo:** la biblioteca solo se lee al construir.
>
> **Aviso de Iker:** el repo `neonizador` es **público** y contiene packs de Gumroad de pago. Hay que pasarlo a privado.

---

## PAPELATOR

> **Cambio: a partir de ahora PAPELATOR construye desde la biblioteca común.**
>
> **Qué ha cambiado.** Atlas único: repo privado `IkerEker/TEXTURAS` (rama `atlas` hasta su fusión) + `Biblioteca/` local
> igual en cada ordenador, montada con `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca>`. Raíz por
> `TEXTURAS_ROOT`. Lee `MAPA.md` y `DECISIONES.md` (`add_repo` IkerEker/TEXTURAS, lectura).
>
> **Tu tabla:** `plugins/papelator/uso_id.json`, 750 filas en el orden de tu anexo; `id` = `or:<md5>` del original
> **intacto y con su nombre de siempre** (`originales/papelator/<tu ruta>`). Las 13 filas sin id son procedurales/generadas
> (pantallas, calcos, UI). Las **3 parejas duplicadas** de `imperfecciones/` citan el mismo id dos veces, en el mismo orden.
>
> **Qué tocar (solo herramientas):** `tools/common.py` (`TEXTURAS_ROOT` + `fuente(id)`), `tools/indices/{imp,nimp,pap}_index.json`,
> `fold_sources.json`, `bordes_sets.json`, `PAPERS`, `BOARDS`, `TYPES`/`SRC`, `SRC`/`ITEMS` de `build_overlays.py`, las 2
> rutas de `build_calco.py` y `SRC` de `bordes_v1.py`. Motor, panel y `.ccx`: no se tocan. **Camino seguro: cambiar solo de
> dónde se leen las fotos y no regenerar nada.** No regeneres los milimetrados (`build_grids.py` no es reproducible y se
> ejecuta al importarlo) ni las imperfecciones (`imperf.json` lleva ajustes a mano; `imperf_tune.py` no es idempotente).
>
> **Prueba exacta (ficha §6):** `verificar_assets.py` → «822 PNG comprobados, 0 distintos»; md5 de los 6 JSON:
> `bordes 6170f570…`, `calco 5d6fead3…`, `folds 2cbcb522…`, `imperf 68221955…`, `overlays 5239bc9f…`,
> `papers 17d76067…`; y la columna `md5_archivo` de cada fuente = el md5 del `id`. Si algo se regenera: los 60 renders
> (`art.raw` md5 `4527b81a…`, Node v22.23.4). Cualquier diferencia, a Iker antes de aceptarla.
>
> **Qué dejas de hacer:** cuando la prueba pase, quitar del repo las carpetas de fotos (1,82 GB). Nada de bancos nuevos
> dentro del plugin.
>
> **Qué ganas:** **cinta adhesiva entera** (34 PNG con alfa de ACIDBITE: celo, americana, de pintor, de color), **hoja
> plegada y arrugada 4K** (Fold 1–5, Crumble), **moho real** (`productos/piezas_neonizador/moho`: colonias, tiles,
> manchitas), quemaduras (`…/quemado`), papel gris a escala (`productos/papel_gris`). Bordes quemados: Burning Paper los
> tiene en vídeo; hay que extraer fotogramas (pendiente). Sigue faltando cartón en planta, pliegues 7–8, calco/térmico/couché,
> corcho, pizarra… (`indice/cruce_acidbite.md`). Tu método de alfa de croma ya es común (`tools/atlas/metodo_bordes_matte_papelator.py`).
>
> **Regla:** primero buscar en la biblioteca; lo nuevo se añade allí. **El plugin sigue 100 % autónomo.**
>
> **Aviso de Iker:** el repo `papelator` es **público**; hay que pasarlo a privado.

---

## A MANO

> **Cambio: a partir de ahora A mano construye desde la biblioteca común.**
>
> **Qué ha cambiado.** Atlas único: repo privado `IkerEker/TEXTURAS` (rama `atlas`) + `Biblioteca/` local (montar con
> `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca>`), raíz por `TEXTURAS_ROOT`. Lee `MAPA.md`.
>
> **Tu tabla:** `plugins/a-mano/uso_id.json`: las 88 cintas (orden #0–#87) con el `or:<md5>` de su foto, las 4 fotos de
> grumos, y `fuentes_en_orden` = tus `SOURCES` en su orden exacto, cada una con id, familia e `inicio` (top/left). Los
> duplicados de `CERAS/` y `GUACHE/` se citan dos veces, como hoy.
>
> **Qué tocar:** `tools/extract_textures.py` (raíz configurable y `SOURCES` por ids, mismo orden) y `tools/grumos.py`
> (`PLAN` por id). Unas 20 líneas. Motor, panel, `js/texdata.js` y `js/grumosdata.js` (siguen versionados): no se tocan.
>
> **Prueba exacta (ficha §6):** `python3 tools/extract_textures.py && md5sum js/texdata.js` → `182e0cdba680cba58fea00c0dd254ca5`;
> `python3 tools/grumos.py && md5sum js/grumosdata.js` → `d3ca0cf24cb8a2ba3fa4b8a3869c2eba`; `git status --short js/`
> vacío. Si no sale exacto: la huella de render (27 presets) de tu ficha y decírselo a Iker.
>
> **Qué dejas de hacer:** cuando pase, borrar `TRAZOS/` (165 MB) y `referencias/texturas/` del repo y actualizar los textos
> que los citan. No crear bancos nuevos.
>
> **Ya publicado como producto común:** tus 88 cintas (`productos/cintas_trazo`, byte a byte iguales) y tus 50 sellos
> (`productos/sellos_relieve`). Si cambias la extracción, vuelve a publicarlos con `tools/atlas/productos_amano.py`.
>
> **Qué ganas:** grano de papel **real** y a escala (`productos/papel_gris`, 128 = plano, px/mm conocido) para sustituir el
> sintético cuando quieras (cambia el resultado: decisión de Iker); goteos reales con medidas (`productos/piezas_neonizador/goteos`)
> para los chorretones; rotulador y tinta con alfa de ACIDBITE (trazos de anotación, no cintas largas). Puedes poner a 0
> el `CAP` de `rotu` y `boli` (11 cintas sin uso, ~118 KB). Sigue faltando tiza/pastel, brocha larga y grumos grandes.
>
> **Regla:** primero buscar en la biblioteca. **El plugin sigue 100 % autónomo.**
>
> **Aviso de Iker:** el repo `a-mano` es **público**; hay que pasarlo a privado.

---

## ANALOG FX

> **Cambio: a partir de ahora Analog FX construye desde la biblioteca común.**
>
> **Qué ha cambiado.** Atlas único: repo privado `IkerEker/TEXTURAS` (rama `atlas`) + `Biblioteca/` local (montar con
> `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca>`), raíz por `TEXTURAS_ROOT`. Lee `MAPA.md`.
>
> **Tu tabla:** `plugins/analog-fx/uso_id.json`, 294 filas (las de tu anexo, en orden); `nombre_interno` = tu id de plugin
> (solo esas se usan); `id` = `or:<md5>` del original intacto; `productos_comunes` = su versión tileable de TEXTURAS.
>
> **Qué tocar:** `tools/textures_manifest.json` (familia/orden → id), `tools/build_textures.py` (`--biblioteca`),
> `tools/build_tintas.py` (conservar «tono/raw»), `tools/build_drips.py` (o consumir directamente `manchas/goteos`, que es
> tu propia clasificación). `plugin/js/*`, `textures.json`, `.bin` y `package.sh`: no se tocan.
>
> **Decisión por defecto: originales (resultado idéntico).** Adoptar los tileables nuevos de TEXTURAS cambiaría un poco
> el resultado: solo si Iker lo decide.
>
> **Prueba exacta (ficha §6):** antes, `find plugin/textures plugin/drips -type f -exec md5sum {} + | sort -k2 > ref_assets.md5`
> y los renders `.ppm` de Letras (semillas 3 y 7) e Imágenes. Después, mismos md5. Si cambian fuentes: PSNR ≥ 40 dB y
> diferencia máxima ≤ 8 por canal, revisando a ojo Humedad, Tinta corrida, Acuarelado, Fotocopia, Láser roto, Estampado
> manchado y Destrozado; y decírselo a Iker. `.ccx` ≈ 40,4 MB.
>
> **Qué dejas de hacer:** cuando pase, quitar del repo `textures-src/` (1,1 GB), `Tintas impresas/`, `GOTAS/` y
> `BIBLIOTECA/goteos/`. No crear bancos nuevos. Recuerda: solo cargas la `_1` de cada familia (salvo `desgaste` y `tinta`)
> y `goteo` y `gubia` no se usan: puedes quitarlas del `.ccx`.
>
> **Qué ganas:** escala real (`tile_mm`, `px_por_mm`) para fijar `physSampler` por datos; papel gris a escala; grano y polvo
> de película reales (16mm/35mm/Super 8 de ACIDBITE) y ruido VHS/CRT para técnicas analógicas; recetas en
> `tecnicas/look_pelicula.md` y `look_analogico.md`. Sigue faltando fibra de celulosa real, tóner real, sello de goma,
> rodillo y veta de madera para grabado.
>
> **Regla:** primero buscar en la biblioteca. **El plugin sigue 100 % autónomo.**
>
> **Aviso de Iker:** el repo `analog-fx-plugin` se puede leer sin credenciales (parece **público**); hay que pasarlo a privado.

---

## TRAZO

> **Cambio: a partir de ahora Trazo construye desde la biblioteca común.**
>
> **Qué ha cambiado.** Atlas único: repo privado `IkerEker/TEXTURAS` (rama `atlas`) + `Biblioteca/` local (montar con
> `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca>`), raíz por `TEXTURAS_ROOT`. Lee `MAPA.md`.
>
> **Primero:** comprueba que tu build actual se reproduce (ficha §6.1): `md5sum plugin/textures/*.bin > /tmp/antes.md5`,
> `python3 tools/build_assets.py && python3 tools/extract_papers.py`, `md5sum -c`. Si no sale igual, para y díselo a Iker
> antes de migrar nada.
>
> **Tu tabla:** `plugins/trazo/uso_id.json`: tus patrones de `build_assets.py` resueltos a archivos (orden alfabético,
> como un glob ordenado), cada uno con su `or:<md5>`, familia y `q`. Nombres oficiales: `pin_gouache` (que es **óleo**)
> → `oleo`; `pin_guache` → `gouache` (en la tabla; tus nombres internos no cambian).
>
> **Qué tocar:** `tools/build_assets.py` (`FAMILIES`, `STAMP_TAGS`, `OVERLAYS`, MAT, RTILE, RGRAND → ids),
> `tools/extract_papers.py` (`KINDS`), `ES.ROOT` → `TEXTURAS_ROOT`. Los parámetros (`WIDTH`, `HMAXF`, `CAP`…) siguen en Trazo.
> El motor y `plugin/textures/*.bin`: no se tocan. Aprovecha para que `package.py` falle si falta un `.bin`.
>
> **Prueba exacta (ficha §6):** nivel 1 (md5 de los 20 `.bin` iguales); si no, nivel 2 (cabeceras TRZ1 y diferencia media 0);
> nivel 3 (`tools/run.js` con semilla 7 en las 7 técnicas, AE = 0); nivel 4 (`flow_test.js` → «TODO OK», `.ccx` de 56
> archivos ≈ 18,7 MB). Cualquier cambio, a Iker.
>
> **Qué dejas de hacer:** cuando pase, quitar `TEXTURES/` (1,3 GB) del repo y el peso muerto (`pin_cera`, `pin_pastel`,
> `ov_carbon`, `ov_goteos`, `ov_grafito`, ~3,7 MB) si lo confirmas. No crear bancos nuevos.
>
> **Qué ganas:** papeles con **px/mm real** (`productos/papel_gris`, `tileables/papel` con `tile_mm`) en lugar de suponer
> 10 px/mm; cintas enderezadas de A mano como referencia (`productos/cintas_trazo`); tiles de pintura sin costura de
> TEXTURAS a resolución completa. Sigue faltando óleo con empaste, pastel real, grafito por durezas y floraciones reales.
>
> **Regla:** primero buscar en la biblioteca. **El plugin sigue 100 % autónomo.**
>
> **Aviso de Iker:** el repo `trazo` se puede leer sin credenciales (parece **público**); hay que pasarlo a privado.

---

## CARTELATOR

> **Cambio:** existe un atlas de texturas común (repo privado `IkerEker/TEXTURAS`, rama `atlas`; empieza por `MAPA.md`).
> **Hoy no tienes que cambiar nada:** Cartelator no usa texturas.
>
> 1. **Crea tu repo privado** en GitHub (`IkerEker/cartelator`) y sube el proyecto: ahora solo vive en esta conversación
>    y en un zip.
> 2. Prueba exacta, por si acaso: `sha256` del `main.js` empaquetado →
>    `4cdf9021700cddf71d00625dc2e93cf94586160eab1b995b3fbaac697edc181d`, y el `.ccx` con sus 27 archivos.
> 3. **Para el futuro** (tus «acabados»): bordes rasgados (`bordes/*`, tiras de PAPELATOR), borde de brocha seca
>    (`productos/cintas_trazo`, formato A mano), grano a escala con px/mm (`productos/papel_gris`). Sello de caucho /
>    tinta de grabado **todavía no existe**: si lo necesitas, se añade a la biblioteca. El camino que mantiene el `.ccx`
>    autónomo es el de A mano: `tools/build.py` lee la biblioteca por id y genera un `js/texdata.js` en base64.
> 4. Tus iconos se quedan en `icons/` (son interfaz) y tus `referencias/` (carteles ajenos) no entran en la biblioteca.
>
> **Regla:** si algún día necesitas una textura, primero la buscas en la biblioteca; si no está, se añade allí. El plugin
> sigue 100 % autónomo.
