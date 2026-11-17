with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('return {')
# find return inside computeMathematicalKundli
pos_cm = text.find('computeMathematicalKundli(')
pos_ret = text.find('return {', pos_cm + 2500)
print(text[pos_ret:pos_ret+1500])
