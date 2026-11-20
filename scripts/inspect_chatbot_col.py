with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 171312
print(content[idx-300:idx+1500])

