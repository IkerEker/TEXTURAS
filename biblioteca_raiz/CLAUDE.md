# BIBLIOTECA DE IKER · cómo buscar y elegir material (léelo entero antes de buscar nada)

Esta carpeta es la biblioteca común de Iker para todos sus plugins: **9.031 recursos revisados uno a uno a ojo**,
cada uno con una ficha (qué es, nota 1–5, defectos, familia, para qué sirve, cuándo usarlo y cuándo no, color,
estilo, modo de fusión, medidas). Iker ha pagado y trabajado mucho por este material. **Úsalo entero y con variedad.**

```
Biblioteca/
├── CLAUDE.md          ← esto
├── TEXTURAS/          repo con lo procesado, el ÍNDICE (indice/indice.json) y el BUSCADOR (tools/atlas/buscar.py)
├── ACIDBITE/          2.925 recursos de pago: transiciones, overlays, vídeo, sonidos, LUT, plantillas
├── originales/        fuentes intactas de los plugins (bit a bit)
├── generadas/         lo nuevo que se cree
├── plugins/<plugin>/  la casa de cada plugin
├── _busquedas/        hojas de miniaturas que crea el buscador (se pueden borrar)
└── _uso/              qué ha elegido cada plugin (lo escribe el buscador con --apuntar)
```

## 0. Antes de la primera búsqueda de la conversación

1. Actualiza la biblioteca: `git -C TEXTURAS pull --ff-only` (o doble clic en `ACTUALIZAR_TEXTURAS.bat`).
2. Comprueba que el buscador es el nuevo: `python TEXTURAS/tools/atlas/buscar.py --version` → tiene que decir **v3**.
3. La primera vez, mira las **necesidades ya resueltas** (`buscar.py --necesidades`) y qué hay en la biblioteca (`--mapa`, `--papeles`).

(Si trabajas en la nube con el repo `IkerEker/TEXTURAS`, rama `atlas`, es lo mismo: `python3 tools/atlas/buscar.py …`
desde el clon.)

## 1. La regla que lo cambia todo

**Se busca SOLO con `buscar.py`.** Nunca elijas:
- abriendo carpetas y cogiendo lo primero que ves;
- con `catalogo.json` o `CATALOGO.md` (son viejos y solo tienen una parte);
- leyendo `indice.json` con tu propio script y quedándote con los primeros (salen siempre los mismos, en el orden
  del archivo, y nunca sale ACIDBITE).

El buscador ordena por lo que **encaja** con lo que pides, entiende sinónimos, inglés, plurales y género, y te
devuelve un **ABANICO**: 12 opciones buenas y distintas entre sí (familias, colecciones, aspecto), con algo de azar.
**La número 1 no es «la buena».** Todas encajan. Se elige mirando.

## 2. Lo más rápido: necesidades ya resueltas (empieza SIEMPRE por aquí)

Hay **78 necesidades** con su lista hecha: de 5 a 16 opciones cada una, **elegidas mirando una a una**, variadas
(familias distintas, TEXTURAS + ACIDBITE + originales) y con su **hoja de miniaturas ya hecha**. No hay que barrer nada.
```
python TEXTURAS/tools/atlas/buscar.py --necesidades            # el catálogo (fondos, superposiciones, relieves,
                                                               #   piezas, trazos, luz, vídeo, sonido, LUT)
python TEXTURAS/tools/atlas/buscar.py --necesidades papel      # filtrado
python TEXTURAS/tools/atlas/buscar.py --necesidad pieza_goteo  # sus opciones + «HOJA YA HECHA: …jpg» → ábrela con Read
```
Si tu necesidad está ahí, **usa varias de su lista** (son todas buenas y distintas). Si no está o quieres más, busca
libre (abajo); el buscador te sugiere también las necesidades que encajan con tus palabras.
Los scripts de construcción pueden leerlas directamente: `indice/necesidades.json` (o `from biblioteca import Biblioteca`,
`Biblioteca().necesidad('pieza_goteo')`).

## 3. Búsqueda libre (5 pasos)

