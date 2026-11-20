with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('modalEditProfile')
print(text[idx-100:idx+2000])

