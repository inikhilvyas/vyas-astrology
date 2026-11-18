with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'.{0,40}(?:17|18)\s*(?:नवंबर|Nov|nov|November|नवम्बर).{0,40}', text, re.I)
for m in matches[:20]:
    print(m)

print("--- Check Dasha dates or other date displays ---")
matches2 = re.findall(r'.{0,40}17/11/.{0,40}', text)
for m in matches2[:10]:
    print(m)
matches3 = re.findall(r'.{0,40}18/11/.{0,40}', text)
for m in matches3[:10]:
    print(m)

