with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 631140
print(content[idx:idx+4500])

