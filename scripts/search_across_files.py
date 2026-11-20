import os

search_terms = ['गुरु D9', 'मंगल D9', 'D9 कुण्डली', 'd9']
found = []
for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'venv' in root:
        continue
    for f in files:
        if f.endswith(('.js', '.json', '.php', '.html', '.ts', '.py')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    cnt = fl.read()
                    for st in ['गुरु D9', 'मंगल D9', 'D9']:
                        if st in cnt:
                            found.append((p, st))
                            break
            except Exception as e:
                pass

print(f"Found {len(found)} files:")
for p, st in found[:20]:
    print(p, st)

