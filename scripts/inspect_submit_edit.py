with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('submitProfileEdit(')
if idx == -1: idx = text.find('submitProfileEdit')
print(text[idx-50:idx+1500])

