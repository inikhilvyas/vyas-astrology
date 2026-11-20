with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('openEditProfileModal: function')
if pos == -1:
    pos = text.find('openEditProfileModal()')
    pos = text.find('openEditProfileModal', pos+20)

print("openEditProfileModal fn pos:", pos)
if pos != -1:
    print(text[pos-50:pos+1500])

