with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {')
idx2 = text.find('return {', idx + 2000)
print("Final general return at", idx2)
print(text[idx2:idx2+1500])

