import glob

for p in glob.glob('scripts/*.py'):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        cnt = f.read()
        if ' D9' in cnt or 'd9' in cnt:
            if 'guru D9' in cnt or 'गुरु D9' in cnt or 'D9' in cnt:
                for line in cnt.splitlines():
                    if 'गुरु D9' in line or ' D9' in line:
                        print(p, line[:100])

