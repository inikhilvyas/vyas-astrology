with open('src/vyas/ephem.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in ephem.py: {len(lines)}")
for i, l in enumerate(lines[:120]):
    print(f"L{i+1}: {l}", end='')

