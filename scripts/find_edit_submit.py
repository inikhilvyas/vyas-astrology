with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('modalEditProfile')
idx2 = text.find('</form>', idx)
if idx2 == -1: idx2 = text.find('</div>\n    </div>\n', idx + 500)
print(text[idx:idx2+500])

