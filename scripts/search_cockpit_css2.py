with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
for m in re.finditer(r'\.cockpit-col|\.app-layout|\.dashboard-grid|\.desktop-container', content):
    print(m.start())
    print(content[m.start():m.start()+250])
    print('='*40)

