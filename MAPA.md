# MAPA · la puerta de entrada al atlas de texturas de Iker

**Para Claude, desde cualquier conversación:** antes de dibujar, generar o pedir una textura, búscala aquí.
Si no está, se añade aquí (nunca un banco suelto dentro de un plugin).

## Dónde está cada cosa

```
Biblioteca/                      (= TEXTURAS_ROOT; la misma en cada ordenador de Iker; nunca en GitHub)
├── TEXTURAS/                    este repo (privado): lo procesado, el índice, los productos, las recetas
├── ACIDBITE/                    el pack ACIDBITE tal cual (190 GB; 01_TRANSICIONES … 07_SONIDO)
├── originales/                  fuentes intactas de los plugins (por repo y ruta; md5 en el MANIFIESTO)
│   └── heredado/neonizador/     los 715 archivos de los que NEONIZADOR construye hoy su plugin/tex
└── generadas/                   lo que se cree a partir de ahora
```
Montar o comprobar en un ordenador: `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca> [--acidbite <carpeta del pack>]`.

## Cómo buscar

**Método completo y reglas de variedad: `biblioteca_raiz/CLAUDE.md`** (se copia a `Biblioteca/CLAUDE.md`, que cada
plugin carga solo al abrir la carpeta).

0. **`buscar.py --necesidades`** → 78 necesidades (fondos, superposiciones, relieves, piezas, trazos, luz, vídeo,
   sonido, LUT) con su lista curada a ojo (5–16 opciones variadas) y su hoja ya hecha (`indice/necesidades.json`,
   `indice/necesidades_hojas/`). `--necesidad NOMBRE`. Se regeneran con `tools/atlas/necesidades.py` desde
   `indice/necesidades_spec.json` (ahí se fijan a mano los elegidos: `poner`).
1. `python3 tools/atlas/buscar.py <2–4 palabras> --ver` → abanico de 12 opciones buenas y **distintas** (una por
   familia, repartidas entre TEXTURAS, ACIDBITE y originales, con algo de azar) + hoja JPG con miniaturas numeradas.
   Ordena por lo que encaja con la ficha (qué es, familia, clase, uso, color, estilo…), con sinónimos
   (`indice/sinonimos.json`), inglés, plurales y género; la nota multiplica pero no decide sola.
2. Por al menos 3 lados (otro nombre, el efecto, el material vecino) y con el filtro del papel que cumple:
   `--tileable` · `--alfa` · `--clase video|sonido|lut` · `--donde 'orient~vertical'` · `--resumen` para ver cuánto hay.
3. Mira la hoja con Read y elige mirando. `--mas` (otra tanda) · `--familia` · `--parecidos ID` · `--ficha ID`.
4. Varias variantes por efecto, de familias distintas; marca «ya lo usa: …» = evita repetir lo de otro plugin.
5. `--plugin X --apuntar ID…` deja constancia en `Biblioteca/_uso/`.
6. Cada recurso tiene **papel** (fondo repetible, superposición, pieza, relieve, transición, máscara, elemento/superposición/
   fondo animado, sonido, LUT…) y **fondo** (transparente, sobre negro, sobre blanco, gris neutro): `--papel`, `--fondo`,
   `--papeles`. Varias formas a la vez: `"goteo | chorreon | drip"`. Lo que nadie usa: `--sin-usar`.
La lógica está en `tools/atlas/biblioteca.py`; los scripts de construcción pueden importarla (`Biblioteca().buscar(…)`,
`.necesidad(…)`, `.ruta(id)`) en vez de leer el índice a mano.

`buscar.py --mapa` = qué hay en toda la biblioteca. Índice: `indice/indice.json` (esquema en `indice/ESQUEMA.md`).
Nombres de plugins y alias: `indice/nombres.json`. **No elijas leyendo `catalogo.json` o el índice a mano y cogiendo
los primeros** (salen siempre los mismos y nunca ACIDBITE).

## Qué hay (por necesidad)

| Necesitas… | Mira |
|---|---|
| papel, superficie, madera, grunge, líquidos repetibles (con mm) | `tileables/*` · `productos/papel_gris` |
| trazo real (PNG) / cinta enderezada | `trazos/*` · `productos/cintas_trazo` |
| manchas, goteos, salpicaduras, imperfecciones, bordes, pliegues | `manchas/*` · `productos/piezas_neonizador/*` · `imperfecciones/*` · `bordes/*` · `pliegues/*` |
| fuego, chispas, humo, burbujas, moho, gotas | `luz_y_elementos/*` · `productos/piezas_neonizador/*` |
| cinta adhesiva, rotulador/tinta de anotación, hoja plegada 4K | ACIDBITE Ultimate Paper `Toolkit` (`--clase imperfecciones --sub cinta_adhesiva`, `trazos/*_anotacion`, `pliegues/hoja_4k`) |
| transiciones de vídeo (luz, quemado, máscara, glitch, VHS, papel, tela, túnel…) | `--clase video --sub transiciones/` (ACIDBITE) · `video/transiciones/*` (TEXTURAS) |
| look película / analógico / CRT | `--sub pelicula/` · `--sub analogico/` · `superposiciones/*` |
| elementos animados, marcadores, fondos en movimiento | `--sub elementos/` · `--sub fondos/` · `video/elementos/*` |
| sonidos (whoosh, golpes, risers, ambientes…) | `--clase sonido` |
| LUT de película por cámara | `--clase lut` |
| mapas de relieve / desplazamiento (128 = neutro) | campo `desplazamiento` · `productos/sellos_relieve` |

