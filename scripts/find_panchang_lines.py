with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'renderPanchang: function' in l:
        print(f"renderPanchang starts at line {i+1}")
        for j in range(i, i+160):
            if j < len(lines):
                if lines[j].strip().startswith('init') or lines[j].strip().startswith('render'):
                    print(f"   L{j+1}: {lines[j].strip()[:60]}")
        break

