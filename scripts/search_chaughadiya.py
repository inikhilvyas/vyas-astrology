with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'chaughadiya|चौघड़िया', content, re.IGNORECASE)]
print(f"Chaughadiya matches count: {len(matches)}")
for m in matches:
    print(content[max(0, m-50):min(len(content), m+200)])

