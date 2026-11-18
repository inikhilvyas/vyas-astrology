with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(name, dobStr')
print(text[pos:pos+3000])

