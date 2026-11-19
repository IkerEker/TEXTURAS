# Papel de fondo y acabado

- **PAPELATOR:** fondo `_d` (detalle multiplicado), `_ink`, escala real (`tile_mm`). Lo hace él; la biblioteca le da
  los originales (`or:`) intactos y `ancho_real_mm`.
- **NEONIZADOR:** «multiplicar alrededor de la media» `rgb *= 1 + (P/media − 1)·k`, `s = U/260`, repetición en espejo.
  Con tiles reales (`tileable=true`) podría repetir con `wrap: 1` sin simetría visible.
- **A mano:** grano = umbral que se come la tinta en los valles; hoy sintético (256², semilla 11). Candidato real:
  `productos/papel_gris` (128 = plano, `px_por_mm` conocido).
- **Trazo:** soportes sintetizados por fase aleatoria (~10 px/mm supuesto) → `productos/papel_gris` da px/mm real.
- **Analog FX:** tileables cuadrados ecualizados (`physSampler` a ojo) → con `tile_mm` puede fijarse por datos.
- Papeles 9:16 sin repetir: `superposiciones/9x16/*`. Hoja plegada/arrugada a pantalla completa: `pliegues/*`,
  Ultimate Paper `Toolkit/Textures`.
