with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'def\s+[a-zA-Z0-9_]+\s*\(', text)]
print(f"Found {len(matches)} functions in app.py:")
for m in matches[:25]:
    line = text[m:text.find('\n', m)]
    print(" ", line)

