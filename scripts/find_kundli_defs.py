with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(')
# search where computeMathematicalKundli is defined as a method
pos_def = text.find('computeMathematicalKundli(')
pos_def = text.find('computeMathematicalKundli(', pos_def + 30)
while pos_def != -1:
    print(f"Pos {pos_def}:")
    print(text[pos_def-50:pos_def+500])
    print("-"*40)
    pos_def = text.find('computeMathematicalKundli(', pos_def + 30)

