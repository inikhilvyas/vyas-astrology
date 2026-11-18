with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('api.groq.com')
if pos != -1:
    print(text[pos-400:pos+800])

