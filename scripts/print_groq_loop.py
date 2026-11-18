with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('api.groq.com')
print(text[pos-400:pos+1500])

