with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\[data-theme=["\']?light["\']?\].*?\{.*?\}', text, re.DOTALL)
print('Light theme CSS rules in index.html:', len(matches))
for m in matches[:5]:
    print('Rule:', m[:150].replace('\n', ' '))

# Check theme variables
vars_dark = re.findall(r':root\s*\{([^}]+)\}', text)
if vars_dark:
    print("\nRoot variables sample:")
    print(vars_dark[0][:300])

vars_light = re.findall(r'\[data-theme=["\']?light["\']?\]\s*\{([^}]+)\}', text)
if vars_light:
    print("\nLight theme variables sample:")
    print(vars_light[0][:300])
