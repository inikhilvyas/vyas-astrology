with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

import re
matches = list(re.finditer(r'var yAsc\s*=', d_text))
print("Found yAsc in desktop index.html:", len(matches))
for m in matches:
    idx = m.start()
    print(d_text[max(0, idx-300):min(len(d_text), idx+600)])
    print("=" * 60)

matches2 = list(re.finditer(r'computeMathematicalKundli', d_text))
print("Found computeMathematicalKundli in desktop index.html:", len(matches2))
for m in matches2:
    idx = m.start()
    print(d_text[max(0, idx):min(len(d_text), idx+600)])
    print("=" * 60)

