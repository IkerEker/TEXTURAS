# ORDEN PERMANENTE PARA CADA PLUGIN · Biblioteca única + autorrevisión de velocidad y GPU

*(Iker: pega este texto entero en la conversación de cada plugin: NEONIZADOR, NEONIZADOR vídeo, PAPELATOR, A mano,
Analog FX, Trazo y Cartelator. Es el mismo para todos; cada plugin busca su parte en la tabla del final.)*

---

**Esta orden es de Iker y es permanente.** Tiene dos partes, (A) y (B). Antes de nada, copia el apartado
«REGLAS PERMANENTES» del final al `CLAUDE.md` de tu repo, para que la sigan todas tus conversaciones futuras. Después haz
(A) y luego (B) y dame el informe del final.

## 0. Reglas que nada de esto cambia

1. El plugin funciona **100 % solo** en el ordenador de Iker, sin Claude y sin internet. La biblioteca **solo se usa al
   construir**: el `.ccx`/panel lleva dentro todo lo que usa.
2. **Ningún resultado cambia sin que Iker lo sepa.** Tu prueba exacta (tu ficha §6, columna «Prueba» de la tabla final)
   se pasa antes y después de cada cambio. Si un byte o una huella cambia, para y enséñaselo a Iker con el antes y el
   después. Él decide.
3. Repos privados. El material de pago (AcidBite, Gumroad) no se redistribuye ni entra en git.
4. Ninguna textura se da por buena sin mirarla.
5. **No borres nada de golpe.** Se quitan de tu repo las **carpetas de material** (fotos, bancos de texturas), y solo
   cuando tu prueba pase leyendo de la biblioteca. **Tu código, tus herramientas de construcción, tus pruebas y tu
   historial se quedan en tu repo.** Sin ellos no se puede reconstruir ni arreglar el plugin.
6. Trabaja en una rama. No fusiones en `main` sin el OK de Iker (y `main` de NEONIZADOR no se toca sin permiso).

## A. La biblioteca única de Iker es tu ÚNICA fuente de material

**Dónde está.** El repo privado `IkerEker/TEXTURAS`, rama `atlas` (añádelo con `add_repo`, en modo lectura). En cada
ordenador de Iker hay además una carpeta `Biblioteca/` (`TEXTURAS/`, `ACIDBITE/`, `originales/`, `generadas/`); sus
herramientas la encuentran con la variable `TEXTURAS_ROOT`. Material, sonidos, vídeos y escaneos nuevos los mete Iker
**en la biblioteca**, nunca en un plugin.

**Lee primero, en este orden:**
1. `MAPA.md`: dónde está cada cosa y cómo buscar.
2. `DECISIONES.md`: reglas de ids, originales, GPU (§10).
3. `plugins/<tu plugin>.md`: tu ficha.
4. `plugins/<tu plugin>/uso_id.json`: tu tabla `nombre interno → id`, en tu orden.
5. Tu bloque de `plugins/MENSAJES.md`: los pasos concretos de tu migración y tu prueba exacta.
6. `revision/RESUMEN.md`.

**Cómo buscar sin revisarlo todo (la biblioteca ya está revisada a ojo, una a una).** Los 9.031 assets de
`indice/indice.json` llevan una ficha `revision` con estos campos:

| Campo | Qué dice |
|---|---|
| `que_es` | qué es la textura |
| `calidad` | nota de 1 a 5 |
| `defectos` | qué le pasa, si le pasa algo |
| `familia`, `variante`, `mejor_de_familia` | a qué grupo pertenece y si es la mejor de él |
| `uso`, `modo` | para qué sirve y con qué modo de fusión |
| `usar_si`, `evitar_si` | cuándo conviene y cuándo no |
| `color`, `orient`, `escala`, `estilo` | aspecto |
| `medidas` | tamaño, alfa, color medio, pHash… |
| `hoja` | hoja de contactos donde se ve |

Usa siempre el buscador; funciona desde cualquier carpeta:

```bash
python3 <TEXTURAS>/tools/atlas/buscar.py goteo blanco --min 4            # palabras + ficha, mejores primero
python3 <TEXTURAS>/tools/atlas/buscar.py --clase tileables --sub papel --tileable --mejor
python3 <TEXTURAS>/tools/atlas/buscar.py --familia pieza_burbuja --json   # para scripts
python3 <TEXTURAS>/tools/atlas/buscar.py --ficha <id>                     # ficha completa de un asset
```

