with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'\.cockpit-grid|\.main-cockpit', content)]
print(f"cockpit matches count: {len(matches)}")
for m in matches:
    print(content[m:m+300])
    print('='*40)

