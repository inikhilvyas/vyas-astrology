with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function\s+([a-zA-Z0-9_]*Profile[a-zA-Z0-9_]*)\s*\(', text)
print("Profile functions:", matches)

matches2 = re.findall(r'([a-zA-Z0-9_]*Profile[a-zA-Z0-9_]*)\s*:\s*function', text)
print("Profile methods:", matches2)

