with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('computeMathematicalKundli(name, dobStr, tobStr, cityStr, gender, customLat, customLon) {')
idx2 = text.find('return {', idx + 1000)
print("Return statement for general users found at", idx2)
print(text[idx2:idx2+2000])

