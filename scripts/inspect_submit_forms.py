with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('submitProfileEdit')
if pos != -1:
    print("submitProfileEdit:")
    print(text[pos:pos+1500])

pos2 = text.find('submitNewProfile')
if pos2 != -1:
    print("submitNewProfile:")
    print(text[pos2:pos2+1500])

