with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('computeMathematicalKundli(name, dobStr')
# search for charts = or return { inside computeMathematicalKundli
p = text.find('charts: {', pos + 3000)
print(text[p-200:p+1200])

