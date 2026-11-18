with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(7760, min(7830, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')

