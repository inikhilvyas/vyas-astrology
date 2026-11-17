with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos_cm = text.find('computeMathematicalKundli(')
pos_ret = text.find('return {', pos_cm + 5000)
print(text[pos_ret:pos_ret+1200])

