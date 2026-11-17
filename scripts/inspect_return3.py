with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('BHAVA_TITLES')
pos_ret = text.find('return {', pos)
print(text[pos_ret:pos_ret+1200])

