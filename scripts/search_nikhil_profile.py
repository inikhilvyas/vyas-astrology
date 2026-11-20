with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'23°42\'00', content)]
print(f'23°42\'00 matches: {len(matches)}')
for m in matches:
    print(f'Match at {m}:')
    print(content[max(0, m-100):min(len(content), m+300)])

