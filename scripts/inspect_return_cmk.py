with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 611069
idx_ret = content.find('return {', idx)
print(content[idx_ret:idx_ret+2000])

