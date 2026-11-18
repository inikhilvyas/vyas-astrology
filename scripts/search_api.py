with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
keywords = ['fetch(', 'XMLHttpRequest', 'api/', 'streamlit', 'iframe']
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), text)]
    print(f"=== {kw} ({len(matches)} occurrences) ===")
    for m in matches[:5]:
        print(f"  {text[m-20:m+80].strip()[:80]}")

