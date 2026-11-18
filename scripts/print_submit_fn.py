with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('submitProfileEdit:')
if idx == -1: idx = text.find('submitProfileEdit()')
if idx != -1:
    print(text[idx:idx+1500])
else:
    print("Not found with colon")
