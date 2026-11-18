with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(7674, min(7750, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')
