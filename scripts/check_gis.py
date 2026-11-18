with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('google.accounts.id.initialize')
if pos != -1:
    print(text[pos-100:pos+1500])
else:
    print("initialize not found")

