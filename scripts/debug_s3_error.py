import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
s3 = scripts[3]
lines = s3.split('\n')
for i in range(max(0, 5140), min(len(lines), 5160)):
    print(f'{i+1}: {repr(lines[i])}')
