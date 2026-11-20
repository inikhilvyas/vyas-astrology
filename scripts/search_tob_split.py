with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('tobStr.split')
while pos != -1:
    print("Match at", pos)
    print(text[pos-100:pos+300])
    print("-" * 50)
    pos = text.find('tobStr.split', pos+20)

