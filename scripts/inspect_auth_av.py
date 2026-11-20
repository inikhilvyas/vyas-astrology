with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('ashtakavarga', content.find('var AUTHENTIC_BUNDLE'))
print(content[idx-50:idx+800])

