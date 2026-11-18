with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'renderPanchang' in l or 'अभिजित' in l or 'abhijit' in l.lower():
        print(f'{i+1}: {l.strip()[:140]}')
