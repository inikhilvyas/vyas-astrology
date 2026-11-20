with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Lines around 8331:")
for i in range(max(0, 8320), min(len(lines), 8345)):
    print(f"{i+1}: {repr(lines[i])}")

