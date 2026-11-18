# TEXTURAS · guía para Claude

Biblioteca común de Iker: texturas, trazos, manchas, elementos y vídeos **ya limpios, recortados y catalogados**,
sacados de sus plugins de Photoshop (NEONIZADOR, Analog FX, PAPELATOR, A mano, Trazo).
**Regla de oro:** antes de dibujar, generar o pedir una textura en cualquier proyecto, búscala aquí.
Si no está, se añade aquí (ver «Añadir material») y luego se usa; no se crean bancos sueltos dentro de cada plugin.

## Cómo encontrar algo

1. `catalogo.json` → `items[]`: una ficha por archivo (1.678). Campos principales:
   - `archivo`, `id` (= archivo sin extensión), `cat`, `sub`, `carpeta`, `tipo` (`imagen` / `video`)
   - `desc` (qué es, en español), `color`, `color_medio` [r,g,b], `w`, `h`, `alfa` (PNG con transparencia)
   - `modo`: modo de fusión recomendado en Photoshop
   - Tileables: `tileable: true`, `costura` [x, y] (≤ 1 = invisible), `mm_por_px` y `tile_mm` cuando se conoce la
     escala real (papeles, superficies, maderas: vienen de PAPELATOR), `proceso`, `aviso` si la costura puede notarse
   - Recortes: `recorte` (caja en la foto original), `pieza`/`piezas` (trazos separados de una lámina), `tamano_real_mm`
   - `origen`: `ruta` y `repo` del original, `sha1`, `copias` (rutas duplicadas en otros repos)
   - `usado_en`: qué plugin lo usa ya y cómo
   - Vídeo: `fps`, `fps_efectivo` (fotogramas distintos por segundo), `a_saltos`, `duracion`, `fondo`, `comportamiento`,
     `transicion` (cuándo cubre y descubre), `loop`, `version_loop`, `velocidad`, `modo`, `procedencia`
2. `CATALOGO.md`: lo mismo en tablas por carpeta, para leer rápido.
3. `hojas/<carpeta>.jpg`: hoja de contactos de cada carpeta (transparencias sobre damero, tileables repetidos 2×2).
   **Mírala con Read antes de elegir**: la descripción no sustituye a ver la textura.

```python
import json
items = json.load(open('catalogo.json'))['items']
papeles = [e for e in items if e['carpeta'] == 'tileables/papel']
grandes_rgba = [e for e in items if e['cat'] == 'trazos' and e['sub'] == 'carbon' and e['w'] > 1000]
transiciones = [e for e in items if e['tipo'] == 'video' and 'transicion' in e]
```

## Qué hay y cuándo usarlo

| Necesitas… | Carpeta | Formato | Modo |
|---|---|---|---|
| Fondo de papel que se repita (folio, acuarela, kraft, arroz, milimetrado, pentagrama…) | `tileables/papel` | JPG tileable, escala en mm | Multiplicar sobre el arte o Normal como fondo |
| Pared, ladrillo, hormigón, azulejo, granito, asfalto, acero, óxido | `tileables/superficies` | JPG tileable (aparejos con nº entero de piezas) | Normal / Multiplicar |
| Madera, OSB, aglomerado, cartón | `tileables/madera_y_carton` | JPG tileable | Normal |
| Vidrio, plástico, lluvia por DELANTE del arte | `tileables/vidrios_y_plasticos` | JPG sobre negro | Trama |
| Frotado de gouache/óleo, aguada, acuarela | `tileables/pintura` | JPG tileable | Normal / Multiplicar |
| Grunge, tinta impresa, fotocopia, ruido | `tileables/grunge` | JPG tileable | Multiplicar |
| Rayado de grafito o carbón | `tileables/grafito_y_carbon` | JPG tileable | Multiplicar |
| Agua, espuma, mármol líquido, cáusticas | `tileables/liquidos` | JPG tileable | Trama / Superponer |
| Las mismas texturas en 9:16 a pantalla completa (sin repetir) | `superposiciones/9x16/<tipo>` | JPG original | Multiplicar / Superponer |
| Película con polvo y rayas, VHS | `superposiciones/pelicula_polvo_y_rayas`, `vhs` | PNG RGBA + `_trama.jpg` | Normal / Trama |
| Un trazo suelto real (lápiz, carbón, cera, rotulador, boli, pincel, gouache, óleo, aguada) | `trazos/<técnica>` | PNG RGBA recortado, color real | Normal (recolorear: bloquear transparencia y rellenar) |
| Mancha de pincel, mancha grande, mancha de tinta | `manchas/pincel`, `pincel_grandes`, `tinta` | PNG RGBA | Normal |
| Goteo de pintura que cuelga | `manchas/goteos/<clase>` | PNG RGBA, raíz ARRIBA (ver su README) | Normal |
| Café, agua, humedad, grasa, óxido de clip, foxing, quemadura, cera… | `imperfecciones/<tipo>` | PNG RGBA | Multiplicar o Normal |
| Grapas, clip, pinza, sello en seco, hendiduras de escritura | `imperfecciones/<tipo>` (`*_relieve.png`) | gris, 50 % = neutro | Superponer / Luz suave |
| Hoja doblada 1–6 veces, arrugada, muy arrugada | `pliegues/<grupo>` | gris de hoja completa, 50 % = plano | Superponer / Luz suave |
| Borde rasgado, cortado, viejo, cartón, espiral, esquinas | `bordes/<tipo>` (`C_*` = esquinas) | PNG RGBA | Normal |
| Fuego, chispas, brasas, humo, fugas de luz, burbujas, espuma, moho | `luz_y_elementos/<tipo>` | PNG RGBA (transparencia real) + `_trama.jpg` (original sobre negro) | Normal o el `_trama` en Trama |
| Transición de tinta 4K (cubre y descubre) | `video/transiciones/tinta_4k/<dirección>` | MP4 4K 25 fps (8 fotogramas distintos/s) | Máscara de luminancia / mate |
| Papel animado a saltos, grunge, salpicaduras, sellos, líneas | `video/texturas_animadas/<tipo>` | MP4 1080p 12 fps, en loop | Multiplicar (blanco) / Trama (negro) |
| Humo, tinta en agua, espuma, burbujas, fuego blanco, spray | `video/elementos/<tipo>` | MP4 (+ `_loop.mp4` que enlaza sin salto) | Trama sobre negro |

