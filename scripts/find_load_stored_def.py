with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('loadStoredProfile:')
if pos == -1:
    pos = text.find('loadStoredProfile(')
if pos == -1:
    pos = text.find('loadStoredProfile()')

print("Pos:", pos)
print(text[pos:pos+1500])

