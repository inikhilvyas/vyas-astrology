with open('mobile.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'परिचय|bio|founder|संस्थापक|nikhil vyas|1click|1-click', text, re.I):
    st = max(0, m.start()-80)
    en = min(len(text), m.end()+80)
    print(f"[mobile.html] Match at {m.start()}: {text[st:en].replace(chr(10), ' ')}")

