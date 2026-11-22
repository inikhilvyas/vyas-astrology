with open('js/vyas_daivagya_engine.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'VyasSutrasBank' in l or 'sutrasBank' in l.lower() or 'searchSutras' in l:
        print(f"{i+1}: {l.strip()[:100]}")

