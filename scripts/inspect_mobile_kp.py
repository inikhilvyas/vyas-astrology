with open('mobile/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="view-kp"')
print(text[idx-50:idx+800])

