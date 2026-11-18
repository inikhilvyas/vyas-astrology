with open('sw.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
text = re.sub(r"const CACHE_NAME = 'vyas-astra-v2026-v4-full-precision-\d+';", "const CACHE_NAME = 'vyas-astra-v2026-v4-full-precision-9';", text)

with open('sw.js', 'w', encoding='utf-8') as f:
    f.write(text)

print("Bumped Service Worker to v9!")
