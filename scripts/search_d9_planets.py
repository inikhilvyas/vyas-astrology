with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'गुरु D9|मंगल D9|सूर्य D9|केतु D9', content)]
print(f'Matches count: {len(matches)}')
for m in matches:
    print(f'Match at {m}:')
    print(content[max(0, m-100):min(len(content), m+200)])

