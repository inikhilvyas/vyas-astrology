with open('js/vyas_daivagya_engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'VyasAshtakavargaEngine' in l:
        print(f"Line {i+1}: {l.strip()}")
        print("".join(lines[i:i+60]))
        break

