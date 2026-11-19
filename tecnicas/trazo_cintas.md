# Trazos reales con cintas enderezadas

`productos/cintas_trazo` (88): filas a lo largo (fila 0 = arranque de la mano), 0 = papel, 255 = tinta. Son las de A
mano byte a byte (`md5_bytes`).
- Elegir por `familia` (aguada, cera, gouache, lapiz, carbon, pincel, brocha, pincel_fino, rotulador, boligrafo).
- Escala con el trazo: columnas por píxel = `mh / medio_ancho_px`; a lo largo, dividir además por `ar`.
- Trazo más largo que la cinta: remates reales (18 %) y el medio en vaivén. Más fino que 2,2 columnas/píxel: usar una
  copia desenfocada a lo ancho.
- Multiplicar (tinta transparente: lápiz, carbón, aguada) o tapar (pintura opaca).
Trazo (plugin) endereza a su manera (`pin_*`, cabeza/cuerpo/cola): puede partir de los mismos originales `or:`.
Trazos sueltos RGBA para pegar: `trazos/<técnica>` de TEXTURAS; anotaciones con alfa: Ultimate Paper `Ink`/`Marker`.
