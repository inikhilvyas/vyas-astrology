with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'shodhyaPindasTable', text)]
print('Matches in mobile:', len(matches))
for pos in matches:
    print(text[pos-50:pos+200])

