with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'renderDailyHoroscope\s*:\s*function', text):
    pos = m.start()
    print(text[pos:pos+1500])
    print("="*60)

