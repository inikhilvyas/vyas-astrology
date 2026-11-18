with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = text.find('return {\n                profile: {')
if m == -1:
    m = text.find('return {')
    while m != -1 and 'profile: {' not in text[m:m+50]:
        m = text.find('return {', m+1)
print(f"return block at {m}")
print(text[m:m+2500])

