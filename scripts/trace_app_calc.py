with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'def\s+calculate_[a-zA-Z0-9_]*', text)]
print(f"Found {len(matches)} calculate_ functions in app.py:")
for m in matches[:15]:
    line = text[m:text.find('\n', m)]
    print(" ", line)

