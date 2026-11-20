with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('async askSage(query, activeChart)')
print(text[pos+800:pos+2500])
