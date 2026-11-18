with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'dms:\s*"[^"]*""', text)
print("Unescaped dms quotes:", matches)

matches2 = re.findall(r'.{0,40}\d+°\d+\'\d+""', text)
print("Unescaped degree quotes:", matches2)

