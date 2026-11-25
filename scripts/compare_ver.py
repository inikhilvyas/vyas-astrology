import os, re

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root:
        continue
    for f in files:
        if f.endswith(('.py', '.sh', '.bat', '.ps1', '.json', '.txt', '.md')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    c = fp.read()
                    if 'webhook' in c.lower() or 'deploy' in c.lower() and 'hostinger' in c.lower():
                        matches = re.findall(r'https?://[^\s\'"<>]+webhook[^\s\'"<>]*', c, re.IGNORECASE)
                        if matches:
                            print(f"{p}: {matches}")
            except Exception:
                pass
