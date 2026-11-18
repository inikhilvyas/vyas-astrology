with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = 0
found = []
target = '4 24" width="15"'
while True:
    pos = text.find(target, pos)
    if pos == -1:
        break
    found.append(pos)
    pos += len(target)

print(f"Found {len(found)} occurrences of target:")
for p in found:
    print(f"Pos {p}:")
    print(text[p-50:p+120])
    print("-" * 50)

