with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('dPanChoghadiyaGrid')
print(content[idx-400:idx+600])

