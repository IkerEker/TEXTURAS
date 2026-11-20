# Revisión 100 % de la Biblioteca — resumen

Revisión hecha a ojo, archivo por archivo, con hojas de contactos (imágenes enteras + recorte 1:1; vídeos con tira de 12 fotogramas + recorte 1:1). Noche del 19 al 20-11-2026. Audio no escuchado (`audio_revisado: false`, se copia lo que ya se sabía en `audio_conocido`).

## Recuento

| Colección | En el índice | Vistos a ojo | Ficha sin vista (sonido, plantillas) | Sin ficha |
|---|---:|---:|---:|---:|
| ACIDBITE | 2925 | 2215 | 710 | 0 |
| TEXTURAS | 3668 | 3668 | 0 | 0 |
| originales | 2438 | 2435 | 3 | 0 |
| **Total** | **9031** | **8318** | **713** | **0** |

Vistos a ojo + ficha sin vista + sin ficha = 8318 + 713 + 0 = 9031 (total del índice: 9031).

Sin vista: 658 sonidos de ACIDBITE (no se escuchan: `audio_revisado: false`, con lo que ya se sabía en `audio_conocido`) y 55 plantillas o proyectos de programa (.drt, .prfpset, .mogrt, .prproj, .aep), que no son imagen ni vídeo.

- Sin ficha: **0** (lista en `NO_VISTOS.md`).
- Fichas de ids que ya no están en el índice: 0.
- Ids repetidos en el índice (mismo contenido md5 en dos rutas, comparten ficha): 4 → `or:9fac33d56870c26d250702899c647efc`, `or:ca608e84f6645839f5ff2d3b21579d5f`, `or:c619621ca98345da2215a43385ad4498`, `or:080b9643beb82bc6d1cf9fb44ee2a4da`
- Familias declaradas: 270; usadas en fichas: 269.

## Calidad (1 = no usar … 5 = trabajo final sin tocar)

| Colección | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| ACIDBITE | 0 | 11 | 76 | 365 | 1763 |
| TEXTURAS | 41 | 241 | 769 | 1671 | 946 |
| originales | 0 | 260 | 291 | 354 | 1530 |
| **Total** | **41** | **512** | **1136** | **2390** | **4239** |

## Lo mejor (20 primeros «mejor de su familia» con nota 5)

- `tx:bordes/acuarela/borde_gris_claro_0508` — franja de papel gris claro cuyo borde superior está rasgado con fibras largas, despeinadas y abundantes (tira_borde_rasgado_blanco)
- `tx:bordes/artesanal/borde_papel_artesanal_0458` — papel artesanal crema con rasgado muy fibroso y un hueco (tira_borde_artesanal)
- `tx:bordes/bisel/borde_azul_0538` — cartulina azul marino con rasgado blanco ancho y fibras largas (tira_borde_color_fibra)
- `tx:bordes/bisel/borde_papel_azul_rasgado_0459` — cartulina azul eléctrico con rasgado blanco fino y fibras; fieltro visible (tira_borde_color_fibra)
- `tx:bordes/blanco/borde_blanco_0533` — hoja blanca arrancada con dientes muy rotos y jirones (tira_borde_perforado)
- `tx:bordes/blanco/borde_gris_claro_0524` — papel blanco grueso con mechones de fibra muy largos, enredados y sedosos que salen del rasgado (tira_borde_fibra_larga)
- `tx:bordes/blanco/papel_blanco_rasgado_0579` — papel blanco con rasgado fino, limpio, con doble capa blanca visible (tira_borde_rasgado_blanco)
- `tx:bordes/carton/borde_carton_corrugado_0453` — cartón kraft con la capa superior pelada en el canto, fibras y manchas (tira_borde_carton)
- `tx:bordes/carton/borde_naranja_0530` — cartón tostado con canto en escalones quemados y grietas, muy detallado (tira_borde_quemado)
- `tx:bordes/carton/borde_naranja_0552` — papel tostado con canto en almenas oscurecidas y grietas (tira_borde_quemado)
- `tx:bordes/carton/carton_corrugado_desgarrado_0478` — cartón ondulado desgarrado con la onda abierta y una fibra larga suelta (tira_borde_carton)
- `tx:bordes/espiral/borde_cuaderno_espiral_rasgado_0455` — hoja blanca de cuaderno de espiral arrancada: agujeros redondos limpios con lengüetas rotas (tira_borde_perforado)
- `tx:bordes/gris/cartulina_gris_rasgada_0477` — cartulina gris con rasgado ondulado y capas claras bien definidas (tira_borde_gris_fibra)
- `tx:bordes/kraft/papel_kraft_rasgado_0586` — papel kraft naranja con rasgado de fibras largas y tiesas (tira_borde_kraft)
- `tx:bordes/periodico/textura_macro_papel_rasgado_0603` — papel reciclado beige en macro con fibras muy visibles (tira_borde_reciclado)
- `tx:bordes/viejo/papel_antiguo_rasgado_0576` — papel ocre antiguo con canto desconchado en escamas levantadas (tira_borde_antiguo)
- `tx:bordes/washi/borde_gris_claro_0507` — papel blanco grueso con mechones largos, sedosos y curvos hacia la derecha (tira_borde_fibra_larga)
- `tx:imperfecciones/acida/migracion_acida_0863` — migración ácida rectangular con borde oscuro muy marcado y manchas (migracion_acida)
- `tx:imperfecciones/agua/mancha_agua_seca_0904` — cerco de agua ondulado con borde marcado y legible (mancha_agua)
- `tx:imperfecciones/cafe/cerco_cafe_0853` — cerco de taza de café grueso con borde oscuro, marca de goteo y salpicaduras (cerco_cafe)

Hay 188 elementos marcados como «mejor de su familia» en total (campo `mejor_de_familia` en `FICHAS.json` y en el índice).

## No recomendados (nota 1–2): 553

