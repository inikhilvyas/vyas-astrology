with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
modals = re.findall(r'<div[^>]+id=["\']([^"\']*modal[^"\']*)["\']', text, re.I)
print('Modals found:', modals)

# Search for openNewKundli or similar
matches = re.findall(r'(\w+NewKundli\w*|\w+NewChart\w*|\w+BirthModal\w*)', text)
print('Function matches:', set(matches))

# Search for 'नई कुण्डली' click
for m in re.finditer(r'नई कुण्डली', text):
    start = max(0, m.start() - 150)
    end = min(len(text), m.end() + 150)
    print("Match around 'नई कुण्डली':\n", text[start:end], "\n---")

