import os

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'books' in root:
        continue
    for f in files:
        if f.endswith(('.php', '.js', '.py', '.json', '.html')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    content = fl.read()
                    if 'गुरु D9' in content or 'शुक्र D9' in content:
                        print(f"FOUND IN: {p}")
            except Exception as e:
                pass
print("Done searching.")