Tiras de fotogramas de cada vídeo: `video/_tiras/`.

## Formatos y convenciones

- **PNG RGBA**: alfa = cobertura real (pincel seco, aguadas y bordes parciales se conservan), RGB = color del trazo
  **descontaminado** del fondo (sin halo blanco, negro ni verde). Recortado a su contenido con un pequeño margen.
- **`*_trama.jpg`**: el original sobre negro, misma caja que su pareja PNG. Úsalo en Trama si quieres la luz tal cual.
- **Tileables JPG** (calidad 95, 4:4:4): luz de la toma aplanada, cosidos con corte de costura óptimo (detalle) y fundido
  (bajas frecuencias). Patrones (cuadrículas, rayados, isométricos) y aparejos (ladrillo, azulejo, adoquín) miden un
  número entero de periodos para que las líneas casen. `tile_mm` = tamaño real del tile cuando se conoce.
- **Relieves y pliegues**: escala de grises con 50 % = sin efecto.
- Nombres: `<descripción>_<nnnn>[_<pieza>].<ext>` (nnnn = nº de fuente, estable entre regeneraciones).
- Los originales **no** están aquí: siguen en su repo (`origen.repo` / `origen.ruta`). Este repo guarda solo lo procesado.

## Usarlo desde un plugin

No metas TEXTURAS entero en un plugin (≈2,5 GB). Copia en el build del plugin solo lo que use, por `id`:
```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/IkerEker/TEXTURAS.git
cd TEXTURAS && git sparse-checkout set tileables/papel manchas/goteos   # solo esas carpetas
```
Después redúcelo al tamaño que necesite el plugin (como hacen PAPELATOR y Trazo con sus `.bin`).

## Avisos

- 13 tileables con `aviso`: plásticos arrugados y cáusticas con brillos largos; la costura puede verse en el cruce.
- `procedencia` «Gumroad»: packs de pago, uso propio, **no redistribuir** (el repo debe ser privado).
- No incluido a propósito: ESTILO (dataset de ilustración), `neonizador/MUESTRAS` (vídeos de referencia de otros
  artistas), los fotogramas PNG de las transiciones de Gumroad (están como vídeo) y las fotos de `GOTAS/`
  (están procesadas en `manchas/goteos`). Lista completa en `catalogo.json` → `omitidos`.

## Añadir material

1. Sube las fotos/vídeos a una carpeta de cualquier repo de Iker (o aquí, en `_entrada/`).
2. Regenera con `tools/` (instrucciones en `tools/README.md`): inventario → clasificar (añade la regla o la fila en
   `clasificar.py`) → `procesar.py` → `video_proc.py` → `hojas_salida.py` → `construir_catalogo.py`.
3. Revisa las hojas de contactos de lo nuevo antes de subir. Nunca des por buena una textura sin mirarla.
