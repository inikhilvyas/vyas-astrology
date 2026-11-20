with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'<div[^>]*class=["\'][^"\']*modal[^"\']*["\'][^>]*id=["\']([^"\']+)["\']', text, re.I):
    print("Modal ID:", m.group(1))

pos = 715849
st = text.rfind('<div', 0, pos)
# search backwards for id
while st > 0 and 'id=' not in text[st:pos]:
    st = text.rfind('<div', 0, st)
print("Enclosing container:\n", text[st:st+300])

