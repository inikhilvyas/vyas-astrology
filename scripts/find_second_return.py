with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {')
idx2 = text.find('return {', idx + 10000)
print("Second return at", idx2)
if idx2 != -1:
    print(text[idx2:idx2+1500])

