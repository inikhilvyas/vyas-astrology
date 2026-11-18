with open('src/vyas/ephem.py', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('def ayanamsa_deg(')
print(text[pos:pos+600])

