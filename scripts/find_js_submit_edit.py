with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('submitProfileEdit:')
if idx == -1: idx = text.find('submitProfileEdit()')
if idx == -1: idx = text.find('submitProfileEdit')
print("Found submitProfileEdit at", idx)
print(text[idx:idx+1500])

