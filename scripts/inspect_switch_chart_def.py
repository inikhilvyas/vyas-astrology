with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
for m in re.finditer(r'switchChart\s*\(|switchChart\s*:\s*function', content):
    print(m.start())
    print(content[m.start()-50:m.start()+400])
    print('='*40)

