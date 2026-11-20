import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

matches = re.findall(r'id=[\"\'](modal[a-zA-Z0-9_]*)[\"\']', text)
print("Modals found:", set(matches))

