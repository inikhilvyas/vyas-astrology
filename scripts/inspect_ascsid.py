with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('var ascSid =')
print("ascSid found at", idx)
if idx != -1:
    print(text[idx-200:idx+800])

