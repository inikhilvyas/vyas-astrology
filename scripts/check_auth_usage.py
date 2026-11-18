with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\w*(?:googleUser|isLoggedIn|requireAuth|checkAuth|userProfile|VIP)\w*)', text)
counts = {}
for m in matches:
    counts[m] = counts.get(m, 0) + 1

for k, v in sorted(counts.items(), key=lambda x: -x[1])[:25]:
    print(f'{k}: {v}')

