with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(8700, 8760):
    if i < len(lines):
        print(f"L{i+1}: {lines[i]}", end='')

