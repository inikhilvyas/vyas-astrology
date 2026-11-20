with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('window.VyasAIEngine.chatHistory.push')
if pos != -1:
    print(text[pos-200:pos+1000])

import re
matches = re.findall(r'id=["\'][^"\']*chat[^"\']*["\']', text, re.I)
print("Chat element IDs:", matches)

