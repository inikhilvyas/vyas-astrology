import re

for fname in ['index.html', 'mobile/index.html', 'jaimini-astrology/index.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f'=== {fname} ===')
    for m in re.finditer(r'<input[^>]+>', text):
        tag = m.group(0)
        if 'date' in tag.lower() or 'name' in tag.lower() or 'value=' in tag.lower():
            line_no = text[:m.start()].count('\n') + 1
            print(f'Line {line_no}: {tag}')
