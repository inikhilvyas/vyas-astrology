import os, re

keywords = ['संस्थापक', '1click', '1-click', 'quickLogin', 'nikhilvyas']
results = {k: [] for k in keywords}

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '__pycache__' in root or 'books' in root:
        continue
    for f in files:
        if f.endswith(('.html', '.js', '.py', '.json', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                for k in keywords:
                    for m in re.finditer(re.escape(k), content, re.I):
                        st = max(0, m.start()-60)
                        en = min(len(content), m.end()+60)
                        results[k].append((p, m.start(), content[st:en].replace('\n', ' ')))
            except Exception:
                pass

for k, matches in results.items():
    print(f"=== Keyword: {k} (Total: {len(matches)}) ===")
    for p, idx, snippet in matches[:10]:
        print(f"  {p}:{idx} -> {snippet}")

