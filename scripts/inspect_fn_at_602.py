with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 602769
print(text[pos:pos+2500])

