with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(12200, min(12235, len(lines))):
    print(f'{i+1}: {lines[i].strip()[:90]}')

