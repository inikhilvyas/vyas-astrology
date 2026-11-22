import urllib.request
import time

urls = [
    'https://vyasastro.in/?v=' + str(int(time.time())),
    'https://vyasastro.in/kundli-matching/?v=' + str(int(time.time())),
    'https://vyasastro.in/mobile/?v=' + str(int(time.time()))
]

forbidden = ['9414121172', 'vyasbilawas', '1984-11-23', 'निखिल']

for u in urls:
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8', errors='ignore')
            found = [f for f in forbidden if f in body]
            print(f"{u.split('?')[0]} -> Leaks found: {found} (Length: {len(body)})")
    except Exception as e:
        print(f"{u} -> Error: {e}")

