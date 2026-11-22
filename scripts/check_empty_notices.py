for p in ['ashtakavarga/index.html', 'varshphal/index.html', 'nadi-astrology/index.html']:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f"=== {p} ===")
    import re
    m = re.search(r'function showEmptyKundliNotice\(\) \{[\s\S]*?\}', c)
    if m:
        print(m.group(0))
    else:
        print("Not found!")

