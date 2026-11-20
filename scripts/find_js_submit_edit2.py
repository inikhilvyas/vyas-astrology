with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('submitProfileEdit() {')
if idx == -1: idx = text.find('submitProfileEdit: function')
if idx == -1: idx = text.find('submitProfileEdit')
# search for occurrences after char 200000
idx = text.find('submitProfileEdit', 200000)
print("Found submitProfileEdit after 200000 at", idx)
if idx != -1:
    print(text[idx-50:idx+1500])

