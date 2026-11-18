with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('generateDiamondSVG(housesData, size, title)')
print(text[pos+800:pos+3500])

