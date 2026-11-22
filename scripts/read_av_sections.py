with open('ashtakavarga/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("Total lines in ashtakavarga/index.html:", len(lines))
for i, l in enumerate(lines):
    if '<section' in l or '<h2' in l or '<h3' in l or 'id="' in l and ('Wrap' in l or 'Box' in l or 'Content' in l or 'table' in l.lower()):
        print(f"{i+1}: {l.strip()[:100]}")

