with open('api/ai_chat.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i in range(25, min(140, len(lines))):
    print(f"{i+1}: {lines[i].strip()[:100]}")

