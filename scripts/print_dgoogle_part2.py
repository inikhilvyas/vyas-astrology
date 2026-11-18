with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="dGoogleUnauth"')
print(text[pos+1000:pos+3000])

