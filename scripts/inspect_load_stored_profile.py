with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('loadStoredProfile() {')
print(text[pos+2000:pos+4000])
