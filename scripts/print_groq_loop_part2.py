with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('api.groq.com')
print(text[pos+1000:pos+2000])

