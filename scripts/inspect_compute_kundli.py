with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = text.find('computeMathematicalKundli(')
print(f"computeMathematicalKundli found at {m}")
print(text[m:m+5000])
