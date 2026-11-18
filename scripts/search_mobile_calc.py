with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'computeMathematicalKundli', text)]
print(f"computeMathematicalKundli in mobile/index.html: {len(matches)}")
for m in matches:
    print(text[m-50:m+150])

