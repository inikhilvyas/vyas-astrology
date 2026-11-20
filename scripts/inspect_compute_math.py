with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(name, dobStr, tobStr')
if pos != -1:
    print(text[pos:pos+2500])

