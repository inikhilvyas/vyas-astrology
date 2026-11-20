with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'[\'"]d9[\'"]', content, re.IGNORECASE)]
print(f'd9 matches count: {len(matches)}')
for m in matches:
    print(f'--- MATCH AT {m} ---')
    print(content[max(0, m-80):min(len(content), m+200)])