- Por defecto oculta lo marcado REHACER, lo sustituido y lo dudoso (`--todo` lo enseña).
- Ordena por nota y pone delante el mejor de cada familia.
- No recorras carpetas a mano ni vuelvas a revisar bancos enteros: **busca en las fichas y mira solo la `hoja` de lo
  que vas a usar** (con Read).
- Para cada función nueva o mejora, recorre **todas** las clases que puedan servir (`MAPA.md` → «Qué hay»). Eso
  incluye AcidBite (`ab:`), collage, vídeo y sonido. Así no se te escapa nada.

**Cómo se construye.** Tu herramienta de construcción lee cada archivo **por id**:
- `or:<md5>` para originales bit a bit;
- `tx:` para lo procesado;
- `ab:` para AcidBite.

Resuelve el id con `indice/indice.json` (campo `archivo`) sobre `TEXTURAS_ROOT`. Hoy tus `.bin`/PNG salen de tus
fuentes de siempre. Si aún no está hecho, haz la migración de tu bloque de `MENSAJES.md`, en este orden:
1. Pasa tu prueba exacta.
2. Cambia solo de dónde se lee.
3. Vuelve a pasar la prueba: tiene que dar idéntico.
4. Solo entonces quita de tu repo las carpetas de material.

**Si te falta algo.** No lo dibujes, no lo descargues y no crees un banco. Busca primero. Si de verdad no está,
termina tu respuesta con un bloque **«PEDIDO PARA LA BIBLIOTECA:»** que diga qué necesitas, para qué, el formato, el
tamaño y el modo. Iker se lo pasa a la conversación de TEXTURAS, que lo añade, lo revisa y le da un id.

**Cambiar a material mejor de la biblioteca** (por ejemplo, una pieza rehecha o un tile de verdad repetible) cambia el
resultado. Propónlo con el antes y el después y espera el sí de Iker.

## B. Autorrevisión: más rápido y por la gráfica, sin cambiar el resultado

1. **El hardware de Iker (PC con Windows, captura del 20-11-2026):**
   - **2 × NVIDIA GeForce RTX 4090** (GPU 0 y GPU 1, 24 GB de VRAM cada una);
   - CPU a ~4,9 GHz y 64 GB de RAM;
   - SSD NVMe.

   Tu sandbox no tiene GPU, así que las medidas reales se hacen en su PC. Si necesitas la versión del driver, pide
   `nvidia-smi`. Con dos gráficas: aprovecha que hay dos (por ejemplo, una calcula mientras la otra codifica vídeo o
   prepara la siguiente tanda), pero el plugin tiene que funcionar bien con una sola y sin ninguna.
2. **Mide antes de tocar.** Crea un banco de pruebas fijo: mismos documentos, tamaños, efectos e intensidades y misma
   semilla. Debe medir el tiempo por efecto y fase (cargar texturas, calcular, devolver a Photoshop/AE) y la memoria.
   - Tiene que poder ejecutarse en el PC de Iker con una sola orden (un `.bat`/`node …`) y escribir un JSON de
     resultados.
   - Las medidas de la sandbox no valen como referencia.
3. **Revisa tu código buscando dónde se va el tiempo.** Candidatos habituales:
   - decodificar o convertir texturas en cada uso → hazlo una vez y guárdalo en caché;
   - preparar al construir (mipmaps, tamaños reducidos, LUT) lo que hoy se calcula en vivo;
   - bucles por píxel → arrays tipados y menos copias;
   - trabajo independiente → workers;
   - operaciones que Photoshop ya hace de forma nativa (y acelerada) → `batchPlay`;
   - vídeo → ffmpeg con NVENC/NVDEC.
4. **GPU todo lo posible, con estas condiciones:**
   - **Comprueba qué ofrece tu anfitrión** (UXP de Photoshop, CEP de After Effects, Node) **en la versión que usa
     Iker**, y pruébalo. No supongas. NEONIZADOR vídeo ya usa WebGL2 en CEP: es el modelo a seguir allí.
   - Las herramientas de construcción pueden usar GPU para **analizar**. Lo que **alimenta al plugin** se genera en
     CPU y de forma determinista (DECISIONES §10), porque dos gráficas no dan los mismos bytes.
   - Cada camino nuevo por GPU **conserva el camino CPU**: como referencia y como respaldo si la gráfica no está o
     falla. El plugin tiene que funcionar igual en un ordenador sin esas gráficas.
   - Si la versión GPU da **exactamente** tu prueba exacta, se puede activar.
   - Si difiere aunque sea un poco, mide la diferencia (máxima por canal, % de píxeles distintos) y prepara
     imágenes del antes y el después. Queda **apagada** hasta que Iker diga sí. Nunca se activa sin avisar.
