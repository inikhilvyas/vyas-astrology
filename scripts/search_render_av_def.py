with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('renderAshtakavarga()')
if idx == -1:
    idx = content.find('renderAshtakavarga(')
    idx = content.find('renderAshtakavarga', idx+1)
print('renderAshtakavarga definition at:', idx)
print(content[idx:idx+2500])

