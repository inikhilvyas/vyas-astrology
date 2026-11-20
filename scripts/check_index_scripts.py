with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script\b[^>]*src=[\'"]([^\'"]+)[\'"]', text, re.I)
print("Script tags with src in index.html:")
for s in scripts:
    print(" ", s)

print("\nVyasSutrasBank occurrences in index.html:")
for m in re.finditer(r'VyasSutrasBank', text):
    start = max(0, m.start() - 60)
    end = min(len(text), m.end() + 60)
    print(" ", text[start:end].replace('\n', ' '))

