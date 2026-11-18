with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Check for raw SVG snippets that aren't inside tags
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'viewBox' in line and not line.strip().startswith('<') and not 'var ' in line and not 'return ' in line and not "'" in line and not '"' in line:
        print(f"Suspicious line {i+1}: {line.strip()[:100]}")

# Check for leaked SVG attributes
for attr in ['width="15"', 'height="15"', 'stroke="#d4af37"', 'stroke-width="2"']:
    for i, line in enumerate(lines):
        if attr in line and not ('<' in line or "'" in line or '"' in line or '`' in line):
            print(f"Leaked attr at line {i+1}: {line.strip()[:100]}")

print("Leak scan completed!")

