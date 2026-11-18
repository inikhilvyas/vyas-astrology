import os

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('Length of index.html:', len(text))
queries = [
    'v-icon v-globe',
    '4 24" width="15"',
    'VYAS DAY INDEX',
    'Sampat (सम्पत तारा',
    '11:58',
    'langSwitch',
    'toggleLanguage',
    'd4af37'
]

for q in queries:
    count = text.count(q)
    pos = text.find(q)
    print(f"'{q}': count={count}, first_pos={pos}")
    if count > 0 and count <= 5:
        # print snippet
        start = max(0, pos - 100)
        end = min(len(text), pos + 200)
        print(f"   Snippet for {q}:\n{text[start:end]}\n" + "-"*40)
