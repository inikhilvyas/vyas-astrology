with open('mobile/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re

# Fix any unescaped double quotes inside double-quoted JS strings in vratsByTithi
def fix_line(line):
    if '<svg class="v-icon' in line and (line.strip().startswith('"') or re.match(r'^\s*\d+:\s*"', line)):
        # replace unescaped inner double quotes with \"
        # e.g. 10: "<svg class=\"v-icon...
        return re.sub(r'class="([^"]*)"', r'class=\"\1\"', line)
    return line

lines = content.split('\n')
for i, l in enumerate(lines):
    if '<svg class="v-icon' in l:
        # replace double quotes inside svg with single quotes
        # e.g. <svg class='v-icon' viewBox='0 0 24 24'...
        lines[i] = re.sub(r'(\w+)="([^"]*)"', r"\1='\2'", l)

with open('mobile/index.html', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Fixed quotes in mobile/index.html!")
