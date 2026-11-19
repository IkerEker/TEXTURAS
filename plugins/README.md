# plugins/ · cómo usa cada plugin las texturas

Fichas escritas por la conversación de cada plugin (19-11-2026) con el mismo guion. Son la base para conectar cada
plugin a la biblioteca común **sin cambiar su resultado**. Aquí se guardan tal cual llegaron; las conclusiones de la
conciliación están en `CONCILIACION.md`.

| Plugin | Ficha | Anexos | Cómo lleva las texturas | Prueba de «no cambia nada» |
|---|---|---|---|---|
| A mano | `a-mano.md` | `a-mano.json` | base64 de 8 bits dentro de `main.js` (cintas de trazo, sellos de grumo, grano sintético) | los dos módulos generados salen byte a byte |
| Cartelator | `cartelator.md` | — | **no usa ninguna textura** hoy (todo procedural) | sha256 del `main.js` empaquetado |
| Analog FX | `analog-fx.md` | — | `.bin` crudos en `plugin/textures/` + `textures.json`, y `drips/drips.bin`; leídos de la carpeta del plugin | (ver su apartado 6) |
| NEONIZADOR (Photoshop) | `neonizador.md` | `neonizador/assets.json`, `fuentes.json`, `huellas.json`, `golden.js` | 287 `.bin` crudos (L/LA/RGB/RGBA) + `index.json` en `plugin/tex/`, leídos de la carpeta del plugin | md5 de cada `.bin`; huellas de 49 efectos × 3 intensidades (`golden.js`) |
| NEONIZADOR (vídeo / After Effects) | `neonizador_video.md` | `neonizador/anexo_video.json` | los mismos `.bin`, copiados al panel CEP | sha256 de `index.json` y de los `.bin`; 49 huellas a intensidad 0,6 |
| PAPELATOR | `papelator.md` | `papelator/anexo.json` | 822 PNG de 8 bits + 6 JSON en `plugin/assets/`, leídos al ejecutar | md5 de píxeles de los 822 PNG + md5 de los 6 JSON + 60 renders |
| Trazo | `trazo.md` | (anexo dentro) | 20 `.bin` TRZ1 (cabecera JSON + planos uint8) en `plugin/textures/`, leídos de la carpeta del plugin | md5 de los `.bin` (reproducibilidad del build sin verificar) + renders `tools/run.js` con semilla |

Regla común a todos: **la biblioteca alimenta la construcción, no la ejecución**. Cada plugin sigue llevando dentro
del `.ccx` lo que usa y funciona sin internet ni Claude.
