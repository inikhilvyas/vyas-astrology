with open('src/vyas/ephem.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def sidereal_lon(')
print(text[pos:pos+1500])

