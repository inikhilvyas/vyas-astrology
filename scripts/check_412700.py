with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 412700
print(text[pos-100:pos+600])

