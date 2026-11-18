with open('mobile/index.html', 'r', encoding='utf-8') as f:
    m_text = f.read()

import re
matches = [m.start() for m in re.finditer('Abhijit', m_text, re.I)]
for p in matches:
    print(m_text[p-50:p+200])
    print("-"*40)

