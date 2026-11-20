with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('renderAshtakavarga')
print('renderAshtakavarga at:', idx)
if idx != -1:
    print(content[idx:idx+2500])

