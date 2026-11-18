with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(8885, min(8930, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')

