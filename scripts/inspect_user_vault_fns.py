with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('loadFromUserVault')
while pos != -1:
    print("Match at", pos)
    print(text[pos-50:pos+500])
    print("-" * 50)
    pos = text.find('loadFromUserVault', pos+20)

