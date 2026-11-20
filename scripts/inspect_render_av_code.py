with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 549267
print(content[idx:idx+2500])

