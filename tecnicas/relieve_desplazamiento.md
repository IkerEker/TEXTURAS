# Relieve y desplazamiento

Convención común: **gris 8 bits, 128 = sin efecto** (más = sube/luz, menos = baja/sombra). Campo `desplazamiento`.
- Relieves de TEXTURAS (`*_relieve.png`), pliegues (`pliegues/*`, 128 = plano): superponer/luz suave o como mapa.
- `productos/sellos_relieve` (grumos de A mano, luz desde arriba): sumar a la luz; no rotar.
- `productos/papel_gris`: relieve de papel a escala.
- Vidrios (`tileables/vidrios_y_plasticos`): NEONIZADOR desplaza con el **gradiente** de la foto desenfocada.
- `desplazamiento/ruido` = Morpheus `Noise_01-16` (AcidBite): el `SelfDisplace` de su plantilla de After Effects
  (desplazar el plano por una textura de ruido animada) → modelo para transiciones de Neonizador vídeo.
- Deformación por efecto (ACIDBITE): Wave Warp (VHS, Textile, look analógico), Spherize y Lens Distortion (Punch Hole, Tunnel).
