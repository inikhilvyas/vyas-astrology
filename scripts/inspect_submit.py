with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('submitNewProfileModal(')
if idx == -1: idx = text.find('submitNewProfileModal')
print(text[idx-50:idx+2000])

