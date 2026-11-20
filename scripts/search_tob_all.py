with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'split\(["\']:["]\)|tob|\.tob', text):
    st = max(0, m.start()-50)
    en = min(len(text), m.end()+80)
    print("Match at", m.start(), ":", repr(text[st:en].replace('\n', ' ')))

