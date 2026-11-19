# collage/ · piezas para collage recortadas (19-11-2026)

De `Biblioteca/AÑADIDOS/COLLAGE` (251 imágenes generadas por Iker con Gemini sobre fondo liso; 4 duplicadas exactas).
**475 piezas** PNG RGBA, una por objeto, recortadas a su contenido. Catálogo: `catalogo.json` (ficha por pieza) y `CATALOGO.md`.
Hojas de revisión: `hojas/<familia>.jpg` (cada pieza sobre damero, negro y magenta).

- **Opacos** (papeles, cintas de papel/tela/vinilo, etiquetas, pegatinas, notas, pintura): alfa = cobertura; bordes rasgados
  y fibras con alfa parcial; color descontaminado del gris del fondo. La **sombra de contacto va aparte** (`*_sombra.png`,
  negro + alfa, misma caja), nunca dentro de la pieza. La sombra que cae *sobre* la propia pieza (bajo un doblez) sí es pieza.
- **Translúcidos / transparentes** (celo, cinta ámbar, papel de seda, gel, restos de adhesivo): alfa mínima respecto al
  fondo medido: dejan ver lo que haya debajo. Úsalos en Normal.
- **Grafito**: hoja entera; RGBA (papel = transparente) y `_multiplicar.jpg` (papel = blanco puro).
- Cuadernos: los agujeros de la perforación son agujeros. Etiquetas arrancadas: capas finas semitransparentes.

**Descartadas** (Iker, 19-11-2026): washi tape rosa/gris/verde de las imágenes 90, 104, 129 y 195 — el papel casi del
color del fondo no se separa bien. Lista en `_trabajo/revision.json`.

Originales en `Biblioteca/originales/collage/` (manifiesto `originales/MANIFIESTO.json` → `collage`).
Regenerar: `python3 tools/atlas/collage.py <AÑADIDOS/COLLAGE>` → `python3 tools/atlas/collage_catalogo.py`.
Tabla de qué es cada imagen: `tools/atlas/collage_tabla.py`.
