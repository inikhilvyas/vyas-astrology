with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderJaimini()')
print("renderJaimini in index.html:")
print(text[pos:pos+800])
