# Gumroad · lo que tiene Iker y cómo se usa

19-11-2026. Todo el material de Gumroad de Iker es de **un solo autor: Studio DamDam** (damdam.studio,
`studiodamdam.gumroad.com`). Son texturas y transiciones **pintadas a mano fotograma a fotograma y escaneadas en 4K**
(papel, tinta, spray). Material de pago (el spray es gratuito/«paga lo que quieras»): uso propio, **no redistribuir**.

Fuentes de este documento: las páginas de sus productos en Gumroad, sus **dos proyectos de After Effects** (que vienen con
los packs y están en `originales/neonizador/TEXTURAS/GUMROAD/*.aep`, leídos por dentro) y el análisis de los archivos
que ya hizo TEXTURAS (`catalogo.json`, `video/_tiras/`).

## 1. Qué tiene (y dónde está en el atlas)

| Producto en Gumroad | Lo que tiene Iker | En TEXTURAS (procesado) | Formato |
|---|---|---|---|
| **Textured Transition Pack** (21 transiciones: 7 horizontales, 7 verticales, 7 diagonales + texturas de papel; vendido con «21 mattes») | `TransitionPack4K_Gumroad/Textured_MOVs` (21 + 3 `_Texture`, MP4) y `Textured_PNGs` (las mismas en **PNG 4K sin pérdida**, 8 fotogramas cada una) | `video/transiciones/tinta_4k/{horizontal,vertical,diagonal}` (+ `*_textura`) | MP4 H.264 4K 25 fps con **8 fotogramas distintos por segundo** (cada dibujo dura 3 fotogramas); 1 s. PNG RGBA (alfa opaco) = la versión limpia |
| **Animated Paper Texture Pack + AE Project** (13 bucles + 2 transiciones) | `AnimatedTexturesPack_QuickTimeProRes` (15 .mov) + `GUMROAD_PaperTexturePromo (2).aep` | `video/texturas_animadas/{papel,grunge,lineas,salpicaduras,sellos,manchas}` y `video/transiciones/pintura` | ProRes, **12 fps** reales, 4–10 s, en bucle (salvo Paint Leaks y la transición 2) |
| **Free Spray Paint Textures + AE Project** (4 sprays) | `QuickTime/T1–T4.mov` + `SprayPaintTextrues_Gumroad (1).aep` | `video/elementos/spray/t1–t4` | 25 fps con 12,5 fotogramas distintos/s, 0,32 s, sobre blanco (el producto original también trae PNG con alfa; Iker tiene los .mov) |

**Re-descarga completa (19-11-2026, `Biblioteca/AÑADIDOS/GUMROAD`)** — comparada por md5 (`gumroad/lista_md5_anadidos_2026-11-19.csv`,
`tools/atlas/gumroad_anadidos.py`): de 319 archivos, **187 ya estaban** (los 168 PNG 4K, los 15 bucles de papel y los 4 sprays: idénticos).
**132 son nuevos** (5,1 GB) y van a `originales/gumroad/` (el montaje los copia de AÑADIDOS; los zip no se tocan):

| Nuevo | Qué es | En el atlas |
|---|---|---|
| **21 `Matte_MOVs`** | los mates del autor: ProRes 4444 XQ 4K, 25 fps, 1 s, **RGB negro + ALFA = tinta**, mismos 8 dibujos que la versión texturada | `productos/mates_tinta_4k/` (alfa → luminancia, blanco = tinta cubre; `mates.json` con cobertura por fotograma; hoja `productos/hojas/mates_tinta_4k.jpg`, revisada). Cubre del todo a 0,52 s (diagonales) / 0,40 s (horizontales y verticales) y empieza a descubrir 3 fotogramas después; **vertical_6 nunca cubre entera (máx. 97,6 %)**. Todas arrancan y acaban con algo de tinta: para un corte limpio, recortar el primer y último dibujo |
| **24 `Textured_MOVs` en ProRes** | la calidad original de las transiciones (ProRes 4444 XQ, sin alfa). Lo que tenían los plugins eran MP4 de 2–3 MB | solo en `originales/gumroad/`; `video/transiciones/tinta_4k` sigue igual (los PNG 4K ya eran la versión sin pérdida) |
| **Free Cyanotype Textures** (7 × 10 PNG) | cianotipias pintadas a mano fotograma a fotograma y escaneadas, 1920×1080, opacas (azul de Prusia sobre papel) | `originales/gumroad/cianotipia/`; hoja `gumroad/hojas/cianotipia.jpg`. Uso: multiplicar a pantalla completa a 12 fps, o como mate de luminancia (el azul tapa) |
| **Easy Slit Scan Effect + AE Project** (16 mapas + .aep) | 8 mapas horizontales y 8 verticales: degradados grises animados, 1080×1920 (vertical, para redes), 24 fps, 4 s. El .aep usa **Displacement Map** (15 capas, «Use For Horizontal/Vertical Displacement»), **Simple Choker** y **Camera Lens Blur** | `originales/gumroad/slitscan/`; hoja `gumroad/hojas/slitscan.jpg`. Uso: mapa de Displacement Map (estira la imagen en franjas) o de Time Displacement para slit-scan real |

