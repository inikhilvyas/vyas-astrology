with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'id=["\']([a-zA-Z0-9_]*Modal)["\']', text)
print("Modals found:", set(matches))

