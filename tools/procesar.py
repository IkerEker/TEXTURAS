#!/usr/bin/env python3
"""Procesa las imágenes clasificadas y escribe la biblioteca TEXTURAS.
Uso: python3 procesar.py clasif.json RAIZ_REPOS DESTINO DIR_RESULTADOS [filtro_categoria] [max_items]
Se puede reanudar: cada fuente deja DIR_RESULTADOS/<n>.json con sus entradas de catálogo."""
import sys, os, re, json, hashlib, traceback, unicodedata
import numpy as np
from PIL import Image
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tx

CLASIF, R, DEST, RES = sys.argv[1:5]
FILT = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != '-' else None
MAXN = int(sys.argv[6]) if len(sys.argv) > 6 else None

SUBN = {
 'aguada': 'aguada', 'boligrafo': 'bolígrafo', 'brocha': 'brocha', 'carbon': 'carboncillo', 'cera': 'cera', 'gouache': 'gouache',
 'lapiz': 'grafito', 'oleo': 'óleo', 'pincel': 'pincel', 'pincel_fino': 'pincel fino', 'pincel_seco': 'pincel seco',
 'rotulador': 'rotulador', 'rotulador_gastado': 'rotulador gastado', 'pincel_grandes': 'mancha grande de pincel',
 'goteos_pintura_blanca': 'goteo de pintura blanca', 'tinta': 'mancha de tinta', 'fuego': 'fuego', 'chispas': 'chispas',
 'humo': 'humo', 'fugas_de_luz': 'fuga de luz', 'burbujas_y_espuma': 'burbujas y espuma', 'moho': 'colonia de moho',
}
T916 = {'pintura_color': ('pintura', 'color'), 'pintura_gris': ('pintura', 'gris'), 'aguada': ('pintura', 'aguada'),
        'grafito': ('grafito_y_carbon', 'grafito'), 'carbon': ('grafito_y_carbon', 'carbon'), 'grunge': ('grunge', 'grunge'),
        'grunge_cuadricula': ('grunge', 'cuadricula_sucia'), 'ruido': ('grunge', 'ruido'), 'goteos': ('goteos', 'goteos'),
        'veta': ('veta_pintada', 'veta'), 'fotocopia': ('grunge', 'fotocopia')}
MODO = {'tileables/papel': 'multiplicar (sobre el arte) o normal (como fondo)', 'tileables/superficies': 'normal (fondo) · multiplicar para dar textura',
        'tileables/madera_y_carton': 'normal (fondo)', 'tileables/vidrios_y_plasticos': 'trama (va delante del arte)',
        'tileables/grunge': 'multiplicar', 'tileables/liquidos': 'trama o superponer', 'tileables/pintura': 'normal o multiplicar',
        'tileables/grafito_y_carbon': 'multiplicar', 'tileables/goteos': 'multiplicar', 'tileables/veta_pintada': 'multiplicar o normal',
        'tileables/naturaleza': 'normal o superponer'}


def slug(s, n=48):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+', '_', s.lower()).strip('_')
    s = re.sub(r'_(sobre|en|de|del|la|el|los|las|con|y|un|una)_', '_', '_' + s + '_').strip('_')
    s = re.sub(r'_(sobre|en|de|del|la|el|los|las|con|y|un|una)_', '_', '_' + s + '_').strip('_')
    return s[:n].strip('_')


def u8(a):
    return np.clip(np.round(a * 255), 0, 255).astype(np.uint8)


