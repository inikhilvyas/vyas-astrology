with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(8990, min(9030, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')

