import os

results = []
for root, dirs, files in os.walk('.'):
    if any(ex in root for ex in ['.git', 'node_modules', '.gemini', 'books', '.venv', '.venv311']):
        continue
    for f in files:
        if any(k in f.lower() for k in ['tele', 'bot', 'tlg', 'chat']):
            results.append(os.path.join(root, f))
        elif f.endswith(('.py', '.json', '.php', '.env', '.bat', '.sh', '.js')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                    c = fl.read()
                    if 'telegram' in c.lower() or 't.me' in c.lower() or 'bot_token' in c.lower():
                        results.append(p)
            except Exception:
                pass

print(f"Found {len(results)} potential files:")
for r in sorted(list(set(results))):
    print(" ", r)

