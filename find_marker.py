with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find("// vyas_daivagya_vision.js")
print("Desktop pos1:", pos1)
print(text[pos1+31000:pos1+33000])
