with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'toISOString', text)]
print(f"Total toISOString: {len(matches)}")
for pos in matches:
    print(text[pos-50:pos+100])
    print("-"*40)

