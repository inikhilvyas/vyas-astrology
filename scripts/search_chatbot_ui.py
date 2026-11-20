with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = [m.start() for m in re.finditer(r'आचार्य व्यास • वैदिक AI परामर्श|ai-chat-column|chatbot-card|modalChatbot', content)]
print(f"Chatbot matches count: {len(matches)}")
for m in matches:
    print(f"Match at {m}:")
    print(content[max(0, m-80):min(len(content), m+200)])
    print('='*40)

