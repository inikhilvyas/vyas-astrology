with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('google.accounts.id.prompt')
print("google.accounts.id.prompt found at", pos)

