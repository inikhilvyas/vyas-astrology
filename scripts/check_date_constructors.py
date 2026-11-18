with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# search where Date is calculated or formatted
matches = re.finditer(r'new Date\((.*?)\)', text)
dates_found = set()
for m in matches:
    arg = m.group(1).strip()
    if arg and len(arg) < 50:
        dates_found.add(arg)

print("Dates found in new Date(...):")
for d in sorted(list(dates_found))[:30]:
    print(" ", d)

