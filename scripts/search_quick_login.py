with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'quickLoginFounder|nikhilvyas007', text, re.I):
    st = max(0, m.start()-80)
    en = min(len(text), m.end()+80)
    print("Match at", m.start(), ":", repr(text[st:en]))

