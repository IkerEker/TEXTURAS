import sys, re, xml.etree.ElementTree as ET
TICKS = 254016000000
def load(p):
    root = ET.parse(p).getroot()
    byid, byuid = {}, {}
    for el in root:
        if 'ObjectID' in el.attrib: byid[el.attrib['ObjectID']] = el
        if 'ObjectUID' in el.attrib: byuid[el.attrib['ObjectUID']] = el
    return root, byid, byuid
def ref(el, byid, byuid):
    if el is None: return None
    if 'ObjectRef' in el.attrib: return byid.get(el.attrib['ObjectRef'])
    if 'ObjectURef' in el.attrib: return byuid.get(el.attrib['ObjectURef'])
    return None
def media_name(ti, byid, byuid):
    sc = ref(ti.find('.//SubClip'), byid, byuid)
    if sc is None: return None, None
    clip = ref(sc.find('.//Clip'), byid, byuid)
    if clip is None: return sc.findtext('.//Name'), None
    src = ref(clip.find('.//Source'), byid, byuid)
    if src is None: return sc.findtext('.//Name'), None
    med = ref(src.find('.//Media'), byid, byuid)
    seq = None
    if med is not None:
        fp = med.findtext('.//ActualMediaFilePath') or med.findtext('.//FilePath') or ''
        if fp and not fp.isdigit():
            return re.split(r'[\\/]', fp)[-1], None
    s2 = ref(src.find('.//Sequence'), byid, byuid) if src is not None else None
    return sc.findtext('.//Name'), ('anidada' if s2 is not None or (src is not None and 'Sequence' in src.tag) else None)
def effects(ti, byid, byuid):
    out = []
    comps = ref(ti.find('.//ComponentOwner/Components'), byid, byuid)
    if comps is None: return out
    for c in comps.iter('Component'):
        ce = ref(c, byid, byuid)
        if ce is None: continue
        mn = ce.findtext('.//MatchName') or ''
        dn = ce.findtext('.//DisplayName') or ''
        params = {}
        for p in ce.iter('Param'):
            pe = ref(p, byid, byuid)
            if pe is None: continue
            nm = pe.findtext('.//Name') or ''
            val = pe.findtext('.//StartKeyframe') or pe.findtext('.//CurrentValue') or ''
            if nm: params[nm] = val.split(',')[1] if ',' in val else val
        out.append((mn or dn, params))
    return out
def main(p):
    root, byid, byuid = load(p)
    for seq in root.iter('Sequence'):
        name = seq.findtext('Name')
        if not name: continue
        tg = ref(seq.find('.//TrackGroups/TrackGroup/Second'), byid, byuid)
        if tg is None: continue
        rows = []
        tracks = [ref(t, byid, byuid) for t in tg.iter('Track')]
        for ti_, tr in enumerate(tracks):
            if tr is None or 'Video' not in tr.tag: continue
            for it in tr.iter('TrackItem'):
                ti = ref(it, byid, byuid)
                if ti is None or 'VideoClipTrackItem' not in ti.tag: continue
                st = int(ti.findtext('.//TrackItem/Start') or 0); en = int(ti.findtext('.//TrackItem/End') or 0)
                mn, kind = media_name(ti, byid, byuid)
                eff = effects(ti, byid, byuid)
                rows.append((ti_ + 1, st / TICKS, en / TICKS, mn, kind, eff))
        if rows:
            print(f'\n### {name}')
            for r in sorted(rows, key=lambda r: (r[1], r[0])):
                ef = []
                for mnm, pr in r[5]:
                    short = mnm.replace('AE.ADBE ', '')
                    keep = {k: v for k, v in pr.items() if re.search(r'blend|matte|composite|reverse|opacity', k, re.I)}
                    if short not in ('Motion',) or keep: ef.append(f'{short}{keep if keep else ""}')
                print(f'  V{r[0]} {r[1]:7.3f}-{r[2]:7.3f}s  {r[3]} {r[4] or ""}  | ' + '; '.join(ef))
main(sys.argv[1])