## Para los plugins

**Orden permanente para cada plugin (biblioteca única + velocidad/GPU): `plugins/ORDEN_PLUGINS.md`.**
**ORDEN 2 (dejar GitHub, casa en `Biblioteca\plugins\<plugin>\`, sin repetidos): `plugins/ORDEN_CARPETA_LOCAL.md`.**

- La biblioteca **solo se usa al construir**; el `.ccx` lleva dentro lo que usa y funciona sin Claude ni internet.
- Cada plugin lee por **id** con `TEXTURAS_ROOT`: su tabla exacta, en su orden, en `plugins/<plugin>/uso_id.json`.
- Originales por `or:<md5>` (bit a bit); productos por `tx:`; AcidBite por `ab:`.
- Antes y después de cambiar de origen: su prueba exacta (ficha §6).

## Documentos

**Traspaso completo (todo en un archivo): `CONTEXTO_BIBLIOTECA.md`.**

`DECISIONES.md` (cómo y por qué se unió todo) · `TRASPASO.md` · `acidbite/ESTADO.md` · `gumroad/ESTADO.md` (packs de Studio DamDam: qué hay y cómo los usa su autor) · `plugins/README.md` y
`CONCILIACION.md` · `indice/cruce_acidbite.md` (qué aporta AcidBite y qué sigue faltando) · `productos/README.md`.
Material de pago (ACIDBITE, Gumroad): uso propio, **no redistribuir**; repo privado.

## collage/ (19-11-2026)
475 piezas recortadas para collage (papeles, cintas, etiquetas, pegatinas, notas, pintura, gel, restos de adhesivo, grafito). Ver `collage/README.md`.

## revision/ (noche 19→20-11-2026): revisión 100 % a ojo
Cada asset de `indice/indice.json` lleva ahora un campo `revision` con su ficha: qué es, nota 1–5, defectos,
familia y variante, en qué se diferencia, uso, modo, usar si / evitar si, color, orientación, estilo, contenido,
comportamiento (vídeo) y medidas. 8318 vistos a ojo; 713 con ficha sin vista (658 sonidos no escuchados,
`audio_revisado: false`; 55 plantillas/proyectos de programa). Empieza por `revision/RESUMEN.md`;
`A_REHACER.md` (21), `NO_VISTOS.md`, `FICHAS.json` (todas juntas) y `familias.json`.
Regenerar: `tools/atlas/revision_sin_vista.py` y luego `tools/atlas/revision_resumen.py --indice`.

**Rehechas (20-11-2026):** las 21 marcadas REHACER están resueltas. 17 piezas de `productos/piezas_neonizador` se
rehicieron con el mismo nombre (burbujas completas, tiles de espuma repetibles sin cruz, gotas enteras, goteo sin croma):
detalle y origen en `productos/piezas_neonizador/REHECHAS.json`, antes/después en `productos/hojas/rehechas_2026-11-20.jpg`,
scripts en `tools/atlas/rehacer/`. Las copias exactas de NEONIZADOR siguen como `or:` heredado con `sustituido_por`.

**Pendientes resueltos (20-11-2026, mañana):**
- 0 dudosos:
  - las 59 LUT de Super 8 son copias byte a byte de las de 16mm (`duplicado_de`);
  - los vídeos con texto o personas, vistos a tamaño completo, llevan `aviso`/`contenido`;
  - los goteos translúcidos se comprobaron contra su foto.
- 0 correcciones: `indice/correcciones.json`, que aplica `construir_indice.py` (los archivos no se renombran).
- Sonidos: los 658 medidos (`revision/audio_medido.json`, `tools/atlas/medir_audio.py`). Siguen sin escucharse; `suena_como` sale de las medidas.
- Plantillas: las 55 leídas por dentro (`revision/plantillas_leidas.json`, `tools/atlas/leer_plantillas.py`): medios que usan, efectos, huecos de los .mogrt y duración.

## Recortes mejorados (20-11-2026)

849 recortes `tx:` rehechos y sustituidos en su sitio (mismo nombre, mismo tamaño y caja). Registro en
`revision/recortes_mejorados.json` (motivo y arreglo de cada uno); en el índice cada asset lleva `recorte_mejorado`.
Muestra en `revision/recortes_mejorados_antes_despues.jpg`.
- Salpicaduras de tinta y óxido/café, fibras, goteos (manchas y productos) y 38 trazos: sin cerco claro ni oscuro en el contorno.
- 18 bordes rehechos desde la foto con el matte de PAPELATOR: sin velo ni bandas semitransparentes en el fondo.
- 29 bordes de papel blanco o gris con las fibras teñidas por el croma (rosa, verde o cian) devueltas al color del papel
  (`tools/atlas/quitar_tinte_croma.py`).
- Se dejan como estaban a propósito, porque «arreglarlos» los empeoraba: gotas, burbujas, fuego y chispas (el alfa es luz),
  moho, quemado, café y foxing, collage (los brillos y cantos son del material), lápiz, cera y gouache, y bordes de cartón marrón o papel azul.
- Ningún plugin lee `tx:`: leen sus `or:` exactos, así que ningún resultado de plugin cambia.
