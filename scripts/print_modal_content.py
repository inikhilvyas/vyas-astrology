with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="modalGoogleAuth"')
print(text[pos:pos+4500])

