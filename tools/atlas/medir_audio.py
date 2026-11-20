"""Mide sonidos (cualquier formato que lea ffmpeg) y escribe una ficha de audio objetiva por archivo.
  python3 tools/atlas/medir_audio.py <archivo>...            → JSON por línea
Mide: formato, duración, nivel (RMS y pico), silencios al principio y al final, ataque y caída, nº de golpes,
dónde está el golpe principal, reparto grave/medio/agudo, brillo (centroide), si es tonal o ruido (y su nota
aproximada), si sube o baja de tono/brillo (riser/downer), estéreo y si podría hacer bucle. Con eso da una
frase descriptiva («suena_como») que SOLO dice lo que se deduce de las medidas."""
import sys, json, subprocess, numpy as np

def info(p):
    j = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-select_streams', 'a:0', '-of', 'json', p],
                                  capture_output=True, text=True).stdout or '{}')
    s = (j.get('streams') or [{}])[0]
    return dict(sr=int(s.get('sample_rate', 0) or 0), canales=int(s.get('channels', 0) or 0),
                codec=s.get('codec_name'), bits=s.get('bits_per_raw_sample') or s.get('bits_per_sample'))

def leer(p, sr=44100):
    r = subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-i', p, '-f', 'f32le', '-ac', '2', '-ar', str(sr), '-'], capture_output=True)
    x = np.frombuffer(r.stdout, np.float32).reshape(-1, 2)
    return x, sr

def db(v): return float(20 * np.log10(max(v, 1e-9)))

NOTAS = ['do', 'do#', 're', 're#', 'mi', 'fa', 'fa#', 'sol', 'sol#', 'la', 'la#', 'si']
def nota(f):
    if not f or f < 20: return None
    n = int(round(12 * np.log2(f / 440.0) + 57)); return f'{NOTAS[n % 12]}{n // 12}'

