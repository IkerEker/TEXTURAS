# ORDEN 3 · Mejoras de la Biblioteca y cómo usarlas desde hoy (20-11-2026)

*(Iker: pega todo lo que hay debajo de la línea en la conversación de cada plugin: NEONIZADOR, NEONIZADOR vídeo,
PAPELATOR, A mano, Analog FX, Trazo, Cartelator y los nuevos. Es el mismo texto para todos.)*

---

**Orden de Iker, permanente.** La Biblioteca ha mejorado y desde hoy **tienes que usar estas mejoras**. Hasta ahora
todos los plugins elegíais casi siempre el mismo material. La causa era el buscador. Lee esto entero, haz los
pasos en orden y termina con el informe del final.

## Qué ha mejorado

### 1. El buscador nuevo (`TEXTURAS/tools/atlas/buscar.py` v2)

**Antes.** Más de 4.000 recursos tienen nota 5. Ante ese empate, el buscador los devolvía en el orden del archivo.
Salían siempre los mismos, y ACIDBITE (2.925 recursos de pago) no aparecía nunca. Además exigía todas las palabras
exactas: «papel viejo» no encontraba «antiguo», «envejecido» ni «vintage».

**Ahora:**
- **Ordena por lo que encaja** con la ficha revisada a ojo de cada recurso: qué es, familia, clase, uso, color,
  estilo. Las palabras raras pesan más que las comunes.
- **Entiende sinónimos** (más de 560 palabras en `indice/sinonimos.json`), inglés, plurales, género y frases como
  «cinta adhesiva» o «fuga de luz».
- **El objeto manda y el color o el tamaño matizan.** «goteo rojo» trae goteos, primero los más rojos. Si ninguno es
  rojo, lo avisa: es una pieza que se recolorea.
- **Devuelve un ABANICO de 12 opciones buenas y distintas:**
  - una por familia;
  - repartidas entre TEXTURAS, ACIDBITE y originales;
  - distintas de aspecto;
  - con algo de azar.

  `--mas` trae otras 12. Medido en 20 búsquedas típicas: antes salían 5,8 familias distintas entre las 12 primeras;
  ahora 10,5. ACIDBITE aparece en casi todas.
- **Hace una hoja de miniaturas.** `--ver` crea un JPG numerado en `Biblioteca/_busquedas/`, para elegir mirando.
- **Marca lo que ya usa otro plugin** («ya lo usa: …») y lo pone un poco más abajo. Con `--plugin <tú> --apuntar <ids>`
  dejas constancia en `Biblioteca/_uso/`.
- **No mezcla lo que no pides.** Esconde las fuentes ya procesadas y las copias. Tutoriales, plantillas, LUT y sonidos
  solo salen si los pides.
- **Más opciones:** `--mapa` (qué hay en toda la biblioteca), `--resumen`, `--familia`, `--parecidos`, `--ficha`,
  `--donde`, `--explicar`.

### 1 bis. Necesidades ya resueltas (lo más rápido, v3)

- **78 necesidades** (fondos, superposiciones, relieves, piezas, trazos, luz, vídeo, sonido, LUT) con su lista hecha:
  5–16 opciones **elegidas mirando una a una**, variadas, y su **hoja de miniaturas ya hecha**.
- `buscar.py --necesidades` (catálogo) · `buscar.py --necesidad pieza_goteo` (opciones + hoja). En scripts:
  `indice/necesidades.json` o `from biblioteca import Biblioteca; Biblioteca().necesidad('pieza_goteo')`.
- Cada recurso tiene ahora **papel** (fondo repetible, superposición, pieza, relieve, transición, máscara, animado,
  sonido, LUT…) y **fondo** (transparente / sobre negro / sobre blanco): `--papel`, `--fondo`, `--papeles`.
- `"goteo | chorreon | drip"` busca varias formas a la vez; `--sin-usar` enseña lo que no usa ningún plugin, y lo
  bueno sin usar sube un poco en todos los abanicos (para darle vida).

### 2. Instrucción en la raíz: `Biblioteca/CLAUDE.md`

Se carga sola al abrir la carpeta Biblioteca. Trae el método de búsqueda, las reglas de variedad, cómo leer un
resultado y atajos por necesidad. **Es la referencia desde hoy.** En el repo está en `biblioteca_raiz/CLAUDE.md`.

### 3. Recortes mejorados: 849 piezas `tx:` limpias

Mismo nombre, mismo tamaño y misma caja. Registro en `revision/recortes_mejorados.json` y en la ficha de cada una
(campo `recorte_mejorado`).

