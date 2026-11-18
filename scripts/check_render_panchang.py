with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('renderPanchang: function()')
print(text[pos:pos+3500])

