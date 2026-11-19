"""Lee presets de Premiere (.prfpset): por preset, efectos y parámetros. Uso: leer_presets.py <salida.json> <prfpset...>"""
import sys, json, os, xml.etree.ElementTree as ET
res = {}
for f in sys.argv[2:]:
    root = ET.parse(f).getroot()
    out, preset, eff = {}, os.path.basename(f), None
    for el in root:
        mn = el.findtext('.//MatchName')
        nm = el.findtext('Name')
        if mn and 'Component' in el.tag:
            eff = dict(efecto=mn.replace('AE.ADBE ', '').replace('PR.ADBE ', ''), params={})
            out.setdefault(preset, []).append(eff)
        elif el.tag.endswith('Param') and eff is not None:
            pn = (el.findtext('Name') or '').strip(':')
            v = el.findtext('StartKeyframe') or el.findtext('CurrentValue') or ''
            if pn: eff['params'][pn] = v.split(',')[1] if ',' in v else v
        elif nm and el.tag not in ('Tree',) and nm not in ('Root', 'Presets'):
            preset, eff = nm, None
    res[os.path.basename(f)] = out
json.dump(res, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
for f, ps in res.items():
    for p, L in ps.items():
        for e in L:
            if 'Track Matte' in e['efecto']: print(p, '|', {k: v for k, v in e['params'].items() if k in ('Matte', 'Composite Using', 'Reverse')})