Por familia (las 25 con más):

- or_heredado_neonizador: 260
- pieza_pavesa: 103
- pieza_chispa: 33
- residuo_adhesivo: 22
- pieza_gota_agua: 16
- pieza_goteo_fino: 13
- tile_916: 9
- tile_grunge: 9
- pieza_burbuja: 9
- pieza_moho_manchita: 8
- pieza_salpicadura_oxido: 8
- pieza_goteo_ondulado: 7
- co_cinta_transparente: 7
- ab_optico: 6
- goteo_fino: 6
- gota_suelta: 5
- espuma_tile: 4
- tile_gouache_calido: 3
- tile_gouache_frio: 3
- trazo_grafito: 3
- co_gel: 3
- gota_3d: 2
- pieza_goteo_blanco: 2
- co_grafito: 2
- goteo_seco: 1

Lista completa: buscar `"calidad": 1` o `2` en `FICHAS.json`.

## Correcciones (lo visto contradice el nombre o el índice): 93

- `TEXTURAS/bordes/C_vieja/fragmentos_papel_envejecido_cuadricula_0499.png` — CORRECCIÓN: no tiene cuadrícula visible pese al nombre
- `TEXTURAS/bordes/bisel/borde_azul_0506.png` — CORRECCIÓN: el rasgado está en el borde inferior, no arriba como el resto
- `TEXTURAS/bordes/gris/borde_papel_rasgado_verde_vivo_0452.png` — CORRECCIÓN: no es verde, es gris
- `TEXTURAS/imperfecciones/uv/textura_circular_papel_quemado_0970.png` — nombre dice «papel quemado» pero es un amarilleo suave, no quemadura (corrección)
- `TEXTURAS/superposiciones/9x16/aguada/aguada_1192.jpg` — el nombre dice aguada pero es pasta/gouache con relieve de brocha (corrección)
- `TEXTURAS/superposiciones/9x16/grafito/grafito_1162.jpg` — el nombre dice grafito pero son pinceladas de pintura sobre lienzo (corrección)
- `TEXTURAS/superposiciones/9x16/veta/veta_1216.jpg` — no es 9:16 aunque esté en la carpeta 9x16 (corrección)
- `TEXTURAS/tileables/grafito_y_carbon/grafito_gris_claro_1162.jpg` — nombre dice grafito pero es pintura sobre lienzo (corrección)
- `TEXTURAS/tileables/papel/papel_milimetrado_azul_1006.jpg` — el nombre dice milimetrado pero es cuadrícula simple de cuadro grande (corrección)
- `TEXTURAS/tileables/pintura/color_gris_1158.jpg` — el nombre dice gris pero es muy colorida (corrección); repetición evidente
- `TEXTURAS/tileables/pintura/color_gris_1166.jpg` — el nombre dice gris pero es verde agua (corrección); repetición evidente
- `TEXTURAS/tileables/pintura/color_gris_1167.jpg` — el nombre dice gris pero es azul verdoso (corrección); repetición evidente
- `TEXTURAS/tileables/pintura/color_gris_1188.jpg` — nombre dice gris pero es oliva y azul (corrección); repetición evidente
- `TEXTURAS/tileables/pintura/color_gris_1224.jpg` — nombre dice gris pero es azul cobalto (corrección); repetición evidente
- `TEXTURAS/tileables/pintura/color_gris_1226.jpg` — nombre dice gris pero es turquesa (corrección); repetición evidente
- `TEXTURAS/tileables/pintura/color_naranja_1189.jpg` — nombre dice naranja pero es beige grisáceo (corrección); repetición visible
- `TEXTURAS/tileables/pintura/color_naranja_1219.jpg` — nombre dice naranja pero es crema y gris (corrección); repetición evidente
- `TEXTURAS/video/elementos/fuego_y_humo/llamas_y_humo_blancos_monocromo_que_ocup_0006.mp4` — corrección: el catálogo dice fondo gris claro y modo multiplicar, pero se ve fuego blanco sobre negro: debe usarse en trama
- `TEXTURAS/video/transiciones/pintura/transition_texture2.mp4` — corrección: el catálogo dice diagonal pero el brochazo es horizontal y avanza de arriba abajo
- `TEXTURAS/video/transiciones/tinta_4k/horizontal/horizontal_7.mp4` — a saltos (8 fps); corrección: no barre en horizontal sino que cierra desde los lados hacia el centro
- `TEXTURAS/video/transiciones/tinta_4k/vertical/vertical_3.mp4` — a saltos (8 fps); corrección: los trazos son verticales pero no barren de arriba abajo, aparecen por todo el ancho
- `TEXTURAS/video/transiciones/tinta_4k/vertical/vertical_7.mp4` — a saltos (8 fps); corrección: cierra desde arriba y abajo hacia el centro (tipo telón horizontal)
- `originales/papelator/APOYO/TRAZOS/Ocho pinceladas azules sobre blanco.png` — CORRECCIÓN: el nombre dice ocho pero se ven siete
- `originales/analog-fx-plugin/GOTAS/Goteos de pintura seca sobre negro.png` — CORRECCIÓN: son manchas sueltas con goteo, no goteos desde el borde
- `originales/analog-fx-plugin/textures-src/OTRAS TEXTURAS/TEXTURAS EN 9-16 NO TILEABLES/Gemini_Generated_Image_vw4bpmvw4bpmvw4b.jpg` — CORRECCIÓN: no es 9:16, es casi cuadrado (2072×2048)
- `originales/neonizador/TEXTURAS/GUMROAD/AnimatedTexturesPack_QuickTimeProRes/Texture8_BlackPaper_Stamps.mov` — CORRECCIÓN: el nombre dice BlackPaper pero se ve papel blanco con sellos negros
- `originales/neonizador/TEXTURAS/GUMROAD/TransitionPack4K_Gumroad/Textured_MOVs/Horizontal/H3.mp4` — CORRECCIÓN: rellena por franjas, no barre; duplicado del ProRes H3
- `originales/neonizador/TEXTURAS/GUMROAD/TransitionPack4K_Gumroad/Textured_MOVs/Horizontal/H6.mp4` — CORRECCIÓN: bloques en varios puntos; duplicado del ProRes H6
- `originales/neonizador/TEXTURAS/GUMROAD/TransitionPack4K_Gumroad/Textured_MOVs/Horizontal/H7.mp4` — CORRECCIÓN: cierre tipo telón; duplicado del ProRes H7
- `originales/neonizador/TEXTURAS/GUMROAD/TransitionPack4K_Gumroad/Textured_MOVs/Vertical/V3.mp4` — CORRECCIÓN: rellena por columnas; duplicado del ProRes V3
- `originales/neonizador/TEXTURAS/GUMROAD/TransitionPack4K_Gumroad/Textured_MOVs/Vertical/V6.mp4` — CORRECCIÓN: bloques en varios puntos; duplicado del ProRes V6
- `originales/neonizador/TEXTURAS/GUMROAD/TransitionPack4K_Gumroad/Textured_MOVs/Vertical/V7.mp4` — CORRECCIÓN: entra por arriba y abajo a la vez; duplicado del ProRes V7
- `originales/papelator/NUEVAS/PLIEGUES/PLIEGUES/Textura de pliegues en cuadrícula 4×4.png` — sutil, CORRECCIÓN: se ven 3×4 paneles, no 4×4
- `originales/papelator/SOBREPONER/Textura de vidrio acanalado en gris.png` — CORRECCIÓN: es gris claro, no fondo negro: en trama aclara todo el cuadro
- `originales/papelator/SOBREPONER/Textura de vidrio estriado translúcido.png` — CORRECCIÓN: fondo gris claro, no negro
- `originales/papelator/imperfecciones/Textura Circular de Papel Quemado.png` — CORRECCIÓN: el nombre dice papel quemado pero es una mancha cálida difusa sin carbonizado
- `originales/papelator/BORDES/Borde de papel translúcido rasgado.png` — CORRECCIÓN: fondo negro, no verde
- `originales/papelator/BORDES/Gemini_Generated_Image_46yjm846yjm846yj.jpg` — CORRECCIÓN: tiene fondo azul arriba y verde abajo, no es un borde simple
- `originales/papelator/BORDES/Gemini_Generated_Image_i1b606i1b606i1b6.jpg` — CORRECCIÓN: es un trozo de cartón entero, no solo un borde superior
- `originales/papelator/BORDES/Gemini_Generated_Image_jbxigjjbxigjjbxi.jpg` — CORRECCIÓN: es una tira estrecha, no un borde de página
- `originales/papelator/BORDES/Gemini_Generated_Image_k8uuprk8uuprk8uu.jpg` — CORRECCIÓN: bloque aislado, no borde de página
- `originales/papelator/BORDES/Gemini_Generated_Image_mxqlttmxqlttmxql.jpg` — CORRECCIÓN: tira aislada, no borde de página
- `originales/papelator/BORDES/Gemini_Generated_Image_n2513an2513an251.jpg` — CORRECCIÓN: bloque aislado, no borde de página
- `originales/papelator/BORDES/Gemini_Generated_Image_t4qy3tt4qy3tt4qy.jpg` — CORRECCIÓN: bloque con esquina, no borde completo
- `originales/papelator/BORDES/Gemini_Generated_Image_uu6xw7uu6xw7uu6x.jpg` — CORRECCIÓN: tira aislada, no borde de página
- `originales/gumroad/slitscan/Displacements_Horizontal/D1.mp4` — ninguno; CORRECCIÓN: la desc dice 1080×1920 pero la versión horizontal se ve 16:9 apaisada
- `originales/gumroad/slitscan/Displacements_Horizontal/D2.mp4` — muy oscuro, poco rango; CORRECCIÓN: la desc dice 1080×1920 pero la versión horizontal se ve 16:9 apaisada
- `originales/gumroad/slitscan/Displacements_Horizontal/D3.mp4` — ninguno; CORRECCIÓN: la desc dice 1080×1920 pero la versión horizontal se ve 16:9 apaisada
- `originales/gumroad/slitscan/Displacements_Horizontal/D4.mp4` — ninguno; CORRECCIÓN: la desc dice 1080×1920 pero la versión horizontal se ve 16:9 apaisada
- `originales/gumroad/slitscan/Displacements_Horizontal/D5.mp4` — muy oscuro; CORRECCIÓN: la desc dice 1080×1920 pero la versión horizontal se ve 16:9 apaisada
- `originales/gumroad/slitscan/Displacements_Horizontal/D6.mp4` — oscuro; CORRECCIÓN: la desc dice 1080×1920 pero la versión horizontal se ve 16:9 apaisada
- `originales/gumroad/slitscan/Displacements_Horizontal/D7.mp4` — CORRECCIÓN: la desc dice 1080×1920 pero se ve 16:9 apaisado
- `originales/gumroad/slitscan/Displacements_Horizontal/D8.mp4` — CORRECCIÓN: la desc dice 1080×1920 pero se ve 16:9 apaisado
- `originales/gumroad/TransitionPack4K_Gumroad/Matte_MOVs/Horizontal/H3.mov` — CORRECCIÓN: no barre de lado a lado como H1/H2, rellena por franjas horizontales
- `originales/gumroad/TransitionPack4K_Gumroad/Matte_MOVs/Horizontal/H6.mov` — CORRECCIÓN: no barre de izquierda a derecha, los bloques salen en varios puntos a la vez
- `originales/gumroad/TransitionPack4K_Gumroad/Matte_MOVs/Horizontal/H7.mov` — CORRECCIÓN: entra por los dos lados (cierre tipo telón), no de izquierda a derecha
- `originales/gumroad/TransitionPack4K_Gumroad/Matte_MOVs/Vertical/V3.mov` — CORRECCIÓN: no baja de arriba abajo, rellena por columnas verticales
- `originales/gumroad/TransitionPack4K_Gumroad/Matte_MOVs/Vertical/V6.mov` — CORRECCIÓN: no baja de arriba abajo, bloques en varios puntos
- `originales/gumroad/TransitionPack4K_Gumroad/Matte_MOVs/Vertical/V7.mov` — CORRECCIÓN: entra por arriba y abajo a la vez, no de arriba abajo
- `originales/gumroad/TransitionPack4K_Gumroad/Textured_MOVs/Horizontal/H3.mov` — CORRECCIÓN: rellena por franjas, no barre de lado a lado
- `originales/gumroad/TransitionPack4K_Gumroad/Textured_MOVs/Horizontal/H6.mov` — CORRECCIÓN: bloques en varios puntos, no barrido
- `originales/gumroad/TransitionPack4K_Gumroad/Textured_MOVs/Horizontal/H7.mov` — CORRECCIÓN: cierre tipo telón por los dos lados
- `originales/gumroad/TransitionPack4K_Gumroad/Textured_MOVs/Vertical/V3.mov` — CORRECCIÓN: rellena por columnas, no baja
- `originales/gumroad/TransitionPack4K_Gumroad/Textured_MOVs/Vertical/V6.mov` — CORRECCIÓN: bloques en varios puntos, no baja
- `originales/gumroad/TransitionPack4K_Gumroad/Textured_MOVs/Vertical/V7.mov` — CORRECCIÓN: entra por arriba y abajo a la vez
- `ACIDBITE/01_TRANSICIONES/Textile Transitions/Assets/Toolkit/Texture Animations/Paper Textures/Paper Texture 1.mov` — CORRECCIÓN: el índice dice multiplicar pero es oscuro sobre negro: en multiplicar oscurece todo; usar trama o invertir
- `ACIDBITE/01_TRANSICIONES/Textile Transitions/Assets/Toolkit/Texture Animations/Paper Textures/Paper Texture 2.mov` — CORRECCIÓN: el índice dice multiplicar pero es luz sobre negro: mejor superponer o trama
- `ACIDBITE/01_TRANSICIONES/Textile Transitions/Assets/Toolkit/Texture Animations/Paper Textures/Paper Texture 3.mov` — CORRECCIÓN: el índice dice multiplicar pero es oscuro: usar trama o invertir
- `ACIDBITE/01_TRANSICIONES/Textile Transitions/Assets/Toolkit/Texture Animations/Paper Textures/Paper Texture 4.mov` — CORRECCIÓN: el índice dice multiplicar pero es oscuro: usar trama o invertir
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  1 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  10 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  2 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  3 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  4 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  5 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  6 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  7 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  8 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Flat/Viewfinders 16mm 1.85  9 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/02_PELICULA/Viewfinders Plus/Assets/16mm/Scope/Viewfinders 16mm scope 1 (Multiply).mov` — CORRECCIÓN: el nombre dice Multiply pero son líneas claras sobre negro: usar trama
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Opener/Opener 07.mov` — CORRECCIÓN: el índice dice trama pero es negro sobre blanco: usar multiplicar; dudoso: texto manuscrito ilegible
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Opener/Opener 08.mov` — CORRECCIÓN: el índice dice trama pero es oscuro sobre blanco: usar multiplicar
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Opener/Opener 09.mov` — CORRECCIÓN: el índice dice trama pero es oscuro sobre blanco: usar multiplicar
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Animated Markers/Assets/Symbols/Left Arrow.mov` — CORRECCIÓN: el archivo se llama Left Arrow pero la flecha apunta a la derecha
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Animated Markers/Assets/Symbols/Right Arrow.mov` — CORRECCIÓN: el archivo se llama Right Arrow pero la flecha apunta a la izquierda (nombres de Left/Right intercambiados)
- `TEXTURAS/collage/cintas/carrocero/carrocero_0185_1.png` — CORRECCIÓN: es una tira blanca estrecha (parece cinta correctora o papel), no carrocero beige
- `TEXTURAS/collage/cintas/carrocero/carrocero_0185_2.png` — CORRECCIÓN: tira blanca estrecha, no carrocero beige
- `TEXTURAS/collage/cintas/carrocero/carrocero_0185_3.png` — CORRECCIÓN: tira blanca estrecha, no carrocero beige
- `TEXTURAS/collage/cintas/carrocero/carrocero_0186_1.png` — CORRECCIÓN: tira blanca estrecha, no carrocero beige
- `TEXTURAS/collage/cintas/carrocero/carrocero_0186_2.png` — CORRECCIÓN: es cinta correctora blanca, no carrocero (igual que correctora_0174)
- `TEXTURAS/collage/cintas/carrocero/carrocero_0186_3.png` — CORRECCIÓN: es cinta correctora blanca, no carrocero
- `originales/collage/PEGATINAS/Tiras de cinta de papel sobre gris (1).png` — CORRECCIÓN: el nombre dice cinta de papel pero son tiras blancas tipo correctora (origen de carrocero_0185/0186 mal clasificados)
- `originales/collage/PEGATINAS/Tiras de cinta de papel sobre gris (2).png` — CORRECCIÓN: el nombre dice cinta de papel pero son tiras blancas tipo correctora

