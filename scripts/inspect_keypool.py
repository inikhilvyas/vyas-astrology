with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('keyPool:')
if pos != -1:
    print(text[pos-50:pos+1500])

