with open('js/vyas_sutras_bank.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'matchChart' in l or 'searchSutras' in l or 'VyasSutrasBank =' in l:
        print(f"{i+1}: {l.strip()[:100]}")

