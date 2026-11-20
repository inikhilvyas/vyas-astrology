with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 689242
print(text[pos:pos+3500])

