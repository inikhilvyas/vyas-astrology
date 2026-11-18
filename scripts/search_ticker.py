with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer('headerPanchangTicker', text):
    pos = m.start()
    print(text[pos-100:pos+300])
    print("="*60)

