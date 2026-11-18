with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(7665, min(7720, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')

