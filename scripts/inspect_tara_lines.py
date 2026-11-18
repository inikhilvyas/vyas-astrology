with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(7575, min(7645, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')
