with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 390564
print(text[pos-200:pos+1500])

