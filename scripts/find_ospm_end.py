with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('openSavedProfilesModal')
print("openSavedProfilesModal found at:", pos)
if pos != -1:
    print(text[pos:pos+1500])

