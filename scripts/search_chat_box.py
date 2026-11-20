with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'askSage|askAI|sendChat|aiMessage|concierge|आचार्य व्यास', text, re.I):
    st = max(0, m.start()-50)
    en = min(len(text), m.end()+100)
    print("Match at", m.start(), ":", text[st:en].replace('\n', ' '))

