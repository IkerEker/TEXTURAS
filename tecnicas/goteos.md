# Goteos que cuelgan

- `productos/piezas_neonizador/goteos/*` (NEONIZADOR): LA/RGBA, **raíz arriba**, con `medidas` `ax` (posición del cuello 0–1),
  `sw` (ancho del cuello px), `bw` (gota), `len`, `wob` (ondulación), `cont` (continuidad), `crack`.
  Clases gruesa, fina, ondulada, agrietada, gota, mancha, borde, sueltos.
- `manchas/goteos/<clase>` (TEXTURAS, 219, clases de Analog FX: lágrima, fina, serpenteante, seca, impacto, suelta).
- Uso (NEONIZADOR `GT.bajoLetras`): elegir el de proporción largo/ancho más parecida, escalar `sw` al ancho pedido,
  estirar en vertical ≤ ×1,4, colorear con el color de la letra usando el gris como brillo.
- A mano hace sus chorretones por código: estos son el material real si algún día los quiere.
