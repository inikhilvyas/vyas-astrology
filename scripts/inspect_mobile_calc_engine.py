with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

# Find calculation engine inside mobile/index.html
print("=== CALCULATION IN MOBILE/INDEX.HTML ===")
for m in re.finditer(r'var ayanamsa = norm\(23\.8', text):
    idx = m.start()
    print("Found ayanamsa calculation at", idx)
    print(text[max(0, idx-500):min(len(text), idx+1500)])
    print("=" * 60)

# Find Ashtakavarga table rendering
print("=== ASHTAKAVARGA RENDERING ===")
for m in re.finditer(r'renderPavTable|renderAshtakavarga|bavTable|ashtakavargaTable', text):
    idx = m.start()
    print("Found AV match at", idx)
    print(text[max(0, idx-100):min(len(text), idx+600)])
    print("=" * 60)

