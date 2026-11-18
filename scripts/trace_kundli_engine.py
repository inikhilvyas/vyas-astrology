with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
keywords = [
    'AUTHENTIC_BUNDLE',
    'computeMathematicalKundli',
    'loadStoredProfile',
    'loadAuthenticProfile',
    'renderChart',
    'drawNorthIndianChart',
    'planet_table'
]

for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), text)]
    print(f"=== {kw} ({len(matches)} occurrences) ===")
    for m in matches[:4]:
        print(f"  at {m}: {text[m-40:m+120].strip()[:100]}")