5. **Optimizaciones que no cambian el resultado** (caché, menos copias, precálculo idéntico, cargar menos): hazlas si
   la prueba exacta da idéntico y el banco de pruebas mejora. Si no mejora de verdad, deshazla.

## Informe que me das al terminar

1. Qué has leído y tu tabla de ids.
2. Estado de la migración (de dónde lees ahora y qué carpetas de material puedes quitar ya).
3. Qué partes van ya por GPU y cuáles podrían ir.
4. Una tabla antes/después del banco de pruebas (tiempo por efecto).
5. Qué has cambiado y la prueba exacta de cada cambio («idéntico» o la diferencia medida).
6. Lo que necesita mi decisión, con imágenes.
7. Tus «PEDIDOS PARA LA BIBLIOTECA».

Corto y claro.

## REGLAS PERMANENTES (copiar al `CLAUDE.md` del plugin)

```
## Biblioteca y velocidad (orden de Iker, 20-11-2026; texto completo: TEXTURAS/plugins/ORDEN_PLUGINS.md)
- Material SOLO de la biblioteca IkerEker/TEXTURAS (rama atlas) + Biblioteca/ local (TEXTURAS_ROOT). Nada de bancos propios.
- Buscar con tools/atlas/buscar.py (usa las fichas de la revisión 100 %: nota, mejor de familia, usar/evitar si);
  mirar la `hoja` de lo elegido; no revisar bancos enteros; recorrer todas las clases útiles (incl. ab:, vídeo, sonido).
- Construir leyendo por id (or:/tx:/ab:) vía indice/indice.json. El plugin lleva dentro lo que usa: funciona sin Claude ni internet.
- Si falta algo: «PEDIDO PARA LA BIBLIOTECA:» al final de la respuesta; nunca dibujarlo/descargarlo dentro del plugin.
- Prueba exacta antes y después de todo cambio; cualquier diferencia → Iker decide con antes/después.
- Velocidad: medir con el banco de pruebas en el PC de Iker; GPU donde se pueda, con camino CPU de respaldo;
  una versión GPU que no dé idéntico queda apagada hasta que Iker diga sí. Gráficas de Iker: 2 × RTX 4090 (24 GB c/u), 64 GB RAM.
- El código, las herramientas y las pruebas se quedan en este repo; solo se quitan carpetas de material ya migradas.
```

## Tu parte (busca tu fila)

| Plugin | Ficha | Tabla de ids | Prueba exacta | Notas |
|---|---|---|---|---|
| NEONIZADOR (Photoshop) | `plugins/neonizador.md` | `neonizador/uso_id.json` (287) | sha256 `index.json` → `3db2fb598471d78e`; `.bin` concatenados → `3be83b02c7c0874e`; `refhash.js`, `golden.js`, `uxptest.js` | lee los `or:` heredados (idénticos). Las 17 piezas rehechas de `productos/` no las lee ningún efecto. El repo debe pasar a **privado** (lleva Gumroad). |
| NEONIZADOR vídeo (AE) | `plugins/neonizador_video.md` | la misma + `anexo_video.json` | sha256 de `index.json` y `.bin`; 49 huellas a 0,6 | ya usa WebGL2. Los fotogramas de GPU varían por tarjeta: la referencia exacta son los `.bin` y las huellas CPU. |
| PAPELATOR | `plugins/papelator.md` | `papelator/uso_id.json` (750) | `verificar_assets.py` → 0 distintos; md5 de los 6 JSON; 60 renders | no regenerar milimetrados ni imperfecciones (no son reproducibles). |
| A mano | `plugins/a-mano.md` | `a-mano/uso_id.json` | los dos módulos generados byte a byte | publica cintas y sellos en `productos/`. |
| Analog FX | `plugins/analog-fx.md` | `analog-fx/uso_id.json` | ficha §6 | Iker aún no ha decidido si adopta los tileables nuevos: por defecto, idéntico. Hoy calcula en JS puro, buen candidato a la parte B. |
| Trazo | `plugins/trazo.md` | `trazo/uso_id.json` | md5 de los 20 `.bin` + renders `tools/run.js` | verificar primero que el build es reproducible. |
| Cartelator | `plugins/cartelator.md` | — (no usa texturas) | sha256 del `main.js` empaquetado | la parte A vale para lo nuevo: si una función nueva necesita textura, sale de la biblioteca. |
