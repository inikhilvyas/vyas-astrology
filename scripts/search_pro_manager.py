with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'modalProManager', text):
    st = max(0, m.start()-100)
    en = min(len(text), m.end()+200)
    print("Match at", m.start(), ":\n", text[st:en])
    print("-" * 50)

