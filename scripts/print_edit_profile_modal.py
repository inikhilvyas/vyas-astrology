with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="modalEditProfile"')
if idx == -1:
    idx = text.find("id='modalEditProfile'")
print(text[idx:idx+2500])
