import os

for f in os.listdir('scripts'):
    p = os.path.join('scripts', f)
    if os.path.isfile(p):
        with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
            c = fl.read()
            if 'ftp' in c.lower() or 'hostinger' in c.lower() or 'webhook' in c.lower() or 'git push' in c.lower():
                print(f, "mentions deployment keywords")

