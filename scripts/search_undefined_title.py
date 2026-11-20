with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'chartHeaderTitle|\+.*title', content, re.IGNORECASE)]
print(f"Matches count: {len(matches)}")
for m in matches:
    print(content[max(0, m-50):min(len(content), m+150)])
    print('-'*30)

