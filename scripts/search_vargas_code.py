with open('js/vyas_astronomical_engine.js', 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'calcVargaSign' in l or 'varga' in l.lower() and 'function' in l:
        print(f"{i+1}: {l.strip()[:100]}")
    if 'D60' in l or 'D-60' in l or 'shashtiamsha' in l.lower() or 'nadiamsha' in l.lower():
        print(f"{i+1}: {l.strip()[:100]}")

