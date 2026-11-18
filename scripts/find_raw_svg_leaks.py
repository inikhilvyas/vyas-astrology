with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'v-icon v-globe' in l or 'langSwitch' in l or 'v-icon v-spark' in l or '4 24" width="15"' in l:
        print(f'{i+1}: {l.strip()[:150]}')
