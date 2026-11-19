# Sincronía de audio

- Muchos clips de AcidBite traen el SFX **dentro** (`audio.incrustado`): moverlo con el vídeo.
- Si no: `audio.sfx` (emparejado; mira `audio.confianza`), `audio.sfx_acidbite` (el de sus plantillas) o
  `audio.sfx_familia` (cualquiera de la familia del pack).
- Regla: **el pico del sonido** (`audio.envolvente.pico_s` del .wav) **sobre el corte/pico de la imagen**
  (`transicion.corte_s`). Si el sonido es más largo, se recorta la cola, no el ataque.
- Packs de sonido (`clase=sonido`): whoosh/barrido para cortinillas, golpe (hits) para cortes secos, subida (riser)
  antes de un cambio, ambiente/textura de fondo en bucle, glitch con glitches.
- Ojo: `Collage.02/03.wav` de Ultimate Paper van cruzados (el índice ya los da bien).
