with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(name, dobStr')
# search for charts: { inside computeMathematicalKundli
p = text.find('d1: {', pos)
print(text[p-50:p+1200])

