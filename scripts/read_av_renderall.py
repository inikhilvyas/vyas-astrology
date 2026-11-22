with open('ashtakavarga/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(740, min(800, len(lines))):
    print(f"{i+1}: {lines[i].strip()}")
