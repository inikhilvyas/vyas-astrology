with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

patterns = [
    r'1984-11-23',
    r'Falna',
    r'16:51',
    r'217\.7138',
    r'224\.6495',
    r'281\.9427',
    r'224\.639',
    r'nikhilvyas007',
    r'quickLoginFounder',
    r'1-क्लिक संस्थापक',
    r'isFounderPrecise'
]

for pat in patterns:
    matches = list(re.finditer(pat, text, re.I))
    print(f"Pattern '{pat}': {len(matches)} matches")
    for m in matches[:5]:
        st = max(0, m.start()-60)
        en = min(len(text), m.end()+60)
        print("  Line approx:", text[:m.start()].count('\n')+1, ":", repr(text[st:en].replace('\n', ' ')))

