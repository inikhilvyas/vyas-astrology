with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Last 2000 chars of index.html:")
print(text[-2000:])

