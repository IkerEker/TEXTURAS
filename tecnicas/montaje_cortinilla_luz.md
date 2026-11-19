# Cortinilla de luz sobre el corte

**Assets:** `clase=video` y `sub` en `transiciones/luz`, `transiciones/barrido_luz`, `pelicula/quemados`,
`pelicula/fugas_de_luz`, `elementos/refracciones`, `analogico/crt` (Flashes, Flares, Glitches).

1. Pista encima de los dos planos, **modo trama (Screen)**. Wipe & Light no: va *intercalado* (ver abajo).
2. Colocar el clip para que `transicion.corte_s` caiga **justo en el corte**. Es el fotograma más brillante (si el
   blanco dura varios fotogramas, su centro). Light Transitions duran 4–22 fotogramas: es su diseño.
3. Recolorear al color que toque (neón): Color Balance HLS → Hue, o Hue vs Hue (lo hace ACIDBITE en sus tutoriales).
4. Sonido: si `audio.incrustado`, ya viene; si no, `audio.sfx`. El pico del sonido sobre el corte.
5. Retiming: 50–200 % con fusión de fotogramas; el SFX no se estira, se realinea al pico.

**Intercalado (Wipe & Light, Cyber):** el clip entero entre los dos planos, en la misma pista, con fundidos de opacidad
de 2–4 fotogramas en las uniones.

**Pyro** también admite **diferencia** (tutorial de Light Transitions).
