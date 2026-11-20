with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== 10930-10960 ===")
for i in range(10930, 10960):
    print(f"{i+1}: {lines[i]}", end='')

print("=== 11255-11285 ===")
for i in range(11255, 11285):
    print(f"{i+1}: {lines[i]}", end='')

