with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx, l in enumerate(lines):
    if 'googleUser' in l or 'googleSignIn' in l or 'GOOGLE_CLIENT_ID' in l:
        print(f'{idx+1}: {l.strip()[:110]}')

