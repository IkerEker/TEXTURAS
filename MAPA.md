# MAPA · la puerta de entrada al atlas de texturas de Iker

**Para Claude, desde cualquier conversación:** antes de dibujar, generar o pedir una textura, búscala aquí.
Si no está, se añade aquí (nunca un banco suelto dentro de un plugin).

## Dónde está cada cosa

```
Biblioteca/                      (= TEXTURAS_ROOT; la misma en cada ordenador de Iker; nunca en GitHub)
├── TEXTURAS/                    este repo (privado): lo procesado, el índice, los productos, las recetas
├── ACIDBITE/                    el pack ACIDBITE tal cual (190 GB; 01_TRANSICIONES … 07_SONIDO)
├── originales/                  fuentes intactas de los plugins (por repo y ruta; md5 en el MANIFIESTO)
│   └── heredado/neonizador/     los 715 archivos de los que NEONIZADOR construye hoy su plugin/tex
└── generadas/                   lo que se cree a partir de ahora
```
Montar o comprobar en un ordenador: `python TEXTURAS/tools/atlas/montar_biblioteca.py --raiz <Biblioteca> [--acidbite <carpeta del pack>]`.

## Cómo buscar

1. **`indice/indice.json`** (8.154 assets: 3.172 TEXTURAS, 2.925 ACIDBITE, 2.057 originales). Esquema: `indice/ESQUEMA.md`.
   `python3 tools/atlas/buscar.py <palabras> [--clase …] [--sub …] [--modo …] [--colocacion …] [--alfa] [--tileable]`
   Usa las fichas de la revisión: `--min 4`, `--mejor`, `--familia …`, `--ficha <id>`, `--json`; oculta REHACER/sustituidos (`--todo`).
2. **Mira la hoja** (`hoja` de cada asset) con Read antes de elegir. Ninguna textura se da por buena sin mirarla.
3. **Cómo se usa:** `tecnicas/` (recetas) · `acidbite/COMO_LO_USA_ACIDBITE.md` · `CLAUDE.md` (tabla de TEXTURAS).
4. **Nombres:** `indice/nombres.json` traduce alias (inglés de ACIDBITE, nombres de plugins) al nombre oficial.

## Qué hay (por necesidad)

| Necesitas… | Mira |
|---|---|
| papel, superficie, madera, grunge, líquidos repetibles (con mm) | `tileables/*` · `productos/papel_gris` |
| trazo real (PNG) / cinta enderezada | `trazos/*` · `productos/cintas_trazo` |
| manchas, goteos, salpicaduras, imperfecciones, bordes, pliegues | `manchas/*` · `productos/piezas_neonizador/*` · `imperfecciones/*` · `bordes/*` · `pliegues/*` |
| fuego, chispas, humo, burbujas, moho, gotas | `luz_y_elementos/*` · `productos/piezas_neonizador/*` |
| cinta adhesiva, rotulador/tinta de anotación, hoja plegada 4K | ACIDBITE Ultimate Paper `Toolkit` (`--clase imperfecciones --sub cinta_adhesiva`, `trazos/*_anotacion`, `pliegues/hoja_4k`) |
| transiciones de vídeo (luz, quemado, máscara, glitch, VHS, papel, tela, túnel…) | `--clase video --sub transiciones/` (ACIDBITE) · `video/transiciones/*` (TEXTURAS) |
| look película / analógico / CRT | `--sub pelicula/` · `--sub analogico/` · `superposiciones/*` |
| elementos animados, marcadores, fondos en movimiento | `--sub elementos/` · `--sub fondos/` · `video/elementos/*` |
| sonidos (whoosh, golpes, risers, ambientes…) | `--clase sonido` |
| LUT de película por cámara | `--clase lut` |
| mapas de relieve / desplazamiento (128 = neutro) | campo `desplazamiento` · `productos/sellos_relieve` |

## Para los plugins

**Orden permanente para cada plugin (biblioteca única + velocidad/GPU): `plugins/ORDEN_PLUGINS.md`.**

- La biblioteca **solo se usa al construir**; el `.ccx` lleva dentro lo que usa y funciona sin Claude ni internet.
- Cada plugin lee por **id** con `TEXTURAS_ROOT`: su tabla exacta, en su orden, en `plugins/<plugin>/uso_id.json`.
- Originales por `or:<md5>` (bit a bit); productos por `tx:`; AcidBite por `ab:`.
- Antes y después de cambiar de origen: su prueba exacta (ficha §6).

## Documentos

`DECISIONES.md` (cómo y por qué se unió todo) · `TRASPASO.md` · `acidbite/ESTADO.md` · `gumroad/ESTADO.md` (packs de Studio DamDam: qué hay y cómo los usa su autor) · `plugins/README.md` y
`CONCILIACION.md` · `indice/cruce_acidbite.md` (qué aporta AcidBite y qué sigue faltando) · `productos/README.md`.
Material de pago (ACIDBITE, Gumroad): uso propio, **no redistribuir**; repo privado.

## collage/ (19-11-2026)
475 piezas recortadas para collage (papeles, cintas, etiquetas, pegatinas, notas, pintura, gel, restos de adhesivo, grafito). Ver `collage/README.md`.

## revision/ (noche 19→20-11-2026): revisión 100 % a ojo
Cada asset de `indice/indice.json` lleva ahora un campo `revision` con su ficha: qué es, nota 1–5, defectos,
familia y variante, en qué se diferencia, uso, modo, usar si / evitar si, color, orientación, estilo, contenido,
comportamiento (vídeo) y medidas. 8318 vistos a ojo; 713 con ficha sin vista (658 sonidos no escuchados,
`audio_revisado: false`; 55 plantillas/proyectos de programa). Empieza por `revision/RESUMEN.md`;
`A_REHACER.md` (21), `NO_VISTOS.md`, `FICHAS.json` (todas juntas) y `familias.json`.
Regenerar: `tools/atlas/revision_sin_vista.py` y luego `tools/atlas/revision_resumen.py --indice`.

**Rehechas (20-11-2026):** las 21 marcadas REHACER están resueltas. 17 piezas de `productos/piezas_neonizador` se
rehicieron con el mismo nombre (burbujas completas, tiles de espuma repetibles sin cruz, gotas enteras, goteo sin croma):
detalle y origen en `productos/piezas_neonizador/REHECHAS.json`, antes/después en `productos/hojas/rehechas_2026-11-20.jpg`,
scripts en `tools/atlas/rehacer/`. Las copias exactas de NEONIZADOR siguen como `or:` heredado con `sustituido_por`.
