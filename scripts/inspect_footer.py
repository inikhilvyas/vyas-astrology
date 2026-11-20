with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'<footer', text, re.I))
for m in matches:
    pos = m.start()
    print("Footer at:", pos)
    print(text[pos:pos+2500])

