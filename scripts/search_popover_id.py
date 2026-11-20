with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'userProfilePopover', text):
    st = max(0, m.start()-80)
    en = min(len(text), m.end()+120)
    print("Match at", m.start(), ":", repr(text[st:en]))

