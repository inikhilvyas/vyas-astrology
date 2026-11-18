with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'loadStoredProfile' in l:
        for j in range(i, min(i+70, len(lines))):
            print(f'{j+1}: {lines[j].strip()}')
        break

