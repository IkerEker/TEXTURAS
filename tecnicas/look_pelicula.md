# Look película (16mm, 35mm, Super 8)

De abajo arriba, todo a **24 fps**:
1. Metraje + **LUT** (`clase=lut`, elegir por `lut.camara_entrada`; Rec.709 → `FilmLUT_Rec709`).
2. **Grano** (`pelicula/*`, carpeta `Grain (Overlay)`) en **superponer** todo el plano; más presencia: luz fuerte (35mm: +14 contraste).
3. **Ventanilla/gate**: `(Multiply)` = interior blanco, bordes negros; `(alpha)` = recortada, Normal (escalar el metraje para que quepa).
4. **Perforaciones** en trama.
5. **Texturas 35mm** en luz focal (Pin Light); una en diferencia.
6. **Quemado** en trama sobre el corte, cortando en el fotograma más brillante; su SFX debajo. Si enseña la perforación,
   escalar y desplazar para sacarla de cuadro.

En foto fija (PAPELATOR/Analog FX): `superposiciones/pelicula_polvo_y_rayas` de TEXTURAS y fotogramas de AcidBite.
**Visores** (`pelicula/visores`): los .mov en **trama** (aunque el nombre diga Multiply); los PNG en multiplicar.