**Paso 1. Describe la necesidad en 2–4 palabras:** el objeto o material, más el aspecto, más el uso.
```
python TEXTURAS/tools/atlas/buscar.py papel viejo calido --ver
```
Cuenta solo lo que buscas, sin frases: «textura de papel que parezca antiguo para fondo» → `papel viejo fondo`.
El color y el tamaño matizan: «goteo rojo» trae goteos, primero los más rojos. Si ninguno es rojo, te lo dice: es
una pieza que se recolorea.

**Paso 2. Ábrelo por al menos 3 lados.** Haz 3 búsquedas distintas como mínimo:
- otro nombre: `goteo` / `chorreon` / `drip`;
- el efecto que quieres conseguir: `envejecer`, `quemado`, `humedad`;
- el material de al lado: `carton`, `pergamino`, `periodico`.

Ajusta el **papel que cumple** (cada recurso tiene uno, deducido de su ficha; `--papeles` los lista):

| Lo quieres como… | Filtro |
|---|---|
| fondo que se repite | `--papel "fondo repetible"` |
| imagen encima a pantalla completa | `--papel superposicion` |
| pieza suelta con transparencia | `--papel pieza` |
| relieve gris 50 % (superponer / desplazar) | `--papel relieve` |
| transición de vídeo | `--papel transicion` |
| mate / máscara | `--papel mascara` |
| elemento animado / superposición animada / fondo animado | `--papel "elemento animado"` … |
| sonido · LUT | `--clase sonido` · `--clase lut` |
| según el fondo de la imagen | `--fondo transparente` · `--fondo "sobre negro"` (Trama) · `--fondo "sobre blanco"` (Multiplicar) |
| formato vertical | `--donde 'orient~vertical'` |
| varias formas de decirlo a la vez | `buscar.py "goteo | chorreon | drip"` |
| lo que no usa todavía ningún plugin | `--sin-usar` |

Para ver cuánto hay antes de elegir: `--resumen`. Te dice cuántos encajan en cada clase y familia.

**Paso 3. MIRA.** Con `--ver` el buscador hace una hoja JPG con las miniaturas numeradas (la ruta sale al final:
`HOJA: …/_busquedas/….jpg`). **Ábrela con Read** y elige mirando, nunca solo por el texto.
- Si dice «hoja de su grupo», la miniatura es la hoja de contactos de su carpeta. La pieza exacta está en su `archivo`.
- `--ficha ID` da la ficha completa.
- Las variantes de una pieza que te gusta salen con `--familia NOMBRE`; las que se le parecen, con `--parecidos ID`.
- Si no te convence nada: `--mas` (la siguiente tanda de 12 distintas) o vuelve a lanzar la búsqueda (otra mezcla).

**Paso 4. Elige CON VARIEDAD.** Las reglas de variedad están en el apartado 3.

**Paso 5. Apunta lo que eliges.** Así el resto de plugins lo saben y no repiten:
```
python TEXTURAS/tools/atlas/buscar.py --plugin <tu_plugin> --apuntar <id> <id> …
```
Y en tu `uso_id.json` deja, por cada id, para qué lo usas y qué búsquedas hiciste.

## 4. Reglas de variedad (lo que Iker pide expresamente)

1. **Nada de una sola textura por efecto** si el efecto es de textura, papel, mancha, luz, polvo, transición o
   similar. Mete varias variantes reales. Como guía, **6–12 por efecto**, de **al menos 3 familias distintas** y, si
   las hay, de más de una colección (TEXTURAS, ACIDBITE, originales). El plugin las ofrece como variantes o elige
   entre ellas con semilla, para que cada resultado no sea igual. Si de verdad solo tiene sentido una, explícale a
   Iker por qué.
2. **Una por familia.** Una familia son variantes de lo mismo, y dos de la misma familia casi no aportan. Repite
   familia solo cuando ya has cubierto las demás que encajan.
3. **ACIDBITE cuenta.** Es material de pago, de lo mejor para vídeo: transiciones, overlays, película, CRT, luz,
   sonido. Si tu búsqueda encaja con ACIDBITE y no eliges nada de allí, justifícalo.
4. **No copies lo que ya usa otro plugin** (el buscador marca «ya lo usa: …» y lo pone un poco más abajo). Úsalo
   solo si es claramente lo mejor y dilo.
