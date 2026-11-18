#!/usr/bin/env python3
"""Vídeos: análisis completo, copia/transcodificación, versión en loop sin corte y tira de fotogramas.
Uso: python3 video_proc.py inv2.json RAIZ_REPOS DESTINO salida.json"""
import sys, os, json, subprocess, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont

INV, R, DEST, OUT = sys.argv[1:5]
W = 160
try:
    F = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 11)
except Exception:
    F = None

# qué es cada vídeo (revisado a ojo en las tiras de fotogramas)
GEM = {
 '1871041d': ('elementos/espuma', 'Espuma de burbujas blancas, en movimiento suave'),
 '42327423': ('elementos/tinta_en_agua', 'Tinta blanca y negra en agua: remolinos tipo mármol que se agitan en el centro'),
 'ee65a014': ('elementos/tinta_en_agua', 'Tinta en agua: mármol que estalla en el centro y vuelve a asentarse'),
 'f9e16056': ('elementos/tinta_en_agua', 'Tinta en agua: estallido de gotas en el centro; acaba como empieza'),
 '261113_0002': ('elementos/agua_y_espuma', 'Agua negra con burbujas y espuma, oleaje lento (cuadrado)'),
 '261113_0003': ('elementos/humo', 'Humo que nace abajo y sube hasta llenar el encuadre, sobre gris'),
 '261113_0004': ('elementos/humo', 'Columna de humo blanco sobre negro, ondulando'),
 '261113_0005': ('elementos/burbujas', 'Hilera de burbujas que aparece y sube por el centro, sobre negro'),
 '261113_0006': ('elementos/fuego_y_humo', 'Llamas y humo blancos (monocromo) que ocupan todo el cuadro'),
 '26654cfd': ('elementos/humo', 'Dos columnas de humo blanco que suben y se enroscan, sobre negro'),
 '2de3380b': ('elementos/tinta_en_agua', 'Tinta blanca en agua oscura: remolinos y gotas'),
 '2f91d53f': ('elementos/agua_y_espuma', 'Espuma oscura sobre agua, apaisado, casi quieta'),
 '61380f62': ('elementos/tinta_en_agua', 'Remolinos de tinta clara en agua, densos'),
 '907c9571': ('elementos/agua_y_espuma', 'Espuma de mar blanca sobre agua oscura, apaisado'),
}
GUM = {
 'Texture1_BlackPaper': ('texturas_animadas/papel', 'Papel negro con grano, animado a saltos (boil)'),
 'Texture2_WhitePaper': ('texturas_animadas/papel', 'Papel blanco con grano, animado a saltos (boil)'),
 'Texture3_BlackPaper_Grunge': ('texturas_animadas/grunge', 'Pinceladas blancas grunge sobre papel negro, cambian cada fotograma'),
 'Texture4_WhitePaper_Grunge': ('texturas_animadas/grunge', 'Manchas y rayas negras grunge sobre papel blanco, cambian cada fotograma'),
 'Texture5_BlackPaper_Splashes': ('texturas_animadas/salpicaduras', 'Salpicaduras blancas que aparecen sobre papel negro'),
 'Texture6_WhitePaper_Splashes': ('texturas_animadas/salpicaduras', 'Salpicaduras y goterones negros sobre papel blanco'),
 'Texture7_BlackPaper_Stamps': ('texturas_animadas/sellos', 'Estampaciones blancas (huellas de tampón) sobre papel negro'),
 'Texture8_BlackPaper_Stamps': ('texturas_animadas/sellos', 'Estampaciones negras (huellas de tampón) sobre papel blanco'),
 'Texture9_BlackPaper_VerticalLines': ('texturas_animadas/lineas', 'Papel negro con líneas verticales finas, animado'),
 'Texture10_WhitePaper_VerticalLines': ('texturas_animadas/lineas', 'Papel blanco con líneas verticales, animado'),
 'Texture11_BlackPaper_HorizontalLines': ('texturas_animadas/lineas', 'Papel negro con líneas horizontales, animado'),
 'Texture12_WhitePaper_HorizontalLines': ('texturas_animadas/lineas', 'Papel blanco pautado (líneas horizontales), animado'),
 'Texture13_PaintLeaks': ('texturas_animadas/manchas', 'Manchas de agua/pintura que aparecen y se secan sobre papel blanco'),
 'TransitionTexture_1': ('transiciones/pintura', 'Brochazo negro que barre la pantalla de izquierda a derecha y la descubre'),
 'TransitionTexture2': ('transiciones/pintura', 'Brochazo negro diagonal que cubre y descubre la pantalla'),
 'T1': ('elementos/spray', 'Manchas de spray negro que aparecen a saltos sobre papel (stop motion, 8 fotogramas)'),
 'T2': ('elementos/spray', 'Trazos de spray negro (garabatos) que aparecen a saltos sobre papel'),
 'T3': ('elementos/spray', 'Formas de spray negro que cambian a saltos sobre papel'),
 'T4': ('elementos/spray', 'Mancha y trazos de spray que aparecen a saltos sobre papel'),
}
TRANS = {'D': 'diagonal', 'H': 'horizontal', 'V': 'vertical'}
TDESC = {1: 'mancha de tinta con bordes rotos', 2: 'pinceladas de tinta', 3: 'trazos de rotulador inclinados', 4: 'brochazos',
         5: 'garabatos de tinta', 6: 'bloques de tinta rayados', 7: 'tinta seca y textura de esponja'}


