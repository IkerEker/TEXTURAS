# Cruce AcidBite × TEXTURAS

**1. ¿Hay algo repetido?** No. Hash perceptivo (pHash 64 bits, el mismo de `tools/inventario.py`) de los 8 fotogramas de
cada clip/imagen de AcidBite (1.626) contra los 4.237 `phash` de `tools/estado/inv2.json` y los fotogramas de los
57 vídeos de TEXTURAS. Distancia mínima: 2 (1 caso), 4 (4), 6 (9). Los 14 más cercanos, **revisados a ojo uno a uno**,
son falsos parecidos: superficies casi lisas (papel blanco con una marca, fondo negro con un brillo) que dan hashes
casi iguales. Ningún asset de AcidBite está en TEXTURAS ni al revés. Datos: `cruce_phash_acidbite.json`
(script `tools/atlas/cruce_phash.py`).

**2. Huecos de las fichas que cubre AcidBite:** tabla en `DECISIONES.md` §13. Lo más útil y nuevo:
- **Cinta adhesiva entera** (34 PNG RGBA: celo, americana, de pintor, de colores) → PAPELATOR.
- **Máscara de fósforo / scanlines / nieve** (`Shadow Mask.png`, `Scanlines.png`, CRT `Dirt`, `Noise_01-16`) → NEONIZADOR (crt, fosforo, vhs).
- **Rayas de tracking VHS y glitch en vídeo** (Analog Video, VHS, Cyber) → NEONIZADOR vídeo.
- **Fuego 4K con alfa** (Burning Paper) → NEONIZADOR vídeo; fotogramas para **bordes quemados** → PAPELATOR (por extraer).
- **Hoja plegada/arrugada 4K** (Ultimate Paper Fold/Crumble) → PAPELATOR (pliegues), NEONIZADOR (acabado pliegue).
- **Trazos de rotulador y tinta con alfa** (Ultimate Paper Marker/Ink, 71) → anotaciones; no son cintas largas.
- **Ruido para desplazamiento** (Morpheus `Noise_01-16`) → transiciones por desplazamiento.

**3. Técnicas de sus tutoriales que sirven a cada plugin** → `tecnicas/` (cada receta dice para quién).

**Sigue faltando** (no lo trae ninguno): moho variado, tiza/pastel, grafito por durezas, spray real sobre pared, sello
de goma, rodillo/brayer, fibras de celulosa, tóner real, tubos de neón, imagen térmica, papeles nuevos (calco, carbón,
térmico, couché, seda, sobres), corcho, pizarra, plástico mate, polvo de escáner, pliegues 7–8 y hoja enrollada.