5. **Si Iker pide «otra», «más variedad» o «no siempre lo mismo»,** no repitas la búsqueda igual. Usa `--mas`,
   otras palabras u otra clase.
6. **La nota no lo es todo.** Una de nota 4 que encaja mejor gana a una de nota 5 que encaja peor. Hay más de 4.000
   con nota 5: la nota no sirve para desempatar.

## 5. Cómo leer un resultado

```
 3. [5/5] tx:tileables/papel/textura_pergamino_envejecido_1058  ★mejor de su familia
    pergamino envejecido ocre con manchas moteadas                      ← qué es (visto a ojo)
    fondo repetible · imagen · 1150×1150 · fondo opaco · modo multiplicar · ocre · antiguo  ← papel, tipo, tamaño…
    usar si: … · evitar si: …                                           ← cuándo conviene
    defectos: …                                                         ← si tiene alguno
    archivo: TEXTURAS/tileables/papel/…jpg                              ← ruta dentro de Biblioteca/
    familia: tile_papel (variantes: --familia tile_papel) · ya lo usa: papelator   (o «sin usar»)
```

**Los ids** dicen de dónde sale cada cosa. Tu build lee por id, resolviendo `archivo` en `indice/indice.json`:

| Prefijo | Qué es |
|---|---|
| `tx:` | procesado y limpio (recortado, repetible, mejorado) |
| `ab:` | ACIDBITE |
| `or:<md5>` | original bit a bit |

## 6. Atajos por necesidad (si no te vale ninguna de `--necesidades`)

| Necesitas | Prueba |
|---|---|
| fondo de papel / superficie | `papel --tileable` · `pared --tileable` · `madera` · `carton` · `grunge --tileable` |
| papel que se pueda doblar o arrugar | `pliegue` · `arrugado` · relieves (50 % gris = neutro, modo superponer) |
| piezas sueltas | `mancha` · `goteo` · `salpicadura` · `cinta` · `pegatina` · `etiqueta` · `borde rasgado` (`--alfa`) |
| suciedad e imperfecciones | `cafe` · `humedad` · `moho` · `foxing` · `huella` · `grapa` · `quemado` · `polvo` |
| trazo a mano | `trazo lapiz` · `rotulador` · `pincel` · `acuarela` · `cera` · `subrayado` · `flecha` |
| luz y elementos | `fuego` · `chispa` · `humo` · `fuga de luz` · `bokeh` · `burbuja` · `lluvia` |
| look de película o analógico | `polvo pelicula` · `rayado` · `grano` · `vhs` · `crt` · `glitch` · `--clase lut` |
| transiciones de vídeo | `transicion` + el material: `transicion papel`, `transicion tinta`, `transicion quemado`, `transicion luz` |
| sonidos | `whoosh` · `golpe` · `papel` · `ambiente` · `riser` (`--clase sonido`) |
| partículas para usar en masa | `--relleno` (chispas y pavesas pequeñas pensadas para fondos con desenfoque) |

Filtros con cualquier campo de la ficha: `--donde 'w>=2000'`, `'color~azul'`, `'medidas.luminancia<0.3'`,
`'video.duracion<=2'`, `'video.loop=True'`. También `--min 4`, `--mejor`, `--clase`, `--sub`, `--json`.
Todo en `buscar.py --help`.

## 7. Si no está

No lo dibujes, no lo descargues y no crees un banco dentro del plugin. Busca con 3 formulaciones distintas y con
`--resumen`. Si de verdad no está, termina tu respuesta con un bloque **«PEDIDO PARA LA BIBLIOTECA:»**: qué, para
qué, formato, tamaño y modo. Iker lo pasa a la conversación de TEXTURAS.

## 8. Reglas permanentes

- **Los plugins funcionan solos, sin Claude y sin internet.** La biblioteca solo se usa al construir; el plugin
  lleva dentro lo que usa.
- **Ningún plugin cambia su resultado sin que Iker lo sepa.** Pasa su prueba exacta antes y después de cada cambio.
- **El material de pago no se redistribuye ni sale de los repos privados.** Es ACIDBITE, Gumroad y todo lo marcado
  con `licencia`.
- **No borres ni muevas nada de esta carpeta.** No toques los zip ni los originales.
- **Ninguna textura se da por buena sin mirarla.**
