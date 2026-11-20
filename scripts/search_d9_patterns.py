with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'[\'"]\s*D9[\'"]|\+.*D9|\bvk\b|vargaKey', content)]
print(f'Matches count: {len(matches)}')
found = []
for m in re.finditer(r'\+\s*[\'"][ ]*D[0-9]+[\'"]|\bvk\.toUpperCase\(\)|\bD9\b', content):
    line = content[max(0, m.start()-100):min(len(content), m.start()+150)]
    found.append(line)

print(f"Specific found count: {len(found)}")
for l in found[:20]:
    print("---")
    print(l)

