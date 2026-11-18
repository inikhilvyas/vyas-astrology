with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('loadStoredProfile', text)]
print("Total occurrences:", len(matches))
for p in matches:
    print(p, text[p-30:p+100])
    print("-"*40)

