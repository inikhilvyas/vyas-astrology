with open('api/ai_chat.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i in range(535, min(615, len(lines))):
    print(f"{i+1}: {lines[i].strip()[:100]}")

