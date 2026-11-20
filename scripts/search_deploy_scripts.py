import os

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.gemini' in root or 'books' in root:
        continue
    for f in files:
        if 'deploy' in f.lower() or 'hook' in f.lower() or 'hostinger' in f.lower():
            print(os.path.join(root, f))

