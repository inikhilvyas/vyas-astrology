import re

files = ['index.html', 'mobile.html', 'admin.html', 'mobile.js', 'mobile_dasha_full.js', 'init_dasha_full.js']
keywords = ['संस्थापक', 'Founder', '1click', '1-click', '1 click', 'quickLogin', '9414121172', 'nikhilvyas']

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            c = fh.read()
        for k in keywords:
            for m in re.finditer(re.escape(k), c, re.I):
                st = max(0, m.start()-70)
                en = min(len(c), m.end()+70)
                print(f"[{f}] {k} at {m.start()}: {repr(c[st:en])}")
    except FileNotFoundError:
        pass