## Dudosos (no está claro qué es o hay algo que comprobar): 86

- `TEXTURAS/manchas/goteos/lagrima/goteo_061.png` — goteo 3D con zona translúcida/agujereada arriba · dudoso: huecos internos en la mitad superior (puede ser pintura fina translúcida o fallo de recorte)
- `TEXTURAS/manchas/goteos/lagrima/goteo_062.png` — goteo 3D con parte alta muy rota y translúcida · dudoso: huecos internos arriba (posible fallo de recorte)
- `TEXTURAS/manchas/goteos/lagrima/goteo_064.png` — goteo 3D que se afina con raíz translúcida · dudoso: zona translúcida arriba
- `TEXTURAS/superposiciones/degradados/horizonte_abstracto_tonos_grisaceos_0367.jpg` — degradado horizontal de grises: claro arriba, banda oscura, gris abajo (tipo horizonte o tubo metálico) · dudoso: parece foto desenfocada de metal/horizonte; poco uso como textura
- `TEXTURAS/video/elementos/tinta_en_agua/remolinos_de_tinta_clara_en_agua_0f62.mp4` — remolinos densos de tinta clara (gris) en agua · dudoso: el fondo se ve gris medio; en multiplicar oscurece todo el cuadro
- `ACIDBITE/01_TRANSICIONES/Cine Snip Transitions/Assets/Cine Snip Transition 78 ACIDBITE.mov` — película gris clara con letras pálidas borrosas que desaparecen · dudoso: las letras no se leen
- `ACIDBITE/01_TRANSICIONES/Cyber Transitions/Assets/Clean/Clean_02.mov` — pantallazos oscuros azul-violeta con una palabra borrosa (parece «PICTURE») · dudoso: se intuye texto PICTURE en un fotograma
- `ACIDBITE/01_TRANSICIONES/Cyber Transitions/Assets/Glitchy/Glitchy_29.mov` — glitch con texto técnico ilegible (HUD o esquema) en rojo, verde y violeta · dudoso: hay texto o números pequeños ilegibles
- `ACIDBITE/01_TRANSICIONES/Punch Hole Transitions/Assets/Overlays/FRAME_difference.mov` — foto Polaroid clara con agujero que se perfora; texto pequeño ilegible al pie · dudoso: texto pequeño ilegible en la foto
- `ACIDBITE/01_TRANSICIONES/Wipe and Light Transitions/Assets/Wipes/Wipe 27.mov` — barrido por escalera mecánica con una persona difusa y luego negro · dudoso: se intuye una persona desenfocada
- `ACIDBITE/01_TRANSICIONES/Wipe and Light Transitions/Assets/Wipes/Wipe 31.mov` — barrido por fachadas con letras grandes ilegibles · dudoso: letras de un rótulo de tienda
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_ARRILog-C.cube` — LUT de película frío de Super 8 Package para metraje ARRILog-C; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Blackmagic.cube` — LUT de película frío de Super 8 Package para metraje Blackmagic; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709.cube` — LUT de película frío de Super 8 Package para metraje Rec709; en la prueba es la más suave y natural, sin virar; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_CanonLog.cube` — LUT de película frío de Super 8 Package para metraje Rec709 CanonLog; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_CanonLog2.cube` — LUT de película frío de Super 8 Package para metraje Rec709 CanonLog2; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_CanonLog3.cube` — LUT de película frío de Super 8 Package para metraje Rec709 CanonLog3; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_DLog.cube` — LUT de película frío de Super 8 Package para metraje Rec709 DLog; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_FLog.cube` — LUT de película frío de Super 8 Package para metraje Rec709 FLog; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_FLog2.cube` — LUT de película frío de Super 8 Package para metraje Rec709 FLog2; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_REDLog3G10.cube` — LUT de película frío de Super 8 Package para metraje Rec709 REDLog3G10; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_SLog.cube` — LUT de película frío de Super 8 Package para metraje Rec709 SLog; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_Rec709_SLog2.cube` — LUT de película frío de Super 8 Package para metraje Rec709 SLog2; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_SLog3.cube` — LUT de película frío de Super 8 Package para metraje SLog3; en la prueba satura y contrasta mucho (es para S-Log3); dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT cooler/FilmLUT-cooler_V-Log.cube` — LUT de película frío de Super 8 Package para metraje V-Log; en la prueba: verdes y cian más fríos, rojos algo apagados, sombras azuladas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_ARRILog-C.cube` — LUT de película cálido de Super 8 Package para metraje ARRILog-C; en la prueba vira a naranja, amarillo y magenta; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Blackmagic.cube` — LUT de película cálido de Super 8 Package para metraje Blackmagic; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709.cube` — LUT de película cálido de Super 8 Package para metraje Rec709; en la prueba la más natural y suave de las cálidas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_CanonLog.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 CanonLog; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_CanonLog2.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 CanonLog2; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_CanonLog3.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 CanonLog3; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_DLog.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 DLog; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_FLog.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 FLog; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_FLog2.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 FLog2; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_REDLog3G10.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 REDLog3G10; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_SLog.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 SLog; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_Rec709_SLog2.cube` — LUT de película cálido de Super 8 Package para metraje Rec709 SLog2; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_SLog3.cube` — LUT de película cálido de Super 8 Package para metraje SLog3; en la prueba satura mucho los rojos (es para S-Log3); dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT warmer/FilmLUT-warmer_V-Log.cube` — LUT de película cálido de Super 8 Package para metraje V-Log; en la prueba: tono cálido, naranjas y crema, blancos amarillentos, sombras verdosas; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_ARRILog-C.cube` — LUT de película neutro de Super 8 Package para metraje ARRILog-C; en la prueba neutra: colores naturales con algo de contraste; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Blackmagic.cube` — LUT de película neutro de Super 8 Package para metraje Blackmagic; en la prueba neutra con amarillos dorados y blancos limpios; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709.cube` — LUT de película neutro de Super 8 Package para metraje Rec709; en la prueba la más suave, apaga el espectro; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_CanonLog.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 CanonLog; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_CanonLog2.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 CanonLog2; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_CanonLog3.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 CanonLog3; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_DLog.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 DLog; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_FLog.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 FLog; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_FLog2.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 FLog2; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_REDLog3G10.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 REDLog3G10; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_SLog.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 SLog; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_Rec709_SLog2.cube` — LUT de película neutro de Super 8 Package para metraje Rec709 SLog2; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_SLog3.cube` — LUT de película neutro de Super 8 Package para metraje SLog3; en la prueba satura mucho los rojos (es para S-Log3); dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/FilmLUT/FilmLUT_V-Log.cube` — LUT de película neutro de Super 8 Package para metraje V-Log; en la prueba neutra: colores naturales, algo de contraste y amarillos dorados; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Arri Log-C to REC709 - WideGamut.cube` — LUT técnica de conversión: Arri Log-C a REC709 - WideGamut (normaliza el metraje log antes de etalonar); en la prueba satura todo muy fuerte porque espera metraje log; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Blackmagic Design Film Gen 5 to Blackmagic Design Video Gen 5.cube` — LUT técnica de conversión: Blackmagic Design Film Gen 5 a Blackmagic Design Video Gen 5 (normaliza el metraje log antes de etalonar); en la prueba satura al máximo porque espera metraje log; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Blackmagic Design Film Gen 5 to REC709 - Wide Gamut Gen 4-5.cube` — LUT técnica de conversión: Blackmagic Design Film Gen 5 a REC709 - Wide Gamut Gen 4-5 (normaliza el metraje log antes de etalonar); en la prueba satura mucho porque espera metraje log; dudoso: en la prueba se ve igual que la del mismo nombre en 16mm Package (probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Canon Log to REC709 - Cinema Gamut.cube` — LUT técnica de conversión: Canon Log a REC709 - Cinema Gamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Canon Log2 to REC709 - Cinema Gamut.cube` — LUT técnica de conversión: Canon Log2 a REC709 - Cinema Gamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Canon Log3 to REC709 - Cinema Gamut.cube` — LUT técnica de conversión: Canon Log3 a REC709 - Cinema Gamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/DJI D-Log to REC709 - DJI D-Gamut.cube` — LUT técnica de conversión: DJI D-Log a REC709 - DJI D-Gamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Fuji FLog to REC709 - FGamut.cube` — LUT técnica de conversión: Fuji FLog a REC709 - FGamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Fuji FLog2 to REC709 - FGamut.cube` — LUT técnica de conversión: Fuji FLog2 a REC709 - FGamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Nikon N-Log to REC709.cube` — LUT técnica de conversión: Nikon N-Log a REC709 (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Panasonic V-Log to REC709 - V-Gamut.cube` — LUT técnica de conversión: Panasonic V-Log a REC709 - V-Gamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/RED Log3G10 to REC709 - REDWideGamutRGB.cube` — LUT técnica de conversión: RED Log3G10 a REC709 - REDWideGamutRGB (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/REDgamma4 to REC709 - REDWideGamutRGB.cube` — LUT técnica de conversión: REDgamma4 a REC709 - REDWideGamutRGB (normaliza el metraje log antes de etalonar); en la prueba más apagada y con azul en el papel milimetrado; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/REDlogFilm to REC709 - REDWideGamutRGB.cube` — LUT técnica de conversión: REDlogFilm a REC709 - REDWideGamutRGB (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Sony S-Log to REC709 - Sony S-Gamut.cube` — LUT técnica de conversión: Sony S-Log a REC709 - Sony S-Gamut (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Sony S-Log2 to REC709 - Sony S-Gamut3.Cine.cube` — LUT técnica de conversión: Sony S-Log2 a REC709 - Sony S-Gamut3.Cine (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/02_PELICULA/Super 8 Package/Assets/LUTs/Utility LUTs/Sony S-Log3 to REC709 - Sony S-Gamut3.Cine.cube` — LUT técnica de conversión: Sony S-Log3 a REC709 - Sony S-Gamut3.Cine (normaliza el metraje log antes de etalonar); en la prueba satura y contrasta mucho porque espera metraje log; dudoso: igual que la del mismo nombre en 16mm Package (LUT técnica estándar, probablemente el mismo archivo) · ninguno
- `ACIDBITE/03_TEXTURAS_OVERLAYS/CRT Elements/Assets/Wipes/CRT Wipe 26 ACIDBITE.mov` — negro y luego barrido por una habitación con ventanas (se ve un interior) · dudoso: parece filmar un interior real más que la pantalla
- `ACIDBITE/03_TEXTURAS_OVERLAYS/DynamiXXX/Assets/DynamiXXX 36.mov` — negro con formas pequeñas naranjas sueltas y luego mancha incandescente que crece · dudoso: una de las formas pequeñas del inicio parece una esvástica; revisar antes de usar
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Super Mixed Media Pack/Assets/Frames/Mixed Media Frame 08 ACIDBITE.mov` — papel azul y verde con cruz; ventanas que se dividen; recortes de OJOS de una foto · dudoso: recortes de ojos de una persona real en dos fotogramas
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Super Mixed Media Pack/Assets/Transitions/Alpha Transitions/Mixed Media Alpha Transition 11 ACIDBITE.mov` — collage de estrellas azules, cruces blancas, garabatos y papeles con firma · dudoso: papeles con firmas o garabatos manuscritos
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Super Mixed Media Pack/Assets/Transitions/Overlay Transitions/Mixed Media Overlay Transition 03 ACIDBITE.mov` — papeles rosa moteado y negro que cubren a saltos; texto manuscrito ilegible · dudoso: texto manuscrito ilegible en un fotograma
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Collage/Collage 03.mov` — papel negro cortado en rectángulos (sin ventanas visibles), casi quieto · dudoso: no se ven huecos transparentes claros
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Opener/Opener 03.mov` — clips metálicos, garabatos azules y rayas sobre negro · dudoso: garabatos manuscritos ilegibles
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Opener/Opener 07.mov` — papel blanco con garabatos y texto manuscrito ilegible en negro, celo · CORRECCIÓN: el índice dice trama pero es negro sobre blanco: usar multiplicar; dudoso: texto manuscrito ilegible
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Marker/Red Symbol.png` — símbolo rojo: D con raya en medio (parece un plano) · dudoso: símbolo poco claro (D o puerta)
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Animated Markers/Assets/Letters/r_small.mov` — minúscula «r» con el gancho hacia la izquierda (parece r en espejo o un 7) · dudoso: la r está dibujada como en espejo
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Cinemarkers 2/Assets/Cinemarkers 2 001.mov` — letras amarillas rayadas que cambian cada fotograma (texto en vertical) · dudoso: las letras no forman una palabra clara
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Cinemarkers 2/Assets/Cinemarkers 2 005.mov` — letras «ab» rojas rayadas (probable logo de ACIDBITE) · dudoso: firma de la marca
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Cinemarkers 2/Assets/Cinemarkers 2 063.mov` — letras «ab» blancas en vertical (probable logo de ACIDBITE) · dudoso: firma de la marca
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Cinemarkers/Assets/Overlays/ab.mov` — letras «ab» pintadas en crema (probable logo de ACIDBITE) · dudoso: parece la firma o logo de la marca, no usar como texto propio
- `TEXTURAS/productos/piezas_neonizador/burbujas/burbujas_228_07.png` — media burbuja: solo la mitad inferior visible · dudoso: la parte superior es tan transparente que desaparece; se ve como un cuenco
- `TEXTURAS/productos/piezas_neonizador/burbujas/burbujas_228_08.png` — media burbuja: solo el arco superior visible · dudoso: la mitad inferior apenas existe

## Cuidado al usar (contenido sensible o que puede pasar por real): 22

- `TEXTURAS/imperfecciones/sello_seco/sello_notarial_mexicano_relieve_blanco_0967_relieve.png` — relieve de sello notarial en seco redondo con balanza y laurel · texto concreto legible: «NOTARÍA PÚBLICA · ESTADO DE MÉXICO»
- `TEXTURAS/imperfecciones/sello_seco/sello_notarial_oficial_relieve_blanco_0968_relieve.png` — relieve de sello notarial dentado con balanza y laurel · texto legible: «NOTARÍA PÚBLICA · OFICIAL»
- `TEXTURAS/imperfecciones/sello_seco/sello_notarial_relieve_blanco_0966_relieve.png` — relieve de sello notarial con balanza · texto legible: «NOTARÍA PÚBLICA · REPÚBLICA»
- `TEXTURAS/tileables/vidrios_y_plasticos/brillo_arrugado_0804.jpg` — plástico arrugado con brillos sobre negro · aviso del catálogo: brillos largos, la costura puede notarse en el cruce
- `originales/papelator/imperfecciones/Sello notarial en relieve blanco.png` — sello en seco circular «NOTARÍA PÚBLICA / REPÚBLICA» con balanza · texto legible de notaría: puede parecer documento oficial
- `originales/papelator/imperfecciones/Sello notarial mexicano en relieve blanco.png` — sello en seco «NOTARÍA PÚBLICA / ESTADO DE MÉXICO» con balanza · nombra un estado real: evitar en piezas que puedan pasar por documento oficial
- `originales/papelator/imperfecciones/Sello notarial oficial en relieve blanco.png` — sello en seco dentado «NOTARÍA PÚBLICA / OFICIAL» · texto legible de notaría
- `ACIDBITE/01_TRANSICIONES/Tunnel Transitions/Assets/Tunnel_06.mov` — túnel rojo orgánico (parece interior de un cuerpo) recto · aspecto visceral, como un vaso sanguíneo
- `ACIDBITE/01_TRANSICIONES/Tunnel Transitions/Assets/Tunnel_06_curve.mov` — túnel rojo orgánico con curva · aspecto visceral
- `ACIDBITE/01_TRANSICIONES/Tunnel Transitions/Assets/Tunnel_06_rotate.mov` — túnel rojo orgánico que gira · aspecto visceral
- `ACIDBITE/02_PELICULA/35mm Package/Tutorial/35MM_Tutorial.mp4` — tutorial de 35mm Package presentado a cámara por una persona (micrófono), con rótulos GRAIN y FILM GATES · es documentación; sale el presentador (persona real)
- `ACIDBITE/03_TEXTURAS_OVERLAYS/Dissected Textures/Assets/Alpha/Dissected Alpha Texture 04.mov` — papel azul-gris y RADIOGRAFÍAS de huesos, tornillos y suturas; entra con una mancha rasgada · contiene radiografías médicas (huesos con tornillos): imagen sensible
- `ACIDBITE/03_TEXTURAS_OVERLAYS/DynamiXXX/Assets/DynamiXXX 36.mov` — negro con formas pequeñas naranjas sueltas y luego mancha incandescente que crece · dudoso: una de las formas pequeñas del inicio parece una esvástica; revisar antes de usar
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Super Mixed Media Pack/Assets/Frames/Mixed Media Frame 08 ACIDBITE.mov` — papel azul y verde con cruz; ventanas que se dividen; recortes de OJOS de una foto · dudoso: recortes de ojos de una persona real en dos fotogramas
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 1.png` — salpicadura roja con zonas semitransparentes · puede leerse como sangre
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 2.png` — salpicadura roja estrellada · puede leerse como sangre
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 3.png` — salpicadura roja dispersa con muchas gotas · puede leerse como sangre
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 4.png` — salpicadura roja grande · puede leerse como sangre
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 5.png` — salpicadura roja con rayos · puede leerse como sangre
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 6.png` — salpicadura roja horizontal · puede leerse como sangre
- `ACIDBITE/04_COLLAGE_MIXED_MEDIA/Ultimate Paper Pack/Assets/Toolkit/Ink/Red Splatter 7.png` — salpicadura roja estrellada vertical · puede leerse como sangre
- `ACIDBITE/05_ANIMACIONES_ELEMENTOS/Cinemarkers 2/Assets/Cinemarkers 2 014.mov` — pinceladas rojo sangre y salpicaduras sobre blanco · puede leerse como sangre

## Familias más numerosas

- **or_heredado_neonizador** (711): recorte o JPG re-guardado heredado de NEONIZADOR/BIBLIOTECA (burbujas, espuma, elementos…) que se conserva tal cual para que el plugin salga igual
- **pieza_pavesa** (267): pavesa (trocito de papel o ceniza ardiendo) diminuta recortada de NEONIZADOR
- **or_collage_fuente** (235): imagen fuente 1254 px generada con IA (Gemini) por Iker: un trozo de papel o material sobre fondo liso gris/azul pizarra, de la que se recortaron las piezas de 
- **ab_lut** (220): LUT .cube de ACIDBITE (pago) para dar look de película o normalizar metraje log
- **ab_marcador_flecha** (186): flecha, icono o forma dibujada a rotulador y animada a saltos (2000×2000 con alfa) de ACIDBITE Animated Markers
- **or_gumroad_fotograma_transicion** (168): fotograma PNG 3840×2160 suelto de una transición de tinta de Studio DamDam (pack de pago, no redistribuir), copia en NEONIZADOR/TEXTURAS
- **pieza_salpicadura_oxido** (150): grupo de salpicaduras ocre-óxido con halo difuso y puntos densos, 150-280 px
- **or_papelator_imperfeccion** (144): foto original 2048 px (IA) de una mancha o imperfección sobre papel blanco (aro de café, salpicado, humedad, té, huella dactilar, tinta, óxido de clip), fuente 
- **pieza_gota_agua** (140): gota o chorrito de agua transparente cayendo recortada de NEONIZADOR (alfa = luz)
- **or_papelator_borde_croma** (136): foto original (IA) de borde de papel o cartón rasgado arriba sobre fondo verde croma, 1536×1024, de la que salen bordes/
- **pieza_chispa** (128): chispa suelta diminuta (10-60 px) recortada de NEONIZADOR: trazo incandescente amarillo-naranja-rojo
- **or_textura_9x16** (122): textura original 9:16 (1536×2752, generada con IA) a pantalla completa, no tileable, de la que salen superposiciones/9x16
- **salpicadura_tinta** (106): salpicadura de tinta negra en gotas y regueros
- **ab_marcador_letra** (106): letra, número o signo escrito con rotulador a mano y animado a saltos (2000×2000 con alfa) del abecedario de ACIDBITE Animated Markers
- **ab_cinemarker2** (105): marca rayada o pintada sobre película negra (4K, sobre negro) de ACIDBITE Cinemarkers 2: letras, flechas, círculos, marcos y garabatos que vibran a saltos
- **ab_luces_ungraded** (101): versión SIN etalonar (Ungraded, perfil plano) de los clips de ACIDBITE Light Transitions: mismo contenido que la versión Graded pero con negros levantados (gris
- **cinta_trazo** (88): cinta de trazo reducida para el plugin Trazo: máscara en grises (blanco = trazo, negro = vacío) de un trazo real vertical, 46 px de ancho (13 px los bolígrafos)
- **tile_916** (86): versión tileable (1408×2624) de una superposición 9:16
- **ab_cine_snip** (84): tira de película real (4096×3072 con alfa a los lados = perforaciones transparentes) de ACIDBITE: fotogramas de cola de película verdes con garabatos de rotulad
- **pieza_fibra** (80): fibra textil suelta (pelo de papel de seguridad, como en billetes) recortada, blanca, roja o azul
- **pieza_polvo** (80): mota de polvo/pelusa diminuta recortada (contorno gris oscuro)
- **or_papelator_papel_tileable** (78): foto original (IA) de papel a página completa: milimetrado, cuadriculado, isométrico, de puntos, pautado o liso texturado, fuente de tileables/papel
- **tile_papel** (77): papel tileable (folio, acuarela, kraft, cuadrícula, pentagrama…) con escala real en mm
- **or_papelator_pliegue_fuente** (76): foto original (IA) de hoja de papel gris doblada (A4 vertical 1055×1491) con pliegues en cruz, cuadrícula o bandas, fuente de pliegues/
- **tile_superficie** (71): superficie arquitectónica tileable (ladrillo, piedra, azulejo, adoquín, pared, pintura) en color real
- **or_papelator_superficie** (71): foto original (IA) de superficie arquitectónica a página completa (ladrillo, piedra, azulejo, estuco, terrazo, mortero) de PAPELATOR, fuente de tileables/superf
- **ab_pincelada** (71): pincelada real de tinta o gouache escaneada en alta resolución con alfa, de ACIDBITE Ultimate Paper Pack (negras, azules y de otros colores): flechas, X, círcul
- **or_gumroad_cianotipia** (70): fotograma 1920×1080 de textura animada de cianotipia pintada a mano y escaneada (Studio DamDam, Free Cyanotype Textures, no redistribuir): mancha azul de Prusia
- **ab_optico** (68): reflejos ópticos reales (cristal o prisma delante del objetivo: destellos, bokeh, aberración) en tonos fríos azul-gris, 4K sobre negro, de ACIDBITE Optical Elem
- **goteo_serpenteante** (66): goteo que serpentea en curvas (pintura que baja zigzagueando), con gotas y ensanches

## Dónde está cada cosa

- `revision/fichas/<lote>.json`: fichas por lote (las crea `tools/atlas/revision.py fichas`).
- `revision/FICHAS.json`: todas las fichas juntas, por id.
- `revision/familias.json`: familias (uso, modo, usar si, evitar si, mejor).
- `revision/hojas/<lote>.jpg`: la hoja que se miró para cada lote.
- `indice/indice.json`: cada asset lleva ahora `revision` (la ficha); ningún campo anterior se ha tocado.
