with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 485354
print(content[idx+2000:idx+4000])