def save_png(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(u8(arr)).save(path, compress_level=7)


def save_jpg(arr, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.fromarray(u8(arr)).save(path, quality=95, subsampling=0, optimize=True)


def base_entry(c, x):
    e = dict(origen=dict(ruta=c['src'], copias=c.get('copias', [])), metodo=c['metodo'])
    for k in ('usado_en', 'id', 'nombre', 'grupo', 'colorable', 'aparejo', 'material', 'tipo_papel', 'modo_papelator',
              'donde', 'desplazamiento_mm', 'relieve_mm', 'variante'):
        if c.get(k) is not None:
            e[k] = c[k]
    return e


def stats(rgba):
    a = rgba[..., 3] if rgba.shape[-1] == 4 else None
    rgb = rgba[..., :3] if rgba.ndim == 3 else np.dstack([rgba] * 3)
    if a is not None and (a > 0.5).any():
        m = rgb[a > 0.5].mean(0)
    else:
        m = rgb.reshape(-1, 3).mean(0)
    return [int(v * 255) for v in m]


LIMPIA = re.compile(r'\s*\b(sobre|en)\s+(un\s+)?(fondo\s+)?(verde(\s+(croma|intenso|crom[aá]tico|chroma))?|negro(\s+(brillante|reluciente|puro))?|blanco|la\s+oscuridad|oscuridad|fondo\s+oscuro|papel\s+blanco|el\s+vac[ií]o\s+negro)\b[^a-zA-Z]*$', re.I)


def limpia(d):
    if not d:
        return d
    d2 = LIMPIA.sub('', d).strip(' -_')
    return d2 or d


def name_for(c, i=None):
    d = limpia(c.get('desc_origen'))
    return slug(d) if d else slug(c.get('nombre') or '')


def process(args):
    n, c = args
    out = []
    src = os.path.join(R, c['src'])
    rgb = tx.load(src)
    H, W = rgb.shape[:2]
    cat, sub, met = c.get('cat'), c.get('sub'), c['metodo']
    folder = os.path.join(cat, sub)
    nm = name_for(c)
    tag = '%04d' % n

    def add(rel, arr, kind, **kw):
        path = os.path.join(DEST, rel)
        (save_png if kind == 'png' else save_jpg)(arr, path)
        e = base_entry(c, None)
        e.update(archivo=rel, cat=cat, sub=sub, w=int(arr.shape[1]), h=int(arr.shape[0]),
                 alfa=bool(arr.ndim == 3 and arr.shape[-1] == 4), bytes=os.path.getsize(path), color_medio=stats(arr) if arr.ndim == 3 else None)
        e.update(kw)
        out.append(e)
        return e

    if met in ('papel_piezas', 'papel_entera'):
        rgba, info = tx.from_paper(rgb, solid_pct=95 if cat == 'imperfecciones' else 65)
        if met == 'papel_piezas' and cat == 'trazos':
            pieces = tx.split_pieces(rgba)
        elif met == 'papel_piezas':
            pieces = tx.split_pieces(rgba, join_frac=0.05, min_frac=0.004)
        else:
            p, box = tx.crop_alpha(rgba)
            pieces = [(p, box)]
        pieces = [p for p in pieces if p[0].shape[0] > 8 and p[0].shape[1] > 8]
        for k, (p, box) in enumerate(pieces):
            col = tx.color_name(np.array(stats(p)) / 255)
            base = nm or slug(('trazo ' if cat == 'trazos' else '') + SUBN.get(sub, sub.replace('_', ' ')) + ' ' + col)
            fn = '%s_%s%s.png' % (base, tag, ('_%02d' % (k + 1)) if len(pieces) > 1 else '')
            desc = limpia(c.get('desc_origen')) or SUBN.get(sub, sub.replace('_', ' '))
            if cat == 'trazos':
                desc = 'Trazo de %s %s' % (SUBN.get(sub, sub), col) + (' (%d de %d de «%s»)' % (k + 1, len(pieces), c['desc_origen'])
                                                                     if c.get('desc_origen') and len(pieces) > 1 else '')
            add(os.path.join(folder, fn), p, 'png', desc=desc, color=col, modo='normal', recorte=list(box), papel=info,
                tamano_real_mm=c.get('mm'), pieza=k + 1, piezas=len(pieces))
    elif met == 'relieve':
        g, gain = tx.relief_gray(rgb)
        m = np.abs(g - 0.5) > 0.03
        ys, xs = np.where(m)
        if len(ys):
            pad = int(min(H, W) * 0.04)
            y0, y1, x0, x1 = max(0, ys.min() - pad), min(H, ys.max() + pad), max(0, xs.min() - pad), min(W, xs.max() + pad)
            g = g[y0:y1, x0:x1]
        add(os.path.join(folder, '%s_%s_relieve.png' % (nm or slug(sub), tag)), g, 'png', desc=(c.get('nombre') or c.get('desc_origen') or sub) + ' (relieve)',
            modo='superponer o luz suave (gris 50 % = neutro)', ganancia=gain, tamano_real_mm=c.get('mm'))
    elif met == 'pliegue':
        g = tx.fold_shading(rgb)
        add(os.path.join(folder, '%s_%s.png' % (nm or 'pliegues_' + slug(sub), tag)), g, 'png', desc=c.get('desc_origen') or 'Pliegues (%s)' % sub.replace('_', ' '),
            modo='superponer o luz suave (gris 50 % = papel plano)', hoja_completa=True)
    elif met == 'croma':
        if tx.is_chroma(rgb):
            rgba, info = tx.from_chroma(rgb); how = 'croma verde'
        elif float((rgb.max(-1) < 0.06).mean()) > 0.15:
            rgba, info = tx.from_black_cover(rgb); how = 'fondo negro'
        else:
            rgba, info = tx.from_paper(rgb); how = 'fondo claro'
        p, box = tx.crop_alpha(rgba, pad_frac=0.005)
        col = tx.color_name(np.array(stats(p)) / 255)
        if sub == 'otros':
            dl = (c.get('desc_origen') or '').lower()
            mat = ('carton' if 'cart' in dl else 'kraft' if 'kraft' in dl else 'viejo' if ('antiguo' in dl or 'envejecido' in dl or 'pergamino' in dl)
                   else 'artesanal' if 'artesanal' in dl else None)
            if mat is None:
                mat = ('carton' if col.startswith('marrón') or col.startswith('naranja') else 'gris' if col in ('gris', 'gris oscuro')
                       else 'bisel' if col.startswith(('azul', 'rojo', 'verde', 'violeta', 'rosa', 'turquesa'))
                       else 'viejo' if col.startswith('amarillo') else 'blanco')
            folder2 = os.path.join(cat, mat)
        else:
            folder2 = folder
        add(os.path.join(folder2, '%s_%s.png' % (nm if c.get('desc_origen') else 'borde_' + slug(col), tag)), p, 'png',
            desc=limpia(c.get('desc_origen')) or 'Borde de papel %s' % col, color=col, modo='normal', recorte=list(box), fondo_original=how)
    elif met in ('negro_luz', 'negro_objeto'):
        full = cat == 'superposiciones'
        rgba, info = tx.from_black(rgb) if met == 'negro_luz' else tx.from_black_cover(rgb, 40)
        if full:
            p, box = rgba, (0, H, 0, W)
        else:
            p, box = tx.crop_alpha(rgba, thr=0.02, pad_frac=0.02)
        e = add(os.path.join(folder, '%s_%s.png' % (nm or slug(SUBN.get(sub, sub)), tag)), p, 'png', desc=limpia(c.get('desc_origen')) or SUBN.get(sub, sub),
                modo='normal (transparencia real)' if met == 'negro_luz' else 'normal', recorte=list(box), **info)
        if met == 'negro_luz':
            y0, y1, x0, x1 = box
            t = add(os.path.join(folder, '%s_%s_trama.jpg' % (nm or slug(SUBN.get(sub, sub)), tag)), rgb[y0:y1, x0:x1], 'jpg',
                    desc=(c.get('desc_origen') or sub) + ' (sobre negro, para modo Trama)', modo='trama / sobreexponer color', pareja=e['archivo'])
            e['pareja'] = t['archivo']
    elif met in ('tileable', 'tileable_verificar', 'tileable_patron', 'superposicion_y_tile', 'superposicion'):
        mmpp = None
        if c.get('mm') and met != 'superposicion_y_tile':
            mmpp = float(c['mm']) / W
        if met in ('superposicion_y_tile', 'superposicion'):
            sname = sub
            add(os.path.join(cat, sub.replace('9x16_', '9x16/'), '%s_%s.jpg' % (nm if c.get('desc_origen') else slug(sub.replace('9x16_', '')), tag)), rgb, 'jpg',
                desc=c.get('desc_origen') or 'Textura 9:16 · %s' % sub.replace('9x16_', '').replace('_', ' '),
                modo='multiplicar / superponer (pantalla completa)', tileable=False, proporcion='%d:%d' % (W, H))
            if met == 'superposicion':
                return out
            hm, hs = tx.homogeneity(rgb)
            if hm > 0.45:
                out[-1]['tile'] = 'no (composición poco homogénea: %.2f)' % hm
                return out
            tsub, var = T916.get(sub.replace('9x16_', ''), ('otras', sub))
            folder = os.path.join('tileables', tsub)
            c = dict(c, variante=var)
        before = tx.seam_score(rgb)
        how = None
        if met == 'tileable_verificar' and max(before) < 1.25:
            tile, how = rgb, 'ya era tileable'
        elif met == 'tileable_patron' or c.get('aparejo'):
            flat = tx.flatten_light(rgb, max(H, W) / 5)
            tile, info = tx.make_tileable_periodic(flat)
            how = 'número entero de periodos + costura óptima (%s)' % info
        else:
            flat = tx.flatten_light(rgb, max(H, W) / 5)
            if c.get('girar'):
                flat = np.rot90(flat).copy()
            best = None
            for O in (None, min(H, W) // 6, min(H, W) // 4):   # si la costura se nota, más franja de solape
                t_ = tx.make_tileable(flat, O=O)
                sc = max(tx.seam_score(t_))
                if best is None or sc < best[0]:
                    best = (sc, t_, O)
                if sc < 1.2:
                    break
            tile = best[1]
            how = 'luz aplanada + costura óptima (altas) + fundido (bajas)' + ('' if best[2] is None else ', solape %d px' % best[2])
        after = tx.seam_score(tile)
        key = folder.replace(os.sep, '/')
        tcol = tx.color_name(tile.reshape(-1, 3).mean(0))
        d = c.get('nombre') or c.get('desc_origen') or '%s %s' % ((c.get('variante') or sub).replace('_', ' '), tcol)
        add(os.path.join(folder, '%s_%s.jpg' % (nm if (c.get('desc_origen') or c.get('nombre')) else slug('%s_%s' % (c.get('variante') or sub, tcol)), tag)),
            tile, 'jpg', desc=d, color=tcol, modo=MODO.get(key, 'normal'), tileable=True, costura_antes=list(before), costura=list(after),
            proceso=how, mm_por_px=round(mmpp, 5) if mmpp else None,
            tile_mm=[round(tile.shape[1] * mmpp, 1), round(tile.shape[0] * mmpp, 1)] if mmpp else None,
            periodo_mm=c.get('periodo_mm'), onda_mm=c.get('onda_mm'))
    elif met == 'omitir':
        return [dict(omitido=c['src'], motivo=c.get('motivo'))]
    else:
        return [dict(error='método desconocido', src=c['src'])]
    return out


def job(a):
    n, c = a
    p = os.path.join(RES, '%04d.json' % n)
    if os.path.exists(p):
        return n, 'hecho'
    try:
        r = process(a)
        json.dump(r, open(p, 'w'), ensure_ascii=False, indent=0)
        return n, '%d archivos' % len([e for e in r if 'archivo' in e])
    except Exception as e:
        return n, 'ERROR ' + repr(e)[:300] + ' ' + traceback.format_exc()[-400:]


PATRON = re.compile(r'cuadricul|milimetr|isom[eé]tr|punteado|pautado|rayado|triangular|azulejo', re.I)


OVERRIDE = {
 'papelator/NUEVAS/TEXTURA_IMPERFECCIONES/Gemini_Generated_Image_6lto7b6lto7b6lto.jpg': dict(metodo='relieve'),
 'papelator/NUEVAS/TEXTURA_IMPERFECCIONES/Primer plano de dos perforaciones en papel blanco.png': dict(metodo='relieve'),
 'papelator/imperfecciones/Gemini_Generated_Image_bcw9d7bcw9d7bcw9.jpg': dict(sub='huella_grasa', metodo='relieve', nombre='Huellas dactilares tenues'),
 'papelator/imperfecciones/Gemini_Generated_Image_mezhg4mezhg4mezh.jpg': dict(sub='huella_grasa', metodo='relieve', nombre='Huellas dactilares tenues'),
 'papelator/imperfecciones/Textura de papel marfil fibroso.png': dict(cat='tileables', sub='papel', metodo='tileable'),
 'papelator/NUEVAS/TEXTURA_IMPERFECCIONES/Textura de papel con sutil pliegue curvo.png': dict(sub='arruguita', metodo='relieve'),
}


def fix_class(c):
    c.update(OVERRIDE.get(c['src'], {}))
    if c.get('cat') == 'tileables' and c['metodo'] in ('tileable', 'tileable_verificar') and PATRON.search(c.get('desc_origen') or ''):
        c['metodo'] = 'tileable_patron'
    if c.get('cat') == 'imperfecciones' and c['metodo'] == 'papel_piezas':
        c['metodo'] = 'papel_entera'
    if c.get('sub') == 'sin_clasificar' and c.get('cat') == 'pliegues':
        l = (c.get('desc_origen') or '').lower()
        c['sub'] = '4_pliegues' if 'cuadr' in l else '1_pliegues' if ('horizontal' in l or 'central' in l) else '2_pliegues'
    return c


if __name__ == '__main__':
    os.makedirs(RES, exist_ok=True)
    cl = [fix_class(c) for c in json.load(open(CLASIF))]
    todo = [(n, c) for n, c in enumerate(cl) if (FILT is None or (c.get('cat') or '-') == FILT or c['metodo'] == FILT)]
    todo = [t for t in todo if not os.path.exists(os.path.join(RES, '%04d.json' % t[0]))]
    if MAXN:
        todo = todo[:MAXN]
    print(len(todo), 'por hacer', flush=True)
    with ProcessPoolExecutor(2) as ex:
        for n, msg in ex.map(job, todo, chunksize=1):
            if 'ERROR' in msg or n % 20 == 0:
                print(n, cl[n]['src'][-60:], msg, flush=True)
    print('fin')