def medir(p):
    m = dict(info(p)); x, sr = leer(p)
    if len(x) == 0: return dict(m, error='no se pudo leer')
    mono = x.mean(1); n = len(mono); m['duracion_s'] = round(n / sr, 3)
    m['pico_dbfs'] = round(db(np.abs(x).max()), 1); m['rms_dbfs'] = round(db(np.sqrt((mono ** 2).mean())), 1)
    hop = int(sr * 0.01); win = hop * 4
    fr = np.lib.stride_tricks.sliding_window_view(np.pad(mono, (0, win)), win)[::hop][: max(1, n // hop)]
    env = np.sqrt((fr ** 2).mean(1)); envdb = 20 * np.log10(np.maximum(env, 1e-9)); t = np.arange(len(env)) * hop / sr
    pk = int(env.argmax()); m['golpe_principal_s'] = round(float(t[pk]), 2)
    act = envdb > (envdb.max() - 40)
    m['silencio_inicio_s'] = round(float(t[np.argmax(act)]), 2) if act.any() else None
    m['silencio_final_s'] = round(float(m['duracion_s'] - t[len(act) - 1 - np.argmax(act[::-1])]), 2) if act.any() else None
    lo, hi = env[pk] * 0.1, env[pk] * 0.9
    a0 = np.where(env[:pk + 1] < lo)[0]; a1 = np.where(env[:pk + 1] >= hi)[0]
    m['ataque_s'] = round(float(t[a1[0]] - (t[a0[-1]] if len(a0) else 0)), 3) if len(a1) else None
    tail = np.where(envdb[pk:] < envdb[pk] - 20)[0]
    m['caida_s'] = round(float(tail[0] * hop / sr), 2) if len(tail) else None
    m['rango_dinamico_db'] = round(float(np.percentile(envdb[act], 95) - np.percentile(envdb[act], 10)), 1) if act.sum() > 3 else 0.0
    # espectro por tramos
    W = np.hanning(2048); F = np.fft.rfftfreq(2048, 1 / sr)
    seg = [mono[i:i + 2048] for i in range(0, max(1, n - 2048), max(512, (n - 2048) // 200 or 512))]
    seg = [s for s in seg if len(s) == 2048 and np.abs(s).max() > 1e-4]
    if seg:
        S = np.abs(np.fft.rfft(np.array(seg) * W, axis=1)) ** 2
        tot = S.sum(1, keepdims=True) + 1e-20; P = S.sum(0)
        b = lambda a, z: float(P[(F >= a) & (F < z)].sum() / P.sum())
        m['graves_pct'] = round(100 * b(20, 250)); m['medios_pct'] = round(100 * b(250, 4000)); m['agudos_pct'] = round(100 * b(4000, 22050))
        cen = (S * F).sum(1) / tot[:, 0]; m['brillo_hz'] = int(np.median(cen))
        third = max(1, len(cen) // 3); d = np.median(cen[-third:]) - np.median(cen[:third])
        m['brillo_tendencia'] = 'sube' if d > 0.35 * np.median(cen) else 'baja' if d < -0.35 * np.median(cen) else 'estable'
        flat = np.exp(np.log(S + 1e-20).mean(1)) / (S.mean(1) + 1e-20); m['planitud'] = round(float(np.median(flat)), 3)
        # tono: FFT larga por tramos; hace falta el MISMO pico estrecho en la mayoría de tramos (no basta un retumbo grave)
        N2 = 8192; W2 = np.hanning(N2); F2 = np.fft.rfftfreq(N2, 1 / sr)
        seg2 = [mono[i:i + N2] for i in range(0, max(1, n - N2), max(N2 // 2, (n - N2) // 40 or N2))]
        seg2 = [s2 for s2 in seg2 if len(s2) == N2 and np.abs(s2).max() > 1e-3]
        picos = []
        for s2 in seg2:
            S2 = np.abs(np.fft.rfft(s2 * W2)) ** 2; S2[F2 < 80] = 0; k = int(S2.argmax())
            if S2[max(0, k - 2):k + 3].sum() / (S2.sum() + 1e-20) > 0.25: picos.append(F2[k])
        if len(seg2) >= 2 and len(picos) >= 0.6 * len(seg2):
            f0 = float(np.median(picos)); est = np.mean([abs(p_ - f0) < 0.03 * f0 for p_ in picos])
            m['tonal'] = bool(est > 0.7)
            if m['tonal']: m['tono_hz'] = round(f0, 1); m['nota'] = nota(f0)
        else: m['tonal'] = False
    # golpes (flujo de energía)
    on = np.diff(envdb); thr = max(6.0, np.percentile(on, 99) * 0.6)
    peaks = [i for i in range(1, len(on) - 1) if on[i] > thr and on[i] >= on[i - 1] and on[i] >= on[i + 1] and envdb[i + 1] > envdb.max() - 30]
    g = []; 
    for i in peaks:
        if not g or i - g[-1] > 8: g.append(i)
    m['golpes'] = len(g)
    # estéreo
    L, R = x[:, 0], x[:, 1]
    if np.abs(L - R).max() < 1e-6: m['estereo'] = 'mono'
    else:
        c = float(np.corrcoef(L, R)[0, 1]) if L.std() > 0 and R.std() > 0 else 1.0
        m['estereo'] = 'casi mono' if c > 0.95 else 'estéreo' if c > 0.3 else 'estéreo muy abierto'
        m['correlacion_lr'] = round(c, 2)
    # bucle
    if m['duracion_s'] > 1.5 and (m['silencio_inicio_s'] or 0) < 0.05 and (m['silencio_final_s'] or 0) < 0.05:
        a = env[: int(0.25 * sr / hop)].mean(); z = env[-int(0.25 * sr / hop):].mean()
        m['bucle_posible'] = bool(abs(db(a) - db(z)) < 3 and m['rango_dinamico_db'] < 15)
    else: m['bucle_posible'] = False
    m['suena_como'] = frase(m); return m

def frase(m):
    d = m['duracion_s']; p = []
    at = m.get('ataque_s') if m.get('ataque_s') is not None else 1; pk = m.get('golpe_principal_s') or 0
    if m.get('tonal'): base = f"tono sostenido (~{m.get('tono_hz')} Hz, {m.get('nota')})"
    elif m.get('rango_dinamico_db', 99) < 8 and d >= 1.5: base = 'sonido continuo y estable (sin golpe)'
    elif d >= 8: base = 'grabación larga / ambiente' + (f" con {m['golpes']} golpes o eventos marcados" if (m.get('golpes') or 0) >= 3 else '')
    elif (m.get('golpes') or 0) >= 4 and d < 6: base = f"serie de {m['golpes']} golpes"
    elif at < 0.03 and (m.get('caida_s') or 9) < 0.6: base = 'golpe seco'
    elif at < 0.05: base = 'impacto con cola'
    elif at >= 0.4 and pk >= 0.5 * d: base = f"subida (riser) que crece hasta {pk} s" + (' y corta' if (m.get('caida_s') or 9) < 0.3 else ' y se apaga')
    elif d < 6: base = f'barrido (whoosh) que entra, llega al máximo a {pk} s y se va'
    elif m.get('rango_dinamico_db', 99) < 12: base = 'ambiente/textura continua'
    else: base = 'textura con cambios'
    p.append(base)
    g, a = m.get('graves_pct', 0), m.get('agudos_pct', 0)
    p.append('muy grave' if g > 60 else 'grave' if g > 40 else 'agudo/brillante' if a > 35 else 'de registro medio')
    if m.get('brillo_tendencia') in ('sube', 'baja'): p.append(f"el brillo {m['brillo_tendencia']}")
    if not m.get('tonal') and (m.get('planitud') or 0) > 0.25: p.append('ruidoso (tipo soplido o estática)')
    if m.get('bucle_posible'): p.append('podría ir en bucle')
    if (m.get('silencio_inicio_s') or 0) > 0.2: p.append(f"empieza con {m['silencio_inicio_s']} s de silencio")
    if not base.startswith(('barrido', 'subida')): p.append(f'máximo a {m["golpe_principal_s"]} s de {d} s')
    return ', '.join(p)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        try: print(json.dumps(dict(archivo=p, **medir(p)), ensure_ascii=False))
        except Exception as e: print(json.dumps(dict(archivo=p, error=str(e)[:100]), ensure_ascii=False))
