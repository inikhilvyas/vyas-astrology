with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 602769
pos2 = text.find('loadCustomProfile', pos)
print("loadCustomProfile from pos:", pos2)
if pos2 != -1:
    print(text[pos2-100:pos2+300])
else:
    print(text[pos+1000:pos+3000])

