with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('isNikhilVyas &&')
print(text[idx+3000:idx+5500])

