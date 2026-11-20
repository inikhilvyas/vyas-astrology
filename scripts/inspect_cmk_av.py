with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('10. AUTHENTIC PARASHARI BPHS ASHTAKAVARGA ENGINE')
print(content[idx:idx+2500])

