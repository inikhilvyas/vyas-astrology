with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'31.*26.*29.*24', content)]
print(f"Matches count: {len(matches)}")
for m in matches:
    print(f"Match at {m}:")
    print(content[max(0, m-50):min(len(content), m+200)])

