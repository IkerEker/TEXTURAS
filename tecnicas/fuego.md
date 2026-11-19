# Fuego, pavesas y humo

- **Llamas** `productos/piezas_neonizador/fuego/llamas` (lengua 14, masa 7, base 3): RGBA, alfa = luz; `medidas.lean`, `base_x`.
  NEONIZADOR usa solo la silueta (alfa) y colorea por distancia con su LUT.
- **Pavesas** (267) y **chispas** (128, giradas a horizontal, con `len` y `ang`): sumar luz (trama).
- **Humo** (4, LA): muy tenue al fondo.
- Llamas grandes con color: `luz_y_elementos/fuego` (TEXTURAS, unmultiply).
- **Vídeo:** Burning Paper (fuego 4K con alfa, 48 fps) en trama; recolorear con Hue vs Hue.
- Quemaduras: `productos/piezas_neonizador/quemado` (9) y `imperfecciones/quemadura*` de TEXTURAS.
Dos métodos de alfa conviven: NEONIZADOR `clip((max−0,03)/0,72)^0,85` y TEXTURAS `from_black` (unmultiply). El campo
`metodo` dice cuál; para NEONIZADOR bit a bit, el suyo.
