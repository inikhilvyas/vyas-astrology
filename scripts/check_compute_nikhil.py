with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(name, dobStr')
pos2 = text.find('1984-11-23', pos)
print("pos2:", pos2)
if pos2 != -1:
    print(text[pos2-100:pos2+600])
else:
    print("1984-11-23 not found in computeMathematicalKundli")

