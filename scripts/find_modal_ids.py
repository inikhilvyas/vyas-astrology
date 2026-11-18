with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'id=["\']([a-zA-Z0-9_-]*modal[a-zA-Z0-9_-]*)["\']', text, re.I)
print("Modal IDs found:", set(matches))

pos = text.find('closeModals')
if pos != -1:
    print(text[pos-50:pos+300])

