for fn in ['index.html', 'mobile/index.html']:
    with open(fn, 'r', encoding='utf-8') as f:
        text = f.read()
    import re
    matches = [m.start() for m in re.finditer(r'localStorage\.removeItem', text)]
    print(f"=== {fn}: {len(matches)} removeItem occurrences ===")
    for m in matches:
        print(" ", text[m-50:m+150].strip().replace('\n', ' '))
