import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- 1. MODAL EDIT PROFILE ---")
pos = text.find('id="modalEditProfile"')
if pos != -1:
    print(text[pos:pos+1500])
else:
    print("modalEditProfile NOT found with id=\"modalEditProfile\"")
    for m in re.finditer(r'modalEditProfile', text):
        print(text[m.start()-50:m.start()+200])

print("\n--- 2. MODAL GOOGLE AUTH ---")
pos = text.find('id="modalGoogleAuth"')
if pos != -1:
    print(text[pos:pos+1500])
else:
    print("modalGoogleAuth NOT found")

print("\n--- 3. OPEN NEW PROFILE MODAL IMPLEMENTATION ---")
pos = text.find('openNewProfileModal')
while pos != -1:
    print(text[pos-50:pos+300])
    pos = text.find('openNewProfileModal', pos+20)
    if pos > 480000: break

