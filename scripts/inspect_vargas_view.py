with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-vargas"')
print(text[idx-50:idx+2000])

