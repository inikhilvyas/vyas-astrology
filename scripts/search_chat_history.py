with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for m in re.finditer(r'chatHistory|chat_history|askVyasAI|aiChatMessages|aiChatInput', text):
    st = max(0, m.start()-60)
    en = min(len(text), m.end()+120)
    print("Match at", m.start(), ":\n", text[st:en].replace('\n', ' '))
    print("-" * 50)

