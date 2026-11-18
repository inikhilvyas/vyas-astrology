with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== LINES 7640-7670 ===")
for i in range(7635, min(7675, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')

print("\n=== LINES 8758-8830 ===")
for i in range(8755, min(8830, len(lines))):
    print(f'{i+1}: {lines[i].strip()}')
