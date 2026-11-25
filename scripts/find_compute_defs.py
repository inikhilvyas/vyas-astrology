with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    d_text = f.read()

with open('mobile/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    m_text = f.read()

import re

for label, text in [("DESKTOP", d_text), ("MOBILE", m_text)]:
    matches = list(re.finditer(r'computeMathematicalKundli\s*\([^)]*\)\s*\{', text))
    print(f"=== {label} DEFINITION matches: {len(matches)} ===")
    for m in matches:
        idx = m.start()
        print(f"Match at {idx}:")
        print(text[idx:idx+800])
        print("=" * 60)

