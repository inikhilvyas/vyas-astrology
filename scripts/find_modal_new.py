with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('modalNewProfile')
print("modalNewProfile found at", idx)
if idx != -1:
    print(text[idx:idx+1500])

