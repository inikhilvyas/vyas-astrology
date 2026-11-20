with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('inspectPlanet: function')
if pos == -1:
    pos = text.find('inspectPlanet(')

print("inspectPlanet pos:", pos)
if pos != -1:
    print(text[pos-50:pos+2500])

