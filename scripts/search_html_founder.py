with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'परिचय|bio|founder|about|nikhil vyas', text, re.I):
    st = max(0, m.start()-80)
    en = min(len(text), m.end()+80)
    # filter out js comments or scripts
    snippet = text[st:en]
    if '<' in snippet and '>' in snippet:
        print(f"HTML Match at {m.start()}: {snippet.replace(chr(10), ' ')}")

