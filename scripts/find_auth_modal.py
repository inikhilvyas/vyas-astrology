with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find modal for google login or auth
pos = text.find('modalGoogleAuth')
if pos == -1:
    pos = text.find('modalGoogleLogin')
if pos == -1:
    pos = text.find('Google Login')

print("Found at:", pos)
if pos != -1:
    print(text[pos-200:pos+1500])

# Also search for '1-Click' or 'एक-क्लिक' or 'निखिल व्यास' in buttons or HTML
for m in re.finditer(r'1-Click|1-क्लिक|एक-क्लिक|Quick Login', text, re.I):
    st = max(0, m.start()-100)
    en = min(len(text), m.end()+200)
    print("Match 1-click at", m.start(), ":\n", text[st:en])

