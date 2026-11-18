with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="googleAuthModal"')
if pos != -1:
    print(text[pos-50:pos+1200])
else:
    print("googleAuthModal not found")

