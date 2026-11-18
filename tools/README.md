# tools · cómo se genera TEXTURAS

Requisitos: Python 3 con numpy, scipy, Pillow (y opencv opcional), y ffmpeg/ffprobe.
Los repos de origen se clonan uno al lado de otro en una carpeta (p. ej. `~/fuentes/neonizador`, `~/fuentes/papelator`…)
con `git clone --depth 1`. `TEXTURAS` es el destino.

```bash
F=~/fuentes; T=~/TEXTURAS; W=~/trabajo; mkdir -p $W
python3 inventario.py $F $W/inventario.json            # hash, medidas, fondo, costura de cada imagen y vídeo
python3 roles.py $W/inventario.json $W/inv2.json         # fuente / procesado / referencia / ruido + duplicados
python3 hojas.py $W/inv2.json $F $W/hojas                # hojas de las fuentes (para revisar y clasificar)
python3 clasificar.py $W/inv2.json $F $W/hojas/indice.json $W/clasif.json
python3 procesar.py $W/clasif.json $F $T $W/res [categoría]   # reanudable; una categoría o todas
python3 video_proc.py $W/inv2.json $F $T $W/videos_cat.json
python3 hojas_salida.py $T $T/hojas
python3 construir_catalogo.py $W/res $W/videos_cat.json $W/inv2.json $T
```

- `tx.py`: la biblioteca de procesado (recorte sobre papel, sobre negro y sobre croma con color descontaminado;
  separación de piezas; tileables con corte de costura óptimo y periodos; relieves; pliegues; nombre de color).
  Reúne lo que ya hacían `PAPELATOR/tools/common.py` e `imperf_lib.py` y lo generaliza.
- `clasificar.py` lee (sin ejecutarlas) las tablas de los plugins: papeles y escalas de `build_papers.py`, superficies de
  `build_surfaces.py`, maderas de `build_boards.py`, vidrios de `build_overlays.py`, imperfecciones de `build_imperf*.py`,
  pliegues de `build_folds.py`, bordes de `bordes_sets.json`, técnicas de `A mano/tools/extract_textures.py` y de Trazo.
  Las 99 texturas 9:16 de Trazo se clasificaron a ojo (tabla `V916`).
- Para material nuevo: añade su regla en `regla()` de `clasificar.py`, vuelve a procesar solo esa categoría y revisa su hoja.
