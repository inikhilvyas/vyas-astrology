with open('nadi-astrology/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'loadAndRenderNadi' in l or 'activeChart' in l:
        print(f"{i+1}: {l.strip()[:100]}")
