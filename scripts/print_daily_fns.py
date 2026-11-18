with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for fn in ['updateDailyHoroscopeUI', 'initDailyDashboard', 'renderPanchang']:
    pos = text.find(fn)
    if pos != -1:
        print(f"=== Function: {fn} (pos {pos}) ===")
        print(text[pos:pos+1500])
        print("="*60)

