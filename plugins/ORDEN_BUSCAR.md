# ORDEN 3 · Buscar bien en la biblioteca (20-11-2026)

*(Iker: pega el texto de abajo, entero, en la conversación de cada plugin.)*

---

**Orden de Iker, permanente: cambia cómo se busca material en la Biblioteca.** Hasta ahora todos elegíais casi lo
mismo. El buscador viejo, ante empates (hay más de 4.000 recursos con nota 5), devolvía las cosas en el orden del
archivo: salían siempre las primeras y nunca ACIDBITE. Ya está arreglado. Haz esto en orden:

1. **Actualiza y comprueba.**
   - Ejecuta `git -C <Biblioteca>/TEXTURAS pull --ff-only` (o haz doble clic en `Biblioteca/ACTUALIZAR_TEXTURAS.bat`).
   - Comprueba que `python <Biblioteca>/TEXTURAS/tools/atlas/buscar.py --version` dice **v2**.
   - Si trabajas con el repo en la nube, haz `git pull` de `IkerEker/TEXTURAS`, rama `atlas`.
2. **Lee entero `Biblioteca/CLAUDE.md`.** En el repo está en `biblioteca_raiz/CLAUDE.md`. Ese es el método desde
   ahora: abanico con `--ver`, al menos 3 búsquedas desde lados distintos, mirar la hoja, reglas de variedad y
   `--apuntar`.
3. **Actualiza tu `CLAUDE.md`.** En tu bloque «Biblioteca y velocidad», cambia la línea de cómo buscar por esta:
   ```
   - Buscar SIEMPRE con TEXTURAS/tools/atlas/buscar.py v2 y el método de Biblioteca/CLAUDE.md: 2–4 palabras --ver →
     ≥3 búsquedas desde lados distintos + filtro de papel (--tileable/--alfa/--clase) → mirar la hoja → elegir con
     VARIEDAD (varias variantes por efecto, una por familia, ACIDBITE cuenta, no copiar lo que «ya lo usa» otro plugin)
     → --plugin <yo> --apuntar ids. Nunca carpetas/catalogo.json/índice a mano cogiendo los primeros.
   ```
4. **Repasa lo que ya elegiste con el método viejo.** Para cada efecto o función que usa material de la biblioteca:
   1. Rehaz la búsqueda con el método nuevo.
   2. Mira la hoja.
   3. Propón qué añadirías o cambiarías para que tenga variedad de verdad. Como guía: 6–12 variantes por efecto, de
      al menos 3 familias y de más de una colección si las hay.

   **No cambies nada que altere un resultado ya entregado sin el sí de Iker.** Enséñale el antes y el después.
   Lo que estés construyendo ahora, hazlo ya con el método nuevo.
5. **Apunta lo que uses:** `buscar.py --plugin <tu_plugin> --apuntar <ids>`. Así los demás plugins ven que ya está
   cogido.
6. **Informe para Iker**, corto, con una tabla por efecto:
   - cuántas variantes, familias y colecciones tenía antes;
   - cuántas propones ahora;
   - qué búsquedas hiciste;
   - la ruta de las hojas `_busquedas/*.jpg` que miraste.
