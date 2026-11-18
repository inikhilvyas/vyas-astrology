with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'vIndexVal' in l or 'initDailyDashboard' in l or 'TODAY\'S TARA' in l:
        print(f'{i+1}: {l.strip()[:140]}')
