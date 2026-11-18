with open('mobile/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1040, min(1130, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')
