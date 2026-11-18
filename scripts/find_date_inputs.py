with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<input[^>]*type="date"[^>]*>', text)
print("Date inputs:")
for m in matches:
    print(m)

# Find where date input value is set in js
matches2 = re.findall(r'\.value\s*=\s*[^;\n]*date[^;\n]*', text, re.I)
print("\nJS date value sets:")
for m in matches2:
    print(m)

