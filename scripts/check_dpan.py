with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'id=["\']dPan\w+["\']', text)
print("Panchang elements:", set(matches))

# Also search for where dPan elements are assigned in JS
matches2 = re.findall(r'el\w+\.innerText\s*=\s*[^;\n]+', text)
for m in matches2[:25]:
    print(" ", m)

