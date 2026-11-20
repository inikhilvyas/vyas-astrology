with open('admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("admin.html length:", len(text))
pos = text.find('id="')
print("Sample content from admin.html:")
print(text[:1200])

