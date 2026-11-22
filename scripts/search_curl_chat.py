with open('api/ai_chat.php', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'curl' in l.lower() or 'groq' in l.lower() or 'api.groq.com' in l:
        print(f"{i+1}: {l.strip()[:100]}")

