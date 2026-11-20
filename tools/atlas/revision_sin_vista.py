"""Fichas de lo que no se puede mirar como imagen: sonido (no se escucha, regla de la noche) y plantillas o proyectos
de editor (.drt, .prfpset, .mogrt, .prproj, .aep). Se copia lo que ya sabía el índice y se marca
revisado_por_vista: false (y audio_revisado: false en el sonido).

  python3 tools/atlas/revision_sin_vista.py   → revision/fichas/zz_sin_vista.json
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RV = ROOT / 'revision'
EXT = {'drt': 'plantilla de DaVinci Resolve (.drt)', 'prfpset': 'preajuste de efectos de Premiere (.prfpset)',
       'mogrt': 'plantilla de gráficos animados de Premiere (.mogrt)', 'prproj': 'proyecto de Premiere (.prproj)',
       'aep': 'proyecto de After Effects (.aep)'}


def main():
    A = json.load(open(ROOT / 'indice/indice.json'))['assets']
    vistas = set()
    for f in (RV / 'fichas').glob('*.json'):
        if f.name != 'zz_sin_vista.json':
            vistas |= set(json.load(open(f)))
    med = {}
    if (RV / 'audio_medido.json').exists(): med = json.load(open(RV / 'audio_medido.json'))['sonidos']
    plt = {}
    if (RV / 'plantillas_leidas.json').exists(): plt = json.load(open(RV / 'plantillas_leidas.json'))['plantillas']
    out = {}
    for a in A:
        if a['id'] in vistas:
            continue
        nombre = a['archivo'].rsplit('/', 1)[-1]
        base = dict(familia=None, variante=None, diferencia='-', mejor_de_familia=False, calidad=None,
                    revisado_por_vista=False, rehacer=False, dudoso=False, fecha='2026-11-20',
                    pack=a.get('pack'), licencia=a.get('licencia'))
        if a.get('tipo') == 'audio':
            au = a.get('audio') or {}
            env = au.get('envolvente') or {}
            base.update(
                nivel='sin_vista (sonido, no escuchado)',
                que_es=f'efecto de sonido «{nombre}» del pack {a.get("pack")} ({a.get("sub")}); forma medida: '
                       f'{env.get("forma", "?")}, {au.get("duracion", "?")} s, pico {env.get("pico_dbfs", "?")} dBFS',
                defectos='no escuchado',
                uso=f'sonido de {a.get("sub")} para acompañar transiciones o elementos'
                    + (' (va con los clips ' + ', '.join(au['clips']) + ')' if au.get('clips') else ''),
                modo='audio', audio_conocido=au, audio_revisado=False,
                estilo=', '.join(a.get('estilos') or []))
            m = med.get(a['id'])
            if m:
                base.update(nivel='medido (sin escuchar)', audio_medido=m,
                            que_es=base['que_es'] + '; medido: ' + m['suena_como'],
                            defectos='no escuchado: la descripción sale de medirlo (duración, nivel, golpes, graves/agudos, brillo)',
                            escala=f"{m.get('duracion_s')} s", orient=m.get('estereo', '-'))
        else:
            ext = nombre.rsplit('.', 1)[-1].lower()
            base.update(
                nivel='sin_vista (plantilla o proyecto de programa)',
                que_es=f'{EXT.get(ext, "archivo de programa")} «{nombre}»' + (f' del pack {a.get("pack")}' if a.get('pack') else ''),
                defectos='no es una imagen ni un vídeo: no se puede mirar en una hoja; solo funciona dentro de su programa',
                uso='abrir en el programa correspondiente; no sirve para los plugins (que solo usan imágenes y vídeos)',
                modo='no aplica')
            pl = plt.get(a['id'])
            if pl:
                base.update(nivel='leído por dentro (sin abrir el programa)', plantilla_leida=pl,
                            que_es=base['que_es'] + '; ' + pl['resumen'])
        out[a['id']] = base
    json.dump(out, open(RV / 'fichas' / 'zz_sin_vista.json', 'w'), ensure_ascii=False, indent=0)
    print('fichas sin vista:', len(out))


if __name__ == '__main__':
    main()
