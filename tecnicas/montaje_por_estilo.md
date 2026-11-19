# Montaje automático por estilo

Cinco estilos con sus packs, colocaciones, modos y reglas: `acidbite/datos/estilos.json` → `estilos`; las 29 recetas
exactas de ACIDBITE en `recetas_acidbite`. Resumen:

| Estilo | Qué usar | Reglas |
|---|---|---|
| Cortinillas de luz | Light/Wipe & Light, Film Burns/Leaks, Optical, CRT flashes | pico sobre el corte; SFX al pico; recolorear |
| Collage | Ultimate Paper, Super Mixed Media, Textile, Punch Hole, Animated Markers, Cinemarkers, Burning Paper | máscara + copia visible; 12/8 fps; papel en multiplicar |
| Urbano | Dissected, Cracked Glass, DynamiXXX, Animated Markers, Urban SFX | golpes < 1 s; hits/metal en el corte |
| Tecnológico | CRT, Analog Video, Cyber, VHS, Tunnel, Morpheus, Viewfinders, Dystopia SFX | ruido en superponer; glitch intercalado ≈1 s |
| Cine | 16/35/S8, Burns, Leaks, Cine Snip, Cinemarkers | pila de película, 24 fps, LUT por cámara |

Velocidad (`video.velocidad`) para casar con el ritmo: estático/lento en planos largos; rápido/muy rápido en cortes.
Vertical: todo es 16:9 (o 4:3/2000²): recortar al centro o escalar ×1,78 (`aspecto`).
