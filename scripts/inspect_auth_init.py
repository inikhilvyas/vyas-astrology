with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 377171
print(text[pos-200:pos+1200])

