#!/usr/bin/env python3
"""Rebuild the CKW_USAGE table in index.html from the production planner.

The Fabric usage tab needs metres of cloth per garment for every code that
Clockwork make for us. The production planner already carries that figure for
8,000-odd codes (its FABRIC_USAGE table, taken from the All Costings sheet,
and FABRIC_MARKERS, the cutting room's lay plans). This script copies the
figures for the codes that matter here - every code in the planner's own
data.json (stock rows, open and booked containers) and every other size or
colour of the same style - into index.html as CKW_USAGE, so the tab needs no
live link to the other app.

    python3 tools/build-fabric-usage.py [path/to/Tibard-Productionplan/index.html]

Run it again when the production planner's usage tables change (a new style,
a corrected figure) and commit the result. A code with no figure here is
shown on the tab as a gap, and a figure typed on the tab outranks this table.

CKW_USAGE = { code: [metres of main cloth per garment, metres of mesh or 0] }
"""
import json, re, sys, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, '..', 'index.html')
PP = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'Tibard-Productionplan', 'index.html')

SIZE = {'%02d' % n for n in range(6, 61, 2)}
CUST = re.compile(r'^(ABS|ALS|ANG|ASK|BC|BEEF|BE|BID|CAR|FB|INN|MIL|MVS|PE|SL|TGI|TW|WAG|YO)(?=(CI|CJ|CT|AP|HT|TB|WT|WCL|NOTS))')

def split_code(code):
    """code -> (stem, colour, suffix): CJ01935201 -> (CJ0193, 01, '').
    Mirrors splitCode() in index.html; keep the two the same."""
    c = code.strip().upper()
    m = re.match(r'^([A-Z0-9]+?)(\d{2})([A-Z]{0,3}|/\d{1,3})$', c)
    if not m:
        return (c, '', '')
    rest, col, suf = m.group(1), m.group(2), m.group(3)
    m2 = re.match(r'^(.*?)(XXL|XS|SS|MM|LL|XL|XX)$', rest)
    if m2 and len(m2.group(1)) >= 4:
        return (m2.group(1), col, suf)
    m3 = re.match(r'^(.*?)(\d{2})$', rest)
    if m3 and m3.group(2) in SIZE and (re.search(r'\d{4}$', m3.group(1)) or re.search(r'[A-Z]{3}$', m3.group(1))):
        return (m3.group(1), col, suf)
    return (rest, col, suf)

def base_stem(stem):
    s = CUST.sub('', stem)
    s = re.sub(r'ECO$', '', s)
    return s

def main():
    page = open(PAGE, encoding='utf-8').read()
    pp = open(PP, encoding='utf-8').read()
    fu = json.loads(re.search(r'var FABRIC_USAGE=(\{.*?\});', pp, re.S).group(1))
    fm = json.loads(re.search(r'var FABRIC_MARKERS=(\{.*?\});', pp, re.S).group(1))
    data = json.load(open(os.path.join(HERE, '..', 'data.json'), encoding='utf-8'))
    codes = set(r['code'].upper() for r in data.get('rows', []))
    for po in data.get('cPOs', []) + data.get('bookedPOs', []):
        for it in po.get('items', []):
            codes.add(str(it.get('code', '')).upper())
    stems = set()
    for c in codes:
        st = split_code(c)[0]
        stems.add(st); stems.add(base_stem(st))
    out = {}
    for code in sorted(set(fu) | set(fm)):
        st = split_code(code)[0]
        if st not in stems and base_stem(st) not in stems:
            continue
        m = fu.get(code, [None, 0])[1] or 0
        mesh = 0
        if code in fm and fm[code][0] > 0:
            m = fm[code][0]           # the cutting room's marker outranks All Costings
            mesh = fm[code][1] or 0
        if not m:
            continue
        out[code] = [round(float(m), 3), round(float(mesh), 3)]
    js = 'var CKW_USAGE=' + json.dumps(out, separators=(',', ':')) + ';'
    new, n = re.subn(r'var CKW_USAGE=\{.*?\};', lambda _: js, page, count=1, flags=re.S)
    if n != 1:
        sys.exit('CKW_USAGE not found in index.html')
    open(PAGE, 'w', encoding='utf-8').write(new)
    have = sum(1 for c in codes if c in out)
    print('CKW_USAGE: %d codes written; %d of the %d codes in data.json have a direct figure' % (len(out), have, len(codes)))

if __name__ == '__main__':
    main()
