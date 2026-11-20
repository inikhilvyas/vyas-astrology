with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 509848
print(content[idx-1200:idx+1500])

