with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('Sign circle badge')
print(content[idx:idx+1500])

