with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('updateGoogleAuthUI: function')
if pos == -1:
    pos = text.find('updateGoogleAuthUI()')
    pos = text.find('updateGoogleAuthUI', pos+20)

print("updateGoogleAuthUI fn pos:", pos)
if pos != -1:
    print(text[pos-50:pos+1500])

