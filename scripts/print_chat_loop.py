with open('api/ai_chat.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i in range(540, min(575, len(lines))):
    print(f"{i+1}: {repr(lines[i])}")

