with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(6660, 6720):
    print(f"{i+1}: {lines[i]}", end='')