| Qué | Cuántas | Qué se ha arreglado |
|---|---|---|
| Goteos (manchas y piezas de NEONIZADOR) | 452 | sin línea oscura en el contorno y sin escalones |
| Salpicaduras de tinta y de óxido/café | 248 | sin cerco claro |
| Fibras | 65 | sin cerco claro |
| Trazos | 38 | sin cerco claro |
| Bordes de papel | 46 | sin velo de croma en el fondo y sin fibras teñidas de rosa, verde o cian |

Muestra: `revision/recortes_mejorados_antes_despues.jpg`.

**Tu plugin hoy lee sus `or:` exactos, así que nada de esto ha cambiado tu resultado.** Pasarte a un `tx:` mejorado
sí lo cambia: se propone con antes y después y se espera el sí de Iker. Para lo nuevo que construyas, usa
directamente los `tx:` mejorados.

### 4. Fichas completas

- Los 86 recursos dudosos y las 92 correcciones están resueltos.
- Los 658 sonidos están medidos: duración, forma y picos.
- Las 55 plantillas están leídas por dentro, sin abrir el programa.
- Las 384 chispas y pavesas pequeñas están marcadas como «relleno de fondo». Están pensadas para usarlas en masa con
  desenfoque de movimiento: `--relleno`.

## Qué tienes que hacer, en orden

1. **Actualiza y comprueba.**
   - En el PC, ejecuta `git -C <Biblioteca>/TEXTURAS pull --ff-only` (o haz doble clic en
     `Biblioteca/ACTUALIZAR_TEXTURAS.bat`).
   - Si trabajas con el repo en la nube, haz `git pull` de `IkerEker/TEXTURAS`, rama `atlas`.
   - `buscar.py --version` tiene que decir **v3**. Si no, para y díselo a Iker.
2. **Lee entero `Biblioteca/CLAUDE.md`** (o `biblioteca_raiz/CLAUDE.md`). Después ejecuta `buscar.py --mapa` una vez
   para ver todo lo que hay.
3. **Actualiza tu `CLAUDE.md`.** En tu bloque «Biblioteca y velocidad», cambia la línea de cómo buscar por estas,
   tal cual:
   ```
   - Buscar SIEMPRE con TEXTURAS/tools/atlas/buscar.py v3 y el método de Biblioteca/CLAUDE.md: 2–4 palabras --ver →
     ≥3 búsquedas desde lados distintos + filtro de papel (--tileable/--alfa/--clase) → mirar la hoja → elegir con
     VARIEDAD (6–12 variantes por efecto, ≥3 familias, una por familia, ACIDBITE cuenta, no copiar lo que «ya lo usa»
     otro plugin) → --plugin <yo> --apuntar ids. Nunca carpetas, catalogo.json ni el índice a mano cogiendo los primeros.
   - Para lo nuevo, usar los tx: con recorte_mejorado. Pasar un efecto existente de or: a tx: = cambia el resultado
     → antes/después y sí de Iker.
   ```
4. **Usa las mejoras desde ya en todo lo nuevo, empezando por `--necesidades`.** Cualquier efecto, función o variante que estés construyendo o
   vayas a construir se busca y se elige con el método nuevo. No hace falta preguntar.
5. **Repasa lo que ya tienes**, efecto por efecto:
   1. Rehaz la búsqueda con el método nuevo y `--ver`.
   2. Mira la hoja.
   3. Prepara la propuesta: qué variantes añadirías (6–12 por efecto, al menos 3 familias, más de una colección si las
      hay) y qué piezas cambiarías por su `tx:` mejorado.

   **No cambies nada que altere un resultado ya entregado sin el sí de Iker.** Prepara el antes y el después, pasa tu
   prueba exacta y espera.
6. **Apunta lo que usas:** `buscar.py --plugin <tu_plugin> --apuntar <ids>`. Incluye lo que ya usabas, para que los
   demás plugins lo vean.

## Informe para Iker (al terminar, corto)

1. **Comprobación:** «buscar.py v3 ✓» y «CLAUDE.md actualizado ✓».
2. **Tabla por efecto** que use material de la biblioteca:

   | Efecto | Antes: variantes / familias / colecciones | Propuesta: variantes / familias / colecciones | Búsquedas hechas | Hoja mirada (`_busquedas/…jpg`) |
   |---|---|---|---|---|

3. **Piezas que podrían pasar a su `tx:` mejorado:** cuáles y qué cambiaría en el resultado.
4. **Qué necesita su sí** y qué ya has hecho por ser nuevo.
5. **Si falta algo en la biblioteca:** un bloque «PEDIDO PARA LA BIBLIOTECA:» (qué, para qué, formato, tamaño y
   modo).
