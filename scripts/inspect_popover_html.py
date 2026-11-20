with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 76029
print(text[pos-100:pos+1200])