Sigue sin estar: su pack de 65 glitches CRT (no comprado).

## 2. Cómo dice el autor que se usan

En las tres páginas, lo mismo: **cada clip sirve de tres maneras** — como **superposición (overlay)**, como **mapa de
desplazamiento** y como **capa de mate (matte)** — y «el mismo material da resultados distintos según cómo se apilen
las capas». Del pack de papel: superponer sobre una composición digital limpia para darle aire analógico; usar como
mapa de desplazamiento para tipografía orgánica en movimiento; y como mate para transiciones que imitan papel que se
rasga.

Vídeos del autor (no se han podido abrir desde aquí: YouTube limitó el acceso; pendiente de verlos):
- Promo del pack de papel: https://youtu.be/x6mZW8wEJDE
- **Tutorial**: https://youtu.be/Tf9NZ6m--HI

## 3. Lo que hacen en sus propios proyectos de After Effects (leído del .aep)

`GUMROAD_PaperTexturePromo (2).aep` (composiciones «ANIMATED TEXTURES FOR: AFTEREFFECTS», «13 LOOPABLE TEXTURES + 2
transitions», «USE as OVERLAYs OR MATTeS», «COMBINE», «MIX», «REMIX») y `SprayPaintTextrues_Gumroad (1).aep`
(composiciones `Texture_Overlay` y `Textures_Displacement`). Efectos que usan:

| Técnica | Efectos en su proyecto | Cómo |
|---|---|---|
| **Desplazamiento** («tipografía orgánica») | `Displacement Map` (varias capas) + a veces `Turbulent Displace` | la textura animada como capa de mapa, canal **Luminancia** en horizontal y vertical, **desplazamiento pequeño** (unos 5–25 px en el promo de papel; más fuerte en el spray), «Wrap Pixels Around»; el texto/forma tiembla siguiendo el papel |
| **Ritmo a saltos** | `Posterize Time` a **12 y 6 fps** (papel) y **8 y 6 fps** (spray) | todo lo que se mueve (texto, formas) va al mismo ritmo de animación a mano que la textura |
| **Mate** | `CC Threshold`, `Simple Choker` (Choke Matte), `Curves`, `Invert`, `Brightness & Contrast` | la textura se umbraliza/contrasta para hacer un mate limpio; Invert para cambiar qué tapa; Choke para cerrar el borde |
| **Overlay** | modos de fusión de capa (no legibles del binario) | papel negro → **trama/Screen**; papel blanco → **multiplicar** (lo confirma la medida de TEXTURAS: fondos negro/blanco) |
| Extras de animación | `Echo`, `Fast Box Blur`, `Sharpen` y la expresión «Schmeeer» (estela por movimiento) | estelas y suavizado en el promo del spray |

## 4. Recetas para usarlo (en el atlas: `tecnicas/pintado_a_mano_damdam.md`)

Resumen: transiciones texturadas como **mate de luminancia** (negro tapa, blanco deja ver; Reverse si va al revés) o
encima en multiplicar; papeles animados en **trama** (negros) o **multiplicar** (blancos) todo el plano, a 12 fps; y como
**mapa de desplazamiento** de texto/neón con Luminancia y pocos píxeles; todo a 12/8/6 fps con Posterize Time para que
case con el «hecho a mano».

## 5. Pendiente

- Ver el tutorial y el promo del autor (enlaces arriba) y anotar lo que añadan.
- Leer valores exactos del .aep de SlitScan (cuántos píxeles desplaza) cuando haya un lector de .aep fiable.
- Iker: volver a lanzar `MONTAR_BIBLIOTECA.bat` para que copie los 132 nuevos a `originales/gumroad/`.
