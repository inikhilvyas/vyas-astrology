with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('submitProfileEdit: function')
if pos == -1:
    pos = text.find('submitProfileEdit(')
    pos = text.find('submitProfileEdit', pos+20)

print("submitProfileEdit fn pos:", pos)
if pos != -1:
    print(text[pos-50:pos+1500])

pos2 = text.find('submitNewProfile: function')
if pos2 == -1:
    pos2 = text.find('submitNewProfile(')
    pos2 = text.find('submitNewProfile', pos2+20)

print("submitNewProfile fn pos:", pos2)
if pos2 != -1:
    print(text[pos2-50:pos2+1500])

