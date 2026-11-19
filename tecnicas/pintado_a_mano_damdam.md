# Texturas pintadas a mano (Studio DamDam, Gumroad)

Material: `video/transiciones/tinta_4k/*` (21 transiciones de 1 s, 8 dibujos/s), `video/transiciones/pintura/*`,
`video/texturas_animadas/*` (papel, grunge, líneas, salpicaduras, sellos, manchas; 12 fps, bucles), `video/elementos/spray/*`.
Detalle y fuentes: `gumroad/ESTADO.md`. El autor: «overlay, displacement map o matte; según cómo se apilen, distinto resultado».

## 1. Transición con mate de luminancia
- Pistas: V1 plano que sale · V2 plano que entra con **Track Matte Luma** → V3 · V3 la transición (oculta).
- Negro = tapa, blanco = deja ver; si entra al revés, **Reverse/Invert**. Para un mate más limpio: Curves o CC Threshold
  y Simple Choker (lo hace el autor). Para precisión, usa los **PNG 4K** (8 fotogramas por transición, sin compresión) a 8 fps.
- Opcional: la transición visible encima en **multiplicar** para ver la tinta, y su `*_textura` en **trama** encima.

## 2. Superposición de papel animado (todo el plano)
- Papel/grunge/líneas **negros → trama**; **blancos → multiplicar**. Opacidad al gusto. Son bucles: se repiten sin salto.
- A 12 fps: pon el resto de la animación con **Posterize Time 12** (o 6) para que todo respire igual.

## 3. Mapa de desplazamiento («tipografía orgánica»)
- Precompón la textura; en el texto/neón: **Displacement Map**, capa = la textura, Luminancia en H y V,
  **pocos píxeles** (≈ 5–25 a 1080p; escala con la resolución), Wrap Pixels Around. Más agresivo: Turbulent Displace suave.
- Neonizador: es el modelo para que los trazos «vibren» como hechos a mano en vídeo.

## 4. Combinar
- Mate de una transición + desplazamiento del texto con la misma textura + papel en trama encima = el look del promo.
- Spray (`t1–t4`, sobre blanco, 0,32 s): **multiplicar** encima del corte o como mate tras umbralizar.

Ritmo: todo esto está animado a mano a 8–12 dibujos por segundo; acelerar con fusión de fotogramas lo estropea:
cambia la velocidad por **saltos** (Posterize Time), no por interpolación.
