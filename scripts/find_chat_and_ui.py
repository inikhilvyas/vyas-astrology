with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

# Find AI concierge / chat modal in index.html
print("=== CHAT MODAL / AI CONCIERGE SEARCH ===")
for m in re.finditer(r'<div[^>]+id=["\'](?:ai|chat|concierge)[^"\']*["\']', text, re.IGNORECASE):
    idx = m.start()
    print(text[idx:idx+400])
    print("-" * 50)

# Find where chat messages are sent in script
print("=== SCRIPT CHAT SEARCH ===")
for m in re.finditer(r'(?:fetch|XMLHttpRequest|\.post)\([^\)]*(?:chat|ask|ai|api)[^\)]*\)', text, re.IGNORECASE):
    idx = m.start()
    print(text[max(0, idx-100):min(len(text), idx+300)])
    print("-" * 50)

