with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = 611069
# find where computeMathematicalKundli ends
# look for return { profile:
idx_ret = content.find('profile:', idx + 10000)
print('profile: found at:', idx_ret)
print(content[idx_ret-100:idx_ret+1200])

