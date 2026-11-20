with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('var AUTHENTIC_BUNDLE')
print(content[idx:idx+3500])

