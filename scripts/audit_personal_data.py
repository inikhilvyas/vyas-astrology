import os

for fname in ['index.html', 'mobile/index.html']:
    with open(fname, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    print('==============================')
    print('FILE:', fname, f'({len(lines)} lines)')
    print('==============================')
    for i, line in enumerate(lines):
        for needle in ['1984', 'Nikhil', 'निखिल', 'founder', 'Pali', 'पाली']:
            if needle in line:
                if 'option value="pali"' in line or 'id: "pali"' in line:
                    continue
                print(f'{i+1}: [{needle}] {line.strip()[:110]}')
                break
