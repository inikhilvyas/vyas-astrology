with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 482676
print(content[idx:idx+2000])

