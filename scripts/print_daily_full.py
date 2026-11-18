with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('vTodayTaraVal')
print("Found vTodayTaraVal at", pos)
print(text[pos-200:pos+2500])

