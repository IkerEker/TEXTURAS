# Transición por máscara (Track Matte)

**Assets:** `transicion.tipo = mascara` (Cracked Glass, Burning Paper luma mattes, Textile frames, Punch Hole keys,
Cinemarkers Alpha Transitions, Ultimate Paper rips, Super Mixed Media) y `video/transiciones/tinta_4k` de TEXTURAS.

Pistas (de abajo arriba): V1 plano que sale · V2 plano que entra con **Track Matte Key** → V3 · V3 la máscara (no se
ve) · V4 opcional: copia visible en el modo de `modos_acidbite` (fuego en Screen, borde de papel en Normal…).

- `mascara_alfa` → Composite using **Matte Alpha**; `mascara_luma` → **Matte Luma**.
- `transicion.invertir = true` → activar **Reverse** (el hueco es la parte transparente/oscura y crece).
- El plano entrante **empieza a la vez que la máscara**; el saliente dura al menos hasta `transicion.revelado_s`.

Recetas exactas de ACIDBITE (leídas de sus proyectos):
- **Textile:** Matte Alpha; Reverse en 1, 3, 4, 5. Copia visible del Frame en Screen (1, 4–7), Lighten (2) o
  Difference (3, 8). Saliente con Posterize + Wave Warp. Texturas: Grunge en Screen, Textile Texture Animation en Multiply.
- **Punch Hole:** el **saliente** se anida, se congela y se vuelve a anidar; lleva la máscara (Matte Alpha sin Reverse);
  por el agujero se ve el entrante. Copia visible de la Key en Screen / Linear Dodge / Color Dodge / Lighter Color;
  Filmburn en Difference + Invert + Spherize/Lens Distortion.
- **Burning Paper:** luma matte con Reverse; el fuego encima en Screen (recolorear con Hue vs Hue).
- **Cracked Glass:** Matte Alpha; los trozos revelan el entrante.
- **Dissected Alpha** no es transición: es `recorte` (el plano se ve solo dentro de la forma).
