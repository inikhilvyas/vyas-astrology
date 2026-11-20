with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 692700
print(text[pos:pos+3500])