def frames(path, w, h):
    hh = int(round(h * W / w / 2)) * 2
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', 'scale=%d:%d' % (W, hh), '-f', 'rawvideo',
                          '-pix_fmt', 'rgb24', '-'], capture_output=True, timeout=900).stdout
    n = len(raw) // (W * hh * 3)
    return np.frombuffer(raw[:n * W * hh * 3], np.uint8).reshape(n, hh, W, 3), hh


def analiza(x, path):
    F_, hh = frames(path, x['w'], x['h'])
    n = len(F_); fps = x['fps']
    L = (F_.astype(np.float32) @ np.array([0.299, 0.587, 0.114], np.float32)) / 255
    dark = (L < 0.25).mean((1, 2)); light = (L > 0.70).mean((1, 2))
    dif = np.abs(np.diff(L, axis=0)).mean((1, 2)) if n > 1 else np.zeros(0)
    uniq = 1 + int((dif > 0.002).sum()) if n > 1 else 1
    med = float(np.median(dif)) if len(dif) else 0
    loopd = float(np.abs(L[0] - L[-1]).mean())
    loop = bool(len(dif) and loopd <= max(1.5 * med, 0.004))
    # fondo dominante (mediana global por píxel) -> polaridad
    bgl = float(np.median(L))
    fondo = 'negro' if bgl < 0.2 else 'blanco' if bgl > 0.75 else 'gris oscuro' if bgl < 0.45 else 'gris claro'
    global L0, L1
    L0, L1 = L[: max(1, n // 10)].mean(), L[-max(1, n // 10):].mean()
    r = dict(frames=n, fotogramas_distintos=uniq, fps=fps,
             fps_efectivo=round(fps * uniq / max(n, 1), 2),
             a_saltos=bool(uniq < 0.8 * n), duracion=round(n / fps, 3) if fps else None,
             fondo=fondo, lum_media=round(float(L.mean()), 3), loop=loop, dif_inicio_fin=round(loopd, 4),
             movimiento=round(float(dif.mean()) * 100, 2) if len(dif) else 0)
    # transición: alguna vez casi todo negro partiendo de claro
    full = np.where(dark > 0.88)[0]
    if light[0] > 0.45 and len(full):
        r['transicion'] = dict(empieza='claro', cubre_total_s=round(full[0] / fps, 3), descubre_desde_s=round(full[-1] / fps, 3),
                               acaba='claro' if light[-1] > 0.45 else 'oscuro', tinta_al_empezar=round(float(dark[0]), 3))
        r['comportamiento'] = 'transición: la tinta cubre toda la pantalla en %.2f s y la descubre desde %.2f s' % (full[0] / fps, full[-1] / fps)
    else:
        # cobertura del efecto respecto al fondo
        cov = ((L > 0.22).mean((1, 2)) if fondo in ('negro', 'gris oscuro') else (L < 0.55).mean((1, 2)))
        r['cobertura_inicio'] = round(float(cov[0]), 3); r['cobertura_fin'] = round(float(cov[-1]), 3)
        r['cobertura_max'] = round(float(cov.max()), 3)
        if cov[0] < 0.01 and cov.max() > 0.03:
            k = int(np.argmax(cov > 0.01))
            r['comportamiento'] = 'empieza vacío y el efecto aparece hacia %.2f s' % (k / fps)
        elif loop:
            r['comportamiento'] = 'continuo y en loop (el último fotograma enlaza con el primero)'
        else:
            r['comportamiento'] = 'continuo: el efecto ya está puesto desde el primer fotograma'
    mv = r['movimiento']
    r['velocidad'] = 'casi quieto' if mv < 1 else 'lento' if mv < 3 else 'medio' if mv < 8 else 'rápido'
    r['modo'] = ('trama (el negro desaparece)' if fondo in ('negro', 'gris oscuro') else 'multiplicar (el blanco desaparece)')
    if 'transicion' in r:
        r['modo'] = 'máscara de luminancia / mate de seguimiento (negro = tapa, blanco = deja ver) o multiplicar'
    # tira
    idx = np.linspace(0, n - 1, 10).round().astype(int)
    strip = Image.new('RGB', (W * 10, hh + 18), (25, 25, 25)); d = ImageDraw.Draw(strip)
    for j, i in enumerate(idx):
        strip.paste(Image.fromarray(F_[i]), (j * W, 16)); d.text((j * W + 2, 2), '%.2fs' % (i / fps), fill=(255, 220, 0), font=F)
    return r, strip


def ff(args):
    p = subprocess.run(['ffmpeg', '-v', 'error', '-y'] + args, capture_output=True, text=True, timeout=900)
    if p.returncode:
        raise RuntimeError(p.stderr[-400:])


def main():
    d = json.load(open(INV))
    vs = [x for x in d if x.get('tipo') == 'video' and x['canonico'] == x['ruta'] and x['rol'] == 'fuente']
    cat = []
    for x in sorted(vs, key=lambda x: x['ruta']):
        src = os.path.join(R, x['ruta']); b = os.path.splitext(os.path.basename(x['ruta']))[0]
        gk = next((k for k in GEM if k in b), None)
        if gk:
            folder, desc = GEM[gk]; name = re.sub(r'[^a-z0-9]+', '_', desc.lower().split(':')[0].split(',')[0])[:40].strip('_') + '_' + gk[-4:]
            lic = 'IA (Gemini/Kling), del usuario'
        elif b in GUM:
            folder, desc = GUM[b]; name = re.sub(r'(?<!^)(?=[A-Z])', '_', b).lower().replace('__', '_')
            lic = 'Gumroad (pack comercial: uso propio, no redistribuir)'
        elif re.match(r'^[DHV](\d|_Texture)$', b):
            dirn = TRANS[b[0]]
            if b.endswith('Texture'):
                folder, desc, name = 'transiciones/tinta_4k/' + dirn, 'Textura de papel que acompaña a las transiciones %s (capa superior)' % dirn, '%s_textura' % dirn
            else:
                k = int(b[1]); folder = 'transiciones/tinta_4k/' + dirn
                desc = 'Transición %s de %s (4K): cubre la pantalla y la descubre' % (dirn, TDESC.get(k, 'tinta')); name = '%s_%d' % (dirn, k)
            lic = 'Gumroad (pack comercial: uso propio, no redistribuir)'
        else:
            folder, desc, name, lic = 'otros', b, b.lower(), '?'
        info, strip = analiza(x, src)
        outdir = os.path.join(DEST, 'video', folder); os.makedirs(outdir, exist_ok=True)
        ext = '.mp4'
        dst = os.path.join(outdir, name + ext)
        if x.get('codec') == 'prores':
            ff(['-i', src, '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', dst])
            conv = 'ProRes 422 10 bits -> H.264 CRF 18 (alta calidad; el original ProRes sigue en NEONIZADOR)'
        else:
            ff(['-i', src, '-an', '-c:v', 'copy', '-movflags', '+faststart', dst])
            conv = 'copia sin recomprimir (sin audio)'
        rel = os.path.relpath(dst, DEST)
        strip_rel = os.path.join('video', '_tiras', name + '.jpg')
        os.makedirs(os.path.join(DEST, 'video', '_tiras'), exist_ok=True)
        strip.save(os.path.join(DEST, strip_rel), quality=82)
        e = dict(archivo=rel, cat='video', sub=folder, desc=desc, w=x['w'], h=x['h'], codec_origen=x.get('codec'),
                 pix_fmt_origen=x.get('pix_fmt'), alfa=False, conversion=conv, procedencia=lic, tira=strip_rel,
                 bytes=os.path.getsize(dst), origen=dict(ruta=x['ruta']), **info)
        # versión en loop sin corte para lo continuo que no enlaza
        if 'transicion' not in info and not info['loop'] and info['duracion'] and info['duracion'] >= 4 and \
                folder.startswith('elementos') and 'aparece' not in info['comportamiento'] and 'spray' not in folder \
                and abs(float(L0) - float(L1)) < 0.05 and abs(info.get('cobertura_inicio', 0) - info.get('cobertura_fin', 0)) < 0.12:
            D = min(1.5, info['duracion'] / 5); Lr = info['duracion']
            lp = os.path.join(outdir, name + '_loop.mp4')
            ff(['-i', dst, '-filter_complex',
                '[0:v]split[a][b];[a]trim=start=%.3f,setpts=PTS-STARTPTS[m];[b]trim=0:%.3f,setpts=PTS-STARTPTS[h];'
                '[m][h]xfade=transition=fade:duration=%.3f:offset=%.3f,format=yuv420p[v]' % (D, D, D, Lr - 2 * D),
                '-map', '[v]', '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '14', '-movflags', '+faststart', lp])
            e['version_loop'] = dict(archivo=os.path.relpath(lp, DEST), duracion=round(Lr - D, 3), fundido_s=round(D, 2),
                                     como='el último %.1f s se funde con el arranque: se puede repetir sin salto' % D)
        cat.append(e)
        print('%-45s %-55s %s' % (rel[-45:], info['comportamiento'][:55], info['fps_efectivo']), flush=True)
    json.dump(cat, open(OUT, 'w'), ensure_ascii=False, indent=1)


main()
