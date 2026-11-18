with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'id=["\'](?:inpCity|modalNewKundli|modalNewChart|citySuggestions|inpLat|inpLon)["\']', text)]
print(f"Found {len(matches)} matches")
for idx in matches:
    print('--- MATCH ---')
    print(text[max(0, idx-100):min(len(text), idx+400)])
