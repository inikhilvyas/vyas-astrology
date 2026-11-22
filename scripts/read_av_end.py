with open('js/vyas_daivagya_engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2380, min(2460, len(lines))):
    print(f"{i+1}: {lines[i].strip()}")

