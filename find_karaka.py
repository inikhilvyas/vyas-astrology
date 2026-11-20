with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('k.karaka')
print("Position:", pos)
print(text[pos-100:pos+200])

