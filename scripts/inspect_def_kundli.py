with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = text.find('computeMathematicalKundli(name, dobStr')
if m == -1:
    m = text.find('computeMathematicalKundli(name')
print(f"definition found at {m}")
print(text[m:m+5000])

