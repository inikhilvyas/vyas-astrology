with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<div\b[^>]*id=["\']modalGoogleAuth["\'][^>]*>.*?(?=<!--\s*End\s*modalGoogleAuth|</div>\s*</div>\s*</div>)', text, re.DOTALL)
if m:
    print('Found modalGoogleAuth snippet (length:', len(m.group(0)), ')')
    print(m.group(0)[:800])
else:
    print('Not found directly.')

