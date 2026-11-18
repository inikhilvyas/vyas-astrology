with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('panchangDateInput', text)]
print(f"panchangDateInput matches: {len(matches)}")
for pos in matches:
    print(text[pos-100:pos+200])
    print("-" * 50)

