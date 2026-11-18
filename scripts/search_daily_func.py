with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'daily', text, re.I)]
print(f"Total 'daily' occurrences: {len(matches)}")

for pos in matches:
    snippet = text[pos-30:pos+100]
    if any(k in snippet for k in ['function', 'render', 'Personalized', ' राशिफल']):
        print(f"Pos {pos}: {snippet}")

