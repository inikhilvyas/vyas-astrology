with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['chat.php', 'sendChatMessage', 'askSage', 'askDaivagya', 'groq', 'chatMessageInput']):
        if len(l.strip()) < 120:
            print(f"{i+1}: {l.strip()}")

