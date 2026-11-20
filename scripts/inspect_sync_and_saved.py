with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('syncCloudProfiles')
while pos != -1:
    print("Match at", pos)
    print(text[pos-50:pos+800])
    print("-" * 50)
    pos = text.find('syncCloudProfiles', pos+20)

pos2 = text.find('openSavedProfilesModal')
while pos2 != -1:
    print("openSavedProfilesModal at", pos2)
    print(text[pos2-50:pos2+800])
    print("-" * 50)
    pos2 = text.find('openSavedProfilesModal', pos2+20)

