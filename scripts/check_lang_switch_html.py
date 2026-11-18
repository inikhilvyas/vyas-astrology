with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="langSwitchBtn"')
print(text[pos:pos+700])

